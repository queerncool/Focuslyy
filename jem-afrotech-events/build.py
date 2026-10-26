#!/usr/bin/env python3
"""Builds the HtmlEmbed snippets for jem.social/afrotech-2026-events from Keith Azodeh's AfroTech sheet.
usage: python3 -I build.py <afrotech.xlsx> <out_dir>
"""
import openpyxl, sys, os, re, html, datetime, json, collections

SRC, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)
SIGNUP = 'https://app.jem.social/signup?source=afrotech_2026_list'
SNAPSHOT = 'Oct 26, 2026'
BASE = datetime.date(1899, 12, 30)
PREVIEW_DAYS = {1, 2}          # Sun Nov 1 + Mon Nov 2 stay open; the rest is gated
CATS = ['networking', 'party', 'social', 'career', 'founder', 'workshop']

def esc(s): return html.escape(str(s), quote=True)

# ---------- load + clean ----------
wb = openpyxl.load_workbook(SRC, data_only=True)
rows = list(wb['_Event Feed'].iter_rows(values_only=True))
hdr = rows[0]
raw = [dict(zip(hdr, r)) for r in rows[1:] if r[3]]

def mins(x):
    if isinstance(x, (int, float)): return round(float(x) * 1440) % 1440
    return None

def clock(m):
    h, mi = divmod(m, 60)
    return f"{(h % 12) or 12}:{mi:02d} {'AM' if h < 12 else 'PM'}"

events, seen = [], set()
for d in raw:
    date = BASE + datetime.timedelta(days=int(d['Date']))
    s, e = mins(d['Start']), mins(d['End'])
    if s is not None and e is not None and s >= 18 * 60 and 12 * 60 <= e < 17 * 60:
        e -= 12 * 60                      # "9:00 PM - 2:00 PM" in the sheet means 2 AM
    name = re.sub(r'\s+', ' ', str(d['Event'])).strip()
    key = (date, re.sub(r'[^a-z0-9]', '', name.lower()), s)
    if key in seen: continue              # exact duplicate rows (same event, day, start)
    seen.add(key)
    if s == 0 and e is not None and e >= 23 * 60: when = 'All day'
    elif s is None: when = 'Time TBA'
    else: when = clock(s)
    until = clock(e) if (s is not None and e is not None and when != 'All day' and e != s) else ''
    price = str(d['Price'] or '').strip()
    if price.lower() == 'free': ptxt, pk = 'Free', 'free'
    elif re.fullmatch(r'\d+(\.\d+)?', price): ptxt, pk = '$' + format(float(price), 'g'), 'paid'
    elif price.lower() == 'paid': ptxt, pk = 'Paid', 'paid'
    else: ptxt, pk = 'Price TBA', 'tba'
    cats = [c.strip().lower() for c in str(d['Categories'] or '').split(',') if c.strip()]
    venue = str(d['Venue'] or '').strip()
    if venue.upper() in ('TBA', 'TBD'): venue = ''
    addr = str(d['Address'] or '').strip()
    if addr.upper() in ('TBA', 'TBD'): addr = ''
    desc = re.sub(r'\s+', ' ', str(d['Description'] or '')).strip()
    full = desc
    if len(desc) > 210: desc = desc[:210].rsplit(' ', 1)[0].rstrip(',.;:-–— ') + '…'
    events.append(dict(date=date, s=s if s is not None else 9999, when=when, until=until, name=name,
                       host=str(d['Host'] or '').strip(), link=str(d['Details / Tickets'] or '').strip(),
                       ptxt=ptxt, pk=pk, type=str(d['Type'] or 'Community').strip(), cats=cats,
                       venue=venue, addr=addr, desc=desc, full=full))

events.sort(key=lambda x: (x['date'], x['s'], x['name'].lower()))
by_day = collections.OrderedDict()
for ev in events: by_day.setdefault(ev['date'], []).append(ev)

N = len(events)
N_FREE = sum(e['pk'] == 'free' for e in events)
TYPES = collections.Counter(e['type'] for e in events)
N_PREVIEW = sum(len(v) for k, v in by_day.items() if k.day in PREVIEW_DAYS)
N_LOCKED = N - N_PREVIEW
CAT_N = {c: sum(c in e['cats'] for e in events) for c in CATS}
busiest = sorted(by_day.items(), key=lambda kv: -len(kv[1]))[:2]
first, last = min(by_day), max(by_day)

def dayname(d, short=False): return d.strftime('%a' if short else '%A') + (f' {d.day}' if short else f', {d:%b} {d.day}')

