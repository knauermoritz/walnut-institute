#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont
import math, os

W, H = 1200, 630
BG   = (20, 20, 20)       # near-black background
BLUE = (20, 0, 255)        # brand blue

out = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(out)

# ── subtle blue gradient stripe on left ──────────────────────────────────────
for x in range(480):
    alpha = max(0, 0.18 - x / 480 * 0.18)
    r = int(BG[0] + (BLUE[0] - BG[0]) * alpha)
    g = int(BG[1] + (BLUE[1] - BG[1]) * alpha)
    b = int(BG[2] + (BLUE[2] - BG[2]) * alpha)
    draw.line([(x, 0), (x, H)], fill=(r, g, b))

# ── app screenshot (right side, with rounded corners + shadow) ───────────────
ss = Image.open(os.path.join(os.path.dirname(__file__), "ss-walnut.png")).convert("RGBA")
ss_h = int(H * 0.88)
ss_w = int(ss.width * ss_h / ss.height)
ss   = ss.resize((ss_w, ss_h), Image.LANCZOS)

# shadow
shadow = Image.new("RGBA", out.size, (0, 0, 0, 0))
sd = ImageDraw.Draw(shadow)
sx = W - ss_w - 48
sy = (H - ss_h) // 2
for i in range(24, 0, -1):
    sd.rounded_rectangle([sx-i, sy-i//2, sx+ss_w+i, sy+ss_h+i//2],
                         radius=28, fill=(0,0,0, int(120*i/24)))
out.paste(Image.alpha_composite(Image.new("RGBA", out.size, (0,0,0,0)), shadow).convert("RGB"),
          mask=shadow.split()[3])

# paste screenshot
mask = Image.new("L", ss.size, 0)
ImageDraw.Draw(mask).rounded_rectangle([0, 0, ss_w-1, ss_h-1], radius=22, fill=255)
out.paste(ss, (sx, sy), mask)

# ── walnut logo (SVG rendered as circles/paths via pillow draw) ──────────────
lx, ly, ls = 64, 56, 52   # logo x, y, size
r = ls // 2

def rounded_rect(d, x, y, w, h, rx, fill):
    d.rounded_rectangle([x, y, x+w, y+h], radius=rx, fill=fill)

# blue rounded square background
rounded_rect(draw, lx, ly, ls, ls, rx=12, fill=BLUE)

# two white arc shapes (walnut icon)
draw2 = ImageDraw.Draw(out)
# left arc (D-shape facing right)
lc = (lx + ls*0.34, ly + ls*0.5)   # center of left circle
draw2.ellipse([lx + ls*0.04, ly + ls*0.09,
               lx + ls*0.64, ly + ls*0.91], fill="white")
# cut out center to make arc
draw2.rounded_rectangle([lx + ls*0.34, ly + ls*0.09,
                          lx + ls*0.64, ly + ls*0.91],
                         radius=2, fill=BLUE)
# right arc (D-shape facing left)
draw2.ellipse([lx + ls*0.36, ly + ls*0.09,
               lx + ls*0.96, ly + ls*0.91], fill="white")
draw2.rounded_rectangle([lx + ls*0.36, ly + ls*0.09,
                          lx + ls*0.66, ly + ls*0.91],
                         radius=2, fill=BLUE)

# ── text ─────────────────────────────────────────────────────────────────────
try:
    font_name  = ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc", 64)
    font_tag   = ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc", 22)
    font_sub   = ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc", 20)
except:
    font_name  = ImageFont.load_default()
    font_tag   = font_name
    font_sub   = font_name

# "Walnut"
draw.text((lx, ly + ls + 28), "Walnut", font=font_name, fill="white")

# tagline
draw.text((lx, ly + ls + 28 + 76), "Schule. Digitalisieren.", font=font_tag,
          fill=(255, 255, 255, 160))

# sub
draw.text((lx, ly + ls + 28 + 76 + 36),
          "Aufgaben · Noten · Korrekturen — alles auf einem Gerät.",
          font=font_sub, fill=(160, 160, 160))

# thin blue accent line under logo
draw.rectangle([lx, ly + ls + 18, lx + 32, ly + ls + 20], fill=BLUE)

# ── save ─────────────────────────────────────────────────────────────────────
out_path = os.path.join(os.path.dirname(__file__), "og-image.png")
out.save(out_path, "PNG", optimize=True)
print(f"Saved → {out_path}  ({W}×{H})")
