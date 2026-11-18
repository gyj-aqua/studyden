# -*- coding: utf-8 -*-
"""Builds the home-screen icon: Mochi on the Tidepool teal, in the sizes an
install needs. Run after changing art/mochi.png."""
from PIL import Image, ImageDraw
import os

HERE = os.path.dirname(os.path.abspath(__file__))
S = 1024
TEAL, TEAL_L = (13, 133, 160), (31, 160, 186)

img = Image.new('RGBA', (S, S), (0, 0, 0, 0))
ImageDraw.Draw(img).rounded_rectangle([0, 0, S - 1, S - 1], radius=int(S * 0.225), fill=TEAL)

# a soft vertical gradient, light at the top
grad = Image.new('L', (1, S))
gp = grad.load()
for y in range(S):
    gp[0, y] = int(255 * max(0.0, 1.0 - (y / float(S - 1)) * 1.3) ** 1.5)
wash = Image.new('RGBA', (S, S), TEAL_L + (255,))
wash.putalpha(grad.resize((S, S)))
img.alpha_composite(Image.composite(wash, Image.new('RGBA', (S, S), (0, 0, 0, 0)), img.split()[3]))

# the companion, inside the safe area a maskable icon needs
mochi = Image.open(os.path.join(HERE, 'art', 'mochi.png')).convert('RGBA')
side = int(S * 0.64)
mochi = mochi.resize((side, side), Image.LANCZOS)
shadow = Image.new('RGBA', (S, S), (0, 0, 0, 0))
ImageDraw.Draw(shadow).ellipse([S * .30, S * .76, S * .70, S * .815], fill=(10, 60, 75, 70))
img.alpha_composite(shadow)
img.alpha_composite(mochi, ((S - side) // 2, int(S * 0.18)))

written = []
for name, px in (('icon-512.png', 512), ('icon-192.png', 192), ('apple-touch-icon.png', 180)):
    img.resize((px, px), Image.LANCZOS).convert('RGB').save(os.path.join(HERE, name))
    written.append(name)
print('icons written:', ', '.join(written))
