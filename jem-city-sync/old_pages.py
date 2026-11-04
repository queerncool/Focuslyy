"""Take old /find-influencers/ pages off the live site once their redirects exist, and check the redirects.
  python3 old_pages.py check SLUGFILE        how many of the slugs are live items (dry run)
  python3 old_pages.py unpublish SLUGFILE    mark each item draft (so a site publish can't bring it back), then remove it from the live site
  python3 old_pages.py verify SLUGFILE [N]   request N old URLs (default all) and report each one's status and redirect target
SLUGFILE: one slug per line, or 'old path,new path' CSV rows (header allowed)."""
import sys, json, importlib.util, urllib.request, urllib.error, http.client, ssl, time
spec = importlib.util.spec_from_file_location('js', __import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), 'jem_sync.py'))
js = importlib.util.module_from_spec(spec); spec.loader.exec_module(js)

def slugs(path):
    out = []
    for line in open(path):
        line = line.strip()
        if not line or line.lower().startswith('old path'): continue
        out.append(line.split(',')[0].rsplit('/', 1)[-1])
    return out

def live_items(want):
    items = [it for it in js.list_items(js.OLD_COLL) if it['fieldData']['slug'] in want]
    return items

def cmd_check(path):
    want = set(slugs(path)); items = live_items(want)
    live = [it for it in items if not it['isDraft']]
    print(f'{len(want)} slugs, {len(items)} found in the old collection, {len(live)} not draft, {len(want) - len(items)} not found')

def cmd_unpublish(path):
    want = set(slugs(path)); items = live_items(want); ids = [it['id'] for it in items]
    for i in range(0, len(ids), 100):
        b = ids[i:i + 100]
        js.wf('PATCH', f'/collections/{js.OLD_COLL}/items', {'items': [{'id': x, 'isDraft': True} for x in b]})
        try: js.wf('DELETE', f'/collections/{js.OLD_COLL}/items/live', {'items': [{'id': x} for x in b]})
        except Exception as e: print('unpublish batch error (may already be off the live site):', str(e)[:200])
        print(f'{min(i + 100, len(ids))}/{len(ids)} done')

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k): return None

def cmd_verify(path, n=None):
    ss = slugs(path); ss = ss[:int(n)] if n else ss
    op = urllib.request.build_opener(NoRedirect)
    tally = {}
    for s in ss:
        u = f'https://www.jem.social/find-influencers/{s}?nocache={int(time.time())}'
        try: r = op.open(urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'}), timeout=30); code, loc = r.status, ''
        except urllib.error.HTTPError as e: code, loc = e.code, e.headers.get('Location', '')
        tally[code] = tally.get(code, 0) + 1
        if code != 301 or n: print(code, s, '->', loc)
    print('status counts:', tally)

if __name__ == '__main__':
    {'check': cmd_check, 'unpublish': cmd_unpublish, 'verify': cmd_verify}[sys.argv[1]](*sys.argv[2:])
