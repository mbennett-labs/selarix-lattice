#!/usr/bin/env python3
"""
==============================================================================
reporter_morning_digest.py — SELARIX Lattice Reporter v1
==============================================================================
Kind: script
Status: active (v1 — pure templating, no LLM)
What it does: Reads all project status files in the lattice repo, composes a
              four-section morning digest, pipes it to telegram_send.sh for
              delivery to Mike's SELARIX Board channel.
When to use it: Via cron `0 11 * * *` (= 7 AM EST during DST). Manual invocation
                for testing: `python3 reporter_morning_digest.py [--dry-run]`
When not to use it: Do not run more than once per morning — Mike's digest is a
                    single daily event. Multiple invocations will spam the
                    channel.
Dependencies: Python 3.8+, git (for `git pull` preflight), jq (via telegram_send.sh)
              Env file: /home/selarix/.selarix.env
              Lattice repo: /home/selarix/lattice (git clone of selarix-lattice)
Model compatibility: v1 = no model. v1.1 will add optional DeepSeek rewrite pass.
Last updated: 2026-04-24 by Claude + Mike
==============================================================================
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import logging
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

# --- Config ---------------------------------------------------------------

LATTICE_ROOT = Path(os.environ.get("LATTICE_ROOT", "/home/selarix/lattice"))
TELEGRAM_ADAPTER = Path(
    os.environ.get(
        "TELEGRAM_ADAPTER",
        str(LATTICE_ROOT / "toolshed" / "adapters" / "telegram_send.sh"),
    )
)
LOG_DIR = Path(os.environ.get("REPORTER_LOG_DIR", "/var/log/selarix/reporter"))

# Staleness thresholds
STALE_HOURS = 48        # project flagged stale if latest status older than this
UNACKED_HOURS = 24      # inbox directive flagged if unprocessed longer than this

# Digest constraints
MAX_NEEDS_ITEMS = 5
MAX_CLEAN_ITEMS = 8
MAX_ONDECK_ITEMS = 3
MAX_DIGEST_WORDS = 400  # soft ceiling; warn but don't truncate

# --- Logging --------------------------------------------------------------

LOG_DIR.mkdir(parents=True, exist_ok=True)
TODAY = dt.date.today().isoformat()
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / f"{TODAY}.log"),
        logging.StreamHandler(sys.stdout),
    ],
)
log = logging.getLogger("reporter")


# --- Git preflight --------------------------------------------------------

def git_pull_lattice() -> bool:
    """Pull latest lattice repo state. Return True on success, False if we'll
    run against cached state instead. Never fatal — Reporter must always ship."""
    try:
        result = subprocess.run(
            ["git", "-C", str(LATTICE_ROOT), "pull", "--ff-only", "origin", "main"],
            capture_output=True, text=True, timeout=30,
        )
        if result.returncode == 0:
            log.info("git pull OK")
            return True
        log.warning("git pull non-zero exit: %s", result.stderr.strip())
        return False
    except Exception as e:
        log.warning("git pull exception: %s", e)
        return False


# --- Project discovery & status reading -----------------------------------

def discover_projects() -> list[Path]:
    """Find all project directories with a manifest.json."""
    projects_dir = LATTICE_ROOT / "projects"
    if not projects_dir.is_dir():
        log.error("projects dir not found at %s", projects_dir)
        return []
    return sorted(p for p in projects_dir.iterdir() if p.is_dir() and (p / "manifest.json").is_file())


def load_manifest(project_dir: Path) -> dict[str, Any]:
    try:
        return json.loads((project_dir / "manifest.json").read_text())
    except Exception as e:
        log.warning("failed to load manifest for %s: %s", project_dir.name, e)
        return {"project_name": project_dir.name, "mode": "unknown"}


def latest_status(project_dir: Path) -> tuple[dict[str, Any] | None, dt.date | None]:
    """Return (status_dict, status_date) — the most recent status file, or (None, None)."""
    status_dir = project_dir / "status"
    if not status_dir.is_dir():
        return None, None
    candidates = sorted(status_dir.glob("*.json"), reverse=True)
    for path in candidates:
        try:
            data = json.loads(path.read_text())
            date_str = data.get("date") or path.stem
            return data, dt.date.fromisoformat(date_str)
        except Exception as e:
            log.warning("skipping malformed status file %s: %s", path, e)
            continue
    return None, None


def unprocessed_inbox(project_dir: Path) -> list[dict[str, Any]]:
    """Return directives that have not been moved to /inbox/processed/ and are
    older than UNACKED_HOURS."""
    inbox = project_dir / "inbox"
    if not inbox.is_dir():
        return []
    now = dt.datetime.now(dt.timezone.utc)
    unacked = []
    for path in inbox.glob("*.json"):
        try:
            data = json.loads(path.read_text())
            ts = dt.datetime.fromisoformat(data["timestamp"].replace("Z", "+00:00"))
            age_hours = (now - ts).total_seconds() / 3600
            if age_hours > UNACKED_HOURS:
                unacked.append(data)
        except Exception as e:
            log.warning("skipping malformed inbox file %s: %s", path, e)
    return unacked


# --- Digest composition ---------------------------------------------------

def collect_project_state() -> list[dict[str, Any]]:
    """Build a list of per-project state dicts for digest composition."""
    today = dt.date.today()
    state = []
    for project_dir in discover_projects():
        manifest = load_manifest(project_dir)
        status, status_date = latest_status(project_dir)
        is_stale = False
        if status_date is None:
            is_stale = True
            age_days = None
        else:
            age_days = (today - status_date).days
            if age_days * 24 > STALE_HOURS:
                is_stale = True
        state.append({
            "name": manifest.get("project_name", project_dir.name),
            "mode": manifest.get("mode", "unknown"),
            "priority": manifest.get("priority", "medium"),
            "status": status or {},
            "status_date": status_date,
            "age_days": age_days,
            "is_stale": is_stale,
            "unacked_directives": unprocessed_inbox(project_dir),
        })
    return state


def build_needs_today(state: list[dict[str, Any]]) -> list[str]:
    """Aggregate across projects: blocked items + unacked inbox + stale flags."""
    items: list[tuple[int, str]] = []  # (priority_rank, line)
    for proj in state:
        # Low-power and paused projects don't block Mike
        if proj["mode"] in ("low-power", "paused"):
            continue

        # Blocked items (project-declared)
        for blocker in proj["status"].get("blocked", []):
            severity = blocker.get("severity", "medium")
            rank = {"high": 0, "medium": 1, "low": 2}.get(severity, 1)
            needs = blocker.get("needs", "action")
            issue = blocker.get("issue", "unspecified blocker")
            items.append((rank, f"• [{proj['name']}] {issue} — {needs}"))

        # Board flags (project escalations)
        for flag in proj["status"].get("flags_for_board", []):
            items.append((0, f"• [{proj['name']}] {flag}"))

        # Stale project (active mode, no recent status)
        if proj["is_stale"] and proj["mode"] in ("build", "maintain"):
            age_str = f"{proj['age_days']}d" if proj["age_days"] is not None else "never reported"
            items.append((0, f"• [{proj['name']}] stale — last status {age_str}"))

        # Unacked directives
        for directive in proj["unacked_directives"]:
            cmd = directive.get("command", "note")
            content = directive.get("content", "")[:80]
            items.append((0, f"• [{proj['name']}] unacked directive: {cmd} — {content}"))

    items.sort(key=lambda x: x[0])
    return [line for _, line in items[:MAX_NEEDS_ITEMS]]


def build_running_clean(state: list[dict[str, Any]]) -> list[str]:
    """One-line health confirmations per project."""
    lines: list[str] = []
    for proj in state:
        name = proj["name"]
        mode = proj["mode"]
        status = proj["status"]

        if proj["is_stale"]:
            continue  # stale handled in Needs-you-today, don't double-list

        # Custom one-liners based on project mode and health signals
        health = status.get("health_signals", {})
        uptime = health.get("uptime_pct")
        errors = health.get("agent_errors", 0)

        if mode == "low-power":
            suffix = "low-power, no action needed"
        elif uptime is not None and errors == 0:
            suffix = f"uptime {uptime:.0f}%, 0 errors"
        elif errors == 0:
            suffix = "healthy"
        else:
            continue  # if there are errors, it's not "running clean"

        lines.append(f"• {name} — {suffix}")
        if len(lines) >= MAX_CLEAN_ITEMS:
            break

    if not lines:
        lines.append("• (no healthy-signal projects reporting)")
    return lines


def build_momentum(state: list[dict[str, Any]]) -> str:
    """2–3 lines: what shipped, what revenue came in, direction."""
    completed_count = 0
    revenue_total_usd = 0.0
    revenue_types: set[str] = set()

    for proj in state:
        status = proj["status"]
        completed_count += len(status.get("completed", []))
        for ev in status.get("revenue_events", []):
            amount = ev.get("amount_usd", 0.0)
            try:
                revenue_total_usd += float(amount)
            except (TypeError, ValueError):
                pass
            if ev.get("type"):
                revenue_types.add(ev["type"])

    lines: list[str] = []
    if completed_count > 0:
        lines.append(f"Shipped {completed_count} task{'s' if completed_count != 1 else ''} across active projects since last digest.")
    if revenue_total_usd > 0:
        types_str = ", ".join(sorted(revenue_types)) if revenue_types else "mixed"
        lines.append(f"Revenue events: ${revenue_total_usd:.2f} ({types_str}).")
    if not lines:
        lines.append("Flat since last digest. Reporter loop is the new movement.")
    return "\n".join(lines)


def build_on_deck(state: list[dict[str, Any]]) -> list[str]:
    """What's proposed next. Pulled from `in_progress` with soonest ETAs."""
    items: list[tuple[str, str]] = []  # (eta, line)
    for proj in state:
        for task in proj["status"].get("in_progress", []):
            agent = task.get("agent", "pool")
            desc = task.get("task", "unspecified")
            eta = task.get("eta", "tbd")
            items.append((eta, f"→ [{proj['name']}] {desc} ({agent}, eta {eta})"))

    items.sort(key=lambda x: x[0])  # lexicographic sort works for ISO dates
    return [line for _, line in items[:MAX_ONDECK_ITEMS]]


