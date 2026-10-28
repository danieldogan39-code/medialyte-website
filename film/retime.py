"""Sprecher neu takten: an Kapitelgrenzen etwas mehr Luft, Schnitt jeweils in der leisesten Stelle der Pause.
Schreibt audio/vo_timed.wav und timing.json (Sätze und Wörter in der Zeit des fertigen Films)."""
import json, re, subprocess, numpy as np
SR = 44100
raw = subprocess.run(["ffmpeg","-v","error","-i","audio/vo_take1.mp3","-f","f32le","-ac","1","-ar",str(SR),"-"], capture_output=True).stdout
a = np.frombuffer(raw, np.float32).copy()
W = json.load(open("audio/vo_take1.words.json"))["words"]
sents=[]; cur=[]
for w in W:
    cur.append(w)
    if re.search(r"[.?!]$", w["w"]) and not re.match(r"^\d", w["w"]):
        sents.append(cur); cur=[]
if cur: sents.append(cur)
LEAD = 0.9
EXTRA = {5: 0.85, 10: 0.75, 14: 0.75, 20: 0.6, 8: 0.35, 21: 0.45, 4: 0.0}   # Satzindex -> zusätzliche Pause davor
TAIL = 3.8
# Schnittpunkte: leiseste 20-ms-Stelle zwischen Satzende und nächstem Satzanfang
def quietest(t0, t1):
    i0, i1 = int(max(0, t0) * SR), int(min(len(a) / SR, t1) * SR)
    if i1 - i0 < 882: i0, i1 = int((t0 - .15) * SR), int((t1 + .15) * SR)
    win = 882; best = None
    for i in range(i0, i1 - win, 220):
        e = float(np.sqrt(np.mean(a[i:i + win] ** 2)))
        if best is None or e < best[0]: best = (e, i + win // 2)
    return best[1] / SR, 20 * np.log10(best[0] + 1e-9)
cuts = {}
for k in EXTRA:
    t, db = quietest(sents[k - 1][-1]["e"] - 0.05, sents[k][0]["s"] + 0.05)
    cuts[k] = t
    print(f"Schnitt vor Satz {k:2d} bei {t:6.2f}s, Pegel {db:5.1f} dB")
# Zusammensetzen
order = sorted(cuts)
pieces = []; prev = 0.0; shift = LEAD; mapping = []   # (src_from, src_to, dst_offset)
F = int(0.012 * SR)
def faded(seg, head, tail):
    seg = seg.copy()
    if head and len(seg) > F: seg[:F] *= np.linspace(0, 1, F, dtype=np.float32)
    if tail and len(seg) > F: seg[-F:] *= np.linspace(1, 0, F, dtype=np.float32)
    return seg
for n, k in enumerate(order):
    t = cuts[k]
    pieces.append(faded(a[int(prev * SR):int(t * SR)], n > 0, True)); mapping.append((prev, t, shift))
    pieces.append(np.zeros(int(EXTRA[k] * SR), np.float32)); shift += EXTRA[k]; prev = t
pieces.append(faded(a[int(prev * SR):], True, False)); mapping.append((prev, len(a) / SR, shift))
out = np.concatenate([np.zeros(int(LEAD * SR), np.float32)] + pieces + [np.zeros(int(TAIL * SR), np.float32)])
# kurze Blenden an den Schnitten vermeiden Knackser (Schnitte liegen ohnehin in der Stille)
subprocess.run(["ffmpeg","-v","error","-y","-f","f32le","-ar",str(SR),"-ac","1","-i","-","audio/vo_timed.wav"], input=out.tobytes())
def m(t):
    for f, to, off in mapping:
        if f - 1e-6 <= t <= to + 1e-6: return round(t + off, 3)
    return round(t + mapping[-1][2], 3)
words = [{"w": w["w"], "s": m(w["s"]), "e": m(w["e"])} for w in W]
S = []
for s in sents:
    S.append({"s": m(s[0]["s"]), "e": m(s[-1]["e"]), "t": " ".join(x["w"] for x in s)})
dur = len(out) / SR
json.dump({"duration": round(dur, 3), "sentences": S, "words": words}, open("timing.json", "w"), ensure_ascii=False, indent=1)
print("Gesamt", round(dur, 2), "s")
for i, s in enumerate(S): print(f"{i:2d} {s['s']:6.2f}-{s['e']:6.2f} {s['t'][:70]}")
