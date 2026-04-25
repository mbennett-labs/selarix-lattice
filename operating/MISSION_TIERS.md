# MISSION TIERS

**Document type:** Operating framework — meta-organizational
**Status:** Canonical (v1)
**Location:** `/operating/MISSION_TIERS.md`
**Last updated:** 2026-04-25 by Mike + Claude
**Read before:** Bucketing any new resource, project, agent, directory, or content piece. Updating any existing project's mission. Spawning any new Paperclip company.

---

## Why this doc exists

Without explicit mission tiers, every new idea looks roughly equal in importance. That's how SELARIX ended up with two stalled Paperclip companies (built for paused theses), a TherapistIndex with a broken claim link unfixed for 31 days, and four reference docs all pitching `quantumshieldtools.org` as if it were the next obvious build.

Each individual idea sounded reasonable. Cumulatively, they pulled focus from the actual mission. **Mission tiers exist to keep that drift from happening again.**

---

## The three tiers

### Tier 1 — North Star: QSL healthcare security before Q-Day

**What it is:** The reason Quantum Shield Labs LLC exists. Post-quantum cryptography work for the healthcare sector before quantum computers compromise current encryption standards.

**The big bet:** Healthcare data systems are decades old, run on protocols that will not survive Q-Day, hold the most sensitive personal data in the economy, and are governed by HIPAA frameworks that pre-date the threat. QSL exists to be the post-quantum security layer for healthcare during the 2027–2030 transition window.

**Examples of Tier 1 work:**
- CrawDaddy security scanning (when it earns its existence)
- Bastion sovereign agent (when revenue gate is met)
- $ATTEST token (gated behind CrawDaddy revenue)
- Healthcare-specific PQC consulting work
- HIPAA-aligned post-quantum migration tools
- Original QSL research on healthcare quantum vulnerability

**Tier 1 status today:** Paused, intentionally. Infrastructure kept warm at low power. Will reactivate when Tier 2 sustaining revenue clears the runway to fund it.

**The rule:** Tier 1 work is the only work that justifies QSL's existence over the long arc. Tier 2 and Tier 3 exist *to enable* Tier 1, not to replace it.

---

### Tier 2 — Sustaining: SELARIX directory factory and similar revenue projects

**What it is:** The cash-flowing layer. Directory businesses, content sites, affiliate plays, low-ops digital products that generate near-term revenue without requiring Q-Day to arrive first.

**The job:** Pay the bills. Fund Tier 1 development. Build operating muscle for running multiple small businesses simultaneously. Develop reusable patterns (the Lattice itself was built for this).

**Examples of Tier 2 work:**
- TherapistIndex (DC/MD/VA mental-health directory)
- TheBinMap (US bin-store directory)
- Future directories that pass the John Rush 5-checkbox validation
- Affiliate content sites
- Productized consulting offerings around directory-building (eventually)

**Tier 2 status today:** Active, primary focus. TherapistIndex needs the broken Brevo link fixed and a real claim-conversion campaign run. TheBinMap needs to ship a v1 in a day per Rush's discipline.

**The rule:** Tier 2 must be sustainably profitable per project before adding new ones. Two active directories is the cap until at least one is generating $500/month.

---

### Tier 3 — Cash channel: opportunistic revenue

**What it is:** Faster-payback bets that can fund Tier 1 or Tier 2 development. Often involve real risk (market, regulatory, technical) that Tier 2 doesn't.

**The job:** Inject capital quickly when needed. Optional, not required. Considered only when Tier 2 is stable AND a specific Tier 3 opportunity has clear unit economics.

**Examples of Tier 3 work:**
- Stripe-style payments / merchant tooling (if a clear use case emerges)
- Lewis Jackson-style autonomous trading firm (high risk; deferred until Tier 2 is profitable AND Bookkeeper agent is operational)
- One-time consulting engagements outside the QSL healthcare focus
- Token launches (gated behind Tier 1 product readiness; e.g., $ATTEST)

