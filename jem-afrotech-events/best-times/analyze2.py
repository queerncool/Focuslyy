# Controls for account-reach drift: each post's views are divided by the median views of the
# account's other posts within +/-21 days, so a time slot isn't credited for a good month.
import statistics as st
from datetime import timedelta
from analyze import load, block, DAYS
def rel(rows):
    out = []
    for r in rows:
        nb = [x['v'] for x in rows if x is not r and abs(x['t'] - r['t']) <= timedelta(days=21)]
        if len(nb) < 3: continue
        m = st.median(nb) or 1
        out.append(dict(r, rv=r['v'] / m))
    return out
def show(name, rows):
    rows = rel(rows)
    print(f'\n=== {name} (views vs. same-period median, n={len(rows)}) ===')
    for key, fn, order in (('block', lambda r: block(r['t'].hour), None),
                           ('hour', lambda r: r['t'].hour, None),
                           ('weekday', lambda r: DAYS[r['t'].weekday()], DAYS)):
        g = {}
        for r in rows: g.setdefault(fn(r), []).append(r)
        print(f'-- by {key}')
        for k in (order or sorted(g)):
            if k not in g or len(g[k]) < 3: continue
            xs = g[k]
            print(f'  {str(k):16} n={len(xs):3}  median rel {st.median(x["rv"] for x in xs):4.2f}x  share above period median {sum(x["rv"]>1 for x in xs)/len(xs):4.0%}  comments+shares {sum(x["c"]+x["s"] for x in xs)}')
ig = load('ig.tsv', True); th = load('threads.tsv', False)
show('INSTAGRAM', ig); show('THREADS', th)
