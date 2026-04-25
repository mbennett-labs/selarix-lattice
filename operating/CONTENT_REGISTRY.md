# CONTENT REGISTRY

**Document type:** Living index — append-only
**Status:** Canonical, growing
**Location:** `/operating/CONTENT_REGISTRY.md`
**Last updated:** 2026-04-25 by Mike + Claude
**Convention:** Sorted by date descending (newest first). Searchable by Ctrl+F on creator, topic, or tier.

---

## Why this doc exists

Mike consumes a lot of high-quality reference content extracted from videos, articles, and podcasts. Without an index, those reference docs accumulate in folders and become unfindable. This registry is the index. **One row per reference doc. Three seconds to register a new entry. Five seconds to find any past entry by Ctrl+F.**

Read `/operating/INTAKE_PIPELINE.md` for how new entries get here.

---

## How to use the registry

**To register a new reference doc:**

1. Doc lands in `/content-inputs/` with naming convention `YYYY-MM-DD_creator-or-source_topic-slug.md`
2. Append a row to the table below at the top (most recent first)
3. Required columns: Date | Creator/Source | Topic | Tier | Status | Path
4. Optional but useful: a 1-line "key takeaway" in the Notes column

**To find a past reference:**

- Search by topic keyword (Ctrl+F "directory")
- Search by creator (Ctrl+F "Rush")
- Search by tier (Ctrl+F "Tier 2")
- Filter mentally by status (Acted vs Parked vs Rejected)

**Status values:**

- **Acted** — patterns extracted into toolshed; reference doc is the source-of-truth for those patterns
- **Parked** — interesting but not now; candidate card exists in `/toolshed/candidates/`
- **Rejected** — reviewed and decided not to use; logged in decisions log
- **Pending review** — landed in `/content-inputs/` but not yet reviewed in a build session

---

## Registry

| Date | Creator / Source | Topic | Tier | Status | Path | Notes |
|---|---|---|---|---|---|---|
| 2026-04-25 | IndyDevDan / Stripe Eng | Stripe Minions: Agentic Engineering at $1.9T scale | Mostly park; some Tier 2 patterns | Acted (Blueprint Pattern principle, Toolshed naming validation); rest parked | `/content-inputs/2026-04-25_stripe_minions_agentic_engineering.md` | Most patterns aspirational for SELARIX scale; key takeaways: blueprint pattern (deterministic + agentic interleaved), toolshed-as-meta-tool naming, "specialization is the edge" |
| 2026-04-25 | Connor Finlayson | Directory data sourcing — Find / Enrich / Clean pipeline | Tier 2 | Acted (Perplexity API skill, Tag Generation Pattern, Master Curator thesis); parked Airtable/Apify/Make.com tooling | `/content-inputs/2026-04-25_connor_finlayson_directory_data_sourcing.md` | Key takeaway: Perplexity beats ChatGPT for directory enrichment because of live-cited research; Master Curator > bulk scraping; tag generation enables filtering |
| 2026-04-25 | John Rush | Building SEO Directories — keyword + domain + monetization | Tier 2 | Acted (5-checkbox validation, 80/15/5 rule, post-AI search thesis, claim-listing emphasis) | `/content-inputs/2026-04-25_john_rush_seo_directories.md` | Key takeaway: 80% keyword + domain, 15% data, 5% tech; "if it takes more than a day, you're going wrong"; directories survive AI because users want judgment, not answers |
| 2026-04-25 | Lewis Jackson | Zero-Human AI Trading Firm via Paperclip + Claude Code | Tier 3 candidate | Parked; tactical patterns extracted | `/content-inputs/2026-04-25_lewis_jackson_zero_human_trading_firm.md` | Key takeaway: CEO-only chain of command, heartbeat hiring, Cost Optimizer agent (became Bookkeeper spec); trading firm itself parked until Tier 2 stable |

---

## Pre-pipeline content (registered retroactively)

Content that existed before this pipeline was formalized. Registered for completeness. Some have been acted on; others are unreferenced and may have value to revisit.

