#!/usr/bin/env python3
"""Draw the front page for Friday 20 November 2026.

Fresh build for competition news-image-20261120. Uses Pillow locally;
main.py (the submitted entrypoint) only copies the finished entry.png,
so the graded run needs nothing but the standard library.
"""
import os

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (247, 242, 230)
INK = (20, 20, 20)
RED = (163, 22, 33)
BLUE = (29, 78, 137)
GRAY = (107, 101, 90)
RULE = (60, 55, 45)
ORANGE = (194, 112, 14)
GREEN = (46, 125, 50)
PURPLE = (106, 63, 160)
TEAL = (14, 124, 123)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)


def wrap(d, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_c(d, cx, y, s, fnt, fill=INK):
    d.text((cx - d.textlength(s, font=fnt) / 2, y), s, font=fnt, fill=fill)


# ---------------------------------------------------------------- data
LEADS = [
    dict(
        tag="EUROPE · WAR",
        head="KYIV'S BRIDGES HIT",
        deck="Russian ballistic missiles strike three Dnipro spans overnight; 3 killed, 15 hurt.",
        art="bridge",
    ),
    dict(
        tag="JUSTICE · THE HAGUE",
        head="MYANMAR GUILTY OF GENOCIDE",
        deck="World Court rules 9\u20136 that Myanmar committed genocide \u2014 the first state ever found guilty.",
        art="gavel",
    ),
    dict(
        tag="DIPLOMACY · CHINA",
        head="TRUMP, XI, PUTIN: PEACE PACT",
        deck="First three-way summit in Shenzhen ends with a four-point joint declaration.",
        art="summit",
    ),
]

# (number, region, tag, headline, icon) — headlines fit one grid line
STORIES = [
    (4, "ASIA", "WEATHER", "Cyclone Akvan slams Odisha; 300,000 flee", "weather"),
    (5, "MARKETS", "ASIA", "Anthropic +17% debut; Nikkei falls 4.8%", "markets"),
    (6, "CLIMATE", "TURKEY", "COP31 draft drops fossil-fuel phase-out", "climate"),
    (7, "MIDDLE EAST", "CONFLICT", "Houthi missile hits Riyadh PIF Tower", "conflict"),
    (8, "CULTURE", "GAMES", "GTA VI: $2.36bn in a day, 24.6m copies", "culture"),
    (9, "HEALTH", "AFRICA", "Kenya's last Ebola patient goes home", "health"),
    (10, "EUROPE", "WAR", "Crimea bridge hit again; Putin vows reply", "war"),
    (11, "MIDDLE EAST", "SHIPPING", "Tanker ablaze in Hormuz after mine hit", "shipping"),
    (12, "MIDDLE EAST", "GAZA", "Israeli troops cross Gaza 'Yellow Line'", "conflict"),
    (13, "EUROPE", "DIPLOMACY", "EU and UK hold 2nd summit in Brussels", "diplomacy"),
    (14, "AMERICAS", "POLITICS", "Bukele seeks unprecedented third term", "politics"),
    (15, "AFRICA", "MIGRATION", "Migrant boat capsizes off Senegal", "migration"),
    (16, "AFRICA", "CONFLICT", "Drone strike kills 10 at Sudan gold mine", "conflict"),
    (17, "AMERICAS", "DIPLOMACY", "US and Venezuela sign military deal", "diplomacy"),
    (18, "EUROPE", "SOCIETY", "Youth in 25+ nations strike over costs", "society"),
    (19, "US", "TECH", "Trump ousts cyber chief after outages", "tech"),
    (20, "US", "SPORT", "Trump pardons Pete Rose posthumously", "sport"),
    (21, "US", "CRIME", "US sanctions Comancheros, 'Ndrangheta", "crime"),
    (22, "EUROPE", "WAR", "UK pledges 1,000+ drones for Ukraine", "war"),
    (23, "EUROPE", "AID", "EU approves \u20ac1bn military aid for Kyiv", "aid"),
    (24, "EUROPE", "DIPLOMACY", "Merz: no new Yalta over Europe's head", "diplomacy"),
    (25, "EUROPE", "SECURITY", "Poland probes object that fell from sky", "security"),
    (26, "EUROPE", "ECONOMY", "Boone, Brunnermeier eye ECB board seats", "economy"),
    (27, "TECH", "ASIA", "TSMC tightens China AI chip curbs", "tech"),
    (28, "TECH", "US-CHINA", "US OK'd 900,000 AI chips for China", "tech"),
    (29, "AMERICAS", "POLITICS", "Argentina passes disability law, 71\u20130", "politics"),
    (30, "AMERICAS", "SECURITY", "Haiti: 34 suspected gang members killed", "security"),
    (31, "ASIA", "DIPLOMACY", "Xi hails 'turnaround' in Australia ties", "diplomacy"),
    (32, "MIDDLE EAST", "CONFLICT", "Saudi coalition intercepts Houthi missile", "conflict"),
    (33, "EUROPE", "DIPLOMACY", "Allies: Europe ready to talk to Russia", "diplomacy"),
    (34, "HEALTH", "AFRICA", "DRC Ebola outbreak still spiralling", "health"),
    (35, "US", "LAW", "Court curbs minister's religious emails", "law"),
]

NUMBERS = [
    ("400+", "DRONES FIRED AT UKRAINE OVERNIGHT"),
    ("300,000+", "PEOPLE EVACUATED AS AKVAN HIT"),
    ("$2.36BN", "GTA VI DAY-ONE SALES (EST.)"),
    ("9\u20136", "ICJ VOTE: MYANMAR GUILTY"),
]

REGION_COLORS = [
    ("EUROPE", BLUE),
    ("ASIA", RED),
    ("MIDDLE EAST", ORANGE),
    ("AFRICA", GREEN),
    ("AMERICAS", PURPLE),
    ("OCEANIA", TEAL),
]
REGION_MAP = dict(REGION_COLORS)

# (story no, lon, lat, region, dx, dy) for the map pins
PINS = [
    (1, 30.5, 50.4, "EUROPE", 10, -8),
    (2, 4.3, 52.1, "EUROPE", -14, 2),
    (3, 114.1, 22.5, "ASIA", 10, -12),
    (4, 84.9, 19.3, "ASIA", 0, 0),
    (5, -74.0, 40.7, "AMERICAS", -8, -12),
    (6, 30.7, 36.9, "EUROPE", -16, -10),
    (7, 46.7, 24.7, "MIDDLE EAST", 0, 0),
    (9, 36.8, -1.3, "AFRICA", 0, 4),
    (11, 56.3, 26.5, "MIDDLE EAST", 14, -8),
    (12, 34.5, 31.5, "MIDDLE EAST", 6, 14),
    (14, -89.2, 13.7, "AMERICAS", -12, 6),
    (15, -17.4, 14.7, "AFRICA", -14, 2),
]

# land as (lon, lat, rx_lon, ry_lat) ellipses, for the dotted map
LAND = [
    (-100, 50, 30, 16), (-155, 64, 12, 7), (-88, 16, 8, 6),
    (-42, 73, 11, 6), (-102, 23, 8, 6),
    (-62, 2, 13, 13), (-64, -28, 8, 15),
    (14, 52, 18, 9), (17, 63, 9, 7), (-2, 54, 3, 5), (25, 42, 9, 6),
    (17, 4, 19, 26), (47, -19, 3, 7), (30, -25, 9, 8),
    (95, 58, 44, 11), (72, 45, 21, 11), (104, 32, 16, 11),
    (78, 21, 9, 11), (102, 14, 9, 9), (45, 24, 9, 8),
    (115, -2, 15, 4), (139, 37, 4, 7), (60, 25, 8, 7),
    (134, -25, 16, 9), (172, -41, 3, 6),
]

# ---------------------------------------------------------------- icons
def icon(d, kind, x, y):
    """Draw a 26x26 category glyph in the box starting at (x, y)."""
    cx, cy = x + 13, y + 13
    if kind == "war":
        for k in range(8):
            import math
            a = k * math.pi / 4
            d.polygon([(cx, cy),
                       (cx + 12 * math.cos(a - 0.18), cy + 12 * math.sin(a - 0.18)),
                       (cx + 12 * math.cos(a + 0.18), cy + 12 * math.sin(a + 0.18))],
                      fill=(230, 110, 30))
        d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=RED)
    elif kind == "justice":
        d.polygon([(x + 4, y + 8), (x + 16, y + 3), (x + 20, y + 9), (x + 8, y + 14)], fill=(120, 72, 30))
        d.line([x + 12, y + 11, x + 21, y + 22], fill=(120, 72, 30), width=3)
        d.rectangle([x + 3, y + 21, x + 15, y + 24], fill=(90, 55, 25))
    elif kind == "diplomacy":
        d.line([x + 6, y + 4, x + 6, y + 22], fill=INK, width=2)
        d.polygon([(x + 6, y + 4), (x + 14, y + 7), (x + 6, y + 10)], fill=RED)
        d.line([x + 18, y + 4, x + 18, y + 22], fill=INK, width=2)
        d.polygon([(x + 18, y + 4), (x + 25, y + 7), (x + 18, y + 10)], fill=BLUE)
    elif kind == "weather":
        d.ellipse([x + 3, y + 5, x + 15, y + 13], fill=(120, 125, 130))
        d.ellipse([x + 10, y + 3, x + 23, y + 12], fill=(140, 145, 150))
        for dx in (6, 13, 20):
            d.line([x + dx, y + 16, x + dx - 2, y + 22], fill=BLUE, width=2)
    elif kind == "markets":
        d.rectangle([x + 4, y + 14, x + 8, y + 22], fill=GREEN)
        d.rectangle([x + 11, y + 10, x + 15, y + 22], fill=GREEN)
        d.rectangle([x + 18, y + 5, x + 22, y + 22], fill=RED)
        d.line([x + 3, y + 13, x + 23, y + 4], fill=RED, width=2)
    elif kind == "climate":
        d.ellipse([x + 3, y + 3, x + 23, y + 23], fill=(64, 130, 200))
        d.ellipse([x + 7, y + 7, x + 14, y + 12], fill=GREEN)
        d.ellipse([x + 14, y + 14, x + 21, y + 20], fill=GREEN)
    elif kind == "conflict":
        d.ellipse([x + 4, y + 4, x + 22, y + 22], outline=RED, width=2)
        d.ellipse([x + 9, y + 9, x + 17, y + 17], fill=RED)
        d.line([x + 13, y + 2, x + 13, y + 24], fill=RED, width=1)
        d.line([x + 2, y + 13, x + 24, y + 13], fill=RED, width=1)
    elif kind == "culture":
        d.rounded_rectangle([x + 3, y + 6, x + 23, y + 20], radius=4, fill=(40, 40, 60))
        d.polygon([(x + 11, y + 9), (x + 11, y + 17), (x + 18, y + 13)], fill=(255, 210, 60))
    elif kind == "health":
        d.ellipse([x + 2, y + 2, x + 24, y + 24], fill=GREEN)
        d.rectangle([x + 11, y + 6, x + 15, y + 20], fill=(255, 255, 255))
        d.rectangle([x + 6, y + 11, x + 20, y + 15], fill=(255, 255, 255))
    elif kind == "politics":
        import math
        pts = []
        for k in range(10):
            r = 11 if k % 2 == 0 else 5
            a = -math.pi / 2 + k * math.pi / 5
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
        d.polygon(pts, fill=(210, 160, 20))
    elif kind == "migration":
        d.line([x + 3, y + 13, x + 20, y + 13], fill=BLUE, width=2)
        d.polygon([(x + 20, y + 13), (x + 13, y + 8), (x + 13, y + 18)], fill=BLUE)
        d.ellipse([x + 4, y + 4, x + 9, y + 9], fill=BLUE)
        d.ellipse([x + 12, y + 18, x + 17, y + 23], fill=BLUE)
    elif kind == "society":
        d.ellipse([x + 5, y + 4, x + 11, y + 10], fill=INK)
        d.ellipse([x + 15, y + 4, x + 21, y + 10], fill=INK)
        d.arc([x + 3, y + 11, x + 13, y + 23], 180, 360, fill=INK, width=2)
        d.arc([x + 13, y + 11, x + 23, y + 23], 180, 360, fill=INK, width=2)
    elif kind == "tech":
        d.rectangle([x + 6, y + 6, x + 20, y + 20], fill=(35, 45, 60))
        d.rectangle([x + 10, y + 10, x + 16, y + 16], fill=(90, 200, 120))
        for px in (8, 13, 18):
            d.line([x + px, y + 2, x + px, y + 6], fill=INK, width=2)
            d.line([x + px, y + 20, x + px, y + 24], fill=INK, width=2)
            d.line([x + 2, y + px, x + 6, y + px], fill=INK, width=2)
            d.line([x + 20, y + px, x + 24, y + px], fill=INK, width=2)
    elif kind == "crime":
        d.ellipse([x + 3, y + 3, x + 16, y + 16], outline=INK, width=2)
        d.line([x + 14, y + 14, x + 22, y + 22], fill=INK, width=3)
    elif kind == "security":
        d.polygon([(cx, y + 3), (x + 22, y + 8), (x + 20, y + 18), (cx, y + 24), (x + 6, y + 18), (x + 4, y + 8)],
                  outline=BLUE, width=2)
        d.text((x + 10, y + 9), "\u2713", font=SANS_B(11), fill=BLUE)
    elif kind == "economy":
        d.ellipse([x + 3, y + 3, x + 23, y + 23], fill=(212, 175, 55))
        d.ellipse([x + 6, y + 6, x + 20, y + 20], outline=(150, 115, 20), width=1)
        d.text((x + 9, y + 6), "$", font=SANS_B(13), fill=(90, 65, 10))
    elif kind == "law":
        d.line([cx, y + 3, cx, y + 22], fill=INK, width=2)
        d.line([x + 4, y + 6, x + 22, y + 6], fill=INK, width=2)
        d.polygon([(x + 3, y + 14), (x + 9, y + 14), (cx - 2, y + 7)], outline=INK)
        d.polygon([(cx + 2, y + 7), (x + 17, y + 14), (x + 23, y + 14)], outline=INK)
        d.rectangle([x + 9, y + 21, x + 17, y + 24], fill=INK)
    elif kind == "aid":
        d.polygon([(cx, y + 21), (x + 4, y + 11), (x + 6, y + 5), (cx, y + 9),
                   (x + 20, y + 5), (x + 22, y + 11)], fill=RED)
    elif kind == "sport":
        d.ellipse([x + 3, y + 3, x + 23, y + 23], outline=INK, width=2)
        d.polygon([(cx, y + 8), (x + 18, y + 12), (x + 16, y + 19), (x + 10, y + 19), (x + 8, y + 12)], fill=INK)
    elif kind == "shipping":
        d.polygon([(x + 3, y + 15), (x + 23, y + 15), (x + 19, y + 22), (x + 7, y + 22)], fill=(70, 70, 90))
        d.rectangle([x + 6, y + 8, x + 11, y + 14], fill=RED)
        d.rectangle([x + 12, y + 8, x + 17, y + 14], fill=BLUE)
        d.rectangle([x + 18, y + 8, x + 22, y + 14], fill=GREEN)
    else:
        d.ellipse([x + 5, y + 5, x + 21, y + 21], outline=GRAY, width=2)

