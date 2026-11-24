"""Shared helpers for building buyer-page patches (nothing here writes to Webflow)."""
import json, re, html, sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import jem_sync as J

SP = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out') + '/'   # patches and previews land here (git-ignored)
JEM = 'https://www.jem.social'
MICRO_ID = '69dae160d69e6a2806322de4'          # live page that carries the shared buyer-page CSS in hero-description
END = '</style></div>'

def css_embed():
    hd = J.wf('GET', f'/collections/{J.OLD_COLL}/items/{MICRO_ID}')['fieldData']['hero-description']
    emb = hd[:hd.find(END) + len(END)]
    assert emb.startswith('<div data-rt-embed-type="true">') and '.jl-table' in emb and '.jl-cta' in emb
    return emb

def a(href, text, ext=False):
    return f'<a href="{href}"' + (' rel="nofollow noopener" target="_blank"' if ext else '') + f'>{text}</a>'

def table(head, rows, last_highlight=False):
    th = ''.join(f'<th>{h}</th>' for h in head)
    body = ''
    for ri, r in enumerate(rows):
        cls = ' class="jl-jem"' if (last_highlight and ri == len(rows) - 1) else ''
        body += f'<tr{cls}>' + ''.join(f'<td data-label="{head[i]}">{c}</td>' for i, c in enumerate(r)) + '</tr>'
    return ('<div data-rt-embed-type="true"><div class="jl-scroll"><table class="jl-table"><thead><tr>'
            + th + '</tr></thead><tbody>' + body + '</tbody></table></div></div>')

def utm(slug): return f'utm_source=seo&amp;utm_medium=landing-page&amp;utm_campaign={slug}'
def brief_url(slug): return f'{JEM}/post-a-brief?source=seo_lp_brief&amp;{utm(slug)}'
def signup_url(slug): return f'https://app.jem.social/signup?{utm(slug)}'

def cta_row(href, label, note):
    return f'<div data-rt-embed-type="true"><div class="jl-cta-row"><a class="jl-cta" href="{href}">{label}</a><span>{note}</span></div></div>'

def stats(tiles):
    inner = ''.join(f'<div><div class="jl-st-n">{n}</div><div class="jl-st-l">{l}</div></div>' for n, l in tiles)
    return f'<div data-rt-embed-type="true"><div class="jl-stats">{inner}</div></div>'

QA = [('faq-1-question-2', 'faq-1-answer-3'), ('faq-2-question-2', 'faq-2-answer-3'), ('faq-3-question-2', 'faq-3-answer-3'),
      ('faq-4-question-2', 'faq-4-answer-3'), ('faq-5-question', 'faq-5-answer-2'), ('faq-6-question', 'faq-6-answer-2'),
      ('faq-7-question', 'faq-7-answer-2')]

def finish(name, fd, faqs, guide):
    assert len(faqs) == 7
    for (qk, ak), (q, an) in zip(QA, faqs):
        fd[qk] = q; fd[ak] = an
    fd['guide-section-content'] = guide
    fd['robots'] = None
    assert len(fd['meta-title']) <= 60, len(fd['meta-title'])
    assert len(fd['meta-description']) <= 160, len(fd['meta-description'])
    for k, v in fd.items():
        if isinstance(v, str) and k != 'hero-description' and re.search(r'\b(vetted|verified)\b', v, re.I):
            print('WARN overclaim word in', k)
    json.dump({'fieldData': fd}, open(SP + f'{name}_patch.json', 'w'), indent=1)
    words = len(re.sub(r'<[^>]+>', ' ', html.unescape(guide)).split())
    print(name, '| meta-title', len(fd['meta-title']), '| meta-desc', len(fd['meta-description']), '| guide words ~', words, '| guide chars', len(guide))
