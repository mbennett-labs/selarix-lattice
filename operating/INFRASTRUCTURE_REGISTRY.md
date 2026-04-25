# INFRASTRUCTURE REGISTRY

**Document type:** Living reference — verified state of all SELARIX/QSL infrastructure
**Status:** Canonical, growing
**Location:** `/operating/INFRASTRUCTURE_REGISTRY.md`
**Last updated:** 2026-04-25 by Mike + Claude
**Convention:** Verified facts only. If something is "best guess," mark it explicitly with ❓. Update when reality changes — never let this drift.

---

## Why this doc exists

In today's session (2026-04-25), I asked Mike for the same status info three times that should have been instantly findable: where TheBinMap is deployed, where the SSH key for VPS lives, what mailboxes exist, whether AdSense was approved. Each time it cost 5-15 minutes of friction. Cumulative ~30-45 min of pure session friction that this doc prevents next time.

**The discipline:** when Claude (current or future) asks "where is X" or "is Y configured," the answer is here. If it's not, this doc gets updated immediately so the next ask is free.

---

## Servers and access

### EC2 (US-East-2, Ohio)

| Field | Value |
|---|---|
| Public IP | `3.20.79.143` (Elastic IP, **PERMANENT**) |
| Instance ID | `i-0a3669c59fb773d31` |
| Type | `t3.small` |
| User | `ubuntu` |
| SSH key path (Windows) | `C:\Users\mikeb\.ssh\clawdbot-clean.pem` |
| SSH key issued | 2026-04-08 (replaced compromised `clawdbot-key.pem`) |
| Connect command | `ssh -i C:\Users\mikeb\.ssh\clawdbot-clean.pem ubuntu@3.20.79.143` |
| What runs here | CrawDaddy v1 ACP seller, SN61 Bittensor miner (UID 57), OpenClaw gateway, Moltbook engagement cron, seller watchdog |
| Critical paths | `~/crawdaddy-security/`, `~/.openclaw/`, `~/.bittensor/`, `~/SESSION_HANDOFF.md` |

### VPS (Hostinger)

| Field | Value |
|---|---|
| Public IP | `69.62.69.140` |
| User | `root` (most ops); `selarix` (Paperclip processes) |
| SSH key path (Windows) | `~/.ssh/vps-apr17.pem` (full path: `C:\Users\mikeb\.ssh\vps-apr17.pem`) |
| SSH key NOTE | **Default key auth does NOT work — `-i ~/.ssh/vps-apr17.pem` is required for every command** |
| Connect command | `ssh -i ~/.ssh/vps-apr17.pem root@69.62.69.140` |
| Browser terminal fallback | Available in Hostinger hPanel → VPS → Browser Terminal (no key needed) |
| What runs here | Paperclip (port 3100, as `selarix` user via PM2), Reporter v1.0.5 cron (as root), Polymarket swarm, OpenClaw, SELARIX_INTELLIGENCE.md shared memory |
| Critical paths | `/root/selarix-lattice/`, `/opt/start-paperclip.sh`, `/root/SELARIX_INTELLIGENCE.md`, `/root/.selarix.env`, `/home/selarix/.selarix.env` |
| Env file split | Reporter + root cron jobs read `/root/.selarix.env`. Other adapters expect `/home/selarix/.selarix.env`. **Known config gap — telegram_send.sh fails when run as root.** Fix pending. |

### Local Windows machine

