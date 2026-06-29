from pathlib import Path
import struct
import zlib

OUTPUT = Path('assets/logo.png')
OUTPUT.parent.mkdir(exist_ok=True)

WIDTH, HEIGHT = 800, 320

# Simple PNG writer with RGBA

def chunk(type_bytes, data):
    return struct.pack('!I', len(data)) + type_bytes + data + struct.pack('!I', zlib.crc32(type_bytes + data) & 0xFFFFFFFF)

pixels = []
for y in range(HEIGHT):
    row = []
    for x in range(WIDTH):
        # background gradient
        t = x / WIDTH
        r = int(10 + 30 * t)
        g = int(40 + 80 * t)
        b = int(90 + 100 * t)
        row.append((r, g, b, 255))
    pixels.append(row)

# Draw accent shape
for y in range(60, 260):
    for x in range(60, 260):
        dx = x - 160
        dy = y - 160
        if dx*dx + dy*dy < 11000:
            pixels[y][x] = (0, 176, 255, 255)
for y in range(100, 245):
    for x in range(240, 520):
        if 0 <= x - y + 80 < 40 and 0 <= y - x + 160 < 40:
            pixels[y][x] = (0, 200, 112, 255)
for y in range(120, 220):
    for x in range(320, 520):
        if 100 < (x-360) * 1.2 + (y-160) < 220:
            pixels[y][x] = (255, 255, 255, 255)

# Draw simple wordmark block
for y in range(120, 200):
    for x in range(420, 760):
        if (x - 420) % 60 < 42 and (y - 120) % 80 < 55:
            pixels[y][x] = (12, 27, 219, 255)

# Save PNG
raw = bytearray()
for row in pixels:
    raw.append(0)
    for r, g, b, a in row:
        raw.extend((r, g, b, a))

png = b'\x89PNG\r\n\x1a\n'
png += chunk(b'IHDR', struct.pack('!IIBBBBB', WIDTH, HEIGHT, 8, 6, 0, 0, 0))
png += chunk(b'IDAT', zlib.compress(bytes(raw), 9))
png += chunk(b'IEND', b'')

OUTPUT.write_bytes(png)
print(f'Generated {OUTPUT}')
