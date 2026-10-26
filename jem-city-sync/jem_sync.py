#!/usr/bin/env python3
"""Daily build for Jem Social city pages (Webflow collection "City Influencer Pages").
Webflow is read and written directly through its API: the environment's network secret adds the token
(a WEBFLOW_TOKEN variable is used instead when present). Jem creator data comes from search_influencers
calls made in this Claude session; the script reads their results from the session transcript.
  plan               picks today's pages from the priority list plus stale refreshes, prints the Jem searches
  run                reads the Jem results, uploads photos, writes and publishes pages, syncs robots for approved pages
  approve SLUG...    switches pages to approved, indexes those with 10+ creators, publishes them
  report             one-paragraph summary for Telegram
"""
import json, os, re, sys, glob, html, hashlib, statistics, subprocess, datetime, io, time, math, urllib.request, urllib.error, unicodedata
W = os.path.expanduser('~/jem-sync'); os.makedirs(W, exist_ok=True)
SITE_ID, COLL, OLD_COLL = '67b0d09acc5bda1c5c04566f', '6adc28d2f2806b611dd3a207', '69dae1304d0242f517edcc12'
SITE, CDN, API = 'https://www.jem.social', 'https://cdn.prod.website-files.com/', 'https://api.webflow.com/v2'
SIGNUP = 'https://app.jem.social/signup'
MAX_NEW, MAX_REFRESH = int(os.environ.get('MAX_NEW', 10)), int(os.environ.get('MAX_REFRESH', 4))
REFRESH_DAYS, SKIP_DAYS = int(os.environ.get('REFRESH_DAYS', 27)), 60
SHOW, MIN_BUILD, MIN_INDEX = 20, 5, 10
MAX_ER = 20.0     # engagement above this is treated as a data error and left out
FPV = 'v3:'       # bump when page rules change; older pages get re-rendered as refreshes
PLAT = {'instagram': ('Instagram', 'https://www.instagram.com/{}/'), 'tiktok': ('TikTok', 'https://www.tiktok.com/@{}'),
        'youtube': ('YouTube', 'https://www.youtube.com/@{}')}
# Build order, from the SEO plan: est. visits = "{city} influencers" x 20% + "{city} foodie" x 4% (US searches, Oct 2026).
# (city, state, lat, lon)
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
 ('St. Petersburg', 'FL', 27.77, -82.64), ('Honolulu', 'HI', 21.31, -157.86), ('Birmingham', 'AL', 33.52, -86.80),
 ('Washington', 'DC', 38.91, -77.04), ('Columbus', 'OH', 39.96, -83.00), ('Myrtle Beach', 'SC', 33.69, -78.89),
 ('Milwaukee', 'WI', 43.04, -87.91), ('Jacksonville', 'FL', 30.33, -81.66), ('Palm Springs', 'CA', 33.83, -116.55),
 ('Oakland', 'CA', 37.80, -122.27), ('Boulder', 'CO', 40.01, -105.27), ('Ann Arbor', 'MI', 42.28, -83.74),
 ('Sarasota', 'FL', 27.34, -82.53), ('Raleigh', 'NC', 35.78, -78.64), ('Bakersfield', 'CA', 35.37, -119.02)]
COORD = {(c, s): (la, lo) for c, s, la, lo in PRIORITY}
PASSES = [(None, 'food'), ('fitness', 'beauty', 'fashion')]   # hub + food for every city first, then niche pages
NICHES = ['food', 'fitness', 'beauty', 'fashion']
# words in a creator's profile name that tie them to a niche; a niche page leaves out names that only point elsewhere
NICHE_WORDS = {
 'food': r'food|eat|chef|kitchen|cook|bak|recipe|dining|dine|drink|dessert|bbq|restaurant|tast|bite|brunch|coffee|cocktail|wine|sweet|snack|menu|dietitian|nutrition|grill',
 'fitness': r'fit|gym|coach|trainer|workout|yoga|pilates|weight ?loss|athlet|run|lift|muscle',
 'beauty': r'beauty|makeup|mua|skin|nail|hair|lash|brow|esthetic|cosmetic|glam',
 'fashion': r'fashion|style|stylist|outfit|ootd|wear|wardrobe|boutique|lifestyle',
 'other': r'money|financ|realtor|real estate|mortgage|insurance|attorney|lawyer'}

