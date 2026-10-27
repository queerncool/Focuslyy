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

## Updating the scheduled task

The scheduled task ("Jem city pages daily build") doesn't run this repo copy. A copy of the script is
embedded at the end of the task's prompt, between `#BEGIN-JEM-SYNC` and `#END-JEM-SYNC`. Setup step 1
unpacks it from the session transcript and checks its MD5. Don't have the task download the script:
the run's safety check blocks running code fetched from a URL ("Code from External"), and that
stopped the Oct 27 run. After changing `jem_sync.py`:

1. Replace the embedded copy in the task's prompt with the new file, without its trailing newline.
2. Put the new file's MD5 (`md5sum jem_sync.py`) in setup step 1.
3. Read the task back and check that the embedded copy's MD5 matches.
