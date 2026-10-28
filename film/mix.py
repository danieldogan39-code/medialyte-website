"""Ton des Films: Sprecher + Musik (im Takt geschnitten, unter der Stimme abgesenkt) + Geräusche aus cues.json.
python3 mix.py   ->  out/mix.wav (48 kHz Stereo, -16 LUFS, Spitze -1,5 dBTP)
Musik: ElevenLabs Music (audio/music1.mp3, 96 BPM, am Stück gemessen). Der Aufbruch der Musik (erste Zählzeit bei 39,965 s)
fällt auf die Wende „Genau hier setzen wir an“. Mitten in der Kamerafahrt zum Ablauf springt die Musik zwölf Takte weiter –
auf einer Phrasengrenze, taktgenau und kurz vor der Zählzeit überblendet –, damit ihr natürliches Ende unter der Schlusskarte ausklingt."""
import json, math, subprocess
from pathlib import Path
import numpy as np
SR = 48000
T = json.load(open("timing.json")); DUR = T["duration"]
C = json.load(open("cues.json"))
Path("out").mkdir(exist_ok=True)

def load(path, ch=2):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-f", "f32le", "-ac", str(ch), "-ar", str(SR), "-"], capture_output=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, ch).copy()

def word(w, n=1):
    k = 0
    for x in T["words"]:
        if x["w"].lower().strip(".,!?:– ") == w and (k := k + 1) == n: return x["s"]
    raise KeyError(w)

# ---------------- Musik
# Tempo und Schlagraster sind am Stück gemessen (Autokorrelation der Einsätze: 96,00 BPM, Schläge bei 0,590 s + k·0,625 s,
# ohne Drift). Mit dem früher geschätzten Tempo (95,7) lag der Sprung 90 ms neben dem Takt – das klang wie ein Hänger.
BPM, BEAT0 = 96.0, 0.590
BEAT = 60 / BPM; BAR = 4 * BEAT; PHRASE = 4 * BAR
DOWN = BEAT0 + 63 * BEAT                       # 39,965 s: erste Zählzeit des Aufbruchs (volle Besetzung)
A = DOWN - (word("genau", 2) - 0.01)           # Quelle = Film + A: der Aufbruch fällt auf „Genau“
J = 12 * BAR                                   # zwölf Takte weiter, damit das natürliche Ende unter der Schlusskarte ausklingt
pan = C["B"]["D2E"] + 0.45                     # Mitte der Kamerafahrt zum Ablauf: das Rauschen deckt den Schnitt
X = DOWN + round((pan + A - DOWN) / PHRASE) * PHRASE - A      # Filmzeit des Schnitts, auf einer Phrasengrenze
m = load("audio/music1.mp3")
n = int(DUR * SR); t = np.arange(n) / SR
def take(off):
    idx = np.rint((t + off) * SR).astype(int); v = np.zeros((n, 2), np.float32); ok = (idx >= 0) & (idx < len(m)); v[ok] = m[idx[ok]]; return v
def onsets(x):
    """Einsatzkurve (spektraler Fluss) in 5-ms-Schritten"""
    H, N = 240, 1024; x = x.mean(1)
    fr = np.lib.stride_tricks.sliding_window_view(x, N)[::H]
    S = np.log1p(10 * np.abs(np.fft.rfft(fr * np.hanning(N), axis=1)))
    return np.maximum(0, np.diff(S, axis=0)).sum(1), H / SR
# Feinabgleich: Einsatzkurven beider Stellen um den Schnitt vergleichen und den Sprung auf den besten Versatz legen
def seg(off, a, b):
    i0, i1 = int((X + off + a) * SR), int((X + off + b) * SR); return m[i0:i1]
ea, hop = onsets(seg(A, -2.5, 2.5)); eb, _ = onsets(seg(A + J, -2.5, 2.5))
ea = (ea - ea.mean()) / ea.std(); eb = (eb - eb.mean()) / eb.std()
L = int(0.15 / hop); core = slice(L, len(ea) - L)
lags = list(range(-L, L + 1)); cc = [float(np.dot(ea[core], eb[L + q:len(eb) - L + q])) / (len(ea) - 2 * L) for q in lags]
q = lags[int(np.argmax(cc))]; J += q * hop
print(f"Musik: Sprung 12 Takte, Feinabgleich {q * hop * 1000:+.0f} ms (Übereinstimmung {max(cc):.2f}, ohne Abgleich {cc[L]:.2f})")
# kurze Überblendung, die kurz vor der Zählzeit endet: der Anschlag kommt schon aus dem neuen Teil
XF = 0.05
w = np.clip((t - (X - 0.015 - XF)) / XF, 0, 1)[:, None]
mus = take(A) * np.cos(w * np.pi / 2) + take(A + J) * np.sin(w * np.pi / 2)
mus *= np.clip(t / 0.8, 0, 1)[:, None] * np.clip((DUR - t) / 1.6, 0, 1)[:, None]
print(f"Musik: Quelle = Film + {A:.3f} s, Schnitt bei {X:.3f} s (Quelle {X + A:.3f} -> {X + A + J:.3f}), Ende der Quelle {DUR + A + J:.1f} s")