# National pages built from one Jem search; they share the city template and get built before the next cities.
# Copy placeholders: {N} creators shown, {total} Jem total, {M} "October 2026", {Mon} "Oct 2026".
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
            ('For UGC creators', [('/blog/how-to-become-a-ugc-creator', 'How to become a UGC creator'), ('/opportunities', 'Open brand opportunities'),
                                  ('/blog/ugc-jobs', 'UGC jobs'), ('/earn-money-as-a-ugc-creator', 'Earn money as a UGC creator')])],
  'old': ['find-ugc-creators', 'ugc-creator', 'ugc-content-creator']},
}

def slugify(s): return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')
def esc(s): return html.escape(str(s), quote=True)
def slug_for(city, st, niche): return f'{slugify(city)}-{st.lower()}' if not niche else f'{niche}-influencers-in-{slugify(city)}-{st.lower()}'
def page_url(slug): return f'{SITE}/influencers/{slug}'
def signup(slug): return f'{SIGNUP}?utm_source=seo&amp;utm_medium=city-page&amp;utm_campaign={slug}'
ROLE = {'creator', 'coach', 'trainer', 'influencer', 'blogger', 'vlogger', 'model', 'official', 'fitness', 'lifestyle', 'beauty',
        'fashion', 'food', 'foodie', 'travel', 'pro', 'aging', 'community', 'ugc', 'content', 'personal', 'mua', 'stylist', 'chef',
        'photographer', 'photography', 'photo', 'llc'}
GENERIC = ROLE | {'collaboration', 'collaborations', 'collab', 'collabs', 'brands', 'brand', 'with', 'and', 'for', '&', 'dm', 'business', 'inquiries'}
def clean_name(raw, handle):
    # Jem names often carry bio text: "BRITTFIT MIAMI 🌴 Fitness community", "Alex P | Fitness Coach"
    s = unicodedata.normalize('NFKC', raw or '')    # fancy-font letters (e.g. Fraktur) -> plain
    s = re.sub(r'^[^\w]+', '', s)                   # leading emoji: "💋Danielle💋"
    s = re.split(r'\s[|•·–—/-]\s|\s*[|•·]\s*|,|\s\(|\[', s)[0]
    s = re.split(r'[^\w\s.\'’“”"&+-]', s)[0]         # stop at the first emoji or symbol
    words = s.split()
    while len(words) > 1 and words[-1].lower().strip('.') in ROLE: words.pop()
    s = ' '.join(words).strip(" .-'")
    if s.isupper() and len(s) > 3: s = ' '.join(w.capitalize() if len(w) > 2 else w for w in s.split())
    elif s.islower(): s = s.title()
    if not s or all(w.lower().strip('.') in GENERIC for w in s.split()): return handle   # "Ugc", "Collaboration with brands"
    return s
def save(name, obj): json.dump(obj, open(f'{W}/{name}', 'w'), ensure_ascii=False)
def load(name): return json.load(open(f'{W}/{name}'))
def km(a, b):
    (la1, lo1), (la2, lo2) = a, b
    p = math.pi / 180
    h = math.sin((la2 - la1) * p / 2) ** 2 + math.cos(la1 * p) * math.cos(la2 * p) * math.sin((lo2 - lo1) * p / 2) ** 2
    return 12742 * math.asin(math.sqrt(h))

# ---------- Webflow API ----------
_last = [0.0]
def wf(method, path, body=None, tries=6):
    for k in range(tries):
        gap = time.time() - _last[0]
        if gap < 0.7: time.sleep(0.7 - gap)      # stay under the CMS rate limit
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
    # live slugs of the older /find-influencers/ pages, cached for a week
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

# ---------- transcript reading (Jem results) ----------
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
                        if isinstance(r, dict) and 'results' in r: res[(i.get('niche') or None, i.get('location'))] = r
    return res

# ---------- formatting ----------
def fnum(n):
    if n >= 1e6: s = f'{n / 1e6:.1f}M'
    elif n >= 1e5: s = f'{round(n / 1e3)}K'
    elif n >= 1e3: s = f'{n / 1e3:.1f}K'
    else: s = str(n)
    return s.replace('.0M', 'M').replace('.0K', 'K')
