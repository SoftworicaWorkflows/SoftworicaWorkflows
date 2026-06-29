from pathlib import Path
import math
import struct
import zlib

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / 'assets'
ASSETS.mkdir(exist_ok=True)
(ASSETS / 'screenshots').mkdir(exist_ok=True)


def write_png(path, width, height, pixels):
    def chunk(chunk_type, data):
        return struct.pack('!I', len(data)) + chunk_type + data + struct.pack('!I', zlib.crc32(chunk_type + data) & 0xFFFFFFFF)

    raw = bytearray()
    for row in pixels:
        raw.append(0)
        for r, g, b, a in row:
            raw.extend((r, g, b, a))
    png_data = b'\x89PNG\r\n\x1a\n'
    png_data += chunk(b'IHDR', struct.pack('!IIBBBBB', width, height, 8, 6, 0, 0, 0))
    png_data += chunk(b'IDAT', zlib.compress(bytes(raw), 9))
    png_data += chunk(b'IEND', b'')
    path.write_bytes(png_data)


def rgba(r, g, b, a=255):
    return (r, g, b, a)


def create_logo(path):
    w = h = 640
    pixels = [[rgba(7, 15, 32, 255) for _ in range(w)] for _ in range(h)]
    for y in range(h):
        for x in range(w):
            if 80 <= x <= 560 and 80 <= y <= 560:
                if x in range(120, 220) or y in range(120, 220):
                    pixels[y][x] = rgba(37, 99, 235, 255)
                elif 220 <= x <= 420 and 220 <= y <= 420:
                    pixels[y][x] = rgba(56, 189, 248, 255)
                elif x >= 420 and y >= 420:
                    pixels[y][x] = rgba(30, 64, 175, 255)
            if 160 <= x <= 480 and 160 <= y <= 480:
                if x in range(220, 420) and y in range(220, 420):
                    pixels[y][x] = rgba(255, 255, 255, 255)
    write_png(path, w, h, pixels)


def create_banner(path):
    w, h = 1600, 500
    pixels = [[rgba(3, 10, 25, 255) for _ in range(w)] for _ in range(h)]
    for y in range(h):
        for x in range(w):
            if x < 300 and y < 500:
                pixels[y][x] = rgba(15, 23, 42, 255)
            if 1000 <= x <= 1500 and 80 <= y <= 420:
                pixels[y][x] = rgba(37, 99, 235, 255)
            if 1200 <= x <= 1450 and 120 <= y <= 380:
                pixels[y][x] = rgba(56, 189, 248, 255)
            if 1100 <= x <= 1300 and 150 <= y <= 350:
                pixels[y][x] = rgba(15, 118, 110, 255)
    for y in range(30, 470):
        for x in range(30, 1570):
            if x in range(70, 180) and y in range(80, 110):
                pixels[y][x] = rgba(37, 99, 235, 255)
            if x in range(70, 150) and y in range(140, 180):
                pixels[y][x] = rgba(56, 189, 248, 255)
    write_png(path, w, h, pixels)


def create_hero(path):
    w, h = 1600, 900
    pixels = [[rgba(2, 8, 23, 255) for _ in range(w)] for _ in range(h)]
    for y in range(h):
        for x in range(w):
            if (x + y) % 80 < 20:
                pixels[y][x] = rgba(15, 23, 42, 255)
            if x in range(200, 1400) and y in range(180, 720):
                pixels[y][x] = rgba(10, 20, 40, 255)
    write_png(path, w, h, pixels)


def create_screenshot(path):
    w, h = 1200, 700
    pixels = [[rgba(3, 10, 25, 255) for _ in range(w)] for _ in range(h)]
    for y in range(40, 660):
        for x in range(40, 1160):
            if 40 <= x <= 1160 and 40 <= y <= 660:
                pixels[y][x] = rgba(15, 23, 42, 255)
    for y in range(80, 260):
        for x in range(80, 1120):
            pixels[y][x] = rgba(30, 41, 59, 255)
    for y in range(300, 560):
        for x in range(80, 520):
            pixels[y][x] = rgba(15, 23, 42, 255)
    for y in range(300, 560):
        for x in range(560, 1120):
            pixels[y][x] = rgba(15, 23, 42, 255)
    write_png(path, w, h, pixels)


create_logo(ASSETS / 'logo.png')
create_banner(ASSETS / 'banner.png')
create_hero(ASSETS / 'hero-background.png')
create_screenshot(ASSETS / 'screenshots' / 'dashboard.png')
print('Generated assets')
