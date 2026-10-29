"""Wortzeiten für einen Leistungsfilm: Schreibweise aus <film>.txt, Zeiten aus der Whisper-Erkennung des gewählten Takes.
Der Sprecher beginnt nach LEAD s; hinten bleibt TAIL s für das Schlussbild.  python3 timing.py <film> <take>"""
import difflib, json, re, subprocess, sys
import numpy as np
film, take = sys.argv[1], sys.argv[2]
LEAD, TAIL = 0.35, 2.6
SR = 48000
W = json.load(open(f"audio/{take}.words.json"))["words"]
script = open(f"{film}.txt").read().split()
toks = [x for x in script if x not in ("–", "-")]
key = lambda s: re.sub(r"[^\wäöüß]", "", s.lower()).replace("medialeit", "medialyte")
a = [key(x) for x in toks]; b = [key(x["w"]) for x in W]
sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
out = [None] * len(toks)
for op, i1, i2, j1, j2 in sm.get_opcodes():
    if op == "equal" or (op == "replace" and i2 - i1 == j2 - j1):
        for k in range(i2 - i1): out[i1 + k] = (W[j1 + k]["s"], W[j1 + k]["e"])
    elif op == "replace":                      # ungleiche Länge: gleichmäßig verteilen
        s, e = W[j1]["s"], W[j2 - 1]["e"]
        for k in range(i2 - i1): out[i1 + k] = (s + (e - s) * k / (i2 - i1), s + (e - s) * (k + 1) / (i2 - i1))
miss = [toks[i] for i, x in enumerate(out) if x is None]
assert not miss, miss
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", f"audio/{take}.mp3", "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"], capture_output=True).stdout
x = np.frombuffer(raw, np.float32).copy()
# echter Einsatz: erstes Fenster über -45 dBFS
env = np.array([np.sqrt((x[i:i + 480] ** 2).mean()) for i in range(0, len(x) - 480, 480)])
on = int(np.argmax(env > 10 ** (-45 / 20))) * 480 / SR
shift = LEAD - max(0.0, on - 0.02)
cut = int(max(0.0, on - 0.02) * SR)
y = np.concatenate([np.zeros(int(LEAD * SR), np.float32), x[cut:]])
last = max(e for s, e in out) + shift
dur = round(last + TAIL, 3)
y = np.pad(y, (0, max(0, int(dur * SR) - len(y))))[:int(dur * SR)]
d = f"f{film[0]}"
import os; os.makedirs(d, exist_ok=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", f"{d}/vo.wav"], input=y.tobytes(), check=True)
words = [{"w": toks[i], "s": round(out[i][0] + shift, 3), "e": round(out[i][1] + shift, 3)} for i in range(len(toks))]
json.dump({"duration": dur, "words": words}, open(f"{d}/timing.json", "w"), ensure_ascii=False)
print(film, take, "Einsatz", round(on, 3), "Länge", dur, "Wörter", len(words), "erstes", words[0], "letztes", words[-1])
