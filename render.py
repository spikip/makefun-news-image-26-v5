"""Paint the v5 digest of Thursday 26 November 2026 in one picture.

The idea behind v5 is to change one thing at a time. v3 scored 98.60%
provisional and v4 scored 98.29%, but v4 changed the stories and the
layout together, so the experiment could not say which change cost the
points. v5 therefore keeps v3's stories exactly — the same 34 items,
the same three leading stories, the same figures and the same list of
things that are not 26 November — and only borrows v4's page design:
taller pictures on the three lead cards with big figures stamped on
them, grid cards that show a picture and a headline and nothing else,
no separate strip of statistics, and a larger map next to the list of
the remaining stories. Whichever of v3 and v5 the judge prefers, the
difference will be the design alone.

All figures come from the research notes behind v2 (Reuters, BBC, AP,
FIDE, the Bank of Korea). Nothing from 27 November appears. The code
below was written from scratch in this session.

Only Pillow is used. There is no network, no clock and no randomness,
so running this file twice writes the same PNG bytes twice.
"""
import math as _m

from pathlib import Path
from PIL import Image as _Img, ImageDraw as _Draw, ImageFont as _Font

PAGE_W, PAGE_H = 1024, 1024
OUT_PATH = str(Path(__file__).resolve().parent / "entry.png")
MARGIN = 22
PAGE_INNER = PAGE_W - 2 * MARGIN

SHEET = (0xF8, 0xF4, 0xE9)
SOOT = (0x18, 0x18, 0x18)
FADED = (0x62, 0x5E, 0x54)
SCARLET = (0xB2, 0x1E, 0x20)
DEEPNAVY = (0x16, 0x2C, 0x4C)
EDGE = (0xC6, 0xBF, 0xB0)
OCEAN = (0xE4, 0xE9, 0xE6)
GROUND = (0xCE, 0xC9, 0xAC)
LEAF = (0x1C, 0x76, 0x38)
SKYBLUE = (0x1C, 0x4C, 0x86)
STONE = (0x6A, 0x70, 0x7E)
AMBER = (0xD6, 0xA4, 0x28)
PAPERWHITE = (0xFF, 0xFF, 0xFF)

FONT_DIR = "/usr/share/fonts/truetype/liberation"
FB_SERIF = FONT_DIR + "/LiberationSerif-Bold.ttf"
FR_SERIF = FONT_DIR + "/LiberationSerif-Regular.ttf"
FI_SERIF = FONT_DIR + "/LiberationSerif-Italic.ttf"
FR_SANS = FONT_DIR + "/LiberationSans-Regular.ttf"
FB_SANS = FONT_DIR + "/LiberationSans-Bold.ttf"

_FONTS = {}


def font_for(path, size):
    key = (path, size)
    if key not in _FONTS:
        _FONTS[key] = _Font.truetype(path, size)
    return _FONTS[key]


def text_w(pen, word, font):
    return pen.textlength(word, font=font)


def wrap(pen, word, font, width):
    """Split word greedily into lines that fit inside width."""
    out, cur = [], ""
    for piece in word.split():
        trial = piece if not cur else cur + " " + piece
        if text_w(pen, trial, font) <= width:
            cur = trial
        else:
            if cur:
                out.append(cur)
            cur = piece
    if cur:
        out.append(cur)
    return out


def put_lines(pen, x, y, word, font, width, fill, spacing=None):
    if spacing is None:
        spacing = int(font.size * 1.2)
    for row in wrap(pen, word, font, width):
        pen.text((x, y), row, font=font, fill=fill)
        y += spacing
    return y


def badge(pen, x, y, word, bg, size=10, fg=(255, 255, 255)):
    """A small rounded tag; hands back how wide it came out."""
    ft = font_for(FB_SANS, size)
    bw = int(text_w(pen, word, ft)) + 12
    pen.rounded_rectangle([x, y, x + bw, y + size + 7], radius=3, fill=bg)
    pen.text((x + 6, y + 3), word, font=ft, fill=fg)
    return bw


def flag(pen, x, y, state):
    paint = {"CONFIRMED": LEAF, "OFFICIAL": SKYBLUE, "REPORTED": STONE,
             "CLAIM": SCARLET}
    return badge(pen, x, y, state, paint[state], size=9)


def fade_down(pen, x, y, w, h, top, bottom):
    """A top-to-bottom blend drawn as twelve flat stripes."""
    for k in range(12):
        frac = k / 11
        shade = tuple(int(top[c] + (bottom[c] - top[c]) * frac)
                      for c in range(3))
        top_y = y + int(h * k / 12)
        bot_y = y + int(h * (k + 1) / 12)
        pen.rectangle([x, top_y, x + w - 1, bot_y], fill=shade)


# ------------------------------------------------------------------ stories
# Three lead stories. Each entry carries its number, kicker, headline,
# body, sources, confidence flag, region code and picture key. The
# stories and figures are v3's; the headline wording was refreshed here.
LEADS = [
    {"n": 1, "tag": "NEW YORK · WEATHER",
     "head": "Macy's 100th parade grounded by nor'easter",
     "body": "900,000 homes lose power and 1,000+ flights are grounded. "
             "The parade moves to Saturday.",
     "src": "AP · REUTERS", "flag": "CONFIRMED", "zone": "NA",
     "art": "storm"},
    {"n": 2, "tag": "MUMBAI · REMEMBRANCE",
     "head": "India honours 26/11 dead, 18 years on",
     "body": "Candles at the Gateway of India for the 166 killed in 2008, "
             "as the Constitution turns 77.",
     "src": "PTI · PIB", "flag": "OFFICIAL", "zone": "SAS",
     "art": "india"},
    {"n": 3, "tag": "BRUSSELS · DIPLOMACY",
     "head": "EU summit stalls on €45bn loan for Kyiv",
     "body": "No deal on the 2028–34 budget or the Ukraine loan; leaders "
             "meet again on 17–18 December.",
     "src": "REUTERS · AP", "flag": "CONFIRMED", "zone": "EU",
     "art": "eu"},
]

