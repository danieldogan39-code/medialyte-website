"""Untertitel aus den Wortzeiten (Schreibweise steht schon in timing.json) – als WebVTT und SRT."""
import json, re
d = json.load(open("timing.json"))
W = d["words"]
cues, cur = [], []
def text(ws): return " ".join(x["w"] for x in ws)
for i, w in enumerate(W):
    cur.append(w)
    t = text(cur); end = re.search(r"[.?!:]$", w["w"]); soft = re.search(r"[,–…]$", w["w"])
    nxt = W[i + 1] if i + 1 < len(W) else None
    if end or (soft and len(t) > 34) or len(t) > 78 or nxt is None or (nxt and nxt["s"] - w["e"] > 0.6):
        cues.append(cur); cur = []
WEAK = {"auf", "jeder", "jede", "ist", "mit", "der", "die", "das", "dem", "ihr", "ihre", "von", "und", "in", "im", "zu", "ein",
        "einem", "einer", "sie", "wir", "es", "bei", "aus", "über", "unser", "unserem", "per", "für", "nach"}
def wrap(t):
    """zwei ausgewogene Zeilen; lieber nach Satzzeichen trennen, nie nach einem kleinen Bindewort"""
    if len(t) <= 42: return t
    words = t.split(" "); best = None
    for j in range(1, len(words)):
        a, b = " ".join(words[:j]), " ".join(words[j:])
        score = abs(len(a) - len(b)) + (40 if max(len(a), len(b)) > 42 else 0)
        if a[-1] in ",:–": score -= 12
        if words[j - 1].lower().strip(",.:") in WEAK: score += 15
        if best is None or score < best[0]: best = (score, a + "\n" + b)
    return best[1]
spans = []
for k, c in enumerate(cues):
    s = c[0]["s"] - 0.05
    e = c[-1]["e"] + 0.35
    if k + 1 < len(cues): e = min(e, cues[k + 1][0]["s"] - 0.06)
    spans.append((s, max(e, s + 0.9), wrap(text(c))))
def ts(x, sep="."):
    m, s = divmod(max(0, x), 60); return f"00:{int(m):02d}:{s:06.3f}".replace(".", sep)
vtt = ["WEBVTT", ""]
srt = []
for k, (s, e, t) in enumerate(spans):
    vtt += [f"{ts(s)} --> {ts(e)}", t, ""]
    srt += [str(k + 1), f"{ts(s, ',')} --> {ts(e, ',')}", t, ""]
open("out/medialyte-film.de.vtt", "w").write("\n".join(vtt))
open("out/medialyte-film.de.srt", "w").write("\n".join(srt))
print("\n".join(vtt[:24])); print("…", len(spans), "Untertitel")