def fer(x): return f'{x:.1f}%'

# ---------- plan ----------
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
    save('plan.json', {'work': work, 'date': today.isoformat()})
    print(f'{sum(w["new"] for w in work)} new + {sum(not w["new"] for w in work)} refresh pages ({len(items)} items in the collection).')
    print('\nsearch_influencers calls, one per line (all with min_followers 5000, limit 25):')
    for w in work: print(json.dumps(search_args(w)))

def search_args(w):
    t = TOPICS.get(w['slug'])
    q = dict(t['search']) if t else {'location': f"{w['city']}, {w['st']}"}
    if w['niche'] and not t: q = {'niche': w['niche'], **q}
    return {**q, 'min_followers': 5000, 'limit': 25}

# ---------- creators + photos ----------
def off_niche(name, niche):
    if niche not in NICHE_WORDS: return False
    t, rx = name.lower(), lambda k: re.search(r'\b(?:' + NICHE_WORDS[k] + ')', t)
    if rx(niche): return False
    return any(rx(k) for k in NICHE_WORDS if k != niche)

def candidates(res, exclude, niche):
    rows, seen = [], set()
    for r in res.get('results') or []:
        p, plat = r.get('profile') or {}, (r.get('platform') or '').lower()
        u = (p.get('username') or '').strip().lstrip('@')
        f, er = p.get('followers'), p.get('engagement_percent')
        if plat not in PLAT or not u or not p.get('picture') or not f or er is None or er <= 0 or er > MAX_ER or f < 5000: continue
        if u.lower() in exclude or u.lower() in seen or off_niche(p.get('full_name') or '', niche): continue
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

S3 = [('acl', 'acl'), ('bucket', 'bucket'), ('X-Amz-Algorithm', 'xAmzAlgorithm'), ('X-Amz-Credential', 'xAmzCredential'),
      ('X-Amz-Date', 'xAmzDate'), ('key', 'key'), ('Policy', 'policy'), ('X-Amz-Signature', 'xAmzSignature'),
      ('success_action_status', 'successActionStatus'), ('Content-Type', 'contentType'), ('Cache-Control', 'cacheControl')]

def upload_photo(r):
    """Square 72px JPEG of the creator photo, uploaded to Webflow assets; returns its CDN URL or None."""
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

