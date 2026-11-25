from pagelib import *
SLUG = 'local-influencer-marketing'
FTC = 'https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers'
TODAY = 'November 25, 2026'

cities = json.load(open(SP + 'city_counts_nov25.json'))
ranked = sorted(cities.items(), key=lambda x: -x[1]['n'])
N = len(ranked); n = lambda x: f'{x:,}'
top, rest = ranked[:20], sorted(ranked[20:], key=lambda x: x[1]['h1'])
assert N >= 60, N
city_rows = [[a(f'{JEM}/influencers/{s}', v['h1']), n(v['n'])] for s, v in top]
rest_items = ''.join(f'<li>{a(f"{JEM}/influencers/{s}", v["h1"])} ({n(v["n"])})</li>' for s, v in rest)

guide = (
    '<div data-rt-embed-type="true"><div id="Creators"></div></div>'
    '<h3>What local influencer marketing is</h3>'
    '<p>Local influencer marketing means working with creators whose followers live in the area you serve. It suits businesses with a location or a service area, such as restaurants, salons, gyms, shops and event venues. A local campaign is usually judged on visits, bookings and local sales, not reach alone.</p>'

    '<h3>How to find local influencers</h3>'
    '<ol>'
    '<li><strong>Start with your city.</strong> Jem Social has a creator list for each of ' + str(N) + ' US cities (see the table below).</li>'
    '<li><strong>Narrow the list.</strong> Filter by niche, follower range and engagement rate.</li>'
    '<li><strong>Check the audience.</strong> Each profile in Jem Social shows the audience by city and age.</li>'
    '<li><strong>Read their recent posts.</strong> Look for local places, events and businesses they already feature.</li>'
    '<li><strong>Message them,</strong> or post a brief and let local creators apply to you.</li>'
    '</ol>'
    + cta_row(brief_url(SLUG), 'Post a free brief &rarr;', 'No card needed') +

    '<h3>Check that the audience is local</h3>'
    '<p>Where a creator lives and where their followers live are different things. A creator based in your city can have most of their followers somewhere else, and they won&#x27;t send many people to your shop. Look at the audience by city before you book, and ask the creator for a screenshot of their audience data if you want to double-check.</p>'

    '<h3>Creators by city on Jem Social</h3>'
    f'<p>These are the 20 cities with the most creators who have 5,000 or more followers, as listed on each city page on {TODAY}. Each city page shows the top 20 creators there by engagement.</p>'
    + table(['City', 'Creators with 5,000+ followers'], city_rows) +
    f'<p>Jem Social has lists for {N - 20} more cities:</p>'
    '<ul class="jl-linklist">' + rest_items + '</ul>'
    '<p>Don&#x27;t see your city? Search Jem Social by city, followers and engagement.</p>'

    '<h3>Local campaign ideas</h3>'
    '<ul>'
    '<li><strong>A visit.</strong> The creator visits your shop, restaurant or studio and posts about it.</li>'
    '<li><strong>An event.</strong> A creator covers an opening, a launch or a tasting.</li>'
    '<li><strong>A local offer.</strong> Give each creator their own code or link, so you can see which posts brought people in.</li>'
    '<li><strong>Gifting.</strong> You send product or offer a free service, and the creator decides whether to post.</li>'
    '<li><strong>A local series.</strong> One creator posts about your business regularly over a few weeks.</li>'
    '</ul>'
    '<p>A free meal, product or visit counts as a relationship the creator has to disclose, not only paid posts. The FTC says to disclose the relationship if you got anything of value to mention a product, and to place the disclosure with the post itself. (' + a(FTC, 'FTC: Disclosures 101 for Social Media Influencers', True) + ', checked November 17, 2026.)</p>'

    '<h3>What local influencers cost</h3>'
    '<p>Rates depend on followers, platform, deliverables and usage rights, so there&#x27;s no single price. The ' + a(JEM + '/influencer-rate-calculator', 'Influencer Rate Calculator') + ' gives a starting point, and ' + a(JEM + '/find-influencers/influencer-marketing-for-small-business', 'our small business guide') + ' lists typical rates by creator size. Put your budget in the brief and agree on deliverables and usage rights before any content is made.</p>'

    '<h3>More guides</h3>'
    '<ul>'
    '<li>' + a(JEM + '/find-influencers/influencer-marketing-for-small-business', 'Influencer marketing for small business: what it costs and how to start') + '</li>'
    '<li>' + a(JEM + '/find-influencers/influencer-marketing-campaign', 'Influencer marketing campaign: from brief to results') + '</li>'
    '<li>' + a(JEM + '/find-influencers/pay-influencers', 'How to pay influencers: fees, timing and what to agree first') + '</li>'
    '<li>' + a(JEM + '/local-influencers-near-me', 'Local influencers near me') + '</li>'
    '</ul>'
    + cta_row(signup_url(SLUG), 'Start free 7-day trial &rarr;', '$69/mo (reg. $99), billed monthly')
    + f'<p>Not ready to subscribe? <a href="{brief_url(SLUG)}">Post a free brief</a> instead. Creators apply to you, posting needs no card, and you only pay if you book creators through Jem.</p>'
)

