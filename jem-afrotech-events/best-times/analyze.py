import csv, sys, statistics as st
from datetime import datetime
from zoneinfo import ZoneInfo
CT = ZoneInfo('America/Chicago')
DAYS = ['mon','tue','wed','thu','fri','sat','sun']
def block(h):
    if 5 <= h < 9: return '05-09 early am'
    if 9 <= h < 12: return '09-12 late am'
    if 12 <= h < 15: return '12-15 midday'
    if 15 <= h < 18: return '15-18 afternoon'
    if 18 <= h < 21: return '18-21 evening'
    return '21-05 night'
def load(path, ig):
    rows = []
    for r in csv.reader(open(path), delimiter='\t'):
        t = datetime.fromisoformat(r[0].replace('Z', '+00:00')).astimezone(CT)
        v, l, c, s = (int(float(x)) for x in r[1:5])
        sv = int(float(r[5])) if ig else 0
        # weighted engagement: comments/shares/saves matter most for this campaign
        eng = l + 3*c + 4*s + 3*sv
        rows.append(dict(t=t, v=v, eng=eng, c=c, s=s))
    return rows
def report(name, rows, since=None):
    if since: rows = [r for r in rows if r['t'] >= since]
    print(f'\n=== {name}: n={len(rows)}  window {min(r["t"] for r in rows):%b %d} to {max(r["t"] for r in rows):%b %d} ===')
    med_all = st.median(r['v'] for r in rows)
    print(f'overall median views {med_all:.0f}')
    for key, fn in (('hour block (CT)', lambda r: block(r['t'].hour)), ('weekday', lambda r: DAYS[r['t'].weekday()])):
        g = {}
        for r in rows: g.setdefault(fn(r), []).append(r)
        print(f'-- by {key}')
        order = sorted(g) if key.startswith('hour') else DAYS
        for k in order:
            if k not in g: continue
            xs = g[k]
            print(f'  {k:16} n={len(xs):3}  median views {st.median(x["v"] for x in xs):6.0f}  mean views {st.mean(x["v"] for x in xs):6.0f}  mean wtd-eng {st.mean(x["eng"] for x in xs):5.1f}  views/med {st.median(x["v"] for x in xs)/med_all:4.2f}x')
if __name__ == '__main__':
    ig = load('ig.tsv', True); th = load('threads.tsv', False)
    report('INSTAGRAM @jemsocialapp (all 6 mo)', ig)
    report('INSTAGRAM @jemsocialapp (since Aug 1)', ig, datetime(2026,8,1,tzinfo=CT))
    report('THREADS @jemsocialapp (all 6 mo)', th)
