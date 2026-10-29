"""Ton eines Leistungsfilms: python3 mix.py <n>  ->  f<n>/mix.wav (-14 LUFS, -1 dBTP)
Sprecher (f<n>/vo.wav), Geräusche aus der Bühne (f<n>/cues_v.json), Musik: Quelle = Film + A (Aufbruch auf der Wende T1),
letzter Schlag der Musik (139,965 s) auf cJ (Logo), danach Ausklang."""
import json, math, subprocess, sys
from pathlib import Path
import numpy as np
sys.path.insert(0, "/tmp/claude-0/-home-claude/b87a22e3-5574-5011-b033-0cedfa9a627b/scratchpad/clips")
import os
from common import load, music, SR, FINAL
import audio as AU                      # Geräusch-Bausteine wie in den Clips (sfx_clip, place)
n = sys.argv[1]; F = Path(__file__).parent / f"f{n}"
T = json.load(open(F / "timing.json")); M = T["music"]; DUR = T["duration"]
cues = json.load(open(F / "cues_v.json"))["sfx"]
N = int(round(DUR * SR)); t = np.arange(N) / SR
vo = load(F / "vo.wav", 1)[:, 0]; vo = np.pad(vo, (0, max(0, N - len(vo))))[:N]
m = music()
def take(off):
    idx = np.rint((t + off) * SR).astype(int); v = np.zeros((N, 2), np.float32); ok = (idx >= 0) & (idx < len(m)); v[ok] = m[idx[ok]]; return v
A, cJ = M["A"], M["cJ"]
body = take(A)
XF, pre = 0.04, 0.055
tail = take(FINAL - cJ)
w = np.clip((t - (cJ - pre)) / XF, 0, 1)[:, None]
mus = body * np.cos(w * np.pi / 2) + tail * np.sin(w * np.pi / 2)
mus *= np.clip(t / 0.006, 0, 1)[:, None] * (np.clip((DUR - t) / 0.9, 0, 1) ** 1.5)[:, None]
fx = np.zeros((N + SR * 4, 2), np.float32)
for q in cues:
    x, ref = AU.sfx_clip(q["name"], q["v"])
    AU.place(fx, x, q["at"], ref, q["gain"], q.get("dir", "c"))
fx = fx[:N]
def write(path, x, ch):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", str(ch), "-i", "-", str(path)], input=x.astype(np.float32).tobytes(), check=True)
S = F / "stems"; S.mkdir(exist_ok=True)
write(S / "vo.wav", vo[:, None], 1); write(S / "music.wav", mus, 2); write(S / "sfx.wav", fx, 2)
fg = ("[0:a]pan=stereo|c0=c0|c1=c0,highpass=f=70,acompressor=threshold=0.12:ratio=2.5:attack=8:release=120:makeup=1.6,asplit=2[vo][sc];"
      "[1:a]volume=-14dB[mu];[mu][sc]sidechaincompress=threshold=0.03:ratio=3.5:attack=25:release=450:makeup=1[duck];"
      "[2:a]volume=-2dB[fx];[vo][duck][fx]amix=inputs=3:normalize=0:duration=first[mix]")
raw = F / "mix_raw.wav"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(S / "vo.wav"), "-i", str(S / "music.wav"), "-i", str(S / "sfx.wav"), "-filter_complex", fg, "-map", "[mix]", "-ar", "48000", str(raw)], check=True)
r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(raw), "-af", "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"], capture_output=True, text=True).stderr
js = json.loads(r[r.rindex("{"):r.rindex("}") + 1])
ln = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={js['input_i']}:measured_TP={js['input_tp']}:measured_LRA={js['input_lra']}"
      f":measured_thresh={js['input_thresh']}:offset={js['target_offset']}:linear=true")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(raw), "-af", ln, "-ar", "48000", str(F / "mix.wav")], check=True)
r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(F / "mix.wav"), "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True).stderr
print(n, [l.strip() for l in r.splitlines() if l.strip().startswith(("I:", "Peak:"))][-2:], "Geräusche", len(cues))
