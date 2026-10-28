"""Bühne zusammensetzen: Platzhalter durch Logo, Wortmarke, Symbole und Zeitplan ersetzen, Dateien nach stage/ kopieren.
Schrift und RechnungsRadar-Logo kommen direkt aus der Website (src/assets).
python3 build_stage.py        Breitbild 1920 × 1080 -> stage/
python3 build_stage.py --v    Hochkant 1080 × 1920 -> stage_v/ (mit film_v.css und dem Titelbild cover.html)"""
import json, re, shutil, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT))
import build  # noqa: E402
V = "--v" in sys.argv
SRC, OUT = HERE / "src", HERE / ("stage_v" if V else "stage")
OUT.mkdir(exist_ok=True)
html = (SRC / "index.html").read_text()
html = re.sub(r"\{\{LOGO:([^}]*)\}\}", lambda m: build.LOGO.replace('class="mono"', f'class="{m.group(1) or "mono"}"'), html)
html = html.replace("{{WM}}", build.WORDMARK.replace('class="wordmark"', 'class="wm"'))
html = re.sub(r"\{\{I:(\w+)\}\}", lambda m: build.icon(m.group(1)), html)
html = html.replace("{{TIMING}}", json.dumps(json.load(open(HERE / "timing.json")), ensure_ascii=False))
if V:
    html = html.replace('<link rel="stylesheet" href="film.css">', '<link rel="stylesheet" href="film.css">\n<link rel="stylesheet" href="film_v.css">')
    html = html.replace("<body>", '<body class="v">')
left = re.findall(r"\{\{[^}]+\}\}", html)
assert not left, left
(OUT / "index.html").write_text(html)
for f in ["film.css", "film_v.css", "film.js", "gsap.min.js"]:
    shutil.copy(SRC / f, OUT / f)
shutil.copytree(SRC / "img", OUT / "img", dirs_exist_ok=True)
for f in ["fonts/outfit-latin-wght-normal.woff2", "fonts/outfit-latin-ext-wght-normal.woff2", "img/logos/rechnungsradar.webp"]:
    shutil.copy(ROOT / "src/assets" / f, OUT / Path(f).name)
if V:   # Titelbild für die Apps
    cv = (SRC / "cover.html").read_text()
    cv = re.sub(r"\{\{LOGO:([^}]*)\}\}", lambda m: build.LOGO.replace('class="mono"', f'class="{m.group(1) or "mono"}"'), cv)
    cv = cv.replace("{{WM}}", build.WORDMARK.replace('class="wordmark"', 'class="wm"'))
    cv = re.sub(r"\{\{I:(\w+)\}\}", lambda m: build.icon(m.group(1)), cv)
    (OUT / "cover.html").write_text(cv)
print("Bühne gebaut", len(html))