# Ten grid cards: number, kicker, headline, sources, flag, region, art.
GRID = [
    {"n": 4, "tag": "GENEVA · CHESS",
     "head": "Gukesh, Sindarov share Game 3",
     "src": "FIDE", "flag": "CONFIRMED", "zone": "EU", "art": "chess"},
    {"n": 5, "tag": "KUWAIT · CONFLICT",
     "head": "Two Italians killed in Kuwait strike",
     "src": "REUTERS · BBC", "flag": "CLAIM", "zone": "ME",
     "art": "kuwait"},
    {"n": 6, "tag": "KYIV · WAR",
     "head": "Russia fires 113 drones at Ukraine",
     "src": "BBC · AP", "flag": "REPORTED", "zone": "EU", "art": "kyiv"},
    {"n": 7, "tag": "JAZAN · CONFLICT",
     "head": "Houthi strike kills Jazan worker",
     "src": "AL JAZEERA", "flag": "REPORTED", "zone": "ME",
     "art": "jazan"},
    {"n": 8, "tag": "SEOUL · ECONOMY",
     "head": "Korea lifts its rate to 3.25%",
     "src": "BANK OF KOREA", "flag": "OFFICIAL", "zone": "EA",
     "art": "korea"},
    {"n": 9, "tag": "BANGKOK · DISASTER",
     "head": "Bangkok refinery blast hurts nine",
     "src": "AP · BBC", "flag": "CONFIRMED", "zone": "SEA",
     "art": "bangkok"},
    {"n": 10, "tag": "GAZA CITY · WAR",
     "head": "Israeli strikes kill Hamas officials",
     "src": "FRANCE 24 · BBC", "flag": "REPORTED", "zone": "ME",
     "art": "gaza"},
    {"n": 11, "tag": "FRANKFURT · ECONOMY",
     "head": "De Cos chosen as next ECB chief",
     "src": "REUTERS", "flag": "CONFIRMED", "zone": "EU", "art": "ecb"},
    {"n": 12, "tag": "WASHINGTON · SPACE",
     "head": "FCC clears a million SpaceX satellites",
     "src": "BBC · CNBC", "flag": "CONFIRMED", "zone": "NA",
     "art": "space"},
    {"n": 13, "tag": "DR CONGO · HEALTH",
     "head": "Ebola passes 12,000 in DR Congo",
     "src": "CDC · NPR", "flag": "REPORTED", "zone": "AF",
     "art": "ebola"},
]

# The remaining stories, 14–34: number, headline, city, region code.
ALSO = [
    {"n": 14, "head": "Israeli prosecutors may drop Netanyahu bribery case",
     "city": "Jerusalem", "zone": "ME"},
    {"n": 15, "head": "Cairo tanker crash toll put at 31",
     "city": "Cairo", "zone": "AF"},
    {"n": 16, "head": "Kim pledges more nuclear weapons",
     "city": "Pyongyang", "zone": "EA"},
    {"n": 17, "head": "Huawei convicted of stealing US trade secrets",
     "city": "Brooklyn", "zone": "NA"},
    {"n": 18, "head": "UK net migration down to 77,000",
     "city": "London", "zone": "EU"},
    {"n": 19, "head": "UK–EU treaties carry 10-year exit clause",
     "city": "London", "zone": "EU"},
    {"n": 20, "head": "Spain heads to polls Sunday; right ahead",
     "city": "Madrid", "zone": "EU"},
    {"n": 21, "head": "Brazil recalls its ambassador from Argentina",
     "city": "Brasília", "zone": "SA"},
    {"n": 22, "head": "Venezuela lifts ban on opposition figures",
     "city": "Caracas", "zone": "SA"},
    {"n": 23, "head": "Myanmar rejects part of ICJ ruling",
     "city": "Naypyidaw", "zone": "SEA"},
    {"n": 24, "head": "Baghdad takes over Kurdistan oil",
     "city": "Erbil", "zone": "ME"},
    {"n": 25, "head": "Australia AI spending up 12.2%",
     "city": "Canberra", "zone": "OC"},
    {"n": 26, "head": "Hong Kong marks a year since the Tai Po fire",
     "city": "Hong Kong", "zone": "EA"},
    {"n": 27, "head": "Nepal declares its flood missing dead",
     "city": "Kathmandu", "zone": "SAS"},
    {"n": 28, "head": "Bangladesh garment unrest shuts factories",
     "city": "Dhaka", "zone": "SAS"},
    {"n": 29, "head": "S. Africa court voids Ramaphosa report",
     "city": "Cape Town", "zone": "AF"},
    {"n": 30, "head": "Guinea-Bissau vote pushed to 2028",
     "city": "Bissau", "zone": "AF"},
    {"n": 31, "head": "Colombia frees 76 hostages from supermarket",
     "city": "Cartagena", "zone": "SA"},
    {"n": 32, "head": "UK-sent refugee to Eswatini later died",
     "city": "London", "zone": "EU"},
    {"n": 33, "head": "Poundland folds; 11,000 jobs at risk",
     "city": "Walsall", "zone": "EU"},
    {"n": 34, "head": "US to host Copa América 2028",
     "city": "Asunción", "zone": "SA"},
]

TIMELINE = [
    {"at": "00:00 UTC",
     "what": "Thanksgiving begins in the US as the storm hits"},
    {"at": "02:00 UTC", "what": "Macy's parade move to Saturday announced"},
    {"at": "06:00 UTC",
     "what": "Delhi wakes to Constitution Day and 26/11 tributes"},
    {"at": "07:45 UTC", "what": "Bangkok refinery blast (14:45 local)"},
    {"at": "14:00 UTC", "what": "Chess Game 3 begins in Geneva (15:00 CET)"},
    {"at": "15:00 UTC", "what": "High-wind warning begins in New York"},
]