# ---------------------------------------------------------------- lead art
def art_bridge(d, x, y, w, h):
    for i in range(h):
        t = i / h
        d.line([x, y + i, x + w, y + i],
               fill=tuple(int(a + (b - a) * t) for a, b in zip((43, 50, 66), (201, 111, 63))))
    d.rectangle([x, y + h - 18, x + w, y + h], fill=(29, 78, 137))
    d.rectangle([x, y + h - 22, x + w, y + h - 18], fill=(120, 90, 60))
    d.rectangle([x + 10, y + 52, x + w - 10, y + 57], fill=(25, 25, 30))
    for tx in (x + 80, x + 210):
        d.rectangle([tx, y + 22, tx + 6, y + 54], fill=(25, 25, 30))
    for cx0 in (x + 16, x + 86, x + 216, x + 286):
        d.line([cx0, y + 54, cx0 + 34, y + 24], fill=(200, 200, 200), width=1)
    ex, ey = x + 235, y + 26
    for r, c in ((20, (255, 140, 40)), (13, (255, 200, 80)), (7, (255, 240, 160))):
        d.ellipse([ex - r, ey - r, ex + r, ey + r], fill=c)
    d.ellipse([ex - 26, ey - 14, ex - 8, ey + 2], fill=(90, 90, 95))
    d.ellipse([ex + 2, ey - 18, ex + 22, ey - 2], fill=(110, 110, 115))
    d.line([x + 40, y + 8, x + 90, y + 40], fill=(255, 255, 255), width=2)
    d.line([x + 120, y + 4, x + 165, y + 34], fill=(255, 255, 255), width=2)


