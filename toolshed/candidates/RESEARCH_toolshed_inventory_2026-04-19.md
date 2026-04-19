# SELARIX Lattice Toolshed Research — 2026-04-19

**Research type:** 15-minute deep dive
**Scope:** Tools, libraries, and resources for SELARIX Lattice toolshed population
**Operator:** Mike Bennett / Quantum Shield Labs LLC
**Context:** DeepSeek V3.2 via OpenRouter as primary model; Claude Opus via Max subscription for strategic work; Hostinger VPS + AWS EC2 infrastructure; Paperclip orchestration; directory factory as primary revenue thesis

---

## BLUF (Bottom Line Up Front)

The cheapest, least lock-in solo-op swarm stack for Mike's setup is **LiteLLM + OpenRouter (DeepSeek V3.2 primary) → Astro/Hugo directories with schema-dts → Postiz self-hosted for LinkedIn/X/Farcaster → Stripe+Gumroad webhooks into Postgres/Grafana → Anthropic's `skills` repo as the skill canon → MCP servers for GitHub/Stripe/GSC/GA/AdSense/Gmail/Telegram**.

Every component is OSS or under free-tier pricing at solo scale, all shipped in the last 12 months, and none require frontier-only tool-calling features DeepSeek V3.2 lacks.

**Three deal-breakers to avoid:**
1. LangChain as orchestrator (known bloat)
2. Zapier/Make premium tiers ($500+/mo at directory volume)
3. LinkedIn-posting tools that scrape rather than use the Community Management API (ToS violation)

---

## Category 1 — Adapters (model-agnostic routing)

| # | Tool | What it does | Why it made the cut | OR+DeepSeek | Pricing | Shipped last 12mo |
|---|---|---|---|---|---|---|
| 1 | **LiteLLM (BerriAI)** | Python SDK + self-hostable proxy translating 100+ provider APIs into one OpenAI-compatible interface with retries/fallbacks/cost tracking | De facto standard; 3-line drop-in with first-class `openrouter/*` namespace; free and MIT | ✅ | Free OSS | ✅ v1.83.x April 2026 |
| 2 | **Helicone (AI Gateway + Observability)** | Apache-2.0 proxy logging every LLM request plus a routing gateway; dedicated OpenRouter passthrough | One-line observability, 10k req/mo free; self-host via Docker Compose | ✅ | Free → $20–79/seat | ✅ — ⚠️ Acquired by Mintlify March 2026 |
| 3 | **OpenLLMetry / Traceloop** | OpenTelemetry instrumentations for LLMs, vector DBs, and agent frameworks emitting standard OTel traces to any backend | Vendor-neutral telemetry, zero lock-in, pairs with LiteLLM as the cleanest OSS-only path | ✅ | Free OSS | ✅ v0.47.0 Sept 2025, active |
| 4 | **Portkey Gateway** | Self-hostable AI gateway for 1,600+ LLMs with fallback chains, virtual keys, guardrails, and explicit `@openrouter` provider | Richer free alternative to LiteLLM if the routing UI matters; OSS gateway is $0 | ✅ | Free → $49 Production (Enterprise $2k+ is deal-breaker) | ✅ Feb 2026 docs update |
| 5 | **Vercel AI SDK v5 + @openrouter/ai-sdk-provider** | TypeScript unified SDK for any LLM with `generateText`/`streamText`/`Agent` API and community-maintained OpenRouter provider | Only relevant if any Paperclip worker is Node/TS; cleanest TS adapter | ✅ | Free OSS | ✅ v5 GA July 2025 |
| 6 | **Langfuse** | OSS LLM observability + prompt management with 50k-obs/mo free cloud and full self-host | Sits beside LiteLLM without proxy latency; polished trace UI | ✅ | Free → $59 core, self-host free | ✅ continuous |
| 7 | **OpenRouter baseline (openai SDK + base_url)** | The official `openai` SDK pointed at `https://openrouter.ai/api/v1` with free per-request `total_cost` metadata | Always-works fallback; `:floor`/`:nitro`/`:online` routing modifiers built in | ✅ | 5.5% credit-purchase fee only | ✅ |

**Deal-breakers flagged:**
- RouteLLM — no updates since Aug 2024, violates 12-month rule
- Not Diamond — not an adapter; consume for free indirectly via `openrouter/auto`
- MartianRouter — insufficient public transparency
- Braintrust — eval platform, wrong category; $249/mo
- Portkey Enterprise tier — $2k–10k/mo
- Helicone Team tier — $799/mo

**DeepSeek tool-calling myth:** V3.2 on OpenRouter supports OpenAI-style tool calls per OR's own model page; no adapter above requires a feature DeepSeek lacks.

**Minor bug note:** LiteLLM's OpenRouter embeddings bug (issue #17773, Dec 2025) — route embeddings direct to provider until fixed.

---

## Category 2 — Tools

### 2a. Web scraping stacks (directory extraction at scale)

