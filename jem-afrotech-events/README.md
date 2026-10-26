# jem.social/afrotech-2026-events

This folder is not part of the focuslyy app. It holds the generator for the email-gated AfroTech 2026 events page on
jem.social (Webflow page `afrotech-2026-events`, id `6adefdc4a265abb2dd138171`).

Source data: an AfroTech events sheet (tab `_Event Feed`). The page presents it as organized by Jem Social from public listings.

- `build.py <sheet.xlsx> <out_dir>`: turns the sheet into the page's HtmlEmbed snippets. It drops exact duplicate rows,
  fixes "9 PM to 2 PM" end times to 2 AM, and computes every count shown on the page from the data.
  Events are grouped into category sections (parties, networking, career, founders, workshops, culture), each event
  listed once under its best-fit type. Visitors browse by category tab and filter by price, type or day. In each section
  the first 2 events are open, the next 2 are blurred and the rest stay hidden until the visitor submits the form.
  Jem Social's own events (The Green Room, Sapphic Hour) are pinned in a "Jem Social picks" block at the top.
- `mkpreview.py <dir>` + `shot.js <dir>`: local mock of the Webflow structure, with screenshots and unlock/browse/filter checks.
- `track.js <dir>`: checks UTM capture into hidden form fields and the GA4 / Plausible / Meta / TikTok events.
- `verify.py <get_settings result> <out_dir>`: diffs the embed code read back from Webflow against the generated files.

Page structure in Webflow: head embed (styles, nav) → hero section with native form "AfroTech 2026 List"
(Email, Role, hidden Source, utm_source/medium/campaign/content, Referrer) → preview embed (filter bar, picks, first
sections) → lock block (L1–L4 category embeds + bottom unlock card) → tail embed (cross-sell, FAQ, footer, script).
The unlock state is kept in localStorage key `jem_afrotech26`; `?unlock=1` (used in the email) also unlocks.

## Signup email and ROI tracking

- Webflow webhook (form_submission, "AfroTech 2026 List") → Make scenario 6778857 → Brevo:
  sends the list email from bree@jem.social (`make/email.html`, tag `afrotech-2026-list`) and upserts the contact into
  Brevo list 27 with AT26_ROLE, AT26_SOURCE, AT26_POST and AT26_DATE. `make/bp.json` is the scenario blueprint.
- Conversion events on the page: GA4 `generate_lead`, `afrotech_event_click`, `afrotech_signup_click`,
  `afrotech_category`; Plausible `AfroTech Signup`, `AfroTech Event Click`, `AfroTech Jem Signup Click`,
  `AfroTech Category`; Meta `Lead`; TikTok `SubmitForm`.
- Jem signup links carry `source=afrotech_2026_*` (page: list, creator, brand; email: email_creator, email_brand).
- Revenue: Brevo list 27 contacts whose SUBSCRIPTION_STATUS / PAID_START_DATE show a paid plan after AT26_DATE.

## Carousels and post times

- `carousels/slides.py <out>` renders the Instagram slides. `carousels/slides.py <out> threads` renders the Threads version, where "Comment LINK" becomes "Link in replies".
- `carousels/render.js <html dir> <png dir>` turns the slides into 1080×1350 PNGs and flags any text overflow.
- `carousels/captions.md` holds every caption, DM reply and Threads first reply, plus their scheduled times.
- `best-times/` has the @jemsocialapp timing analysis behind those times (Instagram 7 pm CT, Threads 1 pm CT). Re-run it before scheduling the next campaign.