# ---------- markup ----------
def card(ev):
    keys = ev['cats'] + [ev['type'].lower()] + (['free'] if ev['pk'] == 'free' else [])
    title = esc(ev['name'])
    if ev['link'].startswith('http'):
        title = f"<a href='{esc(ev['link'])}' target='_blank' rel='noopener nofollow'>{title}<span class='at-ext' aria-hidden='true'>↗</span></a>"
    place = ' · '.join(p for p in [esc(ev['venue']), esc(ev['addr']) if ev['addr'] and ev['addr'].lower() not in ev['venue'].lower() else ''] if p) or 'Venue TBA'
    meta = place + (f" · Hosted by {esc(ev['host'])}" if ev['host'] else '')
    tags = f"<span class='at-tag p-{ev['pk']}'>{esc(ev['ptxt'])}</span><span class='at-tag y-{esc(ev['type'].lower())}'>{esc(ev['type'])}</span>"
    tags += ''.join(f"<span class='at-tag'>{esc(c.capitalize())}</span>" for c in ev['cats'])
    until = f"<span>– {ev['until']}</span>" if ev['until'] else ''
    return (f"<article class='at-ev' data-k='{esc(' '.join(keys))}'><div class='at-ev-t'>{ev['when']}{until}</div>"
            f"<div class='at-ev-m'><h3 class='at-ev-h'>{title}</h3><div class='at-ev-meta'>{meta}</div>"
            + (f"<p class='at-ev-d'>{esc(ev['desc'])}</p>" if ev['desc'] else '') +
            f"<div class='at-tags'>{tags}</div></div></article>")

def day_block(d, evs):
    n = len(evs)
    return (f"<section class='at-dayblock' id='nov-{d.day}'><div class='at-day'><h2 class='at-day-h'>{dayname(d)}</h2>"
            f"<span class='at-day-n'>{n} event{'s' if n != 1 else ''}</span></div><div class='at-list'>"
            + ''.join(card(e) for e in evs) + "</div></section>")

FONTS = ("<link rel='preconnect' href='https://fonts.googleapis.com'><link rel='preconnect' href='https://fonts.gstatic.com' crossorigin>"
         "<link href='https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Fraunces:ital,wght@1,900&family=JetBrains+Mono:wght@400;600;700&display=swap' rel='stylesheet'>")

