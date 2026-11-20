#!/usr/bin/env python3
"""Draw the entry image: the world news of Thursday 19 November 2026 in one picture.

A dark broadsheet-style infographic composed with Pillow: every word is real,
spelled text — no generated imagery, no garbled lettering.
Run:  python3 draw_image.py
Writes entry.png (1024 x 1024) next to this file, deterministically.
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
NAVY = (11, 20, 40)
PANEL = (22, 34, 62)
PANEL2 = (16, 27, 52)
GOLD = (232, 184, 84)
CREAM = (244, 238, 224)
WHITE = (255, 255, 255)
MUTED = (168, 178, 198)
RULE = (232, 184, 84)
RED = (226, 88, 66)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(f"{FONT_DIR}/{name}", size)


F_MAST = font("DejaVuSerif-Bold.ttf", 58)
F_DATE = font("DejaVuSans-Bold.ttf", 30)
F_LEAD_K = font("DejaVuSans-Bold.ttf", 20)
F_LEAD_H = font("DejaVuSerif-Bold.ttf", 44)
F_LEAD_B = font("DejaVuSans.ttf", 24)
F_KICK = font("DejaVuSans-Bold.ttf", 18)
F_HEAD = font("DejaVuSans-Bold.ttf", 27)
F_BODY = font("DejaVuSans.ttf", 21)
F_TICK = font("DejaVuSans-Bold.ttf", 20)
F_FOOT = font("DejaVuSans.ttf", 16)


def wrap(draw, text, fnt, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


img = Image.new("RGB", (W, H), NAVY)
d = ImageDraw.Draw(img)

# ---- masthead ----
d.text((48, 34), "THE WORLD TODAY", font=F_MAST, fill=CREAM)
d.text((48, 104), "THURSDAY 19 NOVEMBER 2026", font=F_DATE, fill=GOLD)
d.line([(48, 152), (976, 152)], fill=RULE, width=3)

# ---- lead story ----
lead = (48, 176, 976, 470)
d.rounded_rectangle(lead, radius=14, fill=PANEL)
d.rectangle([48, 176, 62, 470], fill=GOLD)
d.text((84, 196), "SHENZHEN  ·  APEC SUMMIT", font=F_LEAD_K, fill=GOLD)
d.text((84, 226), "Three leaders, one table", font=F_LEAD_H, fill=WHITE)
body = ("Trump, Putin and Xi met in a rare three-way summit on the sidelines "
        "of APEC in Shenzhen and issued a four-point \u201cDeclaration toward "
        "Peace\u201d \u2014 a nod toward peace, not a peace deal.")
y = 292
for line in wrap(d, body, F_LEAD_B, 976 - 84 - 36):
    d.text((84, y), line, font=F_LEAD_B, fill=CREAM)
    y += 32
d.text((84, 420), "THE DAY\u2019S BIGGEST STORY", font=F_KICK, fill=MUTED)

# ---- 2 x 2 grid ----
stories = [
    ("THE HAGUE", "Justice for the Rohingya",
     "The UN\u2019s top court ruled 9\u20136 that Myanmar committed genocide "
     "against the Rohingya in 2017 \u2014 a landmark verdict in Gambia\u2019s case.",
     RED),
    ("WALL STREET", "Anthropic\u2019s $2tn debut",
     "The AI lab\u2019s Nasdaq listing valued it at about $2 trillion, edging "
     "past SpaceX and capping a blockbuster AI debut.",
     GOLD),
    ("UKRAINE", "Crimea bridge hit again",
     "Putin\u2019s prized bridge to occupied Crimea was struck for a third time "
     "this week; he vowed a \u201cfar more painful\u201d response.",
     RED),
    ("WASHINGTON", "Pardon for Pete Rose",
     "Trump posthumously pardoned the late baseball legend for tax crimes \u2014 "
     "the latest step in rehabilitating the banned slugger.",
     GOLD),
]
gx, gy = 48, 494
cw, ch, gap = 452, 196, 24
for i, (kick, head, text, accent) in enumerate(stories):
    x = gx + (i % 2) * (cw + gap)
    y0 = gy + (i // 2) * (ch + gap)
    d.rounded_rectangle([x, y0, x + cw, y0 + ch], radius=12, fill=PANEL2)
    d.rectangle([x, y0, x + 6, y0 + ch], fill=accent)
    d.text((x + 24, y0 + 14), kick, font=F_KICK, fill=accent)
    d.text((x + 24, y0 + 40), head, font=F_HEAD, fill=WHITE)
    yy = y0 + 82
    for line in wrap(d, text, F_BODY, cw - 48):
        d.text((x + 24, yy), line, font=F_BODY, fill=MUTED)
        yy += 27

# ---- ticker (two lines, so nothing is cut off) ----
d.rectangle([0, 918, W, 918 + 2], fill=RULE)
tick1 = ("ALSO  ·  Fiona the hippo dies at Cincinnati Zoo  ·  Van Gogh sells for a "
         "record $190.4m  ·  Bukele seeks a third term")
tick2 = ("US Senate rejects Iran war-powers vote 51\u201348  ·  EU proposes "
         "\u20ac45bn Ukraine loan")
d.text((48, 926), tick1, font=F_TICK, fill=GOLD)
d.text((48, 954), tick2, font=F_TICK, fill=GOLD)
d.text((48, 986), "Sources: BBC · Reuters · AP · Al Jazeera  —  19 November 2026",
       font=F_FOOT, fill=MUTED)

img.save("entry.png", format="PNG", optimize=True)
print("wrote entry.png", img.size)