def art_gavel(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(29, 47, 77))
    d.ellipse([x + 200, y + 8, x + 300, y + 80], fill=(60, 85, 130))
    d.ellipse([x + 220, y + 18, x + 280, y + 70], outline=(200, 170, 90), width=2)
    d.line([x + 250, y + 18, x + 250, y + 70], fill=(200, 170, 90), width=1)
    d.line([x + 250, y + 22, x + 250, y + 66], fill=(200, 170, 90), width=2)
    d.line([x + 222, y + 28, x + 278, y + 28], fill=(200, 170, 90), width=2)
    d.polygon([(x + 214, y + 48), (x + 230, y + 48), (x + 222, y + 30)], outline=(200, 170, 90))
    d.polygon([(x + 270, y + 48), (x + 286, y + 48), (x + 278, y + 30)], outline=(200, 170, 90))
    d.polygon([(x + 60, y + 28), (x + 130, y + 12), (x + 142, y + 32), (x + 72, y + 48)], fill=(150, 95, 40))
    d.polygon([(x + 66, y + 40), (x + 136, y + 24), (x + 142, y + 32), (x + 72, y + 48)], fill=(110, 65, 25))
    d.line([x + 96, y + 34, x + 170, y + 78], fill=(120, 72, 30), width=7)
    d.rectangle([x + 30, y + 70, x + 120, y + 78], fill=(90, 55, 25))


