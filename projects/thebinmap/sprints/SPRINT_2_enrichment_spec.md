# TheBinMap — Sprint 2: Google Places Enrichment + Restock Day Extraction
**Status:** Specced 2026-04-25, ready for tomorrow's Claude Code execution
**Operator:** Mike supervising Claude Code on Windows
**Working dir:** `C:\Users\mikeb\thebinmap`
**Estimated time:** 2-3 hours total (1 hr setup + script, 1-2 hrs execution + verification)
**Estimated cost:** ~$10 one-time, ~$120/year for monthly refresh
**Prerequisites:** GCP Places API enabled + billing account attached on the project owning the existing thebinmap server key

---

## Goal

Add the data fields that the audit identified as missing from listing pages, using Google Places API as the primary source and LLM extraction (DeepSeek via OpenRouter) for restock day inference from review text.

## What this sprint adds to every listing

| Field | Source | Coverage target |
|---|---|---|
| `restock_day` | LLM extraction from Google Places `reviews[]` text | 30-50% of listings (only those with rich reviews) |
| `cheapest_day` | LLM extraction from Google Places `reviews[]` text | 20-40% (similar) |
| `price_ladder` | LLM extraction (e.g., "Fri $10, Sat $7, Sun $4, Mon $1") | 15-30% (most precise field) |
| `photos[]` | Google Places `photos` field | 70-90% (most stores have photos) |
| `facebook_url` | Google Places `socialMedia` field if present | 30-60% |
| `openNow` real-time fix | Client-side computation from existing `periods` array | 100% |

## What this sprint does NOT do

- Does NOT call external APIs from the live site (still static deploy)
- Does NOT modify the user-facing template significantly (template tweaks are separate Sprint 2.5)
- Does NOT replace any existing data — only ADDS columns
- Does NOT touch the seed `src/data/listings.json` file
- Does NOT scrape Facebook (out of scope for this sprint)

---

## Pre-flight checks (Claude Code does these BEFORE main run)

### Check 1 — GCP project setup verified
```bash
# Use the existing thebinmap server key (from NordPass: "Google-thebinmap-thebinmap-server-key")
# Test single Place Details call against a known good place_id from stores.db

curl -X POST -d '{}' \
  -H "Content-Type: application/json" \
  -H "X-Goog-Api-Key: $GOOGLE_API_KEY" \
  -H "X-Goog-FieldMask: id,displayName,formattedAddress,internationalPhoneNumber,websiteUri,regularOpeningHours,photos,reviews,rating,userRatingCount" \
  "https://places.googleapis.com/v1/places/ChIJ_YttWY6hToYRyv__tY4dVTk"
```

**Expected:** 200 OK with full JSON response.

**Failure modes to handle:**
- 403 with "API not enabled" → Halt. Print clear remediation: "Enable Places API (New) at https://console.cloud.google.com/apis/library/places.googleapis.com"
- 403 with "billing not enabled" → Halt. Print: "Attach a billing account to the GCP project (free tier still applies)"
- 401 with "invalid API key" → Halt. Print: "Verify the API key value matches the one in NordPass"

### Check 2 — Cost estimate confirmed
```python
# Print cost calculation BEFORE bulk run starts
print(f"About to make {LISTINGS_TO_PROCESS} Google Places API calls.")
print(f"Estimated cost: ~${LISTINGS_TO_PROCESS * 0.017:.2f}")
print(f"Plus LLM extraction: ~${LISTINGS_TO_PROCESS * 0.0001:.2f} via OpenRouter/DeepSeek")
print(f"Total estimated: ~${LISTINGS_TO_PROCESS * 0.0171:.2f}")
print("Continue? [y/N]: ")
```

**Mike must type 'y' to proceed.** Defensive against accidental full-run.

### Check 3 — Backup the database
```bash
cp data/stores.db data/stores.db.bak.$(date +%Y%m%d-%H%M%S)
```

Always. Before any schema mutation. If anything breaks, we restore.

---

## Phase 1 — Schema additions (5 min)

