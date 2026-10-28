"""Film Bild für Bild rendern – mit Bewegungsunschärfe wie bei einer Kamera (180°-Verschluss).
python3 render.py cues                        Geräusche und Szenengrenzen nach cues.json
python3 render.py probe [fps]                 Bewegung je Bild messen -> motion.json (wie viele Abtastungen pro Bild)
python3 render.py video <out.mkv> [fps] [teile] [--noblur] [--from=s --to=s]
Für jedes Bild wird gemessen, wie weit sich Kanten bewegen. Ruhige Bilder werden einmal aufgenommen, bewegte Bilder
mehrfach innerhalb der Belichtungszeit und im linearen Licht gemittelt. Texte, Zähler und Zustände richten sich dabei
nach der Bildzeit (window.__seek(t, ft)), damit Schrift scharf bleibt. Jeder Abschnitt rendert streng vorwärts."""
import asyncio, base64, functools, http.server, json, math, os, socketserver, subprocess, sys, threading, time
from pathlib import Path
import numpy as np, cv2
from playwright.async_api import async_playwright
D = Path("stage")
SHUTTER, SPACING, SMAX, CALM = 0.5, 3.0, 20, 1.5   # Belichtung in Bildern, Abstand der Abtastungen in px, Obergrenze, Ruhe-Schwelle in px
class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
srv = socketserver.ThreadingTCPServer(("127.0.0.1", 0), functools.partial(Q, directory=str(D)))
port = srv.server_address[1]; threading.Thread(target=srv.serve_forever, daemon=True).start()

async def open_page(p):
    b = await p.chromium.launch(args=["--force-color-profile=srgb", "--font-render-hinting=none", "--disable-lcd-text", "--disable-checker-imaging", "--disable-partial-raster", "--disable-gpu-rasterization"])
    ctx = await b.new_context(viewport={"width": 1920, "height": 1080}, device_scale_factor=1)
    pg = await ctx.new_page(); errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
    await pg.goto(f"http://127.0.0.1:{port}/index.html", wait_until="networkidle")
    await pg.evaluate("document.fonts.ready")
    await pg.wait_for_function("window.__ready === true", timeout=20000)
    cdp = await ctx.new_cdp_session(pg)
    return b, pg, cdp, errs

async def shot(pg, cdp, t, ft):
    await pg.evaluate(f"window.__seek({t:.6f}, {ft:.6f})")
    r = await cdp.send("Page.captureScreenshot", {"format": "png", "optimizeForSpeed": True})
    return cv2.imdecode(np.frombuffer(base64.b64decode(r["data"]), np.uint8), cv2.IMREAD_COLOR)

LUT = ((np.arange(256) / 255.0) ** 2.2).astype(np.float32)          # sRGB -> linear (Näherung genügt fürs Mitteln)
def to_srgb(lin): return np.clip(np.power(np.clip(lin, 0, 1), 1 / 2.2) * 255 + 0.5, 0, 255).astype(np.uint8)

def samples(motion, i):
    """Abtastungen für Bild i aus der gemessenen Bewegung (Kantenweg zum Vor- und Nachbild)"""
    d = motion[i]; n = motion[i + 1] if i + 1 < len(motion) else 0
    L = SHUTTER * max(d, n)
    return 1 if L < CALM else min(SMAX, int(math.ceil(L / SPACING)) + 1)

