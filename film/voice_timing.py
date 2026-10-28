"""Sprecher übernehmen, wie er freigegeben wurde – kein Wort wird gekürzt, gedehnt oder verschoben.
Anfang und Ende bekommen Luft (LEAD/TAIL), und an den Szenenwechseln (AIR) wird nur die vorhandene Stille etwas länger,
damit das Bild Zeit für den Übergang hat und der Text nicht gehetzt wirkt. Die Wortzeiten von ElevenLabs (audio/<take>.align.json) werden auf den
Ton geeicht (Versatz und Drift gegen die echten Pausen) und an jeder Pause auf den hörbaren Einsatz gelegt.
Schreibweise der Wörter aus script.txt.   python3 voice_timing.py <take>  ->  audio/vo_timed.wav, timing.json"""
import difflib, json, re, subprocess, sys, numpy as np
SR = 44100
TAKE = sys.argv[1]
LEAD, TAIL = 1.0, 3.4
# zusätzliche Stille in Sekunden vor diesen Satzanfängen (nur in echter Stille eingefügt)
AIR = {"veraltet": 0.35, "und die anfragen": 0.30, "genau hier": 0.15, "am anfang": 0.35, "innerhalb": 0.25,
       "dann lernen": 0.30, "dahinter": 0.20, "aus über": 0.25, "bei rechnungsradar": 0.25, "schreiben sie": 0.25,
       "bei umfangreichen": 0.30}
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", f"audio/{TAKE}.mp3", "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"], capture_output=True).stdout
a = np.frombuffer(raw, np.float32).copy()
WW = []
for w in json.load(open(f"audio/{TAKE}.align.json"))["words"]:
    t = w["text"]
    if t.startswith("[") or t.startswith("<"): continue
    if t in ("–", "-") and WW: WW[-1]["dash"] = True; continue          # Gedankenstrich gehört zum Wort davor
    WW.append({"w": t, "s": w["start"], "e": w["end"]})
SCRIPT = [x for x in open("script.txt").read().split() if x not in ("–", "-")]
dashed = set()
toks = open("script.txt").read().split()
k = -1
for x in toks:
    if x in ("–", "-"): dashed.add(k)
    else: k += 1
def key(s):
    s = s.lower()
    if s.startswith("/"): return "medialyte"
    return re.sub(r"[^\w%]", "", s)
W = []
sm = difflib.SequenceMatcher(None, [key(w["w"]) for w in WW], [key(s) for s in SCRIPT], autojunk=False)
for op, i1, i2, j1, j2 in sm.get_opcodes():
    if op == "equal" or (op == "replace" and i2 - i1 == j2 - j1):
        for q in range(i2 - i1): W.append({"w": SCRIPT[j1 + q] + (" –" if (j1 + q) in dashed else ""), "s": WW[i1 + q]["s"], "e": WW[i1 + q]["e"]})
    else:
        raise SystemExit(f"Abgleich fehlgeschlagen: {op} {[x['w'] for x in WW[i1:i2]]} / {SCRIPT[j1:j2]}")
P = [re.sub(r" –$", "", w["w"])[-1] if re.sub(r" –$", "", w["w"])[-1] in ".,!?:" else "" for w in W]
# Pegel und Stillen
HOP = 0.005; H = int(HOP * SR); F = len(a) // H
db = 20 * np.log10(np.sqrt((a[:F * H].reshape(F, H) ** 2).mean(1)) + 1e-9)
quiet = db < -52.0
runs = []; i = 0
while i < F:
    if quiet[i]:
        j = i
        while j < F and quiet[j]: j += 1
        runs.append((i * HOP, j * HOP)); i = j
    else: i += 1
first_on = next(i for i in range(F) if not quiet[i]) * HOP
last_off = (F - next(i for i in range(F) if not quiet[F - 1 - i])) * HOP
runs = [r for r in runs if r[0] > first_on and r[1] < last_off and r[1] - r[0] >= 0.06]
def assign(tol, minlen):
    out = {}
    for r0, r1 in runs:
        if r1 - r0 < minlen: continue
        d, i = min((abs(r0 - W[i]["e"]), i) for i in range(len(W) - 1))
        if d <= tol: out.setdefault(i, []).append((r0, r1))
    return out
