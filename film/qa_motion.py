"""Bewegungsprüfung des fertigen Films, Bild für Bild.
- Sprünge: großflächige Änderung von einem Bild zum nächsten, die im Umfeld nicht vorkommt (harter Schnitt)
- Aufploppen: ein kleiner Bereich ändert sich in einem einzigen Bild stark (Element erscheint ohne Übergang)
- Flackern: ein einzelnes Bild weicht von beiden Nachbarn ab
python3 qa_motion.py <film> [fps]"""
import json, subprocess, sys, numpy as np
src = sys.argv[1]; fps = int(sys.argv[2]) if len(sys.argv) > 2 else 60
_wh = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "csv=p=0", src], capture_output=True, text=True).stdout.split(",")
W, H, T = (320, 180, 10) if int(_wh[0]) >= int(_wh[1]) else (180, 320, 10)   # Kacheln zu 10x10 Bildpunkten (entspricht 60x60 im Original)
p = subprocess.Popen(["ffmpeg", "-v", "error", "-i", src, "-vf", f"scale={W}:{H}:flags=area,format=gray", "-f", "rawvideo", "-"], stdout=subprocess.PIPE)
frames = []
while True:
    b = p.stdout.read(W * H)
    if len(b) < W * H: break
    frames.append(np.frombuffer(b, np.uint8))
F = np.array(frames).astype(np.int16).reshape(-1, H, W)
D = np.abs(np.diff(F, axis=0))                                  # Änderung zum Vorbild
mean = D.mean(axis=(1, 2))
tiles = D.reshape(len(D), H // T, T, W // T, T).mean(axis=(2, 4))
tmax = tiles.max(axis=(1, 2))
n = len(F)
print("Bilder:", n, " mittlere Änderung", mean.mean().round(3))
def ctx(arr, k, r=12):
    lo, hi = max(0, k - r), min(len(arr), k + r + 1)
    return np.median(np.r_[arr[lo:k], arr[k + 1:hi]])
out = {"jumps": [], "pops": [], "flicker": []}
for k in range(len(D)):
    c = ctx(mean, k)
    if mean[k] > 1.2 and mean[k] > 4 * max(c, 0.05): out["jumps"].append((k + 1, round((k + 1) / fps, 3), round(float(mean[k]), 2)))
    ct = ctx(tmax, k, 6)
    if tmax[k] > 28 and tmax[k] > 3.5 * max(ct, 2.0):
        yy, xx = np.unravel_index(np.argmax(tiles[k]), tiles[k].shape)
        out["pops"].append((k + 1, round((k + 1) / fps, 3), round(float(tmax[k]), 1), int(xx * T * 6), int(yy * T * 6)))
for k in range(1, n - 1):
    a = np.abs(F[k] - F[k - 1]).mean(); c = np.abs(F[k + 1] - F[k - 1]).mean()
    if a > 1.0 and c < 0.3 * a: out["flicker"].append((k, round(k / fps, 3)))
for key, rows in out.items():
    print(f"{key}: {len(rows)}")
    for r in rows[:60]: print("  ", r)
import os; os.makedirs("qa", exist_ok=True)
json.dump({"mean": mean.round(3).tolist(), "tmax": tmax.round(1).tolist()}, open("qa/motion_v.json" if H > W else "qa/motion.json", "w"))
