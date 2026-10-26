"""Builds the three AfroTech carousels as one HTML file per slide (1080x1350). usage: python3 -I slides.py <out_dir>"""
import os, sys, html, json
OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
# Threads has no comment-to-DM automation, so its CTA points to the link in the first reply
THREADS = len(sys.argv) > 2 and sys.argv[2] == 'threads'
CTA_FOOT, CTA_BOX, CTA_P = (('Link in replies', 'See replies ↓', 'The full list is in the first reply, with RSVP links, sorted by type. Free.') if THREADS else
                            ('Comment LINK', 'Comment LINK', 'We’ll DM you the full list with RSVP links, sorted by type. Free.'))
e = lambda s: html.escape(s, quote=True)

GREEN = dict(when='Sun, Nov 1 · 4–7 PM', name='The Green Room 🌿', where='Sanctuary EaDo · 2108 Leeland St', tag='Free with RSVP')
SAPPHIC = dict(when='Thu, Nov 5 · 8 PM–12 AM', name='Sapphic Hour 💻💖', where='Avant Garden · 411 Westheimer Rd', tag='From $11.99')

DECKS = {
 'creators': dict(
   title='AfroTech week for', acc='creators.', sub='6 rooms worth being in if you make content. Picked from our list of 101.',
   events=[
    ('Tue, Nov 3 · 5–10 PM', 'La Sala: AfroTech Kickoff', 'Fairfax · 81 Drew St', 'An intimate kickoff to meet the people you’ll build with all week.', ['Free']),
    ('Tue, Nov 3 · 7–10 PM', 'ORIGINALITY: Influence vs Imagination', 'Sharespace Navigation · 3536 Navigation Blvd', 'Art exhibition on imagination vs influence, curated by Mueni Loko. Also Wed.', ['$30']),
    ('Wed, Nov 4 · 4:30–8 PM', 'Activated by AJANI', 'Seremoni Brick House · 1125 Providence St', 'Official partner experience: wellness, music, culture, shopping and food.', ['Partner']),
    ('Wed, Nov 4 · 5 PM–12 AM', 'Ladies in Tech & Entertainment Happy Hour', 'Fairfax · 81 Drew St', 'A night celebrating the women shaping tech and entertainment.', []),
    ('Thu, Nov 5 · Time TBA', 'Blavity House Party Block Party', 'Houston · Venue TBA', 'Official block party: special guests, live sets, DJs and a Food Village.', ['Official']),
    ('Fri, Nov 6 · Time TBA', 'Black Women in Tech, Film & Creative Industries Brunch', 'Houston · Venue TBA', 'Guided networking, brand activations and a panel.', ['Partner']),
   ],
   ours=[dict(GREEN, why='Jem Social is a sponsor, and Bree is on the panel Know Your Rights: Protecting What You Create.'),
         dict(SAPPHIC, why='Speed networking for women who love women in tech. Bree is co-hosting with LesbianLand.')]),
 'brands': dict(
   title='AfroTech week for', acc='brands.', sub='6 brand activations worth seeing in person. Picked from our list of 101.',
   events=[
    ('Wed, Nov 4 · 12–8 PM', 'AFROTECH × OOO Lounge: Cultural Living', 'The Grove · 1611 Lamar St', 'AfroTech’s official downtown lounge for connecting between sessions. Wed + Thu.', ['Official']),
    ('Wed, Nov 4 · 1–5 PM', 'Amazon House 2026', 'Location shared after RSVP approval', 'Industry leaders and community changemakers, onsite interviews and music.', ['RSVP approval']),
    ('Wed, Nov 4 · 5–9 PM', 'Access Unlocked by Microsoft', 'Private venue · request to attend', 'Live feedback for makers, Copilot exploration, music and food.', ['Partner', '21+']),
    ('Wed, Nov 4 · 6:30–9:30 PM', 'The Cool Down: Powered by Martell', 'The Podium · 4007B Greenbriar Dr', 'Business-chic networking with Martell, Porsche, Selah and EveryDopeGirl.', ['$30']),
    ('Thu, Nov 5 · 5–9 PM', 'Ancestry Presents: Black Tapestry', 'ART CLUB at POST Houston', 'Culture, heritage and tech, with GRAMMY-winning artist Matt B.', ['Free', 'Partner']),
    ('Thu, Nov 5 · 7 PM–12 AM', 'A Mad Nice AfroTech', 'IYKYK · 1008 Prairie St', 'Jack Daniel’s-sponsored night: Xavier Omär live, DJs, pro portraits.', ['From $25', '21+']),
   ],
   ours=[dict(GREEN, why='Meet creators and local sustainable designers. Jem Social is a sponsor.'),
         dict(SAPPHIC, why='Speed networking for women who love women in tech, co-hosted by Jem Social and LesbianLand.')]),
 'founders': dict(
   title='AfroTech week for', acc='founders.', sub='6 rooms for founders and builders, Tue to Fri. Picked from our list of 101.',
   events=[
    ('Tue, Nov 3 · Time TBA', 'CTRL + ALT + ALIGN: A Founder Reset', '3 Stories', 'A 60-minute Pilates barre reset for founders before the week gets loud.', ['Founders']),
    ('Tue, Nov 3 · 4–8 PM', 'Innovation x Culture Summit', 'The Ion · 4201 Main St', 'Black Futures Market showcase, a fireside chat and a reception.', ['Free']),
    ('Wed, Nov 4 · 9:30–11:30 AM', 'Founder Power Breakfast', '10 min from the convention center', 'Invite-only for Seed to Series A founders. Fireside chat on customer acquisition.', ['Free', 'Apply']),
    ('Thu, Nov 5 · 5–8 PM', 'Conversation and Cocktails by Wilson Sonsini', 'Off the Record · 416 Main St', 'Happy hour with investor Terrence C. Murphy Sr. and DivInc CEO Tauri Laws-Phillips.', ['RSVP required']),
    ('Thu, Nov 5 · 6–10 PM', 'HuLane: Houston Edition', 'Prospect Park · 3100 Fountain View Dr', 'AI-powered matchmaking mixer for founders, creatives and recruiters.', ['Free']),
    ('Fri, Nov 6 · 6–9 PM', '6PM in Houston', 'The Podium at Porsche River Oaks', 'Builders, founders and operators in one room, plus an activation that matches you up.', ['Free for first 200 by 7 PM']),
   ],
   ours=[dict(SAPPHIC, why='Speed networking for women who love women in tech, co-hosted by Jem Social and LesbianLand.')],
   extra=('Launching something this week?', 'Find creators for it on Jem Social. Search 30M+ UGC creators and influencers, then book and pay them in one place.', 'jem.social/influencer-finder')),
}

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1080px;height:1350px}
body{font-family:'Plus Jakarta Sans',sans-serif;-webkit-font-smoothing:antialiased;overflow:hidden}
.s{position:relative;width:1080px;height:1350px;padding:84px 84px 0;display:flex;flex-direction:column}
.pink{background:#E322D0;color:#fff}.light{background:#fff;color:#0F1117}.dark{background:#0F1117;color:#fff}
.z{position:relative;z-index:1}
.acc{font-family:'Fraunces',serif;font-style:italic;font-weight:900}
.pill{display:inline-flex;align-items:center;gap:14px;padding:16px 26px;border-radius:999px;font-family:'JetBrains Mono',monospace;font-size:26px;font-weight:800;letter-spacing:.06em;text-transform:uppercase;background:#0F1117;color:#48DFF4;align-self:flex-start}
.pill i{width:12px;height:12px;border-radius:50%;background:#E322D0;display:block}
.dark .pill{background:#E322D0;color:#fff}.dark .pill i{background:#fff}
.foot{position:absolute;left:84px;right:84px;bottom:60px;display:flex;justify-content:space-between;align-items:center;font-family:'JetBrains Mono',monospace;font-size:26px;font-weight:800;z-index:2}
.logo{font-family:'Plus Jakarta Sans',sans-serif;font-size:42px;font-weight:800;letter-spacing:-.02em}
.logo b{display:inline-block;width:12px;height:12px;background:#E322D0;margin:0 3px -1px;border-radius:2px}
.pink .logo b{background:#0F1117}.pink .foot .r{color:#0F1117}.light .foot .r{color:#B81AA8}.dark .foot .r{color:#48DFF4}
/* cover */
.z.cv{flex:1;display:flex;flex-direction:column;padding-bottom:130px}
.cv .kick{margin-top:auto;font-size:56px;line-height:1.15;font-weight:700;letter-spacing:-.02em;color:#0F1117;max-width:880px}
.cv h1{margin-top:28px;font-size:128px;line-height:.95;font-weight:800;letter-spacing:-.045em}
.cv h1 .acc{display:block;margin-top:14px;font-size:200px;letter-spacing:-.02em;color:#0F1117}
.cv .row{margin-top:64px;margin-bottom:auto;display:flex;align-items:center;gap:22px}
.cv .swipe{background:#0F1117;color:#fff;font-size:40px;font-weight:800;padding:26px 40px;border-radius:22px}
.cv .share{font-size:34px;font-weight:700;color:#0F1117;line-height:1.25}
/* event */
.z.ev{flex:1;display:flex;flex-direction:column;justify-content:center;padding-bottom:120px}
.ev .top{display:flex;align-items:flex-end;justify-content:space-between;gap:24px}
.ev .big{font-family:'Fraunces',serif;font-style:italic;font-weight:900;font-size:210px;line-height:.78;color:#E322D0;letter-spacing:-.03em}
.ev .chip{background:#0F1117;color:#48DFF4;font-family:'JetBrains Mono',monospace;font-size:34px;font-weight:800;letter-spacing:.02em;padding:18px 26px;border-radius:18px;white-space:nowrap}
.ev h2{margin-top:56px;font-size:92px;line-height:1.0;font-weight:800;letter-spacing:-.04em}
.ev .where{margin-top:30px;font-size:38px;font-weight:600;color:#5B5F6E}
.ev .why{margin-top:40px;font-size:46px;line-height:1.3;font-weight:700;color:#0F1117;border-left:12px solid #E322D0;padding-left:34px}
.ev .tags{margin-top:40px;display:flex;flex-wrap:wrap;gap:16px}
.tag{font-family:'JetBrains Mono',monospace;font-size:30px;font-weight:800;letter-spacing:.04em;text-transform:uppercase;padding:14px 22px;border-radius:14px;background:#F2F2F5;color:#3F4350}
.tag.free{background:#D9F9E9;color:#0A7A3E}.tag.off{background:#0F1117;color:#48DFF4}
/* ours */
.ours h2{margin-top:52px;font-size:110px;line-height:1;font-weight:800;letter-spacing:-.045em}
.ours h2 .acc{color:#E322D0}
.ours .sub{margin-top:20px;font-size:38px;line-height:1.35;color:rgba(255,255,255,.88)}
.card{margin-top:36px;background:#fff;color:#0F1117;border-radius:28px;padding:38px 44px}
.card .w{font-family:'JetBrains Mono',monospace;font-size:30px;font-weight:800;color:#B81AA8}
.card h3{margin-top:10px;font-size:58px;line-height:1.05;font-weight:800;letter-spacing:-.03em}
.card .p{margin-top:12px;font-size:30px;font-weight:600;color:#5B5F6E}
.card .y{margin-top:16px;font-size:34px;line-height:1.35;font-weight:600}
.card.dk{background:#E322D0;color:#fff}.card.dk h3{font-size:52px;margin-top:0}.card.dk .w{color:#0F1117 !important}
/* cta */
.cta h2{margin-top:48px;font-size:126px;line-height:.98;font-weight:800;letter-spacing:-.045em}
.cta .box{white-space:nowrap;font-size:112px;display:inline-block;background:#0F1117;color:#fff;padding:10px 34px 18px;border-radius:26px;transform:rotate(-2deg);margin-top:22px}
.cta p{margin-top:48px;font-size:44px;line-height:1.3;font-weight:700;color:#0F1117;max-width:900px}
.stats{margin-top:36px;display:grid;grid-template-columns:1fr 1fr;gap:18px;max-width:912px}
.st{background:#0F1117;border-radius:24px;padding:22px 30px}
.st b{display:block;font-size:66px;font-weight:800;letter-spacing:-.03em;line-height:1;color:#fff}
.st span{font-family:'JetBrains Mono',monospace;font-size:26px;font-weight:800;letter-spacing:.06em;text-transform:uppercase;color:#48DFF4}
.cta .share{margin-top:32px;font-size:38px;font-weight:800;color:#fff}
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
                       f"<div class='kick'>We went through all 101 AfroTech events.</div>"
                       f"<h1>These 6 are for <span class='acc'>{e(d['acc'])}</span></h1>"
                       f"<div class='row'><div class='swipe'>Swipe →</div><div class='share'>📲 Send this to your<br>AfroTech crew</div></div></div>"
                       + foot(1, n, 'Save for this week' if key == 'founders' else 'Save for next week'), 'pink cv'))
    for i, (when, name, where, why, tags) in enumerate(d['events'], 1):
        tg = ''.join(f"<span class='tag {tagcls(t)}'>{e(t)}</span>" for t in tags)
        slides.append(page(f"<div class='z ev'><div class='top'><div class='big'>{i:02d}</div><div class='chip'>{e(when.upper())}</div></div>"
                           f"<h2>{e(name)}</h2><div class='where'>📍 {e(where)}</div><div class='why'>{e(why)}</div><div class='tags'>{tg}</div></div>"
                           + foot(i + 1, n, f'{CTA_FOOT} for all 101'), 'light ev'))
    one = len(d['ours']) == 1
    ex = d.get('extra')
    cards = ''.join(f"<div class='card'><div class='w'>{e(o['when'])}</div><h3>{e(o['name'])}</h3><div class='p'>{e(o['where'])} · {e(o['tag'])}</div>"
                    f"<div class='y'>{e(o['why'])}</div></div>" for o in d['ours'])
    if ex: cards += f"<div class='card dk'><h3>{e(ex[0])}</h3><div class='y'>{e(ex[1])}</div><div class='w' style='margin-top:16px'>{e(ex[2])} →</div></div>"
    slides.append(page(f"<div class='z ours'><div class='pill'><i></i>Jem Social picks</div>"
                       f"<h2>Come find <span class='acc'>us.</span></h2><div class='sub'>{'The AfroTech week event we’re part of.' if one else 'The two AfroTech week events we’re part of.'}</div>{cards}</div>"
                       + foot(n - 1, n, 'See you there'), 'dark ours'))
    slides.append(page("<div class='z cta'><div class='pill'><i></i>All 101 events · one list</div>"
                       f"<h2>Want all 101?<br><span class='box'>{CTA_BOX}</span></h2>"
                       f"<p>{CTA_P}</p>"
                       "<div class='stats'><div class='st'><b>23</b><span>Parties</span></div><div class='st'><b>42</b><span>Networking</span></div>"
                       "<div class='st'><b>12</b><span>Career</span></div><div class='st'><b>34</b><span>Free events</span></div></div>"
                       "<div class='share'>📲 Going with friends? Send them this.</div></div>"
                       + foot(n, n, CTA_FOOT), 'pink cta'))
    files = []
    for j, s in enumerate(slides, 1):
        fn = f'{key}-{j:02d}.html'; open(f'{OUT}/{fn}', 'w').write(s); files.append(fn)
    manifest[key] = files
json.dump(manifest, open(f'{OUT}/manifest.json', 'w'), indent=1)
print({k: len(v) for k, v in manifest.items()})