| Date (best estimate) | Creator / Source | Topic | Tier | Status | Path | Notes |
|---|---|---|---|---|---|---|
| ~April 2026 | Unknown | Bin store market research (24-page report) | Tier 2 (TheBinMap) | Acted | `/mnt/project/MARKET_RESEARCH.md` | Foundational research for TheBinMap; ~4,000-6,000 US bin stores, fragmented, consolidating |
| ~April 2026 | Unknown | TherapistIndex setup and operations notes | Tier 2 (TherapistIndex) | Acted | `/mnt/project/THERAPISTINDEX_READ_FIRST.md` | The "read this first before working on TI" doc; ~2,595 listings, AdSense pending, broken Brevo claim link |
| March 2026 | Internal | CrawDaddy seller incident (Mar 16) | Tier 1 | Acted (watchdog installed, restart procedure documented) | `/mnt/project/CRAWDADDY_INCIDENT_MAR16_2026__1_.md` | Operational incident log; seller crashed silently for 9 days; root cause + fix + diagnostics |
| March 2026 | Internal | QSL BitTensor Ecosystem Map | Tier 1 | Reference (low-power) | `/mnt/project/QSL_BitTensor_Ecosystem_Map_FINAL.md` | Subnet research; SN61 RedTeam mining thesis; static prices, cross-check with taostats.io |
| March 2026 | Internal | $ATTEST Token Whitepaper v0.1 | Tier 1 (deferred) | Parked (revenue-gated) | `/mnt/project/ATTESTATION_Token_Whitepaper_v01.md` | $ATTEST design; gated behind CrawDaddy $500/mo sustained |
| March 2026 | Internal | Bastion sovereign agent genesis | Tier 1 (deferred) | Parked (revenue-gated) | `/mnt/project/Bastion` | Bastion design; same revenue gate as $ATTEST |
| March 2026 | Internal | QSL Blueprint v3 (Paperclip integration) | Architecture reference | Superseded by SELARIX Lattice v1 | `/mnt/project/QSL_Blueprint_v3_Paperclip_Integration.md` | Older blueprint; mostly replaced by Lattice; useful historical reference for Paperclip role mapping |

---

## Categorization helpers (for future Ctrl+F)

**By Tier:**
- Tier 1 (QSL healthcare/PQC): CrawDaddy incident, BitTensor map, $ATTEST whitepaper, Bastion genesis
- Tier 2 (SELARIX directories): Bin store research, TherapistIndex notes, John Rush directories, Connor Finlayson data sourcing
- Tier 3 candidates: Lewis Jackson trading firm, Stripe Minions agentic engineering

**By Topic:**
- Directories: John Rush, Connor Finlayson, Bin store research, TherapistIndex
- Agents / Paperclip: Lewis Jackson, Stripe Minions, QSL Blueprint v3
- Quantum / PQC: $ATTEST whitepaper, Bastion genesis
- Bittensor: Ecosystem map
- Operations / incidents: CrawDaddy Mar 16

**By Creator (external):**
- Lewis Jackson — Zero-Human Trading Firm
- John Rush — SEO Directories
- Connor Finlayson — Directory Data Sourcing
- IndyDevDan / Stripe Eng — Stripe Minions

---

## Rules of the registry

1. **Append-only.** Never delete a row. If a reference doc becomes obsolete, change Status to "Superseded" and add a Notes line pointing to the replacement.
2. **One-line entries.** If a reference needs more context, that goes in the doc itself or in a candidate card. The registry stays scannable.
3. **Date is when the doc was reviewed in a build session,** not when the original video was published. The point is "when did this enter SELARIX awareness."
4. **Path is the canonical location** in `/content-inputs/`. If a doc lives elsewhere temporarily (e.g., uploads folder), the path here is the eventual destination.
5. **No duplicates.** If a creator has multiple pieces, register each as a separate row with different topic slugs.

---

*Content Registry v1 | SELARIX / Quantum Shield Labs LLC | 2026-04-25*
*Extract once. Index forever. Find anything in 5 seconds.*
