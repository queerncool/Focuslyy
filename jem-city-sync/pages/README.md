# Buyer-page builders

Scripts that build the rewritten /find-influencers/ pages. Nothing here writes to Webflow: each `build_*.py` writes
`out/<name>_patch.json` (the `fieldData` to PATCH) and `preview.js` renders it on the live template.

    cd pages && python3 build_pay.py
    NODE_PATH=$(npm root -g) node preview.js pay-influencers pay_patch.json prev_pay

The shared CSS embed is read from the live micro-influencer-platform page's `hero-description`.
`../page-backups/` holds the Webflow items as they were before a rewrite, and snapshots of pages already live.
To publish: PATCH the item with the patch, then POST `/collections/{OLD_COLL}/items/publish`. Setting `robots` to null makes a page indexable.
