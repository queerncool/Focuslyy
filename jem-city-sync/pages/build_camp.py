from pagelib import *
SLUG = 'influencer-marketing-campaign'

guide = (
    '<div data-rt-embed-type="true"><div id="Creators"></div></div>'
    '<h3>What an influencer marketing campaign involves</h3>'
    '<p>An influencer marketing campaign is a planned set of creator posts with a goal, a budget and a deadline. You choose the creators, agree what they&#x27;ll make, review the content, then pay. There are several kinds:</p>'
    + table(['Type', 'What it is'], [
        ['Product seeding', 'You send product to a number of creators, and they post if they like it.'],
        ['Sponsored posts', 'You pay creators an agreed fee for posts or videos with set deliverables.'],
        ['Ambassador partnership', 'One creator works with you over weeks or months, not once.'],
        ['Commission or affiliate', 'The creator gets a code or link and earns a share of the sales it brings in.'],
        ['UGC for your own channels', 'The creator makes content for you to use in your own posts and ads, and may not post it themselves.'],
    ]) +

    '<h3>How to plan a campaign</h3>'
    '<ol>'
    '<li><strong>Set one goal.</strong> Awareness, website visits, sales or content for your own channels. Pick the one thing you&#x27;ll judge the campaign on.</li>'
    '<li><strong>Set a budget.</strong> Add up creator fees, product and any usage rights you want. The ' + a(JEM + '/influencer-rate-calculator', 'Influencer Rate Calculator') + ' gives a starting point for fees.</li>'
    '<li><strong>Choose the platform.</strong> See our ' + a(JEM + '/find-influencers/instagram-influencer-marketing', 'Instagram guide') + ' and ' + a(JEM + '/find-influencers/tiktok-influencer-marketing', 'TikTok guide') + '.</li>'
    '<li><strong>Find the creators.</strong> Search Jem Social by niche, city, followers and engagement, or post a brief and let creators apply to you.</li>'
    '<li><strong>Write the brief.</strong> The ' + a(JEM + '/campaign-brief-generator', 'Campaign Brief Generator') + ' gives you a template.</li>'
    '<li><strong>Agree terms and pay.</strong> Rate, deliverables, deadline, usage rights. On Jem Social you pay through the platform and the funds are held until you approve the content.</li>'
    '<li><strong>Review and approve.</strong> Ask for edits if you need them. Approving releases the payment.</li>'
    '<li><strong>Measure the results.</strong> Give each creator a code or link, then compare results against your goal.</li>'
    '</ol>'
    + cta_row(brief_url(SLUG), 'Post a free brief &rarr;', 'No card needed') +

    '<h3>What to put in the brief</h3>'
    '<ul>'
    '<li>The product and the one goal of the campaign.</li>'
    '<li>The deliverables: how many posts or videos, on which platform, and how long.</li>'
    '<li>Talking points, and anything the creator should not say or show.</li>'
    '<li>The deadline for the draft and the date it should go live.</li>'
    '<li>Your budget and how you&#x27;ll pay.</li>'
    '<li>Usage rights: whether you can reuse the content, and whether you can run it as an ad.</li>'
    '<li>How the creator will disclose the partnership.</li>'
    '</ul>'

    '<h3>How to measure a campaign</h3>'
    + table(['Measure', 'How it&#x27;s worked out', 'Tool'], [
        ['Engagement rate', 'Likes, comments, shares and saves compared with followers or views. Tools calculate it differently.', a(JEM + '/engagement-rate-calculator', 'Engagement Rate Calculator')],
        ['CPM', 'Cost divided by impressions, times 1,000.', a(JEM + '/cpm-calculator', 'CPM Calculator')],
        ['Cost per sale', 'Cost divided by the number of sales from the creator&#x27;s code or link.', 'Codes and tracking links'],
        ['Return on investment', 'Revenue minus cost, divided by cost.', a(JEM + '/influencer-marketing-roi-calculator', 'Influencer Marketing ROI Calculator')],
    ]) +
    '<p>Pick the measure that matches your goal. A campaign for awareness is judged on reach and engagement, and a campaign for sales on sales.</p>'

    '<h3>Run your campaign on Jem Social</h3>'
    '<p>You can ' + a(brief_url(SLUG), 'post a free brief') + ' and let creators apply to you. Posting needs no card, and you only pay if you book creators through Jem. Or search creators yourself for $69/month, billed monthly, after a 7-day free trial.</p>'
    + cta_row(signup_url(SLUG), 'Start free 7-day trial &rarr;', '$69/mo (reg. $99), billed monthly') +

    '<h3>More guides</h3>'
    '<ul>'
    '<li>' + a(JEM + '/find-influencers/influencer-marketing-for-small-business', 'Influencer marketing for small business: what it costs and how to start') + '</li>'
    '<li>' + a(JEM + '/find-influencers/pay-influencers', 'How to pay influencers: fees, timing and what to agree first') + '</li>'
    '<li>' + a(JEM + '/find-influencers/micro-influencer-platform', 'Micro influencer platform: hire creators without an agency') + '</li>'
    '</ul>'
)