CSS = """
.jh,.jh *,.jh *::before,.jh *::after,[data-afro],[data-afro] *{box-sizing:border-box}
.jh,.jh *{margin:0;padding:0;border:0}
.jh,[data-afro]{font-family:'Plus Jakarta Sans',-apple-system,sans-serif !important;color:#0F1117;-webkit-font-smoothing:antialiased}
.jh{background:#fff;line-height:1.55;font-size:16px}
.jh a,[data-afro] a{text-decoration:none !important;cursor:pointer}
.at-mcta{display:none}
.jh-wrap,[data-afro=wrap]{max-width:1180px;margin:0 auto;padding:0 24px}
.jh-ann{background:#0F1117;color:#fff;text-align:center;padding:10px 16px;font-size:13px;font-weight:600}
.jh-ann strong{color:#48DFF4;font-weight:800}
.jh-ann a{color:#fff !important;border-bottom:1px solid rgba(255,255,255,.4);margin-left:6px}
.jh-nav{padding:18px 0;border-bottom:1px solid #EBECF0;background:#fff;position:relative;z-index:50}
.jh-nav-in{max-width:1180px;margin:0 auto;padding:0 24px;display:flex;align-items:center;justify-content:space-between;gap:24px}
.jh-logo{font-size:22px;font-weight:800;color:#0F1117 !important;letter-spacing:-.02em}
.jh-logo .sq{display:inline-block;width:7px;height:7px;background:#E322D0;margin:0 2px -1px;border-radius:1px}
.jh-nl{display:flex;gap:26px}
.jh-nl a{font-size:14px;font-weight:600;color:#5B5F6E !important}
.jh-nl a:hover{color:#0F1117 !important}
.jh-na{display:flex;gap:12px;align-items:center}
.jh-login{font-size:14px;font-weight:600;color:#5B5F6E !important}
.jh-cta-nav{background:#E322D0 !important;color:#fff !important;padding:10px 18px;border-radius:999px;font-size:14px;font-weight:700}
.jh-cta-nav:hover{background:#B81AA8 !important}
.jh-burger{display:none;background:none !important;border:0;padding:8px;cursor:pointer;flex-direction:column;gap:5px}
.jh-burger span{display:block;width:22px;height:2px;background:#0F1117;border-radius:2px;transition:.2s}
.jh-burger.on span:nth-child(1){transform:translateY(7px) rotate(45deg)}
.jh-burger.on span:nth-child(2){opacity:0}
.jh-burger.on span:nth-child(3){transform:translateY(-7px) rotate(-45deg)}
.jh-mm{display:none;position:absolute;top:100%;left:0;right:0;background:#fff;border-bottom:1px solid #EBECF0;box-shadow:0 20px 40px rgba(0,0,0,.08);padding:16px 24px 24px;flex-direction:column}
.jh-mm.on{display:flex}
.jh-mm a{padding:14px 0;border-bottom:1px solid #F5F5F7;font-size:16px;font-weight:600;color:#0F1117 !important;display:block}
.jh-mm a:last-child{border-bottom:0}
[data-afro=hero]{padding:56px 0 56px;position:relative;overflow:hidden;background:#fff}
[data-afro=hero]::before{content:'';position:absolute;top:-180px;right:-100px;width:640px;height:640px;background:radial-gradient(circle,rgba(227,34,208,.15) 0,transparent 70%);border-radius:50%;pointer-events:none}
[data-afro=hero]::after{content:'';position:absolute;bottom:-300px;left:-200px;width:600px;height:600px;background:radial-gradient(circle,rgba(72,223,244,.12) 0,transparent 70%);border-radius:50%;pointer-events:none}
[data-afro=grid]{position:relative;z-index:1;display:grid;grid-template-columns:1fr;gap:36px;align-items:center}
@media(min-width:960px){[data-afro=grid]{grid-template-columns:1.1fr 1fr;gap:56px}}
.jh-pill{display:inline-flex;align-items:center;gap:6px;background:#FEF1FC;color:#B81AA8 !important;padding:7px 14px;border-radius:999px;font-size:12px;font-weight:700;letter-spacing:.04em;text-transform:uppercase;margin-bottom:20px;font-family:'JetBrains Mono',monospace}
.jh-pill .dot{width:7px;height:7px;background:#E322D0;border-radius:50%}
.jh-h1{font-size:50px !important;font-weight:800 !important;line-height:1.03 !important;letter-spacing:-.03em !important;color:#0F1117 !important;margin-bottom:18px !important}
.jh-h1 .acc,.jh-h2 .acc,.at-card-h .acc{font-family:'Fraunces',serif !important;font-style:italic !important;font-weight:900 !important;color:#E322D0 !important}
.jh-lede{font-size:18px;color:#5B5F6E !important;line-height:1.6;margin-bottom:24px}
.jh-lede strong{color:#0F1117;font-weight:700}
.at-stats{display:flex;flex-wrap:wrap;gap:10px;margin-bottom:22px}
.at-stat{background:#fff;border:1px solid #EBECF0;border-radius:14px;padding:12px 16px;min-width:104px}
.at-stat b{display:block;font-size:24px;font-weight:800;letter-spacing:-.02em;color:#0F1117;line-height:1.1}
.at-stat span{font-family:'JetBrains Mono',monospace;font-size:10px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:#5B5F6E}
.at-credit{font-size:13px;color:#5B5F6E;line-height:1.6}
.at-credit a{color:#B81AA8 !important;font-weight:700;border-bottom:1px solid rgba(184,26,168,.3)}
[data-afro=card]{background:#fff;border-radius:22px;border:1px solid #EBECF0;box-shadow:0 30px 70px -20px rgba(15,17,23,.25),0 8px 24px rgba(15,17,23,.06);padding:28px 26px;scroll-margin-top:24px}
.at-card-eye{font-family:'JetBrains Mono',monospace;font-size:11px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;color:#B81AA8;margin-bottom:10px}
.at-card-h{font-size:28px;font-weight:800;letter-spacing:-.025em;line-height:1.1;color:#0F1117;margin-bottom:10px}
.at-card-p{font-size:15px;color:#5B5F6E;line-height:1.55;margin-bottom:14px}
.at-card-ul{list-style:none;margin:0 0 18px;padding:0}
.at-card-ul li{position:relative;padding-left:22px;font-size:14px;color:#0F1117;font-weight:600;margin-bottom:6px}
.at-card-ul li::before{content:'✓';position:absolute;left:0;color:#E322D0;font-weight:800}
.at-ok{display:none;background:#D9F9E9;color:#0A7A3E;border-radius:12px;padding:14px 16px;font-weight:700;font-size:15px;margin-bottom:6px}
.at-ok a{color:#0A7A3E !important;border-bottom:1px solid rgba(10,122,62,.4)}
html.afro-unlocked .at-ok{display:block}
html.afro-unlocked [data-afro=card] .w-form{display:none}
[data-afro=card] .w-form{margin:0}
[data-afro=card] form{margin:0}
.at-lbl,[data-afro=card] label{display:block;font-size:13px;font-weight:700;color:#0F1117;margin:0 0 6px}
[data-afro=card] .w-input,[data-afro=card] .at-select{display:block;width:100%;height:52px;padding:0 16px;margin:0 0 12px;font-size:16px;font-family:inherit;color:#0F1117;background:#FAFAFB;border:1px solid #EBECF0;border-radius:12px;box-shadow:none;outline:0;-webkit-appearance:none;appearance:none}
[data-afro=card] .at-select{background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='8' viewBox='0 0 12 8'%3E%3Cpath d='M1 1l5 5 5-5' stroke='%235B5F6E' stroke-width='2' fill='none'/%3E%3C/svg%3E");background-repeat:no-repeat;background-position:right 16px center;padding-right:40px}
[data-afro=card] .w-input:focus,[data-afro=card] .at-select:focus{border-color:#E322D0;background-color:#fff;box-shadow:0 0 0 3px rgba(227,34,208,.15)}
[data-afro=card] .w-button,[data-afro=card] input[type=submit]{display:block;width:100%;height:56px;margin-top:4px;background:#E322D0;color:#fff;border:0;border-radius:12px;font-family:inherit;font-size:16px;font-weight:800;cursor:pointer;box-shadow:0 8px 24px rgba(227,34,208,.25);-webkit-appearance:none;appearance:none}
[data-afro=card] .w-button:hover,[data-afro=card] input[type=submit]:hover{background:#B81AA8}
.at-fine{font-size:12px;color:#5B5F6E;line-height:1.5;margin-top:12px}
.at-fine a{color:#5B5F6E !important;text-decoration:underline !important}
[data-afro=card] .w-form-done{background:#D9F9E9;color:#0A7A3E;border-radius:12px;padding:16px;font-weight:700;text-align:left}
[data-afro=card] .w-form-fail{background:#FFF1F0;color:#B42318;border-radius:12px;padding:12px 14px;font-size:14px;font-weight:600;margin-top:10px}
.at-bar{position:sticky;top:0;z-index:40;background:rgba(255,255,255,.96);-webkit-backdrop-filter:blur(8px);backdrop-filter:blur(8px);border-top:1px solid #EBECF0;border-bottom:1px solid #EBECF0}
.at-bar-in{max-width:1180px;margin:0 auto;padding:12px 24px;display:flex;flex-direction:column;gap:10px}
.at-row{display:flex;gap:8px;overflow-x:auto;-webkit-overflow-scrolling:touch;scrollbar-width:none;padding-bottom:2px}
.at-row::-webkit-scrollbar{display:none}
.at-row-l{font-family:'JetBrains Mono',monospace;font-size:10px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;color:#8A8E9C;align-self:center;flex:0 0 auto;width:44px}
.at-chip,.at-f{flex:0 0 auto;display:inline-flex;align-items:center;gap:6px;padding:8px 14px;border-radius:999px;border:1px solid #EBECF0;background:#fff;font-family:inherit;font-size:13px;font-weight:700;color:#0F1117 !important;cursor:pointer;white-space:nowrap}
.at-chip:hover,.at-f:hover{border-color:#E322D0;color:#B81AA8 !important}
.at-f span,.at-chip span{font-family:'JetBrains Mono',monospace;font-size:11px;color:#8A8E9C;font-weight:600}
.at-f.on{background:#0F1117;border-color:#0F1117;color:#fff !important}
.at-f.on span{color:#48DFF4}
.at-lists{background:#fff;padding:8px 0 24px}
.at-dayblock{max-width:1180px;margin:0 auto;padding:28px 24px 8px;scroll-margin-top:120px}
.at-day{display:flex;align-items:baseline;justify-content:space-between;gap:16px;padding-bottom:12px;border-bottom:2px solid #0F1117;margin-bottom:4px}
.at-day-h{font-size:26px !important;font-weight:800 !important;letter-spacing:-.02em !important;color:#0F1117 !important;line-height:1.15 !important;margin:0 !important}
.at-day-n{font-family:'JetBrains Mono',monospace;font-size:12px;font-weight:700;color:#B81AA8;white-space:nowrap}
.at-ev{display:grid;grid-template-columns:132px 1fr;gap:20px;padding:20px 0;border-bottom:1px solid #EBECF0}
.at-ev-t{font-family:'JetBrains Mono',monospace;font-size:14px;font-weight:700;color:#0F1117;line-height:1.4}
.at-ev-t span{display:block;font-weight:400;color:#8A8E9C;font-size:12px}
.at-ev-h{font-size:18px !important;font-weight:800 !important;letter-spacing:-.015em !important;line-height:1.3 !important;color:#0F1117 !important;margin:0 0 4px !important}
.at-ev-h a{color:#0F1117 !important}
.at-ev-h a:hover{color:#B81AA8 !important}
.at-ext{font-size:13px;color:#B81AA8;margin-left:6px;font-weight:700}
.at-ev-meta{font-size:13px;color:#5B5F6E;font-weight:600;margin-bottom:6px}
.at-ev-d{font-size:14px;color:#5B5F6E;line-height:1.55;margin-bottom:10px;max-width:760px}
.at-tags{display:flex;flex-wrap:wrap;gap:6px}
.at-tag{font-family:'JetBrains Mono',monospace;font-size:10px;font-weight:800;letter-spacing:.04em;text-transform:uppercase;padding:4px 8px;border-radius:6px;background:#F5F5F7;color:#5B5F6E}
.at-tag.p-free{background:#D9F9E9;color:#0A7A3E}
.at-tag.p-paid{background:#FFF4E5;color:#9A5B00}
.at-tag.y-official{background:#FEF1FC;color:#B81AA8}
.at-tag.y-partner{background:#E6FBFE;color:#04768A}
[data-afro=lock]{position:relative;max-height:1150px;overflow:hidden}
[data-afro=lock] .at-ev{filter:blur(5px);-webkit-user-select:none;user-select:none;pointer-events:none}
html.afro-unlocked [data-afro=lock]{max-height:none;overflow:visible}
html.afro-unlocked [data-afro=lock] .at-ev{filter:none;-webkit-user-select:auto;user-select:auto;pointer-events:auto}
.at-over{position:absolute;left:0;right:0;bottom:0;height:560px;z-index:5;display:flex;align-items:flex-end;justify-content:center;padding:0 24px 56px;background:linear-gradient(180deg,rgba(255,255,255,0) 0,rgba(255,255,255,.92) 38%,#fff 62%)}
html.afro-unlocked .at-over{display:none}
.at-over-c{max-width:520px;text-align:center;background:#0F1117;color:#fff;border-radius:22px;padding:30px 28px;box-shadow:0 30px 70px -20px rgba(15,17,23,.45)}
.at-over-n{font-family:'JetBrains Mono',monospace;font-size:11px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;color:#48DFF4;margin-bottom:8px}
.at-over-h{font-size:24px;font-weight:800;letter-spacing:-.02em;line-height:1.15;margin-bottom:8px;color:#fff}
.at-over-p{font-size:14px;color:rgba(255,255,255,.8);margin-bottom:18px}
.jh-bp{display:inline-flex;align-items:center;gap:8px;background:#E322D0 !important;color:#fff !important;padding:15px 26px;border-radius:12px;font-size:15px;font-weight:700;box-shadow:0 8px 24px rgba(227,34,208,.25)}
.jh-bp:hover{background:#B81AA8 !important}
.at-empty{display:none;max-width:1180px;margin:0 auto;padding:32px 24px;color:#5B5F6E;font-weight:600}
.jh-sec{padding:72px 0}
.jh-sec.alt{background:#FAFAFB;border-top:1px solid #EBECF0;border-bottom:1px solid #EBECF0}
.jh-eye{display:inline-flex;background:#FEF1FC;color:#B81AA8 !important;padding:7px 14px;border-radius:999px;font-size:11px;font-weight:800;letter-spacing:.06em;text-transform:uppercase;margin-bottom:14px;font-family:'JetBrains Mono',monospace}
.jh-h2{font-size:36px !important;font-weight:800 !important;line-height:1.08 !important;letter-spacing:-.028em !important;color:#0F1117 !important;margin-bottom:14px !important;max-width:820px}
.jh-lede2{font-size:17px;color:#5B5F6E !important;line-height:1.65;margin-bottom:28px;max-width:760px}
.jh-ps{display:grid;grid-template-columns:1fr;gap:20px}
@media(min-width:900px){.jh-ps{grid-template-columns:1fr 1fr;gap:24px}}
.jh-ps-c{padding:32px 28px;border-radius:20px;position:relative}
.jh-ps-p{background:#fff;border:2px solid #E322D0}
.jh-ps-s{background:linear-gradient(135deg,#0F1117 0%,#1a1c25 100%);color:#fff;overflow:hidden}
.jh-ps-lbl{font-family:'JetBrains Mono',monospace;font-size:11px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;margin-bottom:10px;color:#B81AA8}
.jh-ps-s .jh-ps-lbl{color:#48DFF4}
.jh-ps-h{font-size:22px;font-weight:800;letter-spacing:-.02em;margin-bottom:12px;color:#0F1117;line-height:1.2}
.jh-ps-s .jh-ps-h{color:#fff}
.jh-ps-body{font-size:15px;line-height:1.6;color:#5B5F6E;margin-bottom:20px}
.jh-ps-s .jh-ps-body{color:rgba(255,255,255,.85)}
.jh-ps-cta{display:inline-flex;align-items:center;background:#0F1117 !important;color:#fff !important;padding:12px 20px;border-radius:99px;font-size:13px;font-weight:700}
.jh-ps-cta:hover{background:#E322D0 !important}
.jh-ps-s .jh-ps-cta{background:#fff !important;color:#0F1117 !important}
.jh-ps-s .jh-ps-cta:hover{background:#48DFF4 !important}
.jh-faq-list{max-width:820px;margin:28px 0 0}
.jh-faq-item{border-top:1px solid #EBECF0}
.jh-faq-item:last-child{border-bottom:1px solid #EBECF0}
.jh-faq-item summary{list-style:none;cursor:pointer;padding:20px 0;display:flex;justify-content:space-between;align-items:flex-start;gap:24px;font-size:17px;font-weight:700;color:#0F1117;line-height:1.35}
.jh-faq-item summary::-webkit-details-marker{display:none}
.jh-faq-item summary:hover{color:#B81AA8}
.jh-faq-item summary::after{content:'+';flex-shrink:0;width:26px;height:26px;display:flex;align-items:center;justify-content:center;background:#FEF1FC;color:#B81AA8;border-radius:8px;font-size:18px;font-weight:600;margin-top:2px}
.jh-faq-item[open] summary::after{content:'−';background:#E322D0;color:#fff}
.jh-faq-a{padding:0 0 20px;font-size:15px;line-height:1.65;color:#5B5F6E;max-width:720px}
.jh-faq-a a{color:#B81AA8 !important;font-weight:700}
.jh-faq-a strong{color:#0F1117;font-weight:700}
.jh-foot{padding:28px 0;background:#fff;border-top:1px solid #EBECF0;text-align:center;font-size:13px;color:#5B5F6E}
.jh-foot a{color:#5B5F6E !important;margin:0 8px}
.jh-foot a:hover{color:#E322D0 !important}
@media(max-width:960px){.jh-nl,.jh-login,.jh-cta-nav{display:none !important}.jh-burger{display:flex !important}}
@media(max-width:959px){.at-mcta{display:flex;justify-content:center;width:100%;margin:-4px 0 22px}}
@media(max-width:760px){.jh-h1{font-size:34px !important}.jh-lede{font-size:16px}.jh-h2{font-size:26px !important}[data-afro=hero]{padding:32px 0 36px}.jh-sec{padding:48px 0}[data-afro=card]{padding:22px 18px}.at-card-h{font-size:24px}.at-ev{grid-template-columns:1fr;gap:6px;padding:18px 0}.at-ev-t span{display:inline;margin-left:6px}.at-day-h{font-size:21px !important}.at-dayblock{padding:22px 16px 4px}.at-bar-in{padding:10px 16px}.at-row-l{display:none}.at-stat{min-width:0;flex:1 1 40%}.jh-ps-c{padding:24px 20px}.at-over{padding:0 16px 40px}.at-over-c{padding:24px 20px}.jh-wrap,[data-afro=wrap]{padding:0 16px}}
"""

