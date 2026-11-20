#!/usr/bin/env python3
"""Draw entry.png for news-image-20261120.

One image summing up the world's news of Friday 20 November 2026:
a newspaper front page ("THE WORLD IN ONE DAY") with a lead story on
Anthropic's Nasdaq debut and the AI-doubt sell-off, four panels (Riyadh,
COP31, Gaza, Kenya) and an "also today" ticker. Pure Pillow, flat vector
pictograms, no network, no randomness: same run, same bytes.

Run: python3 draw.py   (writes entry.png next to this file)
"""

import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

PAPER = (247, 243, 232)
INK = (26, 26, 26)
NAVY = (20, 38, 74)
NAVY_DARK = (13, 27, 54)
RED = (192, 57, 43)
GOLD = (217, 164, 65)
TEAL = (15, 118, 110)
GREY = (96, 96, 96)
WHITE = (255, 255, 255)
CARD = (255, 255, 255)
SAND = (232, 214, 170)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def load_font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_TITLE = load_font("DejaVuSans-Bold.ttf", 54)
F_DATE = load_font("DejaVuSans-Bold.ttf", 28)
F_KICK = load_font("DejaVuSans-Bold.ttf", 21)
F_HEAD = load_font("DejaVuSans-Bold.ttf", 38)
F_PANEL_HEAD = load_font("DejaVuSans-Bold.ttf", 25)
F_BODY = load_font("DejaVuSans.ttf", 22)
F_PANEL_BODY = load_font("DejaVuSans.ttf", 19)
F_TAG = load_font("DejaVuSans-Bold.ttf", 17)
F_TICK_LABEL = load_font("DejaVuSans-Bold.ttf", 24)
F_TICK = load_font("DejaVuSans.ttf", 19)
F_BIG_NUM = load_font("DejaVuSans-Bold.ttf", 46)


def wrap(draw, text, font, max_width):
    """Split text into lines that fit max_width pixels."""
    lines = []
    for paragraph in text.split("\n"):
        words = paragraph.split()
        if not words:
            lines.append("")
            continue
        current = words[0]
        for word in words[1:]:
            trial = current + " " + word
            if draw.textlength(trial, font=font) <= max_width:
                current = trial
            else:
                lines.append(current)
                current = word
        lines.append(current)
    return lines


