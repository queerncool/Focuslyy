#!/usr/bin/env python3
"""Weekly data sync for Jem Social city pages (Webflow collection "City Influencer Pages").
Tool results are read from this Claude session's transcript, so large outputs never need retyping.
  plan     collection listing (labels sync:list:*) -> picks pages, prints Jem searches + old-slug checks
  photos   Jem results + old-slug checks -> picks creators, prepares photo files + create_asset batches
  upload   create_asset results (labels asset:*) -> uploads photo bytes to Webflow S3
  build    renders fieldData, writes update batches to ~/jem-sync/out/
  report   one-paragraph summary for Telegram
"""
import json, os, re, sys, glob, html, hashlib, statistics, subprocess, datetime, io, urllib.request
W = os.path.expanduser('~/jem-sync'); os.makedirs(W, exist_ok=True)
SITE_ID, COLL = '67b0d09acc5bda1c5c04566f', '6adc28d2f2806b611dd3a207'
SITE, SIGNUP, CDN = 'https://www.jem.social', 'https://app.jem.social/signup', 'https://cdn.prod.website-files.com/'
MAX_NEW, MAX_REFRESH, REFRESH_DAYS = int(os.environ.get('MAX_NEW', 10)), int(os.environ.get('MAX_REFRESH', 5)), 27
SHOW, MIN_BUILD, MIN_INDEX = 20, 5, 10
REFRESH_DAYS = int(os.environ.get('REFRESH_DAYS', REFRESH_DAYS))
NICHES = ['fitness', 'beauty', 'fashion', 'food', 'lifestyle', 'travel', 'wellness', 'tech', 'gaming']
PLAT = {'instagram': ('Instagram', 'https://www.instagram.com/{}/'), 'tiktok': ('TikTok', 'https://www.tiktok.com/@{}'),
        'youtube': ('YouTube', 'https://www.youtube.com/@{}')}
# (city slug, display, state) of nearby cities, nearest first
NEARBY = {
 'miami-fl': [('orlando', 'Orlando', 'fl'), ('tampa', 'Tampa', 'fl'), ('jacksonville', 'Jacksonville', 'fl'), ('saint-petersburg', 'St. Petersburg', 'fl')],
 'new-york-ny': [('jersey-city', 'Jersey City', 'nj'), ('newark', 'Newark', 'nj'), ('philadelphia', 'Philadelphia', 'pa')],
 'los-angeles-ca': [('long-beach', 'Long Beach', 'ca'), ('anaheim', 'Anaheim', 'ca'), ('santa-ana', 'Santa Ana', 'ca'), ('irvine', 'Irvine', 'ca'), ('san-diego', 'San Diego', 'ca')],
 'chicago-il': [('milwaukee', 'Milwaukee', 'wi'), ('indianapolis', 'Indianapolis', 'in'), ('detroit', 'Detroit', 'mi'), ('madison', 'Madison', 'wi')],
 'dallas-tx': [('fort-worth', 'Fort Worth', 'tx'), ('plano', 'Plano', 'tx'), ('irving', 'Irving', 'tx'), ('arlington', 'Arlington', 'tx'), ('austin', 'Austin', 'tx'), ('houston', 'Houston', 'tx')],
 'houston-tx': [('san-antonio', 'San Antonio', 'tx'), ('austin', 'Austin', 'tx'), ('dallas', 'Dallas', 'tx'), ('corpus-christi', 'Corpus Christi', 'tx')],
 'atlanta-ga': [('birmingham', 'Birmingham', 'al'), ('charlotte', 'Charlotte', 'nc'), ('nashville', 'Nashville', 'tn'), ('orlando', 'Orlando', 'fl')],
 'austin-tx': [('san-antonio', 'San Antonio', 'tx'), ('houston', 'Houston', 'tx'), ('dallas', 'Dallas', 'tx')],
 'san-diego-ca': [('chula-vista', 'Chula Vista', 'ca'), ('irvine', 'Irvine', 'ca'), ('santa-ana', 'Santa Ana', 'ca'), ('los-angeles', 'Los Angeles', 'ca')],
 'las-vegas-nv': [('henderson', 'Henderson', 'nv'), ('north-las-vegas', 'North Las Vegas', 'nv'), ('phoenix', 'Phoenix', 'az')],
}

