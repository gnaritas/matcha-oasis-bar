#!/usr/bin/env python3
"""og.png 1200x630 — Matcha Oasis Bar (v2: measured clearances, 2x supersample AA).
Deep matcha-green oasis; cream serif wordmark, gold accents, clean flat matcha bowl.
Shop identity only — zero builder tokens."""
from PIL import Image, ImageDraw, ImageFont
import os, math, random

W, H = 1200, 630
S = 2                       # supersample factor for smooth edges
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public", "og.png")

DEEP = (28, 48, 33); MATCHA = (63, 107, 52)
CREAM = (246, 241, 227); MIST = (207, 224, 184); GOLD = (201, 162, 75); LEAF = (143, 191, 111)

def font(paths, size):
    bases = ["/System/Library/Fonts/Supplemental/", "/System/Library/Fonts/"]
    for b in bases:
        for n in paths:
            p = b + n
            if os.path.exists(p):
                try: return ImageFont.truetype(p, size)
                except Exception: pass
    return ImageFont.load_default()

serif = lambda s: font(["Georgia Bold.ttf", "GeorgiaB.ttf", "Georgia.ttf"], s*S)
ital  = lambda s: font(["Georgia Italic.ttf", "GeorgiaI.ttf", "Georgia.ttf"], s*S)
cond  = lambda s: font(["Avenir Next Condensed Bold.ttf", "AvenirNextCondensed-Bold.ttf", "Futura.ttc", "HelveticaNeue-Bold.ttf"], s*S)

# geometry (in 1x space; multiplied by S when drawing)
L = 78                      # left text margin
bx, by = 980, 348           # bowl center
bw = 88                     # bowl half-width at rim
safe = 840                  # max right edge for ALL text (measured check below)

img = Image.new("RGB", (W*S, H*S), DEEP)
d = ImageDraw.Draw(img, "RGBA")

for y in range(H*S):
    t = y / (H*S)
    d.line([(0, y), (W*S, y)], fill=(int(DEEP[0]+(MATCHA[0]-DEEP[0])*t*.85),
                                      int(DEEP[1]+(MATCHA[1]-DEEP[1])*t*.85),
                                      int(DEEP[2]+(MATCHA[2]-DEEP[2])*t*.85)))

def P(x, y): return (x*S, y*S)
def rings(cx, cy, radii, color, widths=(3,)):
    for i, r in enumerate(radii):
        a = max(22, 62 - i*14)
        d.ellipse([P(cx-r, cy-r), P(cx+r, cy+r)], outline=color+(a,), width=(widths[i] if len(widths)>i else widths[0])*S)
rings(1165, -35, [140, 205, 272], MIST)
rings(-55, 660, [120, 185], GOLD)

rng = random.Random(707)
for _ in range(1600):
    x = rng.randint(0, W*S-1); y = rng.randint(0, H*S-1)
    d.point((x, y), fill=(255, 255, 240, rng.randint(3, 13)))

# ---- steam (above bowl surface at by-27; rises ~120px) ----
def steam(x0, phase):
    pts = []
    for k in range(48):
        t = k/47.0
        y = by - 42 - t*118
        x = x0 + 12*math.sin(t*2.6*math.pi + phase)*(0.45+t)
        pts.append(P(x, y))
    d.line(pts, fill=MIST+(120,), width=3*S, joint="curve")
    d.line(pts, fill=MIST+(60,), width=4*S, joint="curve")
steam(bx-56, 0.5); steam(bx, 1.7); steam(bx+56, 2.9)

# ---- saucer (bowl base overlaps it so the bowl rests ON it) ----
d.ellipse([P(bx-116, by+54), P(bx+116, by+80)], fill=(233, 226, 205, 255))
d.ellipse([P(bx-84, by+59), P(bx+84, by+75)], fill=(120, 105, 70, 60))

