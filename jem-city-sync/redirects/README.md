# Redirect files

The Webflow dashboard import replaces every existing rule, so each import file must hold all rules.
Files sent to the owner so far: jem-redirects-146.csv (146 rows, Nov 24), then the 10 wildcard rules added by hand.
`jem-redirects-add-5-rows.csv` holds five more rows (Nov 25) that go at the bottom of the 146 file:
three influencer-marketing-campaign duplicates and two local-influencer-marketing duplicates.
The 146 file itself lived in a scratch folder that was wiped on Nov 24, so ask for the imported copy before running
`old_pages.py unpublish`.
