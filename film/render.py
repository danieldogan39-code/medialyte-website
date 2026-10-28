"""Film rendern. python3 render.py stills <t> [<t> ...]   |   python3 render.py video <out.mp4> [fps] [von] [bis]"""
import asyncio, sys, functools, http.server, socketserver, threading, subprocess, time
from pathlib import Path
from playwright.async_api import async_playwright
D = Path("stage")
class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
srv = socketserver.ThreadingTCPServer(("127.0.0.1", 0), functools.partial(Q, directory=str(D)))
port = srv.server_address[1]; threading.Thread(target=srv.serve_forever, daemon=True).start()
async def open_page(p):
    b = await p.chromium.launch(args=["--disable-gpu-vsync", "--force-color-profile=srgb", "--font-render-hinting=none"])
    ctx = await b.new_context(viewport={"width": 1920, "height": 1080}, device_scale_factor=1)
    pg = await ctx.new_page(); errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
    await pg.goto(f"http://127.0.0.1:{port}/index.html", wait_until="networkidle")
    await pg.evaluate("document.fonts.ready")
    await pg.wait_for_function("window.__ready === true", timeout=10000)
    return b, pg, errs
async def stills(ts):
    async with async_playwright() as p:
        b, pg, errs = await open_page(p)
        Path("stills").mkdir(exist_ok=True)
        for t in ts:
            await pg.evaluate(f"window.__seek({t})")
            await pg.screenshot(path=f"stills/t{float(t):06.2f}.png")
        print("Fehler:", errs)
        await b.close()
async def video(out, fps, t0, t1):
    async with async_playwright() as p:
        b, pg, errs = await open_page(p)
        dur = await pg.evaluate("window.__dur")
        t1 = min(t1 if t1 else dur, dur)
        n = int(round((t1 - t0) * fps))
        cmd = ["ffmpeg", "-v", "error", "-y", "-f", "image2pipe", "-framerate", str(fps), "-c:v", "mjpeg", "-i", "-",
               "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-pix_fmt", "yuv420p", "-r", str(fps), out]
        ff = subprocess.Popen(cmd, stdin=subprocess.PIPE)
        st = time.time()
        for i in range(n):
            await pg.evaluate(f"window.__seek({t0 + i / fps})")
            ff.stdin.write(await pg.screenshot(type="jpeg", quality=95))
            if i % 300 == 0: print(f"  Bild {i}/{n}  {time.time() - st:.0f}s", flush=True)
        ff.stdin.close(); ff.wait()
        print("Fehler:", errs, "Dauer", round(time.time() - st), "s")
        await b.close()
if sys.argv[1] == "stills": asyncio.run(stills([float(x) for x in sys.argv[2:]]))
else:
    fps = int(sys.argv[3]) if len(sys.argv) > 3 else 30
    asyncio.run(video(sys.argv[2], fps, float(sys.argv[4]) if len(sys.argv) > 4 else 0.0, float(sys.argv[5]) if len(sys.argv) > 5 else None))
srv.shutdown()