def compose_digest(state: list[dict[str, Any]], git_pull_ok: bool) -> str:
    """Assemble the four-section digest."""
    today_human = dt.date.today().strftime("%a %b %d")
    header = f"*SELARIX Board — {today_human}*"
    if not git_pull_ok:
        header += "\n_⚠️ git pull failed; running from cached state_"

    needs = build_needs_today(state)
    clean = build_running_clean(state)
    momentum = build_momentum(state)
    ondeck = build_on_deck(state)

    parts = [header]

    parts.append("\n🚨 *Needs you today*")
    if needs:
        parts.extend(needs)
    else:
        parts.append("Nothing blocking. Good morning.")

    parts.append("\n✅ *Running clean*")
    parts.extend(clean)

    parts.append("\n📈 *This week's momentum*")
    parts.append(momentum)

    parts.append("\n🎯 *On deck*")
    if ondeck:
        parts.extend(ondeck)
    else:
        parts.append("→ (nothing in-progress — queue is empty)")

    parts.append("\n_Reply with \"go [number]\" to approve, or free-form to redirect. (v1 does not auto-parse replies; v1.5 will.)_")

    digest = "\n".join(parts)

    # Soft-check word count
    word_count = len(digest.split())
    if word_count > MAX_DIGEST_WORDS:
        log.warning("digest is %d words (ceiling %d) — consider trimming", word_count, MAX_DIGEST_WORDS)
    else:
        log.info("digest word count: %d", word_count)

    return digest


