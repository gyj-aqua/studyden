# -*- coding: utf-8 -*-
"""Rebuilds the ART block in study-den.html from the PNGs in art/.

The companions are the artwork from the reference sheets, cut out and carried
inline so the artifact, the hosted site and the single-file copy all show them
without fetching anything. Run this after changing or adding a character image,
then run build-site.py.
"""
import base64, io, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
PAGE = os.path.join(HERE, 'study-den.html')
ART = os.path.join(HERE, 'art')

s = io.open(PAGE, encoding='utf-8').read()
start = s.index('const ART={')
end = s.index('};', start) + 2

ids = re.findall(r"\{id:'([a-z]+)'", s[end:s.index('];', end)])
lines, total = [], 0
for cid in ids:
    p = os.path.join(ART, cid + '.png')
    raw = io.open(p, 'rb').read()
    total += len(raw)
    lines.append(" %s:'data:image/png;base64,%s'," % (cid, base64.b64encode(raw).decode('ascii')))

s = s[:start] + 'const ART={\n' + '\n'.join(lines) + '\n};' + s[end:]
io.open(PAGE, 'w', encoding='utf-8').write(s)
print('inlined %d images, %.0f KB of artwork' % (len(ids), total / 1024.0))