def slugify(s): return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')
def esc(s): return html.escape(str(s), quote=True)
ROLE = {'creator', 'coach', 'trainer', 'influencer', 'blogger', 'vlogger', 'model', 'official', 'fitness', 'lifestyle', 'beauty',
        'fashion', 'food', 'foodie', 'travel', 'pro', 'aging', 'community', 'ugc', 'content', 'personal', 'mua', 'stylist', 'chef'}
def clean_name(raw, handle):
    # Jem names often carry bio text: "BRITTFIT MIAMI 🌴 Fitness community", "Alex P | Fitness Coach"
    s = re.split(r'\s[|•·–—/-]\s|\s*[|•·]\s*|,', raw or '')[0]
    s = re.split(r'[^\w\s.\'-]', s)[0]          # stop at the first emoji or symbol
    words = s.split()
    while len(words) > 1 and words[-1].lower().strip('.') in ROLE: words.pop()
    s = ' '.join(words).strip(" .-'")
    if s.isupper() and len(s) > 3: s = ' '.join(w.capitalize() if len(w) > 2 else w for w in s.split())
    return s or handle
def save(name, obj): json.dump(obj, open(f'{W}/{name}', 'w'), ensure_ascii=False)
def load(name): return json.load(open(f'{W}/{name}'))

# ---------- transcript reading ----------
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

def events():
    path = os.environ.get('JEM_TRANSCRIPT') or max(glob.glob(os.path.expanduser('~/.claude/projects/*/*.jsonl')), key=os.path.getmtime)
    uses, out = {}, []
    for line in open(path):
        try: o = json.loads(line)
        except Exception: continue
        c = (o.get('message') or {}).get('content')
        if not isinstance(c, list): continue
        for b in c:
            if b.get('type') == 'tool_use': uses[b['id']] = b
            elif b.get('type') == 'tool_result' and b.get('tool_use_id') in uses:
                out.append((uses[b['tool_use_id']], blocks(b.get('content'))))
    return out

def webflow(prefix):
    res = {}
    for use, bl in events():
        if 'Webflow' not in use.get('name', ''): continue
        for t in bl:
            for o in iter_json(t):
                if isinstance(o, dict) and str(o.get('label', '')).startswith(prefix): res[o['label']] = o
    return res

def jem():
    res = {}
    for use, bl in events():
        if not use.get('name', '').endswith('search_influencers'): continue
        i = use.get('input', {})
        for t in bl:
            for o in iter_json(t):
                if isinstance(o, dict) and 'results' in o: res[(i.get('niche'), i.get('location'))] = o
    return res

# ---------- formatting ----------
def fnum(n):
    if n >= 1e6: s = f'{n / 1e6:.1f}M'
    elif n >= 1e5: s = f'{round(n / 1e3)}K'
    elif n >= 1e3: s = f'{n / 1e3:.1f}K'
    else: s = str(n)
    return s.replace('.0M', 'M').replace('.0K', 'K')
def fer(x): return f'{x:.1f}%'
def month(d): return d.strftime('%B %Y')
def page_url(slug): return f'{SITE}/influencers/{slug}'

# ---------- plan ----------
def cmd_plan():
    items = []
    for _, o in sorted(webflow('sync:list').items()): items += o['result']['items']
    if not items: sys.exit('No sync:list results found in this session. Run the list call first.')
    today = datetime.date.today()
    pages, exclude, photos = [], set(), {}
    for it in items:
        f = it['fieldData']
        exclude |= {h.strip().lstrip('@').lower() for h in (f.get('exclude-handles') or '').split(',') if h.strip()}
        for url, hs in re.findall(r'src="(https://cdn\.prod\.website-files\.com/[^"]+?_creator-([a-z0-9-]+)\.jpg)"', f.get('creators-table') or ''):
            photos[hs] = url
        pages.append({'id': it['id'], 'draft': it['isDraft'], 'f': f})
    new = [p for p in pages if p['draft'] and not p['f'].get('creators-table')][:MAX_NEW]
    def age(p):
        d = (p['f'].get('data-updated') or '')[:10]
        return (today - datetime.date.fromisoformat(d)).days if d else 999
    old = sorted([p for p in pages if not p['draft'] and age(p) >= REFRESH_DAYS], key=age, reverse=True)[:MAX_REFRESH]
    work = new + old
    checks = set()
    for p in work:
        f = p['f']; cs, st, n = slugify(f['city']), f['state'].lower(), f['niche']
        checks |= {f'influencers-in-{cs}', f'find-{n}-influencers'}
        for c, _, s in NEARBY.get(f'{cs}-{st}', []): checks |= {f'find-{n}-influencers-in-{c}', f'hire-{n}-influencers-in-{c}-{s}', f'hire-{n}-influencers-in-{c}'}
        for m in NICHES: checks |= {f'find-{m}-influencers-in-{cs}', f'hire-{m}-influencers-in-{cs}-{st}', f'hire-{m}-influencers-in-{cs}'}
    checks = sorted(checks)
    save('plan.json', {'work': [p['id'] for p in work], 'pages': pages, 'exclude': sorted(exclude), 'photos': photos,
                       'checks': checks, 'new': [p['id'] for p in new]})
    print(f'{len(new)} new + {len(old)} refresh pages ({len(pages)} items, {len(exclude)} excluded handles).')
    print('\nSTEP A - search_influencers calls (one per line):')
    for p in work: print(json.dumps({'niche': p['f']['niche'], 'location': f"{p['f']['city']}, {p['f']['state']}", 'min_followers': 5000, 'limit': 25}))
    print('\nSTEP B - old-page existence checks: list_collection_items on 69dae1304d0242f517edcc12, one action per line:')
    for i in range(0, len(checks), 100):
        print(json.dumps({'label': f'sync:old:{i // 100}', 'list_collection_items': {'collection_id': '69dae1304d0242f517edcc12',
              'request': {'limit': 100, 'filter': {'slug': {'in': checks[i:i + 100]}}}}}))

