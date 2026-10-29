"""Web-Fassungen der Leistungsfilme: 720 × 1280, 60 Bilder/s, H.264 in zwei Durchgängen mit Zielgröße, Titelbild als JPG.
python3 web.py <n> [MB]  ->  web/leistung-<name>.mp4, .jpg"""
import json, subprocess, sys
from PIL import Image
n = sys.argv[1]; MB = float(sys.argv[2]) if len(sys.argv) > 2 else 6.5
NAME = {"1": "website-erstellung", "2": "kundenmanagement", "3": "ki-agent", "4": "online-marketing"}[n]
SRC = f"f{n}/out/medialyte-{NAME}.mp4"; OUT = f"web/leistung-{NAME}"
dur = float(json.loads(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", SRC], capture_output=True, text=True).stdout)["format"]["duration"])
kbps = int(MB * 8 * 1000 / dur) - 112
COLOR = ["-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv"]
enc = ["-vf", "scale=720:1280:flags=lanczos", "-c:v", "libx264", "-preset", "slow", "-b:v", f"{kbps}k", "-maxrate", f"{int(kbps * 2.2)}k", "-bufsize", f"{kbps * 4}k",
       "-x264-params", "aq-mode=3:aq-strength=1.0:psy-rd=1.0,0.15:deblock=0,0", "-profile:v", "high", "-level:v", "4.1", "-pix_fmt", "yuv420p", "-g", "120"] + COLOR
def run(a): subprocess.run(["ffmpeg", "-v", "error", "-y"] + a, check=True)
run(["-i", SRC, "-map", "0:v"] + enc + ["-pass", "1", "-passlogfile", f"web/x{n}", "-an", "-f", "mp4", "/dev/null"])
run(["-i", SRC, "-map", "0:v", "-map", "0:a"] + enc + ["-pass", "2", "-passlogfile", f"web/x{n}", "-c:a", "aac", "-b:a", "112k", "-ar", "48000", "-movflags", "+faststart", OUT + ".mp4"])
Image.open(f"f{n}/out/cover.png").convert("RGB").resize((720, 1280), Image.LANCZOS).save(OUT + ".jpg", quality=86, optimize=True, progressive=True)
print(OUT, round(dur, 1), "s", kbps, "kbit/s")