Add columns to the `stores` table. Use SQLite `ALTER TABLE` (only ADD COLUMN works in SQLite — that's fine for our case).

```sql
ALTER TABLE stores ADD COLUMN restock_day TEXT;
ALTER TABLE stores ADD COLUMN cheapest_day TEXT;
ALTER TABLE stores ADD COLUMN price_ladder TEXT;
ALTER TABLE stores ADD COLUMN photos_json TEXT;
ALTER TABLE stores ADD COLUMN socials_json TEXT;
ALTER TABLE stores ADD COLUMN enrichment_run_at TEXT;
ALTER TABLE stores ADD COLUMN enrichment_confidence TEXT;  -- 'high' | 'medium' | 'low' | 'none'
```

Update `src/data/db.ts` `Store` interface to add the new fields:

```typescript
export interface Store {
  // ... existing fields
  restock_day: string | null;          // e.g., "Friday" | "Friday morning" | null
  cheapest_day: string | null;         // e.g., "Wednesday" | null
  price_ladder: string | null;         // e.g., "Fri $10 → Sat $7 → Sun $4 → Mon $1" | null
  photos_json: string | null;          // JSON array of photo URLs
  socials_json: string | null;         // JSON object {facebook, instagram, tiktok}
  enrichment_run_at: string | null;    // ISO timestamp
  enrichment_confidence: string | null;  // 'high' | 'medium' | 'low' | 'none'
}
```

---

## Phase 2 — Test run on 10 listings (15 min + manual review)

**DO NOT run on all 522 immediately.** Run on a curated sample first:

```python
# Pick 10 representative listings:
# - 5 high-review (likely rich review text for LLM extraction)
# - 3 medium-review
# - 2 low-review (test what happens with thin data)

test_query = """
SELECT id, name, city, state, google_place_id, review_count
FROM stores
WHERE google_place_id IS NOT NULL
ORDER BY 
  CASE 
    WHEN review_count > 1000 THEN 1
    WHEN review_count BETWEEN 100 AND 1000 THEN 2
    WHEN review_count > 0 THEN 3
    ELSE 4
  END,
  RANDOM()
LIMIT 10
"""
```

Run enrichment on these 10. Print results to terminal in human-readable format. **Mike manually verifies:**
- Restock days extracted: do they match what reviews actually say? (Spot-check by visiting Google Maps for 3 of them.)
- Cheapest days: same check.
- Photos returned: do URLs work? Open 2 in browser.
- Facebook URLs: do they exist? Open 1.

**If quality is poor:** iterate on the LLM prompt before bulk run. **If quality is good:** proceed to Phase 3.

---

## Phase 3 — Bulk enrichment run on all 522 (30-60 min runtime)

```python
# Pseudocode flow per listing:

for store in get_stores_needing_enrichment():
    try:
        # 1. Fetch from Google Places API (New)
        place_data = fetch_place_details(store.google_place_id, fields=[
            'id', 'displayName', 'formattedAddress', 'internationalPhoneNumber',
            'websiteUri', 'regularOpeningHours', 'photos', 'reviews',
            'rating', 'userRatingCount'
        ])
        
        # 2. Extract photos (just URLs, no fetching the actual images)
        photos = []
        for photo_ref in place_data.get('photos', [])[:5]:  # cap at 5 per store
            photo_url = f"https://places.googleapis.com/v1/{photo_ref['name']}/media?key={API_KEY}&maxHeightPx=400"
            photos.append(photo_url)
        
        # 3. Extract review text for LLM
        review_texts = [r['text']['text'] for r in place_data.get('reviews', [])[:8]]  # most recent 8
        
        # 4. LLM extraction (only if review_texts has substantive content)
        if len(' '.join(review_texts)) > 200:  # at least 200 chars total
            extracted = call_openrouter_deepseek(LLM_EXTRACTION_PROMPT, review_texts)
            # extracted = {'restock_day': '...', 'cheapest_day': '...', 'price_ladder': '...', 'confidence': '...'}
        else:
            extracted = {'restock_day': None, 'cheapest_day': None, 'price_ladder': None, 'confidence': 'none'}
        
        # 5. Update DB row
        update_store(store.id, {
            'restock_day': extracted['restock_day'],
            'cheapest_day': extracted['cheapest_day'],
            'price_ladder': extracted['price_ladder'],
            'photos_json': json.dumps(photos) if photos else None,
            'socials_json': json.dumps({'facebook': place_data.get('socialMedia', {}).get('facebook')}) if place_data.get('socialMedia') else None,
            'enrichment_run_at': datetime.utcnow().isoformat() + 'Z',
            'enrichment_confidence': extracted['confidence'],
        })
        
        log_success(store.id)
        
    except RateLimitError:
        sleep_with_backoff()
        retry
    except PlaceNotFoundError:
        log_skip(store.id, reason='place_not_found')
        continue
    except Exception as e:
        log_error(store.id, error=str(e))
        continue
    
    # Rate limit: respect Google's 100 req/sec but throttle to ~10 req/sec for safety
    time.sleep(0.1)
```

**Output:** Updated `data/stores.db` + `enrichment-run-YYYYMMDD.log` with per-listing outcomes.

---

## LLM extraction prompt (DeepSeek via OpenRouter)

```
You are extracting bin store operational details from Google Maps reviews. 
The reviews are for a single store. Identify factual statements about:

1. RESTOCK DAY — When does the store restock or refresh inventory? 
   Look for phrases like "they restock on Friday", "new stuff arrives Saturday morning", 
   "Friday is the best day", "fresh bins on Thursday evening".

2. CHEAPEST DAY — When are prices lowest? Look for phrases like 
   "$1 day is Wednesday", "everything's a buck on Sunday", "Tuesday is cheap day".

3. PRICE LADDER — Specific pricing across days. E.g. "Friday $10, Saturday $7, 
   Sunday $4, Monday $1". Only extract if multiple days + prices are explicit.

Rules:
- Only extract if MULTIPLE reviews mention the same day, OR if a single review 
  states it confidently as fact (not opinion).
- Return null if no clear pattern emerges. Do NOT guess.
- Format restock_day and cheapest_day as bare day names ("Friday", "Saturday morning") 
  not full sentences.
- Format price_ladder as "Fri $X → Sat $Y → Sun $Z → Mon $W" or null.
- Set confidence: 'high' if 3+ reviews agree, 'medium' if 2 agree, 
  'low' if single confident mention, 'none' if no signal.

Reviews:
{review_texts}

Respond with ONLY a JSON object:
{
  "restock_day": "..." or null,
  "cheapest_day": "..." or null,
  "price_ladder": "..." or null,
  "confidence": "high" | "medium" | "low" | "none"
}
```

**Model:** `deepseek/deepseek-chat` via OpenRouter. Cheap (~$0.0001 per call), good enough for structured extraction.

---

## Phase 4 — Display layer updates (separate template work, ~30 min)

After enrichment lands, update `src/pages/store/[slug].astro` to render the new fields:

```astro
<!-- In the right sidebar Store Info block, add: -->

{store.restock_day && (
  <div class="info-item">
    <h3>RESTOCK DAY</h3>
    <p>{store.restock_day}</p>
  </div>
)}

{store.cheapest_day && (
  <div class="info-item">
    <h3>CHEAPEST DAY</h3>
    <p>{store.cheapest_day}</p>
  </div>
)}

{store.price_ladder && (
  <div class="info-item">
    <h3>PRICING</h3>
    <p>{store.price_ladder}</p>
  </div>
)}

<!-- In the main content area, after About section: -->

{store.photos_json && (() => {
  const photos = JSON.parse(store.photos_json);
  return photos.length > 0 && (
    <section class="photos">
      <h2>Photos</h2>
      <div class="photo-grid">
        {photos.slice(0, 3).map(url => (
          <img src={url} alt={`${store.name} photo`} loading="lazy" />
        ))}
      </div>
    </section>
  );
})()}
```

### openNow real-time fix (separate from main enrichment)

Replace the static `openNow` from `hours_json` with build-time computation:

```typescript
function isOpenNow(periods, currentDate = new Date()): boolean {
  const day = currentDate.getDay(); // 0=Sunday, 6=Saturday
  const minutesIntoDay = currentDate.getHours() * 60 + currentDate.getMinutes();
  
  for (const period of periods || []) {
    if (period.open?.day === day) {
      const openMinutes = period.open.hour * 60 + (period.open.minute || 0);
      const closeMinutes = period.close.hour * 60 + (period.close.minute || 0);
      if (minutesIntoDay >= openMinutes && minutesIntoDay < closeMinutes) {
        return true;
      }
    }
  }
  return false;
}
```

**Caveat:** Astro builds at deploy time, so "build-time openNow" is still stale by the time a user visits. **Best approach:** Compute openNow client-side in a small `<script>` block on the listing page that runs on page load. ~15 lines of vanilla JS, no dependencies.

---

## Phase 5 — Cleanup + verify (15 min)

After display layer updates:

1. **Verify on 5 random listings:** new fields render where data exists, hide cleanly where data is null
2. **Spot-check Google Maps:** for 3 listings with extracted restock_day, verify against actual Google Maps reviews
3. **Commit + push:** all enrichment script + template changes in clean commits
4. **Update `projects/thebinmap/status/`:** new dated status file showing enrichment metrics
5. **Append to `operating/DECISIONS_LOG.md`:** what shipped, what failed, lessons

---

## Sprint 2 success criteria

- [ ] At least 30% of 522 listings (≥157) have a non-null `restock_day` after enrichment
- [ ] At least 70% of 522 listings (≥365) have non-empty `photos_json`
- [ ] All listings retain accurate hours, map, and rating displays
- [ ] No data corruption — backup is untouched and matches restore-able
- [ ] Total cost actually spent: under $15 (estimate $10)
- [ ] Real-time `openNow` works correctly on Saturday afternoons (the bug we caught today)

---

## What gets queued for Sprint 3

- Sprint E (claim outreach) to top-100 by review_count
- Photo carousel UX improvements
- Restock-day filter on /states/[state] pages
- "Open now" filter across the directory
- Schema markup for restock day (so Google search snippets show it)

---

## File outputs from this sprint

When complete, the repo should have:

```
data/
  stores.db                              # enriched
  stores.db.bak.YYYYMMDD-HHMMSS          # safety backup
scripts/
  enrich.py                              # the enrichment script (new)
  README.md                              # how to run it (new)
logs/
  enrichment-run-YYYYMMDD.log            # run log
src/data/db.ts                           # updated Store interface
src/pages/store/[slug].astro             # renders new fields
projects/thebinmap/status/2026-04-26.json   # post-sprint status
operating/DECISIONS_LOG.md               # appended with sprint outcomes
```

---

## Pre-flight checklist for Mike (do this BEFORE running Claude Code)

- [ ] Open https://console.cloud.google.com/
- [ ] Select the project that owns the `Google-thebinmap-thebinmap-server-key`
- [ ] Navigate: APIs & Services → Library → search "Places API (New)" → Enable
- [ ] Navigate: Billing → confirm a billing account is attached (free tier still applies)
- [ ] Have the API key value from NordPass ready to paste when Claude Code prompts
- [ ] Open OpenRouter account, confirm balance ≥$5 (sprint uses ~$0.05 in DeepSeek calls but buffer is safety)
- [ ] OpenRouter API key handy (already in `~/.openclaw/auth.json` on EC2 — may need to add to Windows env or NordPass)

---

## Estimated session timeline

| Time | Activity |
|---|---|
| 0:00 – 0:10 | GCP setup verified, billing confirmed |
| 0:10 – 0:30 | Claude Code reads spec, sets up script scaffolding, schema migration |
| 0:30 – 0:45 | Test run on 10 listings, manual quality check |
| 0:45 – 1:30 | Bulk run on remaining 512 listings (with rate limit pacing) |
| 1:30 – 2:00 | Display layer updates in template |
| 2:00 – 2:15 | Verify on live site after deploy |
| 2:15 – 2:30 | Cleanup, commit, push, update operating docs |

**Total: 2.5 hours of supervised execution.**

---

*Sprint 2 spec drafted 2026-04-25 by Claude Opus 4.7 + Mike Bennett. Ready for execution against fresh energy.*
