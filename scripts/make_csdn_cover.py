#!/usr/bin/env python3
"""Render the CSDN cover for the boundary write-up.

Same rules as `make_demo_gif.py`: every number is copied from
`docs/dry-run-scorecard.md` and `docs/content/csdn.md`. Nothing is rounded up
for effect.

The canvas is 1200x675 (16:9), which is the ratio the CSDN editor crops to.
The layout assumes the image will also be seen as a ~240px wide thumbnail in
the article list, so there is exactly one oversized number and one second line
of text; everything else is decoration that is allowed to disappear.

Usage:
    python scripts/make_csdn_cover.py
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "csdn-cover.png"
FONT_DIR = Path("C:/Windows/Fonts")

W, H = 1200, 675
MARGIN = 80

BG = (11, 11, 12)
FG = (232, 232, 234)
MUTED = (139, 139, 149)
DIM = (104, 104, 114)
ACCENT = (110, 231, 168)
BORDER = (38, 38, 43)
TRACK_BG = (34, 34, 39)

BIG_NUM = "94.5"
BIG_PCT = "%"
LINE_A = "的 Agent Skill"
LINE_B = "没写「什么时候不该用」"
CAPTION = "275 个已安装 skill，只有 15 个写了边界"
KICKER = "AGENT SKILL"
PLATFORMS = "CLAUDE CODE · CODEX · CURSOR"
FOOTER = "8 道门禁 · 16/16 · SHIP"
URL = "github.com/YaBoom/skill-forge"

# The bar is a scale drawing of the sample, not a decoration: 15 of 275.
BAR_TOTAL = 275
BAR_MARKED = 15


def load(name: str, size: int) -> ImageFont.FreeTypeFont:
    path = FONT_DIR / name
    if path.exists():
        return ImageFont.truetype(str(path), size)
    return ImageFont.load_default(size=size)


BIG = load("seguibl.ttf", 268)
PCT = load("seguibl.ttf", 140)
CN = load("msyhbd.ttc", 52)
CN_BIG = load("msyhbd.ttc", 60)
CN_SM = load("msyh.ttc", 16)
CN_FOOT = load("msyhbd.ttc", 13)
LABEL = load("seguibl.ttf", 12)
MICRO = load("segoeuib.ttf", 11)
MONO_SM = load("consola.ttf", 13)


def tracked(d: ImageDraw.ImageDraw, x: float, baseline: float, text: str,
            font: ImageFont.FreeTypeFont, fill, spacing: float) -> float:
    """Draw letter-spaced text on a baseline and return the right edge."""
    cx = x
    for ch in text:
        d.text((cx, baseline), ch, font=font, fill=fill, anchor="ls")
        cx += d.textlength(ch, font=font) + spacing
    return cx - spacing


def tracked_width(d: ImageDraw.ImageDraw, text: str,
                  font: ImageFont.FreeTypeFont, spacing: float) -> float:
    if not text:
        return 0.0
    return sum(d.textlength(ch, font=font) for ch in text) + spacing * (len(text) - 1)


def main() -> int:
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # --- brand rail ----------------------------------------------------------
    d.rectangle([0, 0, W, 4], fill=ACCENT)

    # --- kicker row ----------------------------------------------------------
    d.rectangle([MARGIN, 62, MARGIN + 7, 69], fill=ACCENT)
    tracked(d, MARGIN + 18, 74, KICKER, LABEL, ACCENT, 3.4)
    pw = tracked_width(d, PLATFORMS, MICRO, 2.2)
    tracked(d, W - MARGIN - pw, 74, PLATFORMS, MICRO, DIM, 2.2)

    # --- the number ---------------------------------------------------------
    base = 320
    # Draw the digits one by one so the % sits against the ink, not the advance width.
    right = tracked(d, MARGIN, base, BIG_NUM, BIG, FG, -3.0)
    # Optically centre the smaller % on the digits' cap height (roughly 0.55 of it).
    d.text((right + 4, base - 26), BIG_PCT, font=PCT, fill=MUTED, anchor="ls")

    # --- the claim ----------------------------------------------------------
    y = base + 84
    head_w = d.textlength("的", font=CN) + 9
    d.text((MARGIN, y), "的", font=CN, fill=MUTED, anchor="ls")
    d.text((MARGIN + head_w, y), "Agent Skill", font=CN, fill=ACCENT, anchor="ls")
    d.text((MARGIN, y + 74), LINE_B, font=CN_BIG, fill=FG, anchor="ls")

    # --- evidence bar -------------------------------------------------------
    top = 536
    d.line([(MARGIN, top - 26), (W - MARGIN, top - 26)], fill=BORDER)
    width = W - MARGIN * 2
    d.rounded_rectangle([MARGIN, top, W - MARGIN, top + 8], radius=4, fill=TRACK_BG)
    marked = round(width * BAR_MARKED / BAR_TOTAL)
    d.rounded_rectangle([MARGIN, top, MARGIN + max(marked, 8), top + 8],
                        radius=4, fill=ACCENT)

    d.text((MARGIN, top + 40), CAPTION, font=CN_SM, fill=MUTED, anchor="ls")

    # --- footer -------------------------------------------------------------
    tracked(d, MARGIN, H - 34, FOOTER, CN_FOOT, ACCENT, 0.8)
    uw = d.textlength(URL, font=MONO_SM)
    d.text((W - MARGIN - uw, H - 34), URL, font=MONO_SM, fill=DIM, anchor="ls")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUT, optimize=True)
    size_kb = OUT.stat().st_size / 1024
    print(f"wrote {OUT.relative_to(ROOT)}  {W}x{H}  {size_kb:.0f} KB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
