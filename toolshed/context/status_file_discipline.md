# Status File Discipline

**Kind:** context
**Status:** active
**What it does:** Defines what each field in `/projects/{project}/status/YYYY-MM-DD.json` means and where different kinds of content belong.
**When to use it:** Every time a worker agent, CEO, or human writes a status file for a project in the SELARIX Lattice.
**When not to use it:** n/a — this is canonical. If a field's meaning needs to change, update this doc, don't ignore it.
**Dependencies:** `/contract/status_schema.json`
**Model compatibility:** all
**Last updated:** 2026-04-24 by Claude + Mike

---

## The root cause this doc exists to prevent

The Reporter's first live run (2026-04-24) surfaced a data-discipline problem: the `flags_for_board` array was being used as a dumping ground for "things the Board should know" — completed research findings, context summaries, project overviews — instead of what the schema actually means.

Result: the morning digest's "Needs you today" section was full of informational items that didn't need decisions. Mike couldn't tell signal from noise. That's a status-file-writing failure, not a Reporter failure.

**This doc is the fix.** Use it every time you write a status file.

---

## What each field means

### `completed`

**Definition:** Work that finished in the last 24 hours. Past tense. Done. Shippable, mergeable, live.

**Looks like:**
```json
{"agent": "Builder", "task": "Pushed site scaffold to mbennett-labs/thebinmap", "detail": "commit 7a3f2e1", "time": "2026-04-24T14:12:00Z"}
```

**NOT for:** research findings (those go in `/toolshed/candidates/` or a project doc), ideas (those go in `in_progress` or nowhere), plans (those go in a project doc, not status).

---

### `in_progress`

**Definition:** Work actively being done, with an ETA. Either a pool agent picked it up or a human queued it. If it has no owner and no ETA, it isn't in progress — it's a wish.

**Looks like:**
```json
{"agent": "Writer", "task": "First 10 TheBinMap city pages", "eta": "2026-04-27"}
```

**NOT for:** "someday maybe," "ideas we're exploring," or "things that would be nice." Those go in a project's design doc, not the status file.

---

### `blocked`

**Definition:** Something the project cannot move forward on without external input or a fix. A real obstacle, not a consideration.

**Looks like:**
```json
{"issue": "Google Places API key returns 403 on /places/", "needs": "2-min key scope check in GCP console", "severity": "medium"}
```

**Severity levels:**
- `high` = revenue blocked, downtime active, or customer-facing failure
- `medium` = dev work blocked, 1–2 day impact if not resolved
- `low` = annoying but not urgent, schedule for next week

**NOT for:** "we should probably consider X" (not blocked, just a thought) or "waiting on AdSense review" (that's `flags_for_board`, not a blocker, because the project is moving fine while waiting).

---

### `flags_for_board`

**Definition:** One-line items that **need Mike's decision, approval, or awareness** in the next 24 hours. Each item should be answerable with `go`, `kill`, `defer`, or a one-sentence note.

**Looks like:**
- `"AdSense approval pending, Day 9 of 28 — decide on Ezoic fallback if rejected"` ← needs Mike's awareness + future decision
- `"Polymarket paper trader hit 58% win rate, ready to discuss live USDC transition"` ← needs go/no-go
- `"Domain DNS for thebinmap.com still pointing to Hostinger default — approve switch to Cloudflare Pages?"` ← needs approval

**NOT for:**
- ❌ `"Market research: ~4000-6000 bin stores nationally, fragmented"` — this is *context*, not a decision
- ❌ `"Shopper app + owner SaaS are the monetization targets"` — this is a *plan*, not a decision
- ❌ `"TheBinMap needs repackaging to production repo"` — this is either `in_progress` (if being done) or `blocked` (if something is stopping it), not a flag

**The test:** Can Mike respond to this item with `go`, `kill`, `defer`, or `noted` and be done with it? If yes, it's a flag. If it's just information, put it elsewhere.

---

### `revenue_events`

**Definition:** Money came in, or a measurable revenue-like signal fired. Always with `amount_usd` and `type`.

**Looks like:**
```json
[
  {"type": "adsense_impression", "amount_usd": 0.03, "source": "therapistindex"},
  {"type": "acp_scan", "amount_usd": 0.49, "source": "crawdaddy"}
]
```

**Types worth tracking:** `adsense_impression`, `adsense_click`, `affiliate_click`, `affiliate_sale`, `acp_scan`, `paid_listing`, `subscription_charge`, `consulting_invoice_paid`.

**NOT for:** projected revenue, potential revenue, expected revenue. Only money that has actually moved or events that are directly measurable in production.

---

### `health_signals`

**Definition:** Ambient state of the project's infrastructure. Reporter uses this to populate the "Running clean" section.

**Looks like:**
```json
{"uptime_pct": 99.8, "agent_errors": 0, "last_deploy": "2026-04-23T09:30:00Z"}
```

**Fields Reporter reads:**
- `uptime_pct` (float, 0–100) — used in "Running clean" if no errors
- `agent_errors` (int, 0+) — if >0, project is NOT in "Running clean"

Additional fields (`last_deploy`, `disk_pct`, `queue_depth`, etc.) are fine to add; Reporter ignores what it doesn't know.

---

## Example — what a good status file looks like

```json
{
  "project_name": "therapistindex",
  "date": "2026-04-24",
  "completed": [
    {"agent": "Writer", "task": "Published 'Federal layoff therapy' blog post", "time": "2026-04-24T10:15:00Z"},
    {"agent": "Builder", "task": "Fixed /places/ page Maps API key scope", "time": "2026-04-24T14:40:00Z"}
  ],
  "in_progress": [
    {"agent": "Builder", "task": "Enrich 2,490 listings via Google Places API", "eta": "2026-04-27"}
  ],
  "blocked": [],
  "revenue_events": [],
  "flags_for_board": [
    "AdSense review Day 9 of 28 — confirm Ezoic fallback plan if rejected"
  ],
  "health_signals": {"uptime_pct": 100.0, "agent_errors": 0}
}
```

That produces a clean digest: one real decision in "Needs you today," two shipped items in "This week's momentum," real ETA in "On deck."

---

## Where research findings go (NOT in the status file)

Bin-store market research, competitor teardowns, niche scoring, API discovery — all of that is *context*, not status. It belongs in:

1. **`/toolshed/candidates/`** for tools or services being evaluated
2. **A project's own `/projects/{name}/docs/`** directory for project-specific research
3. **The GitHub repo's `/docs/`** for anything permanent and shared

The status file is **operational**, not archival. It describes what happened in the last 24 hours. Nothing else.

---

## Who writes status files

Today (2026-04-24): Mike + Claude sessions write status files manually when project state changes meaningfully.

Eventually: the project's assigned pool agents (Builder, Writer, Operator, etc.) write their own section of the status file at the end of each work cycle. The Coordinator merges them nightly. The Reporter reads whatever is most recent.

Until pool agents are live, **err on the side of writing too few status files, not too many**. A missing status file is fine (Reporter uses most-recent-available). A status file full of noise is worse — it pollutes the morning digest.

---

*Status file discipline v1 | SELARIX Lattice | 2026-04-24*
*If it needs a decision, it's a flag. If it needs an owner, it's in_progress. Otherwise it's context, and context doesn't belong in status.*
