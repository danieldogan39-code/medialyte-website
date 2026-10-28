"""Untertitel (WebVTT) aus den Wortzeiten – mit der Schreibweise aus dem Drehbuch."""
import json, re
d = json.load(open("timing.json"))
W = [dict(w) for w in d["words"]]
# Schreibweise aus dem Drehbuch (Whisper hört z. B. „Medialeit“ und „%“)
FIX = {9: "Ihre", 10: "Website …", 43: "WhatsApp –", 44: "und", 81: "sie –", 93: "in dem", 108: "Hand:", 113: "Werbung –",
       129: "RechnungsRadar", 136: "Prozent", 150: "Fotos:", 186: "Medialyte.", 187: "Damit"}
for i, v in FIX.items(): W[i]["w"] = v
# getrennte Teile zusammenführen: „E -Mail“, „KI -Agenten“
out = []
for w in W:
    if w["w"].startswith("-") and out:
        out[-1]["w"] += w["w"]; out[-1]["e"] = w["e"]
    else: out.append(w)
W = out
cues, cur = [], []
def text(ws): return " ".join(x["w"] for x in ws)
for i, w in enumerate(W):
    cur.append(w)
    t = text(cur); end = re.search(r"[.?!:]$", w["w"]); soft = re.search(r"[,–…]$", w["w"])
    nxt = W[i + 1] if i + 1 < len(W) else None
    if end or (soft and len(t) > 34) or len(t) > 78 or nxt is None or (nxt and nxt["s"] - w["e"] > 0.6):
        cues.append(cur); cur = []
def ts(x):
    m, s = divmod(max(0, x), 60); return f"00:{int(m):02d}:{s:06.3f}"
lines = ["WEBVTT", ""]
for k, c in enumerate(cues):
    s = c[0]["s"] - 0.05
    e = c[-1]["e"] + 0.35
    if k + 1 < len(cues): e = min(e, cues[k + 1][0]["s"] - 0.06)
    e = max(e, s + 0.9)
    t = text(c)
    if len(t) > 42:  # auf zwei Zeilen umbrechen, möglichst in der Mitte
        words = t.split(" "); best = None
        for j in range(1, len(words)):
            a, b = " ".join(words[:j]), " ".join(words[j:])
            score = abs(len(a) - len(b))
            if best is None or score < best[0]: best = (score, a + "\n" + b)
        t = best[1]
    lines += [f"{ts(s)} --> {ts(e)}", t, ""]
open("out/medialyte-film.de.vtt", "w").write("\n".join(lines))
print("\n".join(lines[:40]))
print("…", len(cues), "Untertitel")
