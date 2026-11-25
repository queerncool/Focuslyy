"""Upgrade the live creator post 'how-do-influencers-make-money' so it also answers 'how do influencers get paid'.
Reads the saved snapshot of the live post, applies exact text replacements, writes out/paid_patch.json (changed fields only)."""
import json, re, html, datetime, os
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'out') + '/'
BK = os.path.join(HERE, '..', 'page-backups') + '/'
post = json.load(open(BK + 'how-do-influencers-make-money.live-snapshot-nov25.json'))['fieldData']
creator_post = json.load(open(BK + 'creator-ugc-platforms-blog.live-snapshot-nov25.json'))['fieldData']['blog-summary']
body = post['blog-summary']
DATE = 'November 25, 2026'

def sub(old, new):
    global body
    assert body.count(old) == 1, (body.count(old), old[:70])
    body = body.replace(old, new)

def a(href, text): return f'<a href="{href}" rel="nofollow noopener" target="_blank">{text}</a>'
J = 'https://www.jem.social'

# 1. intro
sub('<p><em>Last updated: November 2026</em></p>', f'<p><strong>Last updated: {DATE}</strong></p>')
sub('Most creators combine several of these instead of relying on one.</p>',
    'Most creators combine several of these instead of relying on one. How you get paid depends on the stream: brands pay a fee, send product or pay a commission, platforms pay once you pass their thresholds, and your audience pays you directly.</p>')
sub('It does not quote earnings figures, because rates vary too much by niche, platform and audience to give honest averages.',
    'It does not quote average earnings, because rates vary too much by niche, platform and audience to give honest averages. Where it quotes a rate or a platform rule, it names the source and the date it was checked.')

# 2. new section: how and when you get paid (before stream 1)
sub('<h2>1. Sponsored posts and brand deals</h2>',
    '<h2>How and when influencers get paid</h2>'
    '<p>How you get paid depends on who is paying you.</p>'
    '<ul>'
    '<li><strong>Brands</strong> pay a fee, send product or pay a commission on sales. Agree the amount, the date and the method before you start, and put it in writing. On Jem Social, the brand pays through the platform, the funds are held until the brand approves your content, and then they are released to you.</li>'
    '<li><strong>Platforms</strong> pay from ad revenue or rewards programs, but only once you pass their thresholds. The rules are under &ldquo;5. Platform payouts and creator programs&rdquo; below.</li>'
    '<li><strong>Your audience</strong> pays through subscriptions, tips and the products you sell.</li>'
    '</ul>'
    '<p>Whoever is paying, settle three things before you start: how much, by when and by what method. Then you can check each payment against what you agreed.</p>'
    '<h2>1. Sponsored posts and brand deals</h2>')

# 3. rates in section 1
sub('To price a deal, start with the <a href="https://www.jem.social/influencer-rate-calculator">influencer rate calculator</a>, then adjust for usage rights and rush timelines.',
    'To price a deal, start with the <a href="https://www.jem.social/influencer-rate-calculator">influencer rate calculator</a>, then adjust for usage rights and rush timelines. The FAQ on that page lists typical rates per Instagram post: $100 to $500 for nano creators (1,000 to 10,000 followers), $500 to $3,000 for micro creators (10,000 to 100,000) and $3,000 to $15,000 for macro creators (100,000 to 1 million). It puts organic reuse of your content at 10% to 20% more, paid ads at 40% to 60% more and a full buyout at 150% or more. These are estimates, not quotes, and every brand sets its own budget.')

# 4. UGC rates in section 3
sub('Brands care about whether your content looks natural and answers a buyer\'s question.</p>',
    'Brands care about whether your content looks natural and answers a buyer\'s question. The FAQ on the rate calculator page puts UGC creators at typically $150 to $400 per short video and $100 to $250 per static post, before usage rights.</p>')