DATE_CHECK = ("US tariff plan — 25 Nov|Shenzhou-24 docks — 25 Nov|"
              "Huang back at Nvidia — 24 Nov|Nasdaq sell-off — 25 Nov|"
              "Miss Universe crowned — 24 Nov|Banten factory fire — 24 Nov|"
              "ICJ Myanmar ruling — 19 Nov|Tai Po fire itself — 26 Nov '25"
              ).split("|")

ZONES = ["NA", "SA", "EU", "ME", "AF", "SAS", "EA", "SEA", "OC"]
ZONE_NAMES = {"NA": "North America", "SA": "South America",
              "EU": "Europe", "ME": "Middle East",
              "AF": "Africa", "SAS": "South Asia",
              "EA": "East Asia", "SEA": "SE Asia",
              "OC": "Oceania"}
ZONE_PAINT = {"NA": (0x1E, 0x5A, 0x8C), "SA": (0xAA, 0x5A, 0x32),
              "EU": (0x28, 0x5A, 0xAA), "ME": (0xC8, 0x78, 0x28),
              "AF": (0xBE, 0x8C, 0x32), "SAS": (0xD2, 0x6E, 0x3C),
              "EA": (0xAA, 0x3C, 0x3C), "SEA": (0x46, 0x8C, 0x5A),
              "OC": (0x6E, 0x82, 0x5A)}


def zone_tally():
    tally = {z: 0 for z in ZONES}
    for item in LEADS + GRID:
        tally[item["zone"]] += 1
    for item in ALSO:
        tally[item["zone"]] += 1
    return tally


# Map pins: story number, longitude, latitude, leader-line offset.
PINS = [
    {"n": 1, "lon": -74.0, "lat": 40.7, "dx": 0, "dy": 0},
    {"n": 2, "lon": 72.8, "lat": 19.1, "dx": 0, "dy": 0},
    {"n": 3, "lon": 4.35, "lat": 50.85, "dx": -24, "dy": -16},
    {"n": 4, "lon": 6.14, "lat": 46.2, "dx": 22, "dy": -16},
    {"n": 5, "lon": 47.5, "lat": 29.3, "dx": 18, "dy": 12},
    {"n": 6, "lon": 30.5, "lat": 50.45, "dx": 0, "dy": 0},
    {"n": 7, "lon": 42.55, "lat": 16.9, "dx": 0, "dy": 0},
    {"n": 8, "lon": 127.0, "lat": 37.5, "dx": 0, "dy": 0},
    {"n": 9, "lon": 100.5, "lat": 13.75, "dx": 0, "dy": 0},
    {"n": 10, "lon": 34.45, "lat": 31.5, "dx": -16, "dy": 14},
    {"n": 11, "lon": 8.68, "lat": 50.1, "dx": 24, "dy": 12},
    {"n": 12, "lon": -77.0, "lat": 38.9, "dx": -20, "dy": 14},
    {"n": 13, "lon": 23.0, "lat": -2.5, "dx": 0, "dy": 0},
]


def _pts(spec):
    """Turn "lon,lat lon,lat ..." into a list of (lon, lat) pairs."""
    pairs = []
    for chunk in spec.split():
        lon, lat = chunk.split(",")
        pairs.append((int(lon), int(lat)))
    return pairs


# Rough continent outlines (longitude, latitude), sketched by hand.
NORTH_AMERICA = _pts("-168,66 -150,70 -135,68 -125,71 -110,68 -95,69 "
                     "-85,66 -80,73 -70,62 -60,55 -65,45 -75,35 -80,32 "
                     "-85,29 -90,21 -97,16 -94,17 -86,13 -80,9 -85,11 "
                     "-95,16 -105,20 -115,28 -125,40 -125,49 -135,58 "
                     "-150,60 -165,60")
GREENLAND = _pts("-55,60 -43,60 -32,68 -22,70 -30,76 -50,76 -58,70")
SOUTH_AMERICA = _pts("-80,9 -72,11 -62,10 -55,6 -50,0 -40,-5 -35,-9 "
                     "-40,-20 -48,-28 -55,-35 -62,-41 -68,-50 -70,-54 "
                     "-73,-44 -72,-30 -70,-18 -77,-12 -80,-5 -81,1")
EUROPE = _pts("-10,36 -9,43 -2,48 2,51 8,57 10,59 18,56 21,55 28,60 "
              "30,62 24,65 18,69 12,70 6,62 0,58 -5,50 -10,44")
AFRICA = _pts("-17,15 -15,21 -10,31 -5,35 10,37 20,32 30,31 35,28 40,20 "
              "43,12 51,11 48,2 41,-5 40,-15 35,-25 32,-29 25,-34 18,-35 "
              "15,-27 12,-18 9,-1 9,4 -8,5 -13,8")
ASIA = _pts("30,36 36,36 42,39 48,30 54,26 60,25 66,25 72,20 76,10 80,7 "
            "80,13 85,19 89,22 92,16 98,10 100,7 104,2 104,8 108,12 109,14 "
            "106,20 110,20 114,22 118,25 121,28 122,31 120,34 122,38 127,40 "
            "130,42 135,44 138,46 142,50 142,59 150,60 156,52 158,56 162,60 "
            "170,66 178,65 170,60 160,62 155,68 145,72 135,72 125,73 115,74 "
            "105,76 95,76 85,74 75,73 65,72 55,70 45,68 40,67 35,66 30,60 "
            "28,55 30,50 32,45 30,42")
AUSTRALIA = _pts("113,-22 114,-30 115,-35 120,-34 125,-32 130,-32 135,-35 "
                 "140,-38 145,-38 150,-37 150,-30 146,-19 142,-11 137,-12 "
                 "135,-15 132,-12 130,-13 126,-14 122,-17 118,-20")
LAND_MASSES = (NORTH_AMERICA, GREENLAND, SOUTH_AMERICA, EUROPE, AFRICA,
               ASIA, AUSTRALIA)

# ------------------------------------------------------------------- scenes
# Every picture below draws itself inside the box it is handed. The big
# figures live as tags stamped on the pictures (v4's style) instead of
# in a separate strip of statistics.


