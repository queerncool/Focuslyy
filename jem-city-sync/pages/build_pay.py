from pagelib import *
SLUG = 'pay-influencers'
FTC = 'https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers'
IRS = 'https://www.irs.gov/faqs/small-business-self-employed-other-business/form-1099-nec-independent-contractors/form-1099-nec-independent-contractors'

guide = (
    '<div data-rt-embed-type="true"><div id="Creators"></div></div>'
    '<h3>Ways to pay an influencer</h3>'
    '<p>There are four common models, and you can combine them.</p>'
    + table(['Model', 'How it works', 'Watch out for'], [
        ['Flat fee', 'You pay a set amount for a post or video.', 'Agree the deliverables, the deadline and the number of revisions first.'],
        ['Commission', 'The creator gets a code or link and earns a share of the sales it brings in.', 'You need a way to track sales, and some creators will want a fee as well.'],
        ['Product gifting', 'You send the product and the creator decides whether to post.', 'A free product still counts as a relationship the creator has to disclose.'],
        ['Fee plus commission', 'A set fee, plus a share of sales or a bonus.', 'Write down how the bonus is worked out.'],
    ]) +
    '<p>Rates depend on followers, platform, deliverables and usage rights, so there&#x27;s no single price. The ' + a(JEM + '/influencer-rate-calculator', 'Influencer Rate Calculator') + ' gives a starting point.</p>'

    '<h3>When to pay</h3>'
    '<p>You can pay before the content, after it, or in parts. Paying everything up front means you&#x27;ve paid before you&#x27;ve seen the work. Paying only after the post goes live leaves the creator carrying the risk. Holding the payment until you approve the content covers both sides: the money is committed, and it moves when you&#x27;re happy with the work.</p>'

    '<h3>How paying works on Jem Social</h3>'
    '<ol>'
    '<li>Agree the rate, deliverables and usage rights with the creator.</li>'
    '<li>Pay through Jem Social. The funds are held until you approve the content.</li>'
    '<li>The creator makes the content and delivers it.</li>'
    '<li>Review it in Jem Social and ask for edits if you need them.</li>'
    '<li>Approve it, and the payment is released to the creator.</li>'
    '</ol>'
    '<p>Don&#x27;t have creators in mind yet? ' + a(brief_url(SLUG), 'Post a free brief') + ' and let creators apply to you. Posting needs no card, and you only pay if you book creators through Jem.</p>'
    + cta_row(brief_url(SLUG), 'Post a free brief &rarr;', 'No card needed') +

    '<h3>What to agree before you pay</h3>'
    '<ul>'
    '<li><strong>Deliverables.</strong> What the creator will make, how many, on which platform, and how long each one is.</li>'
    '<li><strong>Deadline.</strong> When you need the draft and when it should go live.</li>'
    '<li><strong>Revisions.</strong> How many rounds of edits are included.</li>'
    '<li><strong>Usage rights.</strong> Whether you can reuse the content, and whether you can run it as an ad.</li>'
    '<li><strong>Disclosure.</strong> How the creator will say the post is paid or gifted.</li>'
    '</ul>'
    '<p>The ' + a(JEM + '/campaign-brief-generator', 'Campaign Brief Generator') + ' gives you a template for writing these down.</p>'

    '<h3>Disclosure</h3>'
    '<p>The FTC says an endorsement should make it obvious when the creator has a relationship with the brand, and that relationship includes free products. The disclosure should sit with the endorsement itself, not only on a profile page or behind a &quot;more&quot; link. (' + a(FTC, 'FTC: Disclosures 101 for Social Media Influencers', True) + ', checked November 17, 2026.)</p>'

    '<h3>Taxes in the US</h3>'
    '<p>The IRS says to report payments totaling $600 or more during the year to people who aren&#x27;t employees, such as independent contractors, for services performed for your business, using Form 1099-NEC. For payments made after December 31, 2025, the threshold is $2,000. (' + a(IRS, 'IRS: Form 1099-NEC FAQ', True) + ', checked November 24, 2026.) Many businesses collect a Form W-9 from the creator before paying. Ask an accountant what applies to you. This is general information, not tax or legal advice.</p>'

    '<h3>More guides</h3>'
    '<ul>'
    '<li>' + a(JEM + '/find-influencers/instagram-influencer-marketing', 'Instagram influencer marketing: find, hire and pay creators yourself') + '</li>'
    '<li>' + a(JEM + '/find-influencers/tiktok-influencer-marketing', 'TikTok influencer marketing: find, hire and pay creators yourself') + '</li>'
    '<li>' + a(JEM + '/find-influencers/influencer-marketing-for-small-business', 'Influencer marketing for small business: what it costs and how to start') + '</li>'
    '<li>' + a(JEM + '/find-influencers/top-influencer-marketing-platforms', 'Influencer marketing platforms compared: pricing and fees') + '</li>'
    '</ul>'
    + cta_row(signup_url(SLUG), 'Start free 7-day trial &rarr;', '$69/mo (reg. $99), billed monthly')
)