| # | Tool | What / why | DeepSeek compat | Pricing |
|---|---|---|---|---|
| 1 | **Crawlee (Python/JS)** | Apify's OSS crawler with Playwright, proxy rotation, queues, fingerprints; best free+self-host for Google Maps/Yelp at scale | LLM-agnostic; plug DeepSeek for parsing only | Free, MIT |
| 2 | **Firecrawl (self-host or cloud)** | URL→clean markdown/JSON with JS render, crawl, map, extract; ideal for directory card parsing | ✅ explicit `OPENAI_BASE_URL` → OpenRouter+DeepSeek | Free self-host (AGPL), cloud $16–$333 |
| 3 | **Playwright** | Microsoft browser automation; rock-solid for JS-heavy directories (Yelp, GMaps shells) | LLM-agnostic | Free, Apache-2.0 |
| 4 | **Apify Platform + Store Actors** | Managed cloud for Crawlee + 25k+ pre-built actors including Google Maps Scraper and Yelp | Actors are LLM-free; optional post-process with DeepSeek | Free $5/mo credit → $29 Starter → $199 Scale; ~$7 per 1k GMaps results |
| 5 | **scrapegraph-ai** | Prompt→structured-JSON scraper via directed graph; fits directory fields without selectors | ✅ native DeepSeek class + OpenRouter `base_url` | Free lib; pay LLM tokens |
| 6 | **Jina AI Reader (r.jina.ai)** | Prepend URL → LLM-ready markdown; cheapest "just give me clean text" | Output-only, any LLM downstream | Free tier 10M tokens; token-based paid |
| 7 | **browser-use** | Python AI-agent browser framework with native `ChatOpenRouter` + `ChatDeepSeek` classes | ✅ `ChatOpenRouter(model="deepseek/deepseek-chat")`; use `use_vision=False` to avoid DeepSeek vision bugs | Free OSS, MIT |

