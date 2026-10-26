import json, sys, difflib
res, out = sys.argv[1], sys.argv[2]
blocks = json.load(open(res))
dec = json.JSONDecoder()
for b in blocks:
    t = b.get('text', '')
    i = 0
    while True:
        j = t.find('{', i)
        if j < 0: break
        try: o, i = dec.raw_decode(t, j)
        except ValueError: i = j + 1; continue
        lab = o.get('label')
        code = None
        for r in o.get('result', []):
            for m in (r.get('data') or {}).get('matches', []):
                if m.get('key') == 'code': code = m.get('value')
        if lab is None or code is None: continue
        want = open(f'{out}/{lab}.html').read()
        if code == want: print(f'{lab:10s} OK ({len(code)} chars)')
        else:
            print(f'{lab:10s} MISMATCH got {len(code)} want {len(want)}')
            sm = difflib.SequenceMatcher(None, want, code, autojunk=False)
            for op, a1, a2, b1, b2 in sm.get_opcodes():
                if op != 'equal': print('   ', op, repr(want[max(0,a1-30):a2+30]), '->', repr(code[max(0,b1-30):b2+30]))
