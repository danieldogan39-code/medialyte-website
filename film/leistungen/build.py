"""Bühne eines Leistungsfilms bauen: python3 build.py <n>  ->  f<n>/stage_v/ (index.html + Dateien)"""
import json, re, shutil, sys
from pathlib import Path
sys.path.insert(0, "/home/claude/medialyte-website")
import build as B
n = sys.argv[1]
SRC, D = Path("src"), Path(f"f{n}/stage_v")
D.mkdir(parents=True, exist_ok=True)
body = (SRC / f"f{n}.html").read_text()
html = f"""<!doctype html>
<html lang="de"><head><meta charset="utf-8"><title>Medialyte Leistungsfilm {n}</title>
<link rel="stylesheet" href="film.css"><link rel="stylesheet" href="svc.css"><link rel="stylesheet" href="f{n}.css"></head>
<body class="v"><div id="stage">
<div class="bg" id="bg"><i class="lt lt1" id="lt1"></i><i class="lt lt2" id="lt2"></i><i class="lt lt3" id="lt3"></i><i class="grid" id="grid"></i><i class="grain"></i></div>
{body}
<div class="chap" id="chap"><span class="chap__n" id="chapN">1</span><span class="chap__t" id="chapT"></span><span class="chap__bar"><b id="chapB"></b></span></div>
<i class="vig"></i>
</div>
<script src="gsap.min.js"></script>
<script>window.TM = {{{{TIMING}}}};</script>
<script src="lib.js"></script><script src="common.js"></script><script src="f{n}.js"></script>
</body></html>"""
html = re.sub(r"\{\{LOGO:([^}]*)\}\}", lambda m: B.LOGO.replace('class="mono"', f'class="{m.group(1) or "mono"}"'), html)
html = html.replace("{{WM}}", B.WORDMARK.replace('class="wordmark"', 'class="wm"'))
html = re.sub(r"\{\{I:(\w+)\}\}", lambda m: B.icon(m.group(1)), html)
html = html.replace("{{TIMING}}", json.dumps(json.load(open(f"f{n}/timing.json")), ensure_ascii=False))
left = re.findall(r"\{\{[^}]+\}\}", html); assert not left, left
(D / "index.html").write_text(html)
for f in ["film.css", "svc.css", f"f{n}.css", "lib.js", "common.js", f"f{n}.js", "gsap.min.js", "outfit-latin-wght-normal.woff2", "outfit-latin-ext-wght-normal.woff2"]:
    shutil.copy(SRC / f, D / f)
shutil.copytree(SRC / "img", D / "img", dirs_exist_ok=True)
print("Bühne", n, len(html))
