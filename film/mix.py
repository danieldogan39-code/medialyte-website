"""Musik auf Filmlänge schneiden (Schnitt im Takt, natürliches Ende) und mit dem Sprecher mischen."""
import json, subprocess, numpy as np
SR = 48000
dur = json.load(open("timing.json"))["duration"]
raw = subprocess.run(["ffmpeg","-v","error","-i","audio/music1.mp3","-f","f32le","-ac","2","-ar",str(SR),"-"], capture_output=True).stdout
m = np.frombuffer(raw, np.float32).reshape(-1, 2)
BAR = 4 * 60 / 95.7
JUMP = 20 * BAR              # 20 Takte weiter: Takt bleibt im Raster
X0, XL = 80.0, BAR           # Überblendung über einen Takt
n = int(dur * SR)
out = np.zeros((n, 2), np.float32)
t = np.arange(n) / SR
src_a = (t * SR).astype(int)
src_b = ((t + JUMP) * SR).astype(int)
def take(idx):
    v = np.zeros((len(idx), 2), np.float32); ok = idx < len(m); v[ok] = m[idx[ok]]; return v
A, B = take(src_a), take(src_b)
w = np.clip((t - X0) / XL, 0, 1)[:, None]
out = A * np.cos(w * np.pi / 2) + B * np.sin(w * np.pi / 2)
fade = np.clip((dur - t) / 1.2, 0, 1)[:, None]; out *= fade          # sicherheitshalber sanft auslaufen
fin = np.clip(t / 0.6, 0, 1)[:, None]; out *= fin
subprocess.run(["ffmpeg","-v","error","-y","-f","f32le","-ar",str(SR),"-ac","2","-i","-","audio/music_edit.wav"], input=out.astype(np.float32).tobytes())
# Mischen: Musik leiser, unter der Stimme zusätzlich etwas abgesenkt; danach auf -16 LUFS
fg = ("[0:a]aresample=48000,pan=stereo|c0=c0|c1=c0,highpass=f=70,acompressor=threshold=0.12:ratio=2.5:attack=8:release=120:makeup=1.6,asplit=2[vo][sc];"
      "[1:a]volume=-13dB[mu];[mu][sc]sidechaincompress=threshold=0.03:ratio=3:attack=25:release=420:makeup=1[duck];"
      "[vo][duck]amix=inputs=2:normalize=0:duration=longest[mix]")
subprocess.run(["ffmpeg","-v","error","-y","-i","audio/vo_timed.wav","-i","audio/music_edit.wav","-filter_complex",fg,"-map","[mix]","-ar","48000","audio/mix_raw.wav"], check=True)
# Zweistufige Lautheitsnormalisierung
r = subprocess.run(["ffmpeg","-hide_banner","-nostats","-i","audio/mix_raw.wav","-af","loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json","-f","null","-"], capture_output=True, text=True).stderr
js = json.loads(r[r.rindex("{"):r.rindex("}") + 1])
ln = (f"loudnorm=I=-16:TP=-1.5:LRA=11:measured_I={js['input_i']}:measured_TP={js['input_tp']}:measured_LRA={js['input_lra']}"
      f":measured_thresh={js['input_thresh']}:offset={js['target_offset']}:linear=true")
subprocess.run(["ffmpeg","-v","error","-y","-i","audio/mix_raw.wav","-af",ln,"-ar","48000","audio/mix.wav"], check=True)
r = subprocess.run(["ffmpeg","-hide_banner","-nostats","-i","audio/mix.wav","-af","ebur128=peak=true","-f","null","-"], capture_output=True, text=True).stderr
print([l.strip() for l in r.splitlines() if "I:" in l or "Peak:" in l][-3:])