def stat(n, label): return f"<div class='at-stat'><b>{n}</b><span>{label}</span></div>"

pieces = {}
pieces['A_head'] = FONTS + '<style>' + re.sub(r'\n', '', CSS) + "</style>" + f"""<div class='jh'><div class='jh-ann'>AfroTech week is {first:%b} {first.day}–{last.day}. <strong>{N} events</strong>, one list.<a href='#unlock'>Unlock it free →</a></div><nav class='jh-nav'><div class='jh-nav-in'><a href='https://www.jem.social/' class='jh-logo'>jem<span class='sq' aria-hidden='true'></span>social</a><div class='jh-nl'><a href='https://www.jem.social/for-brands'>For brands</a><a href='https://www.jem.social/earn-money-as-a-creator'>For creators</a><a href='https://www.jem.social/pricing'>Pricing</a><a href='https://www.jem.social/resources'>Resources</a></div><div class='jh-na'><a href='https://app.jem.social/login' class='jh-login'>Log in</a><a href='{SIGNUP}' class='jh-cta-nav'>Join Jem free →</a><button class='jh-burger' aria-label='Menu' onclick='jhNav()'><span></span><span></span><span></span></button></div><div class='jh-mm' id='jhMm'><a href='https://www.jem.social/for-brands'>For brands</a><a href='https://www.jem.social/earn-money-as-a-creator'>For creators</a><a href='https://www.jem.social/pricing'>Pricing</a><a href='https://www.jem.social/resources'>Resources</a><a href='https://app.jem.social/login'>Log in</a><a href='{SIGNUP}'>Join Jem free →</a></div></div></nav></div>"""

