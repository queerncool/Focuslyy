import json, os, re, sys, glob, html, hashlib, statistics, subprocess, datetime, io, time, math, urllib.request, urllib.error, unicodedata, base64
W = os.path.expanduser('~/jem-sync'); os.makedirs(W, exist_ok=True)
SITE_ID, COLL, OLD_COLL = '67b0d09acc5bda1c5c04566f', '6adc28d2f2806b611dd3a207', '69dae1304d0242f517edcc12'
SITE, CDN, API = 'https://www.jem.social', 'https://cdn.prod.website-files.com/', 'https://api.webflow.com/v2'
SIGNUP = 'https://app.jem.social/signup'
MAX_NEW, MAX_REFRESH = int(os.environ.get('MAX_NEW', 10)), int(os.environ.get('MAX_REFRESH', 4))
REFRESH_DAYS, SKIP_DAYS = int(os.environ.get('REFRESH_DAYS', 27)), 60
SHOW, MIN_BUILD, MIN_INDEX = 20, 5, 10
TIERS = [(5000, 9999, '5K–10K'), (10000, 99999, '10K–100K'), (100000, 999999, '100K–1M'), (1000000, None, '1M or more')]
MAX_ER = 20.0
FPV = 'v3:'
PLAT = {'instagram': ('Instagram', 'https://www.instagram.com/{}/'), 'tiktok': ('TikTok', 'https://www.tiktok.com/@{}'),
        'youtube': ('YouTube', 'https://www.youtube.com/@{}')}
PRIORITY = [
 ('New York', 'NY', 40.71, -74.01), ('New Orleans', 'LA', 29.95, -90.07), ('Chicago', 'IL', 41.88, -87.63),
 ('Nashville', 'TN', 36.16, -86.78), ('Charlotte', 'NC', 35.23, -80.84), ('Seattle', 'WA', 47.61, -122.33),
 ('Albuquerque', 'NM', 35.08, -106.65), ('Miami', 'FL', 25.76, -80.19), ('Atlanta', 'GA', 33.75, -84.39),
 ('San Francisco', 'CA', 37.77, -122.42), ('Pittsburgh', 'PA', 40.44, -79.99), ('St. Louis', 'MO', 38.63, -90.20),
 ('Los Angeles', 'CA', 34.05, -118.24), ('Fort Worth', 'TX', 32.76, -97.33), ('Asheville', 'NC', 35.60, -82.55),
 ('Boston', 'MA', 42.36, -71.06), ('Austin', 'TX', 30.27, -97.74), ('Denver', 'CO', 39.74, -104.99),
 ('Portland', 'OR', 45.52, -122.68), ('Memphis', 'TN', 35.15, -90.05), ('Sacramento', 'CA', 38.58, -121.49),
 ('Dallas', 'TX', 32.78, -96.80), ('Tucson', 'AZ', 32.22, -110.97), ('San Diego', 'CA', 32.72, -117.16),
 ('Tampa', 'FL', 27.95, -82.46), ('Savannah', 'GA', 32.08, -81.09), ('San Antonio', 'TX', 29.42, -98.49),
 ('Kansas City', 'MO', 39.10, -94.58), ('Minneapolis', 'MN', 44.98, -93.27), ('Indianapolis', 'IN', 39.77, -86.16),
 ('Cleveland', 'OH', 41.50, -81.69), ('San Jose', 'CA', 37.34, -121.89), ('Houston', 'TX', 29.76, -95.37),
 ('Charleston', 'SC', 32.78, -79.93), ('Las Vegas', 'NV', 36.17, -115.14), ('Philadelphia', 'PA', 39.95, -75.17),
 ('Orlando', 'FL', 28.54, -81.38), ('Scottsdale', 'AZ', 33.49, -111.93), ('Cincinnati', 'OH', 39.10, -84.51),
 ('Baltimore', 'MD', 39.29, -76.61), ('Louisville', 'KY', 38.25, -85.76), ('Virginia Beach', 'VA', 36.85, -75.98),
 ('Reno', 'NV', 39.53, -119.81), ('Durham', 'NC', 35.99, -78.90), ('Phoenix', 'AZ', 33.45, -112.07),
 ('Fort Lauderdale', 'FL', 26.12, -80.14), ('Richmond', 'VA', 37.54, -77.44), ('Madison', 'WI', 43.07, -89.40),
 ('Salt Lake City', 'UT', 40.76, -111.89), ('Detroit', 'MI', 42.33, -83.05), ('Santa Barbara', 'CA', 34.42, -119.70),
 ('Honolulu', 'HI', 21.31, -157.86), ('Birmingham', 'AL', 33.52, -86.80),
 ('Washington', 'DC', 38.91, -77.04), ('Columbus', 'OH', 39.96, -83.00), ('Myrtle Beach', 'SC', 33.69, -78.89),
 ('Milwaukee', 'WI', 43.04, -87.91), ('Jacksonville', 'FL', 30.33, -81.66), ('Palm Springs', 'CA', 33.83, -116.55),
 ('Oakland', 'CA', 37.80, -122.27), ('Boulder', 'CO', 40.01, -105.27), ('Ann Arbor', 'MI', 42.28, -83.74),
 ('Sarasota', 'FL', 27.34, -82.53), ('Raleigh', 'NC', 35.78, -78.64), ('Bakersfield', 'CA', 35.37, -119.02)]
LOCATION = {('Washington', 'DC'): 'District of Columbia, United States'}
COORD = {(c, s): (la, lo) for c, s, la, lo in PRIORITY}
PASSES = [(None,), ('food',), ('fitness', 'beauty', 'fashion')]
NICHES = ['food', 'fitness', 'beauty', 'fashion']
NICHE_WORDS = {
 'food': r'food|eat|chef|kitchen|cook|bak|recipe|dining|dine|drink|dessert|bbq|restaurant|tast|bite|brunch|coffee|cocktail|wine|sweet|snack|menu|dietitian|nutrition|grill',
 'fitness': r'fit|gym|coach|trainer|workout|yoga|pilates|weight ?loss|athlet|run|lift|muscle',
 'beauty': r'beauty|makeup|mua|skin|nail|hair|lash|brow|esthetic|cosmetic|glam',
 'fashion': r'fashion|style|stylist|outfit|ootd|wear|wardrobe|boutique|lifestyle',
 'tech': r'tech|gadget|apps?\b|software|ai\b|gam(?:ing|er)|setup|desk|cod(?:e|ing)|develop|iphone|android|pc\b|computer|electronic',
 'other': r'money|financ|realtor|real estate|mortgage|insurance|attorney|lawyer'}
