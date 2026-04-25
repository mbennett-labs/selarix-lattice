# CAMPAIGNS LOG

**Document type:** Living log — append-only
**Status:** Canonical, growing
**Location:** `/operating/CAMPAIGNS_LOG.md`
**Last updated:** 2026-04-25 by Mike + Claude
**Convention:** Newest campaigns at the top. One entry per outreach effort (email, ad, social, partnership push).

---

## Why this doc exists

The TherapistIndex broken-Brevo-link incident — 870 emails sent in March 2026 with a non-functional CTA, undiscovered for 31 days — is the textbook reason this log exists. Campaigns get sent, results get vaguely remembered, lessons get lost. Months later, someone asks "what happened with the claim outreach" and the answer is fragmented across Gmail, Brevo, WordPress, and old chat sessions.

This log is the single source of truth for outreach activity. **One entry per campaign. Watch metrics every 7 days post-send. Document lessons. Flag failures explicitly.**

---

## Entry format

```
### [Project] [Campaign name] — [Send date]

**Tool:** Brevo / Mailchimp / Gmail / etc.
**Audience:** Source + size
**Send:** Date, count, segments
**Email content:** Subject line + 1-line summary of CTA
**Hypothesis:** What you expected to happen
**7-day metrics:** Open rate / click rate / unsubscribe rate / conversion (define)
**Result vs hypothesis:** Won / lost / mixed / undiagnosed
**Lessons:** What this campaign actually tells you
**Status:** Active / Paused / Closed
**Next action:** Specific next step + owner + ETA
```

---

## Campaigns

### [TherapistIndex] Claim-listing outreach #1 (Automation #1) — 2026-03-24

**Tool:** Brevo (free tier, 300 emails/day cap)
**Audience:** 434 therapist contacts (subset of 441 total in Brevo CRM); pulled from public listing data
**Send:** March 24, 2026; 434 emails delivered via "Automation #1"
**Email content:**
- Subject: (not captured in screenshot — needs Brevo dig)
- CTA: "View & claim your listing here"
- CTA target: SUPPOSED to point to each therapist's individual listing URL on TherapistIndex via `{{ contact.LISTING_URL }}` template variable
- ACTUAL CTA target: `https://app.brevo.com/automation/edit/%7B%7B%20contact.LISTING_URL%20%7D%7D` — **broken**. Pointed to Brevo's own automation editor with an unrendered template variable URL-encoded into the path.

**Hypothesis:** ~5-15% open rate, ~1-3% click rate, ~5-15 claims from the 434 (warm-ish list of public-data-sourced therapists in DC/MD/VA).

**7-day metrics:** Not captured at the time. To recover from Brevo dashboard:
- [ ] Open rate
- [ ] Click rate (will be artificially low — broken link still counts as "clicked" but lands on Brevo error page)
- [ ] Unsubscribe rate
- [ ] Bounce rate