def paint_storm(pen, x, y, w, h):
    fade_down(pen, x, y, w, h, (0x1E, 0x36, 0x60), (0x0C, 0x18, 0x36))
    # city skyline with lit windows
    floor = y + h
    for ox, ow, oh in [(4, 44, 58), (54, 32, 84), (92, 38, 52),
                       (136, 30, 74), (172, 42, 56), (220, 34, 80),
                       (260, 44, 62)]:
        pen.rectangle([x + ox, floor - oh, x + ox + ow, floor],
                      fill=(0x08, 0x0F, 0x22))
        for wy in range(floor - oh + 8, floor - 6, 13):
            for wx in range(x + ox + 6, x + ox + ow - 6, 11):
                pen.rectangle([wx, wy, wx + 4, wy + 6],
                              fill=(0xFF, 0xD4, 0x6C))
    # rain, slanting left
    for k in range(24):
        rx = x + (k * 53) % w
        ry = y + (k * 41) % h
        pen.line([rx, ry, rx - 5, ry + 11], fill=(0x96, 0xAF, 0xD4),
                 width=1)
    # parade balloon: pale face, dark eyes, red nose, smile
    mid_x, mid_y = x + w // 2, y + 50
    pen.ellipse([mid_x - 66, mid_y - 30, mid_x + 66, mid_y + 30],
                fill=(0xF8, 0xF6, 0xF0))
    pen.ellipse([mid_x - 11, mid_y - 7, mid_x - 3, mid_y + 3], fill=SOOT)
    pen.ellipse([mid_x + 5, mid_y - 7, mid_x + 13, mid_y + 3], fill=SOOT)
    pen.ellipse([mid_x - 6, mid_y + 5, mid_x + 8, mid_y + 15],
                fill=SCARLET)
    pen.arc([mid_x - 20, mid_y - 2, mid_x + 22, mid_y + 24], 20, 160,
            fill=SOOT, width=2)
    badge(pen, x + 8, y + h - 26, "POSTPONED TO SATURDAY", SCARLET,
          size=10)
    pen.ellipse([x + w - 54, y + h - 50, x + w - 12, y + h - 8],
                fill=AMBER)
    pen.text((x + w - 42, y + h - 42), "100", font=font_for(FB_SANS, 16),
             fill=SOOT)


def paint_india(pen, x, y, w, h):
    fade_down(pen, x, y, w, h, (0xEC, 0xB0, 0x76), (0xDE, 0x94, 0x58))
    pen.rectangle([x, y + h - 32, x + w, y + h], fill=(0xC6, 0x82, 0x4C))
    # the Gateway arch
    al, ar = x + w // 2 - 50, x + w // 2 + 50
    pen.rectangle([al, y + 54, ar, y + h - 32], fill=(0x94, 0x62, 0x36))
    pen.pieslice([al - 6, y + 10, ar + 6, y + 98], 180, 360,
                 fill=(0x94, 0x62, 0x36))
    pen.pieslice([al + 26, y + 46, ar - 26, y + 120], 180, 360,
                 fill=(0xD8, 0x96, 0x5A))
    pen.rectangle([al + 26, y + 82, ar - 26, y + h - 32],
                  fill=(0xD8, 0x96, 0x5A))
    # a row of small oil lamps
    for k in range(7):
        fx = x + 20 + k * 42
        pen.rectangle([fx, y + h - 50, fx + 8, y + h - 32],
                      fill=(0xFA, 0xF4, 0xE4))
        pen.ellipse([fx + 1, y + h - 60, fx + 7, y + h - 48],
                    fill=(0xFF, 0xBE, 0x3C))
    # flag on its pole
    px = x + w - 50
    pen.rectangle([px, y + 18, px + 3, y + 78], fill=(0x5A, 0x46, 0x32))
    for k, col in enumerate([(0xFF, 0x99, 0x33), (0xFF, 0xFF, 0xFF),
                             (0x13, 0x88, 0x08)]):
        pen.rectangle([px + 3, y + 18 + k * 10, px + 40, y + 28 + k * 10],
                      fill=col)
    pen.ellipse([px + 16, y + 25, px + 24, y + 33], fill=(0x00, 0x00, 0x80))
    badge(pen, x + w - 94, y + 8, "18 YEARS", SOOT, size=10)


def paint_eu(pen, x, y, w, h):
    pen.rectangle([x, y, x + w - 1, y + h - 1], fill=(0x10, 0x30, 0x68))
    cx, cy = x + w // 2, y + h // 2 - 4
    pen.ellipse([cx - 92, cy - 42, cx + 92, cy + 42],
                outline=(0xE8, 0xC8, 0x5A), width=6)
    for k in range(12):
        ang = 2 * _m.pi * k / 12 - _m.pi / 2
        sx = cx + int(72 * _m.cos(ang))
        sy = cy + int(33 * _m.sin(ang))
        pen.ellipse([sx - 4, sy - 4, sx + 4, sy + 4], fill=(0xFF, 0xD7, 0x00))
    pen.text((cx - 26, cy - 10), "EU 27", font=font_for(FB_SANS, 16),
             fill=PAPERWHITE)
    badge(pen, x + 8, y + h - 26, "€45BN LOAN", (0x10, 0x30, 0x68),
          size=10)


