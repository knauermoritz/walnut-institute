#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont
import os

DIR = os.path.dirname(os.path.abspath(__file__))

W, H   = 1200, 630
BG     = (10, 10, 10)
WHITE  = (255, 255, 255)
MUTED  = (120, 120, 120)

out  = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(out)

# ── logo ─────────────────────────────────────────────────────────────────────
LOGO_SIZE = 100
logo = Image.open(os.path.join(DIR, "favicon.png")).convert("RGBA")
logo = logo.resize((LOGO_SIZE, LOGO_SIZE), Image.LANCZOS)

logo_x = (W - LOGO_SIZE) // 2
logo_y = 178

# composite logo over bg colour to avoid white fringe
bg_patch = Image.new("RGBA", (LOGO_SIZE, LOGO_SIZE), BG + (255,))
bg_patch.alpha_composite(logo)
out.paste(bg_patch.convert("RGB"), (logo_x, logo_y))

# ── fonts ─────────────────────────────────────────────────────────────────────
def load_font(size, idx=0):
    for path in ["/System/Library/Fonts/HelveticaNeue.ttc",
                 "/System/Library/Fonts/Helvetica.ttc"]:
        try:
            return ImageFont.truetype(path, size, index=idx)
        except:
            pass
    return ImageFont.load_default()

# index 1 = Bold, index 7 = Light
font_name = load_font(80, idx=1)
font_tag  = load_font(26, idx=7)

# ── "Walnut" ──────────────────────────────────────────────────────────────────
name_text = "Walnut"
bbox = draw.textbbox((0, 0), name_text, font=font_name)
name_w = bbox[2] - bbox[0]
name_x = (W - name_w) // 2
name_y = logo_y + LOGO_SIZE + 28
draw.text((name_x, name_y), name_text, font=font_name, fill=WHITE)

# ── tagline ───────────────────────────────────────────────────────────────────
tag_text = "Schulen digitalisieren"
bbox2 = draw.textbbox((0, 0), tag_text, font=font_tag)
tag_w  = bbox2[2] - bbox2[0]
tag_x  = (W - tag_w) // 2
tag_y  = name_y + (bbox[3] - bbox[1]) + 16
draw.text((tag_x, tag_y), tag_text, font=font_tag, fill=MUTED)

# ── save ──────────────────────────────────────────────────────────────────────
out_path = os.path.join(DIR, "og-image.png")
out.save(out_path, "PNG", optimize=True)
print(f"Saved → {out_path}  ({W}×{H})")
