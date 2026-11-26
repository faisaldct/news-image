#!/usr/bin/env python3
"""Draw the news-image-20261126 entry: a one-page newspaper front page
summing up world news of Thursday 26 November 2026.

Deterministic: no randomness, no timestamps, no network. Run:
    python3 draw_news.py
Writes entry.png (1024x1024, PNG) next to this script.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
PAPER = (250, 245, 236)
INK = (18, 18, 18)
NAVY = (20, 38, 63)
RED = (178, 34, 34)
GOLD = (233, 180, 30)
GOLD_DARK = (190, 140, 10)
GRAY = (96, 92, 84)
RULE = (178, 168, 150)
SKY = (208, 229, 241)
SEA = (126, 178, 213)
PANEL = (235, 240, 244)

FONT_DIR = "/usr/share/fonts/truetype/noto"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_BLACK = lambda s: font("NotoSerifDisplay-Black.ttf", s)
SERIF_BOLD = lambda s: font("NotoSerif-Bold.ttf", s)
SANS_BLACK = lambda s: font("NotoSansDisplay-Black.ttf", s)
SANS_BOLD = lambda s: font("NotoSans-Bold.ttf", s)
SANS_MED = lambda s: font("NotoSans-Medium.ttf", s)
SANS_REG = lambda s: font("NotoSans-Regular.ttf", s)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_centered(draw, cx, y, text, fnt, fill):
    draw.text((cx, y), text, font=fnt, fill=fill, anchor="ma")


def draw_tracked(draw, x, y, text, fnt, fill, tracking=4):
    """Draw text with extra letter spacing, left aligned."""
    cx = x
    for ch in text:
        draw.text((cx, y), ch, font=fnt, fill=fill)
        cx += draw.textlength(ch, font=fnt) + tracking
    return cx


def text_w(draw, text, fnt):
    return draw.textlength(text, font=fnt)


# ---------------------------------------------------------------- icons
def icon_satellite(d, x, y, s):
    """Satellite with solar panels inside a s x s box at (x, y)."""
    d.rectangle([x, y, x + s, y + s], fill=(223, 233, 240))
    cx, cy = x + s // 2, y + s // 2
    # orbit arc
    d.arc([x + 8, y + 8, x + s - 8, y + s - 8], start=200, end=340, fill=(120, 140, 160), width=2)
    # solar panels
    d.rectangle([x + 8, cy - 8, cx - 16, cy + 8], fill=(36, 90, 140))
    d.rectangle([cx + 16, cy - 8, x + s - 8, cy + 8], fill=(36, 90, 140))
    d.line([x + 12, cy - 8, x + 12, cy + 8], fill=(255, 255, 255), width=1)
    d.line([x + s - 12, cy - 8, x + s - 12, cy + 8], fill=(255, 255, 255), width=1)
    # body
    d.rectangle([cx - 16, cy - 13, cx + 16, cy + 13], fill=(70, 80, 95))
    d.rectangle([cx - 16, cy - 13, cx + 16, cy - 6], fill=(150, 160, 175))
    # antenna
    d.line([cx, cy - 13, cx + 10, cy - 26], fill=(70, 80, 95), width=3)
    d.ellipse([cx + 6, cy - 30, cx + 14, cy - 22], fill=RED)
    # stars
    for sx, sy in ((x + 14, y + 14), (x + s - 16, y + 18), (x + 20, y + s - 14)):
        d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=GOLD_DARK)


def icon_chart(d, x, y, s):
    """Falling market chart with coins, inside a s x s box."""
    d.rectangle([x, y, x + s, y + s], fill=(251, 235, 232))
    # axes
    d.line([x + 16, y + 16, x + 16, y + s - 16], fill=INK, width=3)
    d.line([x + 16, y + s - 16, x + s - 14, y + s - 16], fill=INK, width=3)
    # descending line
    pts = [(x + 22, y + 26), (x + 40, y + 38), (x + 58, y + 34), (x + 76, y + 58), (x + 92, y + 78)]
    d.line(pts, fill=RED, width=4, joint="curve")
    for px, py in pts:
        d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=RED)
    # coins
    for cx, cy in ((x + s - 26, y + 22), (x + s - 40, y + 36)):
        d.ellipse([cx - 10, cy - 10, cx + 10, cy + 10], fill=GOLD, outline=GOLD_DARK, width=2)
        d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], outline=GOLD_DARK, width=2)


def icon_shield(d, x, y, s):
    """Shield with a check mark, inside a s x s box."""
    d.rectangle([x, y, x + s, y + s], fill=(223, 233, 240))
    cx = x + s // 2
    top, bot = y + 12, y + s - 12
    shield = [(cx - 32, top), (cx + 32, top), (cx + 32, top + 34),
              (cx, bot), (cx - 32, top + 34)]
    d.polygon(shield, fill=NAVY)
    d.line([(cx - 16, top + 36), (cx - 5, top + 48), (cx + 18, top + 22)],
           fill=(255, 255, 255), width=5, joint="curve")


def icon_flag_coin(d, x, y, s):
    """Ukraine flag bars with a gold coin, inside a s x s box."""
    d.rectangle([x, y, x + s, y + s], fill=(235, 240, 244))
    d.rectangle([x + 14, y + 26, x + s - 14, y + s // 2], fill=(0, 91, 187))
    d.rectangle([x + 14, y + s // 2, x + s - 14, y + s - 26], fill=(255, 213, 0))
    cx, cy = x + s - 34, y + s - 34
    d.ellipse([cx - 18, cy - 18, cx + 18, cy + 18], fill=GOLD, outline=GOLD_DARK, width=3)
    d.ellipse([cx - 11, cy - 11, cx + 11, cy + 11], outline=GOLD_DARK, width=2)


def draw_ship(d, x0, y0, x1, y1):
    """Cargo ship scene (tariffs illustration) inside the given box."""
    d.rectangle([x0, y0, x1, y1], fill=SKY)
    # sun
    d.ellipse([x0 + 18, y0 + 16, x0 + 52, y0 + 50], fill=GOLD)
    # sea
    sea_y = y0 + 146
    d.rectangle([x0, sea_y, x1, y1], fill=SEA)
    # containers: two rows sitting on the hull
    hull_top = y0 + 216
    hull_bot = y0 + 276
    cont_w, cont_h = 74, 34
    row2_y = hull_top - cont_h
    row1_y = row2_y - cont_h - 4
    colors2 = [(178, 34, 34), (36, 90, 140), (212, 172, 13)]
    colors1 = [(30, 132, 73), (202, 88, 24)]
    cx = x0 + 22
    for i, c in enumerate(colors2):
        d.rectangle([cx + i * (cont_w + 5), row2_y, cx + i * (cont_w + 5) + cont_w, row2_y + cont_h], fill=c)
    cx = x0 + 60
    for i, c in enumerate(colors1):
        d.rectangle([cx + i * (cont_w + 5), row1_y, cx + i * (cont_w + 5) + cont_w, row1_y + cont_h], fill=c)
    # bridge tower at the stern (right end)
    d.rectangle([x1 - 46, row1_y - 12, x1 - 16, hull_top], fill=(240, 240, 235))
    d.rectangle([x1 - 46, row1_y - 12, x1 - 16, row1_y + 8], fill=NAVY)
    # hull
    d.polygon([(x0 + 12, hull_top), (x1 - 12, hull_top), (x1 - 34, hull_bot),
               (x0 + 34, hull_bot)], fill=NAVY)
    d.rectangle([x0 + 12, hull_top, x1 - 12, hull_top + 8], fill=(120, 30, 30))
    # wave foam lapping at the hull
    for wy in (hull_bot + 6, hull_bot + 22):
        for wx in range(x0 + 10, x1 - 20, 46):
            d.arc([wx, wy, wx + 34, wy + 14], start=180, end=360, fill=(255, 255, 255), width=3)
    # 35% badge
    bx, by, br = x1 - 58, y0 + 58, 46
    d.ellipse([bx - br, by - br, bx + br, by + br], fill=GOLD, outline=(255, 255, 255), width=4)
    draw_centered(d, bx, by - 26, "35%", SANS_BLACK(40), INK)
    draw_centered(d, bx, by + 16, "TARIFF", SANS_BOLD(15), INK)


# ---------------------------------------------------------------- page
def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # outer frame
    d.rectangle([14, 14, W - 14, H - 14], outline=INK, width=3)
    d.rectangle([22, 22, W - 22, H - 22], outline=RULE, width=1)

    # ---- masthead ----
    d.rectangle([28, 28, W - 28, 162], fill=NAVY)
    draw_centered(d, W // 2, 44, "THE WORLD IN ONE DAY", SERIF_BLACK(54), (255, 255, 255))
    draw_centered(d, W // 2, 108, "THURSDAY  ·  26 NOVEMBER 2026", SANS_BOLD(30), GOLD)
    d.line([48, 152, W - 48, 152], fill=(255, 255, 255), width=1)

    # ---- lead story ----
    lx, lw = 40, 590
    ly = 184
    draw_tracked(d, lx, ly, "TRADE  •  TARIFFS", SANS_BLACK(23), RED, tracking=3)
    headline = "TRUMP HITS CHINA AND THE EU WITH NEW TARIFFS"
    hf = SERIF_BLACK(53)
    lines = wrap(d, headline, hf, lw)
    hy = ly + 38
    for line in lines:
        d.text((lx, hy), line, font=hf, fill=INK)
        hy += 62
    deck = "Fourteen economies face duties of up to 35% from January 2027."
    df = SANS_REG(26)
    dy = hy + 6
    for line in wrap(d, deck, df, lw):
        d.text((lx, dy), line, font=df, fill=(48, 48, 48))
        dy += 33

    # lead illustration (right column)
    draw_ship(d, 652, 184, 984, 500)

    # rule under lead
    d.line([40, 522, 984, 522], fill=INK, width=3)
    d.line([40, 528, 984, 528], fill=RULE, width=1)

    # ---- secondary grid 2x2 ----
    stories = [
        ("SPACEX CLEARED FOR 1M AI SATELLITES IN ORBIT",
         "FCC approves orbital data centres.", icon_satellite),
        ("BITCOIN AND ETHER ETFS SEE RECORD OUTFLOWS",
         "Wall Street exits crypto funds in November.", icon_chart),
        ("DOJ LAUNCHES LARGEST-EVER SCAM CRACKDOWN",
         "800+ defendants charged, crypto fraud included.", icon_shield),
        ("UKRAINE LEGALISES AND TAXES CRYPTO",
         "New market law takes effect July 2027.", icon_flag_coin),
    ]
    cell_w, cell_h = 462, 128
    origins = [(40, 544), (522, 544), (40, 688), (522, 688)]
    tf = SANS_BOLD(25)
    for (title, deck2, icon), (ox, oy) in zip(stories, origins):
        icon(d, ox, oy + 4, 104)
        tx = ox + 120
        tw = cell_w - 120
        tlines = wrap(d, title, tf, tw)[:2]
        ty = oy + 2
        for line in tlines:
            d.text((tx, ty), line, font=tf, fill=INK)
            ty += 31
        dlines = wrap(d, deck2, SANS_REG(20), tw)[:2]
        for line in dlines:
            d.text((tx, ty + 2), line, font=SANS_REG(20), fill=GRAY)
            ty += 24

    # rule above also-today
    d.line([40, 832, 984, 832], fill=INK, width=2)

    # ---- also today strip ----
    draw_tracked(d, 40, 848, "ALSO TODAY", SANS_BLACK(22), RED, tracking=3)
    items = [
        "Amazon and Meta in talks to unblock the Muse AI shopping agent.",
        "DeepMind's mass-spec AI identifies molecules with 97% accuracy.",
        "S&P puts Nvidia on downgrade watch; US GDP revised up.",
        "Trump pardons Thanksgiving turkeys Freedom and Feathers.",
    ]
    col_w = 226
    itf = SANS_REG(19)
    for i, item in enumerate(items):
        ox = 40 + i * (col_w + 10)
        iy = 884
        for line in wrap(d, item, itf, col_w):
            d.text((ox, iy), line, font=itf, fill=(48, 48, 48))
            iy += 25

    # ---- footer ----
    d.line([40, 972, 984, 972], fill=RULE, width=1)
    draw_centered(d, W // 2, 980, "26 NOVEMBER 2026  •  WORLD NEWS IN ONE IMAGE",
                  SANS_BOLD(17), GRAY)

    img.save(OUT, format="PNG", optimize=True)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    build()
