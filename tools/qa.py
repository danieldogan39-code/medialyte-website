"""Lokale Sichtprüfung: startet einen Server auf preview/, macht Screenshots und sammelt Konsolenfehler.
Aufruf: python3 tools/qa.py <ausgabeordner> [pfad ...]
"""
import asyncio, sys, threading, http.server, functools, socketserver
from pathlib import Path
from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parent.parent
PREV = ROOT / "preview"
OUT = Path(sys.argv[1]); OUT.mkdir(parents=True, exist_ok=True)
PATHS = sys.argv[2:] or ["/_qa.html"]

# Startseite wie im Artifact in ein Dokument-Gerüst packen
frag = (PREV / "index.html").read_text()
(PREV / "_qa.html").write_text('<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover"></head><body>' + frag + '</body></html>')

class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
srv = socketserver.TCPServer(("127.0.0.1", 0), functools.partial(Q, directory=str(PREV)))
port = srv.server_address[1]
threading.Thread(target=srv.serve_forever, daemon=True).start()

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for path in PATHS:
            name = path.strip("/").replace("/", "_").replace(".html", "") or "home"
            for label, vp, mob in [("d", {"width": 1440, "height": 900}, False), ("m", {"width": 390, "height": 844}, True)]:
                ctx = await b.new_context(viewport=vp, device_scale_factor=1, is_mobile=mob, has_touch=mob, locale="de-DE", reduced_motion="reduce")
                pg = await ctx.new_page()
                errs = []
                pg.on("console", lambda m: errs.append(f"{m.type}: {m.text}") if m.type in ("error", "warning") else None)
                pg.on("pageerror", lambda e: errs.append(f"pageerror: {e}"))
                pg.on("requestfailed", lambda r: errs.append(f"failed: {r.url}"))
                await pg.goto(f"http://127.0.0.1:{port}{path}", wait_until="networkidle")
                h = await pg.evaluate("document.documentElement.scrollHeight")
                for y in range(0, h, 700):
                    await pg.evaluate(f"window.scrollTo(0,{y})"); await pg.wait_for_timeout(60)
                await pg.evaluate("window.scrollTo(0,0)"); await pg.wait_for_timeout(700)
                w = await pg.evaluate("[document.documentElement.scrollWidth, document.documentElement.clientWidth]")
                await pg.screenshot(path=str(OUT / f"{name}-{label}.png"), full_page=True)
                print(name, label, "scrollWidth/clientWidth", w, "errors:", errs[:8])
                await ctx.close()
        await b.close()
asyncio.run(main())
srv.shutdown()