**Deal-breakers (scraping):**
- Bright Data ($499/mo minimum; overkill for this scale)
- ScrapingBee (JS render burns 5× credits, beaten on price by Jina+Crawlee)
- Stagehand/Browserbase (great OSS lib but production path assumes paid Browserbase; OR/DeepSeek needs custom provider mapping per open issue #790 — keep on bench)

### 2b. Static site generators for directory sites

| # | SSG | What / why | Pricing |
|---|---|---|---|
| 1 | **Hugo** | Go binary; fastest builds; proven at 100k+ pages; batteries-included taxonomies and permalinks driven by JSON/YAML/TOML data dirs | Free, Apache-2.0 |
| 2 | **Astro** | Islands architecture + Zod-validated Content Collections; best DX for JSON/CSV→pages with strong JSON-LD helpers; slower than Hugo past ~20k pages but cleaner DX | Free, MIT |
| 3 | **Eleventy v3/v4** | JS-based minimal SSG; `pagination { size: 1 }` over `_data/*.json` is purpose-built for directory-from-data pattern; zero default JS | Free, MIT |
| 4 | **Next.js static export** | React framework with `output: 'export'`; only pick if you need React components (map widgets, interactive filters); 10k OK, 100k painful | Free, MIT |

**SSG deal-breakers:** Gatsby (stale, GraphQL overhead); Jekyll (slow at directory scale).

**Recommendation for TheBinMap-scale (>10k listings):** Default to Hugo. Switch to Astro only if interactive islands are needed.

### 2c. SEO plumbing

| # | Tool | What / why | Pricing |
|---|---|---|---|
| 1 | **schema-dts (google/schema-dts)** | TypeScript types for the full Schema.org vocabulary; compile-time JSON-LD validation | Free, Apache-2.0 |
| 2 | **@astrojs/sitemap** (or **next-sitemap**) | Auto-generates `sitemap-index.xml` + chunked sitemaps with filter/serialize hooks; handles 45k-URL chunking automatically | Free, MIT |
| 3 | **googleapis Node client** | Official Google SDK for Search Console v1 + AdSense v2; one package covers impressions, clicks, URL inspection, earnings, reports | Free (API quotas) |
| 4 | **Google Rich Results Test + Schema Markup Validator** | Runtime validation of JSON-LD/microdata and rich-result eligibility; pair with schema-dts for CI post-deploy checks | Free |

### 2d. Social posting alternatives to Zapier premium

**WINNER for all three channels (LinkedIn + X + Farcaster) cheaply: Postiz self-hosted** — the only OSS scheduler with native Farcaster provider alongside LinkedIn and X.

| # | Tool | What / why | LinkedIn | X | Farcaster | Pricing |
|---|---|---|---|---|---|---|
| 1 | **Postiz (OSS)** ⭐ | Self-host on any VPS; native providers for X, LinkedIn, Farcaster, Bluesky, Mastodon, Nostr, Threads; public API, webhooks, n8n node, CLI agent | ✅ | ✅ | ✅ | Self-host $0; cloud $29–$79 |
| 2 | **n8n self-hosted + direct APIs** | HTTP Request node + community nodes for X v2, LinkedIn, Neynar (Farcaster); also glues Stripe/Gumroad webhooks | ✅ (Community Mgmt API) | ✅ | ✅ via Neynar | Free self-host; cloud $24+ |
| 3 | **Typefully API v2 (Dec 2025)** | Cleanest REST API for drafts/scheduling; great X threads + LinkedIn | ✅ | ✅ | ❌ (dealbreaker — needs Neynar sidecar) | $12–$40/mo |
| 4 | **Mixpost (OSS, Laravel)** | Mature self-hosted scheduler; X pay-as-you-go added March 2026 | ✅ (Pro) | ✅ | ❌ | Lite free; Pro one-time ~$179 |
| 5 | **Direct APIs (X v2 + LinkedIn Community Mgmt + Neynar)** | Bypass middleware entirely; full control | ✅ but requires 2–8 wk vetting; ToS forbids generic "automate posting" | ✅ but X Basic $200/mo required for posting at volume | ✅ via Neynar (Jan 2026 protocol acquisition) | X Basic $200; Neynar credits; LinkedIn free post-approval |
| 6 | **Pipedream** | Serverless automation with Gumroad/Stripe/HTTP triggers + Node/Python code steps | Via HTTP | Via HTTP | Via HTTP | Free 10k credits → $19+ |
| 7 | **Buffer API** | ⚠️ API being rebuilt; new beta not accepting new developer apps; no Farcaster. Listed for completeness only | ✅ | ✅ | ❌ | $5/channel/mo |

**Deal-breakers (social):**
- LinkedIn ToS prohibits any posting tool that doesn't use the approved Community Management API OAuth — avoid scrapers
- X posting is not free — budget $200/mo Basic tier regardless of wrapper
- Zapier/Make premium plans cross $500/mo at directory volume

### 2e. Revenue tracking

| # | Tool | What / why | Pricing |
|---|---|---|---|
| 1 | **Stripe Node/Python SDK + signed webhooks** | Gold-standard docs; direct ingest to Postgres for Grafana | 2.9% + $0.30/txn; SDK free |
| 2 | **googleapis AdSense Management API v2** | Earnings, reports, sites, ad units, policy issues; 3-year retention; CSV export | Free |
| 3 | **Gumroad API v2 + Ping webhooks** | HMAC-signed webhooks for sale/refund/subscription events; license-key verification | Free (platform fees on sales) |
| 4 | **Umami (self-hosted)** | Cookieless, privacy-first analytics; runs on 512 MB RAM; renameable script bypasses adblockers | Self-host free |
| 5 | **Trackdesk** | SaaS affiliate/referral tracking with 900+ integrations; free up to $1k/mo affiliate revenue | Free → $249 → Enterprise $499+ (deal-breaker at top tier) |

**Pattern recommendation:** Stripe/Gumroad/AdSense → Postgres → Grafana (free cloud tier for solo); Umami for click attribution; Trackdesk free tier for affiliates.

---

## Category 3 — Skills

### 3a. Anthropic published skills (github.com/anthropics/skills — 120k★, Apache-2.0 for open skills)

1. **document-skills bundle (docx, pdf, pptx, xlsx)** — Four skills powering Claude.ai's native Office file editing; prompts + Python scripts transplant to DeepSeek if you carry the SKILL.md + `scripts/` folder. Source-available license — check before redistribution. ⚠️
2. **skill-creator** — Interactive guide for authoring SKILL.md files; the meta-skill for building SELARIX's own lattice of skills. ✅ fully portable.
3. **frontend-design** — React/Tailwind/shadcn scaffolding with embedded design-quality checklists; breaks the "Inter + purple gradient" AI-default look. ✅ portable.
4. **mcp-builder** — Scaffolds high-quality MCP servers in Python/TS from NL spec; pairs with 3b to fill gaps. ✅ portable.
5. **brand-guidelines + doc-coauthoring + internal-comms (Q4 2025–Q1 2026 additions)** — Structured brand color/type templates and 3-phase doc workflows; directly useful as voice-consistency scaffolding. ✅ portable.

### 3b. MCP servers (7 top picks)

| Service | Best server | Notes |
|---|---|---|
| **GitHub** | `github/github-mcp-server` (official) | First-party; OAuth + remote endpoint; most-installed MCP of 2025–26 |
| **Stripe** | `@stripe/mcp` (official) | Remote `https://mcp.stripe.com`; docs at docs.stripe.com/mcp |
| **Google Analytics** | `googleanalytics/google-analytics-mcp` (official, read-only) | Beats community wrappers on auth + schema coverage; `ruchernchong` fallback |
| **Google Search Console** | `Suganthan-Mohanadasan/Suganthans-GSC-MCP` | 20 tools: quick-wins, cannibalisation, decay, CTR benchmarks; has hallucination guardrails |
| **Gmail** | `GongRzhe/Gmail-MCP-Server` | Best-maintained community Gmail MCP; 2k+★ |
| **Telegram** | `chaindead/telegram-mcp` | Most-starred; uses user-API (MTProto) for DMs + channels |
| **AdSense** | `@appsyogi/adsense-mcp-server` | Only actively maintained AdSense MCP; read-only OAuth |

**Gaps:**
- **LinkedIn** has no first-party MCP; `stickerdaniel/linkedin-mcp-server` is the best OSS but uses browser automation (ToS risk) — prefer the Community Mgmt API via `mcp-builder`
- **Google My Business** has no mature MCP as of April 2026 — wrap the Business Profile API via `mcp-builder`
- **WordPress:** `Automattic/mcp-wordpress-remote` (Jan 2026) for .com/Jetpack; `server-wp-mcp` for self-hosted

### 3c. Prompt/skill libraries on GitHub

1. **anthropics/skills + anthropics/anthropic-cookbook** — Primary canonical sources; cookbook code is model-agnostic
2. **VoltAgent/awesome-agent-skills** — 1000+ community skills explicitly cross-compatible (Claude Code, Codex, Gemini CLI, Cursor, Windsurf); best curation of the 2026 entrants
3. **f/awesome-chatgpt-prompts (130k★) + langgptai/awesome-claude-prompts (~10k★)** — Battle-tested role prompts trivially portable to DeepSeek
4. **microsoft/promptbase** — Peer-reviewed Medprompt/Medprompt+ techniques with evaluation harnesses; ⚠️ last major update 2024–25 (method still valid, technique-only)
5. **travisvn/awesome-claude-skills + hesreallyhim/awesome-claude-code + rohitg00/awesome-claude-code-toolkit** — Fast-moving 2026 indexes; cross-reference to avoid stale picks

### 3d. Voice-matching techniques

1. **Exemplar / K-shot progression (Riley Goodside method)** — Instruction → K-shot → K-shot *selection* (embedding-retrieval of closest exemplars) → fine-tune only as last resort; works identically on DeepSeek at 64k context
2. **Brand-bible / style-guide embedding (Anthropic `brand-guidelines` pattern)** — Structured SKILL.md with voice axes (POV, reading level, cadence, forbidden words, signature moves) plus 2–3 gold exemplars; declarative and reusable
3. **DSPy + GEPA "Voice Lattice"** — Model voice as an 8-D vector and use DSPy signatures + GEPA genetic-Pareto optimization; programmatic voice-tuning path; name-matches SELARIX "Lattice" motif. ✅ DeepSeek via OpenRouter as `LM` backend
4. **Simon Willison's style-transfer notes** — Pragmatic writeups on system-prompt voice adoption; plus Qwen3-TTS (Apache-2.0, Jan 2026) for OSS audio cloning to avoid ElevenLabs lock-in
5. **Rewrite-in-style with delta-guarding** — Two-pass pattern: rewrite then diff semantics vs original; fixes short-message mutation failures

---

## Category 4 — Context

### 4a. Directory site SEO playbooks (post-HCU / post-AIO)

**Headline:** Programmatic SEO survived but rules tightened. Google's Scaled Content Abuse policy (Aug + Dec 2025 updates) penalizes thin keyword-swap templates; winners ship data-rich, per-row-enriched pages. Directories have had a measurable renaissance because AI Overviews fumble "best X in [city]" queries — the exact sweet spot for TheBinMap and TherapistIndex.

1. **Frey Chu — Niche Pursuits interview + Ship Your Directory community** — Operator running $2,500+/mo directory portfolio; most directly applicable to SELARIX's thesis. Free podcast/article; paid course separate. Aug 2025, updated late 2025
2. **IndexCraft — "Programmatic SEO Guide 2026"** — 2026-current deep-dive on Scaled Content Abuse, quality gates, indexation management based on 40+ client audits. Free
3. **Search Engine Land — "SEO in 2026"** — 2026 technical-hygiene baseline. Free
4. **Ahrefs Blog — programmatic SEO + directory guides** — Keyword × modifier × location matrix math. Free blog
5. **Evergreen Media — "SEO Trends 2026: Strategies for the AI Era"** — AIO CTR impact data (-34.5% on pos. 1 per Ahrefs). Updated Feb 10, 2026

### 4b. Local SEO + LocalBusiness schema

1. **Google — Local Business Structured Data guide** — Canonical spec; last updated 2025-12-10. Free
2. **Schema.org — LocalBusiness type reference** — Upstream vocabulary for properties Google doesn't document
3. **Whitespark — 2026 Local Search Ranking Factors Report** — Quantifies proximity (~55%), GBP signals (32%), reviews (16–20%); 47 new AI-visibility factors. Free
4. **Sterling Sky — Joy Hawkins research blog** — Rigorous controlled-test studies (GBP posts, geotag, hours-of-operation ranking). Free
5. **BrightLocal — Local Consumer Review Survey 2025 + Local Search Industry Survey** — Consumer-side review behavior and NAP consistency impact. Free

### 4c. Content writing frameworks for voice consistency

1. **Mailchimp Content Style Guide** — Voice pillars + tone-by-emotional-state matrix; best fit for TheBinMap's contractor/homeowner and TherapistIndex's anxious-user audiences
2. **GOV.UK Style Guide + Writing for GOV.UK** — Plain-English, active voice, 25-word sentence discipline; gold standard where users are stressed or in crisis. Monthly editorial review
3. **18F Content Guide** — American-English counterpart; strong on inclusive language. ⚠️ 18F defunded 2025 — frozen-but-valid
4. **Atlassian Design System — Voice and Tone + Writing Style** — Component-level voice embedding; directly transferable to Lattice templated listing cards
5. **Ann Handley — "Everybody Writes" 2nd ed. + Total Annarchy newsletter** — How to *develop* an original persona; fills the gap system guides don't cover

### 4d. Legal/compliance context for directory sites

1. **US Copyright Office — DMCA Designated Agent Directory + §512 resources** — Absolute baseline; $6 fee, 3-year renewal; safe harbor is NOT retroactive pre-designation. Free info
2. **ADA.gov — Title II Web Rule Fact Sheet + First Steps (DOJ 2024 rule, WCAG 2.1 AA)** — Compliance dates April 24, 2026 (pop 50k+) and 2027 (<50k); Title III plaintiffs' bar uses this as de facto standard. Implement WCAG 2.2 AA for 2026-prudent posture
3. **CPPA — 2026 CCPA/CPRA regulations** — Effective Jan 1, 2026; mandatory GPC signal honoring, dark-pattern ban, ADMT oversight. Thresholds $26.625M revenue or 100k Californians or 50% revenue from sale/share
4. **Eric Goldman — Technology & Marketing Law Blog (§230 tracker)** — Jan 2026 roundup covers ~30 recent rulings; §230 weakening at product-liability edges. Free
5. **Congressional Research Service — "§230: An Overview" R46751** — Nonpartisan citation-heavy explainer; best baseline doc for internal policy decks

---

## Category 5 — Templates (pattern-stealing only)

### 5a. Agent framework scaffolds

| # | Framework | Specific pattern to steal | DeepSeek compat | Repo |
|---|---|---|---|---|
| 1 | **LangGraph** | State checkpointing + interrupt/resume via `thread_id`; persist graph state to SQLite/Postgres between node executions | ✅ | github.com/langchain-ai/langgraph |
| 2 | **CrewAI** | YAML-defined role/goal/backstory + sequential vs hierarchical process modes; maps to Paperclip VPS/EC2 worker declarations | ✅ via LiteLLM | github.com/crewAIInc/crewAI |
| 3 | **AutoGen v0.4 / MS Agent Framework** | Event-driven actor mailbox + `GroupChatManager` selector; maps to Redis/NATS between VPS and EC2 | ✅ | github.com/microsoft/autogen, microsoft/agent-framework |
| 4 | **Letta (MemGPT)** | Memory blocks (core/archival/recall) + "sleep-time" background reflection agent writing to its own long-term memory | ✅ | github.com/letta-ai/letta |
| 5 | **Smolagents (HuggingFace)** | `CodeAgent`: LLM emits executable Python code blocks (sandboxed) rather than JSON tool-calls — fewer tokens, plays to DeepSeek's code strength | ✅ | github.com/huggingface/smolagents |
| 6 | **Pydantic AI** | Pydantic-validated structured outputs + `FallbackModel` chaining; first-class `OpenRouterProvider` + `DeepSeekProvider`. **Best-in-class DeepSeek support** | ✅ native | github.com/pydantic/pydantic-ai |
| 7 | **Mastra (TypeScript)** | Workflow suspend/resume with durable step state + A2A protocol (agent-to-agent JSON-RPC 2.0); cleanest TS workflow DX. ⚠️ avoid copying from `ee/` dirs (Mastra Enterprise License) | ✅ native DeepSeek provider | github.com/mastra-ai/mastra |

**Also scan:** OpenAI Agents SDK (steal `handoffs` primitive; Chat Completions mode works with OR+DeepSeek, avoid Responses API mode). Dify (visual DAG + dataset binding UI). n8n AI nodes (credential-scoped node pattern). Flowise (visual flow → JSON manifest export — blueprint for Paperclip task DSL).

**Hardlocked to Claude:** Anthropic's Claude Agent SDK, Claude Code's Agent Teams feature (Opus 4.6 required).

### 5b. Directory site starter templates

1. **ShipFast Directory (Next.js)** — MDX-backed listings + generated sitemap + programmatic per-category SEO; $199–$299 (**do not buy, study public clones**)
2. **LaunchFast Astro Directory** — Content Collections + Astro islands ONLY on the filter bar; zero-JS by default. ~$149 (**do not buy**)
3. **Makerkit (Next.js + Supabase)** — RLS-first multi-tenant schema + feature-flag gating via Supabase; free Lite tier
4. **michaeltroya/supa-next-starter (free OSS)** — Clean `supabase-ssr` auth scaffold; copy as Paperclip dashboard base
5. **Hugo Directory Themes + PocketBase** — Front-matter taxonomies → auto-generated indexes + single-binary SQLite backend with admin UI; deploys on Hostinger with ~0 ops

### 5c. Open-source swarms actually shipped with users

1. **Aider** (github.com/Aider-AI/aider) — Architect + Editor model split (reasoning planner + cheap editor); tree-sitter repo-map for context compression. ~30k★; heavy OpenRouter presence
2. **OpenHands (All-Hands AI)** (github.com/All-Hands-AI/OpenHands) — Event-stream architecture + pluggable `AgentController` + `Runtime` (Docker) separating "what agent decides" from "where code runs." ~40k★; v1.6 Mar 30, 2026 with K8s + Planning Mode
3. **Claude Squad** (github.com/smtg-ai/claude-squad) — Per-task git worktree + tmux session isolation + yolo/auto-accept background mode; exact pattern for solo-op parallelism on one VPS. Despite name, works with Aider/Codex/OpenCode
4. **MetaGPT** (github.com/geekan/MetaGPT) — SOP-as-prompt + shared message pool + structured artifact handoffs (PRD → design → code); enforces deliverable chains over free-form chatter. ~45k★
5. **gptme** (github.com/gptme/gptme) — "Everything is a tool, tools compose via pipes" + hierarchical sub-agent spawn from inside a tool call; ~2k-LOC core small enough to re-implement as a Paperclip worker type

**Also scan:** Cline (plan/act mode toggle + explicit approval gates).

**Excluded:** SWE-agent (research/benchmark-oriented). **Manus** (closed-source, no public repo).

### 5d. Paperclip-compatible orchestration patterns

No public OSS project named "Paperclip" matches Mike's described orchestrator. Pivoting to composable primitives.

1. **Temporal (workflows-as-code)** (github.com/temporalio/temporal, github.com/temporalio/ai-cookbook) — Deterministic Workflow + non-deterministic Activity split → Event-History replay survives VPS restarts; Signals for human-in-loop; Schedules for ambient-agent wake-ups. **Caveat pattern:** offload large LLM payloads to S3/R2 codec to avoid saturating Workflow history
2. **Inngest + Agent Kit** (github.com/inngest/inngest, github.com/inngest/agent-kit) — `step.run()` memoization + `step.waitForEvent()` + `step.sleep()` so retries don't re-burn LLM tokens; native Next.js adapter. ⚠️ cloud pricing balloons on LLM workloads — forecast before using
3. **BullMQ + Redis** (github.com/taskforcesh/bullmq) — Queue-per-agent-role + dead-letter queue + repeatable jobs for polling agents, paired with SQLite/Postgres memory table keyed by job ID; lightest possible orchestration for one-VPS + one-EC2 topology

**Steal-combo blueprint for Paperclip:** LangGraph checkpointing + Temporal replay-from-history + Aider architect/editor split + Claude Squad worktree-per-task + Mastra A2A + Letta sleep-time memory covers durability, cost efficiency, isolation, agent comms, and long-term memory in one solo-op stack.

---

## Category 6 — Candidates (exotic / experimental / new)

### 6a. AI tooling released Jan–Apr 2026 🆕

1. **Hermes Agent v0.10 (Nous Research, Apr 16 2026)** — MIT self-hosting runtime: 118 skills, 3-layer memory, 6-channel gateway (Telegram/Discord/Slack/WhatsApp/Signal/CLI), closed learning loop that compiles sessions into reusable Markdown skills. ✅ OR+DeepSeek. Best fit for VPS-hosted solo swarm
2. **SwarmClaw** (github.com/swarmclawai/swarmclaw) — Self-hosted multi-agent runtime with first-class MCP, 23 LLM providers (OR, DeepSeek, Ollama native), delegation to Claude Code/Codex/OpenCode CLIs, durable jobs + heartbeats. Closest off-the-shelf Lattice-architecture match
3. **Claude Code Agent Teams / Swarm Mode (Feb 2026)** — Native multi-agent orchestration via `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`. Indirect DeepSeek via `ANTHROPIC_BASE_URL` proxy
4. **OpenHands v1.6 + Software Agent SDK (Mar 30 2026)** — K8s support + Planning Mode beta; ~$0.15–0.60/task on DeepSeek
5. **Microsoft Agent Framework 1.0 GA (Apr 3 2026)** — Unified Semantic Kernel + AutoGen with MCP + A2A; useful for any .NET/Azure edge workers
6. **Cursor Automations (early 2026)** — Always-on Cursor agents triggered by GitHub PRs/Slack/Linear/PagerDuty; DeepSeek only via Cursor "Custom API"
7. **last30days-skill (Mar 29 2026)** — Claude Code skill synthesizing Reddit/X/YouTube/HN/Polymarket summaries; good utility brick

### 6b. Under-the-radar practitioners to follow

1. **@skirano (Pietro Schirano)** — X/GitHub. Ex-Anthropic; viral Claude Code DNA-analysis sub-agent swarm thread (Jan 2026, covered in TIME)
2. **@ruvnet (rUv)** — GitHub `ruflo` / Claude-Flow multi-agent swarm with RAG + MCP + Claude Code/Codex integration
3. **@xingyaoww (Xingyao Wang)** — OpenHands lead; production agent SDK patterns, SWE-Bench, CodeAct
4. **@addyosmani (Addy Osmani)** — Concrete Claude Code swarm + MCP patterns for solo builders
5. **@levelsio (Pieter Levels)** — Solo-op monetized directory sites (Nomad List, PhotoAI) now running AI-agent stacks; $3M+ ARR single-operator proof point
6. **@desplega-ai** — `agent-swarm` framework (Docker-isolated workers, Slack/GitHub/email ingress, lead+worker pattern with SQLite memory) — direct Lattice blueprint
7. **DeepSeek team + Zhipu (Z.ai) English blog** — Chinese lab English presence on DSA sparse attention, GLM-5 architecture; GLM-5 "Pony Alpha" OpenRouter stealth-release (Feb 2026)

### 6c. New OpenRouter-compatible models

| # | Model | Context | OR Price (in/out per Mtok) | Tools | Strength |
|---|---|---|---|---|---|
| 1 | **DeepSeek V3.2** (Dec 2025) | 164K | $0.26 / $0.39–0.42 | ✅ | Current sparse-attn workhorse; your primary |
| 2 | **DeepSeek V3.2 Speciale** 🆕 | 164K | $0.40 / $1.20 | ✅ | RL-scaled variant; reportedly edges GPT-5 on hard reasoning. Fallback for hard-task tier |
| 3 | **Kimi K2.5 (MoonshotAI, Jan 2026)** 🆕 | 262K | ~$0.38/M effective | ✅ vision + function | Native "Agent Swarm" paradigm; 76% cheaper than Opus 4.5 on HLE. Directly aligned with Lattice thesis |
| 4 | **GLM-4.6 / GLM-4.7 (Z.ai)** 🆕 | 200K | 4.7: $0.39 / $1.75 | ✅ | Strong coding + agentic; works well in Claude Code/Cline/Roo |
| 5 | **Qwen3-Max / Qwen3.6 Plus (Alibaba, Apr 2 2026)** 🆕 | 262K / 1M | 3.6 Plus: $0.325 / $1.95 | ✅ | Qwen3.6 Plus scored 78.8 SWE-Bench Verified with 1M ctx — best open long-context agentic model at the price |
| 6 | **MiniMax M2.7** 🆕 | 196K | $0.30 / $1.20 | ✅ | 56.2% SWE-Pro, 57% Terminal Bench 2; cheap parallel workers |
| 7 | **Xiaomi MiMo-V2-Flash (Mar 2026)** 🆕 | 256K | very low | ✅ | MoE 309B/15B active; claimed ~3.5% cost of Sonnet 4.5; reasoning toggle |

**Do NOT chase:** "Hunter Alpha" on OR (cloaked, turned out to be Xiaomi MiMo-V2-Pro per Reuters Mar 18 2026, NOT DeepSeek V4). **DeepSeek V4 is NOT public** as of Apr 6 2026 per Reuters/The Information — launch "in next few weeks" on Huawei chips.

### 6d. Experimental patterns

1. **Claude Computer Use + Dispatch (Mar 17/23 2026)** — Phone↔desktop persistent thread + native Mac computer use; Mac-only today, Windows Q3 2026
2. **OpenAI Codex Desktop with computer-use + in-app browser (Apr 16 2026)** — macOS cursor sandbox + embedded Chromium + persistent memory + 90 MCP-native plugins
3. **Pipecat + Cartesia Sonic-3 voice stack** — OSS Python framework (Daily/Pipecat) for build-your-own voice agents at 10k+ min/mo where Retell/Vapi hosted ($0.07–0.13/min) unit economics fail
4. **Autonomous coding agents beyond Claude Code** — OpenHands 1.6, Cline 4.0 (5M installs, MCP-first, approval-per-edit), Aider architect-mode, Devin v2, Factory Droid
5. **Agent memory — Mem0, Zep/Graphiti, Letta, Supermemory** — Mem0 easiest drop-in; Zep best temporal reasoning (Graphiti 63.8% LongMemEval vs Mem0 49%); **Supermemory via MCP is lowest-friction for Lattice**
6. **Anthropic Agent Teams pattern (formalized)** — Inbox + taskboard + TeammateTool pattern now reference architecture copied into desplega-ai/agent-swarm, ruflo, SwarmClaw. Adopt the *pattern* even when swapping models
7. **browser-use / Operator-class** — OpenAI Operator-style agents still chunkier than desktop computer-use; use `browser-use` OSS library for deterministic Playwright+LLM flows when desktop control isn't needed

### 6e. MCP ecosystem developments

1. **MCP donated to Linux Foundation / Agentic AI Foundation (Dec 2025)** — Anthropic/Block/OpenAI co-founded AAIF; OpenAI killed Assistants API and adopted MCP; 97M monthly SDK downloads. OAuth 2.1 + dynamic client registration; SSE deprecated in favor of **Streamable HTTP**
2. **MCP Apps — interactive UI in chat (Jan 2026)** — Tools can return HTML rendered in sandboxed iframe in Claude/ChatGPT/Goose/VS Code via JSON-RPC over postMessage. Co-developed by Anthropic + OpenAI. Big for solo-op dashboards
3. **OpenAI MCP support shipped** — Apps SDK, ChatGPT Developer Mode, Codex CLI native MCP config in `~/.codex/config.toml` with OAuth + bearer token
4. **Registry landscape** — Official `registry.modelcontextprotocol.io` (Sep 2025). Directories: **PulseMCP** (~11,840 hand-reviewed, best editorial), **Glama** (~21,000 widest), **mcp.so** (~19,700 community), **Smithery** (~7,000 cleanest install + hosted remote servers), **Cline Marketplace** (native). For solo-op: Smithery for install, PulseMCP for discovery
5. **Notable new MCP servers worth installing** — `pulsemcp-server` (discovery-as-a-tool), official GitHub MCP, PostgreSQL MCP, Context7 (docs), Chrome DevTools MCP, Playwright MCP, Exa Search MCP, Composio Twitter MCP (OAuth handled), Sentry MCP, Supermemory MCP (agent memory layer)

---

## TOP 10 MUST-EVALUATE — cross-category priority list

In strict priority order for Mike to look at first:

1. **LiteLLM (BerriAI)** — Adapter foundation. Evaluate first; everything else hangs off this abstraction. 3-line drop-in, MIT, explicit OpenRouter+DeepSeek support, continuous releases through April 2026
2. **Postiz (self-hosted)** — Unblocks the Zapier-premium social-posting problem today. Only OSS scheduler covering LinkedIn + X + Farcaster natively. Install on Hostinger VPS for $0
3. **Anthropic skills repo (github.com/anthropics/skills)** — Canonical skill patterns (brand-guidelines, skill-creator, mcp-builder, frontend-design). Clone, adapt SKILL.md prompts for DeepSeek, ship SELARIX-specific skills on top
4. **Firecrawl (self-hosted) + Crawlee** — Directory scraping spine. Firecrawl for clean markdown extraction (explicit `OPENAI_BASE_URL` → OpenRouter/DeepSeek); Crawlee for high-volume crawls. Covers TheBinMap greenfield and TherapistIndex maintenance
5. **Hugo (or Astro for interactivity)** — Directory SSG. Hugo for raw speed at 10k+ listings; switch to Astro only if interactive islands are needed. Both have free schema/sitemap helpers
6. **MCP server bundle — GitHub + Stripe + Google Analytics + GSC + AdSense + Gmail + Telegram** — Seven first-party or top-community servers cover Mike's entire integration surface. All model-agnostic; install via Smithery
7. **Claude Squad (+ Aider profile)** — Solo-op parallelism pattern: per-task git worktrees + tmux sessions + yolo background mode. The pattern worth copying into Paperclip's worker spawner regardless of which coding agent runs inside
8. **Temporal workflows + BullMQ** — Orchestration primitives for Paperclip. Temporal for durable replay-from-history (survives VPS restarts); BullMQ for lightweight queue-per-agent-role. Pick one based on complexity
9. **Pydantic AI** — Best-in-class DeepSeek+OpenRouter support with `FallbackModel` chaining and typed tool I/O. If any Paperclip component is net-new Python, start here rather than CrewAI/LangGraph
10. **Frey Chu directory SEO playbook + Whitespark 2026 Local Ranking Factors Report** — Two context docs that define what good looks like for TheBinMap/TherapistIndex in the post-HCU/post-AIO environment. Before shipping content: read both

---

## Deal-breakers — tools frequently recommended but flagged for SELARIX

| Tool | Reason to avoid |
|---|---|
| **LangChain (as orchestrator)** | Excluded by task; known bloat. OK to reference component-by-component (LangGraph is separate and recommended) |
| **Zapier premium / Make.com premium** | Crosses $500/mo at directory volume; replaced by Postiz + n8n self-host |
| **RouteLLM (lm-sys)** | No meaningful update since Aug 2024 — violates 12-month-shipping rule |
| **Not Diamond / MartianRouter** | Not adapters (routing recommendation only) or insufficient transparency; consume Not Diamond for free via `openrouter/auto` |
| **Bright Data ($499/mo)** | Overkill for salvage-yard/therapist directories; Crawlee+Jina covers it free |
| **ScrapingBee JS-render** | Credits burn 5× on default JS; beaten on price by Jina Reader + Crawlee |
| **Stagehand without Browserbase** | OSS lib great, but production path assumes paid Browserbase cloud; OR/DeepSeek requires custom provider mapping (issue #790) |
| **Buffer API** | Beta rebuild not accepting new dev apps; no Farcaster support |
| **AffiliateWP** | WordPress-only — excluded if stack isn't WP. Prefer Trackdesk free tier |
| **Trackdesk Enterprise ($499+/mo)** | Crosses pricing threshold; stay on free or Business tier |
| **Impact.com / PartnerStack** | $1k–5k/mo for solo scale — violates budget |
| **LinkedIn-posting scrapers** (e.g., stickerdaniel linkedin-mcp-server in write mode) | ToS violation; LinkedIn allows posting only via approved Community Management API OAuth |
| **Helicone Team tier ($799/mo)** | Free + Pro is sufficient at solo scale; also flag March 2026 Mintlify acquisition as roadmap risk |
| **Portkey Enterprise ($2k–10k/mo)** | Deal-breaker pricing; self-host OSS gateway or stay on $49 Production |
| **Braintrust Pro ($249/mo)** | Eval platform not adapter — wrong category |
| **Claude Agent SDK / Claude Code Agent Teams (as core)** | Hardlocked to Claude/Opus — fine for Mike's manual Claude Code use, unsuitable as swarm orchestrator given DeepSeek-primary economics |
| **OpenAI Agents SDK in Responses API mode** | GPT-locked; Chat Completions mode is fine with OR+DeepSeek |
| **Mastra `ee/` directories** | Enterprise License (source-available but paid for prod) — study patterns, don't copy code from `ee/` |
| **n8n** for multi-tenant hosted resale | Sustainable Use License restricts commercial hosting. Self-host for internal SELARIX use is fine |
| **"Hunter Alpha" cloaked model on OpenRouter** | Turned out to be Xiaomi MiMo-V2-Pro per Reuters Mar 18 2026 — NOT DeepSeek V4 |
| **18F Content Guide as live reference** | 18F defunded 2025; site still accessible but frozen. Use as valid historical reference only |
| **Manus** | Closed-source, no public repo — violates task's "must be real shipping software with studyable code" rule |
| **SWE-agent** | Research/benchmark-oriented; not production. Use OpenHands/Aider instead |
| **Gatsby / Jekyll for directories** | Gatsby stale with GraphQL overhead; Jekyll slow at directory scale |

---

**Freshness note:** Every primary recommendation has a public release within the last 12 months (April 2025–April 2026), with many in the last 90 days (Jan–Apr 2026) flagged 🆕 in Category 6.

**Speculation/caveats to verify before committing budget:**
- Hermes Agent v0.10 star-count claims (single-vendor blog — directionally credible, not independently audited)
- Mastra 22k★/1.8M monthly npm figures (vendor-adjacent source)
- AutoGen "maintenance mode" status (community-reported, no Microsoft sunset notice)
- H.R. 6746 §230 sunset (proposed bill, not enacted)
- DOJ Title III formal web rule (under review per Nov 2025 reporting, not yet published — WCAG 2.1/2.2 AA remains de facto plaintiffs'-bar standard)

---

*Research compiled 2026-04-19 via Claude deep-research. Filed as toolshed candidates inventory for SELARIX Lattice v1.*
