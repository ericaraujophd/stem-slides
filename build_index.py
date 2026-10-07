#!/usr/bin/env python3
"""Builds index.html (the GitHub Pages site) from README.md.

Run from the repo folder after editing README.md:  python3 build_index.py
README.md stays the single source of truth: session headings are '## ',
the chair line starts with 'Chair:', and table rows are '| time | presenter | slides |'.
Slides cells are either 'Pending', plain text, or markdown links [label](path).
If images/header.png exists it is shown as a cream band under the maroon title bar.
"""
import re, html, os

lines = open('README.md', encoding='utf-8').read().split('\n')
sessions, cur = [], None
for l in lines:
    if l.startswith('## '):
        cur = {'title': l[3:].strip(), 'chair': '', 'rows': []}
        sessions.append(cur)
    elif cur is not None and l.startswith('Chair:'):
        cur['chair'] = l[6:].strip()
    elif cur is not None and l.startswith('|') and not l.startswith('|---') and 'Presenter' not in l:
        c = [x.strip() for x in l.strip('|').split('|')]
        cur['rows'].append(c)

def cell(s):
    links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', s)
    if links:
        return ' '.join(f'<a class="btn" href="{html.escape(u)}">{html.escape(t)}</a>' for t, u in links)
    if s.lower() == 'pending':
        return '<span class="pending">Pending</span>'
    return f'<span class="note">{html.escape(s)}</span>'

banner = os.path.exists('images/header.png')
parts = []
for s in sessions:
    day, _, rest = s['title'].partition(': ')
    rows = ''.join(f'<tr><td class="t">{html.escape(r[0])}</td><td>{html.escape(r[1])}</td><td class="s">{cell(r[2])}</td></tr>' for r in s['rows'])
    parts.append(f'<section class="card"><h2>{html.escape(s["title"])}</h2><p class="chair">{html.escape(s["chair"] and "Chair: " + s["chair"])}</p><table><tbody>{rows}</tbody></table></section>')

art = '<div class="art"><img src="images/header.png" alt="Sketch of a reformer looking at a pocket watch"></div>' if banner else ''
page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>AI &amp; STEM Track Slides | Wisdom in the Age of AI 2026</title>
<style>
:root{{--maroon:#6E1C2E;--dark:#4a1220;--gold:#F2B705;--ink:#2b2b2b;--bg:#f7f3ef}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:16px/1.5 Georgia,'Times New Roman',serif}}
header{{background:var(--maroon);color:#fff;border-bottom:6px solid var(--gold);position:relative}}
header .shade{{background:linear-gradient(90deg,rgba(74,18,32,.92),rgba(110,28,46,.55));}}
.wrap{{max-width:900px;margin:0 auto;padding:0 20px}}
header .wrap{{display:flex;align-items:center;gap:24px;padding:28px 20px}}
header img{{height:90px;width:auto}}
h1{{margin:0;font-size:1.9rem;line-height:1.2}}
.sub{{color:var(--gold);font:600 .95rem/1.4 Helvetica,Arial,sans-serif;letter-spacing:.08em;text-transform:uppercase;margin:0 0 6px}}
.intro{{font:15px/1.5 Helvetica,Arial,sans-serif;margin:24px 0}}
.card{{background:#fff;border-radius:8px;border-top:4px solid var(--maroon);box-shadow:0 1px 4px rgba(0,0,0,.12);margin:0 0 20px;padding:18px 20px}}
h2{{margin:0;color:var(--maroon);font-size:1.25rem}}.chair{{margin:2px 0 10px;font:italic .95rem Georgia,serif;color:#666}}
table{{width:100%;border-collapse:collapse;font:15px/1.4 Helvetica,Arial,sans-serif}}
td{{padding:9px 6px;border-top:1px solid #eadfd8;vertical-align:top}}td.t{{white-space:nowrap;color:#666;width:80px}}td.s{{text-align:right}}
.btn{{display:inline-block;background:var(--maroon);color:#fff;text-decoration:none;padding:4px 12px;border-radius:14px;font-size:.85rem;margin-left:4px}}
.btn:hover{{background:var(--dark)}}
.pending{{color:#8a7a70;border:1px dashed #c9b8ad;padding:3px 10px;border-radius:14px;font-size:.85rem}}.note{{color:#666;font-size:.9rem}}

.art{{background:#FFFFFF;border-bottom:1px solid #eadfd8;text-align:center}}.art img{{display:block;margin:0 auto;max-width:100%;max-height:300px;object-fit:contain}}
footer{{text-align:center;font:13px Helvetica,Arial,sans-serif;color:#777;padding:10px 0 40px}}footer a{{color:var(--maroon)}}
@media(max-width:560px){{header .wrap{{flex-direction:column;align-items:flex-start}}td.s{{text-align:left}}tr{{display:block;padding:6px 0}}td{{display:inline-block;border:0;padding:2px 6px}}}}
</style></head><body>
<header><div class="shade"><div class="wrap">
<img src="images/calvin-logo.png" alt="Calvin University">
<div><p class="sub">Wisdom in the Age of AI 2026</p><h1>AI &amp; STEM Track Slides</h1></div>
</div></div></header>
{art}
<main class="wrap">
<p class="intro">October 8 and 9, 2026, Calvin University. All sessions are in the Board Room, Prince Conference Center. Files are stored exactly as the presenters sent them. "Pending" means the slides have not been added yet. Questions: <a href="mailto:AI-STEM@calvin.edu">AI-STEM@calvin.edu</a></p>
{''.join(parts)}
</main>
<footer>Source files on <a href="https://github.com/ericaraujophd/stem-slides">GitHub</a></footer>
</body></html>'''
open('index.html', 'w', encoding='utf-8').write(page)
print('index.html written,', len(sessions), 'sessions')
