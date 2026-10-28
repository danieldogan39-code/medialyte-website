"""Bühne zusammensetzen: Platzhalter durch Logo, Wortmarke, Symbole und Zeitplan ersetzen.
Schrift und RechnungsRadar-Logo kommen direkt aus der Website (src/assets)."""
import json, re, shutil, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT))
import build  # noqa: E402
SRC, OUT = HERE / "src", HERE / "stage"
OUT.mkdir(exist_ok=True)
html = (SRC / "index.html").read_text()
html = re.sub(r"\{\{LOGO:([^}]*)\}\}", lambda m: build.LOGO.replace('class="mono"', f'class="{m.group(1) or "mono"}"'), html)
html = html.replace("{{WM}}", build.WORDMARK.replace('class="wordmark"', 'class="wm"'))
html = re.sub(r"\{\{ICO:(\w+):(\w+)\}\}", lambda m: f'<span class="ico ico--{m.group(1)}">{build.icon(m.group(2))}</span>', html)
html = re.sub(r"\{\{I:(\w+)\}\}", lambda m: build.icon(m.group(1)), html)
html = html.replace("{{TIMING}}", json.dumps(json.load(open(HERE / "timing.json")), ensure_ascii=False))
left = re.findall(r"\{\{[^}]+\}\}", html)
assert not left, left
(OUT / "index.html").write_text(html)
for f in ["film.css", "film.js", "gsap.min.js"]:
    shutil.copy(SRC / f, OUT / f)
for f in ["fonts/outfit-latin-wght-normal.woff2", "fonts/outfit-latin-ext-wght-normal.woff2", "img/logos/rechnungsradar.webp"]:
    shutil.copy(ROOT / "src/assets" / f, OUT / Path(f).name)
print("Bühne gebaut", len(html))