async def part(p, out, fps, i0, i1, motion, tag, blur):
    b, pg, cdp, errs = await open_page(p)
    ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", "1920x1080", "-framerate", str(fps), "-i", "-",
                           "-c:v", "libx264", "-preset", "ultrafast", "-qp", "0", "-pix_fmt", "yuv444p",
                           "-vf", "scale=out_color_matrix=bt709:out_range=tv", "-colorspace", "bt709", "-color_primaries", "bt709",
                           "-color_trc", "bt709", "-color_range", "tv", out], stdin=subprocess.PIPE)
    st, total = time.time(), 0
    for i in range(i0, i1):
        t = i / fps
        S = samples(motion, i) if blur and motion else 1
        if S == 1:
            img = await shot(pg, cdp, t, t)
        else:
            acc = None
            for k in range(S):
                ts = t + ((k + 0.5) / S - 0.5) * SHUTTER / fps
                x = LUT[await shot(pg, cdp, ts, t)]
                acc = x if acc is None else acc + x
            img = to_srgb(acc / S)
        total += S
        ff.stdin.write(img.tobytes())
        if (i - i0) % 300 == 0: print(f"  [{tag}] Bild {i - i0}/{i1 - i0}, Aufnahmen {total}, {time.time() - st:.0f}s", flush=True)
    ff.stdin.close(); ff.wait()
    print(f"  [{tag}] fertig: {i1 - i0} Bilder aus {total} Aufnahmen in {time.time() - st:.0f}s, Fehler:", errs or "keine", flush=True)
    await b.close()

async def video(out, fps, parts, blur, t0, t1):
    async with async_playwright() as p:
        b, pg, cdp, errs = await open_page(p)
        dur = await pg.evaluate("window.__dur"); await b.close()
        motion = json.load(open("motion.json"))["disp"] if blur else None
        if motion is not None and len(motion) < int(round(dur * fps)): raise SystemExit("motion.json passt nicht zur Länge – erst probe")
        a, z = int(round((t0 or 0) * fps)), int(round((t1 if t1 is not None else dur) * fps))
        if motion:   # Abschnitte nach Aufwand teilen, nicht nach Bildzahl
            cost = np.cumsum([samples(motion, i) * 1.0 + 0.4 for i in range(a, z)])
            cuts = [a] + [a + int(np.searchsorted(cost, cost[-1] * k / parts)) for k in range(1, parts)] + [z]
        else:
            cuts = [a + round((z - a) * k / parts) for k in range(parts + 1)]
        Path("out").mkdir(exist_ok=True)
        names = [f"out/part{k}.mkv" for k in range(parts)]
        await asyncio.gather(*[part(p, names[k], fps, cuts[k], cuts[k + 1], motion, k, blur) for k in range(parts)])
    Path("out/parts.txt").write_text("".join(f"file '{Path(x).name}'\n" for x in names))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", "out/parts.txt", "-c", "copy", out], check=True)
    for x in names: os.remove(x)
    print("Bilder:", z - a, "->", out)

async def probe(fps):
    async with async_playwright() as p:
        b, pg, cdp, errs = await open_page(p)
        dur = await pg.evaluate("window.__dur")
        n = int(round(dur * fps))
        disp = await pg.evaluate(f"(() => {{ const out = []; window.__probeReset(); for (let i = 0; i < {n}; i++) out.push(Math.round(window.__probe(i / {fps}) * 100) / 100); return out; }})()")
        await b.close()
    json.dump({"fps": fps, "disp": disp}, open("motion.json", "w"))
    S = [samples(disp, i) for i in range(n)]
    print(f"Bilder {n}, bewegt {sum(1 for s in S if s > 1)}, Aufnahmen gesamt {sum(S)} (Faktor {sum(S) / n:.2f}), größter Weg {max(disp):.0f}px")
    print("Fehler:", errs or "keine")

async def cues():
    async with async_playwright() as p:
        b, pg, cdp, errs = await open_page(p)
        d = await pg.evaluate("({sfx: window.__sfx, B: window.__B, dur: window.__dur})")
        await b.close()
    json.dump(d, open("cues.json", "w"), ensure_ascii=False, indent=1)
    print(len(d["sfx"]), "Geräusche, Länge", d["dur"])

if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    opts = dict(a[2:].split("=", 1) if "=" in a else (a[2:], True) for a in sys.argv[1:] if a.startswith("--"))
    if args[0] == "cues": asyncio.run(cues())
    elif args[0] == "probe": asyncio.run(probe(int(args[1]) if len(args) > 1 else 60))
    else:
        fps = int(args[2]) if len(args) > 2 else 60
        parts = int(args[3]) if len(args) > 3 else 2
        asyncio.run(video(args[1], fps, parts, not opts.get("noblur"), float(opts["from"]) if "from" in opts else None, float(opts["to"]) if "to" in opts else None))
    srv.shutdown()
