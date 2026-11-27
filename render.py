#!/usr/bin/env python3
"""Draw the v5 one-day digest for Thursday 26 November 2026.

v5 is a controlled experiment, not a new guess. v3 (98.60% provisional,
12-0, rank ~86) is the best entry so far; v4 (98.29%) changed BOTH the
content and the format and went backwards, so nobody knows which change
cost the margin. v5 holds v3's content fixed — the same 34 stories, the
same three leads, the same facts and the same date-check exclusions —
and only changes the format to v4's: taller lead scenes with big number
badges on them, grid cards with picture plus headline only, no separate
stat strip, a bigger map beside the also-list. If v5 beats v3, the format
was the win; if it does not, v3's denser page was the better trade.

Every number below comes from the v2 research brief (Reuters, BBC, AP,
FIDE, Bank of Korea). No story from 27 November is in here. All code and
all headlines are written fresh in this session.

Deterministic: Pillow only, no network, no clock, no randomness. Two
runs of this file write byte-identical PNGs.
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

PAPER = (248, 244, 233)
INK = (24, 24, 24)
MUTED = (98, 94, 84)
RED = (178, 30, 32)
NAVY = (22, 44, 76)
BORDER = (198, 191, 176)
SEA = (228, 233, 230)
LAND = (206, 201, 172)
GREEN = (28, 118, 56)
BLUE = (28, 76, 134)
GREY = (106, 112, 126)
GOLD = (214, 164, 40)

SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS_R = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"

_font_cache = {}


def get_font(path, size):
    key = (path, size)
    if key not in _font_cache:
        _font_cache[key] = ImageFont.truetype(path, size)
    return _font_cache[key]


def width_of(d, text, font):
    return d.textlength(text, font=font)


def split_lines(d, text, font, width):
    """Greedy wrap of text into lines no wider than width."""
    lines, current = [], ""
    for word in text.split():
        trial = word if not current else current + " " + word
        if width_of(d, trial, font) <= width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_lines(d, x, y, text, font, width, fill, spacing=None):
    if spacing is None:
        spacing = int(font.size * 1.2)
    for line in split_lines(d, text, font, width):
        d.text((x, y), line, font=font, fill=fill)
        y += spacing
    return y


def label_chip(d, x, y, text, bg, size=10, fg=(255, 255, 255)):
    """Small rounded label; returns its pixel width."""
    font = get_font(SANS_B, size)
    w = int(width_of(d, text, font)) + 12
    d.rounded_rectangle([x, y, x + w, y + size + 7], radius=3, fill=bg)
    d.text((x + 6, y + 3), text, font=font, fill=fg)
    return w


def status_tag(d, x, y, status):
    colours = {"CONFIRMED": GREEN, "OFFICIAL": BLUE, "REPORTED": GREY,
               "CLAIM": RED}
    return label_chip(d, x, y, status, colours[status], size=9)


def vgrad(d, x, y, w, h, top, bottom):
    """Vertical gradient in 12 flat bands."""
    for i in range(12):
        t = i / 11
        col = tuple(int(top[c] + (bottom[c] - top[c]) * t) for c in range(3))
        y0 = y + int(h * i / 12)
        y1 = y + int(h * (i + 1) / 12)
        d.rectangle([x, y0, x + w - 1, y1], fill=col)


# ------------------------------------------------------------------ stories
# Leads: (num, kicker, headline, body, source, status, region, scene key)
# Same 34 stories as v3, headlines reworded in this session.
LEADS = [
    (1, "NEW YORK · WEATHER",
     "Macy's 100th parade grounded by nor'easter",
     "900,000 homes lose power and 1,000+ flights are grounded. "
     "The parade moves to Saturday.",
     "AP · REUTERS", "CONFIRMED", "N. America", "storm"),
    (2, "MUMBAI · REMEMBRANCE",
     "India honours 26/11 dead, 18 years on",
     "Candles at the Gateway of India for the 166 killed in 2008, "
     "as the Constitution turns 77.",
     "PTI · PIB", "OFFICIAL", "S. Asia", "india"),
    (3, "BRUSSELS · DIPLOMACY",
     "EU summit stalls on €45bn loan for Kyiv",
     "No deal on the 2028–34 budget or the Ukraine loan; leaders "
     "meet again on 17–18 December.",
     "REUTERS · AP", "CONFIRMED", "Europe", "eu"),
]

# Grid: (num, kicker, headline, source, status, region, scene key)
GRID = [
    (4, "GENEVA · CHESS", "Gukesh, Sindarov share Game 3",
     "FIDE", "CONFIRMED", "Europe", "chess"),
    (5, "KUWAIT · CONFLICT", "Two Italians killed in Kuwait strike",
     "REUTERS · BBC", "CLAIM", "Middle East", "kuwait"),
    (6, "KYIV · WAR", "Russia fires 113 drones at Ukraine",
     "BBC · AP", "REPORTED", "Europe", "kyiv"),
    (7, "JAZAN · CONFLICT", "Houthi strike kills Jazan worker",
     "AL JAZEERA", "REPORTED", "Middle East", "jazan"),
    (8, "SEOUL · ECONOMY", "Korea lifts its rate to 3.25%",
     "BANK OF KOREA", "OFFICIAL", "E. Asia", "korea"),
    (9, "BANGKOK · DISASTER", "Bangkok refinery blast hurts nine",
     "AP · BBC", "CONFIRMED", "SE Asia", "bangkok"),
    (10, "GAZA CITY · WAR", "Israeli strikes kill Hamas officials",
     "FRANCE 24 · BBC", "REPORTED", "Middle East", "gaza"),
    (11, "FRANKFURT · ECONOMY", "De Cos chosen as next ECB chief",
     "REUTERS", "CONFIRMED", "Europe", "ecb"),
    (12, "WASHINGTON · SPACE", "FCC clears a million SpaceX satellites",
     "BBC · CNBC", "CONFIRMED", "N. America", "space"),
    (13, "DR CONGO · HEALTH", "Ebola passes 12,000 in DR Congo",
     "CDC · NPR", "REPORTED", "Africa", "ebola"),
]

# Also list: (num, headline, city, region)
ALSO = [
    (14, "Israeli prosecutors may drop Netanyahu bribery case", "Jerusalem",
     "Middle East"),
    (15, "Cairo tanker crash toll put at 31", "Cairo", "Africa"),
    (16, "Kim pledges more nuclear weapons", "Pyongyang", "E. Asia"),
    (17, "Huawei convicted of stealing US trade secrets", "Brooklyn",
     "N. America"),
    (18, "UK net migration down to 77,000", "London", "Europe"),
    (19, "UK–EU treaties carry 10-year exit clause", "London", "Europe"),
    (20, "Spain heads to polls Sunday; right ahead", "Madrid", "Europe"),
    (21, "Brazil recalls its ambassador from Argentina", "Brasília",
     "S. America"),
    (22, "Venezuela lifts ban on opposition figures", "Caracas",
     "S. America"),
    (23, "Myanmar rejects part of ICJ ruling", "Naypyidaw", "SE Asia"),
    (24, "Baghdad takes over Kurdistan oil", "Erbil", "Middle East"),
    (25, "Australia AI spending up 12.2%", "Canberra", "Oceania"),
    (26, "Hong Kong marks a year since the Tai Po fire", "Hong Kong",
     "E. Asia"),
    (27, "Nepal declares its flood missing dead", "Kathmandu", "S. Asia"),
    (28, "Bangladesh garment unrest shuts factories", "Dhaka", "S. Asia"),
    (29, "S. Africa court voids Ramaphosa report", "Cape Town", "Africa"),
    (30, "Guinea-Bissau vote pushed to 2028", "Bissau", "Africa"),
    (31, "Colombia frees 76 hostages from supermarket", "Cartagena",
     "S. America"),
    (32, "UK-sent refugee to Eswatini later died", "London", "Europe"),
    (33, "Poundland folds; 11,000 jobs at risk", "Walsall", "Europe"),
    (34, "US to host Copa América 2028", "Asunción", "S. America"),
]

TIMELINE = [
    ("00:00 UTC", "Thanksgiving begins in the US as the storm hits"),
    ("02:00 UTC", "Macy's parade move to Saturday announced"),
    ("06:00 UTC", "Delhi wakes to Constitution Day and 26/11 tributes"),
    ("07:45 UTC", "Bangkok refinery blast (14:45 local)"),
    ("14:00 UTC", "Chess Game 3 begins in Geneva (15:00 CET)"),
    ("15:00 UTC", "High-wind warning begins in New York"),
]

DATE_CHECK = [
    "US tariff plan — 25 Nov",
    "Shenzhou-24 docks — 25 Nov",
    "Huang back at Nvidia — 24 Nov",
    "Nasdaq sell-off — 25 Nov",
    "Miss Universe crowned — 24 Nov",
    "Banten factory fire — 24 Nov",
    "ICJ Myanmar ruling — 19 Nov",
    "Tai Po fire itself — 26 Nov '25",
]

REGION_ORDER = ["N. America", "S. America", "Europe", "Middle East",
                "Africa", "S. Asia", "E. Asia", "SE Asia", "Oceania"]
REGION_LABELS = {"N. America": "North America", "S. America": "South America",
                 "Europe": "Europe", "Middle East": "Middle East",
                 "Africa": "Africa", "S. Asia": "South Asia",
                 "E. Asia": "East Asia", "SE Asia": "SE Asia",
                 "Oceania": "Oceania"}
REGION_COLOURS = {"N. America": (30, 90, 140), "S. America": (170, 90, 50),
                  "Europe": (40, 90, 170), "Middle East": (200, 120, 40),
                  "Africa": (190, 140, 50), "S. Asia": (210, 110, 60),
                  "E. Asia": (170, 60, 60), "SE Asia": (70, 140, 90),
                  "Oceania": (110, 130, 90)}


def region_counts():
    counts = {r: 0 for r in REGION_ORDER}
    for story in LEADS:
        counts[story[6]] += 1
    for story in GRID:
        counts[story[5]] += 1
    for _n, _h, _c, region in ALSO:
        counts[region] += 1
    return counts


# Map pins: (story number, lon, lat, badge offset dx, dy)
PINS = [
    (1, -74.0, 40.7, 0, 0), (2, 72.8, 19.1, 0, 0),
    (3, 4.35, 50.85, -24, -16), (4, 6.14, 46.2, 22, -16),
    (5, 47.5, 29.3, 18, 12), (6, 30.5, 50.45, 0, 0),
    (7, 42.55, 16.9, 0, 0), (8, 127.0, 37.5, 0, 0),
    (9, 100.5, 13.75, 0, 0), (10, 34.45, 31.5, -16, 14),
    (11, 8.68, 50.1, 24, 12), (12, -77.0, 38.9, -20, 14),
    (13, 23.0, -2.5, 0, 0),
]


# ------------------------------------------------------------------- scenes
# Each scene draws its own picture in the given box; all geometry here is
# original to this file. Big numbers live as badges on the scenes (v4's
# format) instead of in a separate stat strip.


def scene_storm(d, x, y, w, h):
    vgrad(d, x, y, w, h, (30, 54, 96), (12, 24, 54))
    # skyline, lit windows
    base = y + h
    for bx, bw, bh in [(4, 44, 58), (54, 32, 84), (92, 38, 52),
                       (136, 30, 74), (172, 42, 56), (220, 34, 80),
                       (260, 44, 62)]:
        d.rectangle([x + bx, base - bh, x + bx + bw, base], fill=(8, 15, 34))
        for wy in range(base - bh + 8, base - 6, 13):
            for wx in range(x + bx + 6, x + bx + bw - 6, 11):
                d.rectangle([wx, wy, wx + 4, wy + 6], fill=(255, 212, 108))
    # rain
    for i in range(24):
        rx = x + (i * 53) % w
        ry = y + (i * 41) % h
        d.line([rx, ry, rx - 5, ry + 11], fill=(150, 175, 212), width=1)
    # parade balloon: white face, red nose, smile
    cx, cy = x + w // 2, y + 50
    d.ellipse([cx - 66, cy - 30, cx + 66, cy + 30], fill=(248, 246, 240))
    d.ellipse([cx - 11, cy - 7, cx - 3, cy + 3], fill=(24, 24, 24))
    d.ellipse([cx + 5, cy - 7, cx + 13, cy + 3], fill=(24, 24, 24))
    d.ellipse([cx - 6, cy + 5, cx + 8, cy + 15], fill=(178, 30, 32))
    d.arc([cx - 20, cy - 2, cx + 22, cy + 24], 20, 160, fill=(24, 24, 24),
          width=2)
    label_chip(d, x + 8, y + h - 26, "POSTPONED TO SATURDAY", RED, size=10)
    d.ellipse([x + w - 54, y + h - 50, x + w - 12, y + h - 8], fill=GOLD)
    d.text((x + w - 42, y + h - 42), "100", font=get_font(SANS_B, 16),
           fill=(24, 24, 24))


def scene_india(d, x, y, w, h):
    vgrad(d, x, y, w, h, (236, 176, 118), (222, 148, 88))
    d.rectangle([x, y + h - 32, x + w, y + h], fill=(198, 130, 76))
    # Gateway arch
    ax0, ax1 = x + w // 2 - 50, x + w // 2 + 50
    d.rectangle([ax0, y + 54, ax1, y + h - 32], fill=(148, 98, 54))
    d.pieslice([ax0 - 6, y + 10, ax1 + 6, y + 98], 180, 360,
               fill=(148, 98, 54))
    d.pieslice([ax0 + 26, y + 46, ax1 - 26, y + 120], 180, 360,
               fill=(216, 150, 90))
    d.rectangle([ax0 + 26, y + 82, ax1 - 26, y + h - 32], fill=(216, 150, 90))
    # row of diya flames
    for i in range(7):
        fx = x + 20 + i * 42
        d.rectangle([fx, y + h - 50, fx + 8, y + h - 32],
                    fill=(250, 244, 228))
        d.ellipse([fx + 1, y + h - 60, fx + 7, y + h - 48],
                  fill=(255, 190, 60))
    # flag on a pole
    fx = x + w - 50
    d.rectangle([fx, y + 18, fx + 3, y + 78], fill=(90, 70, 50))
    for i, col in enumerate([(255, 153, 51), (255, 255, 255), (19, 136, 8)]):
        d.rectangle([fx + 3, y + 18 + i * 10, fx + 40, y + 28 + i * 10],
                    fill=col)
    d.ellipse([fx + 16, y + 25, fx + 24, y + 33], fill=(0, 0, 128))
    label_chip(d, x + w - 94, y + 8, "18 YEARS", (24, 24, 24), size=10)


def scene_eu(d, x, y, w, h):
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=(16, 48, 104))
    cx, cy = x + w // 2, y + h // 2 - 4
    d.ellipse([cx - 92, cy - 42, cx + 92, cy + 42], outline=(232, 200, 90),
              width=6)
    for i in range(12):
        a = 2 * math.pi * i / 12 - math.pi / 2
        sx = cx + int(72 * math.cos(a))
        sy = cy + int(33 * math.sin(a))
        d.ellipse([sx - 4, sy - 4, sx + 4, sy + 4], fill=(255, 215, 0))
    d.text((cx - 26, cy - 10), "EU 27", font=get_font(SANS_B, 16),
           fill=(255, 255, 255))
    label_chip(d, x + 8, y + h - 26, "€45BN LOAN", (16, 48, 104), size=10)


def scene_chess(d, x, y, w, h):
    # Small box (grid card): compact board left, one clock and the GAME 3
    # badge right, score strip along the bottom.
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=(26, 68, 48))
    bx, by, sq = x + 12, y + 4, 14
    for r in range(4):
        for c in range(4):
            col = (234, 226, 202) if (r + c) % 2 == 0 else (52, 86, 68)
            d.rectangle([bx + c * sq, by + r * sq, bx + (c + 1) * sq - 1,
                         by + (r + 1) * sq - 1], fill=col)
    d.ellipse([bx + 4, by + 4, bx + 10, by + 10], fill=(24, 24, 24))
    d.ellipse([bx + 3 * sq + 4, by + 3 * sq + 4, bx + 3 * sq + 10,
               by + 3 * sq + 10], fill=(248, 246, 240),
              outline=(24, 24, 24), width=1)
    d.ellipse([bx + 2 * sq + 4, by + 4, bx + 2 * sq + 10, by + 10],
              fill=(248, 246, 240))
    cx = x + w - 80
    d.rectangle([cx, y + 30, cx + 36, y + 46], fill=(255, 255, 255))
    d.text((cx + 7, y + 33), "1:32", font=get_font(SANS_B, 10),
           fill=(20, 20, 20))
    d.rectangle([x, y + h - 18, x + w - 1, y + h - 1], fill=(18, 46, 34))
    d.text((x + 12, y + h - 15), "GUKESH 1–1 SINDAROV",
           font=get_font(SANS_B, 10), fill=(255, 255, 255))
    label_chip(d, x + w - 74, y + 8, "GAME 3", RED, size=10)


def scene_kuwait(d, x, y, w, h):
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=(14, 20, 42))
    d.ellipse([x + w - 46, y + 10, x + w - 16, y + 40],
              fill=(240, 230, 200))
    d.rectangle([x, y + h - 20, x + w, y + h - 1], fill=(64, 52, 38))
    d.rectangle([x + 34, y + h - 52, x + 38, y + h - 20], fill=(40, 40, 40))
    d.rectangle([x + 64, y + h - 42, x + 92, y + h - 20], fill=(60, 60, 60))
    ex, ey = x + w // 2 + 24, y + h - 30
    for r, col in [(15, (255, 118, 28)), (10, (255, 198, 62)),
                   (5, (255, 240, 170))]:
        d.ellipse([ex - r, ey - r, ex + r, ey + r], fill=col)
    label_chip(d, x + 8, y + 8, "2 KILLED", RED, size=10)


def scene_kyiv(d, x, y, w, h):
    vgrad(d, x, y, w, h, (12, 16, 36), (42, 54, 92))
    for i in range(12):
        sx = x + 10 + (i * 37) % (w - 20)
        sy = y + 8 + (i * 13) % 26
        d.ellipse([sx, sy, sx + 2, sy + 2], fill=(255, 255, 255))
    for dx, dy in [(34, 28), (94, 16), (152, 32)]:
        d.line([x + dx - 22, y + dy + 8, x + dx, y + dy],
               fill=(255, 180, 60), width=2)
        d.polygon([(x + dx, y + dy - 4), (x + dx + 16, y + dy),
                   (x + dx, y + dy + 4), (x + dx - 4, y + dy)],
                  fill=(10, 10, 14))
    for bx, by in [(62, 58), (142, 66)]:
        d.ellipse([x + bx - 8, y + by - 8, x + bx + 8, y + by + 8],
                  fill=(255, 200, 60))
        d.ellipse([x + bx - 3, y + by - 3, x + bx + 3, y + by + 3],
                  fill=(255, 255, 255))
    label_chip(d, x + 8, y + h - 26, "113 DRONES", RED, size=10)


def _refinery(d, x, y, w, h, flame):
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=(228, 216, 192))
    d.rectangle([x + 12, y + h - 50, x + w - 12, y + h - 10],
                fill=(92, 90, 86))
    for tx in (28, 76, 124):
        d.rectangle([x + tx, y + 20, x + tx + 12, y + h - 50],
                    fill=(72, 70, 66))
        d.ellipse([x + tx - 6, y + 8, x + tx + 18, y + 28],
                  fill=(152, 148, 140))
    if flame:
        fx, fy = x + w // 2, y + h - 50
        d.polygon([(fx - 14, fy), (fx, fy - 30), (fx + 14, fy)],
                  fill=(255, 140, 40))
        d.ellipse([fx - 8, fy - 14, fx + 8, fy + 2], fill=(255, 210, 80))


def scene_jazan(d, x, y, w, h):
    _refinery(d, x, y, w, h, flame=True)
    for sx, sy, sr in [(150, 22, 12), (168, 14, 15), (188, 24, 10)]:
        d.ellipse([x + sx - sr, y + sy - sr, x + sx + sr, y + sy + sr],
                  fill=(110, 104, 100))
    label_chip(d, x + 8, y + 8, "JAZAN", RED, size=10)


def scene_korea(d, x, y, w, h):
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=(236, 241, 245))
    base = y + h - 16
    for i, bh in enumerate([20, 30, 26, 40, 54]):
        bx = x + 16 + i * 32
        d.rectangle([bx, base - bh, bx + 22, base], fill=(28, 76, 134))
    d.line([x + 12, base - 58, x + w - 14, base - 68], fill=(28, 118, 56),
           width=3)
    d.polygon([(x + w - 28, base - 72), (x + w - 12, base - 68),
               (x + w - 28, base - 62)], fill=(28, 118, 56))
    label_chip(d, x + w - 60, y + h - 26, "3.25%", GREEN, size=10)


def scene_bangkok(d, x, y, w, h):
    vgrad(d, x, y, w, h, (72, 62, 92), (152, 112, 92))
    d.rectangle([x + 12, y + h - 42, x + w - 12, y + h - 12],
                fill=(42, 38, 42))
    for tx in (30, 70, 110, 150):
        d.rectangle([x + tx, y + h - 64, x + tx + 8, y + h - 42],
                    fill=(42, 38, 42))
    fx, fy = x + w // 2, y + h - 38
    for r, col in [(17, (255, 110, 20)), (11, (255, 190, 60)),
                   (6, (255, 240, 150))]:
        d.ellipse([fx - r, fy - r, fx + r, fy + r], fill=col)
    for sx, sy, sr in [(80, 16, 13), (100, 8, 16), (122, 18, 11)]:
        d.ellipse([x + sx - sr, y + sy - sr, x + sx + sr, y + sy + sr],
                  fill=(72, 66, 68))
    label_chip(d, x + 8, y + h - 26, "9 HURT", RED, size=10)


def scene_gaza(d, x, y, w, h):
    vgrad(d, x, y, w, h, (20, 20, 32), (62, 52, 72))
    d.ellipse([x + w - 44, y + 10, x + w - 18, y + 36],
              fill=(240, 220, 160))
    base = y + h - 14
    for bx, bw, bh in [(8, 26, 42), (40, 30, 58), (76, 24, 36),
                       (106, 30, 52), (142, 26, 40), (174, 24, 56)]:
        d.rectangle([x + bx, base - bh, x + bx + bw, base], fill=(18, 18, 26))
        for wy in range(base - bh + 8, base - 6, 11):
            for wx in range(x + bx + 5, x + bx + bw - 4, 9):
                d.rectangle([wx, wy, wx + 3, wy + 4], fill=(255, 200, 90))
    for sx, sy, sr in [(120, 26, 10), (132, 16, 13), (146, 26, 9)]:
        d.ellipse([x + sx - sr, y + sy - sr, x + sx + sr, y + sy + sr],
                  fill=(96, 90, 92))
    label_chip(d, x + 8, y + 8, "GAZA CITY", RED, size=10)


def scene_ecb(d, x, y, w, h):
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=(228, 234, 240))
    bx, by = x + w // 2 - 60, y + h - 54
    d.polygon([(bx - 10, by + 18), (bx + 62, by - 10), (bx + 134, by + 18)],
              fill=(92, 102, 118))
    d.rectangle([bx, by + 18, bx + 124, by + 26], fill=(72, 82, 98))
    for i in range(5):
        cx = bx + 8 + i * 24
        d.rectangle([cx, by + 26, cx + 10, by + 54], fill=(240, 244, 248))
    d.rectangle([bx, by + 54, bx + 124, by + 62], fill=(72, 82, 98))
    d.ellipse([bx + 52, by - 2, bx + 72, by + 18], fill=(255, 215, 0))
    d.text((bx + 58, by + 2), "€", font=get_font(SANS_B, 12),
           fill=(16, 48, 104))
    label_chip(d, x + 8, y + 8, "NEXT ECB CHIEF", (16, 48, 104), size=10)


def scene_space(d, x, y, w, h):
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=(8, 12, 28))
    for i in range(20):
        sx = x + 8 + (i * 41) % (w - 16)
        sy = y + 6 + (i * 19) % (h - 38)
        d.ellipse([sx, sy, sx + 2, sy + 2], fill=(255, 255, 255))
    cx, cy = x + w // 2, y + h // 2 + 4
    d.ellipse([cx - 62, cy - 20, cx + 62, cy + 20],
              outline=(120, 160, 220), width=2)
    for sx, sy in [(-52, -8), (0, -20), (52, -6), (-24, 14), (30, 16)]:
        d.rectangle([cx + sx - 5, cy + sy - 3, cx + sx + 5, cy + sy + 3],
                    fill=(200, 210, 230), outline=(255, 255, 255))
        d.line([cx + sx + 5, cy + sy, cx + sx + 12, cy + sy],
               fill=(200, 210, 230), width=2)
    label_chip(d, x + 8, y + h - 26, "1M SATELLITES", (16, 48, 104),
               size=10)


def scene_ebola(d, x, y, w, h):
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=(96, 22, 22))
    for vx, vy, vr in [(30, 24, 9), (70, 16, 6), (120, 30, 8),
                       (160, 18, 6), (50, 58, 7), (110, 62, 9),
                       (160, 56, 6)]:
        d.ellipse([x + vx - vr, y + vy - vr, x + vx + vr, y + vy + vr],
                  fill=(200, 60, 60), outline=(255, 150, 150), width=1)
        for a in range(6):
            ang = 2 * math.pi * a / 6
            ex = x + vx + int((vr + 4) * math.cos(ang))
            ey = y + vy + int((vr + 4) * math.sin(ang))
            d.ellipse([ex - 1, ey - 1, ex + 1, ey + 1], fill=(255, 150, 150))
    d.text((x + 12, y + h - 34), "12,021", font=get_font(SANS_B, 22),
           fill=(255, 255, 255))
    label_chip(d, x + w - 74, y + 8, "12,021 CASES", RED, size=10)


SCENES = {
    "storm": scene_storm, "india": scene_india, "eu": scene_eu,
    "chess": scene_chess, "kuwait": scene_kuwait, "kyiv": scene_kyiv,
    "jazan": scene_jazan, "korea": scene_korea, "bangkok": scene_bangkok,
    "gaza": scene_gaza, "ecb": scene_ecb, "space": scene_space,
    "ebola": scene_ebola,
}


# ---------------------------------------------------------------------- map
# Coarse continent outlines (lon/lat), drawn by hand for this page.
NORTH_AMERICA = [(-168, 66), (-150, 70), (-135, 68), (-125, 71), (-110, 68),
                 (-95, 69), (-85, 66), (-80, 73), (-70, 62), (-60, 55),
                 (-65, 45), (-75, 35), (-80, 32), (-85, 29), (-90, 21),
                 (-97, 16), (-94, 17), (-86, 13), (-80, 9), (-85, 11),
                 (-95, 16), (-105, 20), (-115, 28), (-125, 40), (-125, 49),
                 (-135, 58), (-150, 60), (-165, 60)]
GREENLAND = [(-55, 60), (-43, 60), (-32, 68), (-22, 70), (-30, 76),
             (-50, 76), (-58, 70)]
SOUTH_AMERICA = [(-80, 9), (-72, 11), (-62, 10), (-55, 6), (-50, 0),
                 (-40, -5), (-35, -9), (-40, -20), (-48, -28), (-55, -35),
                 (-62, -41), (-68, -50), (-70, -54), (-73, -44), (-72, -30),
                 (-70, -18), (-77, -12), (-80, -5), (-81, 1)]
EUROPE = [(-10, 36), (-9, 43), (-2, 48), (2, 51), (8, 57), (10, 59),
          (18, 56), (21, 55), (28, 60), (30, 62), (24, 65), (18, 69),
          (12, 70), (6, 62), (0, 58), (-5, 50), (-10, 44)]
AFRICA = [(-17, 15), (-15, 21), (-10, 31), (-5, 35), (10, 37), (20, 32),
          (30, 31), (35, 28), (40, 20), (43, 12), (51, 11), (48, 2),
          (41, -5), (40, -15), (35, -25), (32, -29), (25, -34), (18, -35),
          (15, -27), (12, -18), (9, -1), (9, 4), (-8, 5), (-13, 8)]
ASIA = [(30, 36), (36, 36), (42, 39), (48, 30), (54, 26), (60, 25),
        (66, 25), (72, 20), (76, 10), (80, 7), (80, 13), (85, 19),
        (89, 22), (92, 16), (98, 10), (100, 7), (104, 2), (104, 8),
        (108, 12), (109, 14), (106, 20), (110, 20), (114, 22), (118, 25),
        (121, 28), (122, 31), (120, 34), (122, 38), (127, 40), (130, 42),
        (135, 44), (138, 46), (142, 50), (142, 59), (150, 60), (156, 52),
        (158, 56), (162, 60), (170, 66), (178, 65), (170, 60), (160, 62),
        (155, 68), (145, 72), (135, 72), (125, 73), (115, 74), (105, 76),
        (95, 76), (85, 74), (75, 73), (65, 72), (55, 70), (45, 68),
        (40, 67), (35, 66), (30, 60), (28, 55), (30, 50), (32, 45),
        (30, 42)]
AUSTRALIA = [(113, -22), (114, -30), (115, -35), (120, -34), (125, -32),
             (130, -32), (135, -35), (140, -38), (145, -38), (150, -37),
             (150, -30), (146, -19), (142, -11), (137, -12), (135, -15),
             (132, -12), (130, -13), (126, -14), (122, -17), (118, -20)]
CONTINENTS = [NORTH_AMERICA, GREENLAND, SOUTH_AMERICA, EUROPE, AFRICA,
              ASIA, AUSTRALIA]


def draw_map(d, mx, my, mw, mh):
    d.rectangle([mx, my, mx + mw - 1, my + mh - 1], fill=SEA,
                outline=BORDER, width=1)
    d.text((mx + 8, my + 5), "WHERE IT HAPPENED — PINS 1–13",
           font=get_font(SANS_B, 11), fill=INK)
    ox, oy = mx + 6, my + 20
    iw, ih = mw - 12, mh - 26

    def proj(lon, lat):
        return (ox + (lon + 170) / 360.0 * iw,
                oy + (78 - lat) / 136.0 * ih)

    for poly in CONTINENTS:
        d.polygon([proj(lon, lat) for lon, lat in poly], fill=LAND)
    for lon, lat, r in [(-2, 54, 3), (138, 38, 3), (172, -41, 3)]:
        px, py = proj(lon, lat)
        d.ellipse([px - r, py - r, px + r, py + r], fill=LAND)
    nf = get_font(SANS_B, 9)
    for num, lon, lat, dx, dy in PINS:
        px, py = proj(lon, lat)
        qx, qy = px + dx, py + dy
        if dx or dy:
            d.line([px, py, qx, qy], fill=RED, width=1)
        d.ellipse([qx - 3, qy - 3, qx + 3, qy + 3], fill=RED)
        d.ellipse([qx - 8, qy - 8, qx + 8, qy + 8], fill=RED,
                  outline=(255, 255, 255), width=1)
        s = str(num)
        d.text((qx - width_of(d, s, nf) / 2, qy - 6), s, font=nf,
               fill=(255, 255, 255))


# -------------------------------------------------------------------- layout
M = 22
CW = W - 2 * M  # 980


def draw_card_frame(d, x, y, w, h, number):
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=(255, 255, 255),
                outline=BORDER, width=1)
    d.ellipse([x + 6, y + 6, x + 26, y + 26], fill=RED)
    f = get_font(SANS_B, 11)
    s = str(number)
    d.text((x + 16 - width_of(d, s, f) / 2, y + 9), s, font=f,
           fill=(255, 255, 255))


def draw_source_line(d, x, y, w, source, status):
    f = get_font(SANS_R, 9)
    bf = get_font(SANS_B, 9)
    tag_w = int(width_of(d, status, bf)) + 12
    label = "SOURCE: " + source
    while width_of(d, label, f) > w - tag_w - 4 and len(label) > 8:
        label = label[:-1]
    d.text((x, y), label, font=f, fill=MUTED)
    status_tag(d, x + w - tag_w, y - 2, status)


def draw_lead(d, x, y, w, h, story):
    num, kicker, headline, body, source, status, _reg, scene = story
    draw_card_frame(d, x, y, w, h, num)
    SCENES[scene](d, x + 1, y + 1, w - 2, 142)
    ty = y + 148
    d.text((x + 10, ty), kicker, font=get_font(SANS_B, 10), fill=RED)
    ty += 15
    ty = draw_lines(d, x + 10, ty, headline, get_font(SERIF_B, 20), w - 20,
                    INK, spacing=23)
    ty = draw_lines(d, x + 10, ty, body, get_font(SERIF_R, 12), w - 20,
                    (60, 58, 52), spacing=15)
    foot_y = max(ty + 2, y + h - 20)
    draw_source_line(d, x + 10, foot_y, w - 20, source, status)


def draw_grid_card(d, x, y, w, h, story):
    # v4 format: scene + headline + source/pill only, no kicker line —
    # the kicker pushed the source line out of the card.
    num, _kicker, headline, source, status, _reg, scene = story
    draw_card_frame(d, x, y, w, h, num)
    SCENES[scene](d, x + 1, y + 1, w - 2, 78)
    ty = y + 82
    ty = draw_lines(d, x + 8, ty, headline, get_font(SANS_B, 13), w - 16,
                    INK, spacing=16)
    foot_y = max(ty + 2, y + h - 16)
    draw_source_line(d, x + 8, foot_y, w - 16, source, status)


def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead
    title = "THE WORLD IN ONE DAY"
    tf = get_font(SERIF_B, 56)
    d.text(((W - width_of(d, title, tf)) / 2, 8), title, font=tf, fill=INK)
    d.rectangle([M, 76, W - M, 78], fill=INK)
    date = "THURSDAY 26 NOVEMBER 2026"
    df = get_font(SANS_B, 19)
    d.text(((W - width_of(d, date, df)) / 2, 84), date, font=df, fill=INK)
    sub = ("A nor'easter grounds New York's 100th Thanksgiving parade, "
           "India marks 18 years since the 26/11 Mumbai attacks, and "
           "Brussels deadlocks over a €45bn loan for Kyiv.")
    draw_lines(d, (W - 900) / 2, 108, sub, get_font(SERIF_I, 14), 900, INK,
               spacing=17)

    # ---- stat boxes: 34 stories, 9 regions, sources/fields (v3's counts)
    boxes = [("34", "STORIES"), ("9", "REGIONS"),
             ("20 SOURCES · 14 FIELDS", "")]
    bw = (CW - 14) // 3
    y = 142
    for i, (big, small) in enumerate(boxes):
        bx = M + i * (bw + 7)
        d.rectangle([bx, y, bx + bw - 1, y + 27], outline=INK, width=1,
                    fill=(255, 255, 255))
        lf = get_font(SANS_B, 17)
        if small:
            label = big + " " + small
            lx = bx + (bw - width_of(d, label, lf)) / 2
            d.text((lx, y + 5), label, font=lf, fill=INK)
            d.text((lx, y + 5), big + " ", font=lf, fill=RED)
        else:
            d.text((bx + (bw - width_of(d, big, lf)) / 2, y + 5), big,
                   font=lf, fill=INK)

    # ---- region bar
    counts = region_counts()
    y = 176
    x = M
    for region in REGION_ORDER:
        w = int(CW * counts[region] / 34)
        d.rectangle([x, y, x + w - 1, y + 7], fill=REGION_COLOURS[region])
        x += w
    labels = "  ·  ".join("%s %d" % (REGION_LABELS[r], counts[r])
                          for r in REGION_ORDER)
    lf = get_font(SANS_R, 11)
    d.text(((W - width_of(d, labels, lf)) / 2, 188), labels, font=lf,
           fill=MUTED)

    # ---- three leads
    lw = (CW - 20) // 3
    y0 = 202
    for i, story in enumerate(LEADS):
        draw_lead(d, M + i * (lw + 10), y0, lw, 264, story)

    # ---- ten grid cards, 5 x 2
    gw = (CW - 40) // 5
    for row in range(2):
        gy = 466 + row * 134
        for col in range(5):
            story = GRID[row * 5 + col]
            draw_grid_card(d, M + col * (gw + 10), gy, gw, 134, story)

    # ---- timeline
    y = 736
    d.text((M, y), "THE DAY IN UTC", font=get_font(SANS_B, 13), fill=INK)
    d.line([M + 130, y + 8, W - M, y + 8], fill=BORDER, width=1)
    for i, (t, txt) in enumerate(TIMELINE):
        tx = M + (i % 3) * 330
        ty = 754 + (i // 3) * 16
        d.text((tx, ty), t, font=get_font(SANS_B, 11), fill=BLUE)
        d.text((tx + 74, ty), txt, font=get_font(SANS_R, 11), fill=INK)

    # ---- bottom: map left, ALSO list right
    d.line([M, 794, W - M, 794], fill=INK, width=2)
    draw_map(d, M, 800, 330, 148)
    ax = M + 330 + 16
    aw = W - M - ax
    d.text((ax, 800), "AND ALSO — STORIES 14–34",
           font=get_font(SANS_B, 12), fill=INK)
    col_w = (aw - 14) // 2
    af = get_font(SANS_R, 10)
    for i, (num, head, city, _reg) in enumerate(ALSO):
        cx = ax + (i // 11) * (col_w + 14)
        cy = 818 + (i % 11) * 11
        d.text((cx, cy), "%d." % num, font=get_font(SANS_B, 10), fill=RED)
        item = "%s — %s" % (head, city)
        if width_of(d, item, af) > col_w - 20:
            item = head
        d.text((cx + 20, cy), item, font=af, fill=INK)

    # ---- date check box: 8 items, 4 columns x 2 rows
    y = 954
    d.rectangle([M, y, W - M, y + 40], outline=RED, width=1,
                fill=(255, 255, 255))
    d.text((M + 8, y + 3), "DATE CHECK — THESE ARE NOT 26 NOVEMBER",
           font=get_font(SANS_B, 11), fill=RED)
    df2 = get_font(SANS_R, 9)
    for i, item in enumerate(DATE_CHECK[:4]):
        d.text((M + 8 + i * 245, y + 16), "× " + item, font=df2, fill=INK)
    for i, item in enumerate(DATE_CHECK[4:]):
        d.text((M + 8 + i * 245, y + 28), "× " + item, font=df2, fill=INK)

    # ---- footer
    d.text((M, 998),
           "Every story here happened or was first reported on Thursday "
           "26 November 2026. Sources are named on each story.",
           font=get_font(SERIF_I, 10), fill=MUTED)
    d.text((M, 1009),
           "HOW SURE: OFFICIAL = government or institution · CONFIRMED = "
           "2+ outlets · REPORTED = one outlet · CLAIM = one side's word "
           "only. Scenes are drawn illustrations, not photographs.",
           font=get_font(SANS_R, 9), fill=MUTED)

    img.save(OUT, format="PNG", optimize=True)
    return OUT


if __name__ == "__main__":
    path = render()
    print("wrote", path, os.path.getsize(path), "bytes")