def paint_chess(pen, x, y, w, h):
    # Compact board on the left, one clock and the GAME 3 tag on the
    # right, the score running along the bottom edge.
    pen.rectangle([x, y, x + w - 1, y + h - 1], fill=(0x1A, 0x44, 0x30))
    bx0, by0, cell = x + 12, y + 4, 14
    for rr in range(4):
        for cc in range(4):
            col = (0xEA, 0xE2, 0xCA) if (rr + cc) % 2 == 0 else (0x34, 0x56, 0x44)
            pen.rectangle([bx0 + cc * cell, by0 + rr * cell,
                           bx0 + (cc + 1) * cell - 1,
                           by0 + (rr + 1) * cell - 1], fill=col)
    pen.ellipse([bx0 + 4, by0 + 4, bx0 + 10, by0 + 10], fill=SOOT)
    pen.ellipse([bx0 + 3 * cell + 4, by0 + 3 * cell + 4,
                 bx0 + 3 * cell + 10, by0 + 3 * cell + 10],
                fill=(0xF8, 0xF6, 0xF0), outline=SOOT, width=1)
    pen.ellipse([bx0 + 2 * cell + 4, by0 + 4, bx0 + 2 * cell + 10,
                 by0 + 10], fill=(0xF8, 0xF6, 0xF0))
    clock_x = x + w - 80
    pen.rectangle([clock_x, y + 30, clock_x + 36, y + 46],
                  fill=PAPERWHITE)
    pen.text((clock_x + 7, y + 33), "1:32", font=font_for(FB_SANS, 10),
             fill=(0x14, 0x14, 0x14))
    pen.rectangle([x, y + h - 18, x + w - 1, y + h - 1],
                  fill=(0x12, 0x2E, 0x22))
    pen.text((x + 12, y + h - 15), "GUKESH 1–1 SINDAROV",
             font=font_for(FB_SANS, 10), fill=PAPERWHITE)
    badge(pen, x + w - 74, y + 8, "GAME 3", SCARLET, size=10)


def paint_kuwait(pen, x, y, w, h):
    pen.rectangle([x, y, x + w - 1, y + h - 1], fill=(0x0E, 0x14, 0x2A))
    pen.ellipse([x + w - 46, y + 10, x + w - 16, y + 40],
                fill=(0xF0, 0xE6, 0xC8))
    pen.rectangle([x, y + h - 20, x + w, y + h - 1], fill=(0x40, 0x34, 0x26))
    pen.rectangle([x + 34, y + h - 52, x + 38, y + h - 20],
                  fill=(0x28, 0x28, 0x28))
    pen.rectangle([x + 64, y + h - 42, x + 92, y + h - 20],
                  fill=(0x3C, 0x3C, 0x3C))
    fx, fy = x + w // 2 + 24, y + h - 30
    for rad, col in [(15, (0xFF, 0x76, 0x1C)), (10, (0xFF, 0xC6, 0x3E)),
                     (5, (0xFF, 0xF0, 0xAA))]:
        pen.ellipse([fx - rad, fy - rad, fx + rad, fy + rad], fill=col)
    badge(pen, x + 8, y + 8, "2 KILLED", SCARLET, size=10)


def paint_kyiv(pen, x, y, w, h):
    fade_down(pen, x, y, w, h, (0x0C, 0x10, 0x24), (0x2A, 0x36, 0x5C))
    for k in range(12):
        sx = x + 10 + (k * 37) % (w - 20)
        sy = y + 8 + (k * 13) % 26
        pen.ellipse([sx, sy, sx + 2, sy + 2], fill=PAPERWHITE)
    for ox, oy in [(34, 28), (94, 16), (152, 32)]:
        pen.line([x + ox - 22, y + oy + 8, x + ox, y + oy],
                 fill=(0xFF, 0xB4, 0x3C), width=2)
        pen.polygon([(x + ox, y + oy - 4), (x + ox + 16, y + oy),
                     (x + ox, y + oy + 4), (x + ox - 4, y + oy)],
                    fill=(0x0A, 0x0A, 0x0E))
    for px, py in [(62, 58), (142, 66)]:
        pen.ellipse([x + px - 8, y + py - 8, x + px + 8, y + py + 8],
                    fill=(0xFF, 0xC8, 0x3C))
        pen.ellipse([x + px - 3, y + py - 3, x + px + 3, y + py + 3],
                    fill=PAPERWHITE)
    badge(pen, x + 8, y + h - 26, "113 DRONES", SCARLET, size=10)

def _plant(pen, x, y, w, h, lit):
    pen.rectangle([x, y, x + w - 1, y + h - 1], fill=(0xE4, 0xD8, 0xC0))
    pen.rectangle([x + 12, y + h - 50, x + w - 12, y + h - 10],
                  fill=(0x5C, 0x5A, 0x56))
    for tx in (28, 76, 124):
        pen.rectangle([x + tx, y + 20, x + tx + 12, y + h - 50],
                      fill=(0x48, 0x46, 0x42))
        pen.ellipse([x + tx - 6, y + 8, x + tx + 18, y + 28],
                    fill=(0x98, 0x94, 0x8C))
    if lit:
        fx, fy = x + w // 2, y + h - 50
        pen.polygon([(fx - 14, fy), (fx, fy - 30), (fx + 14, fy)],
                    fill=(0xFF, 0x8C, 0x28))
        pen.ellipse([fx - 8, fy - 14, fx + 8, fy + 2],
                    fill=(0xFF, 0xD2, 0x50))


def paint_jazan(pen, x, y, w, h):
    _plant(pen, x, y, w, h, lit=True)
    for px, py, pr in [(150, 22, 12), (168, 14, 15), (188, 24, 10)]:
        pen.ellipse([x + px - pr, y + py - pr, x + px + pr, y + py + pr],
                    fill=(0x6E, 0x68, 0x64))
    badge(pen, x + 8, y + 8, "JAZAN", SCARLET, size=10)


def paint_korea(pen, x, y, w, h):
    pen.rectangle([x, y, x + w - 1, y + h - 1], fill=(0xEC, 0xF1, 0xF5))
    floor = y + h - 16
    for k, bh in enumerate([20, 30, 26, 40, 54]):
        bx = x + 16 + k * 32
        pen.rectangle([bx, floor - bh, bx + 22, floor], fill=SKYBLUE)
    pen.line([x + 12, floor - 58, x + w - 14, floor - 68], fill=LEAF,
             width=3)
    pen.polygon([(x + w - 28, floor - 72), (x + w - 12, floor - 68),
                 (x + w - 28, floor - 62)], fill=LEAF)
    badge(pen, x + w - 60, y + h - 26, "3.25%", LEAF, size=10)


