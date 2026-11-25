"""Render the 25 November 2026 front page: THE WORLD bulletin edition.

Design (new for this day): a wire-service bulletin.
  ticker bar -> nameplate -> lead band (illustration left, text right)
  -> triptych of three columns -> footer row of three short items -> source line.
Fonts: Liberation Serif for display, Liberation Sans for decks.
Deterministic: no clock, no randomness, fixed paths, fixed colours.
"""
import json
import os
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = "/usr/share/fonts/truetype/liberation"

PAPER = (247, 243, 234)
INK = (20, 20, 20)
RED = (176, 30, 36)
TEAL = (15, 76, 76)
GOLD = (200, 155, 60)
GREY = (110, 105, 95)
LIGHT = (232, 226, 214)
DARKPANEL = (18, 58, 58)

W = 1024
H = 1024
MARGIN = 36
CW = W - 2 * MARGIN  # 952


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = "LiberationSerif-Bold.ttf"
SERIF = "LiberationSerif-Regular.ttf"
SANS_B = "LiberationSans-Bold.ttf"
SANS = "LiberationSans-Regular.ttf"


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines, each within max_w."""
    words = text.split()
    lines = []
    cur = ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, text, fnt, x, y, max_w, max_lines, leading, fill=INK):
    lines = wrap(draw, text, fnt, max_w)
    assert len(lines) <= max_lines, f"overflow: {len(lines)} > {max_lines} for {text!r}"
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


class Bulletin:
    def __init__(self, data):
        self.data = data
        self.img = Image.new("RGB", (W, H), PAPER)
        self.d = ImageDraw.Draw(self.img)

    # -- icons (simple geometric marks, one per story) -------------------
    def mark_rocket(self, x, y, s, ink):
        d = self.d
        d.polygon([(x + s // 2, y), (x + s, y + s * 3 // 4),
                   (x + s // 2, y + s * 5 // 8), (x, y + s * 3 // 4)], fill=ink)
        d.polygon([(x + s // 2, y + s * 5 // 8), (x + s * 3 // 8, y + s),
                   (x + s * 5 // 8, y + s)], fill=RED)
        d.ellipse([x + s * 3 // 8, y + s // 4, x + s * 5 // 8, y + s // 2],
                  fill=PAPER)

    def mark_tower(self, x, y, s, ink):
        d = self.d
        d.rectangle([x + s // 4, y, x + s * 3 // 4, y + s], fill=ink)
        d.rectangle([x + s // 3, y - s // 6, x + s * 2 // 3, y], fill=ink)
        for row in range(5):
            yy = y + s // 6 + row * s // 6
            d.rectangle([x + s * 5 // 16, yy, x + s * 11 // 16, yy + s // 12],
                        fill=GOLD)

    def mark_factory(self, x, y, s, ink):
        d = self.d
        d.rectangle([x, y + s // 3, x + s, y + s], fill=ink)
        d.rectangle([x + s // 8, y, x + s // 4, y + s // 2], fill=ink)
        d.rectangle([x + s * 3 // 8, y + s // 6, x + s // 2, y + s // 2],
                    fill=ink)
        d.polygon([(x, y + s // 3), (x + s // 4, y + s // 6),
                   (x + s // 2, y + s // 3)], fill=RED)

    def mark_shaft(self, x, y, s, ink):
        d = self.d
        d.rectangle([x + s // 4, y, x + s * 3 // 4, y + s], fill=ink)
        for row in range(4):
            yy = y + s // 8 + row * s // 5
            d.line([x + s // 4, yy, x + s * 3 // 4, yy], fill=GOLD, width=3)
        d.ellipse([x + s * 3 // 8, y + s * 3 // 4, x + s * 5 // 8, y + s],
                  fill=RED)

    def mark_flag(self, x, y, s, ink):
        d = self.d
        d.line([x + s // 6, y, x + s // 6, y + s], fill=ink, width=4)
        d.polygon([(x + s // 6, y), (x + s, y + s // 6),
                   (x + s // 6, y + s // 3)], fill=RED)
        d.rectangle([x, y + s, x + s // 2, y + s + 6], fill=ink)

    def mark_podium(self, x, y, s, ink):
        d = self.d
        d.polygon([(x, y + s), (x + s // 5, y + s // 3),
                   (x + s * 2 // 5, y + s // 3), (x + s * 3 // 5, y + s)],
                  fill=ink)
        d.polygon([(x + s, y + s), (x + s * 4 // 5, y + s // 3),
                   (x + s * 3 // 5, y + s // 3), (x + s * 2 // 5, y + s)],
                  fill=TEAL)
        d.ellipse([x + s // 4, y, x + s * 3 // 4, y + s // 4], fill=GOLD)

    # -- bands ------------------------------------------------------------
    def ticker(self):
        d = self.d
        d.rectangle([0, 26, W, 58], fill=INK)
        left = font(SANS_B, 21)
        right = font(SANS_B, 21)
        d.text((MARGIN, 30), "THE WORLD  —  " + self.data["dateline"],
               font=left, fill=PAPER)
        tag = self.data["tagline"]
        d.text((W - MARGIN - d.textlength(tag, font=right), 30), tag,
               font=right, fill=GOLD)

    def nameplate(self):
        d = self.d
        d.line([MARGIN, 66, W - MARGIN, 66], fill=INK, width=3)
        name = font(SERIF_B, 96)
        title = self.data["paper"]
        d.text(((W - d.textlength(title, font=name)) // 2, 72), title,
               font=name, fill=INK)
        d.line([MARGIN, 176, W - MARGIN, 176], fill=INK, width=3)
        sub = font(SANS, 22)
        line = "THE DAY IN SEVEN STORIES  •  WEDNESDAY 25 NOVEMBER 2026"
        d.text(((W - d.textlength(line, font=sub)) // 2, 186), line,
               font=sub, fill=GREY)

    def lead_art(self, x, y, w, h):
        d = self.d
        d.rectangle([x, y, x + w, y + h], fill=DARKPANEL)
        # skyline silhouette
        for bx, bw, bh in [(18, 46, 120), (76, 34, 168), (122, 52, 96),
                           (186, 38, 148), (236, 44, 110)]:
            d.rectangle([x + bx, y + h - 40 - bh, x + bx + bw, y + h - 40],
                        fill=(8, 34, 34))
        # rescue beacon: white disc, green check
        cx, cy, r = x + w // 2, y + 78, 46
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=PAPER)
        d.line([cx - 22, cy, cx - 6, cy + 16], fill=(34, 139, 34), width=9)
        d.line([cx - 6, cy + 16, cx + 24, cy - 20], fill=(34, 139, 34),
               width=9)
        # three figures below the beacon
        for fx in (x + 66, x + w // 2 - 8, x + w - 82):
            d.ellipse([fx, y + 168, fx + 16, y + 184], fill=GOLD)
            d.rounded_rectangle([fx - 2, y + 188, fx + 18, y + 224],
                                radius=7, fill=PAPER)
        d.text((x + 14, y + h - 30), "CARTAGENA, COLOMBIA",
               font=font(SANS_B, 18), fill=GOLD)

    def lead(self):
        d = self.d
        lead = self.data["lead"]
        self.lead_art(MARGIN, 222, 316, 232)
        tx = MARGIN + 316 + 28
        tw = W - MARGIN - tx
        d.text((tx, 224), lead["kicker"], font=font(SANS_B, 23), fill=RED)
        y = draw_wrapped(d, lead["headline"], font(SERIF_B, 52), tx, 256,
                         tw, 2, 58)
        draw_wrapped(d, lead["deck"], font(SANS, 26), tx, y + 10, tw, 2, 34,
                     fill=(60, 58, 52))

    def triptych(self):
        d = self.d
        d.line([MARGIN, 478, W - MARGIN, 478], fill=INK, width=2)
        marks = [self.mark_rocket, self.mark_tower, self.mark_factory]
        col_w = 304
        for i, story in enumerate(self.data["triptych"]):
            x = MARGIN + i * (col_w + 20)
            marks[i](x, 496, 46, TEAL)
            d.text((x, 552), story["kicker"], font=font(SANS_B, 19),
                   fill=RED)
            y = draw_wrapped(d, story["headline"], font(SERIF_B, 27), x,
                             580, col_w, 2, 33)
            draw_wrapped(d, story["deck"], font(SANS, 19), x, y + 8, col_w,
                         3, 24, fill=(60, 58, 52))
            if i < 2:
                d.line([x + col_w + 10, 496, x + col_w + 10, 726],
                       fill=LIGHT, width=2)

    def footer_row(self):
        d = self.d
        d.line([MARGIN, 746, W - MARGIN, 746], fill=INK, width=2)
        marks = [self.mark_shaft, self.mark_flag, self.mark_podium]
        col_w = 304
        for i, story in enumerate(self.data["footer_row"]):
            x = MARGIN + i * (col_w + 20)
            marks[i](x, 768, 44, TEAL)
            tx = x + 60
            tw = col_w - 60
            d.text((tx, 766), story["kicker"], font=font(SANS_B, 17),
                   fill=RED)
            y = draw_wrapped(d, story["headline"], font(SERIF_B, 22), tx,
                             790, tw, 2, 27)
            draw_wrapped(d, story["deck"], font(SANS, 17), tx, y + 6, tw, 3,
                         22, fill=(60, 58, 52))
            if i < 2:
                d.line([x + col_w + 10, 768, x + col_w + 10, 920],
                       fill=LIGHT, width=2)

    def footer(self):
        d = self.d
        d.line([MARGIN, 940, W - MARGIN, 940], fill=INK, width=2)
        fnt = font(SANS, 17)
        line = self.data["footer"]
        d.text(((W - d.textlength(line, font=fnt)) // 2, 952), line,
               font=fnt, fill=GREY)
        fnt2 = font(SERIF_B, 20)
        end = "THE WORLD  •  25 NOVEMBER 2026"
        d.text(((W - d.textlength(end, font=fnt2)) // 2, 978), end,
               font=fnt2, fill=INK)

    def compose(self):
        self.ticker()
        self.nameplate()
        self.lead()
        self.triptych()
        self.footer_row()
        self.footer()
        return self.img


def main():
    with open(os.path.join(HERE, "news.json"), encoding="utf-8") as fh:
        data = json.load(fh)
    img = Bulletin(data).compose()
    out = os.path.join(HERE, "entry.png")
    img.save(out, "PNG")
    print("wrote", out, img.size)


if __name__ == "__main__":
    main()
