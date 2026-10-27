"""Erzeugt Favicon-PNGs und das Vorschaubild für soziale Netzwerke (og.jpg) mit Chromium.
Aufruf: python3 tools/icons_og.py
"""
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "src/assets/img"
FONT = (ROOT / "src/assets/fonts/outfit-latin-wght-normal.woff2").as_uri()
LOGO = (ROOT / "tools/logo-inline.svg").read_text()
FAV = (IMG / "favicon.svg").read_text()

OG = f"""<!doctype html><html><head><style>
@font-face{{font-family:Outfit;src:url('{FONT}') format('woff2');font-weight:100 900}}
*{{margin:0;box-sizing:border-box}}
body{{width:1200px;height:630px;background:#0E192A;font-family:Outfit,sans-serif;color:#fff;position:relative;overflow:hidden}}
.g{{position:absolute;inset:0;background:radial-gradient(50% 70% at 85% 20%,rgba(255,87,87,.28),transparent 70%),radial-gradient(40% 60% at 0% 100%,rgba(91,140,255,.14),transparent 70%)}}
.d{{position:absolute;inset:0;background-image:radial-gradient(rgba(255,255,255,.07) 1px,transparent 1px);background-size:28px 28px}}
.w{{position:absolute;left:84px;top:78px;right:84px;bottom:70px;display:flex;flex-direction:column;justify-content:space-between}}
.logo{{display:flex;align-items:center;gap:18px;font-size:34px;font-weight:700;letter-spacing:-.02em}}
.logo svg{{width:86px;color:#FF5757}}
h1{{font-size:70px;line-height:1.04;font-weight:700;letter-spacing:-.03em;max-width:930px}}
h1 span{{color:#FF5757}}
.f{{display:flex;gap:14px;font-size:24px;color:#C9CED6}}
.f b{{display:inline-flex;align-items:center;gap:10px;padding:10px 18px;border-radius:999px;border:1px solid #3A4556;font-weight:500}}
</style></head><body><div class="g"></div><div class="d"></div><div class="w">
<div class="logo">{LOGO}Medialyte</div>
<h1>Individuelle Lösungen zur <span>Entwicklung</span> von Kundenbeziehungen</h1>
<div class="f"><b>Websites</b><b>Kundenmanagement</b><b>KI-Agent</b><b>Werbung</b></div>
</div></body></html>"""


async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1200, "height": 630})
        await pg.set_content(OG)
        await pg.wait_for_timeout(400)
        await pg.screenshot(path=str(IMG / "og.jpg"), type="jpeg", quality=88)
        for size, name in [(32, "favicon-32.png"), (180, "apple-touch-icon.png"), (512, "icon-512.png")]:
            pg2 = await b.new_page(viewport={"width": size, "height": size})
            await pg2.set_content(f"<style>*{{margin:0}}svg{{width:{size}px;height:{size}px;display:block}}</style>{FAV}")
            await pg2.screenshot(path=str(IMG / name), omit_background=True)
            await pg2.close()
        await b.close()
    print("og.jpg und Icons erstellt")

asyncio.run(main())
