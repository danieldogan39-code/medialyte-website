"""Fertige Dateien aus der verlustfreien Zwischendatei und dem Mix:
Web-MP4 (H.264, schnell startend), WebM (VP9) und Master (H.264 nahezu verlustfrei).
aq-mode 3 gibt dunklen, flachen Verläufen mehr Bits – sonst bilden sich im Navy-Hintergrund Stufen."""
import subprocess, sys
V, A = "out/film60.mkv", "audio/mix.wav"
X264 = ["-x264-params", "aq-mode=3:aq-strength=1.0:psy-rd=1.0,0.15:deblock=0,0"]
COLOR = ["-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv"]
def run(args): print(" ".join(args[-1:])); subprocess.run(["ffmpeg", "-v", "error", "-y"] + args, check=True)
what = sys.argv[1:] or ["web", "master", "webm"]
if "web" in what:
    run(["-i", V, "-i", A, "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "slow", "-crf", "20"] + X264 +
        ["-profile:v", "high", "-level:v", "4.2", "-pix_fmt", "yuv420p", "-g", "120"] + COLOR +
        ["-c:a", "aac", "-b:a", "160k", "-ar", "48000", "-movflags", "+faststart", "out/medialyte-film.mp4"])
if "master" in what:
    run(["-i", V, "-i", A, "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "slow", "-crf", "12"] + X264 +
        ["-profile:v", "high", "-pix_fmt", "yuv420p"] + COLOR + ["-c:a", "aac", "-b:a", "320k", "-ar", "48000", "-movflags", "+faststart",
         "out/medialyte-film-master.mp4"])
if "webm" in what:
    base = ["-i", V, "-map", "0:v", "-c:v", "libvpx-vp9", "-b:v", "0", "-crf", "32", "-row-mt", "1", "-tile-columns", "2", "-auto-alt-ref", "1", "-lag-in-frames", "25",
            "-deadline", "good", "-cpu-used", "2", "-pix_fmt", "yuv420p", "-g", "120"] + COLOR
    run(base + ["-pass", "1", "-passlogfile", "out/vp9", "-an", "-f", "null", "/dev/null"])
    run(["-i", V, "-i", A, "-map", "0:v", "-map", "1:a"] + base[4:] + ["-pass", "2", "-passlogfile", "out/vp9",
         "-c:a", "libopus", "-b:a", "128k", "-ar", "48000", "out/medialyte-film.webm"])
