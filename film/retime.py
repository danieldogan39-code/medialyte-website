"""Sprecher takten, ohne in den Ton zu schneiden.
Gekürzt oder verlängert wird nur echte Stille (unter -52 dB); die Ränder jeder Stille bleiben stehen,
Atmer, Ausklang und Anlaute werden nie angefasst. Pausen je nach Stelle im Text: Komma kurz, Satzende etwas
länger, Szenenwechsel und Kapitel mit Luft für das Bild.
Wortzeiten: aus audio/<take>.align.json (Zeiten von ElevenLabs) oder ersatzweise <take>.words.json (Whisper),
auf den Ton geeicht und an jeder Pause auf den hörbaren Einsatz gelegt. Schreibweise aus script.txt.
python3 retime.py [take]   ->  audio/vo_timed.wav und timing.json (Sätze und Wörter in Filmzeit)"""
import difflib, json, os, re, subprocess, sys, numpy as np
SR = 44100
TAKE = sys.argv[1] if len(sys.argv) > 1 else "vo3_take2"
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", f"audio/{TAKE}.mp3", "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"], capture_output=True).stdout
a = np.frombuffer(raw, np.float32).copy()

# ---- Wörter laden und mit dem Drehbuch abgleichen
if os.path.exists(f"audio/{TAKE}.align.json"):
    WW = [{"w": w["text"], "s": w["start"], "e": w["end"]} for w in json.load(open(f"audio/{TAKE}.align.json"))["words"]
          if not w["text"].startswith(("<", "time=", "/>"))]
else:
    WW = []
    for w in json.load(open(f"audio/{TAKE}.words.json"))["words"]:
        if w["w"].startswith("-") and WW: WW[-1]["w"] += w["w"]; WW[-1]["e"] = w["e"]     # „E -Mail“ -> „E-Mail“
        else: WW.append(dict(w))
SCRIPT = open("script.txt").read().split()
SAME = {"%": "prozent", "medialeit": "medialyte", "achtundvierzig": "48", "zweihundert": "200", "zweihundertdreißig": "230"}
def key(s):
    k = re.sub(r"[^\w%]", "", s.lower()); return SAME.get(k, k)
W = []
sm = difflib.SequenceMatcher(None, [key(w["w"]) for w in WW], [key(s) for s in SCRIPT], autojunk=False)
for op, i1, i2, j1, j2 in sm.get_opcodes():
    if op == "equal" or (op == "replace" and i2 - i1 == j2 - j1):
        for k in range(i2 - i1): W.append({"w": SCRIPT[j1 + k], "s": WW[i1 + k]["s"], "e": WW[i1 + k]["e"]})
    elif op == "replace":
        W.append({"w": " ".join(SCRIPT[j1:j2]), "s": WW[i1]["s"], "e": WW[i2 - 1]["e"]})
        print("  zusammengefasst:", [x["w"] for x in WW[i1:i2]], "->", SCRIPT[j1:j2])
    elif op == "delete":
        for k in range(i1, i2): W.append(dict(WW[k])); print("  nur gehört:", WW[k]["w"])
    else:
        print("  ! nicht gehört:", SCRIPT[j1:j2]); W[-1]["w"] += " " + " ".join(SCRIPT[j1:j2])
N = [re.sub(r"[.,!?:;„“\"()–…]", "", w["w"].lower()).strip() for w in W]
P = [w["w"][-1] if w["w"][-1] in ".,!?:" else "" for w in W]

# ---- Pegel in 5-ms-Schritten, stille Abschnitte finden
HOP = 0.005; H = int(HOP * SR); F = len(a) // H
db = 20 * np.log10(np.sqrt((a[:F * H].reshape(F, H) ** 2).mean(1)) + 1e-9)
quiet = db < -52.0
runs = []; k = 0
while k < F:
    if quiet[k]:
        j = k
        while j < F and quiet[j]: j += 1
        runs.append((k * HOP, j * HOP)); k = j
    else: k += 1
first_on = next(i for i in range(F) if not quiet[i]) * HOP
last_off = (F - next(i for i in range(F) if not quiet[F - 1 - i])) * HOP
runs = [r for r in runs if r[0] > first_on and r[1] < last_off and r[1] - r[0] >= 0.06]

# ---- Wortzeiten eichen: Wortenden gegen den Beginn der deutlichen Pausen (linear, gleicht Versatz und Drift aus)
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
for _ in range(3):                                # robust: Ausreißer (Atmer, Ausklang) aus der Eichung nehmen
    alpha, beta = np.polyfit(x[keep], y[keep], 1)
    keep = np.abs(y - (alpha * x + beta)) < 0.07
for w in W: w["s"] = alpha * w["s"] + beta; w["e"] = alpha * w["e"] + beta
res = (y - (alpha * x + beta))[keep]
print(f"  Eichung: t = {alpha:.5f}·t {beta:+.3f}   Rest ±{np.abs(res).max():.3f}s aus {keep.sum()} von {len(pairs)} Pausen")
used = assign(0.12, 0.06)

# ---- Pausenregeln: Grenze nach Wort i -> (min, max) der Stille in Sekunden
def at_phrase(i, phrase):
    ks = phrase.split(); return N[i + 1:i + 1 + len(ks)] == ks