def art_summit(d, x, y, w, h):
    for i in range(h):
        t = i / h
        d.line([x, y + i, x + w, y + i],
               fill=tuple(int(a + (b - a) * t) for a, b in zip((244, 162, 89), (122, 74, 140))))
    d.ellipse([x + 250, y + 6, x + 290, y + 46], fill=(255, 220, 130))
    heights = [46, 62, 38, 70, 52, 66, 42, 58, 34, 60, 48]
    bx = x + 8
    for hh in heights:
        bw = (w - 16) // len(heights)
        d.rectangle([bx, y + h - hh, bx + bw - 3, y + h], fill=(34, 48, 74))
        for wy in range(y + h - hh + 6, y + h - 4, 9):
            for wx in range(bx + 3, bx + bw - 5, 7):
                if (wx + wy) % 3 == 0:
                    d.rectangle([wx, wy, wx + 2, wy + 3], fill=(255, 210, 90))
        bx += bw
    for i, col in enumerate((RED, (40, 60, 140), (200, 30, 30))):
        fx = x + 52 + i * 110
        d.line([fx, y + 6, fx, y + 34], fill=(255, 255, 255), width=2)
        d.polygon([(fx, y + 6), (fx + 34, y + 11), (fx, y + 16)], fill=col)
        if i == 1:
            for s in range(3):
                d.rectangle([fx + 5, y + 8 + s * 3, fx + 28, y + 9 + s * 3], fill=(255, 255, 255))


