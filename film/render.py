"""Film Bild für Bild rendern (verlustfrei als PNG aus Chromium, dann in eine hochwertige Zwischendatei).
python3 render.py stills <t> [<t> ...]        Einzelbilder nach stills/ (Zeiten aufsteigend angeben)
python3 render.py video <out.mkv> [fps] [teile]  ganzer Film, in <teile> parallelen Abschnitten
Die Zeitleiste ist pausiert und wird über window.__seek(t) gestellt; Rückrufe (Texte, Klassen) laufen dabei
in Reihenfolge, deshalb rendert jeder Abschnitt ab seinem Anfang streng vorwärts."""
import asyncio, base64, functools, http.server, os, socketserver, subprocess, sys, threading, time
from pathlib import Path
from playwright.async_api import async_playwright
D = Path("stage")
class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
srv = socketserver.ThreadingTCPServer(("127.0.0.1", 0), functools.partial(Q, directory=str(D)))
port = srv.server_address[1]; threading.Thread(target=srv.serve_forever, daemon=True).start()

async def open_page(p):
    b = await p.chromium.launch(args=["--force-color-profile=srgb", "--font-render-hinting=none", "--disable-lcd-text"])
    ctx = await b.new_context(viewport={"width": 1920, "height": 1080}, device_scale_factor=1)
    pg = await ctx.new_page(); errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
    await pg.goto(f"http://127.0.0.1:{port}/index.html", wait_until="networkidle")
    await pg.evaluate("document.fonts.ready")
    await pg.wait_for_function("window.__ready === true", timeout=10000)
    cdp = await ctx.new_cdp_session(pg)
    return b, pg, cdp, errs

async def grab(pg, cdp, t):
    await pg.evaluate(f"window.__seek({t})")
    r = await cdp.send("Page.captureScreenshot", {"format": "png", "optimizeForSpeed": True})
    return base64.b64decode(r["data"])

async def stills(ts):
    async with async_playwright() as p:
        b, pg, cdp, errs = await open_page(p)
        Path("stills").mkdir(exist_ok=True)
        for t in ts:
            Path(f"stills/t{float(t):06.2f}.png").write_bytes(await grab(pg, cdp, t))
        print("Fehler:", errs or "keine")
        await b.close()

async def part(p, out, fps, i0, i1, tag):
    b, pg, cdp, errs = await open_page(p)
    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "image2pipe", "-framerate", str(fps), "-c:v", "png", "-i", "-",
           "-c:v", "libx264", "-preset", "ultrafast", "-qp", "0", "-pix_fmt", "yuv444p",
           "-vf", "scale=out_color_matrix=bt709:out_range=tv",
           "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv", out]
    ff = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    st = time.time()
    for i in range(i0, i1):
        ff.stdin.write(await grab(pg, cdp, i / fps))
        if (i - i0) % 600 == 0: print(f"  [{tag}] Bild {i - i0}/{i1 - i0}  {time.time() - st:.0f}s", flush=True)
    ff.stdin.close(); ff.wait()
    print(f"  [{tag}] fertig in {time.time() - st:.0f}s, Fehler:", errs or "keine", flush=True)
    await b.close()

async def video(out, fps, parts):
    async with async_playwright() as p:
        b, pg, cdp, errs = await open_page(p)
        dur = await pg.evaluate("window.__dur"); await b.close()
        n = int(round(dur * fps))
        cuts = [round(n * k / parts) for k in range(parts + 1)]
        names = [f"out/part{k}.mkv" for k in range(parts)]
        await asyncio.gather(*[part(p, names[k], fps, cuts[k], cuts[k + 1], k) for k in range(parts)])
    Path("out/parts.txt").write_text("".join(f"file '{Path(x).name}'\n" for x in names))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", "out/parts.txt", "-c", "copy", out], check=True)
    for x in names: os.remove(x)
    print("Bilder:", n, "->", out)

if sys.argv[1] == "stills": asyncio.run(stills([float(x) for x in sys.argv[2:]]))
else:
    fps = int(sys.argv[3]) if len(sys.argv) > 3 else 60
    parts = int(sys.argv[4]) if len(sys.argv) > 4 else 2
    asyncio.run(video(sys.argv[2], fps, parts))
srv.shutdown()