**Result vs hypothesis:** ~3 claims and ~3 unsubscribes (per Mike's recollection). Catastrophically low — but **NOT** because the strategy was wrong. The CTA link was broken. Conversions came from people who manually navigated to TherapistIndex, not from the email link.

**Lessons:**
1. **TEST THE EMAIL LINK BEFORE SEND.** Send to your own email first. Click the CTA. Confirm it lands where you intend. This is non-negotiable.
2. **The Brevo template variable `{{ contact.LISTING_URL }}` does not auto-resolve when prefixed with another URL.** Either the field doesn't exist on contacts, OR Brevo's editor wrapped the variable into its own base URL during template construction.
3. **Watching metrics for 7 days post-send is the lesson Mike was missing.** A 0% click rate would have surfaced the broken link in 24 hours. Instead, the campaign sat broken for 31 days.

**Status:** Closed (and broken). Do NOT re-send this automation as-is.

**Next action:**
1. Sequence Claude Code job to:
   - Verify whether `LISTING_URL` is a real custom contact field in Brevo
   - If yes: confirm the field is populated for all 441 contacts (likely it isn't, since Brevo wrapped the unresolved variable)
   - If no: create the field and populate from WordPress listings export (match by therapist name + city/state)
   - Fix the email CTA: plain hyperlink to `{{ contact.LISTING_URL }}`, no Brevo URL prefix
   - Pause the existing automation while fixing
2. Test send to Mike's own email; click CTA; confirm landing page
3. Resend to a 20-30 contact test segment; wait 7 days; measure
4. If conversion is reasonable (target: 3-5% click → claim), expand to remaining contacts
5. If conversion is still poor with working link, then it's a strategic problem and we revisit messaging/audience

**Owner:** Claude Code job; Mike approves before send to test segment.
**ETA:** Not today (deferred to dedicated Claude Code session).

---

### [TherapistIndex] Blog promo to therapist list (TherapistIndex Blog Campaign March 2026) — 2026-03-24

**Tool:** Brevo
**Audience:** 436 therapist contacts (similar overlap with claim-listing list)
**Send:** March 24, 2026; 436 emails delivered
**Email content:**
- Subject: "Your patients are googling these 3 questions"
- Primary message: Promote 3 new TherapistIndex blog posts (federal layoff therapy, insurance comparison, psychiatrist/therapist/psychologist/counselor differences)
- Secondary CTA: "View & claim your listing here" — **same broken link as Automation #1**

**Hypothesis:** Drive blog traffic from therapists themselves (warming them up to TherapistIndex as a useful resource), with secondary claim-listing nudge.

**7-day metrics:** Not captured. To recover from Brevo dashboard.

**Result vs hypothesis:** Mixed-purpose email; primary blog promo CTA may have worked partially; secondary claim CTA broken. Cannot disentangle without metrics.

**Lessons:**
1. **Mixed-purpose emails are diagnostically expensive.** When the primary and secondary CTAs are different, you can't tell which one worked or didn't. Future: one campaign = one CTA.
2. **Same broken-link bug as Automation #1** confirms this was a template-construction issue, not a one-off mistake. Likely both automations were built from the same broken email template draft.

**Status:** Active per Brevo dashboard (2026-04-25). **Should be paused** until link is fixed — currently still capable of sending broken links to any new contacts added.

**Next action:**
1. **Pause this automation in Brevo dashboard immediately** (Manage status → Pause)
2. After fixing the link in Automation #1, decide whether this blog-promo campaign should be re-sent at all (mixed-purpose lesson suggests redesigning into a focused single-CTA email)

**Owner:** Mike (UI click for pause); then sequenced into Claude Code job.
**ETA:** Pause today (2 minutes); redesign decision deferred.

---

## Pre-pipeline campaigns (registered retroactively)

(None other than the two above currently known. If older outreach efforts are remembered or discovered in dashboard digs, add here.)

---

## Discipline rules

1. **Every outreach campaign gets an entry, even if it bombs.** Especially if it bombs.
2. **Test the CTA before send.** Email to yourself, click every link, confirm landing page is the intended one. Take screenshot if needed for paranoia.
3. **Set a 7-day-post-send check** on calendar at moment of send. Pull metrics. Update entry. Mark Result.
4. **One CTA per email.** Mixed-purpose emails are diagnostically expensive and convert worse.
5. **Entry status reflects current truth.** A 31-day-old broken automation marked "Active" in Brevo while this log says nothing is the failure mode. Status here matches reality, even if it means writing "still broken."
6. **Lessons section is the gold.** Three months from now, the lessons are what get re-read before the next campaign. Make them specific and actionable.

---

## Categorization helpers (for future Ctrl+F)

**By Project:**
- TherapistIndex: 2 entries (both broken — see above)

**By Tool:**
- Brevo: 2 entries

**By Status:**
- Active: 1 (Blog Campaign — needs immediate pause)
- Closed: 1 (Automation #1 — needs Claude Code fix)

**By Result:**
- Won: 0
- Lost / Undiagnosed-due-to-broken-CTA: 2

---

*Campaigns Log v1 | SELARIX / Quantum Shield Labs LLC | 2026-04-25*
*Test the link. Watch the metrics. Document the lesson. Or repeat the mistake.*