# ---------------- Geräusche
M = json.load(open("sfx/sfx_map.json"))
DEF = {   # Typ: (Varianten [(Datei-Typ, Nr)], Ausrichtung, Ausschnitt in s)
    "whoosh": ([("whoosh", 0), ("whoosh", 1)], "peak", None),
    "swoosh": ([("swoosh", 3), ("swoosh", 0)], "peak", None),
    "tap": ([("tap", 3)], "onset", (0, 0.12)),
    "pop": ([("pop", 0), ("pop", 3), ("pop", 2)], "onset", (0, 0.35)),
    "ping": ([("ping", 0), ("ping", 2), ("ping", 3), ("ping", 1)], "onset", None),
    "typing": ([("typing", 0), ("typing", 1), ("typing", 3)], "onset", (0, 1.5)),
    "riser": ([("riser", 3), ("riser", 1)], "end", None),
    "impact": ([("impact", 0), ("swoosh", 1), ("impact", 0)], "onset", None),
    "paper": ([("paper", 2)], "onset", None),
    "success": ([("success", 0), ("success", 2), ("success", 3), ("success", 1)], "onset", None),
    "click": ([("click", 2)], "onset", (0, 0.08)),
    "blips": ([("blips", 1), ("blips", 0), ("blips", 3), ("blips", 2)], "onset", (0, 0.6)),
}
cache = {}
def clip(typ, v):
    files, align, cut = DEF[typ]
    ft, fv = files[v % len(files)]
    key = (ft, fv, cut)
    if key not in cache:
        x = load(Path("sfx") / f"{M[ft][fv]}.mp3")
        H = int(0.01 * SR); F = len(x) // H
        env = 20 * np.log10(np.sqrt((x[:F * H].mean(1).reshape(F, H) ** 2).mean(1)) + 1e-9)
        pk = env.max()
        on = next(i for i in range(F) if env[i] > pk - 30) * H
        if cut:
            x = x[on + int(cut[0] * SR): on + int(cut[1] * SR)].copy(); on = 0
            fd = min(len(x) // 3, int(0.03 * SR)); x[-fd:] *= np.linspace(1, 0, fd)[:, None]
            F = len(x) // H; env = 20 * np.log10(np.sqrt((x[:F * H].mean(1).reshape(F, H) ** 2).mean(1)) + 1e-9); pk = env.max()
        x *= 10 ** ((-12 - pk) / 20)                       # lauteste 10 ms auf -12 dBFS
        ipk = int(np.argmax(env)) * H
        end = (F - next(i for i in range(F) if env[F - 1 - i] > pk - 20)) * H
        cache[key] = (x, {"onset": on, "peak": ipk, "end": end}[align])
    return cache[key]
sfx = np.zeros((n + SR * 4, 2), np.float32)
for c in C["sfx"]:
    x, ref = clip(c["name"], c["v"])
    g = 10 ** (c["gain"] / 20)
    y = x * g
    if c.get("dir") == "rl":                               # Kamerafahrt nach links: Geräusch wandert von rechts nach links
        p = np.linspace(0.35, -0.35, len(y))
        y = y * np.stack([np.sqrt((1 - p) / 2), np.sqrt((1 + p) / 2)], 1) * math.sqrt(2)
    s = int(round(c["at"] * SR)) - ref
    if s < 0: y = y[-s:]; s = 0
    sfx[s:s + len(y)] += y
sfx = sfx[:n]
print("Geräusche:", len(C["sfx"]))

# ---------------- Sprecher
vo = load("audio/vo_timed.wav", 1)[:, 0]
vo = np.pad(vo, (0, max(0, n - len(vo))))[:n]
def write(path, x, ch):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", str(ch), "-i", "-", path], input=x.astype(np.float32).tobytes(), check=True)
write("out/vo.wav", vo[:, None], 1); write("out/music.wav", mus, 2); write("out/sfx.wav", sfx, 2)
fg = ("[0:a]pan=stereo|c0=c0|c1=c0,highpass=f=70,acompressor=threshold=0.12:ratio=2.5:attack=8:release=120:makeup=1.6,asplit=2[vo][sc];"
      "[1:a]volume=-14dB[mu];[mu][sc]sidechaincompress=threshold=0.03:ratio=3.5:attack=25:release=450:makeup=1[duck];"
      "[2:a]volume=-2dB[fx];"
      "[vo][duck][fx]amix=inputs=3:normalize=0:duration=first[mix]")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "out/vo.wav", "-i", "out/music.wav", "-i", "out/sfx.wav", "-filter_complex", fg,
                "-map", "[mix]", "-ar", "48000", "out/mix_raw.wav"], check=True)
r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", "out/mix_raw.wav", "-af", "loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"], capture_output=True, text=True).stderr
js = json.loads(r[r.rindex("{"):r.rindex("}") + 1])
ln = (f"loudnorm=I=-16:TP=-1.5:LRA=11:measured_I={js['input_i']}:measured_TP={js['input_tp']}:measured_LRA={js['input_lra']}"
      f":measured_thresh={js['input_thresh']}:offset={js['target_offset']}:linear=true")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "out/mix_raw.wav", "-af", ln, "-ar", "48000", "out/mix.wav"], check=True)
r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", "out/mix.wav", "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True).stderr
print([l.strip() for l in r.splitlines() if "I:" in l or "Peak:" in l][-3:])