**Tier 3 status today:** Inactive. No Tier 3 bets in flight. Stripe and Trading Firm noted as candidates only.

**The rule:** No Tier 3 work begins until two things are true: (1) Tier 2 is generating sustained monthly revenue, (2) the specific Tier 3 opportunity has a written 1-page business case showing unit economics.

---

## How to use this doc

### When evaluating a new resource (extracted video, article, podcast)

After reading the reference doc, ask in this order:

1. **Does this advance Tier 1?** Rare. If yes, escalate.
2. **Does this serve an active Tier 2 project?** Most common. If yes, extract specific tactical patterns.
3. **Does this enable a Tier 3 candidate that has a real business case?** Usually no. Park in `/toolshed/candidates/`.
4. **None of the above?** Park in candidates with activation criteria.

The convergence sections in extraction reports often pitch Tier 3 ideas with Tier 1 framing. Treat those as inspiration, not roadmap.

### When proposing a new project, directory, or Paperclip company

Every new project must declare its tier in its `manifest.json`:

```json
{
  "project_name": "...",
  "mission_tier": "tier_1 | tier_2 | tier_3",
  "tier_justification": "one-sentence reason this serves the declared tier",
  ...
}
```

Without a declared tier and justification, the project does not get built.

### When pruning existing work

Any project, agent, or campaign that does not clearly serve one of the three tiers gets paused, parked, or terminated. Stale work is worse than no work — it pollutes status signals and confuses future-you.

---

## Tier reassignment is allowed (and tracked)

Theses change. Q-Day timelines slip. Markets shift. A Tier 1 bet that turns out to be wrong becomes a Tier 3 candidate. A Tier 2 directory that organically pivots toward enterprise security work might earn Tier 1 status.

**Reassignments must be logged** in `/operating/DECISIONS_LOG.md` with rationale. Silent tier drift is the failure mode this doc exists to prevent.

---

## Current state of all active and paused work

| Project / asset | Tier | Status | Notes |
|---|---|---|---|
| TherapistIndex | Tier 2 | Active — needs claim-link fix + monetization push | 2,595 listings, 9 clicks/month, broken Brevo CTA |
| TheBinMap | Tier 2 | Active — needs v1 ship per Rush 1-day discipline | Domain owned, scaffold ephemeral |
| CrawDaddy | Tier 1 | Low-power maintenance | Below $500/mo revenue gate; v2 ACP migration queued |
| Bastion | Tier 1 | Deferred | Gated behind CrawDaddy revenue |
| $ATTEST | Tier 1 | Deferred | Gated behind CrawDaddy revenue |
| SN61 Bittensor miner | Tier 1 | Low-power | Trust rebuilding post-IP-migration |
| Reporter v1.0.5 | Operational layer | Active | Cross-tier infrastructure |
| QSL Security Ops (Paperclip) | Was Tier 1 | Stalled — needs cleanup or rebuild | Built for old security-vendor thesis |
| SELARIX Operations (Paperclip) | Was Tier 3 (Polymarket) | Stalled — needs cleanup or rebuild | Built for paused trading thesis |
| Polymarket swarm | Tier 3 | Low-power | Paper trading; no real capital deployed |
| Stripe payments | Tier 3 candidate | Parked | Noted as potential cash channel; no business case yet |
| Trading firm (Lewis Jackson stack) | Tier 3 candidate | Parked | Activation criteria in candidate card |
| `quantumshieldtools.org` | Tier 1 / Tier 2 hybrid candidate | Parked | Pitched in 4 extraction reports; not yet evaluated |

---

## The non-negotiable

**Tier 1 is why this exists. Tier 2 funds it. Tier 3 accelerates it when conditions are right. Anything that doesn't serve one of those three doesn't belong on the roadmap.**

---

*Mission Tiers v1 | SELARIX / Quantum Shield Labs LLC | 2026-04-25*
*Q-Day is coming. Tier 1 is the work that matters when it arrives.*
