"""Sichtprüfung der Vorschau: Bildschirmfotos einzelner Bereiche bei echter Bewegung.

Aufruf:
  python3 tools/shots.py <ausgabe> [breite x höhe ...] [--page /pfad/] [--full] [--reduce]
Beispiel:
  python3 tools/shots.py /tmp/qa 1440x900 390x844
Ohne --page wird die Startseite (in ein Dokument-Gerüst verpackt) geprüft.
"""
import asyncio
import functools
import http.server
import socketserver
import sys
import threading
from pathlib import Path

from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parent.parent
PREV = ROOT / "preview"
args = sys.argv[1:]
OUT = Path(args.pop(0)); OUT.mkdir(parents=True, exist_ok=True)
page_path = "/_qa.html"
full = "--full" in args
reduce = "--reduce" in args
if "--page" in args:
    page_path = args[args.index("--page") + 1]
sizes = [a for a in args if "x" in a and a[0].isdigit()] or ["1440x900", "390x844"]

frag = (PREV / "index.html").read_text()
(PREV / "_qa.html").write_text('<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover"></head><body>' + frag + '</body></html>')


class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass


srv = socketserver.TCPServer(("127.0.0.1", 0), functools.partial(Q, directory=str(PREV)))
port = srv.server_address[1]
threading.Thread(target=srv.serve_forever, daemon=True).start()

SECTIONS = ["start", "idee", "leistungen", "referenzen", "ergebnisse", "vergleich", "pakete", "ablauf", "team", "film", "faq", "termin"]


async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for s in sizes:
            w, h = map(int, s.split("x"))
            mob = w < 800
            ctx = await b.new_context(viewport={"width": w, "height": h}, device_scale_factor=1, is_mobile=mob, has_touch=mob,
                                      locale="de-DE", reduced_motion="reduce" if reduce else "no-preference")
            pg = await ctx.new_page()
            errs = []
            pg.on("console", lambda m: errs.append(f"{m.type}: {m.text}") if m.type in ("error", "warning") else None)
            pg.on("pageerror", lambda e: errs.append(f"pageerror: {e}"))
            pg.on("requestfailed", lambda r: errs.append(f"failed: {r.url}"))
            await pg.goto(f"http://127.0.0.1:{port}{page_path}", wait_until="networkidle")
            await pg.wait_for_timeout(2600)
            tag = f"{w}"
            await pg.screenshot(path=str(OUT / f"{tag}-00-top.png"))
            if full:
                hh = await pg.evaluate("document.documentElement.scrollHeight")
                for y in range(0, hh, 600):
                    await pg.evaluate(f"window.scrollTo(0,{y})"); await pg.wait_for_timeout(50)
                await pg.wait_for_timeout(800)
                await pg.screenshot(path=str(OUT / f"{tag}-full.png"), full_page=True)
            elif page_path == "/_qa.html":
                for i, sid in enumerate(SECTIONS[1:], 1):
                    ok = await pg.evaluate(f"(function(){{var el=document.getElementById('{sid}'); if(!el) return false; window.scrollTo(0, el.getBoundingClientRect().top + scrollY - 10); return true;}})()")
                    if not ok:
                        continue
                    await pg.wait_for_timeout(2200)
                    await pg.screenshot(path=str(OUT / f"{tag}-{i:02d}-{sid}.png"))
                    if sid == "leistungen":
                        # angeheftete Kundenreise: mehrere Positionen
                        top = await pg.evaluate("document.querySelector('[data-journey]').getBoundingClientRect().top + scrollY")
                        for k in range(8):
                            await pg.evaluate(f"window.scrollTo(0,{top} + {k} * innerHeight * 0.75)")
                            await pg.wait_for_timeout(1500)
                            await pg.screenshot(path=str(OUT / f"{tag}-{i:02d}-{sid}-{k}.png"))
            sw = await pg.evaluate("[document.documentElement.scrollWidth, document.documentElement.clientWidth]")
            print(s, "scrollWidth/clientWidth", sw, "errors:", errs[:8])
            await ctx.close()
        await b.close()


asyncio.run(main())
srv.shutdown()