# --- Telegram delivery ----------------------------------------------------

def send_to_telegram(digest: str) -> bool:
    if not TELEGRAM_ADAPTER.exists():
        log.error("telegram adapter not found at %s", TELEGRAM_ADAPTER)
        return False
    try:
        result = subprocess.run(
            ["bash", str(TELEGRAM_ADAPTER)],
            input=digest, text=True, capture_output=True, timeout=15,
        )
        if result.returncode != 0:
            log.error("telegram_send.sh exit=%d stderr=%s", result.returncode, result.stderr.strip())
            return False
        log.info("telegram send OK: %s", result.stdout.strip())
        return True
    except Exception as e:
        log.error("telegram send exception: %s", e)
        return False


# --- Main -----------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(description="SELARIX Reporter v1 — morning digest")
    parser.add_argument("--dry-run", action="store_true",
                        help="Compose digest and print to stdout; do not send to Telegram")
    parser.add_argument("--no-pull", action="store_true",
                        help="Skip git pull (for local testing)")
    args = parser.parse_args()

    log.info("=== Reporter v1 run start ===")
    log.info("lattice_root=%s", LATTICE_ROOT)

    git_pull_ok = True if args.no_pull else git_pull_lattice()

    state = collect_project_state()
    log.info("discovered %d project(s)", len(state))
    for proj in state:
        log.info("  %s [%s] stale=%s age=%s",
                 proj["name"], proj["mode"], proj["is_stale"], proj["age_days"])

    digest = compose_digest(state, git_pull_ok)

    if args.dry_run:
        print("--- DIGEST (dry run) ---")
        print(digest)
        print("--- END ---")
        return 0

    # Always write the digest to disk before sending, so we have a record even
    # if Telegram send fails.
    snapshot_path = LOG_DIR / f"{TODAY}.txt"
    snapshot_path.write_text(digest)
    log.info("digest snapshot written to %s", snapshot_path)

    if not send_to_telegram(digest):
        log.error("telegram send failed — digest saved but not delivered")
        return 1

    log.info("=== Reporter v1 run complete ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
