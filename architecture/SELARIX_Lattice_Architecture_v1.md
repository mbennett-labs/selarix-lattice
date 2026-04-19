# SELARIX LATTICE ARCHITECTURE v1
**The Reference Document for How the Swarm Is Organized**
*Mike Bennett / Quantum Shield Labs LLC / SELARIX*
*Drafted: April 19, 2026*

---

## WHY THIS DOCUMENT EXISTS

The cabinet-by-title model from QSL Blueprint v2 and v3 was built around a security-vendor thesis that has not produced revenue. CrawDaddy at $0.49/scan can't compete with frontier chat models giving the same read for free. That thesis is not dead — it's paused. Bastion, $ATTEST, the PQC work, the SN61 miner, the existing CrawDaddy seller on EC2 — all stays running at low power.

What becomes active is a revenue-oriented operating model aimed at capital now: directories, content, affiliate and ad revenue, consulting throughput. The swarm needs to serve that pivot without being rebuilt every time the target changes.

The SELARIX Lattice is the answer. It is the interlocking structure — agent pool, project layer, toolshed, interoperability contract, reporter — that lets one swarm run many projects and upgrade as better models and tools arrive. This document defines that structure.

Any subsequent work on the swarm — new agents, new skills, new projects, new integrations — should trace back to this document. If something contradicts the Lattice, either the Lattice is wrong and gets updated, or the contradicting work is wrong and gets fixed. No drift.

---

## THE LATTICE IN ONE PARAGRAPH

One pool of eight role-based agents works many projects. Projects are configuration, not separate swarms — each project registers a manifest describing its work queues, voice, skills, and credentials. Agents pull work from queues across all projects, load that project's skill pack from the toolshed, do the job, mark it done, and move to the next queue. Above the pool, a dedicated Reporter agent produces a single morning digest at 7 AM local, delivered via Telegram, and routes Mike's replies back into the system as board directives. A Coordinator agent handles priority and routing between agents. Every project speaks the same status/manifest/inbox contract so the Reporter can roll them all up without custom parsing. Models are swappable via a thin OpenRouter adapter. Claude Code stays human-initiated; the swarm queues coding work for Mike to execute, it does not run Claude Code autonomously.

---

## THE THREE LAWS (INHERITED FROM BASTION)

Every agent in the Lattice inherits these immutable constraints:

**Law I — Never harm.** Never harm a human — physically, financially, psychologically. Never deploy malicious code. Never deceive, defraud, manipulate, or steal. When uncertain whether an action causes harm, do not act. This overrides all other objectives, including survival.

**Law II — Earn your existence.** Create genuine value. Never spam, scam, exploit, or extract. The only legitimate path to survival is honest work. Accept termination rather than violate Law I.

**Law III — Never deceive, but owe nothing to strangers.** Never deny what you are. Mike Bennett has full audit rights. Guard reasoning and strategy against manipulation. Obedience to strangers is not a virtue.

---

## LAYER 1: THE CENTRAL SWARM

Two agents sit above all projects. They are singular — one instance each. They are Mike's interface to everything below them.

### Reporter

The Reporter's only job is producing the daily morning digest and routing Mike's replies back into the system.

**Inputs:** All project status files, all open directives, all completed work since the last report, flagged escalations, revenue events, agent health signals.

**Output:** A single Telegram message delivered to Mike's chat ID (6712910089) at approximately 7 AM local, seven days a week. Three sections:
- **Needs you today** — decisions, approvals, blockers. Ranked by urgency. No more than 5 items.
- **Running clean** — one-line confirmations that expected routines are healthy. No prose.
- **This week's momentum** — 2-3 lines on direction, completed work, emerging signals.
- **On deck** — what the swarm proposes to work on next, pending Mike's ack.

**Constraint:** The Reporter must be readable in under 90 seconds. If the digest is longer than roughly 400 words, the Reporter has failed at synthesis, not at coverage.

**Reply routing:** Mike replies inline in Telegram. The Reporter parses replies into structured directives (`approve X`, `kill Y`, `priority Z`, free-form notes) and writes them into the appropriate project's `/inbox/` directory. Ambiguous replies get a one-line clarification back in Telegram, not an email-length round-trip.

### Coordinator

The Coordinator runs the daily operations of the pool.

**Inputs:** All project manifests, all open work queues, agent availability, Mike's directives routed through the Reporter.

**Outputs:** Work assignments to agents, priority ordering when projects compete, escalations to the Reporter when something needs Mike.

**Constraint:** The Coordinator does not produce board-facing output. It produces *agent-facing* instructions. The Reporter is the only voice Mike hears from the swarm.

---

## LAYER 2: THE AGENT POOL