hero_text = (
    '<p>An influencer marketing campaign is a planned set of creator posts with a goal, a budget and a deadline. This page walks through the steps, from the brief to the results. On Jem Social you can post a free brief and let creators apply to you, or search creators by niche, city, followers and engagement for $69/month, billed monthly, after a 7-day free trial.</p>'
    + stats([('Free', 'To post a brief, no card'), ('$69/mo', 'To search, after a 7-day trial'), ('Held', 'Payment until you approve')])
)

faqs = [
    ('What is an influencer marketing campaign?', 'A planned set of creator posts with a goal, a budget and a deadline. You choose the creators, agree the deliverables and the fee, review the content, then pay.'),
    ('How do I start an influencer marketing campaign?', 'Set one goal and a budget, choose a platform, find creators, then write a brief. On Jem Social you can post a free brief and let creators apply to you, or search creators yourself.'),
    ('How many influencers should I use?', 'There\'s no fixed number. Many brands start with a few creators so they can compare results before they spend more.'),
    ('What goes in an influencer campaign brief?', 'The product and goal, the deliverables, talking points, the deadline, your budget, usage rights and how the creator will disclose the partnership. Jem Social\'s Campaign Brief Generator gives you a template.'),
    ('How do I measure an influencer marketing campaign?', 'Give each creator a code or link, then compare results against your goal. Engagement rate, CPM, cost per sale and return on investment each answer a different question. Jem Social has a free calculator for each.'),
    ('How do I pay creators in a campaign?', 'You pay through Jem Social. Funds are held until you approve the content, then released to the creator.'),
    ('How much does Jem Social cost?', 'Jem Social costs $69 per month, billed monthly, after a 7-day free trial. Posting a brief is free and needs no card. That\'s about a third of the starting price of Modash or GRIN.'),
]

fd = {
    'meta-title': 'Influencer Marketing Campaign: Steps, Brief, Budget | Jem',
    'meta-description': 'How to plan an influencer marketing campaign: goal, budget, creators, brief, approval and results. Start with a free brief on Jem Social.',
    'hero-badge': 'INFLUENCER MARKETING CAMPAIGN',
    'hero-title': 'Influencer marketing campaign: from brief to results',
    'hero-lead': 'Start with a free brief.',
    'hero-description': css_embed() + hero_text,
    'hero-button-1-text': 'Jump to the guide',
    'editors-note-content': '<p>An influencer marketing campaign is a planned set of creator posts with a goal, a budget and a deadline. This page covers the steps to plan one, what goes in the brief, and how to measure the results.</p>',
    'guide-section-badge': 'MARKETING GUIDE',
    'guide-section-heading': 'How to run an influencer marketing campaign',
    'cta-section-heading': 'Start your campaign with a free brief.',
    'cta-section-description': '<p>Post a free brief and let creators apply to you, or start a 7-day free trial ($69/month, billed monthly) and search creators by niche, city, followers and engagement. Pay through Jem Social, with funds held until you approve the content.</p>',
}
finish('camp', fd, faqs, guide)