def paint_bangkok(pen, x, y, w, h):
    fade_down(pen, x, y, w, h, (0x48, 0x3E, 0x5C), (0x98, 0x70, 0x5C))
    pen.rectangle([x + 12, y + h - 42, x + w - 12, y + h - 12],
                  fill=(0x2A, 0x26, 0x2A))
    for px in (30, 70, 110, 150):
        pen.rectangle([x + px, y + h - 64, x + px + 8, y + h - 42],
                      fill=(0x2A, 0x26, 0x2A))
    fx, fy = x + w // 2, y + h - 38
    for rad, col in [(17, (0xFF, 0x6E, 0x14)), (11, (0xFF, 0xBE, 0x3C)),
                     (6, (0xFF, 0xF0, 0x96))]:
        pen.ellipse([fx - rad, fy - rad, fx + rad, fy + rad], fill=col)
    for px, py, pr in [(80, 16, 13), (100, 8, 16), (122, 18, 11)]:
        pen.ellipse([x + px - pr, y + py - pr, x + px + pr, y + py + pr],
                    fill=(0x48, 0x42, 0x44))
    badge(pen, x + 8, y + h - 26, "9 HURT", SCARLET, size=10)


def paint_gaza(pen, x, y, w, h):
    fade_down(pen, x, y, w, h, (0x14, 0x14, 0x20), (0x3E, 0x34, 0x48))
    pen.ellipse([x + w - 44, y + 10, x + w - 18, y + 36],
                fill=(0xF0, 0xDC, 0xA0))
    floor = y + h - 14
    for ox, ow, oh in [(8, 26, 42), (40, 30, 58), (76, 24, 36),
                       (106, 30, 52), (142, 26, 40), (174, 24, 56)]:
        pen.rectangle([x + ox, floor - oh, x + ox + ow, floor],
                      fill=(0x12, 0x12, 0x1A))
        for wy in range(floor - oh + 8, floor - 6, 11):
            for wx in range(x + ox + 5, x + ox + ow - 4, 9):
                pen.rectangle([wx, wy, wx + 3, wy + 4],
                              fill=(0xFF, 0xC8, 0x5A))
    for px, py, pr in [(120, 26, 10), (132, 16, 13), (146, 26, 9)]:
        pen.ellipse([x + px - pr, y + py - pr, x + px + pr, y + py + pr],
                    fill=(0x60, 0x5A, 0x5C))
    badge(pen, x + 8, y + 8, "GAZA CITY", SCARLET, size=10)


def paint_ecb(pen, x, y, w, h):
    pen.rectangle([x, y, x + w - 1, y + h - 1], fill=(0xE4, 0xEA, 0xF0))
    hx, hy = x + w // 2 - 60, y + h - 54
    pen.polygon([(hx - 10, hy + 18), (hx + 62, hy - 10),
                 (hx + 134, hy + 18)], fill=(0x5C, 0x66, 0x76))
    pen.rectangle([hx, hy + 18, hx + 124, hy + 26], fill=(0x48, 0x52, 0x62))
    for k in range(5):
        cx = hx + 8 + k * 24
        pen.rectangle([cx, hy + 26, cx + 10, hy + 54],
                      fill=(0xF0, 0xF4, 0xF8))
    pen.rectangle([hx, hy + 54, hx + 124, hy + 62], fill=(0x48, 0x52, 0x62))
    pen.ellipse([hx + 52, hy - 2, hx + 72, hy + 18], fill=(0xFF, 0xD7, 0x00))
    pen.text((hx + 58, hy + 2), "€", font=font_for(FB_SANS, 12),
             fill=(0x10, 0x30, 0x68))
    badge(pen, x + 8, y + 8, "NEXT ECB CHIEF", (0x10, 0x30, 0x68),
          size=10)


def paint_space(pen, x, y, w, h):
    pen.rectangle([x, y, x + w - 1, y + h - 1], fill=(0x08, 0x0C, 0x1C))
    for k in range(20):
        sx = x + 8 + (k * 41) % (w - 16)
        sy = y + 6 + (k * 19) % (h - 38)
        pen.ellipse([sx, sy, sx + 2, sy + 2], fill=PAPERWHITE)
    cx, cy = x + w // 2, y + h // 2 + 4
    pen.ellipse([cx - 62, cy - 20, cx + 62, cy + 20],
                outline=(0x78, 0xA0, 0xDC), width=2)
    for ox, oy in [(-52, -8), (0, -20), (52, -6), (-24, 14), (30, 16)]:
        pen.rectangle([cx + ox - 5, cy + oy - 3, cx + ox + 5, cy + oy + 3],
                      fill=(0xC8, 0xD2, 0xE6), outline=PAPERWHITE)
        pen.line([cx + ox + 5, cy + oy, cx + ox + 12, cy + oy],
                 fill=(0xC8, 0xD2, 0xE6), width=2)
    badge(pen, x + 8, y + h - 26, "1M SATELLITES", (0x10, 0x30, 0x68),
          size=10)


def paint_ebola(pen, x, y, w, h):
    pen.rectangle([x, y, x + w - 1, y + h - 1], fill=(0x60, 0x16, 0x16))
    for px, py, pr in [(30, 24, 9), (70, 16, 6), (120, 30, 8),
                       (160, 18, 6), (50, 58, 7), (110, 62, 9),
                       (160, 56, 6)]:
        pen.ellipse([x + px - pr, y + py - pr, x + px + pr, y + py + pr],
                    fill=(0xC8, 0x3C, 0x3C), outline=(0xFF, 0x96, 0x96),
                    width=1)
        for k in range(6):
            ang = 2 * _m.pi * k / 6
            ex = x + px + int((pr + 4) * _m.cos(ang))
            ey = y + py + int((pr + 4) * _m.sin(ang))
            pen.ellipse([ex - 1, ey - 1, ex + 1, ey + 1],
                        fill=(0xFF, 0x96, 0x96))
    pen.text((x + 12, y + h - 34), "12,021", font=font_for(FB_SANS, 22),
             fill=PAPERWHITE)
    badge(pen, x + w - 74, y + 8, "12,021 CASES", SCARLET, size=10)