| Field | Value |
|---|---|
| Hostname | HP Omen (Mike's primary dev machine) |
| Home dir | `C:\Users\mikeb\` |
| Node version | v22.14.0 (current LTS+) |
| Local repo: thebinmap | `C:\Users\mikeb\thebinmap\` (Astro 5, fully built, `node_modules` and `dist/` present) |
| Local repo: paperclip | `C:\Users\mikeb\paperclip\` (secondary/backup; primary is on VPS) |
| Local repo: researchbot | `C:\Users\mikeb\researchbot\` (Python; runs daily 6am UTC via PM2 cron — currently disabled per Memory #12) |
| Local repo: acp-cli | `C:\Users\mikeb\acp-cli` (CrawDaddy v2 ACP CLI; run via `npx tsx bin/acp.ts <command>`) |
| Credentials manager | NordPass (replaced Chrome password storage post-Layemor incident 2026-04-03) |
| Stale credential file | `~/.git-credentials` exists, may contain stale GitHub creds — TODO inspect and clean |

---

## Domains and DNS

### thebinmap.com

| Field | Value |
|---|---|
| Registrar | Hostinger |
| DNS provider | Cloudflare (verified via `nslookup`: 104.21.84.151, 172.67.194.47) |
| Hosting | Cloudflare Pages, auto-deploys from `mbennett-labs/thebinmap` main branch |
| Verified live | ✅ 2026-04-25, serving 522 listings across 21 states |
| Live URL | https://thebinmap.com |

### therapistindex.com

| Field | Value |
|---|---|
| Registrar | Hostinger |
| Hosting | Hostinger (WordPress) |
| Stack | WordPress + GeoDirectory + BlockStrap + Yoast SEO + LiteSpeed Cache + Ninja Forms + UsersWP + WP Mail SMTP |
| Listings | ~2,595 |
| Indexed pages | 2,160 (per Search Console as of Apr 22) |

### quantumshieldlabs.dev

| Field | Value |
|---|---|
| Registrar | Hostinger |
| Hosting | Hostinger VPS (`69.62.69.140`) via nginx |
| Subdomains | `paperclip.quantumshieldlabs.dev` (port 3100, Let's Encrypt SSL) |

### thebinmap.com email

6 mailboxes via Hostinger Free Business Email plan, expires 2027-04-17:

| Mailbox | Forwarder configured |
|---|---|
| info@thebinmap.com | ✅ → mikebennett637@gmail.com (verified) |
| michael@thebinmap.com | ✅ |
| privacy@thebinmap.com | ✅ |
| legal@thebinmap.com | ✅ |
| support@thebinmap.com | ✅ |
| hello@thebinmap.com | ✅ |

Mailbox limits: 94/100 remaining. 0% storage used across all.

---

## Project deployment status

### TheBinMap (Tier 2)

| Item | Status |
|---|---|
| Code | ✅ Astro 5 static, 19 commits, complete |
| GitHub repo | `mbennett-labs/thebinmap` (public as of 2026-04-25) |
| Local build | ✅ Verified working at localhost:4321 |
| Production deploy | ✅ Live at thebinmap.com via Cloudflare Pages |
| Listings | 522 across 21 states (TX 100, OH 90, FL 88, TN 75, VA 48, etc.) |
| Search Console | ✅ Domain property registered, sitemap submitted |
| AdSense | ✅ Approved, site connected |
| AdSense Auto ads | ❌ **OFF — single toggle to flip to start serving ads** |
| Contact form | ✅ Working, Web3Forms relay → mikebennett637@gmail.com |
| Search traffic | 0 clicks (too new — Google indexing in progress, expect 30-90 days) |

### TherapistIndex (Tier 2)

| Item | Status |
|---|---|
| Site | ✅ Live, 2,595 listings |
| Indexed pages | 2,160 in Google |
| Blog posts | 12 published under "Therapist Index Editorial" byline |
| AdSense | ✅ Approved and ON (per Apr 25 AdSense screenshot showing "Auto ads ON") |
| Brevo outreach | 2 campaigns sent 2026-03-24 to ~440 contacts (~870 sends total). 6 reactions (3 claims, 3 unsubscribes). 0.7% reaction rate — bottom of B2B cold benchmark. **Not a broken-link issue (verified) — strategy needs traffic-first then re-outreach later.** |
| Known issues | Google Maps API broken on /places/, dual CTAs both link /places/, listings sort "Newest" surfaces low-rated providers |

### CrawDaddy v1 (Tier 1, paused)

| Item | Status |
|---|---|
| Wallet | `0xfBE01B3FA4a480271a215846E3664353A940Fe9b` (replaced Apr 12 — old `0x8c8D...` compromised) |
| Status | Below $500/mo revenue gate; v2 migration plan written, Phase 2 execution queued |
| Runs on | EC2, `~/.openclaw/virtuals-acp/` |

### CrawDaddy v2 (Tier 1, paused)

| Item | Status |
|---|---|
| v2 agent ID | `019db59f-d5bf-782b-9484-064490ea5ba3` |
| v2 wallet | `0xfb3e3609...e3c04` (Base) |
| Token | `$CRAWDAD` ERC-20 at `0x30370E314dc93c5f926677Eb84bdc59372E0E1E3` (Base, 1B supply, 1265 holders) |
| P256 signer | Registered Apr 22; private key in Windows Credential Manager (set by acp-cli on `C:\Users\mikeb\acp-cli`) |
| Currently | OFFLINE in v2 — needs `seller.ts` rewrite for v2 SDK |

### Reporter v1.0.5 (Lattice Layer 1)

| Item | Status |
|---|---|
| Location | `/root/selarix-lattice/toolshed/scripts/reporter_morning_digest.py` |
| Schedule | `0 11 * * *` (cron, root user) — 7 AM EST during DST |
| Output | Telegram via `@SelarixBoard_bot` to chat ID `6712910089` |
| Logs | `/var/log/selarix/reporter/cron.log` + daily snapshots |
| Status | ✅ Live, working since 2026-04-24 evening |
| Backup | `reporter_morning_digest.py.bak.v1_0_4` (untracked, local-only) |

---

## Credentials and accounts

| Service | Account | Notes |
|---|---|---|
| GitHub | `mbennett-labs` | PAT used for VPS pushes (cached 8hr on VPS as of Apr 25) |
| OpenRouter | New account (replaced deleted one Apr 24) | Funded $10 buffer; key in `~/.openclaw/auth.json` on EC2 |
| Anthropic | Multiple keys rotated post-Layemor; 5 stale deleted | New SELARIX-ResearchBot key created (currently disabled per Memory #12) |
| Google | mikebennett637@gmail.com | AdSense, Search Console, Analytics |
| Hostinger | Mike's account | Domain registrar + email + VPS |
| Cloudflare | Mike's account | DNS + Pages for thebinmap.com |
| Web3Forms | Free tier | API key in TheBinMap source code (not placeholder — verified working) |
| Telegram bots | `@blocdev_bot` (Moltbook + chat ID 6712910089) | `@SelarixBoard_bot` (Reporter, token rotated Apr 24 after chat-leak incident) |
| Brevo | Quantum Shield account | Free tier 300 emails/day; 441 contacts in CRM |
| AdSense publisher ID | `pub-8898439032475025` | Sites: thebinmap.com (Auto ads OFF), therapistindex.com (Auto ads ON) |
| NordPass | Mike's vault | Replaces Chrome password manager post-Layemor |

---

## Quick-reference matrix: "where do I go for X?"

| Need | Go here |
|---|---|
| TheBinMap site | https://thebinmap.com |
| TheBinMap GitHub | https://github.com/mbennett-labs/thebinmap |
| TheBinMap deploy logs | dash.cloudflare.com → Pages → thebinmap |
| TheBinMap analytics | search.google.com/search-console (thebinmap.com Domain property) |
| TheBinMap AdSense | adsense.google.com/adsense/u/0/pub-8898439032475025 |
| TherapistIndex admin | therapistindex.com/wp-admin |
| TherapistIndex Search Console | search.google.com/search-console (therapistindex.com property) |
| Brevo outreach | app.brevo.com → Marketing → Email or Automations |
| Lattice repo (canonical) | github.com/mbennett-labs/selarix-lattice |
| Paperclip dashboard | paperclip.quantumshieldlabs.dev |
| EC2 console | aws.amazon.com → EC2 us-east-2 |
| Hostinger VPS | hpanel.hostinger.com → VPS |
| Telegram morning digest | `@SelarixBoard_bot` (chat ID 6712910089) |
| Telegram swarm alerts | `@blocdev_bot` (same chat ID) |

---

## Known broken / known config gaps

Living list of "I know this isn't ideal but it works around it":

1. **VPS SSH requires `-i ~/.ssh/vps-apr17.pem` flag** — default key auth fails. Worth fixing eventually.
2. **Env file split** — `/root/.selarix.env` (root cron) vs `/home/selarix/.selarix.env` (selarix-user processes). `telegram_send.sh` from root fails. Fix: symlink or update adapter.
3. **TherapistIndex Google Maps API** broken on `/places/` page ("Maps failed to load")
4. **TherapistIndex dual CTAs** on home both link to `/places/`
5. **TherapistIndex listings sort** by "Newest" surfaces low-rated providers
6. **CrawDaddy v2 seller offline** — needs SDK rewrite (Phase 2 of migration plan)
7. **ResearchBot + ContentBot disabled** — dead Anthropic key from Layemor rotation, OpenRouter migration not done (Memory #12 TODO)
8. **`.git-credentials` on Windows** — may contain stale GitHub creds, inspect and clean
9. **`/home/mikeb/` and possibly other dirs are accidentally git-initialized on Windows** — discovered today when `git add` worked from wrong directory

---

## Maintenance discipline

This doc gets updated:

- **Immediately** when any infrastructure changes (new server, new domain, key rotation, deploy target change)
- **Immediately** when Claude or Mike asks a question that this doc should have answered but didn't — update it before answering
- **Verified facts only** — if you don't know, mark with ❓ rather than guessing
- **Append "Last verified: YYYY-MM-DD"** at the bottom of any section that's been spot-checked recently

---

## Today's session friction inventory (2026-04-25)

What I had to ask Mike for that should have been here:

1. Where is the lattice repo? (Answer: `/root/selarix-lattice/` on VPS)
2. What's the SSH key for VPS? (Answer: `~/.ssh/vps-apr17.pem`)
3. Where is the local TheBinMap repo? (Answer: `C:\Users\mikeb\thebinmap`)
4. Is TheBinMap deployed yet? (Answer: yes, fully, since ~Apr 19)
5. What's the deploy target — Cloudflare Pages or Vercel? (Answer: Cloudflare Pages)
6. Is AdSense approved for TheBinMap? (Answer: yes, but Auto ads OFF)
7. Does info@thebinmap.com forward? (Answer: yes, to mikebennett637@gmail.com)
8. What email tool sent the claim outreach? (Answer: Brevo)

Each of these cost 5-15 min to ask + verify + correct. Total friction: ~30-45 min today.

**Goal:** zero friction-of-this-type in the next session. Watch this metric drop.

---

*Infrastructure Registry v1 | SELARIX / Quantum Shield Labs LLC | 2026-04-25*
*Verified facts only. Update before next ask.*

## Append 2026-04-25 — TheBinMap data layer + email flow

### TheBinMap data architecture (verified today)

**The 522 listings live in SQLite, NOT in JSON.** Earlier project notes incorrectly suggested data was in JSON files. Reality:

| Path | What it is | Use |
|---|---|---|
| `data/stores.db` (repo root, NOT src/data) | SQLite database, 1MB, 522 rows | **Production data — what the live site renders** |
| `src/data/db.ts` | TypeScript loader (uses sql.js) | Reads stores.db at build time |
| `src/data/listings.json` | 30-store seed file with 25 fabricated placeholders | **Appears unused** — investigate references later, leave for now |
| `src/data/metros.ts` | City/metro mapping helper | TypeScript, build-time |

**SQLite schema (stores table) — 24 columns:**
```
id, google_place_id, name, slug, address, city, state, state_name, zip_code,
latitude, longitude, phone, website, google_maps_url, facebook_url, hours_json,
rating, review_count, store_type, description, verified, featured, last_verified, created_at
```

**Data quality (audited 2026-04-25):**
| Field | Coverage | Notes |
|---|---|---|
| google_place_id | 522/522 (100%) | All from Google Places |
| address | 522/522 (100%) | Real |
| latitude / longitude | 522/522 (100%) | Map embedding ready |
| rating | 497/522 (95%) | Real Google ratings |
| review_count | 497/522 (95%) | Real |
| phone | 415/522 (80%) | Real |
| hours_json | 491/522 (94%) | Structured Google data with weekdayDescriptions array |
| facebook_url | 0/522 | Empty — Sprint 2 enrichment target |
| restock_day | N/A — column doesn't exist | Sprint 2 will add |
| cheapest_day | N/A — column doesn't exist | Sprint 2 will add |
| photos | N/A — not stored | Sprint 2 will add via Place IDs |

**State concentration:**
TX (100), OH (90), FL (88), TN (75), VA (48), NC (34), KY (33), AL (15), GA (10), MS (6), IN/MD/SC (4 each), PA (3), AR (2), CA/DC/LA/MA/MI/OK (1 each).

### TheBinMap email infrastructure (verified today)

**Hostinger Free Business Email plan, expires 2027-04-17. 6 mailboxes, all forwarders configured with "Save copies enabled":**

| Mailbox | Forwards to | Keep copy |
|---|---|---|
| info@thebinmap.com | mikebennett637@gmail.com | ✅ |
| michael@thebinmap.com | mikebennett637@gmail.com | ✅ |
| privacy@thebinmap.com | mikebennett637@gmail.com | ✅ |
| legal@thebinmap.com | mikebennett637@gmail.com | ✅ |
| support@thebinmap.com | mikebennett637@gmail.com | ✅ |
| hello@thebinmap.com | mikebennett637@gmail.com | ✅ |

**Web3Forms submission flow (separate path — does NOT touch Hostinger):**
```
User fills form on thebinmap.com
  → POSTs to api.web3forms.com
  → Web3Forms sends from notify+xxxxxx@web3forms.com
  → Direct delivery to mikebennett637@gmail.com
  (info@thebinmap.com is NOT in this path)
```

**Web3Forms keys present in 3 source files:**
- `src/pages/contact.astro`
- `src/pages/submit.astro`
- `src/pages/claim.astro` (if claim form uses Web3Forms)

**Email-archive enhancement (parked):** To get form submissions in info@ AND gmail, switch Web3Forms delivery destination to info@thebinmap.com. Hostinger forwarder then handles gmail copy automatically. ~20 min when ready.

### TheBinMap site architecture (verified)

| Aspect | Value |
|---|---|
| Framework | Astro 5 (static site generator) |
| Hosting | Cloudflare Pages, auto-deploys from main branch |
| GitHub repo | `mbennett-labs/thebinmap` (public) |
| Local dev | `C:\Users\mikeb\thebinmap`, `pnpm dev` → localhost:4321 |
| Node version | v22.14.0 |
| Build artifact | `dist/` (HTML pre-rendered at build time) |
| AdSense | ✅ Approved + Auto ads ON (as of 2026-04-25) |
| Search Console | ✅ Verified (Domain property) |
| DNS | Cloudflare (104.21.84.151, 172.67.194.47) |

### Today's friction inventory update

Friction questions resolved today that should never need re-asking (already in INFRASTRUCTURE_REGISTRY or now documented above):

1. ❓ "Where does the data live — JSON or DB?" → DB at `data/stores.db` (was confused by `src/data/listings.json` seed)
2. ❓ "Are the 522 listings real?" → Yes, 100% have Google Place IDs and real addresses
3. ❓ "Does info@thebinmap.com forward?" → Yes, with "Save copies" enabled
4. ❓ "Where do Web3Forms submissions land?" → mikebennett637@gmail.com directly, bypasses Hostinger
5. ❓ "Does /stores page exist?" → Yes, alphabetical full-directory listing of all 522
6. ❓ "Is AdSense approved for TheBinMap?" → Yes, Auto ads now ON

**Friction goal:** zero same-question re-asks in next session. Watch this metric.

---