TOPICS = {
 'ugc-creators': {
  'search': {'niche': 'ugc', 'location': 'United States'}, 'niche': 'ugc', 'Label': 'UGC Creators', 'crumb': 'UGC creators',
  'noun': 'UGC creators', 'who': 'US UGC creators', 'scope': 'tagged UGC and based in the US',
  'h1': 'Top {N} UGC Creators to Hire ({M})', 'title': 'Top {N} UGC Creators to Hire ({Mon}) | Jem Social',
  'desc': "Browse {N} of Jem Social's {total} US UGC creators with follower counts and engagement rates.",
  'intro': 'Jem Social has {total} UGC creators in the US with at least 5,000 followers. Here are {N} of them, sorted by engagement rate.',
  'micro': '7-day free trial, then $69/month. Search UGC creators by niche, city, followers and engagement.',
  'list': '{N} UGC creators', 'band': 'Hire UGC creators for your brand', 'steps': 'How to hire UGC creators',
  'faqs': [
   ('What is a UGC creator?', "A UGC (user-generated content) creator makes photos and videos that brands use in their own marketing and ads, such as reviews, "
    "unboxings and tutorials. The brand gets the content to post itself, so the creator's own audience size matters less than for an influencer post.", None),
   ('How many UGC creators are on Jem Social?', 'Jem Social lists {total} US creators tagged UGC with at least 5,000 followers as of {M}. This page shows {N} of them, sorted by engagement rate.', None),
   ('How much do UGC creators charge?', "Rates depend on the deliverables, usage rights and the creator's experience. The UGC Rate Card Generator gives a starting point, and each creator's rate estimate is in Jem Social.",
    "Rates depend on the deliverables, usage rights and the creator's experience. The <a href=\"/ugc-rate-card-generator\" class=\"jp-inline-link\">UGC Rate Card Generator</a> gives a starting point, and each creator's rate estimate is in Jem Social."),
   ('How do I hire UGC creators?', "Start a 7-day free trial to see each creator's email and audience data. Then message them and pay through Jem Social, with funds held until you approve the content.", None),
   ('How do I become a UGC creator?', "Make a free Jem Social creator profile to pitch brands and track every application in one place. Brands post open UGC roles on Jem Social's opportunities page.",
    "Make a free Jem Social creator profile to pitch brands and track every application in one place. Brands post open UGC roles on the <a href=\"/opportunities\" class=\"jp-inline-link\">opportunities page</a>."),
   ('How much does Jem Social cost?', 'For brands, Jem Social costs $69 per month after a 7-day free trial. For creators, pitching brands is free, or $20 per month for Premium.', None)],
  'links': [('UGC resources', [('/ugc-rate-card-generator', 'UGC rate card generator'), ('/free-ugc-contract-template', 'Free UGC contract template'),
                               ('/blog/what-is-ugc', 'What is UGC?'), ('/hire-tech-ugc-creators', 'Hire tech UGC creators')]),
            ('UGC by niche', [('/influencers/tech-ugc-creators', 'Tech UGC creators')]),
            ('For UGC creators', [('/blog/how-to-become-a-ugc-creator', 'How to become a UGC creator'), ('/opportunities', 'Open brand opportunities'),
                                  ('/blog/ugc-jobs', 'UGC jobs'), ('/earn-money-as-a-ugc-creator', 'Earn money as a UGC creator')])],
  'old': ['find-ugc-creators', 'ugc-creator', 'ugc-content-creator'], 'show': 50, 'pages': 2, 'tiers': True},
 'fitness': {
  'search': {'niche': 'fitness', 'location': 'United States'}, 'niche': 'fitness', 'Label': 'Fitness Influencers', 'crumb': 'Fitness influencers',
  'noun': 'fitness creators', 'who': 'US fitness creators', 'scope': 'tagged fitness and based in the US', 'city_niche': 'fitness',
  'city_label': 'Fitness influencers by city',
  'h1': 'Top {N} Fitness Influencers for Brands ({M})', 'title': 'Top {N} Fitness Influencers for Brands ({Mon}) | Jem Social',
  'desc': "Browse {N} of Jem Social's {total} US fitness influencers with follower counts and engagement rates.",
  'intro': 'Jem Social has {total} fitness creators in the US with at least 5,000 followers. Here are {N} of them, sorted by engagement rate.',
  'micro': '7-day free trial, then $69/month. Search fitness creators by city, followers and engagement.',
  'list': '{N} US fitness influencers', 'band': 'Reach fitness influencers directly', 'steps': 'How to run a fitness influencer campaign',
  'faqs': [
   ('Who are the top fitness influencers on Jem Social?', 'By engagement rate, the top three on this page are {top3}.', None),
   ('How many fitness influencers are on Jem Social?', 'Jem Social lists {total} US creators tagged fitness with at least 5,000 followers as of {M}. This page shows {N} of them, sorted by engagement rate.', None),
   ('What engagement rate do fitness influencers get?', 'The median engagement rate among the {N} creators on this page is {med}. Engagement varies with audience size, so compare creators in the same follower range.', None),
   ('How much do fitness influencers charge?', "Rates depend on followers, platform and deliverables. The Influencer Rate Calculator gives a starting point, and each creator's rate estimate is in Jem Social.",
    "Rates depend on followers, platform and deliverables. The <a href=\"/influencer-rate-calculator\" class=\"jp-inline-link\">Influencer Rate Calculator</a> gives a starting point, and each creator's rate estimate is in Jem Social."),
   ('How do I find fitness influencers near me?', 'Search Jem Social by niche and city, or start with the city pages linked below.', None),
   ('How do I contact these creators?', "Start a 7-day free trial to see each creator's email and audience data, then message them from Jem Social.", None),
   ('How much does Jem Social cost?', 'Jem Social costs $69 per month after a 7-day free trial. One plan covers creator search in every city and niche, outreach and campaign management.', None)],
  'links': [('More fitness lists', [('/famous-fitness-influencers', 'Famous fitness influencers'), ('/biggest-fitness-influencers', 'Biggest fitness influencers'),
                                    ('/black-fitness-influencers', 'Black fitness influencers'), ('/most-successful-fitness-influencers-females', 'Most successful female fitness influencers')]),
            ('Tools', [('/engagement-rate-calculator', 'Engagement rate calculator'), ('/influencer-rate-calculator', 'Influencer rate calculator'),
                       ('/campaign-brief-generator', 'Campaign brief generator'), ('/creator-pages/how-to-pitch-brands-as-a-fitness-creator', 'For creators: pitch fitness brands')])],
  'old': ['find-fitness-influencers', 'best-fitness-influencers', 'top-fitness-influencers'], 'show': 50, 'pages': 2, 'tiers': True},
 'tech-ugc-creators': {
  'search': {'niche': 'tech', 'query': 'ugc', 'location': 'United States'}, 'niche': 'tech', 'Label': 'Tech UGC Creators', 'crumb': 'Tech', 'more_label': 'Tech UGC creators',
  'parent': ('/influencers/ugc-creators', 'UGC creators'), 'drop': r'\b(?:nail|lash|brow|vet|pharmacy|surgical|esthetic|hair|massage) tech',
  'noun': 'tech UGC creators', 'who': 'US tech UGC creators', 'scope': 'tagged tech and based in the US, whose profiles mention UGC', 'city_niche': False,
  'h1': 'Top {N} Tech UGC Creators to Hire ({M})', 'title': 'Top {N} Tech UGC Creators to Hire ({Mon}) | Jem Social',
  'desc': "Browse {N} of Jem Social's {total} US tech UGC creators with follower counts and engagement rates.",
  'intro': 'Jem Social has {total} US creators tagged tech whose profiles mention UGC, with at least 5,000 followers. Here are {N} of them, sorted by engagement rate.',
  'micro': '7-day free trial, then $69/month. Search UGC creators by niche, city, followers and engagement.',
  'list': '{N} tech UGC creators', 'band': 'Hire tech UGC creators for your app or product', 'steps': 'How to hire tech UGC creators',
  'faqs': [
   ('What is tech UGC?', 'Tech UGC is creator-made video and photo content for apps, software and gadgets, such as app walkthroughs, unboxings, '
    'setup tours and first-impression reviews. Brands run it in their own ads and social channels.', None),
   ('How many tech UGC creators are on Jem Social?', 'As of {M}, {total} US creators tagged tech mention UGC in their profiles and have at least 5,000 followers. This page shows {N} of them, sorted by engagement rate.', None),
   ('How much do tech UGC creators charge?', "Rates depend on the deliverables, usage rights and the creator's experience. The UGC Rate Card Generator gives a starting point, and each creator's rate estimate is in Jem Social.",
    "Rates depend on the deliverables, usage rights and the creator's experience. The <a href=\"/ugc-rate-card-generator\" class=\"jp-inline-link\">UGC Rate Card Generator</a> gives a starting point, and each creator's rate estimate is in Jem Social."),
   ('How do I hire tech UGC creators for my app?', "Start a 7-day free trial to see each creator's email and audience data. Then message them and pay through Jem Social, with funds held until you approve the content.",
    "Start a 7-day free trial to see each creator's email and audience data. Then message them and pay through Jem Social, with funds held until you approve the content. "
    "<a href=\"/hire-tech-ugc-creators\" class=\"jp-inline-link\">See how app teams hire tech UGC creators</a>."),
   ('How much does Jem Social cost?', 'For brands, Jem Social costs $69 per month after a 7-day free trial. For creators, pitching brands is free, or $20 per month for Premium.', None)],
  'links': [('Tech UGC', [('/hire-tech-ugc-creators', 'Hire tech UGC creators for your app'), ('/use-cases/hire-tech-ugc-creators-and-influencers', 'UGC for apps and tech products'),
                          ('/blog/tech-ugc', 'Tech UGC guide for creators'), ('/ugc-rate-card-generator', 'UGC rate card generator')]),
            ('More UGC', [('/influencers/ugc-creators', 'All UGC creators'), ('/free-ugc-contract-template', 'Free UGC contract template'), ('/blog/what-is-ugc', 'What is UGC?')])],
  'old': []},
}
TOOLS = [('/engagement-rate-calculator', 'Engagement rate calculator'), ('/influencer-rate-calculator', 'Influencer rate calculator'),
         ('/campaign-brief-generator', 'Campaign brief generator')]