pieces['H_copy'] = f"""<div><div class='jh-pill'><span class='dot'></span>AfroTech 2026 · Houston · {first:%b} {first.day}–{last.day}</div><h1 class='jh-h1'>Every AfroTech 2026 event, <span class='acc'>in one list.</span></h1><p class='jh-lede'><strong>{N} parties, mixers, dinners, runs and official meetups</strong> happening around AfroTech week in Houston. Filter by day, price and vibe, and find your rooms before they fill up.</p><a href='#unlock' class='jh-bp at-mcta'>Unlock the full list ↓</a><div class='at-stats'>{stat(N, 'Events')}{stat(N_FREE, 'Listed free')}{stat(TYPES['Official'], 'Official')}{stat(len(by_day), 'Days')}</div><p class='at-credit'>Organized by Jem Social from public event listings. Updated {SNAPSHOT}.</p></div>"""

pieces['G_cardhead'] = f"""<div class='at-card-eye'>Free · {N} events · {first:%b} {first.day}–{last.day}</div><div class='at-card-h'>Get the <span class='acc'>full list.</span></div><p class='at-card-p'>Enter your email to unlock every event, {first:%A} through {last:%A}.</p><ul class='at-card-ul'><li>Ticket and RSVP links for every event</li><li>Filter by free, parties, networking and more</li><li>Official, partner and community events</li></ul><div class='at-ok'>✓ You're in. The full list is unlocked. <a href='#nov-3'>Jump to Tuesday ↓</a></div>"""