hero_text = (
    '<p>Paying an influencer means agreeing a fee, a way to pay and a point at which the money moves. On Jem Social you pay through Jem, and the funds are held until you approve the content. Then they&#x27;re released to the creator. '
    'Post a free brief to get started, or search creators for $69/month, billed monthly, after a 7-day free trial.</p>'
    + stats([('Held', 'Until you approve the content'), ('Free', 'To post a brief, no card'), ('$69/mo', 'To search, after a 7-day trial')])
)

faqs = [
    ('How do I pay an influencer?', 'Agree a fee, a way to pay and when the money moves. You can pay a flat fee, a commission, product or a mix. On Jem Social you pay through the platform, and the funds are held until you approve the content.'),
    ('Should I pay influencers up front?', 'Paying in full before you&#x27;ve seen the content means you carry the risk. Holding payment until you approve the content protects both sides. On Jem Social, funds are held until you approve it, then released to the creator.'.replace('&#x27;', "'")),
    ('How does payment work on Jem Social?', 'You agree the rate and deliverables with the creator and pay through Jem Social. The funds are held while the creator makes the content. You review it, ask for edits if you need them, and approve it. The payment is then released to the creator.'),
    ('Can I pay influencers with free products?', 'Some creators will post in exchange for a free product, but many will also ask for a fee. The FTC says a free product is a relationship the creator should disclose.'),
    ('Do I need to send influencers a 1099?', 'In the US, the IRS says to report payments to independent contractors on Form 1099-NEC when they total $600 or more in a year, or $2,000 or more for payments made after December 31, 2025. Ask an accountant what applies to you.'),
    ('How much should I pay an influencer?', 'Rates depend on followers, platform, deliverables and usage rights, so there\'s no single price. Jem Social\'s Influencer Rate Calculator gives a starting point, and each creator\'s rate estimate is in Jem Social.'),
    ('How much does Jem Social cost?', 'Jem Social costs $69 per month, billed monthly, after a 7-day free trial. Posting a brief is free and needs no card. That\'s about a third of the starting price of Modash or GRIN.'),
]

fd = {
    'meta-title': 'How to Pay Influencers: Fees, Timing, Taxes | Jem Social',
    'meta-description': 'How to pay influencers: flat fee, commission or product, when to pay, what to agree first and 1099 basics. On Jem Social, funds are held until you approve.',
    'hero-badge': 'PAY INFLUENCERS',
    'hero-title': 'How to pay influencers: fees, timing and what to agree first',
    'hero-lead': 'Payment held until you approve.',
    'hero-description': css_embed() + hero_text,
    'hero-button-1-text': 'Jump to the guide',
    'editors-note-content': '<p>Paying an influencer means giving a creator money, product or a share of sales in return for content. This page covers the main ways to pay, when to release payment, and what to agree first. It isn&#x27;t legal or tax advice.</p>',
    'guide-section-badge': 'MARKETING GUIDE',
    'guide-section-heading': 'How to pay influencers: a guide for brands',
    'cta-section-heading': 'Pay creators for content you approve.',
    'cta-section-description': '<p>Post a free brief, or start a 7-day free trial ($69/month, billed monthly) and search creators by niche, city, followers and engagement. Pay through Jem Social, with funds held until you approve the content.</p>',
}
finish('pay', fd, faqs, guide)
