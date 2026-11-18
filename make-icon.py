# -*- coding: utf-8 -*-
"""Draws the Study Den app icon (Nori the otter) and writes the PNG sizes a
home-screen install needs. Rendered at 4x and downscaled for clean edges."""
from PIL import Image, ImageDraw
import os

S = 4096                      # supersample canvas
OUT = os.path.dirname(os.path.abspath(__file__))

TEAL   = (13, 133, 160)
TEAL_L = (31, 160, 186)
FUR    = (181, 128, 79)
FUR_D  = (122, 84, 48)
CREAM  = (243, 224, 198)
WHITE  = (253, 243, 228)
INK    = (51, 48, 74)
PINK   = (212, 156, 149)

img = Image.new('RGBA', (S, S), (0, 0, 0, 0))
d = ImageDraw.Draw(img)

# full-bleed rounded square so the icon also works as a maskable icon
d.rounded_rectangle([0, 0, S - 1, S - 1], radius=int(S * 0.225), fill=TEAL)
# a soft vertical gradient, light at the top
grad = Image.new('L', (1, S))
gp = grad.load()
for y in range(S):
    t = y / float(S - 1)
    gp[0, y] = int(255 * max(0.0, 1.0 - t * 1.3) ** 1.5)
wash = Image.new('RGBA', (S, S), TEAL_L + (255,))
wash.putalpha(grad.resize((S, S)))
img.alpha_composite(Image.composite(wash, Image.new('RGBA', (S, S), (0, 0, 0, 0)),
                                    img.split()[3]))
d = ImageDraw.Draw(img)

def e(cx, cy, rx, ry, fill, outline=None, w=0):
    d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=fill, outline=outline, width=w)

u = S / 100.0                 # work in 0-100 units
LW = int(2.0 * u)

# ears, behind the head
for ex in (30.5, 69.5):
    e(ex * u, 33 * u, 9.5 * u, 9.5 * u, FUR, FUR_D, LW)
    e(ex * u, 33 * u, 4.6 * u, 4.6 * u, PINK)

# head
e(50 * u, 52 * u, 27 * u, 25 * u, FUR, FUR_D, LW)
# cheek/chin patch
e(50 * u, 60 * u, 19 * u, 16 * u, CREAM)
# muzzle
e(50 * u, 62 * u, 13 * u, 9.5 * u, WHITE, FUR_D, int(1.4 * u))

# eyes with a highlight and a small glint
for ex in (40.5, 59.5):
    e(ex * u, 47 * u, 4.4 * u, 4.8 * u, INK)
    e((ex + 1.5) * u, 45.2 * u, 1.5 * u, 1.5 * u, (255, 255, 255))
    e((ex - 1.4) * u, 49.4 * u, 0.8 * u, 0.8 * u, (255, 255, 255, 190))

# brows
for sx, ex2 in ((35.5, 44.5), (55.5, 64.5)):
    d.line([sx * u, 39.4 * u, ex2 * u, 38.2 * u], fill=FUR_D, width=int(1.7 * u),
           joint='curve')

# blush
e(31 * u, 56 * u, 4.2 * u, 2.7 * u, PINK + (150,))
e(69 * u, 56 * u, 4.2 * u, 2.7 * u, PINK + (150,))

# nose + smile
d.rounded_rectangle([46.3 * u, 56.2 * u, 53.7 * u, 61.2 * u], radius=2.4 * u, fill=INK)
d.arc([44 * u, 59 * u, 50.4 * u, 66 * u], 10, 150, fill=INK, width=int(1.7 * u))
d.arc([49.6 * u, 59 * u, 56 * u, 66 * u], 30, 170, fill=INK, width=int(1.7 * u))

# whiskers
for sy, dy in ((60.5, -1.6), (63.5, 1.6)):
    d.line([36 * u, sy * u, 25 * u, (sy + dy) * u], fill=FUR_D, width=int(1.2 * u))
    d.line([64 * u, sy * u, 75 * u, (sy + dy) * u], fill=FUR_D, width=int(1.2 * u))

base = img.resize((1024, 1024), Image.LANCZOS)
written = []
for name, px in (('icon-512.png', 512), ('icon-192.png', 192), ('apple-touch-icon.png', 180)):
    base.resize((px, px), Image.LANCZOS).save(os.path.join(OUT, name))
    written.append(name)
print('icons written:', ', '.join(written))
