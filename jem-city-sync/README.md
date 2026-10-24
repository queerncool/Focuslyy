# Jem Social city pages: weekly sync

This folder is not part of the focuslyy app. It holds the script for the scheduled job that fills
jem.social's "City Influencer Pages" Webflow collection with real Jem Social creator data.

- `jem_sync.py`: renders each page from Jem Social search results (`plan` → `photos` → `upload` → `build` → `report`).
  The step-by-step runbook is in the scheduled task's prompt.
- Queue: draft items in the Webflow collection. The job builds up to 10 queued pages and refreshes up to 5 pages
  older than 27 days per run.
- Go-live gate: the **Approved** switch on each CMS item. Unapproved pages stay `noindex, follow` and are never
  pushed to the live site by the job.
- Removal requests: add the handle to **Exclude handles** on any item; the next run drops it everywhere.
