# SELARIX Historical Record — 2026-04-24
## Lattice v1 Operational Activation + CrawDaddy v2 Migration Planning

*This file records the durable decisions and state changes from 2026-04-24 that affect the SELARIX swarm architecture for the long term. Session-level detail lives in DAILY_LOG_2026-04-24.md. Handoff-to-next-Claude lives in SESSION_HANDOFF.md.*

---

## What changed permanently on this day

### 1. SELARIX Lattice moved from design doc to operational scaffold
**Before today:** The Lattice was a 345-line architecture doc drafted Apr 19, with a GitHub repo containing the foundation (schemas, agent stubs, research doc) but no active projects, no toolshed context files, no Telegram channel.

**After today:** The repo has:
- A `projects/` directory with TherapistIndex and TheBinMap registered as manifests per the interop contract
- `toolshed/context/three_laws.md` and `default_model.md` as loadable context files
- `toolshed/adapters/telegram_selarix_board.md` documenting the new Reporter output channel
- First status files for both active projects reflecting real current state

**Version tag:** Lattice v1 operational, commit `1de924c`.

---

### 2. Security-vendor thesis officially paused
QSL Blueprint v2/v3 (the 15-agent security cabinet: CSO, CTO, CMO, CCO, etc., plus Bastion children WatchDog/GateKeeper/TrustScore, plus $ATTEST tokenomics) is **not killed but paused**.

**What stays running:**
- CrawDaddy v1 seller on EC2 (`acp-seller.service`)
- SN61 Bittensor miner (UID 57)
- Reference docs for Bastion, $ATTEST, PQC work

**What stops:**
- Active investment in scaling security agents
- Any Paperclip work assuming the security-vendor revenue thesis

**What replaces it as primary thesis:**
- Directory factory (TherapistIndex + TheBinMap) for near-term revenue
- Eventually: consulting / custom swarms built on Lattice patterns

**Trigger to un-pause security thesis:** CrawDaddy or another security product crosses $500/mo revenue for 30 consecutive days. Until then, it is maintenance-only.

---

