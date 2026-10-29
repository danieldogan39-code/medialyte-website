"""Titelbild eines Leistungsfilms: python3 cover.py <n> <t>  ->  f<n>/out/cover.jpg (1080 × 1920; Logo unten, Inhalt im 3:4-Ausschnitt des Profilrasters)"""
import asyncio, functools, http.server, socketserver, sys, threading
from pathlib import Path
from PIL import Image
n, t = sys.argv[1], float(sys.argv[2])
FIX = {"2": "['#lq1','#lq2','#lq3'].forEach(function(s){gsap.set(s,{clearProps:'transform,filter,opacity,visibility'});});"}
D = Path(f"f{n}/stage_v"); Path(f"f{n}/out").mkdir(exist_ok=True)
class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
srv = socketserver.ThreadingTCPServer(("127.0.0.1", 0), functools.partial(Q, directory=str(D)))
threading.Thread(target=srv.serve_forever, daemon=True).start()
async def main():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch(args=["--force-color-profile=srgb", "--font-render-hinting=none"])
        pg = await b.new_page(viewport={"width": 1080, "height": 1920})
        await pg.goto(f"http://127.0.0.1:{srv.server_address[1]}/index.html", wait_until="networkidle")
        await pg.wait_for_function("window.__ready === true", timeout=20000)
        await pg.evaluate(f"window.__seek({t})")
        await pg.evaluate(FIX.get(n, ""))
        await pg.evaluate("""() => {
          const l = document.querySelector('#lock').cloneNode(true); l.removeAttribute('id');
          l.querySelectorAll('[id]').forEach(e => { if (!e.closest('svg')) e.removeAttribute('id'); });
          l.querySelectorAll('.lock__mk,.lock__wm').forEach(e => { e.style.opacity = 1; e.style.visibility = 'visible'; e.style.transform = 'none'; e.style.clipPath = 'none'; });
          const w = document.createElement('div');
          w.style.cssText = 'position:absolute;left:0;right:0;top:1400px;display:flex;justify-content:center;z-index:60;transform:scale(.62);transform-origin:50% 0';
          w.appendChild(l); document.querySelector('#stage').appendChild(w);
        }""")
        await pg.screenshot(path=f"f{n}/out/cover.png")
        await b.close()
asyncio.run(main()); srv.shutdown()
Image.open(f"f{n}/out/cover.png").convert("RGB").save(f"f{n}/out/cover.jpg", quality=93)
print("Titelbild", n)