CHAPTER = ["genau hier", "am anfang", "das alles", "und wenn sich", "medialyte"]   # „Genau hier setzen wir an.“ braucht Nachhall
SCENE = ["und die anfragen", "dann lernen", "aus über", "bei umfangreichen"]
def rule(i):
    if any(at_phrase(i, p) for p in CHAPTER): return (0.82, 0.88)
    if any(at_phrase(i, p) for p in SCENE): return (0.58, 0.64)
    return {".": (0.0, 0.45), "!": (0.0, 0.45), "?": (0.0, 0.42), ":": (0.0, 0.40), ",": (0.0, 0.28)}.get(P[i], (0.0, 0.14))
plan = []
for i, rs in used.items():
    lo, hi = rule(i)
    r0, r1 = max(rs, key=lambda r: r[1] - r[0])           # nur die längste Stille an dieser Grenze wird verändert
    other = sum(b - a_ for a_, b in rs) - (r1 - r0)
    cur = r1 - r0
    tgt = min(max(cur, lo - other), hi - other)
    plan.append((r0, r1, max(tgt, min(cur, 0.08)), i))
for i in range(len(W) - 1):                      # Szenengrenze ganz ohne Stille: an der leisesten Stelle Luft einfügen
    lo, hi = rule(i)
    if lo > 0 and i not in used:
        f0, f1 = int((W[i]["e"] - 0.15) / HOP), int((W[i + 1]["s"] + 0.15) / HOP)
        j = f0 + int(np.argmin(db[f0:f1]))
        if db[j] < -50:
            plan.append((j * HOP, j * HOP, lo, i)); used[i] = [(j * HOP, j * HOP)]
            print(f"  Luft eingefügt vor „{W[i + 1]['w']}“ bei {j * HOP:.2f}s ({db[j]:.0f} dB)")
        else: print(f"  ! keine leise Stelle vor „{W[i + 1]['w']}“ – bleibt wie gesprochen")
plan.sort()

# ---- Wortgrenzen an Pausen auf den Ton legen (Ende = Beginn der Stille, nächster Anfang = ihr Ende)
for i, rs in used.items():
    W[i]["e"] = min(r[0] for r in rs); W[i + 1]["s"] = max(r[1] for r in rs)
for i in range(1, len(W)):                       # Reihenfolge und Mindestdauer sichern
    W[i]["s"] = max(W[i]["s"], W[i - 1]["s"] + 0.06)
    W[i - 1]["e"] = min(max(W[i - 1]["e"], W[i - 1]["s"] + 0.06), W[i]["s"] if (i - 1) not in used else W[i - 1]["e"])
    W[i]["e"] = max(W[i]["e"], W[i]["s"] + 0.06)

# ---- Zusammensetzen: Stille in der Mitte kürzen bzw. verlängern
LEAD, TAIL, KEEP = 0.8, 3.2, 0.04
FADE = int(0.006 * SR)
def seg(t0, t1):
    s = a[int(round(t0 * SR)):int(round(t1 * SR))].copy()
    if len(s) > 2 * FADE:
        s[:FADE] *= np.linspace(0, 1, FADE, dtype=np.float32); s[-FADE:] *= np.linspace(1, 0, FADE, dtype=np.float32)
    return s
src0 = max(0.0, first_on - 0.05)
pieces = [np.zeros(int(LEAD * SR), np.float32)]
mapping = []          # (quelle_von, quelle_bis, verschiebung) der behaltenen Stücke
pos, shift, log = src0, LEAD - src0, []
for r0, r1, tgt, i in plan:
    cur = r1 - r0
    if abs(tgt - cur) < 0.02: continue
    if tgt < cur:
        cut = cur - tgt
        m0 = max(r0 + KEEP, r0 + (cur - cut) / 2); m1 = m0 + cut
        pieces.append(seg(pos, m0)); mapping.append((pos, m0, shift)); shift -= cut; pos = m1
    else:
        mid = (r0 + r1) / 2
        pieces.append(seg(pos, mid)); mapping.append((pos, mid, shift))
        pieces.append(np.zeros(int(round((tgt - cur) * SR)), np.float32)); shift += tgt - cur; pos = mid
    log.append((W[i]["w"], W[i + 1]["w"], cur, tgt))
end = min(len(a) / SR, last_off + 0.25)
pieces.append(seg(pos, end)); mapping.append((pos, end, shift))
pieces.append(np.zeros(int(TAIL * SR), np.float32))
out = np.concatenate(pieces)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "audio/vo_timed.wav"], input=out.tobytes(), check=True)
def m(t):
    for f, to, off in mapping:
        if t < f: return f + off
        if t <= to: return t + off
    return mapping[-1][1] + mapping[-1][2]
words = [{"w": w["w"], "s": round(m(w["s"]), 3), "e": round(m(w["e"]), 3)} for w in W]
sents, cur = [], []
for w, p in zip(words, P):
    cur.append(w)
    if p and p in ".?!": sents.append(cur); cur = []
if cur: sents.append(cur)
S = [{"s": s[0]["s"], "e": s[-1]["e"], "t": " ".join(x["w"] for x in s)} for s in sents]
dur = round(len(out) / SR, 3)
json.dump({"duration": dur, "sentences": S, "words": words}, open("timing.json", "w"), ensure_ascii=False, indent=1)
for a_, b_, c, t in log: print(f"  {a_:>18s} | {b_:<16s} {c:4.2f}s -> {t:4.2f}s")
print("Gesamt", dur, "s")
def lvl(s, e):
    x = out[int(s * SR):int(e * SR)]; return 20 * np.log10(np.sqrt((x ** 2).mean()) + 1e-9)
for i, s in enumerate(S): print(f"{i:2d} {s['s']:6.2f}-{s['e']:6.2f} {lvl(s['s'], s['e']):5.1f} dB  {s['t'][:70]}")
