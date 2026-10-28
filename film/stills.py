"""Standbilder zu Filmzeiten: python3 stills.py [--v] [--prefix=x] <t> [<t> ...]  (aufsteigend; Bewegungsunschärfe aus; --v: Hochkant)"""
import asyncio, functools, http.server, socketserver, sys, threading
from pathlib import Path
from playwright.async_api import async_playwright
V = "--v" in sys.argv
if V: sys.argv.remove("--v")
D = Path("stage_v" if V else "stage")
W, H = (1080, 1920) if V else (1920, 1080)
class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
srv = socketserver.ThreadingTCPServer(("127.0.0.1", 0), functools.partial(Q, directory=str(D)))
port = srv.server_address[1]; threading.Thread(target=srv.serve_forever, daemon=True).start()
async def main(ts, prefix):
    async with async_playwright() as p:
        b = await p.chromium.launch(args=["--force-color-profile=srgb", "--font-render-hinting=none", "--disable-lcd-text"])
        pg = await b.new_page(viewport={"width": W, "height": H})
        errs = []; pg.on("pageerror", lambda e: errs.append(str(e))); pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
        await pg.goto(f"http://127.0.0.1:{port}/index.html", wait_until="networkidle")
        await pg.evaluate("document.fonts.ready")
        await pg.wait_for_function("window.__ready === true", timeout=15000)
        Path("stills_v" if V else "stills").mkdir(exist_ok=True)
        for t in ts:
            await pg.evaluate(f"window.__seek({t})")
            await pg.screenshot(path=f"{'stills_v' if V else 'stills'}/{prefix}{t:06.2f}.png")
        print("Fehler:", errs or "keine")
        await b.close()
pre = ""
args = sys.argv[1:]
if args and args[0].startswith("--prefix="): pre = args.pop(0).split("=", 1)[1]
asyncio.run(main([float(x) for x in args], pre))
srv.shutdown()
