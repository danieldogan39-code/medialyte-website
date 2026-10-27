"""Bereitet alle Bilder für die Website auf (WebP, zugeschnitten, passende Größen).
Quelle: Downloads der alten Seite + Referenz-Screenshots im Scratchpad.
Aufruf: python3 tools/assets.py <scratchpad-pfad>
"""
import re, sys, json
from pathlib import Path
from PIL import Image

S = Path(sys.argv[1])
P = Path(__file__).resolve().parent.parent
IMG = P / "src/assets/img"
OLD = S / "old-assets"
REFS = S / "refs"

def save_webp(im, path, q=78):
    path.parent.mkdir(parents=True, exist_ok=True)
    im.save(path, "WEBP", quality=q, method=6)
    return path

# 1) Logo: zugeschnittene Varianten
svg = (P / "tools/logo-original.svg").read_text()
svg = re.sub(r'width="500"', '', svg)
svg = re.sub(r'height="500"', '', svg)
svg = svg.replace('viewBox="0 0 375 374.999991"', 'viewBox="34 54 314 236"')
(IMG / "logo-ml.svg").write_text(svg)
svg_current = svg.replace("fill:#ff5757", "fill:currentColor")
(P / "tools/logo-inline.svg").write_text(svg_current)
# Favicon: Korall-Logo auf Nachtblau
inner = re.search(r"<svg[^>]*>(.*)</svg>", svg, re.S).group(1)
fav = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">'
       '<rect width="64" height="64" rx="14" fill="#0E192A"/>'
       '<g transform="translate(6.5 12.9) scale(0.1622)">'
       f'<g transform="translate(-34 -54)">{inner}</g></g></svg>')
(IMG / "favicon.svg").write_text(fav)

# 2) Kunden-Logos (weiß auf transparent), zugeschnitten, 100 px hoch
names = ["rubin", "fassadentrio", "ritz", "rechnungsradar", "cv", "hubo-dmoran", "deluxe-design",
         "amore-eventdeko", "ionos-agency-partner", "garee-beauty", "glory-angels", "sabaai-thai", "gado-energie"]
logos = []
for i, n in enumerate(names, 1):
    im = Image.open(OLD / f"marquee-{i:02d}.png").convert("RGBA")
    im = im.crop(im.getbbox())
    h = 100
    w = round(im.width * h / im.height)
    im = im.resize((w, h), Image.LANCZOS)
    save_webp(im, IMG / "logos" / f"{n}.webp", q=90)
    logos.append({"file": f"{n}.webp", "w": w, "h": h})
(IMG / "logos/logos.json").write_text(json.dumps(logos, indent=1))

# 3) Avatare (rund zugeschnitten im CSS), 112 px
for src, dst in [("avatar-gado.jpg", "gado"), ("avatar-2.jpg", "cv"), ("avatar-3.jpg", "rechnungsradar")]:
    im = Image.open(OLD / src).convert("RGB")
    s = min(im.size); im = im.crop(((im.width - s) // 2, (im.height - s) // 2, (im.width + s) // 2, (im.height + s) // 2))
    save_webp(im.resize((112, 112), Image.LANCZOS), IMG / "logos" / f"avatar-{dst}.webp", q=85)

# 4) Vorher/Nachher RechnungsRadar (echte Screenshots der alten Seite)
#    Beide auf denselben Ausschnitt (1280 × 560, oberer Bereich), damit der Regler gleiche Stellen vergleicht.
#    Beim alten Bild werden Scrollleiste rechts und ein Rest am linken Rand abgeschnitten.
for src, dst, box in [("rr-vorher.png", "rechnungsradar-vorher", (3, 0, 1273)), ("rr-nachher.png", "rechnungsradar-nachher", (0, 0, 1280))]:
    im = Image.open(OLD / src).convert("RGB")
    w = 1280; im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    x0, y0, x1 = box
    im = im.crop((x0, y0, x1, im.height))
    im = im.resize((1280, round(im.height * 1280 / im.width)), Image.LANCZOS).crop((0, 0, 1280, 560))
    save_webp(im, IMG / "refs" / f"{dst}.webp", q=86)

# 5) Referenz-Screenshots
meta = {}
for key in ["rr", "rubin", "ritz"]:
    name = {"rr": "rechnungsradar", "rubin": "rubin", "ritz": "ritz"}[key]
    d_top = Image.open(REFS / f"{key}-d-top.png").convert("RGB")
    save_webp(d_top.resize((1200, 750), Image.LANCZOS), IMG / "refs" / f"{name}-desktop.webp", q=80)
    save_webp(d_top.resize((640, 400), Image.LANCZOS), IMG / "refs" / f"{name}-desktop-sm.webp", q=78)
    d_full = Image.open(REFS / f"{key}-d-full.png").convert("RGB")
    w = 1000; hh = round(d_full.height * w / d_full.width)
    d_full = d_full.resize((w, hh), Image.LANCZOS)
    if d_full.height > 9000:
        d_full = d_full.crop((0, 0, w, 9000))
    save_webp(d_full, IMG / "refs" / f"{name}-desktop-full.webp", q=70)
    m_top = Image.open(REFS / f"{key}-m-top.png").convert("RGB")
    save_webp(m_top.resize((390, 844), Image.LANCZOS), IMG / "refs" / f"{name}-mobile.webp", q=80)
    m_full = Image.open(REFS / f"{key}-m-full.png").convert("RGB")
    mh = round(m_full.height * 390 / m_full.width)
    m_full = m_full.resize((390, mh), Image.LANCZOS)
    if m_full.height > 9000:
        m_full = m_full.crop((0, 0, 390, 9000))
    save_webp(m_full, IMG / "refs" / f"{name}-mobile-full.webp", q=70)
    meta[name] = {"desktop_full_h": d_full.height, "mobile_full_h": m_full.height}
(IMG / "refs/refs.json").write_text(json.dumps(meta, indent=1))

total = sum(f.stat().st_size for f in IMG.rglob("*") if f.is_file())
print("Bilder gesamt:", round(total / 1024), "KB")
for f in sorted(IMG.rglob("*.webp")):
    print(f.relative_to(IMG), round(f.stat().st_size / 1024), "KB")
