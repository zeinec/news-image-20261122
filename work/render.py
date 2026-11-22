#!/usr/bin/env python3
"""Draw GLOBAL HERALD, Sunday 22 November 2026 — one-page vintage colour
front page, 1024x1024. Everything is drawn from scratch with Pillow
primitives and real typeset text, so every letter stays legible.

Stories are the day's news as first reported 22 November 2026 (see the
README for sources). Lead: Iran's IRGC claims missile and drone strikes
on two US Patriot radars at bases in Bahrain.
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "entry.png")

W, H = 1024, 1024
PAPER = (246, 239, 217)
PANEL = (238, 229, 200)
INK = (25, 23, 19)
RED = (176, 42, 32)
NAVY = (31, 58, 95)
NAVY_DARK = (22, 40, 66)
TEAL = (15, 110, 110)
GREEN = (46, 110, 58)
SLATE = (70, 80, 95)
MAROON = (128, 32, 48)
ORANGE = (196, 96, 20)
GOLD = (184, 134, 30)
GOLD_LT = (226, 178, 80)
SEA = (214, 228, 232)
LAND = (185, 198, 155)
LAND_EDGE = (125, 143, 95)
RULE = (201, 191, 165)
GRID = (216, 207, 175)

FDIR = "/usr/share/fonts/truetype/noto/"
FALLBACK = "/usr/share/fonts/truetype/dejavu/"


def load_font(name, size):
    for base in (FDIR, FALLBACK):
        try:
            return ImageFont.truetype(base + name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def serif_black(s):
    return load_font("NotoSerif-Black.ttf", s)


def serif_bold(s):
    return load_font("NotoSerif-Bold.ttf", s)


def serif(s):
    return load_font("NotoSerif-Regular.ttf", s)


def serif_it(s):
    return load_font("NotoSerif-Italic.ttf", s)


def sans_bold(s):
    return load_font("NotoSans-Bold.ttf", s)


def sans(s):
    return load_font("NotoSans-Regular.ttf", s)


def wrap_text(draw, text, font, width):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=font) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def centred(draw, cx, y, text, font, fill=INK):
    draw.text((cx - draw.textlength(text, font=font) / 2, y), text,
              font=font, fill=fill)


def draw_star(draw, cx, cy, r, fill):
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    draw.polygon(pts, fill=fill, outline=(255, 255, 255))


def lonlat(lon, lat):
    x = 40 + (lon + 170) * 944 / 360
    y = 560 + (75 - lat) * 160 / 130
    return (x, y)


CONTINENTS = {
    "north_america": [(-166, 68), (-150, 70), (-135, 69), (-125, 71),
                      (-110, 68), (-95, 69), (-85, 66), (-80, 73),
                      (-76, 62), (-65, 60), (-60, 55), (-55, 47),
                      (-60, 44), (-65, 44), (-70, 42), (-75, 35),
                      (-80, 32), (-81, 26), (-84, 30), (-89, 29),
                      (-91, 19), (-95, 18), (-97, 16), (-92, 15),
                      (-86, 12), (-83, 9), (-79, 8), (-83, 9),
                      (-88, 14), (-92, 15), (-97, 18), (-105, 20),
                      (-110, 23), (-114, 28), (-120, 34), (-124, 40),
                      (-124, 48), (-130, 55), (-140, 60), (-150, 61),
                      (-158, 58), (-162, 55), (-166, 60)],
    "south_america": [(-79, 9), (-75, 10), (-72, 11), (-64, 10),
                      (-60, 8), (-55, 6), (-52, 4), (-50, 0),
                      (-44, -3), (-38, -5), (-35, -8), (-38, -15),
                      (-40, -22), (-46, -28), (-52, -33), (-58, -38),
                      (-62, -41), (-66, -47), (-68, -52), (-70, -54),
                      (-73, -50), (-74, -44), (-73, -37), (-72, -30),
                      (-73, -22), (-75, -15), (-78, -8), (-80, -4),
                      (-81, 1), (-80, 6)],
    "africa": [(-6, 35), (-10, 31), (-15, 27), (-17, 21), (-17, 15),
               (-15, 11), (-12, 8), (-8, 4), (-4, 5), (2, 6), (6, 4),
               (9, 4), (12, -1), (13, -5), (12, -10), (13, -15),
               (12, -18), (15, -22), (16, -28), (19, -33), (26, -34),
               (32, -28), (35, -24), (36, -20), (40, -16), (40, -10),
               (42, -4), (44, -1), (48, 2), (51, 11), (44, 11),
               (40, 15), (38, 18), (35, 22), (32, 28), (30, 31),
               (25, 32), (20, 32), (15, 32), (10, 34), (5, 37), (0, 36)],
    "europe": [(-10, 36), (-9, 38), (-9, 43), (-2, 44), (-4, 48),
               (-2, 49), (0, 51), (3, 53), (5, 53), (8, 55), (8, 57),
               (10, 59), (12, 58), (18, 56), (21, 55), (24, 58),
               (21, 60), (18, 62), (12, 64), (10, 66), (14, 68),
               (18, 69), (25, 71), (30, 70), (32, 68), (35, 66),
               (40, 64), (44, 62), (46, 58), (44, 55), (40, 52),
               (38, 48), (36, 45), (34, 44), (30, 46), (28, 45),
               (26, 42), (24, 40), (22, 38), (20, 40), (18, 40),
               (15, 38), (12, 38), (10, 37), (8, 39), (3, 42),
               (0, 40), (-2, 37), (-6, 36)],
    "asia": [(32, 36), (36, 36), (40, 38), (44, 39), (48, 41), (52, 44),
             (56, 46), (60, 48), (66, 50), (72, 52), (78, 54), (84, 56),
             (90, 58), (96, 60), (102, 62), (108, 64), (114, 66),
             (120, 68), (126, 70), (132, 71), (138, 72), (144, 71),
             (150, 70), (156, 69), (162, 68), (170, 67), (178, 66),
             (180, 65), (172, 64), (164, 60), (158, 56), (156, 52),
             (150, 50), (145, 45), (142, 42), (140, 39), (138, 36),
             (136, 34), (134, 32), (132, 30), (130, 28), (128, 26),
             (126, 24), (124, 22), (122, 20), (120, 18), (118, 16),
             (116, 14), (114, 12), (112, 10), (110, 8), (108, 10),
             (106, 12), (104, 10), (102, 8), (100, 6), (98, 8),
             (96, 10), (94, 14), (92, 16), (90, 18), (88, 20),
             (86, 20), (84, 18), (82, 16), (80, 14), (78, 12),
             (76, 10), (74, 12), (72, 16), (70, 18), (68, 20),
             (66, 22), (64, 24), (62, 26), (60, 28), (58, 30),
             (56, 32), (54, 34), (52, 36), (50, 38), (48, 36),
             (46, 34), (44, 32), (42, 30), (40, 28), (38, 26),
             (36, 24), (34, 28), (32, 30), (34, 32)],
    "australia": [(114, -22), (118, -20), (122, -18), (126, -14),
                  (130, -12), (135, -12), (140, -17), (142, -11),
                  (146, -14), (150, -20), (153, -24), (150, -28),
                  (146, -32), (142, -35), (138, -35), (134, -33),
                  (130, -32), (126, -32), (122, -34), (118, -35),
                  (114, -32), (113, -26)],
}

ISLANDS = {
    "uk": [(-3, 53), (-1, 54), (0, 56), (1, 58), (0, 57), (-2, 54),
           (-4, 52), (-5, 51), (-4, 53)],
    "japan": [(130, 31), (132, 33), (135, 35), (137, 36), (139, 38),
              (141, 40), (141, 42), (140, 44), (142, 44), (143, 42),
              (141, 39), (139, 37), (137, 35), (134, 34), (131, 32)],
    "new_zealand": [(167, -45), (170, -42), (173, -40), (176, -38),
                    (174, -41), (171, -44), (168, -46)],
}

# (number, lon, lat, colour, label) — 1 is the lead story, starred.
PINS = [
    (1, 50.5, 26.2, RED, "BAHRAIN"),
    (2, 106.8, -6.2, TEAL, "JAKARTA"),
    (3, 22.0, 51.0, NAVY, "LVIV"),
    (4, 33.0, 35.0, MAROON, "ANTALYA"),
    (5, -74.0, 40.7, ORANGE, "NEW YORK"),
    (6, 96.2, 19.8, GREEN, "NAYPYIDAW"),
    (7, 114.2, 22.3, GOLD, "HONG KONG"),
]

# (number, kicker, headline, deck, colour)
CARDS = [
    (2, "JAKARTA  •  BRUSSELS", "A DEAL A DECADE IN THE MAKING",
     "EU and Indonesia sign a pact; 98.5% of tariffs to go.", TEAL),
    (3, "LVIV  •  UKRAINE", "MISSILES HIT LVIV",
     "Russian strike kills two and injures ten.", NAVY),
    (4, "ANTALYA  •  TURKEY", "CLIMATE TALKS RUN OVER",
     "Fossil-fuel and finance rows stall the deal.", MAROON),
    (5, "NEW YORK  •  MARKETS", "TECH ROUT DEEPENS",
     "Wall Street slide spreads; Asian shares fall.", ORANGE),
    (6, "NAYPYIDAW  •  MYANMAR", "QUAKE JOLTS MYANMAR",
     "Magnitude 4.1 tremor shakes the early hours.", GREEN),
    (7, "HONG KONG  •  CHINA", "HONG KONG GOES TO POLLS",
     "5,700 voters choose the Election Committee.", GOLD),
]


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- outer double border --------------------------------------------
    d.rectangle([14, 14, W - 15, H - 15], outline=INK, width=2)
    d.rectangle([20, 20, W - 21, H - 21], outline=RULE, width=1)

    # ---- masthead ---------------------------------------------------------
    centred(d, 512, 30, "T H E   W O R L D   I N   O N E   P A G E",
            sans_bold(15), fill=SLATE)
    d.line([90, 56, 300, 56], fill=RULE, width=1)
    d.line([724, 56, 934, 56], fill=RULE, width=1)
    centred(d, 512, 54, "GLOBAL HERALD", serif_black(82))
    centred(d, 512, 150,
            "SUNDAY,  22 NOVEMBER 2026    •    IN FULL COLOUR    •    FREE",
            sans_bold(17))
    d.line([28, 182, 996, 182], fill=INK, width=4)
    d.line([28, 188, 996, 188], fill=INK, width=1)

    # ---- lead story -------------------------------------------------------
    d.text((28, 202), "BAHRAIN  •  THE GULF", font=sans_bold(20), fill=RED)
    d.text((28, 228), "IRAN STRIKES", font=serif_black(64), fill=INK)
    d.text((28, 296), "U.S. BASES", font=serif_black(64), fill=INK)
    d.line([28, 372, 120, 372], fill=RED, width=4)
    deck = ("Tehran claims its missiles and drones hit two American "
            "Patriot radars.")
    for i, ln in enumerate(wrap_text(d, deck, serif_it(24), 596)):
        d.text((28, 384 + i * 30), ln, font=serif_it(24), fill=INK)
    body = ("The Revolutionary Guard said its aerospace force struck the "
            "al-Riffa and Awali bases in retaliation for US drone flights. "
            "Bahrain called it a heinous aggression.")
    for i, ln in enumerate(wrap_text(d, body, serif(19), 596)):
        d.text((28, 446 + i * 25), ln, font=serif(19), fill=INK)

    # ---- lead illustration: radar night over the Gulf ----------------------
    d.rectangle([648, 202, 996, 512], fill=NAVY)
    d.rectangle([648, 202, 996, 236], fill=RED)
    centred(d, 822, 210, "IRGC CLAIMS: PATRIOT RADARS HIT",
            sans_bold(15), fill=(255, 255, 255))
    cx, cy = 822, 340
    for r in (46, 78, 110):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=GOLD_LT,
                  width=2)
    d.line([cx, cy, cx + 92, cy - 62], fill=GOLD_LT, width=2)
    for sx, sy, ex, ey in ((680, 260, 800, 320), (700, 300, 810, 340),
                           (960, 270, 850, 330)):
        d.line([sx, sy, ex, ey], fill=(255, 255, 255), width=3)
        d.ellipse([ex - 4, ey - 4, ex + 4, ey + 4], fill=RED)
    for sx, sy in ((700, 280), (760, 260), (900, 260), (940, 320),
                   (680, 360), (960, 380)):
        d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 255, 255))
    d.rectangle([648, 440, 996, 512], fill=NAVY_DARK)
    for dome_x, label in ((730, "AL-RIFFA"), (880, "AWALI")):
        d.pieslice([dome_x - 42, 440, dome_x + 42, 524], 180, 360,
                   fill=(16, 28, 48), outline=GOLD_LT, width=2)
        d.line([dome_x, 440, dome_x, 398], fill=GOLD_LT, width=2)
        d.ellipse([dome_x - 3, 395, dome_x + 3, 401], fill=RED)
        centred(d, dome_x, 482, label, sans_bold(13), fill=GOLD_LT)

    # ---- map band ----------------------------------------------------------
    d.text((28, 528), "THE WORLD TODAY", font=sans_bold(18), fill=NAVY)
    d.line([28, 550, 996, 550], fill=INK, width=2)
    d.rectangle([28, 556, 996, 720], fill=SEA)
    for lon in (-150, -120, -90, -60, -30, 0, 30, 60, 90, 120, 150):
        x, _ = lonlat(lon, 75)
        d.line([x, 556, x, 720], fill=GRID, width=1)
    for lat in (60, 30, 0, -30):
        _, y = lonlat(0, lat)
        d.line([28, y, 996, y], fill=GRID, width=1)
    for pts in list(CONTINENTS.values()) + list(ISLANDS.values()):
        d.polygon([lonlat(lon, lat) for lon, lat in pts], fill=LAND,
                  outline=LAND_EDGE)
    for lon, lat in ((100, 0), (110, -5), (120, -8), (130, -3)):
        x, y = lonlat(lon, lat)
        d.ellipse([x - 4, y - 2, x + 4, y + 2], fill=LAND,
                  outline=LAND_EDGE)
    for num, lon, lat, colour, _label in PINS:
        x, y = lonlat(lon, lat)
        if num == 1:
            draw_star(d, x, y, 16, RED)
        else:
            d.ellipse([x - 11, y - 11, x + 11, y + 11], fill=colour,
                      outline=(255, 255, 255), width=2)
            centred(d, x, y - 8, str(num), sans_bold(13),
                    fill=(255, 255, 255))
    centred(d, 512, 728,
            "1 BAHRAIN *    •    2 JAKARTA    •    3 LVIV    •    "
            "4 ANTALYA    •    5 NEW YORK    •    6 NAYPYIDAW    •    "
            "7 HONG KONG", sans_bold(13), fill=SLATE)

    # ---- six story cards ---------------------------------------------------
    for idx, (num, kicker, headline, deck, colour) in enumerate(CARDS):
        col = idx % 3
        row = idx // 3
        x = 28 + col * 328
        y = 750 + row * 118
        d.rectangle([x, y, x + 26, y + 26], fill=colour)
        centred(d, x + 13, y + 4, str(num), sans_bold(15),
                fill=(255, 255, 255))
        d.text((x + 34, y + 4), kicker, font=sans_bold(14), fill=colour)
        for i, ln in enumerate(wrap_text(d, headline, serif_bold(20), 312)):
            d.text((x, y + 30 + i * 24), ln, font=serif_bold(20), fill=INK)
        for i, ln in enumerate(wrap_text(d, deck, sans(13), 312)):
            d.text((x, y + 78 + i * 17), ln, font=sans(13), fill=INK)

    # ---- footer ------------------------------------------------------------
    centred(d, 512, 988,
            "GLOBAL HERALD  •  Sunday 22 November 2026  •  Seven stories, "
            "one page", sans_bold(13), fill=SLATE)

    img.save(OUT, optimize=True)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