def national(slug, label, lbl, noun, search, scope, fphrase='with at least 5,000 followers', city_niche=False, define=None, extra=(), old=None, drop=None, niche_label=None):
    base = slug
    faqs = [(f'Who are the top {lbl} on Jem Social?', 'By engagement rate, the top three on this page are {top3}.', None),
            (f'How many {lbl} are on Jem Social?', 'Jem Social lists {total} US ' + noun + ' ' + fphrase + ' as of {M}. This page shows {N} of them, sorted by engagement rate.', None)]
    if define: faqs.append(define)
    faqs += [(f'What engagement rate do {lbl} get?', 'The median engagement rate among the {N} creators on this page is {med}. Engagement varies with audience size, so compare creators in the same follower range.', None),
             (f'How much do {lbl} charge?', "Rates depend on followers, platform and deliverables. The Influencer Rate Calculator gives a starting point, and each creator's rate estimate is in Jem Social.",
              "Rates depend on followers, platform and deliverables. The <a href=\"/influencer-rate-calculator\" class=\"jp-inline-link\">Influencer Rate Calculator</a> gives a starting point, and each creator's rate estimate is in Jem Social."),
             ('How do I contact these creators?', "Start a 7-day free trial to see each creator's email and audience data, then message them from Jem Social.", None),
             ('How much does Jem Social cost?', 'Jem Social costs $69 per month after a 7-day free trial. One plan covers creator search in every city and niche, outreach and campaign management.', None)]
    return slug, {
        'search': search, 'niche': search.get('niche') or slug, 'Label': label, 'crumb': lbl, 'noun': noun, 'who': f'US {noun}',
        'scope': scope, 'fphrase': fphrase, 'city_niche': city_niche, 'city_label': f'{lbl} by city' if city_niche else 'Influencers by city',
        'h1': f'Top {{N}} {label} for Brands ({{M}})', 'title': f'Top {{N}} {label} for Brands ({{Mon}}) | Jem Social',
        'desc': f"Browse {{N}} of Jem Social's {{total}} US {lbl} with follower counts and engagement rates.",
        'intro': f'Jem Social has {{total}} US {noun} {fphrase}. Here are {{N}} of them, sorted by engagement rate.',
        'micro': '7-day free trial, then $69/month. Search creators by niche, city, followers and engagement.',
        'list': f'{{N}} US {lbl}', 'band': f'Reach {lbl} directly', 'steps': f'How to run a campaign with {lbl}',
        'faqs': faqs, 'links': ([('Related pages', list(extra))] if extra else []) + [('Tools', TOOLS)],
        'old': old if old is not None else [f'find-{base}-influencers', f'best-{base}-influencers', f'top-{base}-influencers', f'{base}-influencers'],
        **({'drop': drop} if drop else {}), **({'niche_label': niche_label} if niche_label else {})}
US = 'United States'
NATIONAL = [
 national('golf', 'Golf Influencers', 'golf influencers', 'golf creators', {'niche': 'golf', 'location': US}, 'tagged golf and based in the US'),
 national('fashion', 'Fashion Influencers', 'fashion influencers', 'fashion creators', {'niche': 'fashion', 'location': US}, 'tagged fashion and based in the US',
          city_niche='fashion', extra=[('/urban-fashion-influencers', 'Urban fashion influencers'), ('/amazon-mens-fashion-influencers', "Amazon men's fashion influencers"),
                                       ('/creator-pages/how-to-pitch-brands-as-a-fashion-creator', 'For creators: pitch fashion brands')]),
 national('micro', 'Micro Influencers', 'micro influencers', 'micro influencers', {'location': US, 'min_followers': 10000, 'max_followers': 100000},
          'based in the US', fphrase='with 10,000 to 100,000 followers', city_niche=None,
          define=('What is a micro influencer?', 'On this page, a micro influencer is a creator with 10,000 to 100,000 followers. Definitions vary between agencies and platforms.', None),
          extra=[('/blog-micro-influencer-vs-macro-influencer', 'Micro vs. macro influencers'), ('/influencer-marketing/micro-influencer', 'Micro influencer marketing'),
                 ('/find-influencers/micro-influencer-platform', 'Micro influencer platform')],
          old=['find-micro-influencers', 'best-micro-influencers', 'top-micro-influencers', 'micro-influencers']),
 national('beauty', 'Beauty Influencers', 'beauty influencers', 'beauty creators', {'niche': 'beauty', 'location': US}, 'tagged beauty and based in the US',
          city_niche='beauty', extra=[('/top-beauty-influencers', 'Top beauty influencers'), ('/clean-beauty-influencers', 'Clean beauty influencers'),
                                      ('/creator-pages/how-to-pitch-brands-as-a-beauty-creator', 'For creators: pitch beauty brands')]),
 national('food', 'Food Influencers', 'food influencers', 'food creators', {'niche': 'food', 'location': US}, 'tagged food and based in the US',
          city_niche='food', extra=[('/famous-food-influencers', 'Famous food influencers'), ('/food-and-beverage-influencers', 'Food and beverage influencers'),
                                    ('/local-food-influencers', 'Local food influencers'), ('/creator-pages/how-to-pitch-brands-as-a-food-creator', 'For creators: pitch food brands')]),
 national('nano', 'Nano Influencers', 'nano influencers', 'nano influencers', {'location': US, 'min_followers': 1000, 'max_followers': 10000},
          'based in the US', fphrase='with 1,000 to 10,000 followers', city_niche=None,
          define=('What is a nano influencer?', 'On this page, a nano influencer is a creator with 1,000 to 10,000 followers. Definitions vary between agencies and platforms.', None),
          extra=[('/influencers/micro', 'Micro influencers (10K to 100K)')], old=['find-nano-influencers', 'best-nano-influencers', 'top-nano-influencers', 'nano-influencers']),
 national('travel', 'Travel Influencers', 'travel influencers', 'travel creators', {'niche': 'travel', 'location': US}, 'tagged travel and based in the US',
          extra=[('/top-travel-influencers', 'Top travel influencers'), ('/creator-pages/how-to-pitch-brands-as-a-travel-creator', 'For creators: pitch travel brands')]),
 national('lifestyle', 'Lifestyle Influencers', 'lifestyle influencers', 'lifestyle creators', {'niche': 'lifestyle', 'location': US}, 'tagged lifestyle and based in the US',
          extra=[('/influencers/fashion', 'Fashion influencers'), ('/influencers/beauty', 'Beauty influencers'), ('/influencers/travel', 'Travel influencers')]),
 national('wellness', 'Wellness Influencers', 'wellness influencers', 'wellness creators', {'niche': 'wellness', 'location': US}, 'tagged wellness and based in the US',
          extra=[('/influencers/fitness', 'Fitness influencers'), ('/influencers/food', 'Food influencers'), ('/influencers/beauty', 'Beauty influencers')]),
 national('mom', 'Mom Influencers', 'mom influencers', 'mom creators', {'niche': 'mom', 'location': US}, 'tagged mom and based in the US',
          extra=[('/influencers/food', 'Food influencers'), ('/influencers/fitness', 'Fitness influencers'), ('/influencers/micro', 'Micro influencers')]),
 national('tech', 'Tech Influencers', 'tech influencers', 'tech creators', {'niche': 'tech', 'location': US}, 'tagged tech and based in the US',
          drop=r'\b(?:nail|lash|brow|vet|pharmacy|surgical|esthetic|hair|massage) tech|\b(?:virginia|georgia|texas|louisiana|tennessee) tech\b',
          extra=[('/influencers/tech-ugc-creators', 'Tech UGC creators'), ('/influencers/ugc-creators', 'UGC creators')]),
 national('cooking', 'Cooking Influencers', 'cooking influencers', 'cooking creators', {'niche': 'cooking', 'location': US}, 'tagged cooking and based in the US',
          extra=[('/influencers/food', 'Food influencers'), ('/influencers/wellness', 'Wellness influencers')]),
 national('music', 'Music Influencers', 'music influencers', 'music creators', {'niche': 'music', 'location': US}, 'tagged music and based in the US'),
 national('menswear', 'Menswear Influencers', 'menswear influencers', 'menswear creators', {'niche': 'fashion', 'query': 'menswear', 'location': US},
          'tagged fashion and based in the US, whose profiles mention menswear',
          define=('What is a menswear influencer?', 'On this page, a menswear influencer is a US fashion creator whose profile mentions menswear.', None),
          extra=[('/influencers/fashion', 'All fashion influencers'), ('/influencers/fitness', 'Fitness influencers')],
          old=['male-fashion-influencers', 'find-male-fashion-influencers', 'top-male-fashion-influencers', 'find-menswear-influencers', 'menswear-influencers']),
 national('outdoor', 'Outdoor Influencers', 'outdoor influencers', 'outdoor creators', {'niche': 'outdoor', 'location': US}, 'tagged outdoor and based in the US',
          extra=[('/influencers/travel', 'Travel influencers'), ('/influencers/fitness', 'Fitness influencers'), ('/influencers/golf', 'Golf influencers')]),
 national('pets', 'Pet Influencers', 'pet influencers', 'pet creators', {'niche': 'pets', 'location': US}, 'tagged pets and based in the US',
          extra=[('/influencers/ugc-creators', 'UGC creators'), ('/influencers/outdoor', 'Outdoor influencers'), ('/influencers/mom', 'Mom influencers')],
          old=['pet-influencers', 'find-pet-influencers', 'top-pet-influencers', 'best-pet-influencers', 'dog-influencers', 'find-dog-influencers',
               'top-dog-influencers', 'find-pets-influencers']),
 national('tiktok', 'TikTok Influencers', 'TikTok influencers', 'TikTok creators', {'platform': 'tiktok', 'location': US},
          'whose main platform is TikTok, based in the US', niche_label='TikTok',
          extra=[('/influencers/ugc-creators', 'UGC creators'), ('/influencers/micro', 'Micro influencers'), ('/influencers/fitness', 'Fitness influencers')]),
 national('amazon', 'Amazon Influencers', 'Amazon influencers', 'creators matched to Amazon', {'query': 'amazon', 'location': US},
          "matched to Amazon by Jem Social's keyword search and based in the US", niche_label='Amazon',
          define=('What is an Amazon influencer?', 'Usually a creator in the Amazon Influencer Program, with an Amazon storefront that earns commission on the '
                  "products they recommend. This page lists creators that Jem Social's keyword search matches to Amazon.", None),
          extra=[('/influencers/lifestyle', 'Lifestyle influencers'), ('/influencers/mom', 'Mom influencers'), ('/influencers/fashion', 'Fashion influencers')]),
]
TOPICS.update(dict(NATIONAL))
def slugify(s): return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')
def esc(s): return html.escape(str(s), quote=True)
def slug_for(city, st, niche): return f'{slugify(city)}-{st.lower()}' if not niche else f'{niche}-influencers-in-{slugify(city)}-{st.lower()}'
def page_url(slug): return f'{SITE}/influencers/{slug}'
def signup(slug): return f'{SIGNUP}?plan=price_1RH6oxB5nBZIUygBaJwlEgXP&amp;source=seo_city&amp;utm_source=seo&amp;utm_medium=city-page&amp;utm_campaign={slug}'
ROLE = {'creator', 'coach', 'trainer', 'influencer', 'blogger', 'vlogger', 'model', 'official', 'fitness', 'lifestyle', 'beauty',
        'fashion', 'food', 'foodie', 'travel', 'pro', 'aging', 'community', 'ugc', 'content', 'personal', 'mua', 'stylist', 'chef',
        'photographer', 'photography', 'photo', 'llc'}