# ---------- creators + photos ----------
def candidates(res, exclude):
    rows, seen = [], set()
    for r in res.get('results') or []:
        p, plat = r.get('profile') or {}, (r.get('platform') or '').lower()
        u = (p.get('username') or '').strip().lstrip('@')
        f, er = p.get('followers'), p.get('engagement_percent')
        if plat not in PLAT or not u or not p.get('picture') or not f or er is None or er <= 0 or f < 5000: continue
        if u.lower() in exclude or u.lower() in seen: continue
        seen.add(u.lower())
        rows.append({'u': u, 'hs': slugify(u), 'name': clean_name(p.get('full_name'), u), 'pic': p['picture'],
                     'f': int(f), 'er': float(er), 'plat': plat})
    return sorted(rows, key=lambda r: -r['er'])

def pil():
    # some containers ship a broken Pillow; fall back to a private install
    try:
        from PIL import Image; return Image
    except Exception:
        for k in [k for k in sys.modules if k == 'PIL' or k.startswith('PIL.')]: del sys.modules[k]
        lib = os.path.expanduser('~/pylib')
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-q', '--target', lib, 'pillow'], capture_output=True)
        sys.path.insert(0, lib)
        from PIL import Image; return Image

def fetch_photo(r):
    Image = pil()
    path = f'{W}/photos/creator-{r["hs"]}.jpg'
    if os.path.exists(path): return path
    os.makedirs(f'{W}/photos', exist_ok=True)
    try:
        data = urllib.request.urlopen(r['pic'], timeout=20).read()
        im = Image.open(io.BytesIO(data)).convert('RGB')
        s = min(im.size); l, t = (im.width - s) // 2, (im.height - s) // 2
        im.crop((l, t, l + s, t + s)).resize((72, 72), Image.LANCZOS).save(path, 'JPEG', quality=72, optimize=True)
        return path
    except Exception as e:
        print(f'  photo failed for @{r["u"]}: {e}'); return None

def cmd_photos():
    plan, J = load('plan.json'), jem()
    exclude, photos = set(plan['exclude']), plan['photos']
    old = set()
    for _, o in webflow('sync:old').items(): old |= {it['fieldData']['slug'] for it in o['result']['items'] if not it['isDraft']}
    picked, need, missing = {}, {}, []
    for p in plan['pages']:
        if p['id'] not in plan['work']: continue
        f = p['f']; key = (f['niche'], f"{f['city']}, {f['state']}")
        if key not in J: missing.append(f['name']); continue
        rows = []
        for r in candidates(J[key], exclude):
            if len(rows) == SHOW: break
            if r['hs'] in photos or fetch_photo(r): rows.append(r)
            if r['hs'] not in photos and r['hs'] not in need and os.path.exists(f'{W}/photos/creator-{r["hs"]}.jpg'):
                need[r['hs']] = hashlib.md5(open(f'{W}/photos/creator-{r["hs"]}.jpg', 'rb').read()).hexdigest()
        picked[p['id']] = {'rows': rows, 'total': int(J[key].get('total_estimate') or 0)}
    save('picked.json', {'picked': picked, 'old': sorted(old), 'need': need})
    if missing: print('No Jem results yet for:', '; '.join(missing))
    acts = [{'label': f'asset:{hs}', 'create_asset': {'site_id': SITE_ID, 'file_name': f'creator-{hs}.jpg', 'file_hash': h}} for hs, h in sorted(need.items())]
    print(f'{len(picked)} pages have creators; {len(need)} new photos to upload.')
    for i in range(0, len(acts), 40):
        fn = f'{W}/assets_{i // 40}.json'; json.dump(acts[i:i + 40], open(fn, 'w'), separators=(',', ':'))
        print('create_asset batch (send this file as data_assets_tool actions):', fn)

