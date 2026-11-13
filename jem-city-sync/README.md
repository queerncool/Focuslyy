# Jem Social city pages: daily build

`jem_sync.py` builds the data-backed pages at jem.social/influencers/... (Webflow collection
"City Influencer Pages"). It builds pages in this order, with buyer searches first:

1. National lists whose searches are mostly buyers (golf, fashion, micro, beauty, food, nano, travel).
2. Every city's hub page ("{city} influencers").
3. Food pages ("{city} foodie").
4. Fitness, beauty and fashion pages.

- **Webflow:** read and written directly through the Webflow API. The cloud environment's network secret
  adds the token; a `WEBFLOW_TOKEN` variable works too.
- **Jem data:** comes from `search_influencers` calls (Jem Social connector) made in the same Claude
  session. The script reads their results from the session transcript.

## Daily run

1. `python3 jem_sync.py plan` picks up to 10 new pages and 4 stale ones (27+ days old, or built under
   older page rules). It prints one `search_influencers` argument set per page.
2. Make those searches.
3. `python3 jem_sync.py run` picks creators, uploads photos, writes and publishes the pages, and syncs
   robots tags. It's safe to rerun.
4. `python3 jem_sync.py report` prints a one-paragraph summary for Telegram.

## Page rules

- **Building:** a page is built only with 5+ creators who pass the filters:
  - 5k+ followers
  - engagement between 0 and 20%
  - a photo
  - for niche pages, a profile name that doesn't point to a different niche

  New pages go live as `noindex, follow`.
- **Indexing:** a page is indexed only when its Approved switch is on and it shows 10+ creators.
  `python3 jem_sync.py approve SLUG...` approves pages, publishes them, and prints the 301s to add in
  Webflow (from the page's Old URLs field).
- **Too few creators:** pages with fewer than 5 are saved as drafts marked `skip:` and retried after 60 days.
- **The two biggest lists** (UGC creators, fitness) show up to 50 creators from two result pages (`'show'`, `'pages'` in
  `TOPICS`) and a follower-size breakdown from four count searches (`'tiers'`). Their headline total is the sum of the four
  bands, because Jem's estimates vary slightly between calls. Platform counts aren't shown: Jem's platform filter returns
  wrong totals (Nov 2026).

## Maintenance commands

- `FORCE=slug,slug python3 jem_sync.py plan` adds those pages to today's refresh, then `run` as usual.
- `python3 jem_sync.py relink [--dry]` rewrites the "Browse all" links on every live city page (the US list for the
  page's niche, UGC creators, the platforms comparison, the calculator) and adds a "Compare platforms" column to
  national lists, without new Jem searches. `ONLY=slug,slug` limits it to those pages.
- **Platforms link (Nov 13, 2026):** every city, niche and national page links to
  `/find-influencers/top-influencer-marketing-platforms` (`PLATFORMS` in `jem_sync.py`). New and refreshed pages get it
  from `render()`; existing pages got it from `relink`. The old related-links blocks are backed up outside the repo.
- `python3 old_pages.py check|unpublish|verify FILE` retires old /find-influencers/ pages once their redirects exist.

## Updating the scheduled task

The scheduled task ("Jem city pages daily build") doesn't run this repo copy, and it doesn't download anything:
the run's safety check blocks code fetched from a URL ("Code from External"), which stopped the Oct 27 run.
Instead, `jem_sync_task.py` is embedded at the end of the task's prompt, between `#BEGIN-JEM-SYNC` and
`#END-JEM-SYNC`, and setup step 1 unpacks it and checks its MD5.

`jem_sync_task.py` is generated: `python3 make_task_copy.py` strips comments, docstrings and the in-session-only
commands (`approve`, `relink`, marked in `jem_sync.py`). Task prompts are limited to 64 KB (65,536 bytes); the
Nov 13 prompt is 64,789 bytes, so about 750 bytes are left. After changing `jem_sync.py`:

1. Run `python3 make_task_copy.py`. It prints the size and MD5.
2. Replace the embedded copy in the task's prompt with `jem_sync_task.py`, without its trailing newline, and put
   the new MD5 in setup step 1.
3. Read the task back and check that the embedded copy matches `jem_sync_task.py` byte for byte.

If a change doesn't fit, split the work: for example, move the national lists to a second scheduled task.