GENERIC = ROLE | {'collaboration', 'collaborations', 'collab', 'collabs', 'brands', 'brand', 'with', 'and', 'for', '&', 'dm', 'business', 'inquiries'}
def clean_name(raw, handle):
    s = unicodedata.normalize('NFKC', raw or '')
    s = re.sub(r'^[^\w]+', '', s)
    s = re.split(r'\s[|•·–—/-]\s|\s*[|•·]\s*|,|\s\(|\[', s)[0]
    s = re.split(r'[^\w\s.\'’“”"&+-]', s)[0]
    if '-' in s:
        left, right = s.split('-', 1)
        if ' ' in right.strip() and re.search(r'\b(?:' + '|'.join(NICHE_WORDS.values()) + r'|health|functional|wellness|' + '|'.join(ROLE) + ')', right.lower()):
            s = left
    words = s.split()
    while len(words) > 1 and words[-1].lower().strip('.') in ROLE: words.pop()
    s = ' '.join(words).strip(" .-'")
    if s.isupper() and len(s) > 3: s = ' '.join(w.capitalize() if len(w) > 2 else w for w in s.split())
    elif s.islower(): s = s.title()
    if not s or all(w.lower().strip('.') in GENERIC for w in s.split()): return handle
    return s
def save(name, obj): json.dump(obj, open(f'{W}/{name}', 'w'), ensure_ascii=False)
def load(name): return json.load(open(f'{W}/{name}'))
def km(a, b):
    (la1, lo1), (la2, lo2) = a, b
    p = math.pi / 180
    h = math.sin((la2 - la1) * p / 2) ** 2 + math.cos(la1 * p) * math.cos(la2 * p) * math.sin((lo2 - lo1) * p / 2) ** 2
    return 12742 * math.asin(math.sqrt(h))
_last = [0.0]
def wf(method, path, body=None, tries=6):
    for k in range(tries):
        gap = time.time() - _last[0]
        if gap < 0.7: time.sleep(0.7 - gap)
        _last[0] = time.time()
        req = urllib.request.Request(API + path, method=method, data=None if body is None else json.dumps(body).encode(),
                                     headers={'Content-Type': 'application/json', 'Accept': 'application/json'})
        if os.environ.get('WEBFLOW_TOKEN'): req.add_header('Authorization', 'Bearer ' + os.environ['WEBFLOW_TOKEN'])
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                raw = r.read(); return json.loads(raw) if raw else {}
        except urllib.error.HTTPError as e:
            msg = e.read().decode('utf-8', 'replace')[:400]
            if e.code == 429 or e.code >= 500:
                time.sleep(int(e.headers.get('Retry-After') or 0) or 3 * (k + 1)); continue
            raise RuntimeError(f'Webflow {method} {path}: {e.code} {msg}')
        except urllib.error.URLError:
            time.sleep(3 * (k + 1))
    raise RuntimeError(f'Webflow {method} {path}: gave up after {tries} tries')
def list_items(coll):
    out, off = [], 0
    while True:
        d = wf('GET', f'/collections/{coll}/items?limit=100&offset={off}')
        out += d.get('items') or []; off += 100
        if off >= (d.get('pagination') or {}).get('total', 0): return out
def old_slugs():
    p = f'{W}/old_slugs.json'
    if os.path.exists(p) and time.time() - os.path.getmtime(p) < 7 * 86400: return set(load('old_slugs.json'))
    s = sorted(it['fieldData']['slug'] for it in list_items(OLD_COLL) if not it['isDraft'] and not it.get('isArchived'))
    save('old_slugs.json', s); return set(s)
def asset_photos():
    out, off = {}, 0
    while True:
        d = wf('GET', f'/sites/{SITE_ID}/assets?limit=100&offset={off}')
        for a in d.get('assets') or []:
            m = re.fullmatch(r'creator-([a-z0-9-]+)\.jpg', a.get('displayName') or '')
            if m and a.get('originalFileName'): out.setdefault(m.group(1), f'{CDN}{SITE_ID}/{a["originalFileName"]}')
        off += 100
        if off >= (d.get('pagination') or {}).get('total', 0): return out
def publish(ids):
    for i in range(0, len(ids), 100): wf('POST', f'/collections/{COLL}/items/publish', {'itemIds': ids[i:i + 100]})
def n_rows(f): return (f.get('creators-table') or '').count('class="jp-rank"')
def want_robots(f): return 'index, follow' if f.get('approved') and n_rows(f) >= MIN_INDEX else 'noindex, follow'
def iter_json(t):
    d, i, t = json.JSONDecoder(), 0, (t or '').strip()
    while i < len(t):
        while i < len(t) and t[i] in ' \n\r\t,': i += 1
        if i >= len(t): break
        try: o, i = d.raw_decode(t, i)
        except ValueError:
            nxt = t.find('{', i + 1)
            if nxt < 0: break
            i = nxt; continue
        yield o