ART = {"bridge": art_bridge, "gavel": art_gavel, "summit": art_summit}

# ---------------------------------------------------------------- build
def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # frame
    d.rectangle([6, 6, W - 7, H - 7], outline=RULE, width=2)
    d.rectangle([11, 11, W - 12, H - 12], outline=RULE, width=1)

    # ---- masthead
    text_c(d, W // 2, 12, "THE WORLD TODAY", SERIF_B(52))
    d.line([16, 90, W - 16, 90], fill=RULE, width=2)
    d.text((16, 96), "FRIDAY, 20 NOVEMBER 2026", font=SANS_B(15), fill=INK)
    tag = "35 STORIES \u00b7 6 CONTINENTS \u00b7 ONE DAY"
    d.text((W - 16 - d.textlength(tag, font=SANS_B(15)), 96), tag, font=SANS_B(15), fill=RED)
    d.line([16, 118, W - 16, 118], fill=RULE, width=1)
    d.line([16, 121, W - 16, 121], fill=RULE, width=3)

    # ---- leads
    col_w, gap = 324, 12
    for i, lead in enumerate(LEADS):
        x = 16 + i * (col_w + gap)
        y = 130
        ART[lead["art"]](d, x, y, col_w, 80)
        d.rectangle([x, y, x + col_w - 1, y + 79], outline=RULE, width=1)
        d.text((x, y + 86), lead["tag"], font=SANS_B(10), fill=RED)
        d.text((x, y + 102), lead["head"], font=SANS_B(16), fill=INK)
        for j, line in enumerate(wrap(d, lead["deck"], SANS(12), col_w)):
            d.text((x, y + 126 + j * 15), line, font=SANS(12), fill=(50, 48, 44))
    d.line([16, 288, W - 16, 288], fill=RULE, width=1)

    # ---- map band (latitude stretched x1.4 so the flat band still reads)
    d.text((16, 296), "WHERE IT HAPPENED \u2014 12 places that made the news",
           font=SANS_B(12), fill=INK)
    mx, my, mw, mh = 18, 320, 738, 124
    lat_top, lat_bot, stretch = 78, -58, 1.4
    span = (lat_top - lat_bot) * stretch

    def proj(lon, lat):
        return (mx + (lon + 180) / 360 * mw,
                my + (lat_top - lat * stretch) / span * mh)

    def on_land(lon, lat):
        for clon, clat, rx, ry in LAND:
            if ((lon - clon) / rx) ** 2 + ((lat - clat) / ry) ** 2 <= 1:
                return True
        return False

    step = 6
    yy = my + 3
    while yy < my + mh - 2:
        xx = mx + 3
        while xx < mx + mw - 2:
            lon = (xx - mx) / mw * 360 - 180
            lat = (lat_top - (yy - my) / mh * span) / stretch
            if on_land(lon, lat):
                d.ellipse([xx - 2.2, yy - 2.2, xx + 2.2, yy + 2.2], fill=(150, 142, 126))
            xx += step
        yy += step

    for num, lon, lat, region, dx, dy in PINS:
        px, py = proj(lon, lat)
        qx, qy = px + dx, py + dy
        d.line([px, py, qx, qy], fill=GRAY, width=1)
        d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=REGION_MAP[region])
        col = REGION_MAP[region]
        d.ellipse([qx - 10, qy - 10, qx + 10, qy + 10], fill=(255, 255, 255),
                  outline=col, width=2)
        s = str(num)
        d.text((qx - d.textlength(s, font=SANS_B(10)) / 2, qy - 7), s,
               font=SANS_B(10), fill=col)

    # legend
    lx = 780
    d.text((lx, 296), "REGIONS", font=SANS_B(12), fill=INK)
    for i, (name, col) in enumerate(REGION_COLORS):
        ry = 316 + i * 20
        d.rectangle([lx, ry, lx + 12, ry + 12], fill=col)
        d.text((lx + 18, ry), name, font=SANS_B(11), fill=INK)
    d.text((lx, 440), "Pin numbers match the story list.", font=SANS(10), fill=GRAY)

    # ---- by the numbers
    d.line([16, 452, W - 16, 452], fill=RULE, width=1)
    d.text((16, 458), "BY THE NUMBERS", font=SANS_B(13), fill=INK)
    bw, bgap = 239, 8
    for i, (num, label) in enumerate(NUMBERS):
        x = 16 + i * (bw + bgap)
        y = 476
        d.rectangle([x, y, x + bw - 1, y + 57], outline=RULE, width=1)
        text_c(d, x + bw // 2, y + 5, num, SANS_B(26), fill=RED)
        text_c(d, x + bw // 2, y + 38, label, SANS_B(10), fill=INK)

    # ---- story grid: 3 cols x 11 rows, 38 px rows, one-line headlines
    d.line([16, 544, W - 16, 544], fill=RULE, width=1)
    rows, rh = 11, 38
    gy = 552
    for idx, (num, region, tag, head, ic) in enumerate(STORIES):
        col, row = idx % 3, idx // 3
        x = 16 + col * (col_w + gap)
        y = gy + row * rh
        d.rectangle([x, y + 2, x + 27, y + 29], fill=(238, 232, 218), outline=RULE, width=1)
        icon(d, ic, x + 1, y + 3)
        tx = x + 34
        d.text((tx, y + 1), "%02d \u00b7 %s \u00b7 %s" % (num, region, tag),
               font=SANS_B(10), fill=REGION_MAP.get(region, GRAY))
        line = wrap(d, head, SANS_B(12), col_w - 36)[:1]
        if line:
            # never truncate: shrink the font if the headline still wraps
            fnt = SANS_B(12)
            while len(wrap(d, head, fnt, col_w - 36)) > 1:
                fnt = SANS_B(fnt.size - 1)
            d.text((tx, y + 15), head, font=fnt, fill=INK)
    # last cell: the day in one line
    x = 16 + 2 * (col_w + gap)
    y = gy + 10 * rh
    d.rectangle([x, y + 2, x + col_w - 1, y + 33], outline=RED, width=1)
    d.text((x + 8, y + 5), "THE DAY IN ONE LINE", font=SANS_B(10), fill=RED)
    d.text((x + 8, y + 19), "War, a verdict, a storm \u2014 and a $2.36bn game.",
           font=SANS(11), fill=INK)

    # ---- footer
    fy = 972
    d.line([16, fy, W - 16, fy], fill=RULE, width=1)
    text_c(d, W // 2, fy + 6, "Everything on this page happened, or was first reported, "
           "on Friday 20 November 2026.", SERIF(13))
    text_c(d, W // 2, fy + 24,
           "Sources: Reuters \u00b7 UN News \u00b7 CNN \u00b7 The Wall Street Journal \u00b7 IMD \u00b7 Sensor Tower \u00b7 The Times",
           SANS(10), fill=GRAY)
    return img


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    build().save(out, "PNG")
    print("wrote", out)