ARTWORK = {
    "storm": paint_storm, "india": paint_india, "eu": paint_eu,
    "chess": paint_chess, "kuwait": paint_kuwait, "kyiv": paint_kyiv,
    "jazan": paint_jazan, "korea": paint_korea, "bangkok": paint_bangkok,
    "gaza": paint_gaza, "ecb": paint_ecb, "space": paint_space,
    "ebola": paint_ebola,
}

# ---------------------------------------------------------------------- map

def paint_map(pen, mx, my, mw, mh):
    pen.rectangle([mx, my, mx + mw - 1, my + mh - 1], fill=OCEAN,
                  outline=EDGE, width=1)
    pen.text((mx + 8, my + 5), "WHERE IT HAPPENED — PINS 1–13",
             font=font_for(FB_SANS, 11), fill=SOOT)
    ox0, oy0 = mx + 6, my + 20
    inner_w, inner_h = mw - 12, mh - 26

    def _to_xy(lon, lat):
        return (ox0 + (lon + 170) / 360.0 * inner_w,
                oy0 + (78 - lat) / 136.0 * inner_h)

    for shape in LAND_MASSES:
        pen.polygon([_to_xy(lon, lat) for lon, lat in shape], fill=GROUND)
    for lon, lat, rad in [(-2, 54, 3), (138, 38, 3), (172, -41, 3)]:
        qx, qy = _to_xy(lon, lat)
        pen.ellipse([qx - rad, qy - rad, qx + rad, qy + rad], fill=GROUND)
    nf = font_for(FB_SANS, 9)
    for pin in PINS:
        px, py = _to_xy(pin["lon"], pin["lat"])
        qx, qy = px + pin["dx"], py + pin["dy"]
        if pin["dx"] or pin["dy"]:
            pen.line([px, py, qx, qy], fill=SCARLET, width=1)
        pen.ellipse([qx - 3, qy - 3, qx + 3, qy + 3], fill=SCARLET)
        pen.ellipse([qx - 8, qy - 8, qx + 8, qy + 8], fill=SCARLET,
                    outline=PAPERWHITE, width=1)
        s = str(pin["n"])
        pen.text((qx - text_w(pen, s, nf) / 2, qy - 6), s, font=nf,
                 fill=PAPERWHITE)


# -------------------------------------------------------------------- layout

def frame_card(pen, x, y, w, h, number):
    pen.rectangle([x, y, x + w - 1, y + h - 1], fill=PAPERWHITE,
                  outline=EDGE, width=1)
    pen.ellipse([x + 6, y + 6, x + 26, y + 26], fill=SCARLET)
    f = font_for(FB_SANS, 11)
    s = str(number)
    pen.text((x + 16 - text_w(pen, s, f) / 2, y + 9), s, font=f,
             fill=PAPERWHITE)


def source_row(pen, x, y, w, source, status):
    plain = font_for(FR_SANS, 9)
    bold = font_for(FB_SANS, 9)
    tag_w = int(text_w(pen, status, bold)) + 12
    label = "SOURCE: " + source
    while text_w(pen, label, plain) > w - tag_w - 4 and len(label) > 8:
        label = label[:-1]
    pen.text((x, y), label, font=plain, fill=FADED)
    flag(pen, x + w - tag_w, y - 2, status)


def lead_card(pen, x, y, w, h, story):
    frame_card(pen, x, y, w, h, story["n"])
    ARTWORK[story["art"]](pen, x + 1, y + 1, w - 2, 142)
    ty = y + 148
    pen.text((x + 10, ty), story["tag"], font=font_for(FB_SANS, 10),
             fill=SCARLET)
    ty += 15
    ty = put_lines(pen, x + 10, ty, story["head"],
                   font_for(FB_SERIF, 20), w - 20, SOOT, spacing=23)
    ty = put_lines(pen, x + 10, ty, story["body"],
                   font_for(FR_SERIF, 12), w - 20, (0x3C, 0x3A, 0x34),
                   spacing=15)
    foot_y = max(ty + 2, y + h - 20)
    source_row(pen, x + 10, foot_y, w - 20, story["src"], story["flag"])


def grid_card(pen, x, y, w, h, story):
    # v4's shape: picture plus headline plus the source line only. The
    # kicker line is left out — it used to push the source line off the
    # bottom of the card.
    frame_card(pen, x, y, w, h, story["n"])
    ARTWORK[story["art"]](pen, x + 1, y + 1, w - 2, 78)
    ty = y + 82
    ty = put_lines(pen, x + 8, ty, story["head"],
                   font_for(FB_SANS, 13), w - 16, SOOT, spacing=16)
    foot_y = max(ty + 2, y + h - 16)
    source_row(pen, x + 8, foot_y, w - 16, story["src"], story["flag"])