def blocks(content):
    raw = [x.get('text', '') for x in content if isinstance(x, dict)] if isinstance(content, list) else [str(content or '')]
    out = []
    for t in raw:
        m = re.search(r'saved to (/\S+?\.txt)', t)
        if m and os.path.exists(m.group(1)):
            data = open(m.group(1)).read()
            try: out += [x.get('text', '') for x in json.loads(data)]
            except Exception: out.append(data)
        else: out.append(t)
    return out
def jkey(q):
    n = q.get('niche') or None
    return (tuple(n) if isinstance(n, list) else n, q.get('location'), q.get('query') or None, q.get('platform') or None,
            q.get('min_followers'), q.get('max_followers'), q.get('cursor') or None)
def jem():
    path = os.environ.get('JEM_TRANSCRIPT') or max(glob.glob(os.path.expanduser('~/.claude/projects/*/*.jsonl')), key=os.path.getmtime)
    uses, res = {}, {}
    for line in open(path):
        try: o = json.loads(line)
        except Exception: continue
        c = (o.get('message') or {}).get('content')
        if not isinstance(c, list): continue
        for b in c:
            if b.get('type') == 'tool_use': uses[b['id']] = b
            elif b.get('type') == 'tool_result' and b.get('tool_use_id') in uses:
                u = uses[b['tool_use_id']]
                if not u.get('name', '').endswith('search_influencers'): continue
                i = u.get('input', {})
                for t in blocks(b.get('content')):
                    for r in iter_json(t):
                        if isinstance(r, dict) and 'results' in r: res[jkey(i)] = r
    return res
def fnum(n):
    if n >= 1e6: s = f'{n / 1e6:.1f}M'
    elif n >= 1e5: s = f'{round(n / 1e3)}K'
    elif n >= 1e3: s = f'{n / 1e3:.1f}K'
    else: s = str(n)
    return s.replace('.0M', 'M').replace('.0K', 'K')
def fer(x): return f'{x:.1f}%'
def cmd_plan():
    items, today = list_items(COLL), datetime.date.today()
    by = {it['fieldData']['slug']: it for it in items}
    work = []
    def add(city, st, niche, it, new, slug=None):
        work.append({'new': new, 'id': it['id'] if it else None, 'city': city, 'st': st, 'niche': niche, 'slug': slug or slug_for(city, st, niche)})
    def waiting(it):
        if not it: return True
        f, fp = it['fieldData'], it['fieldData'].get('data-fingerprint') or ''
        if not it['isDraft'] and f.get('creators-table'): return False
        return not (fp.startswith('skip:') and (today - datetime.date.fromisoformat(fp[5:15])).days < SKIP_DAYS)
    for sl, t in TOPICS.items():
        if sum(w['new'] for w in work) < MAX_NEW and waiting(by.get(sl)): add('', '', t['niche'], by.get(sl), True, sl)
    for nichs in PASSES:
        for city, st, *_ in PRIORITY:
            for n in nichs:
                if sum(w['new'] for w in work) >= MAX_NEW: break
                it = by.get(slug_for(city, st, n))
                if waiting(it): add(city, st, n, it, True)
    def age(it):
        d = (it['fieldData'].get('data-updated') or '')[:10]
        return (today - datetime.date.fromisoformat(d)).days if d else 999
    live = [it for it in items if not it['isDraft'] and it['fieldData'].get('creators-table')]
    stale = [it for it in live if age(it) >= REFRESH_DAYS or not (it['fieldData'].get('data-fingerprint') or '').startswith(FPV)]
    for it in sorted(stale, key=age, reverse=True)[:MAX_REFRESH]:
        f = it['fieldData']; add(f.get('city') or '', f.get('state') or '', f.get('niche') or None, it, False, f['slug'])
    for sl in [x.strip() for x in os.environ.get('FORCE', '').split(',') if x.strip()]:
        it = by.get(sl)
        if it and sl not in {w['slug'] for w in work}:
            f = it['fieldData']; add(f.get('city') or '', f.get('state') or '', f.get('niche') or None, it, False, sl)
    save('plan.json', {'work': work, 'date': today.isoformat()})
    print(f'{sum(w["new"] for w in work)} new + {sum(not w["new"] for w in work)} refresh pages ({len(items)} items in the collection).')
    print('\nsearch_influencers calls, one per line; use exactly these arguments:')
    for w in work:
        for q in search_list(w): print(json.dumps(q))
def cursor(offset): return base64.b64encode(json.dumps({'offset': offset}, separators=(',', ':')).encode()).decode()
def tier_args(w):
    base = {k: v for k, v in search_args(w).items() if k not in ('limit', 'min_followers', 'max_followers')}
    return [{**base, 'min_followers': lo, **({'max_followers': hi} if hi else {}), 'limit': 1} for lo, hi, _ in TIERS]
def search_list(w):
    t, q = TOPICS.get(w['slug']) or {}, search_args(w)
    return [q] + [{**q, 'cursor': cursor(25 * p)} for p in range(1, t.get('pages', 1))] + (tier_args(w) if t.get('tiers') else [])
def search_args(w):
    t = TOPICS.get(w['slug'])
    q = dict(t['search']) if t else {'location': LOCATION.get((w['city'], w['st']), f"{w['city']}, {w['st']}")}
    if w['niche'] and not t: q = {'niche': w['niche'], **q}
    return {'min_followers': 5000, **q, 'limit': 25}
def off_niche(name, niche):
    if niche not in NICHE_WORDS: return False
    t, rx = name.lower(), lambda k: re.search(r'\b(?:' + NICHE_WORDS[k] + ')', t)
    if rx(niche): return False
    return any(rx(k) for k in NICHE_WORDS if k != niche)
def candidates(res, exclude, niche, drop=None, min_f=5000):
    rows, seen = [], set()
    for r in res.get('results') or []:
        p, plat = r.get('profile') or {}, (r.get('platform') or '').lower()
        u = (p.get('username') or '').strip().lstrip('@')
        f, er = p.get('followers'), p.get('engagement_percent')
        if plat not in PLAT or not u or not p.get('picture') or not f or er is None or er <= 0 or er > MAX_ER or f < min_f: continue
        if u.lower() in exclude or u.lower() in seen or off_niche(p.get('full_name') or '', niche): continue
        if drop and re.search(drop, (p.get('full_name') or '').lower()): continue
        seen.add(u.lower())
        rows.append({'u': u, 'hs': slugify(u), 'name': clean_name(p.get('full_name'), u), 'pic': p['picture'],
                     'f': int(f), 'er': float(er), 'plat': plat})
    return sorted(rows, key=lambda r: -r['er'])
def pil():
    try:
        from PIL import Image; return Image
    except Exception:
        for k in [k for k in sys.modules if k == 'PIL' or k.startswith('PIL.')]: del sys.modules[k]
        lib = os.path.expanduser('~/pylib')
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-q', '--target', lib, 'pillow'], capture_output=True)
        sys.path.insert(0, lib)
        from PIL import Image; return Image
S3 = [('acl', 'acl'), ('bucket', 'bucket'), ('X-Amz-Algorithm', 'xAmzAlgorithm'), ('X-Amz-Credential', 'xAmzCredential'),
      ('X-Amz-Date', 'xAmzDate'), ('key', 'key'), ('Policy', 'policy'), ('X-Amz-Signature', 'xAmzSignature'),
      ('success_action_status', 'successActionStatus'), ('Content-Type', 'contentType'), ('Cache-Control', 'cacheControl')]
def upload_photo(r):
    Image, path = pil(), f'{W}/photos/creator-{r["hs"]}.jpg'
    os.makedirs(f'{W}/photos', exist_ok=True)
    try:
        if not os.path.exists(path):
            im = Image.open(io.BytesIO(urllib.request.urlopen(r['pic'], timeout=20).read())).convert('RGB')
            s = min(im.size); l, t = (im.width - s) // 2, (im.height - s) // 2
            im.crop((l, t, l + s, t + s)).resize((72, 72), Image.LANCZOS).save(path, 'JPEG', quality=72, optimize=True)
        a = wf('POST', f'/sites/{SITE_ID}/assets', {'fileName': f'creator-{r["hs"]}.jpg', 'fileHash': hashlib.md5(open(path, 'rb').read()).hexdigest()})
        d = a.get('uploadDetails') or {}
        args = ['curl', '-sS', '-o', '/dev/null', '-w', '%{http_code}', a.get('uploadUrl') or 'https://webflow-prod-assets.s3.amazonaws.com/']
        for form, k in S3:
            v = d.get(form, d.get(k, d.get(form.lower())))
            if v is not None: args += ['-F', f'{form}={v}']
        args += ['-F', f'file=@{path};type=image/jpeg']
        code = subprocess.run(args, capture_output=True, text=True).stdout.strip()
        if code not in ('200', '201', '204'): print(f'  upload failed for @{r["u"]}: {code}'); return None
        key = d.get('key') or d.get('Key')
        return CDN + key if key else a.get('hostedUrl')
    except Exception as e:
        print(f'  photo failed for @{r["u"]}: {e}'); return None
