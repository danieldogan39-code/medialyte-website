"""Erzeugt die Wortmarke „medialyte“ als SVG-Pfad – unabhängig vom Laden einer Schrift.

Schrift: Red Hat Display Italic (SIL Open Font License, tools/fonts/). Modern, leicht geschwungen
und mit derselben Neigung wie das handgeschriebene ML-Zeichen daneben.

Aufruf: python3 tools/wordmark.py  → tools/wordmark.svg
"""
import io
from pathlib import Path

from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

ROOT = Path(__file__).resolve().parent.parent
FONT = ROOT / "tools/fonts/red-hat-display-latin-wght-italic.woff2"
TEXT = "medialyte"
WEIGHT = 640
TRACK = -0.012        # Laufweite in em (leicht enger, wirkt geschlossener)
# Optischer Ausgleich einzelner Paare (in Font-Einheiten, negativ = enger)
PAIRS = {("l", "y"): -14, ("y", "t"): -10, ("i", "a"): 6, ("d", "i"): 4}

f = TTFont(str(FONT))
f.flavor = None
inst = instancer.instantiateVariableFont(f, {"wght": WEIGHT})
buf = io.BytesIO(); inst.save(buf); buf.seek(0)
font = TTFont(buf)
upm = font["head"].unitsPerEm
gs = font.getGlyphSet()
cmap = font.getBestCmap()
hmtx = font["hmtx"]
os2 = font["OS/2"]
x_h = os2.sxHeight
track = TRACK * upm

# Kerning der Schrift (GPOS) ist für diese kurze Zeichenfolge vernachlässigbar; Paare oben gleichen aus.
pos, x = [], 0.0
for i, ch in enumerate(TEXT):
    g = cmap[ord(ch)]
    pos.append((g, x))
    x += hmtx[g][0]
    if i < len(TEXT) - 1:
        x += track + PAIRS.get((ch, TEXT[i + 1]), 0)

# Grenzen aller Glyphen (y nach oben)
x0s, x1s, y0s, y1s = [], [], [], []
for g, gx in pos:
    bp = BoundsPen(gs)
    gs[g].draw(bp)
    if bp.bounds:
        a, b, c, d = bp.bounds
        x0s.append(gx + a); x1s.append(gx + c); y0s.append(b); y1s.append(d)
left, right, bottom, top = min(x0s), max(x1s), min(y0s), max(y1s)

paths = []
for g, gx in pos:
    pen = SVGPathPen(gs)
    # y nach unten, Oberkante der höchsten Glyphe = 0
    gs[g].draw(TransformPen(pen, (1, 0, 0, -1, gx, top)))
    paths.append(pen.getCommands())
w, h = right - left, top - bottom
d = " ".join(paths)
svg = (f'<svg class="wordmark" viewBox="{left:.0f} 0 {w:.0f} {h:.0f}" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" focusable="false">'
       f'<path fill="currentColor" d="{d}"/></svg>')
(ROOT / "tools/wordmark.svg").write_text(svg)
# Maße für das CSS: Höhe der Marke in em der Schriftgröße, Lage der Grundlinie und Mittellänge
print(f"upm {upm}  Höhe {h:.0f} ({h / upm:.3f} em)  Breite {w:.0f} ({w / h:.3f} × Höhe)  "
      f"Grundlinie bei {top / h:.3f} der Höhe  x-Höhe {x_h} ({x_h / h:.3f} der Höhe)  bytes {len(svg)}")
