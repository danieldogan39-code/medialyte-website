"""Fertiges MP4 eines Leistungsfilms: python3 encode.py <n>  ->  f<n>/out/<name>.mp4 (mit Untertiteln) und <name>-ohne-untertitel.mp4
Bild: f<n>/out/film.mkv (60 Bilder/s, Bewegungsunschärfe), Ton: f<n>/mix.wav (-14 LUFS, -1,5 dBTP), Untertitel aus captions.py."""
import json, os, subprocess, sys
import numpy as np
n = sys.argv[1]; os.environ["FD"] = f"f{n}"
import captions as C
NAME = {"1": "medialyte-website-erstellung", "2": "medialyte-kundenmanagement", "3": "medialyte-ki-agent", "4": "medialyte-online-marketing"}[n]
V, A, FPS = f"f{n}/out/film.mkv", f"f{n}/mix.wav", 60
COLOR = ["-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv"]
X264 = ["-c:v", "libx264", "-preset", "medium", "-crf", "16", "-maxrate", "28M", "-bufsize", "56M", "-profile:v", "high", "-level:v", "4.2",
        "-pix_fmt", "yuv420p", "-g", "120", "-x264-params", "aq-mode=3:aq-strength=1.0:psy-rd=1.0,0.15:deblock=0,0"] + COLOR
AUD = ["-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-movflags", "+faststart"]
dur = float(json.loads(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", V], capture_output=True, text=True).stdout)["format"]["duration"])
N = int(round(dur * FPS))
out = f"f{n}/out/{NAME}.mp4"
ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-i", V, "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"1080x{C.BAND}", "-framerate", str(FPS), "-i", "-",
                       "-i", A, "-filter_complex", f"[0:v][1:v]overlay=0:{C.Y0}:format=yuv444:eof_action=pass[v]",
                       "-map", "[v]", "-map", "2:a"] + X264 + AUD + ["-shortest", out], stdin=subprocess.PIPE)
empty = np.zeros((C.BAND, 1080, 4), np.uint8).tobytes()
for i, b in enumerate(C.frames(FPS, N)):
    ff.stdin.write(empty if b is None else (np.clip(b, 0, 1) * 255 + 0.5).astype(np.uint8).tobytes())
ff.stdin.close(); ff.wait()
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", V, "-i", A, "-map", "0:v", "-map", "1:a"] + X264 + AUD + ["-shortest", out.replace(".mp4", "-ohne-untertitel.mp4")], check=True)
print("fertig", out, N, "Bilder")