# 5. platform payouts with verified rules
YT = 'https://support.google.com/youtube/answer/72851'
YT2 = 'https://www.youtube.com/creators/earn/youtube-partner-program/'
TT = 'https://support.tiktok.com/en/business-and-creator/creator-rewards-program'
IG = 'https://help.instagram.com/493264770320965'
IG2 = 'https://help.instagram.com/478012211024479'
sub('<p>Some platforms share revenue with creators who meet their eligibility rules. Those rules, payout structures and available programs differ by platform and change often. Check the official creator pages for YouTube, TikTok and Instagram for current requirements before you plan around any of them.</p>',
    f'<p>Some platforms share revenue with creators who meet their eligibility rules. These are the rules each platform publishes, checked on {DATE}. They change often, so read the source before you plan around any of them.</p>'
    '<ul>'
    '<li><strong>YouTube.</strong> The YouTube Partner Program allows revenue sharing from ads served on your content. A channel becomes eligible with 1,000 subscribers and either 4,000 qualified public watch hours in the past 12 months or 10 million qualified Shorts views in the past 90 days. YouTube also lists an earlier tier at 500 subscribers, 3 qualified uploads in 90 days and either 3,000 watch hours or 3 million Shorts views, which opens channel memberships. Meeting a threshold does not guarantee entry, because YouTube reviews each channel against its monetization policies. YouTube says it is updating Partner Program terms from February 1, 2027. (' + a(YT, 'YouTube Help') + ', ' + a(YT2, 'YouTube for Creators') + ')</li>'
    '<li><strong>TikTok.</strong> The Creator Rewards Program needs a personal account in an eligible country, an age of 18 or older, at least 10,000 followers and at least 100,000 video views in the last 30 days. Videos must be at least one minute long, and each one needs 1,000 qualified For You feed views to collect rewards. (' + a(TT, 'TikTok Support') + ')</li>'
    '<li><strong>Instagram.</strong> Instagram lists Badges, Bonuses, Creator Marketplace, Gifts and Subscriptions as monetization tools, each with its own eligibility rules. Subscriptions need a professional account with at least 10,000 followers, and you must be 18 or older. (' + a(IG, 'Instagram Help Center') + ', ' + a(IG2, 'Subscriptions eligibility') + ')</li>'
    '</ul>'
    '<p>Most of these programs also depend on your country. If you do not meet the thresholds yet, brand deals and UGC work do not wait on them.</p>')

# 6. taxes after disclosure
IRS1 = 'https://www.irs.gov/businesses/small-businesses-self-employed/self-employed-individuals-tax-center'
IRS2 = 'https://www.irs.gov/businesses/small-businesses-self-employed/self-employment-tax-social-security-and-medicare-taxes'
IRS3 = 'https://www.irs.gov/businesses/understanding-your-form-1099-k'
IRS4 = 'https://www.irs.gov/faqs/small-business-self-employed-other-business/form-1099-nec-independent-contractors/form-1099-nec-independent-contractors'
sub('<h2>Common mistakes that keep creators unpaid</h2>',
    '<h2>Taxes on creator income (US)</h2>'
    '<p>If a brand pays you as an independent contractor, the money is usually self-employment income. The IRS says you have to file an income tax return if your net earnings from self-employment were $400 or more, and that those earnings are generally subject to self-employment tax, which covers Social Security and Medicare. A brand that pays you $600 or more in a year may send you a Form 1099-NEC, and for payments made after December 31, 2025 the reporting threshold is $2,000. Whether or not you receive a form such as a Form 1099-K, the IRS says you must still report any income on your tax return. (' + a(IRS1, 'IRS: self-employed individuals tax center') + ', ' + a(IRS2, 'self-employment tax') + ', ' + a(IRS4, 'Form 1099-NEC FAQ') + ', ' + a(IRS3, 'Form 1099-K') + f'; checked {DATE}.) Ask an accountant what applies to you. This is general information, not tax advice.</p>'
    '<h2>Common mistakes that keep creators unpaid</h2>')

# 7. open campaigns cards before the closing CTA
style = creator_post[creator_post.find('<style>'):creator_post.find('</style>') + 8]
assert '.cpx-opps' in style
def card(brand, title, pay, meta, slug):
    return (f'<div class="cpx-opp"><div class="cpx-brand">{brand}</div><div class="cpx-title">{title}</div><div class="cpx-pay">{pay}</div>'
            f'<div class="cpx-meta">{meta}</div><a href="{J}/opportunities/{slug}?source=blog">View the listing &rarr;</a></div>')
