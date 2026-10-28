"""Erzeugt die Wortmarke „medialyte“ als SVG-Pfad – unabhängig vom Laden einer Schrift.

Schrift: Montserrat Alternates SemiBold (SIL Open Font License, tools/fonts/). Aufrecht, mit den
runden Sonderformen der Alternates-Familie; gesetzt mit HarfBuzz (Unterschneidung der Schrift).

Aufruf: python3 tools/wordmark.py  → tools/wordmark.svg   (benötigt: fonttools, uharfbuzz)
"""
import io
from pathlib import Path

import uharfbuzz as hb
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parent.parent
FONT = ROOT / "tools/fonts/montserrat-alternates-latin-600-normal.woff2"
TEXT = "medialyte"
WEIGHT = 600          # nur für variable Schriften
TRACK = -0.02         # Laufweite in em (leicht enger, wirkt geschlossener)
# Optischer Ausgleich einzelner Paare (in Font-Einheiten, negativ = enger), zusätzlich zur Unterschneidung
PAIRS = {}

f = TTFont(str(FONT))
f.flavor = None
if "fvar" in f:
    from fontTools.varLib import instancer
    f = instancer.instantiateVariableFont(f, {"wght": WEIGHT})
buf = io.BytesIO(); f.save(buf); data = buf.getvalue()
font = TTFont(io.BytesIO(data))
upm = font["head"].unitsPerEm
gs = font.getGlyphSet()
order = font.getGlyphOrder()

# Setzen mit HarfBuzz: Glyphen, Vorschübe und Unterschneidung aus der Schrift
face = hb.Face(data)
hbfont = hb.Font(face)
hbfont.scale = (upm, upm)
b = hb.Buffer(); b.add_str(TEXT); b.guess_segment_properties()
hb.shape(hbfont, b, {"kern": True, "liga": True})
track = TRACK * upm
pos, x = [], 0.0
for i, (inf, p) in enumerate(zip(b.glyph_infos, b.glyph_positions)):
    g = order[inf.codepoint]
    pos.append((g, x + p.x_offset))
    x += p.x_advance
    if i < len(TEXT) - 1:
        x += track + PAIRS.get((TEXT[i], TEXT[i + 1]), 0)

# Grenzen aller Glyphen (y nach oben)
x0s, x1s, y0s, y1s = [], [], [], []
for g, gx in pos:
    bp = BoundsPen(gs)
    gs[g].draw(bp)
    if bp.bounds:
        a, bb, c, d = bp.bounds
        x0s.append(gx + a); x1s.append(gx + c); y0s.append(bb); y1s.append(d)
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
x_h = font["OS/2"].sxHeight
print(f"upm {upm}  Höhe {h:.0f} ({h / upm:.3f} em)  Breite {w:.0f} ({w / h:.3f} × Höhe)  "
      f"Grundlinie bei {top / h:.3f} der Höhe  x-Höhe {x_h} ({x_h / h:.3f} der Höhe)  bytes {len(svg)}")