def build_page():
    page = _Img.new("RGB", (PAGE_W, PAGE_H), SHEET)
    pen = _Draw.Draw(page)

    # ---- masthead
    title = "THE WORLD IN ONE DAY"
    tf = font_for(FB_SERIF, 56)
    pen.text(((PAGE_W - text_w(pen, title, tf)) / 2, 8), title, font=tf,
             fill=SOOT)
    pen.rectangle([MARGIN, 76, PAGE_W - MARGIN, 78], fill=SOOT)
    date = "THURSDAY 26 NOVEMBER 2026"
    df = font_for(FB_SANS, 19)
    pen.text(((PAGE_W - text_w(pen, date, df)) / 2, 84), date, font=df,
             fill=SOOT)
    sub = ("A nor'easter grounds New York's 100th Thanksgiving parade, "
           "India marks 18 years since the 26/11 Mumbai attacks, and "
           "Brussels deadlocks over a €45bn loan for Kyiv.")
    put_lines(pen, (PAGE_W - 900) / 2, 108, sub,
              font_for(FI_SERIF, 14), 900, SOOT, spacing=17)

    # ---- count boxes: 34 stories, 9 regions, sources and fields
    boxes = [{"big": "34", "small": "STORIES"},
             {"big": "9", "small": "REGIONS"},
             {"big": "20 SOURCES · 14 FIELDS", "small": ""}]
    box_w = (PAGE_INNER - 14) // 3
    box_y = 142
    for k, box in enumerate(boxes):
        bx = MARGIN + k * (box_w + 7)
        pen.rectangle([bx, box_y, bx + box_w - 1, box_y + 27], outline=SOOT,
                      width=1, fill=PAPERWHITE)
        lf = font_for(FB_SANS, 17)
        if box["small"]:
            label = box["big"] + " " + box["small"]
            lx = bx + (box_w - text_w(pen, label, lf)) / 2
            pen.text((lx, box_y + 5), label, font=lf, fill=SOOT)
            pen.text((lx, box_y + 5), box["big"] + " ", font=lf,
                     fill=SCARLET)
        else:
            pen.text((bx + (box_w - text_w(pen, box["big"], lf)) / 2,
                      box_y + 5), box["big"], font=lf, fill=SOOT)

    # ---- region bar
    tally = zone_tally()
    bar_y = 176
    bar_x = MARGIN
    for zone in ZONES:
        seg = int(PAGE_INNER * tally[zone] / 34)
        pen.rectangle([bar_x, bar_y, bar_x + seg - 1, bar_y + 7],
                      fill=ZONE_PAINT[zone])
        bar_x += seg
    labels = "  ·  ".join("%s %d" % (ZONE_NAMES[z], tally[z])
                          for z in ZONES)
    lf = font_for(FR_SANS, 11)
    pen.text(((PAGE_W - text_w(pen, labels, lf)) / 2, 188), labels,
             font=lf, fill=FADED)

    # ---- three leads
    lead_w = (PAGE_INNER - 20) // 3
    lead_y = 202
    for k, story in enumerate(LEADS):
        lead_card(pen, MARGIN + k * (lead_w + 10), lead_y, lead_w, 264,
                  story)

    # ---- ten grid cards, five across and two down
    cell_w = (PAGE_INNER - 40) // 5
    for row in range(2):
        cell_y = 466 + row * 134
        for col in range(5):
            story = GRID[row * 5 + col]
            grid_card(pen, MARGIN + col * (cell_w + 10), cell_y, cell_w,
                      134, story)

    # ---- timeline
    tl_y = 736
    pen.text((MARGIN, tl_y), "THE DAY IN UTC", font=font_for(FB_SANS, 13),
             fill=SOOT)
    pen.line([MARGIN + 130, tl_y + 8, PAGE_W - MARGIN, tl_y + 8],
             fill=EDGE, width=1)
    for k, slot in enumerate(TIMELINE):
        tx = MARGIN + (k % 3) * 330
        ty = 754 + (k // 3) * 16
        pen.text((tx, ty), slot["at"], font=font_for(FB_SANS, 11),
                 fill=SKYBLUE)
        pen.text((tx + 74, ty), slot["what"], font=font_for(FR_SANS, 11),
                 fill=SOOT)

    # ---- bottom half: map on the left, the rest of the stories right
    pen.line([MARGIN, 794, PAGE_W - MARGIN, 794], fill=SOOT, width=2)
    paint_map(pen, MARGIN, 800, 330, 148)
    list_x = MARGIN + 330 + 16
    list_w = PAGE_W - MARGIN - list_x
    pen.text((list_x, 800), "AND ALSO — STORIES 14–34",
             font=font_for(FB_SANS, 12), fill=SOOT)
    col_w = (list_w - 14) // 2
    item_ft = font_for(FR_SANS, 10)
    for k, item in enumerate(ALSO):
        cx = list_x + (k // 11) * (col_w + 14)
        cy = 818 + (k % 11) * 11
        pen.text((cx, cy), "%d." % item["n"], font=font_for(FB_SANS, 10),
                 fill=SCARLET)
        text = "%s — %s" % (item["head"], item["city"])
        if text_w(pen, text, item_ft) > col_w - 20:
            text = item["head"]
        pen.text((cx + 20, cy), text, font=item_ft, fill=SOOT)

    # ---- date check: eight items, four columns by two rows
    check_y = 954
    pen.rectangle([MARGIN, check_y, PAGE_W - MARGIN, check_y + 40],
                  outline=SCARLET, width=1, fill=PAPERWHITE)
    pen.text((MARGIN + 8, check_y + 3),
             "DATE CHECK — THESE ARE NOT 26 NOVEMBER",
             font=font_for(FB_SANS, 11), fill=SCARLET)
    check_ft = font_for(FR_SANS, 9)
    for k, item in enumerate(DATE_CHECK[:4]):
        pen.text((MARGIN + 8 + k * 245, check_y + 16), "× " + item,
                 font=check_ft, fill=SOOT)
    for k, item in enumerate(DATE_CHECK[4:]):
        pen.text((MARGIN + 8 + k * 245, check_y + 28), "× " + item,
                 font=check_ft, fill=SOOT)

    # ---- footer
    pen.text((MARGIN, 998),
             "Every story here happened or was first reported on Thursday "
             "26 November 2026. Sources are named on each story.",
             font=font_for(FI_SERIF, 10), fill=FADED)
    pen.text((MARGIN, 1009),
             "HOW SURE: OFFICIAL = government or institution · CONFIRMED = "
             "2+ outlets · REPORTED = one outlet · CLAIM = one side's word "
             "only. Scenes are drawn illustrations, not photographs.",
             font=font_for(FR_SANS, 9), fill=FADED)

    page.save(OUT_PATH, format="PNG", optimize=True)
    return OUT_PATH


if __name__ == "__main__":
    _out = build_page()
    print("wrote", _out, Path(_out).stat().st_size, "bytes")
