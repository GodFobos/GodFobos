"""Shared toolkit for the Night City profile graphics.

Text is converted to SVG paths, so the banners look identical everywhere:
GitHub renders README images through <img>, which can't load web fonts.
"""
from functools import lru_cache
from pathlib import Path

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

FONTS = Path(__file__).parent / "fonts"

# Night City palette
BG = "#07070d"
BG2 = "#0d0d18"
YELLOW = "#fcee0a"
CYAN = "#00f0ff"
RED = "#ff003c"
MAGENTA = "#ff2bd6"
DIM = "#5a5a78"
TEXT = "#d8d8f0"


@lru_cache(maxsize=None)
def _font(name):
    f = TTFont(FONTS / f"{name}.ttf")
    return f, f.getGlyphSet(), f.getBestCmap(), f["hmtx"], f["head"].unitsPerEm


def text_width(s, font, size, spacing=0.0):
    f, gs, cmap, hmtx, upm = _font(font)
    scale = size / upm
    w = 0.0
    for ch in s:
        g = cmap.get(ord(ch)) or cmap.get(ord("?"))
        w += hmtx[g][0] * scale + spacing
    return max(0.0, w - spacing) if s else 0.0


def text_path(s, x, y, font, size, spacing=0.0, anchor="start"):
    """Return the SVG path data for string *s* with its baseline at (x, y)."""
    f, gs, cmap, hmtx, upm = _font(font)
    scale = size / upm
    if anchor != "start":
        w = text_width(s, font, size, spacing)
        x -= w if anchor == "end" else w / 2
    pen = SVGPathPen(gs, ntos=lambda v: f"{v:.1f}".rstrip("0").rstrip("."))
    cx = x
    for ch in s:
        g = cmap.get(ord(ch)) or cmap.get(ord("?"))
        if ch != " ":
            tp = TransformPen(pen, (scale, 0, 0, -scale, cx, y))
            gs[g].draw(tp)
        cx += hmtx[g][0] * scale + spacing
    return pen.getCommands()


def T(s, x, y, font="rajdhani-700", size=16, fill=TEXT, spacing=0.0,
      anchor="start", extra=""):
    """A <path> element that renders text."""
    d = text_path(s, x, y, font, size, spacing, anchor)
    return f'<path d="{d}" fill="{fill}" {extra}/>'


def svg(w, h, body, title, style=""):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" role="img" aria-label="{title}">'
        f"<title>{title}</title>"
        f"<style>{style}</style>{body}</svg>\n"
    )


def glow_filter(fid, color, std=4, strength=2):
    merges = "".join('<feMergeNode in="b"/>' for _ in range(strength))
    return (
        f'<filter id="{fid}" x="-50%" y="-50%" width="200%" height="200%">'
        f'<feGaussianBlur stdDeviation="{std}" result="b0"/>'
        f'<feFlood flood-color="{color}"/><feComposite in2="b0" operator="in" result="b"/>'
        f'<feMerge>{merges}<feMergeNode in="SourceGraphic"/></feMerge></filter>'
    )


def frame(w, h, color=YELLOW, cut=22, inset=1.5, sw=2, extra=""):
    """Cyberpunk panel outline with clipped corners."""
    i, c = inset, cut
    pts = (f"{i+c},{i} {w-i},{i} {w-i},{h-i-c} {w-i-c},{h-i} "
           f"{i},{h-i} {i},{i+c}")
    return f'<polygon points="{pts}" fill="none" stroke="{color}" stroke-width="{sw}" {extra}/>'


def runner(w, h, color=YELLOW, cut=22, inset=1.5, sw=3, dur=7, length=160, name="run"):
    """A light pulse that travels around the clipped panel outline."""
    i, c = inset, cut
    pts = (f"{i+c},{i} {w-i},{i} {w-i},{h-i-c} {w-i-c},{h-i} "
           f"{i},{h-i} {i},{i+c}")
    diag = (2 * c * c) ** 0.5
    per = 2 * (w - 2 * i) + 2 * (h - 2 * i) - 4 * c + 2 * diag
    return (
        f'<style>@keyframes {name}{{from{{stroke-dashoffset:0}}to{{stroke-dashoffset:-{per:.0f}}}}}'
        f'.{name}{{stroke-dasharray:{length} {per - length:.0f};animation:{name} {dur}s linear infinite}}</style>'
        f'<polygon class="{name}" points="{pts}" fill="none" stroke="{color}" stroke-width="{sw}" '
        f'stroke-linecap="square" filter="url(#runglow)"/>'
        f'<polygon class="{name}" style="animation-delay:-{dur/2}s" points="{pts}" fill="none" stroke="{color}" '
        f'stroke-width="{sw}" filter="url(#runglow)"/>'
    )


def runglow(color):
    return glow_filter("runglow", color, 4, 2)


def panel_clip(cid, w, h, cut=22, inset=1.5):
    i, c = inset, cut
    pts = (f"{i+c},{i} {w-i},{i} {w-i},{h-i-c} {w-i-c},{h-i} "
           f"{i},{h-i} {i},{i+c}")
    return f'<clipPath id="{cid}"><polygon points="{pts}"/></clipPath>'
