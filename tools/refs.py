"""Referenz-Screenshots (Playwright-Aufnahmen) in WebP-Dateien für die Website umwandeln.

Aufruf: python3 tools/refs.py <ordner-mit-aufnahmen>
Erwartet je Referenz: <key>-d-hero.png (1440x900 @2x), <key>-m-hero.png (390x844 @3x),
<key>-d-full.png (1440 breit @1.5x), <key>-m-full.png (390 breit @2x).
"""
import json
import sys
from pathlib import Path

from PIL import Image

Image.MAX_IMAGE_PIXELS = None
SRC = Path(sys.argv[1])
OUT = Path(__file__).resolve().parent.parent / "src/assets/img/refs"
KEYS = ["rechnungsradar", "rubin", "ritz"]


def save(im, name, w, q=82, max_h=None):
    h = round(im.height * w / im.width)
    im2 = im.convert("RGB").resize((w, h), Image.LANCZOS)
    if max_h and h > max_h:
        im2 = im2.crop((0, 0, w, max_h))
    im2.save(OUT / name, "WEBP", quality=q, method=6)
    return im2.size


meta = {}
for k in KEYS:
    d_hero = Image.open(SRC / f"{k}-d-hero.png")
    m_hero = Image.open(SRC / f"{k}-m-hero.png")
    d_full = Image.open(SRC / f"{k}-d-full.png")
    m_full = Image.open(SRC / f"{k}-m-full.png")
    save(m_hero, f"{k}-mobile.webp", 600)
    long = save(d_full, f"{k}-long.webp", 1200, q=78, max_h=2400)
    save(d_full, f"{k}-long-sm.webp", 640, q=76, max_h=1280)
    full = save(d_full, f"{k}-full.webp", 1200, q=76, max_h=16000)
    mfull = save(m_full, f"{k}-mobile-full.webp", 520, q=76, max_h=16000)
    meta[k] = {"long_h": long[1], "full_h": full[1], "mobile_full_h": mfull[1]}
    print(k, meta[k])
(OUT / "refs.json").write_text(json.dumps(meta, indent=1))