S3 = [('acl', 'acl'), ('bucket', 'bucket'), ('X-Amz-Algorithm', 'xAmzAlgorithm'), ('X-Amz-Credential', 'xAmzCredential'),
      ('X-Amz-Date', 'xAmzDate'), ('key', 'key'), ('Policy', 'policy'), ('X-Amz-Signature', 'xAmzSignature'),
      ('success_action_status', 'successActionStatus'), ('Content-Type', 'contentType'), ('Cache-Control', 'cacheControl')]

def cmd_upload():
    pk, plan = load('picked.json'), load('plan.json')
    done = plan['photos']; ok = bad = 0
    for label, o in webflow('asset:').items():
        hs = label.split(':', 1)[1]
        if hs not in pk['need'] or hs in done: continue
        r = o.get('result') or {}; d = r.get('uploadDetails') or {}
        if not d: print('  no upload details for', hs, str(o)[:200]); bad += 1; continue
        args = ['curl', '-sS', '-o', '/dev/null', '-w', '%{http_code}', r.get('uploadUrl') or 'https://webflow-prod-assets.s3.amazonaws.com/']
        for form, k in S3:
            if k in d: args += ['-F', f'{form}={d[k]}']
        args += ['-F', f'file=@{W}/photos/creator-{hs}.jpg;type=image/jpeg']
        code = subprocess.run(args, capture_output=True, text=True).stdout.strip()
        if code in ('201', '200', '204'):
            done[hs] = r.get('hostedUrl') or CDN + d['key']; ok += 1
        else: print('  upload failed', hs, code); bad += 1
    save('plan.json', plan)
    print(f'uploaded {ok}, failed {bad}; photos known: {len(done)}')