# ---------- render ----------
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
    noun = f'{niche} creators' if niche else 'creators'            # "food creators"
    who = f'{city} {noun}'                                          # "Chicago food creators"
    t = TOPICS.get(slug)                                            # national page, e.g. /influencers/ugc-creators
    if t: noun, who, Niche = t['noun'], t['who'], t['Label']
    su = signup(slug)
    # table
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
    fp = FPV + hashlib.md5(json.dumps([total, [(r['u'], r['f'], round(r['er'], 2), r['plat']) for r in rows]]).encode()).hexdigest()
    pulled = (datetime.date.fromisoformat(f['data-updated'][:10]) if f.get('data-fingerprint') == fp and f.get('data-updated') else datetime.date.today())
    M, Mon = pulled.strftime('%B %Y'), pulled.strftime('%b %Y')
    # links: new pages that are live (or being built in this run) first, older /find-influencers/ pages as a fallback
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
        browse = [(f'/find-influencers/find-{niche}-influencers', f'All {niche} influencers')] if f'find-{niche}-influencers' in old else []
        cols = [(f'{Niche} near {city}', near[:3]), (f'More in {city}', other[:4])]
    else:
        other = [(h, f'{m.capitalize()} influencers in {city}') for m in NICHES for h in [new_or_old(m, city, st)] if h]
        browse = []
        cols = [(f'{city} by niche', other[:4]), (f'Influencers near {city}', near[:4])]
    browse.append(('/engagement-rate-calculator', 'Engagement rate calculator'))
    cols.append(('Browse all', browse))
    if t:
        hubs = [(f'/influencers/{slug_for(c, s, None)}', f'Influencers in {c}') for c, s, *_ in PRIORITY if slug_for(c, s, None) in live][:4]
        cols = t['links'] + ([('Creators by city', hubs)] if hubs else [])
    col = lambda lab, ls: (f'<div class="jp-related-col"><div class="jp-label">{esc(lab)}</div>' + ''.join(f'<a href="{h}" class="jp-link">{esc(t)}</a>' for h, t in ls) + '</div>') if ls else ''
    related = '<div class="jp-related">' + ''.join(col(a, b) for a, b in cols) + '</div>'
    crumb_city = (f'<a href="{hub_url}" class="jp-crumb-link">{esc(city)}</a>' if hub_url and niche else
                  f'<span class="jp-crumb-{"link" if niche else "current"}">{esc(city)}</span>')
    crumbs = f'<div class="jp-crumbs"><a href="/" class="jp-crumb-link">Home</a><span class="jp-crumb-sep">/</span>{crumb_city}' + \
             (f'<span class="jp-crumb-sep">/</span><span class="jp-crumb-current">{esc(Niche)}</span>' if niche else '') + '</div>'
    if t: crumbs = f'<div class="jp-crumbs"><a href="/" class="jp-crumb-link">Home</a><span class="jp-crumb-sep">/</span><span class="jp-crumb-current">{esc(t["crumb"])}</span></div>'
    glance = lambda num, lab, d='': f'<div class="jp-glance-item{d}"><div class="jp-glance-num">{num}</div><div class="jp-glance-label">{esc(lab)}</div></div>'
    micro = esc(t['micro']) if t else f'7-day free trial, then $69/month. Search creators in every city and niche, not just {esc(city)}.'
    stats = (f'<p class="jp-micro">{micro}</p><div class="jp-glance">'
             + glance(f'{total:,}', f'{who} on Jem Social') + glance(fer(med), 'median engagement on this page', ' jp-glance-divider')
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
        fm = lambda x: x.format(N=N, M=M, Mon=Mon, total=f'{total:,}')
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
    method = (f'How this list was made: Jem Social creators {scope}, with at least 5,000 followers, sorted by engagement rate. '
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
    if t: out.update({'name': t['Label'], 'niche-label': t['niche'].upper() if len(t['niche']) <= 3 else t['niche'].capitalize()})
    return out

# ---------- run ----------
def cmd_run():
    plan, J = load('plan.json'), jem()
    items = list_items(COLL); by_id = {it['id']: it for it in items}
    by_slug = {it['fieldData']['slug']: it for it in items}     # a rerun finds pages an interrupted run already created
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
        q = search_args(w); res = J.get((q.get('niche'), q['location']))
        if not res: rep['no_data'].append(w['slug']); continue
        rows = []
        for r in candidates(res, exclude, w['niche']):
            if len(rows) == SHOW: break
            if r['hs'] not in photos:
                u = upload_photo(r)
                if not u: continue
                photos[r['hs']] = u; rep['uploaded'] += 1
            rows.append(r)
        w['rows'], w['total'] = rows, int(res.get('total_estimate') or 0)
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
    # approved pages index once they show 10+ creators; everything else stays noindex
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

def cmd_approve(slugs):
    items = {it['fieldData']['slug']: it for it in list_items(COLL)}
    pub = []
    for s in slugs:
        it = items.get(s)
        if not it or it['isDraft'] or not it['fieldData'].get('creators-table'): print('not a built page:', s); continue
        f = dict(it['fieldData'], approved=True)
        wf('PATCH', f'/collections/{COLL}/items/{it["id"]}', {'fieldData': {'approved': True, 'robots': want_robots(f)}})
        pub.append(it['id']); print(f'{s}: approved, {want_robots(f)}')
        for o in [x.strip() for x in (f.get('old-urls') or '').split(',') if x.strip()]: print(f'  301  {o}  ->  /influencers/{s}')
    publish(pub)

def cmd_report():
    r = load('report.json'); s = lambda k: ', '.join(r[k][:12]) or 'none'
    print(f"Jem city pages {datetime.date.today():%b %d}: built {len(r['built'])} ({s('built')}); refreshed {len(r['refreshed'])}; "
          f"unchanged {len(r['unchanged'])}; too few creators: {s('too_few')}; no Jem data: {s('no_data')}. "
          f"{len(r['robots'])} robots changes. New pages are live on jem.social/influencers/... as noindex until you approve them.")

if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'approve': cmd_approve(sys.argv[2:])
    else: {'plan': cmd_plan, 'run': cmd_run, 'report': cmd_report}[cmd]()