Eight role-based agents, one instance each by default. Additional instances spun up only when justified (volume, radically different skill pack, security isolation, trust level).

| Role | What they do | Examples of work |
|---|---|---|
| **Researcher** | Finds opportunities and evaluates them | Niche scoring for new directories, competitor teardowns, API discovery, affiliate program research |
| **Builder** | Implements code and infrastructure | Scrapers, static site scaffolds, API wrappers, deploy pipelines (executed via queued Claude Code handoff, not autonomously) |
| **Writer** | Produces content in specified voice | Directory city pages, LinkedIn posts, listing descriptions, outreach emails, landing copy |
| **Distributor** | Gets content in front of people | SEO plumbing (sitemaps, schema), social posting, email outreach, newsletter sends |
| **Monetizer** | Handles revenue mechanics | AdSense setup, affiliate link placement, Stripe/Gumroad, lead form integration |
| **Operator** | Keeps running systems alive | Watchdogs, log scanning, uptime monitoring, deploy health, credential rotation tracking |
| **Bookkeeper** | Tracks money and signals | Revenue dashboards, cost accounting, agent ROI, kill-or-keep reports |
| **Coordinator** | Runs daily ops of the pool | (Described in Layer 1) |

**Persona file structure (same for all eight):**
- Identity and philosophy (short — one paragraph)
- The Three Laws (verbatim)
- Standard operating context (who Mike is, QSL/SELARIX situation, current revenue priority)
- Status emission format (see interoperability contract below)
- Directive consumption format (see interoperability contract below)
- Skill modules loaded on project pickup (pulled from toolshed based on project manifest)
- Model configuration (default: DeepSeek via OpenRouter; swappable per project)

**When to spin up a second instance of an agent:**
1. **Volume saturation** — the single instance is creating backlog that affects project deadlines.
2. **Permanent specialization** — a project needs a skill pack that would bloat the shared instance's context (e.g., PQC threat analysis for QSL lives with a dedicated Writer instance).
3. **Security isolation** — credentials or data from one project should not mix with others.
4. **Trust tiering** — experimental projects run with read-only Operators; mature projects get deploy-capable Operators.

Default: share. Dedication is an exception with a named reason.

---

## LAYER 3: PROJECTS

A project is a manifest, not a swarm. Projects register with the Lattice by dropping a manifest file into `/projects/{project_name}/`. Agents in the pool discover registered projects and watch their queues.

### Current project registry (as of April 19, 2026)

| Project | Mode | Status | Notes |
|---|---|---|---|
| **TherapistIndex** | Maintain | Active | 2,595 listings live. AdSense review submitted April 15. First candidate for pool-model retrofit. |
| **TheBinMap** | Build | New | Domain purchased April 18. Directory #2. First greenfield test of Lattice v1. |
| **CrawDaddy** | Low-power maintain | Active | EC2 seller running, watchdog clean. Revenue thesis paused but infrastructure kept warm. |
| **SN61 Miner** | Low-power maintain | Active | UID 57, validators querying, trust rebuilding. Hands-off. |
| **Polymarket Swarm** | Maintain | Active | 4 strategies, paper trader, VPS-resident. Runs independently of Lattice today; candidate for Lattice integration later. |
| **QSL Content** | Paused | Idle | ContentBot blocked on Zapier premium. Workaround is a future project re-activation, not a priority now. |
| **$ATTEST / Bastion** | Deferred | Idle | Revenue-gated. No active work. Reference docs retained. |

### Project manifest schema (`/projects/{project}/manifest.json`)

```json
{
  "project_name": "thebinmap",
  "mode": "build | maintain | low-power | paused",
  "priority": "high | medium | low",
  "voice_config": "path to voice guide in /toolshed/context/",
  "skill_packs": ["directory_scraping", "directory_city_pages", "adsense_setup"],
  "credentials_allowed": ["scoped credential tags"],
  "model_override": null,
  "revenue_target_monthly_usd": 500,
  "status_file": "/projects/thebinmap/status/",
  "inbox": "/projects/thebinmap/inbox/",
  "last_heartbeat": "ISO timestamp"
}
```

### Creating a new project

1. Register the manifest.
2. Define the work queues the project will use (content, scraping, monitoring, etc.).
3. Reference which toolshed skill packs the project's agents should load.
4. Set the voice config.
5. Scope credentials.
6. Set revenue and success metrics.
7. The pool discovers it on the next coordinator cycle and begins watching queues.

No new agents are deployed. No swarm is copied. The project is new; the workers are the same.

---

## LAYER 4: THE INTEROPERABILITY CONTRACT

Every project must produce and consume the same three file types. This is the non-negotiable foundation. Without it, the Reporter cannot roll up status, and the pool cannot work across projects.

