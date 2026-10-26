"""Builds the three AfroTech carousels as one HTML file per slide (1080x1350). usage: python3 -I slides.py <out_dir>"""
import os, sys, html, json
OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
e = lambda s: html.escape(s, quote=True)

GREEN = dict(when='Sun, Nov 1 · 4–7 PM', name='The Green Room 🌿', where='Sanctuary EaDo · 2108 Leeland St', tag='Free with RSVP')
SAPPHIC = dict(when='Thu, Nov 5 · 8 PM–12 AM', name='Sapphic Hour 💻💖', where='Avant Garden · 411 Westheimer Rd', tag='From $11.99')

DECKS = {
 'creators': dict(
   title='AfroTech week for', acc='creators.', sub='6 rooms worth being in if you make content. Picked from our list of 101.',
   events=[
    ('Tue, Nov 3 · 5–10 PM', 'La Sala: AfroTech Kickoff', 'Fairfax · 81 Drew St', 'An intimate kickoff for the culturally connected. Come meet the people you’ll build with all week.', ['Free']),
    ('Tue, Nov 3 · 7–10 PM', 'ORIGINALITY: Influence vs Imagination', 'Sharespace Navigation · 3536 Navigation Blvd', 'An art exhibition on imagination vs influence, curated by Mueni Loko. Runs again Wed, Nov 4.', ['$30']),
    ('Wed, Nov 4 · 4:30–8 PM', 'Activated by AJANI', 'Seremoni Brick House · 1125 Providence St', 'Official AfroTech partner experience: wellness, movement, music, culture, shopping and food.', ['Partner']),
    ('Wed, Nov 4 · 5 PM–12 AM', 'Ladies in Tech & Entertainment Happy Hour', 'Fairfax · 81 Drew St', 'A night celebrating the women shaping tech and entertainment.', []),
    ('Thu, Nov 5 · Time TBA', 'Blavity House Party Block Party', 'Houston · Venue TBA', 'Official block party with special guests, live performances, DJs and a Food Village with Battle of Jollof.', ['Official']),
    ('Fri, Nov 6 · Time TBA', 'Black Women in Tech, Film & Creative Industries Brunch', 'Houston · Venue TBA', 'Guided networking, brand activations and a panel for Black women across tech, film and creative work.', ['Partner']),
   ],
   ours=[dict(GREEN, why='Jem Social is a sponsor, and Bree is on the panel Know Your Rights: Protecting What You Create.'),
         dict(SAPPHIC, why='Speed networking for women who love women in tech. Bree is co-hosting with LesbianLand.')]),
 'brands': dict(
   title='AfroTech week for', acc='brands.', sub='6 brand activations worth seeing in person. Picked from our list of 101.',
   events=[
    ('Wed, Nov 4 · 12–8 PM', 'AFROTECH × OOO Lounge: Cultural Living', 'The Grove · 1611 Lamar St', 'AfroTech’s official downtown lounge with Out of Office, built for connecting between sessions. Open Wed and Thu.', ['Official']),
    ('Wed, Nov 4 · 1–5 PM', 'Amazon House 2026', 'Location shared after RSVP approval', 'Amazon Amplify brings industry leaders and community changemakers together for conversations, onsite interviews and music.', ['RSVP approval']),
    ('Wed, Nov 4 · 5–9 PM', 'Access Unlocked by Microsoft', 'Private venue · request to attend', 'Microsoft’s House of Black TechXcellence: live feedback for makers, Copilot exploration, music and food.', ['Partner', '21+']),
    ('Wed, Nov 4 · 6:30–9:30 PM', 'The Cool Down: Powered by Martell', 'The Podium · 4007B Greenbriar Dr', 'A business-chic networking night built with Martell, Porsche, Selah, EveryDopeGirl and EveryDopeMan.', ['$30']),
    ('Thu, Nov 5 · 5–9 PM', 'Ancestry Presents: Black Tapestry', 'ART CLUB at POST Houston', 'Ancestry’s activation on culture, heritage and technology, with GRAMMY-winning artist Matt B.', ['Free', 'Partner']),
    ('Thu, Nov 5 · 7 PM–12 AM', 'A Mad Nice AfroTech', 'IYKYK · 1008 Prairie St', 'A Jack Daniel’s-sponsored night with Xavier Omär live, DJs and professional portraits.', ['From $25', '21+']),
   ],
   ours=[dict(GREEN, why='Meet creators and local sustainable designers. Jem Social is a sponsor.'),
         dict(SAPPHIC, why='Speed networking for women who love women in tech, co-hosted by Jem Social and LesbianLand.')]),
 'founders': dict(
   title='AfroTech week for', acc='founders.', sub='6 rooms for founders and builders, Tue to Fri. Picked from our list of 101.',
   events=[
    ('Tue, Nov 3 · Time TBA', 'CTRL + ALT + ALIGN: A Founder Reset', '3 Stories', 'A 60-minute Pilates barre reset for founders, builders and operators before the week gets loud.', ['Founders']),
    ('Tue, Nov 3 · 4–8 PM', 'Innovation x Culture Summit', 'The Ion · 4201 Main St', 'The Black Futures Market showcase, a fireside chat on culture and entrepreneurship, and a reception.', ['Free']),
    ('Wed, Nov 4 · 9:30–11:30 AM', 'Founder Power Breakfast', '10 min from the convention center', 'Mogul Millennial’s invite-only breakfast for Seed to Series A founders, with a fireside chat on customer acquisition.', ['Free', 'Apply']),
    ('Thu, Nov 5 · 5–8 PM', 'Conversation and Cocktails by Wilson Sonsini', 'Off the Record · 416 Main St', 'Happy hour with investor Terrence C. Murphy Sr. and DivInc CEO Tauri Laws-Phillips.', ['RSVP required']),
    ('Thu, Nov 5 · 6–10 PM', 'HuLane: Houston Edition', 'Prospect Park · 3100 Fountain View Dr', 'HuCapital and Black Men in Tech’s AI-powered matchmaking mixer for founders, creatives and recruiters.', ['Free']),
    ('Fri, Nov 6 · 6–9 PM', '6PM in Houston', 'The Podium at Porsche River Oaks', 'Builders, founders and operators in one room, with an activation that matches you with people to meet.', ['Free for first 200 by 7 PM']),
   ],
   ours=[dict(SAPPHIC, why='Speed networking for women who love women in tech, co-hosted by Jem Social and LesbianLand.')],
   extra=('Launching something this week?', 'Find creators for it on Jem Social. Search 30M+ UGC creators and influencers, then book and pay them in one place.', 'jem.social/influencer-finder')),
}

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1080px;height:1350px}
body{font-family:'Plus Jakarta Sans',sans-serif;-webkit-font-smoothing:antialiased;overflow:hidden}
.s{position:relative;width:1080px;height:1350px;padding:84px 84px 0;display:flex;flex-direction:column}
.dark{background:#0F1117;color:#fff}
.light{background:#fff;color:#0F1117}
.pink{background:#E322D0;color:#fff}
.glow::before{content:'';position:absolute;top:-260px;right:-220px;width:900px;height:900px;border-radius:50%;background:radial-gradient(circle,rgba(227,34,208,.42) 0,transparent 68%)}
.glow::after{content:'';position:absolute;bottom:-320px;left:-260px;width:900px;height:900px;border-radius:50%;background:radial-gradient(circle,rgba(72,223,244,.22) 0,transparent 68%)}
.z{position:relative;z-index:1}
.mono{font-family:'JetBrains Mono',monospace}
.acc{font-family:'Fraunces',serif;font-style:italic;font-weight:900;color:#E322D0}
.pill{display:inline-flex;align-items:center;gap:14px;padding:16px 26px;border-radius:999px;font-family:'JetBrains Mono',monospace;font-size:24px;font-weight:700;letter-spacing:.06em;text-transform:uppercase}
.dark .pill{background:rgba(255,255,255,.08);color:#48DFF4}
.light .pill{background:#FEF1FC;color:#B81AA8}
.pill i{width:12px;height:12px;border-radius:50%;background:#E322D0;display:block}
.foot{position:absolute;left:84px;right:84px;bottom:64px;display:flex;justify-content:space-between;align-items:center;font-family:'JetBrains Mono',monospace;font-size:24px;font-weight:700;z-index:2}
.logo{font-family:'Plus Jakarta Sans',sans-serif;font-size:40px;font-weight:800;letter-spacing:-.02em}
.logo b{display:inline-block;width:12px;height:12px;background:#E322D0;margin:0 3px -1px;border-radius:2px}
.pink .logo b{background:#fff}
.dark .foot .r{color:#48DFF4}.light .foot .r{color:#B81AA8}.pink .foot .r{color:#fff}
/* cover */
.cv h1{font-size:132px;line-height:.98;font-weight:800;letter-spacing:-.04em;margin:64px 0 40px}
.cv h1 .acc{display:block;font-size:150px;letter-spacing:-.02em}
.cv p{font-size:42px;line-height:1.35;color:rgba(255,255,255,.82);max-width:860px}
.cv .swipe{margin-top:72px;display:inline-flex;align-items:center;gap:18px;background:#E322D0;color:#fff;font-size:34px;font-weight:800;padding:26px 40px;border-radius:20px}
/* event */
.ev .num{font-family:'JetBrains Mono',monospace;font-size:30px;font-weight:700;color:#B81AA8;letter-spacing:.04em}
.ev .when{margin-top:56px;font-family:'JetBrains Mono',monospace;font-size:38px;font-weight:700;color:#0F1117}
.ev h2{margin-top:26px;font-size:84px;line-height:1.02;font-weight:800;letter-spacing:-.035em}
.ev .where{margin-top:28px;font-size:34px;font-weight:600;color:#5B5F6E}
.ev .why{margin-top:48px;background:#FEF1FC;border-left:10px solid #E322D0;border-radius:0 24px 24px 0;padding:38px 42px;font-size:40px;line-height:1.38;font-weight:600;color:#0F1117}
.ev .tags{margin-top:40px;display:flex;flex-wrap:wrap;gap:16px}
.tag{font-family:'JetBrains Mono',monospace;font-size:26px;font-weight:800;letter-spacing:.04em;text-transform:uppercase;padding:12px 20px;border-radius:12px;background:#F5F5F7;color:#5B5F6E}
.tag.free{background:#D9F9E9;color:#0A7A3E}.tag.off{background:#0F1117;color:#48DFF4}.tag.jem{background:#E322D0;color:#fff}
/* ours */
.ours h2{margin-top:56px;font-size:104px;line-height:1;font-weight:800;letter-spacing:-.04em}
.ours h2 .acc{color:#fff}
.ours .sub{margin-top:24px;font-size:38px;line-height:1.35;color:rgba(255,255,255,.9)}
.card{margin-top:40px;background:#fff;color:#0F1117;border-radius:28px;padding:40px 44px}
.card .w{font-family:'JetBrains Mono',monospace;font-size:28px;font-weight:700;color:#B81AA8}
.card h3{margin-top:12px;font-size:56px;line-height:1.05;font-weight:800;letter-spacing:-.03em}
.card .p{margin-top:12px;font-size:28px;font-weight:600;color:#5B5F6E}
.card .y{margin-top:18px;font-size:32px;line-height:1.38;font-weight:600}
.card.dk{background:#0F1117;color:#fff}.card.dk h3{font-size:50px;margin-top:0}
/* cta */
.cta h2{margin-top:56px;font-size:108px;line-height:1;font-weight:800;letter-spacing:-.04em}
.cta .box{display:inline-block;background:#E322D0;color:#fff;padding:6px 30px 14px;border-radius:24px;transform:rotate(-2deg);margin-top:18px}
.cta p{margin-top:40px;font-size:40px;line-height:1.38;color:rgba(255,255,255,.86);max-width:880px}
.stats{margin-top:40px;display:grid;grid-template-columns:1fr 1fr;gap:20px;max-width:900px}
.st{background:rgba(255,255,255,.07);border:2px solid rgba(255,255,255,.12);border-radius:24px;padding:22px 30px}
.st b{display:block;font-size:64px;font-weight:800;letter-spacing:-.03em;line-height:1}
.st span{font-family:'JetBrains Mono',monospace;font-size:26px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:#48DFF4}
.fine{margin-top:32px;font-family:'JetBrains Mono',monospace;font-size:24px;color:rgba(255,255,255,.6)}
"""
FONTS = ("<link rel='preconnect' href='https://fonts.googleapis.com'><link rel='preconnect' href='https://fonts.gstatic.com' crossorigin>"
         "<link href='https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600;700;800&family=Fraunces:ital,wght@1,900&family=JetBrains+Mono:wght@500;700;800&display=swap' rel='stylesheet'>")
def page(body, cls):
    return f"<!doctype html><html><head><meta charset='utf-8'>{FONTS}<style>{CSS}</style></head><body><div class='s {cls}'>{body}</div></body></html>"
def foot(i, n, right): return f"<div class='foot'><div class='logo'>jem<b></b>social</div><div class='r'>{right} · {i}/{n}</div></div>"
def tagcls(t):
    return 'free' if t.lower().startswith('free') else 'off' if t == 'Official' else ''

manifest = {}
for key, d in DECKS.items():
    slides = []
    n = 1 + len(d['events']) + 1 + 1
    slides.append(page(f"<div class='z cv'><div class='pill'><i></i>AfroTech 2026 · Houston · Nov 1–7</div>"
                       f"<h1>{e(d['title'])} <span class='acc'>{e(d['acc'])}</span></h1><p>{e(d['sub'])}</p>"
                       f"<div class='swipe'>Swipe for the list →</div></div>" + foot(1, n, 'Save this'), 'dark glow cv'))
    for i, (when, name, where, why, tags) in enumerate(d['events'], 1):
        tg = ''.join(f"<span class='tag {tagcls(t)}'>{e(t)}</span>" for t in tags)
        slides.append(page(f"<div class='z ev'><div class='num'>{i:02d} / {len(d['events']):02d}</div><div class='when'>{e(when)}</div>"
                           f"<h2>{e(name)}</h2><div class='where'>{e(where)}</div><div class='why'>{e(why)}</div><div class='tags'>{tg}</div></div>"
                           + foot(i + 1, n, 'Comment LINK for all 101'), 'light ev'))
    one = len(d['ours']) == 1
    ex = d.get('extra')
    cards = ''.join(f"<div class='card'><div class='w'>{e(o['when'])}</div><h3>{e(o['name'])}</h3><div class='p'>{e(o['where'])} · {e(o['tag'])}</div>"
                    f"<div class='y'>{e(o['why'])}</div></div>" for o in d['ours'])
    if ex: cards += f"<div class='card dk'><h3>{e(ex[0])}</h3><div class='y'>{e(ex[1])}</div><div class='w' style='margin-top:18px;color:#48DFF4'>{e(ex[2])} →</div></div>"
    slides.append(page(f"<div class='z ours'><div class='pill' style='background:rgba(255,255,255,.18);color:#fff'><i style='background:#fff'></i>Jem Social picks</div>"
                       f"<h2>Come find <span class='acc'>us.</span></h2><div class='sub'>{'The AfroTech week event we’re part of.' if one else 'The two AfroTech week events we’re part of.'}</div>{cards}</div>"
                       + foot(n - 1, n, 'See you there'), 'pink ours'))
    slides.append(page("<div class='z cta'><div class='pill'><i></i>All 101 events · one list</div>"
                       "<h2>Want the full list?<br><span class='box'>Comment LINK</span></h2>"
                       "<p>We’ll DM you all 101 AfroTech 2026 events with RSVP links, sorted by type.</p>"
                       "<div class='stats'><div class='st'><b>23</b><span>Parties</span></div><div class='st'><b>42</b><span>Networking</span></div>"
                       "<div class='st'><b>12</b><span>Career</span></div><div class='st'><b>34</b><span>Free events</span></div></div>"
                       "<div class='fine'>Free list. Confirm details on each event’s page.</div></div>"
                       + foot(n, n, 'Comment LINK'), 'dark glow cta'))
    files = []
    for j, s in enumerate(slides, 1):
        fn = f'{key}-{j:02d}.html'; open(f'{OUT}/{fn}', 'w').write(s); files.append(fn)
    manifest[key] = files
json.dump(manifest, open(f'{OUT}/manifest.json', 'w'), indent=1)
print({k: len(v) for k, v in manifest.items()})
