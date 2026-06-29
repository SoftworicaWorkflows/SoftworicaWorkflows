from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

root = Path(__file__).resolve().parent
assets = root / 'assets'
assets.mkdir(exist_ok=True)
logo_path = assets / 'logo.png'
banner_path = assets / 'banner_hd.png'

W, H = 1600, 420
banner = Image.new('RGBA', (W, H), (6, 11, 26, 255))
d = ImageDraw.Draw(banner)

# gradient overlay
for i in range(H):
    r = int(4 + (30 - 4) * (i / H))
    g = int(14 + (60 - 14) * (i / H))
    b = int(36 + (90 - 36) * (i / H))
    d.line([(0, i), (W, i)], fill=(r, g, b, 255))

# subtle pattern circles
for cx, cy, r in [(120, 120, 90), (W-160, H//2, 120)]:
    d.ellipse((cx-r, cy-r, cx+r, cy+r), outline=(24,124,255,40), width=6)

# paste logo if present
try:
    logo = Image.open(logo_path).convert('RGBA')
    # resize logo
    lw = 220
    logo.thumbnail((lw, lw), Image.LANCZOS)
    banner.paste(logo, (60, (H - logo.height)//2), logo)
except Exception as e:
    print('Logo not found or error:', e)

# Title text
try:
    font_title = ImageFont.truetype('arial.ttf', 48)
    font_sub = ImageFont.truetype('arial.ttf', 20)
except Exception:
    from PIL import ImageFont
    font_title = ImageFont.load_default()
    font_sub = ImageFont.load_default()

x_text = 60 + 240
d.text((x_text, 110), 'Softworica Workflows', font=font_title, fill=(236,246,255,255))
d.text((x_text, 170), 'Your Future, Our Framework — Innovate · Build · Automate · Deploy', font=font_sub, fill=(180,210,235,255))

# CTA bubbles
cta_colors = [(30,144,255),(34,197,94),(168,85,247),(234,179,8)]
cta_texts = ['Innovate','Build','Automate','Deploy']
cx = x_text
cy = 240
for i, txt in enumerate(cta_texts):
    w = 140
    h = 42
    rx = cx + i*(w+14)
    d.rounded_rectangle((rx, cy, rx+w, cy+h), radius=22, fill=cta_colors[i]+(255,))
    # center text
    # compute text size using textbbox for compatibility
    bbox = d.textbbox((0,0), txt, font=font_sub)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    d.text((rx + (w-tw)/2, cy + (h-th)/2), txt, font=font_sub, fill=(255,255,255,255))

# save
banner.save(banner_path)
print('Created', banner_path)