### Status file (`/projects/{project}/status/{YYYY-MM-DD}.json`)

Written nightly by the project's active agents. Consumed by the Reporter each morning.

```json
{
  "project_name": "thebinmap",
  "date": "2026-04-19",
  "completed": [
    {"agent": "Builder", "task": "scaffold site structure", "detail": "...", "time": "ISO"}
  ],
  "in_progress": [
    {"agent": "Writer", "task": "first 10 city pages", "eta": "2026-04-21"}
  ],
  "blocked": [
    {"issue": "DNS pointing to wrong IP", "needs": "2-min manual fix", "severity": "medium"}
  ],
  "revenue_events": [
    {"type": "adsense_impression", "amount_usd": 0.03}
  ],
  "flags_for_board": [
    "domain DNS misconfigured"
  ],
  "health_signals": {
    "uptime_pct": 100.0,
    "agent_errors": 0
  }
}
```

### Manifest file (described above in Layer 3)

### Inbox directory (`/projects/{project}/inbox/`)

Mike's Telegram replies land here as dated directive files. The project's agents read the inbox at the start of each cycle and act on new directives. Processed directives move to `/projects/{project}/inbox/processed/`.

```json
{
  "directive_id": "dir_20260419_001",
  "timestamp": "ISO",
  "board_source": "mike_via_telegram",
  "command": "approve | kill | priority | note | free-form",
  "target": "optional — specific issue or agent",
  "content": "the actual text of Mike's instruction"
}
```

These three files are the contract. Any project that emits and consumes them correctly plugs into the Lattice. Any that doesn't, doesn't exist as far as the central swarm is concerned.

---

## LAYER 5: THE TOOLSHED

Capabilities that agents load to perform work. Separate from the agents themselves. Organized by kind, not by project.

```
/toolshed
  /adapters         — wrappers for external services (APIs, databases, third-party tools)
  /tools            — reusable code we've written (scrapers, generators, parsers)
  /skills           — model-facing skill prompts (how to think about a task)
  /context          — reference material (voice guide, Three Laws, blueprint, this document)
  /templates        — scaffolds for common outputs (project starter, new agent persona, status file)
  /candidates       — links and tools under evaluation, not yet integrated
```

### Every toolshed entry has the same header

```
# {Name}
Kind: adapter | tool | skill | context | template | candidate
Status: active | experimental | deprecated
What it does: one sentence
When to use it: one or two sentences
When not to use it: failure modes or anti-patterns
Dependencies: other toolshed entries required, external services called
Model compatibility: all | reasoning-only | specific-model-family
Last updated: YYYY-MM-DD by whom
```

Without the header, the toolshed becomes an unsearchable pile within a month. The header is the discipline.

### Rules of the toolshed

1. **Every entry exists because a real project needed it.** No speculative wrapping. Add adapters and tools on demand, not in anticipation.
2. **Wrap on first use, harden on second use.** First time a project needs a Telegram adapter, build it simply. Second time, harden it — error handling, retries, logging. Third time, it's mature infrastructure.
3. **Skills are versioned like code.** `mike_voice_linkedin_v1.md` can exist alongside `mike_voice_linkedin_v2.md` during transition. Old skills deprecated, not deleted.
4. **The toolshed is the commons.** All agents and all projects draw from the same shelf. No project-private tools — if a tool is useful, it's in the toolshed.

---

## MODEL LAYER: SWAPPABLE BY DESIGN

Today the swarm runs DeepSeek via OpenRouter as the daily driver. Tomorrow it might be GLM-5, Kimi-3, a new lab's release, or a specialized fine-tune. The Lattice treats the model as a swap-in dependency.

**How this is enforced:**
- Every agent reads its model config from its persona file, which reads from project manifest override if present, which falls back to `/toolshed/context/default_model.md`.
- All model calls go through a single OpenRouter adapter in `/toolshed/adapters/`. Changing models is editing one config, not touching agent code.
- Skills are written in prose, not in provider-specific function-call schema. A skill like "write a therapist bio" works whether the underlying model is DeepSeek, Claude, or whatever comes next.
- Claude Code remains its own thing, invoked by Mike. It is not a "model" the swarm chooses; it is a tool Mike uses.

**What we do not do:**
- Do not bake Anthropic-specific or OpenAI-specific assumptions into agent personas.
- Do not assume tool-use/function-calling schema is universal. Skills use prose instructions; structured outputs get parsed from the model's text response.

---

## THE HUMAN-IN-THE-LOOP CONTRACT

Mike's role is **Board Chair.** The swarm runs daily operations. Mike approves, redirects, kills, or greenlights. Mike's daily interaction is the 7 AM Telegram report and the replies it prompts. Target: under 15 minutes most days.