cards = (
    card('Filterbuy', 'UGC Hosts for Home Air Filters', '$600 USD per month for 25 accepted videos, plus performance pay once a video reaches 10,000 views.', 'Remote. US and Canada only.<br>Open until Dec 11, 2026', 'ugc-hosts-for-home-air-filters')
    + card('DealSeek Canada', 'Canadian Creators for a Deals Platform', 'A guaranteed monthly base of $400&ndash;$600 USD, plus $1 per 1,000 views and milestone bonuses.', 'Remote. Canada only.<br>Open until Dec 11, 2026', 'canadian-creators-for-a-deals-platform')
    + card('Danzify', 'Danzify Pet Creator Program', '$400 a month guaranteed, plus view-based milestone bonuses of up to $250 per video.', 'Needs a pet you can film with. The listing says no UGC experience or large following is required.<br>Open until Dec 31, 2026', 'danzify-pet-creator-program-400-month-up-to-250-video')
    + card('Zoo Atlanta', 'Zoo Atlanta Content Creator Collaboration', 'Gifted. One Instagram Reel, reviewed by the zoo before you post.', 'The listing asks for 10&ndash;50k followers.<br>Open until Dec 17, 2026', 'zoo-atlanta-content-creator-collaboration')
)
sub('<h2>Send your first three pitches this week</h2>',
    '<h2>Open campaigns you can apply to now</h2>'
    f'<p>These listings were open on the Jem Social Opportunity Board on {DATE}. Three pay a monthly base plus bonuses and one is gifted, so you can see how the pay differs. Listings close and change, so check the board for what is live today.</p>'
    f'<div data-rt-embed-type="true">{style}<div class="cpx-opps">{cards}</div></div>'
    f'<p><a href="{J}/opportunities?source=blog">See every open campaign on the Jem Social Opportunity Board</a>. Applying is free.</p>'
    '<h2>Send your first three pitches this week</h2>')

fd = {
    'name': 'How Do Influencers Make Money and Get Paid? 8 Income Streams',
    'meta-title': 'How Influencers Make Money and Get Paid (2026) | Jem Social',
    'meta-description': 'How influencers make money and get paid: brand deals, UGC, affiliate and platform payouts, with YouTube and TikTok thresholds, typical rates and US tax basics.',
    'blog-post-content': 'How influencers make money and get paid: eight income streams, the YouTube, TikTok and Instagram payout rules, typical rates and US tax basics.',
    'blog-summary': body,
    'key-takeaways': '<ul><li>Influencers get paid by brands (a fee, product or a commission), by platforms once they pass thresholds, and by their audience.</li><li>In November 2026, YouTube ad revenue sharing needs 1,000 subscribers plus 4,000 watch hours or 10 million Shorts views, and TikTok Creator Rewards needs 10,000 followers and 100,000 views in 30 days.</li><li>Jem Social&#39;s rate calculator page lists typical Instagram post rates from $100 to $500 for nano creators to $3,000 to $15,000 for macro creators. They are estimates, not quotes.</li><li>In the US, report the income whether or not you get a form. The Form 1099-NEC threshold is $2,000 for payments made after December 31, 2025.</li><li>On Jem Social the brand&#39;s payment is held until it approves your content, and applying to campaigns is free.</li></ul>',
    'faq-5-question': 'How and when do influencers get paid?',
    'faq-5-answer': 'It depends on the deal. Brands pay a fee, product or a commission, and you should agree the amount, the date and the method before you start. Platforms pay once you pass their thresholds. On Jem Social, the brand pays through the platform, the funds are held until the brand approves your content, and then they are released to you.',
    'faq-1-answer': 'Influencers earn from brand sponsorships, UGC deals, affiliate commissions, platform payouts, their own products, memberships and events. Most combine two or more streams. Brand-paid work is usually the first to start, and brands pay a fee, send product or pay a commission on sales.',
    'updated-date': datetime.datetime(2026, 11, 25, 13, 0).strftime('%Y-%m-%dT%H:%M:%S.000Z'),
    'related-posts': list(post['related-posts']) + ['6adcff4c71fcc71a877db103'],
}
assert len(fd['meta-title']) <= 60, len(fd['meta-title'])
assert len(fd['meta-description']) <= 160, len(fd['meta-description'])
os.makedirs(OUT, exist_ok=True)
json.dump({'fieldData': fd}, open(OUT + 'paid_patch.json', 'w'), indent=1)
words = len(re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', re.sub(r'<style>[\s\S]*?</style>', '', body)))).split())
print('meta-title', len(fd['meta-title']), '| meta-desc', len(fd['meta-description']), '| body words ~', words, '| body chars', len(body), '(was', len(post['blog-summary']), ')')
