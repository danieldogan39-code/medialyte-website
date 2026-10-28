"""Hochkant-Fassung für Social Media fertig machen (Reels, TikTok, YouTube Shorts, LinkedIn).
Ton: derselbe Mix wie im Breitbild, aber auf -14 LUFS / -1 dBTP (Lautheit der Plattformen).
Bild: H.264 High, 1080 × 1920, 60 Bilder/s, mit eingebrannten Untertiteln (captions_v.py) und ohne.
python3 encode_v.py   ->  out/medialyte-film-hochkant.mp4, out/medialyte-film-hochkant-ohne-untertitel.mp4"""
import json, subprocess, sys
import numpy as np
import captions_v as C
V, FPS = "out/film_v60.mkv", 60
COLOR = ["-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv"]

# Ton
r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", "out/mix_raw.wav", "-af", "loudnorm=I=-14:TP=-1.0:LRA=11:print_format=json", "-f", "null", "-"],
                   capture_output=True, text=True).stderr
js = json.loads(r[r.rindex("{"):r.rindex("}") + 1])
ln = (f"loudnorm=I=-14:TP=-1.0:LRA=11:measured_I={js['input_i']}:measured_TP={js['input_tp']}:measured_LRA={js['input_lra']}"
      f":measured_thresh={js['input_thresh']}:offset={js['target_offset']}:linear=true")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "out/mix_raw.wav", "-af", ln, "-ar", "48000", "out/mix_social.wav"], check=True)
r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", "out/mix_social.wav", "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True).stderr
print("Ton:", [l.strip() for l in r.splitlines() if "I:" in l or "Peak:" in l][-2:])

dur = float(json.loads(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", V], capture_output=True, text=True).stdout)["format"]["duration"])
n = int(round(dur * FPS))
X264 = ["-c:v", "libx264", "-preset", "medium", "-crf", "16", "-maxrate", "28M", "-bufsize", "56M", "-profile:v", "high", "-level:v", "4.2",
        "-pix_fmt", "yuv420p", "-g", "120", "-x264-params", "aq-mode=3:aq-strength=1.0:psy-rd=1.0,0.15:deblock=0,0"] + COLOR
AUD = ["-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-movflags", "+faststart"]
what = sys.argv[1:] or ["cap", "clean"]

if "cap" in what:
    # Untertitel-Streifen (RGBA) als zweiter Eingang, über das Bild gelegt
    ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-i", V, "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"1080x{C.BAND}", "-framerate", str(FPS), "-i", "-",
                           "-i", "out/mix_social.wav", "-filter_complex", f"[0:v][1:v]overlay=0:{C.Y0}:format=yuv444:eof_action=pass[v]",
                           "-map", "[v]", "-map", "2:a"] + X264 + AUD + ["-shortest", "out/medialyte-film-hochkant.mp4"], stdin=subprocess.PIPE)
    empty = np.zeros((C.BAND, 1080, 4), np.uint8).tobytes()
    for i, b in enumerate(C.frames(FPS, n)):
        ff.stdin.write(empty if b is None else (np.clip(b, 0, 1) * 255 + 0.5).astype(np.uint8).tobytes())
        if i % 1200 == 0: print("  Untertitel", i, "/", n, flush=True)
    ff.stdin.close(); ff.wait()
    print("mit Untertiteln: out/medialyte-film-hochkant.mp4")
if "clean" in what:
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", V, "-i", "out/mix_social.wav", "-map", "0:v", "-map", "1:a"] + X264 + AUD +
                   ["-shortest", "out/medialyte-film-hochkant-ohne-untertitel.mp4"], check=True)
    print("ohne Untertitel: out/medialyte-film-hochkant-ohne-untertitel.mp4")