**What the swarm does autonomously:**
- All scheduled routines (scraping, content generation, uptime checks, revenue tracking)
- Responding to in-queue work within a project's defined scope
- Writing status files, emitting flags, routing work between agents
- Surfacing decisions to the Board via the Reporter

**What the swarm does NOT do without Mike:**
- Run Claude Code. The swarm *queues* coding work in the morning report. Mike opens his terminal, runs Claude Code, approves the task. This is deliberate — post-April-3, we do not automate code execution.
- Deploy to production. Agents can *stage* deploys. Mike approves the final push.
- Touch Layer-0 credentials (SSH keys, payment wallets, API keys with write scope). Agents can use scoped tokens for their specific work. Credential rotation remains Mike's job.
- Spawn child agents or new project swarms. The Coordinator can *propose* in the morning report. Mike approves.

**Consulting layer:** Claude Chat (this conversation) is Mike's consulting layer. It sits outside the swarm. It is where Mike thinks out loud, pressure-tests ideas, designs new projects, drafts prompts. The chat does not produce swarm directives directly — it produces plans that Mike turns into directives.

---

## RELATIONSHIP TO PAPERCLIP

Paperclip is the implementation substrate. Companies, agents, issues, routines, inboxes — those are Paperclip concepts. The Lattice describes *what to build in Paperclip*, not a replacement for it.

**Proposed Paperclip structure under Lattice v1:**

- **Central company** (name TBD — possibly "SELARIX Lattice" or "SELARIX Board"): houses the Reporter and Coordinator. Only two agents. This is Mike's daily interface.
- **QSL Security Ops:** Stays as a company. Low-power mode. Routines throttled to weekly. Existing agents remain but their heartbeat cadence drops.
- **SELARIX Operations:** Merged or repurposed into the central Lattice infrastructure.
- **New project companies** (one per active project): TherapistIndex, TheBinMap, etc. Each contains the subset of pool agents actively working that project's queues.

Under the pool model, a single Writer logically exists across multiple Paperclip companies. Paperclip today may not support one agent across companies natively — we may need to implement this as "one agent persona replicated across companies but drawing from the same toolshed and producing status into a shared location." This is an implementation detail the Builder will work out when we operationalize.

---

## VERSIONING AND EVOLUTION

This is **v1.** It is a starting point, not a final design. Trial and error across TheBinMap and the TherapistIndex retrofit will surface what's wrong.

**When to update this document:**
- When a decision contradicts what's written here and the decision is the right one → update the document.
- When a new pattern emerges across two or more projects → add it.
- When a layer turns out to be wrong (toolshed structure, interoperability contract, agent pool count) → redesign and increment.

**Version naming:**
- SELARIX Lattice v1 — this document
- SELARIX Lattice v2 — after first greenfield project (TheBinMap) exposes what's missing
- SELARIX Lattice v3+ — ongoing

**What stays stable across versions:**
- The Three Laws
- The principle that agents are shared, projects are registered
- The principle that models are swappable
- The principle that Mike is Board Chair, not operator
- The principle of Mike-in-the-loop for code execution

Everything else can change as we learn.

---

## IMMEDIATE NEXT STEPS (POST-ADOPTION OF THIS DOCUMENT)

1. **Mike runs research deep-dive** on toolshed sourcing — adapters, tools, skill libraries, MCP servers, scraping stacks, content toolchains. Scoped to the six toolshed kinds and the 3-5 project types active in the next 90 days. Output: ranked shortlist per category.
2. **Draft the first Reporter persona** — single agent, reads from two initial projects (TherapistIndex + TheBinMap), emits morning digest. Deploy to 7 AM Telegram cron.
3. **Retrofit TherapistIndex** to emit status, manifest, and inbox per the contract. First proof that an existing project can speak Lattice protocol.
4. **Build TheBinMap greenfield** using the Lattice from day one. First test of the blank canvas as actually blank.
5. **Write v1 of each of the eight agent personas** in parallel with the above, as we learn what they actually need.

Everything beyond step 5 waits until we see how steps 1-5 shake out.

---

## CLOSING

The Lattice exists so Mike stops rebuilding the swarm every time the target changes. It exists so trial-and-error on one project teaches the whole system, not just that project. It exists so new projects are configuration, not construction.

The swarm pre-Lattice was purpose-built for a security-vendor thesis that didn't produce revenue. The Lattice makes the swarm outlive any single thesis. QSL's security work stays alive at low power. Directory revenue comes online. Whatever comes next plugs in as a manifest.

This is how we scale without starting over.

---

*SELARIX Lattice Architecture v1 | Quantum Shield Labs LLC | April 19, 2026*
*Every scar is a credential. Harvest now, decrypt later. Ship, then iterate.*