# ---- bowl: clean flat design ----
rim_y, base_y = by-24, by+56
top_l, top_r = bx-bw, bx+bw
bot_l, bot_r = bx-bw*0.72, bx+bw*0.72
poly = [P(top_l, rim_y), P(top_r, rim_y), P(bot_r, base_y), P(bot_l, base_y)]
d.polygon(poly, fill=CREAM+(255,), outline=(44, 58, 38, 255), width=4*S)
d.ellipse([P(bot_l, base_y-16), P(bot_r, base_y+14)], fill=CREAM+(255,), outline=(44, 58, 38, 255), width=4*S)
# belly band
d.line([P(bx-bw*0.86, by+22), P(bx+bw*0.86, by+22)], fill=GOLD+(215,), width=4*S)
d.line([P(bx-bw*0.80, by+34), P(bx+bw*0.80, by+34)], fill=GOLD+(140,), width=3*S)
# matcha surface (rim ellipse)
d.ellipse([P(top_l, rim_y-14), P(top_r, rim_y+14)], fill=LEAF+(255,), outline=(44, 58, 38, 255), width=4*S)
d.ellipse([P(bx-bw*0.62, rim_y-9), P(bx+bw*0.62, rim_y+9)], fill=(168, 207, 138, 255))

# ---- type (measure everything, enforce clearance) ----
texts = []  # (draw_args, font, x, y) to bbox-check right edges
def put(x, y, txt, fnt, fill):
    d.text((x*S, y*S), txt, font=fnt, fill=fill)
    bb = d.textbbox((x*S, y*S), txt, font=fnt)
    texts.append((txt[:24], bb[2]/S))

def fit(txt, mk, start, right):
    s = start
    while True:
        f = mk(s)
        w = d.textbbox((0, 0), txt, font=f)[2] / S
        if w <= right - L or s <= 14: return s, f
        s -= 1

k_size, k = fit("MATCHA  \u00b7  BUBBLE TEA  \u00b7  REFRESHERS", cond, 29, safe)
put(L, 92, "MATCHA  \u00b7  BUBBLE TEA  \u00b7  REFRESHERS", k, GOLD+(255,))

# headline: shrink until within safe edge
size, f1 = fit("Matcha Oasis Bar", serif, 92, safe)
put(L, 146, "Matcha Oasis Bar", f1, (249, 246, 232, 255))

quote = "\u201cA little escape in every sip.\u201d"
q_size, fq = fit(quote, ital, 42, safe)
put(L, 270, quote, fq, MIST+(255,))

meta = "113 W. MOUNTAIN ST  \u00b7  DOWNTOWN KERNERSVILLE, NC"
mm_size, fm = fit(meta, cond, 30, safe)
put(L, 396, meta, fm, (246, 241, 227, 255))
meta2 = "OPEN MON\u2013SAT 10AM\u20138PM  \u00b7  RATED 5.0 ON GOOGLE"
m2_size, fm2 = fit(meta2, cond, 27, safe)
put(L, 442, meta2, fm2, (207, 224, 184, 255))

# gold rule: width = measured meta width (balanced)
mw = d.textbbox((L*S, 396*S), meta, font=fm)[2]/S - L
d.line([P(L, 360), P(L+mw, 360)], fill=GOLD+(205,), width=3*S)

img = img.resize((W, H), Image.LANCZOS)
img.save(OUT, "PNG", optimize=True)

# ---- clearance report (1x coordinates) ----
bowl_left = bx - bw
steam_left = min(bx-56, bx, bx+56) - 12 - 4
max_text_r = max(t[1] for t in texts)
print(f"sizes: headline={size}px kicker={k_size} quote={q_size} meta={mm_size} meta2={m2_size}")
for name, r in texts: print(f"  text r={r:6.0f}  {name}")
print(f"max text right = {max_text_r:.0f}; bowl left = {bowl_left}; steam left = {steam_left:.0f}")
ok = max_text_r <= min(bowl_left, steam_left) - 18
print("CLEARANCE:", "PASS" if ok else "FAIL", "(need 18px min gap)")
assert max_text_r <= safe + 5, "text past safe edge"
assert ok, "text collides with art"
print("saved", OUT, os.path.getsize(OUT), "bytes")
