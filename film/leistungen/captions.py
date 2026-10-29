"""Eingebrannte Untertitel für die Hochkant-Fassung (Reels, TikTok, Shorts).
Kurze Abschnitte (höchstens zwei Zeilen), das gesprochene Wort wird hell, die folgenden Wörter stehen gedämpft daneben.
Wo die Bühne denselben Satz schon groß zeigt (Wende, Frage, Abschluss), treten die Untertitel zurück.
Die Zustände werden einmal mit der Filmschrift (Outfit) gerendert und dann Bild für Bild als Streifen über das Video gelegt.

python3 captions_v.py states                 Zustände rendern -> capcache/
python3 captions_v.py preview <t> [<t> ...]  Standbilder aus stills_v/ mit Untertiteln -> stills_v/cap_<t>.png
Als Modul: frames(fps, n) liefert die Streifen (RGBA, 1080 × BAND) für das Kodieren (encode_v.py)."""
import asyncio, functools, http.server, json, math, re, socketserver, sys, threading
from pathlib import Path
import numpy as np
from PIL import Image

import os
FD = os.environ["FD"]
T = json.load(open(f"{FD}/timing.json"))
W = T["words"]
B = {}
BAND, Y0 = 240, 1320          # Streifen 1080 × 240, oben bei y 1320 (Mitte der Untertitel bei y 1440)
MAXL = 30                     # Zeichen je Zeile
CACHE = Path(f"{FD}/capcache")
HIDE = set(json.load(open(f"{FD}/hide.json")))

def norm(s): return re.sub(r"[^\wäöüß ]", "", s.lower().replace("–", " ")).split()

WEAKW = {"auf", "jeder", "jede", "ist", "mit", "der", "die", "das", "dem", "ihr", "ihre", "von", "und", "in", "im", "zu", "ein",
         "einem", "einer", "bei", "aus", "über", "unser", "unserem", "per", "für", "nach", "den", "vom", "kamen"}

def lines_of(ws, score=False):
    """Text in eine oder zwei ausgewogene Zeilen teilen (nie hinter einem kleinen Bindewort, gern nach Satzzeichen)"""
    t = [w["w"] for w in ws]
    if len(" ".join(t)) <= MAXL: return ([t], 0) if score else [t]
    best = None
    for j in range(1, len(t)):
        a, b = " ".join(t[:j]), " ".join(t[j:])
        sc = abs(len(a) - len(b)) * 0.6 + (80 if max(len(a), len(b)) > MAXL else 0)
        if a[-1] in ",:–": sc -= 10
        if t[j - 1].lower().strip(",.:") in WEAKW: sc += 22
        if best is None or sc < best[0]: best = (sc, j)
    L = [t[:best[1]], t[best[1]:]]
    return (L, best[0]) if score else L

def fits(ws):
    L = lines_of(ws); return len(L) <= 2 and all(len(" ".join(l)) <= MAXL for l in L)

def split_sentence(ws):
    """Satz in möglichst wenige, ausgewogene Abschnitte teilen – bevorzugt nach Komma oder Gedankenstrich und an Sprechpausen"""
    n = len(ws); INF = 1e9
    dp = [0.0] + [INF] * n; back = [0] * (n + 1)
    for j in range(1, n + 1):
        for i in range(j):
            if dp[i] >= INF or not fits(ws[i:j]): continue
            ch = len(" ".join(w["w"] for w in ws[i:j]))
            c = dp[i] + 12 + (22 if ch < 12 else 0) + lines_of(ws[i:j], True)[1]
            if j < n:
                w = ws[j - 1]["w"]; pause = ws[j]["s"] - ws[j - 1]["e"]
                c += 0 if re.search(r"[,:–]$", w) else 9
                c += 16 if w.lower().strip(",.:–") in WEAKW else 0
                c -= 6 if pause > 0.3 else 0
            if c < dp[j]: dp[j], back[j] = c, i
    out, j = [], n
    while j > 0: out.append(ws[back[j]:j]); j = back[j]
    return out[::-1]

def build():
    cues, cur = [], []
    for i, w in enumerate(W):
        cur.append(w)
        if re.search(r"[.?!:]$", w["w"]) or i + 1 == len(W):
            cues += split_sentence(cur); cur = []
    out = []
    for k, c in enumerate(cues):
        s = c[0]["s"] - 0.06
        e = c[-1]["e"] + 0.5
        if k + 1 < len(cues): e = min(e, cues[k + 1][0]["s"] - 0.06)
        out.append({"words": c, "lines": lines_of(c), "s": s, "e": max(e, s + 0.6), "hide": any(" ".join(norm(" ".join(x["w"] for x in c))) in h for h in HIDE)})
    for k, c in enumerate(out):
        nxt = out[k + 1] if k + 1 < len(out) else None
        c["fade"] = nxt is None or nxt["hide"] or nxt["s"] - c["e"] > 0.08     # ausblenden, wenn nicht direkt der nächste folgt
    return out

CUES = build()