hero_text = (
    f'<p>Local influencer marketing means working with creators whose followers live in the area you serve. Jem Social has creator lists for {N} US cities, and each profile shows the audience by city and age. '
    'Post a free brief and let local creators apply to you, or search by city for $69/month, billed monthly, after a 7-day free trial.</p>'
    + stats([(str(N), 'US city lists on Jem Social'), ('Free', 'To post a brief, no card'), ('$69/mo', 'To search, after a 7-day trial')])
)

faqs = [
    ('What is local influencer marketing?', 'Working with creators whose followers live in the area you serve, usually to bring people to a shop, restaurant, studio or event. It\'s judged on visits, bookings and local sales as well as reach.'),
    ('How do I find local influencers?', 'Start from a creator list for your city, then filter by niche, follower range and engagement rate. Check each creator\'s audience by city and read their recent posts. Or post a brief and let local creators apply to you.'),
    ('How do I know a creator\'s audience is local?', 'Check the audience by city. Where a creator lives and where their followers live can differ. Each profile in Jem Social shows the audience by city and age.'),
    ('How much do local influencers cost?', 'Rates depend on followers, platform, deliverables and usage rights, so there\'s no single price. Jem Social\'s Influencer Rate Calculator gives a starting point, and each creator\'s rate estimate is in Jem Social.'),
    ('Which cities does Jem Social cover?', f'Jem Social has creator lists for {N} US cities, from New York and Los Angeles to smaller cities. You can also search any other city by followers and engagement.'),
    ('Can I post a free brief for local creators?', 'Yes. Describe the job and your budget, and creators apply to you. Posting needs no card, and you only pay if you book creators through Jem.'),
    ('How much does Jem Social cost?', 'Jem Social costs $69 per month, billed monthly, after a 7-day free trial. That\'s about a third of the starting price of Modash or GRIN.'),
]

fd = {
    'meta-title': 'Local Influencer Marketing: Find Creators in Your City | Jem',
    'meta-description': 'How to find and hire local influencers: pick your city, check the audience is local and plan the campaign. Creator lists for dozens of US cities on Jem Social.',
    'hero-badge': 'LOCAL INFLUENCER MARKETING',
    'hero-title': 'Local influencer marketing: how to find and hire creators in your city',
    'hero-lead': 'Find creators by city.',
    'hero-description': css_embed() + hero_text,
    'hero-button-1-text': 'Jump to the guide',
    'editors-note-content': f'<p>Local influencer marketing means paying creators, or sending them product, to reach people in a particular area. This page covers how to find local creators, how to check their audience, and how to plan a campaign. City counts are from each city page on {TODAY}.</p>',
    'guide-section-badge': 'MARKETING GUIDE',
    'guide-section-heading': 'Local influencer marketing: a guide for brands',
    'cta-section-heading': 'Find creators in your city.',
    'cta-section-description': '<p>Post a free brief and let local creators apply to you, or start a 7-day free trial ($69/month, billed monthly) and search by city, niche, followers and engagement. Pay through Jem Social, with funds held until you approve the content.</p>',
}
finish('local', fd, faqs, guide)