pieces['F_fields'] = """<label class='at-lbl' for='at-role'>I'm going as a…</label><select class='at-select' id='at-role' name='Role' required><option value=''>Choose one</option><option>Creator or influencer</option><option>Brand or marketer</option><option>Agency</option><option>Founder or builder</option><option>Just attending</option></select><input type='hidden' name='Source' value='afrotech-2026-events'>"""

pieces['F_fine'] = """<p class='at-fine'>By unlocking, you agree to get AfroTech updates and Jem Social emails. Unsubscribe anytime. <a href='https://www.jem.social/privacy-policy'>Privacy policy</a></p>"""

chips_day = ''.join(f"<a class='at-chip' href='#nov-{d.day}'>{d:%a} {d.day}<span>{len(v)}</span></a>" for d, v in by_day.items())
chips_f = f"<button type='button' class='at-f on' data-f='all' aria-pressed='true'>All<span>{N}</span></button>"
chips_f += f"<button type='button' class='at-f' data-f='free' aria-pressed='false'>Free<span>{N_FREE}</span></button>"
chips_f += f"<button type='button' class='at-f' data-f='official' aria-pressed='false'>Official<span>{TYPES['Official']}</span></button>"
chips_f += ''.join(f"<button type='button' class='at-f' data-f='{c}' aria-pressed='false'>{c.capitalize()}<span>{CAT_N[c]}</span></button>" for c in CATS if CAT_N[c])
pieces['P_preview'] = (f"<div class='jh'><div class='at-bar'><div class='at-bar-in'><div class='at-row'><span class='at-row-l'>Day</span>{chips_day}</div>"
                       f"<div class='at-row'><span class='at-row-l'>Show</span>{chips_f}</div></div></div><div class='at-lists'>"
                       + ''.join(day_block(d, v) for d, v in by_day.items() if d.day in PREVIEW_DAYS)
                       + "<div class='at-empty' id='at-empty'>No events match that filter on these days.</div></div></div>")