PAGE = """<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:"Outfit";src:url("outfit-latin-wght-normal.woff2") format("woff2");font-weight:100 900;unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+2000-206F,U+2074,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD}
@font-face{font-family:"Outfit";src:url("outfit-latin-ext-wght-normal.woff2") format("woff2");font-weight:100 900;unicode-range:U+0100-02AF,U+0304,U+0308,U+0329,U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20C0,U+2113,U+2C60-2C7F,U+A720-A7FF}
html,body{margin:0;width:1080px;height:%dpx;background:transparent;overflow:hidden}
#c{position:absolute;left:54px;right:54px;top:0;bottom:0;display:flex;flex-direction:column;align-items:center;justify-content:center;
  font-family:"Outfit";font-weight:620;font-size:56px;line-height:1.16;letter-spacing:-.012em;text-align:center;-webkit-font-smoothing:antialiased;
  color:#F6F8FC;text-shadow:0 2px 3px rgba(4,9,18,.55),0 4px 22px rgba(4,9,18,.75)}
#c div{white-space:nowrap}
#c i{font-style:normal;color:rgba(246,248,252,.42);text-shadow:0 3px 18px rgba(4,9,18,.5)}
</style></head><body><div id="c"></div></body></html>""" % BAND

def html_state(c, k):
    n, out = 0, []
    for line in c["lines"]:
        parts = []
        for w in line:
            parts.append(w if n < k else "<i>" + w + "</i>"); n += 1
        out.append("<div>" + " ".join(parts) + "</div>")
    return "".join(out)

async def render_states():
    D = Path(f"{FD}/stage_v"); (D / "cap.html").write_text(PAGE)
    class Q(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a): pass
    srv = socketserver.ThreadingTCPServer(("127.0.0.1", 0), functools.partial(Q, directory=str(D)))
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    from playwright.async_api import async_playwright
    CACHE.mkdir(exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch(args=["--force-color-profile=srgb", "--font-render-hinting=none", "--disable-lcd-text"])
        pg = await b.new_page(viewport={"width": 1080, "height": BAND})
        await pg.goto(f"http://127.0.0.1:{srv.server_address[1]}/cap.html", wait_until="networkidle")
        await pg.evaluate('document.fonts.load(\'620 56px "Outfit"\')'); await pg.evaluate("document.fonts.ready")
        n = 0
        for ci, c in enumerate(CUES):
            if c["hide"]: continue
            for k in range(len(c["words"]) + 1):
                await pg.evaluate("h => document.getElementById('c').innerHTML = h", html_state(c, k))
                await pg.screenshot(path=str(CACHE / f"{ci:03d}_{k:02d}.png"), omit_background=True)
                n += 1
        await b.close()
    srv.shutdown()
    json.dump([{k: v for k, v in c.items() if k != "words"} | {"n": len(c["words"]), "ws": [w["s"] for w in c["words"]]} for c in CUES],
              open(CACHE / "cues.json", "w"), ensure_ascii=False, indent=0)
    print("Zustände:", n, "Abschnitte:", sum(1 for c in CUES if not c["hide"]), "ausgeblendet:", [" ".join(x["w"] for x in c["words"]) for c in CUES if c["hide"]])

_img = {}
def state(ci, k):
    key = (ci, k)
    if key not in _img:
        _img[key] = np.asarray(Image.open(CACHE / f"{ci:03d}_{k:02d}.png").convert("RGBA")).astype(np.float32) / 255.0
    return _img[key]

def ease(x): return 1 - (1 - min(1.0, max(0.0, x))) ** 3

def band(t):
    """Untertitel-Streifen zur Zeit t: RGBA float (BAND × 1080 × 4, Farbe nicht vormultipliziert) oder None"""
    for ci, c in enumerate(CUES):
        if c["hide"] or not (c["s"] <= t < c["e"]): continue
        ws = [w["s"] - 0.03 for w in c["words"]]
        k = sum(1 for s in ws if s <= t)
        img = state(ci, k)
        if k >= 1 and t < ws[k - 1] + 0.09:                      # Wort wird hell: kurz überblenden
            a = (t - ws[k - 1]) / 0.09; img = state(ci, k - 1) * (1 - a) + img * a
        alpha, dy = 1.0, 0.0
        if t - c["s"] < 0.16: e = ease((t - c["s"]) / 0.16); alpha *= e; dy = 10 * (1 - e)
        if c["fade"] and c["e"] - t < 0.14: alpha *= max(0.0, (c["e"] - t) / 0.14)
        out = img.copy(); out[..., 3] *= alpha
        if dy:
            sh = int(round(dy)); out = np.roll(out, sh, axis=0); out[:sh] = 0
        return out
    return None

def frames(fps, n):
    for i in range(n):
        b = band(i / fps)
        yield b

def preview(ts):
    for t in ts:
        f = Path("stills_v") / f"{t:06.2f}.png"
        im = np.asarray(Image.open(f).convert("RGB")).astype(np.float32) / 255.0
        b = band(t)
        if b is not None:
            seg = im[Y0:Y0 + BAND]; a = b[..., 3:4]
            im[Y0:Y0 + BAND] = seg * (1 - a) + b[..., :3] * a
        Image.fromarray((im * 255 + 0.5).astype(np.uint8)).save(Path("stills_v") / f"cap_{t:06.2f}.png")
    print("Vorschau:", len(ts))

if __name__ == "__main__":
    if sys.argv[1] == "states": asyncio.run(render_states())
    elif sys.argv[1] == "list":
        for c in CUES: print(f"{c['s']:6.2f}-{c['e']:6.2f} {'(aus) ' if c['hide'] else ''}{' / '.join(' '.join(l) for l in c['lines'])}")
    else: preview([float(x) for x in sys.argv[2:]])