# ---------- render ----------
def render(p, data, plan, old, approved_new):
    f = p['f']; city, st, niche, Niche = f['city'], f['state'], f['niche'], f['niche-label']
    cs, slug, url = slugify(city), f['slug'], page_url(f['slug'])
    rows = [r for r in data['rows'] if r['hs'] in plan['photos']]
    N = len(rows); total = max(data['total'], N)
    ers = [r['er'] for r in rows]; fl = [r['f'] for r in rows]
    med = statistics.median(ers); lo, hi = min(fl), max(fl)
    plats = {}
    for r in rows: plats[r['plat']] = plats.get(r['plat'], 0) + 1
    top = max(plats, key=plats.get); share = round(100 * plats[top] / N)
    small = [r['er'] for r in rows if r['f'] < 50000]; big = [r['er'] for r in rows if r['f'] >= 100000]
    # table
    trs = ''.join(
        f'<div class="jp-row"><div class="jp-rank">{i}</div><div class="jp-who"><img class="jp-photo" src="{plan["photos"][r["hs"]]}" '
        f'alt="{esc(r["name"])}" width="36" height="36" loading="lazy"><div class="jp-who-text"><div class="jp-name">{esc(r["name"])}</div>'
        f'<a class="jp-handle-1" href="{PLAT[r["plat"]][1].format(r["u"])}" rel="nofollow noopener">@{esc(r["u"])}</a></div></div>'
        f'<div class="jp-plat">{PLAT[r["plat"]][0]}</div><div class="jp-num">{fnum(r["f"])}</div><div class="jp-num">{fer(r["er"])}</div>'
        f'<a class="jp-unlock" href="{SIGNUP}">Unlock</a></div>' for i, r in enumerate(rows, 1))
    more = total - N
    more_html = (f'<span class="jp-more-count">+{more:,} more {esc(city)} {niche} creators</span><span class="jp-more-cta">Unlock the full list, free for 7 days →</span>'
                 if more > 0 else '<span class="jp-more-count">Contact info for every creator above</span><span class="jp-more-cta">See it free for 7 days →</span>')
    table = ('<div class="jp-table"><div class="jp-row jp-row-head"><div class="jp-th">#</div><div class="jp-th">Creator</div><div class="jp-th">Platform</div>'
             '<div class="jp-th jp-th-right">Followers</div><div class="jp-th jp-th-right">Engagement</div><div class="jp-th jp-th-right">Contact</div></div>'
             f'<div class="jp-rows">{trs}<a class="jp-more" href="{SIGNUP}">{more_html}</a></div></div>')
    fp = hashlib.md5(json.dumps([total, [(r['u'], r['f'], round(r['er'], 2), r['plat']) for r in rows]]).encode()).hexdigest()
    prev = f.get('data-fingerprint')
    pulled = (datetime.date.fromisoformat(f['data-updated'][:10]) if prev == fp and f.get('data-updated') else datetime.date.today())
    M, Mon = month(pulled), pulled.strftime('%b %Y')
    # links
    def link_for(n, c, s):
        sl = f'{n}-influencers-in-{c}-{s}'
        if sl in approved_new: return f'/influencers/{sl}'
        for o in (f'find-{n}-influencers-in-{c}', f'hire-{n}-influencers-in-{c}-{s}', f'hire-{n}-influencers-in-{c}'):
            if o in old: return f'/find-influencers/{o}'
    near = [(link_for(niche, c, s), f'{Niche} influencers in {d}') for c, d, s in NEARBY.get(f'{cs}-{st.lower()}', [])]
    near = [x for x in near if x[0]][:3]
    other = [(link_for(m, cs, st.lower()), f'{m.capitalize()} influencers in {city}') for m in NICHES if m != niche]
    other = [x for x in other if x[0]][:4]
    browse = []
    hub = f'influencers-in-{cs}'
    if hub in old: browse.append((f'/find-influencers/{hub}', f'All {city} influencers'))
    if f'find-{niche}-influencers' in old: browse.append((f'/find-influencers/find-{niche}-influencers', f'All {niche} influencers'))
    browse.append(('/engagement-rate-calculator', 'Engagement rate calculator'))
    col = lambda lab, ls: (f'<div class="jp-related-col"><div class="jp-label">{esc(lab)}</div>' + ''.join(f'<a href="{h}" class="jp-link">{esc(t)}</a>' for h, t in ls) + '</div>') if ls else ''
    related = f'<div class="jp-related">{col(f"{Niche} near {city}", near)}{col(f"More in {city}", other)}{col("Browse all", browse)}</div>'
    hub_url = f'/find-influencers/{hub}' if hub in old else None
    crumb_city = f'<a href="{hub_url}" class="jp-crumb-link">{esc(city)}</a>' if hub_url else f'<span class="jp-crumb-link">{esc(city)}</span>'
    crumbs = f'<div class="jp-crumbs"><a href="/" class="jp-crumb-link">Home</a><span class="jp-crumb-sep">/</span>{crumb_city}<span class="jp-crumb-sep">/</span><span class="jp-crumb-current">{esc(Niche)}</span></div>'
    glance = lambda num, lab, d='': f'<div class="jp-glance-item{d}"><div class="jp-glance-num">{num}</div><div class="jp-glance-label">{esc(lab)}</div></div>'
    stats = (f'<p class="jp-micro">7-day free trial, then $69/month. Search creators in every city and niche, not just {esc(city)}.</p><div class="jp-glance">'
             + glance(f'{total:,}', f'{city} {niche} creators on Jem Social') + glance(fer(med), 'median engagement on this page', ' jp-glance-divider')
             + glance(f'{fnum(lo)}–{fnum(hi)}', 'follower range on this page', ' jp-glance-divider')
             + glance(f'{share}%', f'on {PLAT[top][0]}', ' jp-glance-divider') + '</div>')
    # insights: only statements the rows support
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
    insights = '<ul role="list" class="jp-insight-list">' + ''.join(f'<li class="jp-insight">{esc(t)}</li>' for t in ins) + '</ul>'
    calc = '<a href="/influencer-rate-calculator" class="jp-inline-link">Influencer Rate Calculator</a>'
    smaller_higher = len(small) >= 2 and len(big) >= 2 and statistics.median(small) > statistics.median(big)
    faqs = [
        (f'How many {niche} influencers are in {city}?', f'Jem Social lists {total:,} {niche} creators in the {city} area with at least 5,000 followers as of {M}. This page shows {N} of them, sorted by engagement rate.', None),
        (f'What engagement rate do {city} {niche} creators get?', f'The median engagement rate among the {N} creators on this page is {fer(med)}. ' +
         ('Smaller accounts often run higher than large ones, so compare creators in the same follower range.' if smaller_higher else 'Engagement varies with audience size, so compare creators in the same follower range.'), None),
        (f'How much do {city} {niche} influencers charge?', "Rates depend on followers, platform and deliverables. The Influencer Rate Calculator gives a starting point, and each creator's rate estimate is in Jem Social.",
         f"Rates depend on followers, platform and deliverables. The {calc} gives a starting point, and each creator's rate estimate is in Jem Social."),
        ('How do I contact these creators?', "Start a 7-day free trial to see each creator's email and audience data, then message them from Jem Social.", None),
        ('How much does Jem Social cost?', 'Jem Social costs $69 per month after a 7-day free trial. One plan covers creator search in every city and niche, outreach and campaign management.', None)]
    faq = '<div class="jp-faq">' + ''.join(f'<div class="jp-qa"><h3 class="jp-q">{esc(q)}</h3><p class="jp-a">{h or esc(a)}</p></div>' for q, a, h in faqs) + '</div>'
    h1 = f'{N} {Niche} Influencers in {city}, {st} ({M})'
    title = f'{N} {Niche} Influencers in {city}, {st} ({Mon}) | Jem Social'
    if len(title) > 60: title = title.replace(' | Jem Social', '')
    desc = f"Browse {N} of Jem Social's {total:,} {city} {niche} influencers with follower counts and engagement rates."
    meta = desc + ' See contact info with a 7-day free trial.'
    if len(meta) > 160: meta = desc
    person = lambda r: {'@type': 'Person', 'name': r['name'], 'alternateName': '@' + r['u'], 'url': PLAT[r['plat']][1].format(r['u']),
                        'interactionStatistic': {'@type': 'InteractionCounter', 'interactionType': 'https://schema.org/FollowAction', 'userInteractionCount': r['f']}}
    crumbs_ld = [{'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': SITE + '/'}]
    if hub_url: crumbs_ld.append({'@type': 'ListItem', 'position': 2, 'name': city, 'item': SITE + hub_url})
    crumbs_ld.append({'@type': 'ListItem', 'position': len(crumbs_ld) + 1, 'name': Niche, 'item': url})
    graph = {'@context': 'https://schema.org', '@graph': [
        {'@type': 'WebPage', '@id': url + '#webpage', 'url': url, 'name': h1, 'description': desc, 'dateModified': pulled.isoformat(), 'inLanguage': 'en',
         'isPartOf': {'@type': 'WebSite', 'name': 'Jem Social', 'url': SITE + '/'}, 'breadcrumb': {'@id': url + '#breadcrumb'}, 'mainEntity': {'@id': url + '#list'}},
        {'@type': 'BreadcrumbList', '@id': url + '#breadcrumb', 'itemListElement': crumbs_ld},
        {'@type': 'ItemList', '@id': url + '#list', 'name': f'{Niche} influencers in {city}, {st}', 'numberOfItems': N,
         'itemListOrder': 'https://schema.org/ItemListOrderDescending', 'itemListElement': [{'@type': 'ListItem', 'position': i, 'item': person(r)} for i, r in enumerate(rows, 1)]},
        {'@type': 'FAQPage', '@id': url + '#faq', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a, _ in faqs]}]}
    ld = json.dumps(graph, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
    rt = lambda x: f'<div data-rt-embed-type="true">{x}</div>'
    approved = bool(f.get('approved'))
    return N, {
        'h1': h1, 'intro': f'Jem Social has {total:,} {niche} creators in the {city} area with at least 5,000 followers. Here are {N} of them, sorted by engagement rate.',
        'hero-button-text': f'See all {total:,} creators, free for 7 days', 'creator-total': f'{total:,}',
        'stat-median-engagement': fer(med), 'stat-follower-range': f'{fnum(lo)}–{fnum(hi)}', 'stat-top-platform-share': f'{share}%',
        'stat-top-platform-label': f'on {PLAT[top][0]}', 'list-heading': f'{N} {city} {niche} creators',
        'method-note': f'How this list was made: Jem Social creators tagged {niche} and based in the {city} area, with at least 5,000 followers, sorted by engagement rate. Data pulled from Jem Social on {pulled.strftime("%B")} {pulled.day}, {pulled.year}.',
        'band-heading': f'Reach {city} {niche} creators directly', 'band-text': f'See all {total:,}, then run the whole campaign in one place.',
        'steps-heading': f'How to run a {niche} campaign with {city} creators', 'seo-title': title, 'meta-description': meta,
        'robots': 'index, follow' if approved and N >= MIN_INDEX else 'noindex, follow', 'updated-label': f'Updated {M}',
        'data-updated': pulled.isoformat() + 'T00:00:00.000Z', 'data-fingerprint': fp,
        'breadcrumb': rt(crumbs), 'hero-stats': rt(stats), 'creators-table': rt(table), 'insights': rt(insights),
        'faq': rt(faq), 'related-links': rt(related), 'schema-markup': rt(f'<script type="application/ld+json">{ld}</script>')}

def cmd_build():
    plan, pk = load('plan.json'), load('picked.json')
    old = set(pk['old']); out = f'{W}/out'; os.makedirs(out, exist_ok=True)
    for x in glob.glob(f'{out}/*'): os.remove(x)
    approved_new = {p['f']['slug'] for p in plan['pages'] if p['f'].get('approved') and not p['draft']}
    ups, report = [], {'built': [], 'refreshed': [], 'unchanged': [], 'too_few': [], 'approved_changed': []}
    for p in plan['pages']:
        d = pk['picked'].get(p['id'])
        if not d: continue
        n_ok = len([r for r in d['rows'] if r['hs'] in plan['photos']])
        if n_ok < MIN_BUILD: report['too_few'].append(f"{p['f']['name']} ({n_ok})"); continue
        N, fd = render(p, d, plan, old, approved_new)
        ch = {k: v for k, v in fd.items() if p['f'].get(k) != v}
        if 'data-updated' in ch: ch['data-updated'] = fd['data-updated']
        if not ch: report['unchanged'].append(p['f']['name']); continue
        item = {'id': p['id'], 'fieldData': ch}
        if p['draft']: item['isDraft'] = False; report['built'].append(p['f']['name'])
        else: report['refreshed'].append(p['f']['name'])
        if p['f'].get('approved'): report['approved_changed'].append(p['id'])
        ups.append(item)
    # one part of one page per file, under 20,000 characters, so `cat` always shows it whole
    files, LIM = [], 20000
    size = lambda fd, iid: len(json.dumps([{'id': iid, 'fieldData': fd}], ensure_ascii=False, separators=(',', ':')))
    for item in ups:
        fd, parts, cur = item['fieldData'], [], {}
        for k in sorted(fd, key=lambda k: -len(json.dumps(fd[k], ensure_ascii=False))):
            if cur and size(dict(cur, **{k: fd[k]}), item['id']) > LIM: parts.append(cur); cur = {}
            cur[k] = fd[k]
        parts.append(cur)
        for j, part in enumerate(parts):
            it = {'id': item['id'], 'fieldData': part}
            if j == len(parts) - 1 and 'isDraft' in item: it['isDraft'] = item['isDraft']
            files.append([it])
    for i, f in enumerate(files):
        json.dump(f, open(f'{out}/u{i:03d}.json', 'w'), ensure_ascii=False, separators=(',', ':'))
    save('report.json', report)
    print(json.dumps({k: len(v) for k, v in report.items()}), '\nupdate batches:', ' '.join(sorted(glob.glob(f'{out}/*.json'))))
    if report['approved_changed']: print('approved items to publish live:', json.dumps(report['approved_changed']))

def cmd_report():
    r = load('report.json'); s = lambda k: ', '.join(r[k][:12]) or 'none'
    print(f"Jem city pages sync {datetime.date.today():%b %d}: built {len(r['built'])} ({s('built')}); refreshed {len(r['refreshed'])}; "
          f"unchanged {len(r['unchanged'])}; skipped for too few creators: {s('too_few')}. "
          f"{len(r['approved_changed'])} approved pages pushed live. New pages are on staging (jemsocial.webflow.io/influencers/...) "
          "and stay noindex until you switch on Approved in Webflow CMS.")

if __name__ == '__main__':
    {'plan': cmd_plan, 'photos': cmd_photos, 'upload': cmd_upload, 'build': cmd_build, 'report': cmd_report}[sys.argv[1]]()
