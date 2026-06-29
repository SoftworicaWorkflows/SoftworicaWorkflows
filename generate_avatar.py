from PIL import Image, ImageOps
from pathlib import Path

root = Path(__file__).resolve().parent
assets = root / 'assets'
logo_path = assets / 'logo.png'
avatar_path = assets / 'avatar.png'

W = 512
try:
    logo = Image.open(logo_path).convert('RGBA')
except Exception as e:
    print('Cannot open logo:', e)
    raise

# resize logo to fit
max_logo_w = int(W * 0.7)
ratio = max_logo_w / logo.width
new_size = (int(logo.width * ratio), int(logo.height * ratio))
logo = logo.resize(new_size, Image.LANCZOS)

# create square background
bg = Image.new('RGBA', (W, W), (255,255,255,0))
pos = ((W - logo.width)//2, (W - logo.height)//2)
bg.paste(logo, pos, logo)

# create circular mask
mask = Image.new('L', (W, W), 0)
draw = Image.new('L', (W, W), 0)
from PIL import ImageDraw
ImageDraw.Draw(mask).ellipse((0,0,W,W), fill=255)

result = Image.new('RGBA', (W, W), (255,255,255,0))
result.paste(bg, (0,0), mask)

# optional white circle background for visibility
circle_bg = Image.new('RGBA', (W, W), (255,255,255,255))
circle_bg.putalpha(255)
final = Image.new('RGBA', (W, W), (255,255,255,0))
final.paste(circle_bg, (0,0), mask)
final.paste(result, (0,0), mask)

final.save(avatar_path)
print('Created', avatar_path)