def browse_links(niche, old, live):
    out = []
    if niche and niche in live: out.append((f'/influencers/{niche}', f'All US {niche} influencers'))
    elif niche and f'find-{niche}-influencers' in old: out.append((f'/find-influencers/find-{niche}-influencers', f'All {niche} influencers'))
    if 'ugc-creators' in live: out.append(('/influencers/ugc-creators', 'Hire UGC creators'))
    return out + [('/engagement-rate-calculator', 'Engagement rate calculator')]
def render(w, f, rows, total, photos, old, live):
    city, st, niche = w['city'], w['st'], w['niche']
    Niche = niche.capitalize() if niche else ''
    cs, slug, url = slugify(city), w['slug'], page_url(w['slug'])
    N = len(rows); total = max(total, N)
    ers = [r['er'] for r in rows]; fl = [r['f'] for r in rows]
    med = statistics.median(ers); lo, hi = min(fl), max(fl)
    plats = {}
    for r in rows: plats[r['plat']] = plats.get(r['plat'], 0) + 1
    top = max(plats, key=plats.get); share = round(100 * plats[top] / N)
    small = [r['er'] for r in rows if r['f'] < 50000]; big = [r['er'] for r in rows if r['f'] >= 100000]
    noun = f'{niche} creators' if niche else 'creators'
    who = f'{city} {noun}'
    t = TOPICS.get(slug)
    if t: noun, who, Niche = t['noun'], t['who'], t['Label']
    su = signup(slug)
    trs = ''.join(
        f'<div class="jp-row"><div class="jp-rank">{i}</div><div class="jp-who"><img class="jp-photo" src="{photos[r["hs"]]}" '
        f'alt="{esc(r["name"])}" width="36" height="36" loading="lazy"><div class="jp-who-text"><div class="jp-name">{esc(r["name"])}</div>'
        f'<a class="jp-handle-1" href="{PLAT[r["plat"]][1].format(r["u"])}" rel="nofollow noopener">@{esc(r["u"])}</a></div></div>'
        f'<div class="jp-plat">{PLAT[r["plat"]][0]}</div><div class="jp-num">{fnum(r["f"])}</div><div class="jp-num">{fer(r["er"])}</div>'
        f'<a class="jp-unlock" href="{su}">Unlock</a></div>' for i, r in enumerate(rows, 1))
    more = total - N
    more_html = (f'<span class="jp-more-count">+{more:,} more {esc(who)}</span><span class="jp-more-cta">Unlock the full list, free for 7 days →</span>'
                 if more > 0 else '<span class="jp-more-count">Contact info for every creator above</span><span class="jp-more-cta">See it free for 7 days →</span>')
    table = ('<div class="jp-table"><div class="jp-row jp-row-head"><div class="jp-th">#</div><div class="jp-th">Creator</div><div class="jp-th">Platform</div>'
             '<div class="jp-th jp-th-right">Followers</div><div class="jp-th jp-th-right">Engagement</div><div class="jp-th jp-th-right">Contact</div></div>'
             f'<div class="jp-rows">{trs}<a class="jp-more" href="{su}">{more_html}</a></div></div>')
    fp = FPV + hashlib.md5(json.dumps([total, [(r['u'], r['f'], round(r['er'], 2), r['plat']) for r in rows]] + ([w['tiers']] if w.get('tiers') else [])).encode()).hexdigest()
    pulled = (datetime.date.fromisoformat(f['data-updated'][:10]) if f.get('data-fingerprint') == fp and f.get('data-updated') else datetime.date.today())
    M, Mon = pulled.strftime('%B %Y'), pulled.strftime('%b %Y')
    def new_or_old(n, c, s):
        sl = slug_for(c, s, n)
        if sl in live and sl != slug: return f'/influencers/{sl}'
        if n:
            cc, ss = slugify(c), s.lower()
            for o in (f'find-{n}-influencers-in-{cc}', f'hire-{n}-influencers-in-{cc}-{ss}', f'hire-{n}-influencers-in-{cc}'):
                if o in old: return f'/find-influencers/{o}'
        elif f'influencers-in-{slugify(c)}' in old: return f'/find-influencers/influencers-in-{slugify(c)}'
    here = COORD.get((city, st))
    near_cities = sorted([(km(here, (la, lo)), c, s) for c, s, la, lo in PRIORITY if (c, s) != (city, st) and km(here, (la, lo)) < 800]) if here else []
    near = []
    for _, c, s in near_cities:
        h = new_or_old(niche, c, s)
        if h: near.append((h, f'{Niche} influencers in {c}' if niche else f'Influencers in {c}'))
        if len(near) == 4: break
    hub_url = new_or_old(None, city, st)
    if niche:
        other = ([(hub_url, f'All {city} influencers')] if hub_url else []) + \
                [(h, f'{m.capitalize()} influencers in {city}') for m in NICHES if m != niche for h in [new_or_old(m, city, st)] if h]
        cols = [(f'{Niche} near {city}', near[:3]), (f'More in {city}', other[:4])]
    else:
        other = [(h, f'{m.capitalize()} influencers in {city}') for m in NICHES for h in [new_or_old(m, city, st)] if h]
        cols = [(f'{city} by niche', other[:4]), (f'Influencers near {city}', near[:4])]
    cols.append(('Browse all', browse_links(niche, old, live)))
    if t:
        cn = t.get('city_niche')
        by_city = [] if cn is False else [(f'/influencers/{slug_for(c, s, cn)}', f'{cn.capitalize() + " influencers" if cn else "Influencers"} in {c}')
                   for c, s, *_ in PRIORITY if slug_for(c, s, cn) in live][:6]
        lab = lambda x: (x.get('more_label') or x['crumb'])[:1].upper() + (x.get('more_label') or x['crumb'])[1:]
        more = [(f'/influencers/{sl}', lab(TOPICS[sl])) for sl in TOPICS if sl != slug and sl in live][:4]
        cols = ([(t.get('city_label', 'Creators by city'), by_city)] if by_city else []) + t['links'] + ([('More creator lists', more)] if more else [])
    col = lambda lab, ls: (f'<div class="jp-related-col"><div class="jp-label">{esc(lab)}</div>' + ''.join(f'<a href="{h}" class="jp-link">{esc(t)}</a>' for h, t in ls) + '</div>') if ls else ''
    related = '<div class="jp-related">' + ''.join(col(a, b) for a, b in cols) + '</div>'
    crumb_city = (f'<a href="{hub_url}" class="jp-crumb-link">{esc(city)}</a>' if hub_url and niche else
                  f'<span class="jp-crumb-{"link" if niche else "current"}">{esc(city)}</span>')
    crumbs = f'<div class="jp-crumbs"><a href="/" class="jp-crumb-link">Home</a><span class="jp-crumb-sep">/</span>{crumb_city}' + \
             (f'<span class="jp-crumb-sep">/</span><span class="jp-crumb-current">{esc(Niche)}</span>' if niche else '') + '</div>'
    if t:
        par = (f'<a href="{t["parent"][0]}" class="jp-crumb-link">{esc(t["parent"][1])}</a><span class="jp-crumb-sep">/</span>' if t.get('parent') else '')
        crumbs = (f'<div class="jp-crumbs"><a href="/" class="jp-crumb-link">Home</a><span class="jp-crumb-sep">/</span>{par}'
                  f'<span class="jp-crumb-current">{esc(t["crumb"])}</span></div>')
    glance = lambda num, lab, d='': f'<div class="jp-glance-item{d}"><div class="jp-glance-num">{num}</div><div class="jp-glance-label">{esc(lab)}</div></div>'
    micro = esc(t['micro']) if t else f'7-day free trial, then $69/month. Search creators in every city and niche, not just {esc(city)}.'
    stats = (f'<p class="jp-micro">{micro}</p><div class="jp-glance">'
             + glance(f'{total:,}', f'{who} on Jem Social') + glance(fer(med), 'median engagement on this page', ' jp-glance-divider')
             + glance(f'{fnum(lo)}–{fnum(hi)}', 'follower range on this page', ' jp-glance-divider')
             + glance(f'{share}%', f'on {PLAT[top][0]}', ' jp-glance-divider') + '</div>')
    ins = []
    if len(small) >= 2 and len(big) >= 2:
        ins.append(f'The {len(small)} creators here with under 50K followers have a median engagement rate of {fer(statistics.median(small))}. '
                   f'The {len(big)} with 100K or more have a median of {fer(statistics.median(big))}.')
    k = sum(e >= 2 for e in ers)
    ins.append(f'All {N} creators have an engagement rate of 2% or higher.' if k == N else
               f'{k} of the {N} creators {"has" if k == 1 else "have"} an engagement rate of 2% or higher.' if k else
               f'None of the {N} creators has an engagement rate above 2%; the highest is {fer(max(ers))}.')
    if len(plats) == 1: ins.append(f'All {N} post mainly on {PLAT[top][0]}, with audiences from {fnum(lo)} to {fnum(hi)} followers.')
    else: ins.append('By main platform: ' + ', '.join(f'{c} on {PLAT[pl][0]}' for pl, c in sorted(plats.items(), key=lambda x: -x[1])) + f'. Audiences range from {fnum(lo)} to {fnum(hi)} followers.')
    if w.get('tiers'):
        parts = [f'{n:,} with {lab} followers' for lab, n in w['tiers']]
        ins.append(f'By audience size, Jem Social\'s {total:,} {who}: ' + ', '.join(parts[:-1]) + f' and {parts[-1]}.')
    insights = '<ul role="list" class="jp-insight-list">' + ''.join(f'<li class="jp-insight">{esc(t)}</li>' for t in ins) + '</ul>'
    calc = '<a href="/influencer-rate-calculator" class="jp-inline-link">Influencer Rate Calculator</a>'
    smaller_higher = len(small) >= 2 and len(big) >= 2 and statistics.median(small) > statistics.median(big)
    inf = f'{niche} influencers' if niche else 'influencers'
    faqs = []
    if niche == 'food':
        t3 = rows[:3]
        faqs.append((f'Who are the top foodies in {city}?', f'By engagement rate, the top three on this page are ' +
                     ', '.join(f'{r["name"]} (@{r["u"]})' for r in t3[:-1]) + f' and {t3[-1]["name"]} (@{t3[-1]["u"]}). '
                     f'Jem Social lists {total:,} food creators in the {city} area with at least 5,000 followers as of {M}.', None))
    faqs += [
        (f'How many {inf} are in {city}?', f'Jem Social lists {total:,} {noun} in the {city} area with at least 5,000 followers as of {M}. This page shows {N} of them, sorted by engagement rate.', None),
        (f'What engagement rate do {city} {inf} get?', f'The median engagement rate among the {N} creators on this page is {fer(med)}. ' +
         ('Smaller accounts often run higher than large ones, so compare creators in the same follower range.' if smaller_higher else 'Engagement varies with audience size, so compare creators in the same follower range.'), None),
        (f'How much do {city} {inf} charge?', "Rates depend on followers, platform and deliverables. The Influencer Rate Calculator gives a starting point, and each creator's rate estimate is in Jem Social.",
         f"Rates depend on followers, platform and deliverables. The {calc} gives a starting point, and each creator's rate estimate is in Jem Social."),
        ('How do I contact these creators?', "Start a 7-day free trial to see each creator's email and audience data, then message them from Jem Social.", None),
        ('How much does Jem Social cost?', 'Jem Social costs $69 per month after a 7-day free trial. One plan covers creator search in every city and niche, outreach and campaign management.', None)]
    faq = '<div class="jp-faq">' + ''.join(f'<div class="jp-qa"><h3 class="jp-q">{esc(q)}</h3><p class="jp-a">{h or esc(a)}</p></div>' for q, a, h in faqs) + '</div>'
    if not niche:
        h1, title = f'Top {N} Influencers in {city}, {st} ({M})', f'Top {N} {city} Influencers ({Mon}) | Jem Social'
        desc = f"Browse {N} of Jem Social's {total:,} {city} influencers with follower counts and engagement rates."
        intro = f'Jem Social has {total:,} creators in the {city} area with at least 5,000 followers. Here are {N} of them, from every niche, sorted by engagement rate.'
        list_h, band_h, steps_h = f'{N} {city} creators', f'Reach {city} creators directly', f'How to run an influencer campaign with {city} creators'
    elif niche == 'food':
        h1, title = f'{N} {city} Foodies & Food Influencers ({M})', f'{city} Foodies: {N} Top Food Influencers ({Mon}) | Jem Social'
        desc = f"Meet {N} of Jem Social's {total:,} {city} foodies and food creators, with follower counts and engagement rates."
        intro = f'Jem Social has {total:,} food creators in the {city} area with at least 5,000 followers. Here are {N} {city} foodies, sorted by engagement rate.'
        list_h, band_h, steps_h = f'{N} {city} foodies', f'Restaurant or food brand? Reach {city} food creators directly', f'How to run a food campaign with {city} creators'
    else:
        h1, title = f'{N} {Niche} Influencers in {city}, {st} ({M})', f'{N} {Niche} Influencers in {city}, {st} ({Mon}) | Jem Social'
        desc = f"Browse {N} of Jem Social's {total:,} {city} {niche} influencers with follower counts and engagement rates."
        intro = f'Jem Social has {total:,} {niche} creators in the {city} area with at least 5,000 followers. Here are {N} of them, sorted by engagement rate.'
        list_h, band_h, steps_h = f'{N} {city} {niche} creators', f'Reach {city} {niche} creators directly', f'How to run a {niche} campaign with {city} creators'
    if t:
        t3 = [f'{r["name"]} (@{r["u"]})' for r in rows[:3]]
        fm = lambda x: x.format(N=N, M=M, Mon=Mon, total=f'{total:,}', med=fer(med), top3=', '.join(t3[:-1]) + ' and ' + t3[-1])
        h1, title, desc, intro = fm(t['h1']), fm(t['title']), fm(t['desc']), fm(t['intro'])
        list_h, band_h, steps_h = fm(t['list']), t['band'], t['steps']
        faqs = [(q, fm(a), fm(h) if h else None) for q, a, h in t['faqs']]
        faq = '<div class="jp-faq">' + ''.join(f'<div class="jp-qa"><h3 class="jp-q">{esc(q)}</h3><p class="jp-a">{h or esc(a)}</p></div>' for q, a, h in faqs) + '</div>'
    if len(title) > 60: title = title.replace(' | Jem Social', '')
    meta = desc + ' See contact info with a 7-day free trial.'
    if len(meta) > 160: meta = desc
    person = lambda r: {'@type': 'Person', 'name': r['name'], 'alternateName': '@' + r['u'], 'url': PLAT[r['plat']][1].format(r['u']),
                        'interactionStatistic': {'@type': 'InteractionCounter', 'interactionType': 'https://schema.org/FollowAction', 'userInteractionCount': r['f']}}
    crumbs_ld = [{'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': SITE + '/'}]
    if niche and hub_url: crumbs_ld.append({'@type': 'ListItem', 'position': 2, 'name': city, 'item': SITE + hub_url})
    if t and t.get('parent'): crumbs_ld.append({'@type': 'ListItem', 'position': 2, 'name': t['parent'][1], 'item': SITE + t['parent'][0]})
    crumbs_ld.append({'@type': 'ListItem', 'position': len(crumbs_ld) + 1, 'name': Niche or city, 'item': url})
    graph = {'@context': 'https://schema.org', '@graph': [
        {'@type': 'WebPage', '@id': url + '#webpage', 'url': url, 'name': h1, 'description': desc, 'dateModified': pulled.isoformat(), 'inLanguage': 'en',
         'isPartOf': {'@type': 'WebSite', 'name': 'Jem Social', 'url': SITE + '/'}, 'breadcrumb': {'@id': url + '#breadcrumb'}, 'mainEntity': {'@id': url + '#list'}},
        {'@type': 'BreadcrumbList', '@id': url + '#breadcrumb', 'itemListElement': crumbs_ld},
        {'@type': 'ItemList', '@id': url + '#list', 'name': t['who'] if t else f'{Niche + " influencers" if niche else "Influencers"} in {city}, {st}', 'numberOfItems': N,
         'itemListOrder': 'https://schema.org/ItemListOrderDescending', 'itemListElement': [{'@type': 'ListItem', 'position': i, 'item': person(r)} for i, r in enumerate(rows, 1)]},
        {'@type': 'FAQPage', '@id': url + '#faq', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a, _ in faqs]}]}
    ld = json.dumps(graph, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
    rt = lambda x: f'<div data-rt-embed-type="true">{x}</div>'
    scope = t['scope'] if t else f'tagged {niche} and based in the {city} area' if niche else f'based in the {city} area, in any niche'
    method = (f'How this list was made: Jem Social creators {scope}, {t.get("fphrase", "with at least 5,000 followers") if t else "with at least 5,000 followers"}, sorted by engagement rate. '
              + ('Creators whose profile names point to a different niche are left out. ' if niche in NICHE_WORDS else '')
              + f'Engagement rates above {MAX_ER:g}% are left out as likely data errors. Data pulled from Jem Social on {pulled.strftime("%B")} {pulled.day}, {pulled.year}.')
    olds = [o for o in (t['old'] if t else [f'find-{niche}-influencers-in-{cs}', f'hire-{niche}-influencers-in-{cs}-{st.lower()}', f'hire-{niche}-influencers-in-{cs}']
                        if niche else [f'influencers-in-{cs}']) if o in old]
    approved = bool(f.get('approved'))
    out = {
        'name': f'{Niche + " " if niche else ""}Influencers in {city}, {st}', 'slug': slug, 'city': city, 'state': st,
        'niche': niche or '', 'niche-label': Niche,
        'h1': h1, 'intro': intro, 'hero-button-text': f'See all {total:,} creators, free for 7 days', 'creator-total': f'{total:,}',
        'stat-median-engagement': fer(med), 'stat-follower-range': f'{fnum(lo)}–{fnum(hi)}', 'stat-top-platform-share': f'{share}%',
        'stat-top-platform-label': f'on {PLAT[top][0]}', 'list-heading': list_h, 'method-note': method,
        'band-heading': band_h, 'band-text': f'See all {total:,}, then run the whole campaign in one place.',
        'steps-heading': steps_h, 'seo-title': title, 'meta-description': meta,
        'robots': 'index, follow' if approved and N >= MIN_INDEX else 'noindex, follow', 'updated-label': f'Updated {M}',
        'data-updated': pulled.isoformat() + 'T00:00:00.000Z', 'data-fingerprint': fp,
        'old-urls': ', '.join(f'/find-influencers/{o}' for o in olds),
        'breadcrumb': rt(crumbs), 'hero-stats': rt(stats), 'creators-table': rt(table), 'insights': rt(insights),
        'faq': rt(faq), 'related-links': rt(related), 'schema-markup': rt(f'<script type="application/ld+json">{ld}</script>')}
    if t: out.update({'name': t['Label'], 'niche-label': t.get('niche_label') or (t['niche'].upper() if len(t['niche']) <= 3 else t['niche'].capitalize())})
    return out
def cmd_run():
    plan, J = load('plan.json'), jem()
    items = list_items(COLL); by_id = {it['id']: it for it in items}
    by_slug = {it['fieldData']['slug']: it for it in items}
    exclude = set()
    for it in items: exclude |= {h.strip().lstrip('@').lower() for h in (it['fieldData'].get('exclude-handles') or '').split(',') if h.strip()}
    photos = asset_photos()
    for it in items:
        for u, hs in re.findall(r'src="(https://cdn\.prod\.website-files\.com/[^"]+?_creator-([a-z0-9-]+)\.jpg)"', it['fieldData'].get('creators-table') or ''):
            photos.setdefault(hs, u)
    old = old_slugs()
    live = {it['fieldData']['slug'] for it in items if not it['isDraft'] and it['fieldData'].get('creators-table')}
    rep = {'built': [], 'refreshed': [], 'unchanged': [], 'too_few': [], 'no_data': [], 'robots': [], 'uploaded': 0}
    for w in plan['work']:
        t = TOPICS.get(w['slug']) or {}
        res = J.get(jkey(search_args(w)))
        if not res: rep['no_data'].append(w['slug']); continue
        more_pages = [J.get(jkey({**search_args(w), 'cursor': cursor(25 * p)})) for p in range(1, t.get('pages', 1))]
        res = {**res, 'results': (res.get('results') or []) + [r for m in more_pages if m for r in (m.get('results') or [])]}
        if t.get('tiers'):
            got = [J.get(jkey(q)) for q in tier_args(w)]
            w['tiers'] = [(lab, int(g.get('total_estimate') or 0)) for (_, _, lab), g in zip(TIERS, got)] if all(got) else None
        rows = []
        for r in candidates(res, exclude, w['niche'], t.get('drop'), search_args(w)['min_followers']):
            if len(rows) == t.get('show', SHOW): break
            if r['hs'] not in photos:
                u = upload_photo(r)
                if not u: continue
                photos[r['hs']] = u; rep['uploaded'] += 1
            rows.append(r)
        w['rows'], w['total'] = rows, int(res.get('total_estimate') or 0)
        if w.get('tiers'): w['total'] = sum(n for _, n in w['tiers'])
        if len(rows) >= MIN_BUILD: live.add(w['slug'])
    pub = []
    for w in plan['work']:
        if 'rows' not in w: continue
        it = by_id.get(w['id']) or by_slug.get(w['slug'])
        f = it['fieldData'] if it else {}
        if len(w['rows']) < MIN_BUILD:
            rep['too_few'].append(f"{w['slug']} ({len(w['rows'])})")
            if w['new'] and w['slug'] not in TOPICS:
                mark = {'name': f"{(w['niche'] or '').capitalize() + ' ' if w['niche'] else ''}Influencers in {w['city']}, {w['st']}",
                        'slug': w['slug'], 'city': w['city'], 'state': w['st'], 'niche': w['niche'] or '', 'niche-label': (w['niche'] or '').capitalize(),
                        'data-fingerprint': f'skip:{datetime.date.today().isoformat()}:{len(w["rows"])}', 'robots': 'noindex, follow'}
                if it: wf('PATCH', f'/collections/{COLL}/items/{it["id"]}', {'fieldData': {'data-fingerprint': mark['data-fingerprint']}})
                else: wf('POST', f'/collections/{COLL}/items', {'isDraft': True, 'fieldData': mark})
            continue
        fd = render(w, f, w['rows'], w['total'], photos, old, live)
        if it:
            ch = {k: v for k, v in fd.items() if f.get(k) != v}
            if not ch and not it['isDraft']: rep['unchanged'].append(w['slug']); continue
            wf('PATCH', f'/collections/{COLL}/items/{it["id"]}', {'isDraft': False, 'fieldData': ch})
            iid = it['id']; f.update(ch)
        else:
            iid = wf('POST', f'/collections/{COLL}/items', {'isDraft': False, 'fieldData': fd})['id']
        (rep['built'] if w['new'] else rep['refreshed']).append(w['slug']); pub.append(iid)
    for it in list_items(COLL):
        f = it['fieldData']
        if it['isDraft'] or not f.get('creators-table') or it['id'] in pub: continue
        if f.get('robots') != want_robots(f):
            wf('PATCH', f'/collections/{COLL}/items/{it["id"]}', {'fieldData': {'robots': want_robots(f)}})
            rep['robots'].append(f"{f['slug']} -> {want_robots(f)}"); pub.append(it['id'])
    publish(pub)
    save('report.json', rep)
    print(json.dumps({k: (len(v) if isinstance(v, list) else v) for k, v in rep.items()}))
    for k in ('built', 'refreshed', 'too_few', 'no_data', 'robots'):
        if rep[k]: print(f'{k}: ' + ', '.join(rep[k]))
def cmd_report():
    r = load('report.json'); s = lambda k: ', '.join(r[k][:12]) or 'none'
    print(f"Jem city pages {datetime.date.today():%b %d}: built {len(r['built'])} ({s('built')}); refreshed {len(r['refreshed'])}; "
          f"unchanged {len(r['unchanged'])}; too few creators: {s('too_few')}; no Jem data: {s('no_data')}. "
          f"{len(r['robots'])} robots changes. New pages are live on jem.social/influencers/... as noindex until you approve them.")
if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'approve': cmd_approve(sys.argv[2:])
    elif cmd == 'relink': cmd_relink(dry='--dry' in sys.argv)
    else: {'plan': cmd_plan, 'run': cmd_run, 'report': cmd_report}[cmd]()