locked_days = [(d, v) for d, v in by_day.items() if d.day not in PREVIEW_DAYS]
groups, cur, size = [], [], 0
for d, v in locked_days:                 # keep each embed well under Webflow's embed size limit
    blk = day_block(d, v)
    if cur and size + len(blk) > 30000: groups.append(cur); cur, size = [], 0
    cur.append(blk); size += len(blk)
if cur: groups.append(cur)
for i, g in enumerate(groups, 1): pieces[f'L{i}'] = "<div class='jh'><div class='at-lists'>" + ''.join(g) + "</div></div>"

lfirst, llast = locked_days[0][0], locked_days[-1][0]
pieces['O_overlay'] = f"""<div class='jh'><div class='at-over'><div class='at-over-c'><div class='at-over-n'>{N_LOCKED} more events · {lfirst:%a}–{llast:%a}</div><div class='at-over-h'>The rest of AfroTech week is one email away.</div><p class='at-over-p'>Unlock {lfirst:%A} through {llast:%A}, including the busiest nights of the week.</p><a href='#unlock' class='jh-bp'>Unlock the full list ↑</a></div></div></div>"""

(b1d, b1), (b2d, b2) = busiest
faq = [
    ('When are the AfroTech 2026 events?', f"The events on this list run from <strong>{dayname(first)} through {dayname(last)}, 2026</strong>. The busiest days are {b1d:%A} ({len(b1)} events) and {b2d:%A} ({len(b2)} events)."),
    ('Where do the events take place?', "Most are in Houston. Some venues are only shared after you RSVP, so check each event's page for the address."),
    ('Are these official AfroTech events?', f"Some are. <strong>{TYPES['Official']} are marked official, {TYPES['Partner']} are partner events and {TYPES['Community']} are hosted by the community.</strong> Check each event's own page for entry requirements."),
    ('How many events are free?', f"{N_FREE} of the {N} events are listed as free. The rest are paid or haven't posted a price yet."),
    ('Who put this list together?', "Jem Social organized this list from public event pages and community event lists. Hosting an AfroTech event that's missing? Email <a href='mailto:support@jem.social'>support@jem.social</a>."),
    ('Is this list kept up to date?', f"This page reflects the list as of {SNAPSHOT}. Times, prices and venues change, so confirm on the event's link before you go."),
]
faq_html = ''.join(f"<details class='jh-faq-item'><summary>{q}</summary><div class='jh-faq-a'>{a}</div></details>" for q, a in faq)

