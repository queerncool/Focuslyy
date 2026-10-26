# jem.social/afrotech-2026-events

This folder is not part of the focuslyy app. It holds the generator for the email-gated AfroTech 2026 events page on
jem.social (Webflow page `afrotech-2026-events`, id `6adefdc4a265abb2dd138171`).

Source list: Keith Azodeh's "Afrotech Events" Google Sheet (afrotech.guide), tab `_Event Feed`. The page credits and links him.

- `build.py <sheet.xlsx> <out_dir>`: turns the sheet into the page's HtmlEmbed snippets. It drops exact duplicate rows,
  fixes "9 PM to 2 PM" end times to 2 AM, and computes every count shown on the page from the data.
  Sun + Mon stay open; Tue to Sat render blurred inside the `data-afro="lock"` block until the visitor submits the form.
- `mkpreview.py <dir>` + `shot.js <dir>`: local mock of the Webflow structure, with screenshots and unlock/filter checks.
- `verify.py <get_settings result> <out_dir>`: diffs the embed code read back from Webflow against the generated files.

Page structure in Webflow: head embed (styles, nav) → hero section with native form "AfroTech 2026 List"
(Email, Role, hidden Source) → preview embed → lock block (4 day embeds + overlay) → tail embed (FAQ, footer, unlock script).
Submissions land in Webflow → Forms. The unlock state is kept in localStorage key `jem_afrotech26`.
