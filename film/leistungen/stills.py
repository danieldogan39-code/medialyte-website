"""Standbilder einer Bühne: python3 stills.py <n> <t1> <t2> … -> look/f<n>_sheet.png (und Fehler der Seite)"""
import asyncio, functools, http.server, socketserver, sys, threading
from pathlib import Path
from PIL import Image, ImageDraw
n, ts = sys.argv[1], [float(x) for x in sys.argv[2:]]
D = Path(f"f{n}/stage_v"); Path("look").mkdir(exist_ok=True)
class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
srv = socketserver.ThreadingTCPServer(("127.0.0.1", 0), functools.partial(Q, directory=str(D)))
threading.Thread(target=srv.serve_forever, daemon=True).start()
async def main():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch(args=["--force-color-profile=srgb", "--font-render-hinting=none"])
        pg = await b.new_page(viewport={"width": 1080, "height": 1920})
        errs = []; pg.on("pageerror", lambda e: errs.append(str(e))); pg.on("console", lambda m: errs.append(m.text) if m.type in ("error", "warning") else None)
        await pg.goto(f"http://127.0.0.1:{srv.server_address[1]}/index.html", wait_until="networkidle")
        try: await pg.wait_for_function("window.__ready === true", timeout=20000)
        except Exception as e: print("nicht bereit", errs); raise
        W, H = 270, 480; cols = min(8, len(ts)); rows = (len(ts) + cols - 1) // cols
        s = Image.new("RGB", (cols * W, rows * (H + 20)), "white"); d = ImageDraw.Draw(s)
        for i, t in enumerate(ts):
            await pg.evaluate(f"window.__seek({t})")
            f = f"look/f{n}_{t:06.2f}.png"; await pg.screenshot(path=f)
            x, y = (i % cols) * W, (i // cols) * (H + 20)
            s.paste(Image.open(f).convert("RGB").resize((W, H), Image.LANCZOS), (x, y + 20)); d.text((x + 4, y + 4), f"{t:.2f}", fill="black")
        s.save(f"look/f{n}_sheet.png"); print("Fehler:", errs or "keine", "Dauer", await pg.evaluate("window.__dur"))
        await b.close()
asyncio.run(main()); srv.shutdown()