SCRIPT = """<script>
function jhNav(){document.querySelector('.jh-burger').classList.toggle('on');document.getElementById('jhMm').classList.toggle('on');}
(function(){
var K='jem_afrotech26',H=document.documentElement;
var em=document.querySelector('[data-afro=card] input[type=email]');if(em&&!em.placeholder)em.placeholder='you@email.com';
function unlock(){H.classList.add('afro-unlocked');try{localStorage.setItem(K,'1')}catch(e){}}
try{if(localStorage.getItem(K)==='1')H.classList.add('afro-unlocked')}catch(e){}
var done=document.querySelector('[data-afro=card] .w-form-done');
if(done&&window.MutationObserver){new MutationObserver(function(){if(done.style.display&&done.style.display!=='none')unlock()}).observe(done,{attributes:true,attributeFilter:['style']})}
var fs=[].slice.call(document.querySelectorAll('.at-f')),evs=[].slice.call(document.querySelectorAll('.at-ev')),days=[].slice.call(document.querySelectorAll('.at-dayblock')),empty=document.getElementById('at-empty');
function apply(f){
 evs.forEach(function(e){e.style.display=(f==='all'||(' '+e.getAttribute('data-k')+' ').indexOf(' '+f+' ')>-1)?'':'none'});
 var openShown=0;
 days.forEach(function(d){var n=0;[].forEach.call(d.querySelectorAll('.at-ev'),function(e){if(e.style.display!=='none')n++});d.style.display=n?'':'none';var c=d.querySelector('.at-day-n');if(c)c.textContent=n+(n===1?' event':' events');if(!d.closest('[data-afro=lock]'))openShown+=n});
 if(empty)empty.style.display=openShown?'none':'block';
}
fs.forEach(function(b){b.addEventListener('click',function(){fs.forEach(function(x){x.classList.remove('on');x.setAttribute('aria-pressed','false')});b.classList.add('on');b.setAttribute('aria-pressed','true');apply(b.getAttribute('data-f'))})});
})();
</script>"""

pieces['C_tail'] = f"""<div class='jh'><section class='jh-sec alt'><div class='jh-wrap'><div class='jh-eye'>Heading to AfroTech?</div><h2 class='jh-h2'>Make the trip <span class='acc'>pay off.</span></h2><p class='jh-lede2'>AfroTech week is full of brands, founders and creators in the same rooms. Jem Social helps you turn those intros into partnerships.</p><div class='jh-ps'><div class='jh-ps-c jh-ps-p'><div class='jh-ps-lbl'>// For creators</div><div class='jh-ps-h'>Met a brand at a mixer? Pitch them after.</div><p class='jh-ps-body'>Jem's brand pitch tool keeps every pitch you send to brands in one place, for $20/mo.</p><a href='https://www.jem.social/brand-pitch-tool' class='jh-ps-cta'>See the brand pitch tool →</a></div><div class='jh-ps-c jh-ps-s'><div class='jh-ps-lbl'>// For brands</div><div class='jh-ps-h'>Find creators for your next activation.</div><p class='jh-ps-body'>Search 30M+ UGC creators and influencers on Jem Social, then book and pay them through Jem.</p><a href='https://www.jem.social/influencer-finder' class='jh-ps-cta'>Try the influencer finder →</a></div></div></div></section><section class='jh-sec'><div class='jh-wrap'><div class='jh-eye'>FAQ</div><h2 class='jh-h2'>AfroTech 2026 events, <span class='acc'>answered.</span></h2><div class='jh-faq-list'>{faq_html}</div></div></section><footer class='jh-foot'>© 2026 Jem Social · <a href='https://www.jem.social/'>Home</a> · <a href='https://www.jem.social/pricing'>Pricing</a> · <a href='mailto:support@jem.social'>Contact</a></footer></div>""" + SCRIPT

for k, v in pieces.items():
    open(f'{OUT}/{k}.html', 'w').write(v)
    print(f'{k:10s} {len(v):6d} chars')
json.dump(dict(N=N, N_FREE=N_FREE, TYPES=TYPES, N_PREVIEW=N_PREVIEW, N_LOCKED=N_LOCKED, days={str(k): len(v) for k, v in by_day.items()},
               cats=CAT_N, groups=len(groups)), open(f'{OUT}/stats.json', 'w'), indent=1, default=str)
print(open(f'{OUT}/stats.json').read())

import csv
with open(f'{OUT}/afrotech_2026_events.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['Date', 'Day', 'Start', 'End', 'Event', 'Host', 'Price', 'Type', 'Categories', 'Venue', 'Address', 'Tickets / RSVP', 'Description'])
    for e in events:
        w.writerow([e['date'].isoformat(), e['date'].strftime('%a'), e['when'], e['until'], e['name'], e['host'], e['ptxt'], e['type'],
                    ', '.join(c.capitalize() for c in e['cats']), e['venue'], e['addr'], e['link'], e['full']])
