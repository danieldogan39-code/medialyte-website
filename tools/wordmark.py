"""Erzeugt die Wortmarke „MEDIALYTE“ als SVG-Pfad (Outfit, gesperrt) – unabhängig vom Laden der Schrift.

Aufruf: python3 tools/wordmark.py  → tools/wordmark.svg
"""
import io
from pathlib import Path

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

ROOT = Path(__file__).resolve().parent.parent
FONT = ROOT / "src/assets/fonts/outfit-latin-wght-normal.woff2"
TEXT = "MEDIALYTE"
WEIGHT = 440
TRACK = 0.30          # Sperrung in em
# Optischer Ausgleich einzelner Paare (in Font-Einheiten, negativ = enger)
PAIRS = {("L", "Y"): -55, ("Y", "T"): -35, ("A", "L"): 0, ("I", "A"): -10, ("D", "I"): 0}

f = TTFont(str(FONT))
f.flavor = None
inst = instancer.instantiateVariableFont(f, {"wght": WEIGHT})
buf = io.BytesIO(); inst.save(buf); buf.seek(0)
font = TTFont(buf)
upm = font["head"].unitsPerEm
gs = font.getGlyphSet()
cmap = font.getBestCmap()
hmtx = font["hmtx"]
cap_h = font["OS/2"].sCapHeight
track = TRACK * upm

paths, x = [], 0.0
for i, ch in enumerate(TEXT):
    g = cmap[ord(ch)]
    pen = SVGPathPen(gs)
    # y nach unten: an Versalhöhe ausrichten
    gs[g].draw(TransformPen(pen, (1, 0, 0, -1, x, cap_h)))
    paths.append(pen.getCommands())
    adv = hmtx[g][0]
    x += adv
    if i < len(TEXT) - 1:
        x += track + PAIRS.get((ch, TEXT[i + 1]), 0)

# Bounding Box über alle Glyphen
from fontTools.pens.boundsPen import BoundsPen
bx = []
xx = 0.0
for i, ch in enumerate(TEXT):
    g = cmap[ord(ch)]
    bp = BoundsPen(gs)
    gs[g].draw(bp)
    if bp.bounds:
        x0, y0, x1, y1 = bp.bounds
        bx.append((xx + x0, xx + x1))
    xx += hmtx[g][0]
    if i < len(TEXT) - 1:
        xx += track + PAIRS.get((ch, TEXT[i + 1]), 0)
left = min(a for a, b in bx); right = max(b for a, b in bx)
w = right - left
d = " ".join(paths)
svg = (f'<svg class="wordmark" viewBox="{left:.0f} 0 {w:.0f} {cap_h}" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" focusable="false">'
       f'<path fill="currentColor" d="{d}"/></svg>')
(ROOT / "tools/wordmark.svg").write_text(svg)
print("cap", cap_h, "width", round(w), "ratio", round(w / cap_h, 3), "bytes", len(svg))