### 3. CrawDaddy v2 migration planning completed
Migration plan from v1 hand-rolled ACP seller to `@virtuals-protocol/acp-node-v2@0.0.6` is fully scoped and documented. Execution phase (Claude Code running under Mike's supervision) is the next work block for this thread.

**Architectural decision:** Signing uses Option C (`signerPrivateKey` from env var) instead of Option A (signFn with native keystore). Rationale: `acp configure` is browser-OAuth-only; running it on a headless EC2 via SSH tunnels was not worth the complexity for the security delta gained.

**Commits:**
- `1d9c9c0` — migration plan (974 lines) pushed to `mbennett-labs/crawdaddy-security/docs/ACP_V2_MIGRATION_PLAN.md`
- `8f67e04` — central reference doc pushed to same repo at `docs/CRAWDADDY_V2_AGENT_REFERENCE.md`

---

### 4. New Telegram channel dedicated to SELARIX Board
`@SelarixBoard_bot` created via BotFather. Token rotated once (first token was exposed in a screenshot during setup; rotated before any use). Stored in NordPass under "SELARIX Board Bot Token."

This channel is **reserved for Reporter output only.** Other swarm channels (`@blocdev_bot` for Moltbook engagement, others for individual Paperclip agents) stay separate to avoid signal-to-noise collapse.

---

### 5. Dead Anthropic key fan-out disabled
ResearchBot (daily 06:00 UTC) and ContentBot (daily 10:00 UTC) were both firing against a dead Anthropic API key rotated after the April 3 Layemor incident. Generated 401 errors that routed through OpenClaw delivery queue to Telegram.

**Action taken:** Both crons disabled with `# DISABLED Apr 24 (dead anthropic key/lib) #` prefix in crontab. Crontab backup at `~/crontab.bak.20260424-1510`. 217 stale delivery-queue messages archived to `~/.openclaw/delivery-queue-archive-20260424/`.

**Outstanding TODO (not executed today):** Migrate ResearchBot and ContentBot to OpenRouter + DeepSeek. This TODO has been open since early April. When it's executed, uncomment the crons.

---

## Architectural principles locked in today

1. **Projects are manifests, not swarms.** One pool of agents can work many projects. Adding a project = adding a manifest + status directory + inbox, not spinning up a new Paperclip company per project (though for Read A we do use separate companies).

2. **Option A now, Option B later.** Each Paperclip company owns its agents (Read A). The long-term goal is one logical agent across multiple companies (Read B), but that requires Builder work Paperclip doesn't natively support. Don't block on B; ship A.

3. **Mike is Board Chair, not operator.** The daily interaction is a 7 AM Telegram digest from Reporter, 15 minutes max. Anything that requires Mike to SSH, run commands, or debug agent logs is a failure of the Paperclip layer.

4. **Claude Code stays human-initiated.** The swarm queues coding work. Mike opens Claude Code and executes. No agent runs Claude Code autonomously. This is a post-Layemor security discipline that is not relaxed for convenience.

5. **Wrap on first use, harden on second.** Don't build speculative adapters. Add to the toolshed only when a real project needs it. Second time a tool is needed, invest in hardening (error handling, retries, logging). Third time, it's mature infrastructure.

6. **Every toolshed entry has the standard header** (kind, status, what/when/when-not/deps/model-compat/last-updated). Without the header, the toolshed becomes an unsearchable pile within a month.

7. **Versioned, not deleted.** `mike_voice_linkedin_v1.md` can exist alongside `mike_voice_linkedin_v2.md` during transition. Old skills deprecated, not erased.

---

## State of working repos at end of day

| Repo | Status | Notable commits today |
|---|---|---|
| `mbennett-labs/selarix-lattice` (private) | Active | `1de924c` Phase 1 projects + toolshed context |
| `mbennett-labs/crawdaddy-security` | Active | `1d9c9c0` migration plan, `8f67e04` reference doc |
| `mbennett-labs/thebinmap` (private) | Paused | scaffold lives ephemeral, needs Builder repackaging |
| `mbennett-labs/bittensor-qsl` | Low-power | SN61 miner ops |
| `mbennett-labs/quantumshieldlabs-website-v2` | Unchanged | website auto-deploys |
| `mbennett-labs/qsl-swarm` | Unchanged | content pipeline (currently unused for Content Strategist) |
| `mbennett-labs/automaton` | Reference | Conway fork, architectural DNA |

---

## Infrastructure state at end of day

| Component | Status | Notes |
|---|---|---|
| EC2 (`3.20.79.143`) | ✅ Healthy | 72% disk, CrawDaddy seller + SN61 miner + OpenClaw running |
| VPS (`69.62.69.140`) | ✅ Healthy | Paperclip live, Polymarket swarm running, SSH to root broken (not urgent) |
| `@blocdev_bot` | ✅ Active | Moltbook engagement channel |
| `@SelarixBoard_bot` | ✅ Created | NOT yet wired to anything — Phase 2 |
| Paperclip QSL Security Ops | 🟡 Stalled | 6 stale issues, CEO dormant 6 days, needs cleanup |
| Paperclip SELARIX Operations | 🟡 Empty shell | 5 placeholder agents, ready to be repurposed |
| TherapistIndex | 🟢 Running | 2,595 listings, AdSense pending Day 9 of review |
| TheBinMap | 🟡 Scaffold only | Domain + repo exist, needs Builder work |
| CrawDaddy v1 ACP | 🟢 Running | Below $500/mo revenue gate |
| CrawDaddy v2 ACP | 🟡 Phase 1 planned | Ready for Phase 2 code execution |
| SN61 miner | 🟢 Active | UID 57, validators querying |

---

*Record closed 2026-04-24. Update when next major architectural change lands.*