def draw_lines(draw, x, y, lines, font, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        y += leading
    return y


# ---------------------------------------------------------------- pictograms

def globe(draw, cx, cy, r, fill, line):
    """A simple globe: circle with meridians and a latitude line."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill, outline=line, width=3)
    draw.ellipse([cx - r // 3, cy - r, cx + r // 3, cy + r], outline=line, width=2)
    draw.line([cx - r, cy, cx + r, cy], fill=line, width=2)
    draw.arc([cx - r, cy - r // 2, cx + r, cy + r // 2], 200, 340, fill=line, width=2)


def chart_pictogram(draw, x0, y0, x1, y1):
    """Falling candlestick chart with a red trend arrow."""
    draw.rectangle([x0, y0, x1, y1], fill=CARD, outline=NAVY, width=2)
    base = y1 - 34
    top = y0 + 30
    # axes
    draw.line([x0 + 28, y0 + 16, x0 + 28, base], fill=GREY, width=2)
    draw.line([x0 + 28, base, x1 - 16, base], fill=GREY, width=2)
    # five candles, falling from left to right
    closes = [0.18, 0.34, 0.52, 0.68, 0.84]
    slot = (x1 - x0 - 70) // 5
    for i, frac in enumerate(closes):
        cx = x0 + 48 + i * slot + slot // 2
        body_h = 16 + i * 3
        body_top = top + int(frac * (base - top - 40))
        colour = TEAL if i == 0 else RED
        draw.line([cx, body_top - 10, cx, body_top + body_h + 8], fill=colour, width=3)
        draw.rectangle(
            [cx - 11, body_top, cx + 11, body_top + body_h], fill=colour
        )
    # red arrow down-right
    draw.line(
        [x0 + 40, top + 6, x1 - 30, base - 14], fill=RED, width=5
    )
    draw.polygon(
        [(x1 - 30, base - 14), (x1 - 52, base - 20), (x1 - 40, base - 2)],
        fill=RED,
    )
    draw.text((x0 + 14, y1 - 30), "NIKKEI  -4.8%", font=F_TAG, fill=RED)


def tower_pictogram(draw, x0, y0, x1, y1):
    """A tall tower with a missile trail and smoke."""
    cx = (x0 + x1) // 2
    draw.rectangle([x0, y0, x1, y1], fill=(226, 234, 242))
    # tower body
    draw.polygon(
        [(cx - 34, y1 - 8), (cx - 30, y0 + 52), (cx - 14, y0 + 18),
         (cx, y0 + 6), (cx + 14, y0 + 18), (cx + 30, y0 + 52),
         (cx + 34, y1 - 8)],
        fill=NAVY,
    )
    for row in range(5):
        yy = y0 + 62 + row * 18
        draw.line([cx - 26, yy, cx + 26, yy], fill=GOLD, width=3)
    # ground
    draw.rectangle([x0, y1 - 8, x1, y1], fill=GREY)
    # missile: diagonal streak top-right with smoke puffs
    draw.line([x1 - 6, y0 + 8, cx + 44, y0 + 58], fill=RED, width=5)
    draw.ellipse([x1 - 22, y0 + 2, x1 - 2, y0 + 22], fill=RED)
    for sx, sy, sr in [(x1 - 34, y0 + 30, 9), (x1 - 48, y0 + 44, 7),
                       (x1 - 60, y0 + 56, 5)]:
        draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(200, 200, 200))


def cop_pictogram(draw, x0, y0, x1, y1):
    """A globe with an oil drop crossed out: the dropped phase-out."""
    cx = (x0 + x1) // 2
    cy = (y0 + y1) // 2 - 8
    globe(draw, cx - 18, cy, 46, (214, 232, 226), TEAL)
    # oil drop
    dx, dy = cx + 52, cy + 6
    draw.polygon([(dx, dy - 34), (dx + 22, dy + 8), (dx - 22, dy + 8)], fill=INK)
    draw.ellipse([dx - 22, dy - 2, dx + 22, dy + 30], fill=INK)
    # red slash across the drop
    draw.line([dx - 30, dy - 36, dx + 30, dy + 34], fill=RED, width=6)
    draw.line([dx - 30, dy + 34, dx + 30, dy - 36], fill=RED, width=6)


def line_pictogram(draw, x0, y0, x1, y1):
    """A map strip with a dashed yellow line and an arrow crossing it."""
    draw.rectangle([x0, y0, x1, y1], fill=SAND)
    draw.rectangle([x0, y0 + 18, x1, y0 + 26], fill=(120, 140, 110))
    draw.rectangle([x0, y1 - 26, x1, y1 - 18], fill=(120, 140, 110))
    mid = (y0 + y1) // 2
    # dashed yellow line
    for xx in range(x0 + 8, x1 - 8, 26):
        draw.line([xx, mid, xx + 16, mid], fill=(240, 200, 0), width=6)
    # arrow crossing the line
    draw.line([x0 + 26, y1 - 40, x1 - 26, y0 + 40], fill=NAVY, width=5)
    draw.polygon(
        [(x1 - 26, y0 + 40), (x1 - 54, y0 + 42), (x1 - 38, y0 + 62)],
        fill=NAVY,
    )
    draw.text((x0 + 10, y0 + 6), "YELLOW LINE", font=F_TAG, fill=NAVY)


def health_pictogram(draw, x0, y0, x1, y1):
    """A medical cross in a circle with a '37 days' badge."""
    cx = (x0 + x1) // 2
    cy = (y0 + y1) // 2 - 16
    draw.ellipse([cx - 52, cy - 52, cx + 52, cy + 52], fill=TEAL)
    draw.rectangle([cx - 12, cy - 34, cx + 12, cy + 34], fill=WHITE)
    draw.rectangle([cx - 34, cy - 12, cx + 34, cy + 12], fill=WHITE)
    draw.text((cx - 34, cy + 58), "37 DAYS", font=F_TAG, fill=TEAL)


# ------------------------------------------------------------------- layout

def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- header band
    d.rectangle([0, 0, W, 104], fill=NAVY)
    globe(d, 58, 52, 32, NAVY_DARK, GOLD)
    d.text((106, 12), "THE WORLD IN ONE DAY", font=F_TITLE, fill=WHITE)
    d.text((106, 68), "FRIDAY 20 NOVEMBER 2026", font=F_DATE, fill=GOLD)
    d.text((788, 70), "make.fun", font=F_KICK, fill=(180, 195, 220))

    # ---- lead story: Anthropic debut + AI-doubt sell-off
    d.rectangle([8, 112, 400, 384], fill=CARD, outline=NAVY, width=2)
    chart_pictogram(d, 20, 124, 388, 372)
    d.text((424, 118), "MARKETS  ·  NEW YORK & TOKYO", font=F_KICK, fill=RED)
    head_lines = wrap(
        d,
        "ANTHROPIC'S $2 TRILLION DEBUT \u2014 AND THE AI-DOUBT SELL-OFF",
        F_HEAD,
        592,
    )
    draw_lines(d, 424, 148, head_lines, F_HEAD, INK, 44)
    y = 148 + len(head_lines) * 44 + 8
    body_lines = wrap(
        d,
        "Anthropic shares jump 34% on debut \u2014 the first pure-AI "
        "listing \u2014 as AI-bubble fear sinks the Nikkei 4.8% and Wall "
        "Street falls a fifth day.",
        F_BODY,
        592,
    )
    draw_lines(d, 424, y, body_lines, F_BODY, INK, 28)

    # ---- four panels, 2 x 2
    panels = [
        {
            "kicker": "CONFLICT  ·  MIDDLE EAST",
            "place": "RIYADH",
            "head": "HOUTHI MISSILE HITS TOWER",
            "body": "A missile damages the sovereign wealth fund tower in "
                    "the capital's financial district.",
            "pic": tower_pictogram,
        },
        {
            "kicker": "CLIMATE  ·  ANTALYA",
            "place": "ANTALYA, TURKEY",
            "head": "COP31 DROPS FOSSIL-FUEL EXIT",
            "body": "Negotiators strip any call to phase out fossil fuels "
                    "from the slimmed-down deal.",
            "pic": cop_pictogram,
        },
        {
            "kicker": "CONFLICT  ·  GAZA",
            "place": "CENTRAL GAZA",
            "head": "TROOPS CROSS YELLOW LINE",
            "body": "First crossing of the ceasefire boundary in central "
                    "Gaza since the truce began.",
            "pic": line_pictogram,
        },
        {
            "kicker": "HEALTH  ·  KENYA",
            "place": "NAIROBI, KENYA",
            "head": "LAST EBOLA PATIENT GOES HOME",
            "body": "Discharged 37 days after the first case \u2014 no "
                    "Ebola patients remain in care.",
            "pic": health_pictogram,
        },
    ]
    origins = [(8, 400), (520, 400), (8, 640), (520, 640)]
    for panel, (px, py) in zip(panels, origins):
        d.rectangle([px, py, px + 496, py + 232], fill=CARD, outline=NAVY, width=2)
        d.rectangle([px, py, px + 496, py + 6], fill=NAVY)
        panel["pic"](d, px + 12, py + 18, px + 152, py + 220)
        tx = px + 168
        d.text((tx, py + 16), panel["kicker"], font=F_KICK, fill=RED)
        head = wrap(d, panel["head"], F_PANEL_HEAD, 496 - 168 - 12)
        draw_lines(d, tx, py + 44, head, F_PANEL_HEAD, INK, 30)
        by = py + 44 + len(head) * 30 + 6
        body = wrap(d, panel["body"], F_PANEL_BODY, 496 - 168 - 12)
        draw_lines(d, tx, by, body, F_PANEL_BODY, INK, 24)
        d.text((tx, py + 232 - 26), panel["place"], font=F_TAG, fill=GREY)

    # ---- ticker band: also today
    d.rectangle([0, 880, W, 1016], fill=NAVY_DARK)
    d.text((16, 892), "ALSO TODAY", font=F_TICK_LABEL, fill=GOLD)
    ticker_items = [
        "UK\u2013EU agree youth-mobility deal",
        "Bukele registers for a third term",
        "Senegal boat capsizes, 4 dead",
        "US sanctions Comancheros and \u2019Ndrangheta",
        "Trump pardons Pete Rose",
        "UK sends 1,000 drones to Ukraine",
        "Kyiv hit by ballistic missiles",
        "Genoa airport halts flights after drones",
    ]
    sep = "   \u2022   "
    lines = []
    current = ""
    for item in ticker_items:
        trial = item if not current else current + sep + item
        if d.textlength(trial, font=F_TICK) <= 992:
            current = trial
        else:
            lines.append(current)
            current = item
    if current:
        lines.append(current)
    # The band holds three lines at most: drop trailing items until it fits.
    while len(lines) > 3 and ticker_items:
        ticker_items.pop()
        lines = []
        current = ""
        for item in ticker_items:
            trial = item if not current else current + sep + item
            if d.textlength(trial, font=F_TICK) <= 992:
                current = trial
            else:
                lines.append(current)
                current = item
        if current:
            lines.append(current)
    y = 918
    for line in lines:
        d.text((16, y), line, font=F_TICK, fill=WHITE)
        y += 27

    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out_path, "PNG")
    print("wrote", out_path, img.size, os.path.getsize(out_path), "bytes")


if __name__ == "__main__":
    main()
