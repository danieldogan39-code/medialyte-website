"""Fertige Dateien aus der verlustfreien Zwischendatei und dem Mix:
Web-MP4 (H.264, schnell startend), WebM (VP9) und Master (H.264 nahezu verlustfrei).
aq-mode 3 gibt dunklen, flachen Verläufen mehr Bits – sonst bilden sich im Navy-Hintergrund Stufen."""
import subprocess, sys
V, A = "out/film60.mkv", "out/mix.wav"
X264 = ["-x264-params", "aq-mode=3:aq-strength=1.0:psy-rd=1.0,0.15:deblock=0,0"]
COLOR = ["-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv"]
def run(args): print(" ".join(args[-1:])); subprocess.run(["ffmpeg", "-v", "error", "-y"] + args, check=True)
what = sys.argv[1:] or ["web", "master", "webm"]
if "web" in what:
    # zwei Durchgänge mit Zielgröße: unter 15 MB bleiben (Grenze für Dateien im Artefakt), Bits dort, wo Bewegung ist
    import json as _j
    dur = float(_j.loads(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", V], capture_output=True, text=True).stdout)["format"]["duration"])
    kbps = int(14.3 * 8 * 1000 / dur) - 128
    enc = ["-c:v", "libx264", "-preset", "slow", "-b:v", f"{kbps}k", "-maxrate", f"{int(kbps * 2.2)}k", "-bufsize", f"{int(kbps * 4)}k"] + X264 + \
          ["-profile:v", "high", "-level:v", "4.2", "-pix_fmt", "yuv420p", "-g", "120"] + COLOR
    run(["-i", V, "-map", "0:v"] + enc + ["-pass", "1", "-passlogfile", "out/x264", "-an", "-f", "mp4", "/dev/null"])
    run(["-i", V, "-i", A, "-map", "0:v", "-map", "1:a"] + enc + ["-pass", "2", "-passlogfile", "out/x264",
         "-c:a", "aac", "-b:a", "128k", "-ar", "48000", "-movflags", "+faststart", "out/medialyte-film.mp4"])
if "master" in what:
    run(["-i", V, "-i", A, "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "slow", "-crf", "14"] + X264 +
        ["-profile:v", "high", "-pix_fmt", "yuv420p"] + COLOR + ["-c:a", "aac", "-b:a", "320k", "-ar", "48000", "-movflags", "+faststart",
         "out/medialyte-film-master.mp4"])
if "webm" in what:
    # VP9 in zwei Durchgängen mit Zielrate (gleiche Größenordnung wie das MP4)
    base = ["-i", V, "-map", "0:v", "-c:v", "libvpx-vp9", "-b:v", "950k", "-maxrate", "2000k", "-row-mt", "1", "-tile-columns", "2",
            "-auto-alt-ref", "1", "-lag-in-frames", "25", "-deadline", "good", "-cpu-used", "3", "-pix_fmt", "yuv420p", "-g", "120"] + COLOR
    run(base + ["-pass", "1", "-passlogfile", "out/vp9", "-an", "-f", "null", "/dev/null"])
    run(["-i", V, "-i", A, "-map", "0:v", "-map", "1:a"] + base[4:] + ["-pass", "2", "-passlogfile", "out/vp9",
         "-c:a", "libopus", "-b:a", "112k", "-ar", "48000", "out/medialyte-film.webm"])
