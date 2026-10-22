#!/usr/bin/env python3
"""Render the README hero animation from the recorded dry run.

Every number in the animation is copied from `docs/dry-run-scorecard.md`, which is
the author's own run recorded against `examples/sync-skill-mirror`. Nothing here is
invented: the eight gates, the 16/16 total, the evidence counts and the trigger test
counts all exist in that file.

This is a rendering of a real transcript, not a screen recording. The README says so
next to the image.

Usage:
    python scripts/make_demo_gif.py
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "demo.gif"
FONT_DIR = Path("C:/Windows/Fonts")

W, H = 900, 572
FRAME_MS = 50

BG = (11, 11, 12)
CHROME = (18, 18, 21)
BORDER = (38, 38, 43)
FG = (232, 232, 234)
MUTED = (139, 139, 149)
DIM = (104, 104, 114)
ACCENT = (110, 231, 168)
BADGE_BG = (22, 54, 40)

GATES = [
    "Trigger precision",
    "Progressive disclosure",
    "Token budget",
    "Executability",
    "Evidence anchoring",
    "Safety",
    "Portability",
    "Provability",
]

REQUEST = "Turn what we just did into a reusable skill."
EVIDENCE = "5 evidence signals · 1 redaction · 0 inferred steps"
TESTS = "5 positive · 3 negative trigger tests · dry run executed twice"
OUTPUT = "examples/sync-skill-mirror/SKILL.md · 103 lines · ~890 tokens"


def load(name: str, size: int) -> ImageFont.FreeTypeFont:
    path = FONT_DIR / name
    if path.exists():
        return ImageFont.truetype(str(path), size)
    return ImageFont.load_default(size=size)


MONO = load("consola.ttf", 15)
MONO_SM = load("consola.ttf", 12)
MONO_LG = load("consolab.ttf", 21)
UI = load("segoeui.ttf", 15)
UI_SM = load("segoeui.ttf", 13)
UI_BOLD = load("segoeuib.ttf", 15)
TOTAL = load("segoeuib.ttf", 26)


def mix(a: tuple[int, int, int], b: tuple[int, int, int], t: float) -> tuple[int, int, int]:
    """Blend a toward b by t, used to fake alpha on a flat background."""
    t = max(0.0, min(1.0, t))
    return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))  # type: ignore[return-value]


def tracked(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str,
            font: ImageFont.FreeTypeFont, fill, spacing: int = 2) -> None:
    """Draw letter-spaced text, the way section labels read in the landing page."""
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill)
        x += draw.textlength(ch, font=font) + spacing


def check_mark(draw: ImageDraw.ImageDraw, x: int, y: int, size: int, color) -> None:
    """Vector tick so the glyph never falls back to a missing codepoint."""
    w = max(2, size // 5)
    draw.line([(x + size * 0.10, y + size * 0.52), (x + size * 0.40, y + size * 0.82)],
              fill=color, width=w)
    draw.line([(x + size * 0.40, y + size * 0.82), (x + size * 0.92, y + size * 0.16)],
              fill=color, width=w)


def base_frame() -> tuple[Image.Image, ImageDraw.ImageDraw]:
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 46], fill=CHROME)
    d.line([(0, 46), (W, 46)], fill=BORDER)
    for i in range(3):
        cx = 22 + i * 18
        d.ellipse([cx - 5, 18, cx + 5, 28], fill=(86, 86, 96))
    d.text((84, 15), "skill-forge · dry run", font=UI_SM, fill=MUTED)
    return img, d


def render(i: int) -> Image.Image:
    img, d = base_frame()

    # --- stage 1: the request types itself in ---------------------------------
    typed = min(len(REQUEST), -(-(i + 1) * len(REQUEST) // 24))
    d.text((26, 74), ">", font=MONO, fill=ACCENT)
    d.text((44, 74), REQUEST[:typed], font=MONO, fill=FG)
    if i < 24:
        cx = 44 + d.textlength(REQUEST[:typed], font=MONO) + 2
        d.rectangle([cx, 75, cx + 7, 92], fill=ACCENT)

    # --- stage 2: harvest summary ---------------------------------------------
    if i >= 24:
        t = min(1.0, (i - 24) / 4)
        d.text((44, 100), EVIDENCE, font=MONO_SM, fill=mix(BG, DIM, t))

    # --- stage 3: gates fill in ----------------------------------------------
    if i >= 28:
        d.line([(26, 132), (W - 26, 132)], fill=BORDER)
        d.line([(26, 438), (W - 26, 438)], fill=BORDER)
        tracked(d, (26, 142), "EIGHT GATES", UI_SM, MUTED)

        shown = min(8, (i - 28) // 3 + 1)
        counter = f"{shown}/8"
        cw = d.textlength(counter, font=MONO_SM)
        d.text((W - 30 - cw, 143), counter, font=MONO_SM, fill=ACCENT)

        for k in range(shown):
            row_top = 170 + k * 32
            step = i - (28 + k * 3)
            t = 1.0 if step >= 2 else (0.55 if step == 1 else 0.25)
            dy = 0 if step >= 2 else (3 if step == 1 else 6)
            color = mix(BG, FG, t)
            check_mark(d, 26, row_top + 6 + dy, 13, mix(BG, ACCENT, t))
            d.text((52, row_top + dy), GATES[k], font=UI, fill=color)
            score = "2/2"
            sw = d.textlength(score, font=MONO)
            d.text((W - 30 - sw, row_top + 1 + dy), score, font=MONO, fill=mix(BG, ACCENT, t))

    # --- stage 4: verdict ----------------------------------------------------
    if i >= 52:
        t = min(1.0, (i - 52) / 5)
        d.text((26, 456), "total", font=UI, fill=mix(BG, MUTED, t))
        d.text((78, 448), "16/16", font=TOTAL, fill=mix(BG, ACCENT, t))

        # a badge that draws itself left-to-right
        bx, by, bw, bh = W - 130, 452, 104, 30
        grow = int(bw * t)
        d.rounded_rectangle([bx, by, bx + grow, by + bh], radius=6, fill=mix(BG, BADGE_BG, t))
        if t > 0.75:
            d.text((bx + 20, by + 7), "SHIP", font=UI_BOLD, fill=mix(BADGE_BG, ACCENT, (t - 0.75) / 0.25))

    # --- stage 5: proof line -------------------------------------------------
    if i >= 58:
        t = min(1.0, (i - 58) / 3)
        d.text((26, 502), TESTS, font=UI_SM, fill=mix(BG, DIM, t))
    if i >= 62:
        t = min(1.0, (i - 62) / 3)
        d.text((26, 532), "output", font=MONO_SM, fill=mix(BG, ACCENT, t))
        d.text((78, 530), OUTPUT, font=MONO_SM, fill=mix(BG, MUTED, t))

    return img


def main() -> int:
    typing, gates, tail = 24, 24, 30
    total_frames = typing + 4 + gates + 6 + 4 + tail

    frames = [render(i) for i in range(total_frames)]

    # One shared palette keeps the file small and the flat background clean.
    master = frames[-1].quantize(colors=96, method=Image.MEDIANCUT, dither=Image.NONE)
    paletted = [f.quantize(palette=master, dither=Image.NONE) for f in frames]

    OUT.parent.mkdir(parents=True, exist_ok=True)
    paletted[0].save(
        OUT,
        save_all=True,
        append_images=paletted[1:],
        duration=FRAME_MS,
        loop=0,
        optimize=True,
        disposal=1,
    )
    size_kb = OUT.stat().st_size / 1024
    print(f"wrote {OUT.relative_to(ROOT)}  {total_frames} frames  {size_kb:.0f} KB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
