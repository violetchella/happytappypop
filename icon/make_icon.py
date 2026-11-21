"""Draws the Happy Tappy Pop app icon with Pillow (4x supersampled, then downscaled)."""
import math, sys
from PIL import Image, ImageDraw

OUT = sys.argv[1]  # output path prefix, e.g. /home/.../happy-tappy-pop-icon
S = 4
N = 1024 * S
img = Image.new("RGBA", (N, N))
d = ImageDraw.Draw(img, "RGBA")

def P(*v): return [x * S for x in v]
def hexc(h, a=255):
    h = h.lstrip("#"); return tuple(int(h[i:i+2], 16) for i in (0, 2, 4)) + (a,)
def circle(cx, cy, r, fill): d.ellipse(P(cx - r, cy - r, cx + r, cy + r), fill=fill)
def ellipse(cx, cy, rx, ry, fill): d.ellipse(P(cx - rx, cy - ry, cx + rx, cy + ry), fill=fill)
def poly(pts, fill): d.polygon([(x * S, y * S) for x, y in pts], fill=fill)
def line(x1, y1, x2, y2, w, fill):
    d.line(P(x1, y1, x2, y2), fill=fill, width=w * S)
    circle(x1, y1, w / 2, fill); circle(x2, y2, w / 2, fill)
def star(cx, cy, ro, ri, n=5, rot=-90):
    pts = []
    for i in range(n * 2):
        r = ro if i % 2 == 0 else ri
        a = math.radians(rot + i * 180 / n)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts
def quad(p0, p1, p2, steps=60):
    return [((1-t)**2*p0[0]+2*(1-t)*t*p1[0]+t*t*p2[0], (1-t)**2*p0[1]+2*(1-t)*t*p1[1]+t*t*p2[1])
            for t in (i / steps for i in range(steps + 1))]

# sky gradient
top, bot = hexc("#7FCBF0"), hexc("#CDEFFA")
for y in range(N):
    t = y / N
    d.line([(0, y), (N, y)], fill=tuple(int(top[i] + (bot[i] - top[i]) * t) for i in range(3)) + (255,))

# soft sun glow behind the fox
for r, a in ((400, 40), (320, 50), (250, 60)):
    circle(512, 690, r, (255, 240, 180, a))

# hills
poly(quad((0, 850), (512, 700), (1024, 850)) + [(1024, 1024), (0, 1024)], hexc("#3DB37A"))
poly(quad((0, 930), (512, 840), (1024, 930)) + [(1024, 1024), (0, 1024)], hexc("#2E9A67"))

def bubble(cx, cy, r, color, dark):
    circle(cx, cy, r + 10, (255, 255, 255, 230))       # white rim
    circle(cx, cy, r, hexc(dark))
    circle(cx - r * .06, cy - r * .07, r * .9, hexc(color))
    ellipse(cx - r * .38, cy - r * .42, r * .26, r * .17, (255, 255, 255, 170))
    circle(cx - r * .62, cy - r * .12, r * .07, (255, 255, 255, 150))

# star bubble (red)
bubble(215, 340, 135, "#FF6F59", "#D9523F")
poly(star(210, 345, 72, 30), (255, 255, 255, 255))
# heart bubble (yellow)
bubble(815, 300, 125, "#FFC93C", "#E0A91E")
hx, hy, hs = 812, 305, 34
circle(hx - hs, hy - hs * .35, hs * 1.05, hexc("#2B2D42")); circle(hx + hs, hy - hs * .35, hs * 1.05, hexc("#2B2D42"))
poly([(hx - hs * 2.0, hy - hs * .05), (hx + hs * 2.0, hy - hs * .05), (hx, hy + hs * 2.0)], hexc("#2B2D42"))
# triangle bubble (purple, small)
bubble(130, 640, 78, "#8E6BD8", "#7353BD")
poly([(128, 600), (166, 664), (90, 664)], (255, 255, 255, 255))

# popping bubble (green) at top centre: burst rays, fragments, sparkles
pcx, pcy = 512, 205
for i in range(10):
    a = math.radians(i * 36 + 8)
    line(pcx + math.cos(a) * 70, pcy + math.sin(a) * 70, pcx + math.cos(a) * 128, pcy + math.sin(a) * 128, 20, (255, 255, 255, 255))
for i in range(8):
    a = math.radians(i * 45 + 25)
    circle(pcx + math.cos(a) * 160, pcy + math.sin(a) * 160, 16 if i % 2 else 11, hexc("#3DB37A"))
poly(star(pcx, pcy, 62, 26, n=8, rot=-90), hexc("#FFE36E"))
circle(pcx, pcy, 22, (255, 255, 255, 255))
for (sx, sy, sr) in ((360, 110, 34), (668, 120, 28), (650, 470, 24), (365, 480, 22)):
    poly(star(sx, sy, sr, sr * .28, n=4), (255, 255, 255, 240))

# ---- fox ----
OR, OR2, CREAM, DARK = hexc("#F58A3A"), hexc("#E06F22"), hexc("#FFF6EC"), hexc("#3A2E39")
# ears
for sgn in (-1, 1):
    bx = 512 + sgn * 150
    a, tip, c = (bx - sgn * 105, 615), (bx + sgn * 55, 370), (bx + sgn * 115, 600)
    poly([a, tip, c], OR)
    poly([(bx - sgn * 45, 585), (bx + sgn * 50, 430), (bx + sgn * 85, 585)], hexc("#FFD7B8"))
    lerp = lambda p, q, t: (p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t)
    poly([tip, lerp(tip, a, .22), lerp(tip, c, .22)], DARK)
# head + cheek fluff
ellipse(512, 700, 238, 190, OR)
for sgn in (-1, 1):
    poly([(512 + sgn * 200, 700), (512 + sgn * 290, 790), (512 + sgn * 150, 820)], OR)
    poly([(512 + sgn * 205, 745), (512 + sgn * 268, 800), (512 + sgn * 150, 812)], CREAM)
ellipse(512, 805, 190, 82, CREAM)
ellipse(420, 790, 112, 74, CREAM); ellipse(604, 790, 112, 74, CREAM)
ellipse(512, 568, 120, 40, hexc("#F79A50"))          # forehead highlight
# eyes (happy, shiny)
for ex in (425, 599):
    ellipse(ex, 675, 30, 40, DARK)
    circle(ex + 9, 660, 12, (255, 255, 255, 255)); circle(ex - 9, 690, 5, (255, 255, 255, 220))
# blush
ellipse(372, 752, 34, 18, (255, 140, 150, 140)); ellipse(652, 752, 34, 18, (255, 140, 150, 140))
# nose + smile
ellipse(512, 762, 34, 23, DARK); ellipse(503, 755, 10, 6, (255, 255, 255, 160))
d.arc(P(462, 752, 512, 812), 20, 160, fill=DARK, width=9 * S)
d.arc(P(512, 752, 562, 812), 20, 160, fill=DARK, width=9 * S)
# open happy mouth
poly(quad((482, 806), (512, 856), (542, 806)), hexc("#C2405A"))

big = img.resize((1024, 1024), Image.LANCZOS)
big.save(OUT + "-1024.png")
big.resize((512, 512), Image.LANCZOS).save(OUT + "-512.png")
big.resize((64, 64), Image.LANCZOS).save(OUT + "-64.png")
print("saved")