pairs = [(W[i]["e"], min(r[0] for r in rs)) for i, rs in assign(0.25, 0.15).items()]
x, y = np.array(pairs).T
keep = np.ones(len(x), bool)
for _ in range(3):
    al, be = np.polyfit(x[keep], y[keep], 1)
    keep = np.abs(y - (al * x + be)) < 0.07
for w in W: w["s"] = al * w["s"] + be; w["e"] = al * w["e"] + be
print(f"  Eichung t = {al:.5f}·t {be:+.3f}, Rest ±{np.abs((y - (al * x + be))[keep]).max():.3f}s aus {keep.sum()}/{len(x)} Pausen")
used = assign(0.12, 0.06)
for i, rs in used.items():
    W[i]["e"] = min(r[0] for r in rs); W[i + 1]["s"] = max(r[1] for r in rs)
W[0]["s"] = max(W[0]["s"], first_on)
for i in range(1, len(W)):
    W[i]["s"] = max(W[i]["s"], W[i - 1]["s"] + 0.06)
    if (i - 1) not in used: W[i - 1]["e"] = min(max(W[i - 1]["e"], W[i - 1]["s"] + 0.06), W[i]["s"])
    W[i]["e"] = max(W[i]["e"], W[i]["s"] + 0.06)
# Ton: Anfang und Ende mit Luft; an den AIR-Stellen wird mitten in der Stille etwas Stille eingefügt
N = [re.sub(r"[^\w%]", "", w["w"].lower()) for w in W]
ins = []                                            # (Quellzeit, Sekunden)
for phrase, sec in AIR.items():
    ks = phrase.split()
    hits = [i for i in range(1, len(W)) if N[i:i + len(ks)] == ks]
    assert len(hits) == 1, (phrase, hits)
    i = hits[0]
    g0, g1 = W[i - 1]["e"] - 0.02, W[i]["s"] + 0.02
    inside = [(max(r0, g0), min(r1, g1)) for r0, r1 in runs if r1 > g0 and r0 < g1]
    best = max(inside, key=lambda r: r[1] - r[0], default=None)
    if not best or best[1] - best[0] < 0.05:
        print("  ! keine Stille vor", phrase); continue
    ins.append(((best[0] + best[1]) / 2, sec))
    print(f"  Luft vor „{phrase}“: +{sec:.2f}s (Stille {best[1] - best[0]:.2f}s)")
ins.sort()
src0 = max(0.0, first_on - 0.04)
end = min(len(a) / SR, last_off + 0.3)
FD = int(0.005 * SR)
def piece(t0, t1):
    x = a[int(round(t0 * SR)):int(round(t1 * SR))].copy()
    x[:FD] *= np.linspace(0, 1, FD, dtype=np.float32); x[-FD:] *= np.linspace(1, 0, FD, dtype=np.float32); return x
parts, pos = [np.zeros(int(LEAD * SR), np.float32)], src0
for at, sec in ins:
    parts += [piece(pos, at), np.zeros(int(round(sec * SR)), np.float32)]; pos = at
parts += [piece(pos, end), np.zeros(int(TAIL * SR), np.float32)]
out = np.concatenate(parts)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "audio/vo_timed.wav"], input=out.tobytes(), check=True)
def m(t):
    return t + LEAD - src0 + sum(sec for at, sec in ins if at < t)
words = [{"w": w["w"], "s": round(m(w["s"]), 3), "e": round(m(w["e"]), 3)} for w in W]
sents, cur = [], []
for w, p in zip(words, P):
    cur.append(w)
    if p and p in ".?!": sents.append(cur); cur = []
if cur: sents.append(cur)
S = [{"s": s[0]["s"], "e": s[-1]["e"], "t": " ".join(x["w"] for x in s)} for s in sents]
dur = round(len(out) / SR, 3)
json.dump({"duration": dur, "sentences": S, "words": words}, open("timing.json", "w"), ensure_ascii=False, indent=1)
print("Gesamt", dur, "s")
for i, s in enumerate(S): print(f"{i:2d} {s['s']:6.2f}-{s['e']:6.2f}  {s['t'][:80]}")
