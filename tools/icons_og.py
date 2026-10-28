"""Erzeugt Favicon-PNGs und das Vorschaubild für soziale Netzwerke (og.jpg) mit Chromium.
Aufruf: python3 tools/icons_og.py
"""
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "src/assets/img"
import base64
FONT = "data:font/woff2;base64," + base64.b64encode((ROOT / "src/assets/fonts/outfit-latin-wght-normal.woff2").read_bytes()).decode()
LOGO = (ROOT / "tools/logo-inline.svg").read_text()
FAV = (IMG / "favicon.svg").read_text()

WORDMARK = (ROOT / "tools/wordmark.svg").read_text()
OG = f"""<!doctype html><html><head><style>
@font-face{{font-family:Outfit;src:url('{FONT}') format('woff2');font-weight:100 900}}
*{{margin:0;box-sizing:border-box}}
body{{width:1200px;height:630px;background:#0E192A;font-family:Outfit,sans-serif;color:#F3F5F9;position:relative;overflow:hidden}}
.g{{position:absolute;left:50%;top:-520px;width:1700px;height:1060px;margin-left:-850px;border-radius:50%;background:radial-gradient(closest-side,rgba(64,98,158,.5),rgba(40,64,108,.2) 45%,transparent 72%)}}
.d{{position:absolute;inset:0;background-image:linear-gradient(rgba(170,190,220,.06) 1px,transparent 1px),linear-gradient(90deg,rgba(170,190,220,.06) 1px,transparent 1px);background-size:72px 72px;-webkit-mask-image:radial-gradient(70% 60% at 50% 25%,#000,transparent 80%)}}
.w{{position:absolute;left:88px;top:80px;right:88px;bottom:76px;display:flex;flex-direction:column;justify-content:space-between}}
.logo{{display:flex;align-items:center;gap:16px}}
.logo .mono{{height:62px;width:auto;color:#FF5757}}
.logo .wordmark{{height:45px;width:auto;color:#F3F5F9;margin-top:7px}}
h1{{font-size:80px;line-height:.98;font-weight:600;letter-spacing:-.048em;max-width:1000px;text-wrap:balance}}
h1 span{{display:block;color:#8A9BB4}}
.f{{display:flex;gap:12px;font-size:23px;color:#C3CDDC}}
.f b{{display:inline-flex;align-items:center;padding:10px 20px;border-radius:999px;border:1px solid rgba(170,190,220,.25);font-weight:500}}
</style></head><body><div class="g"></div><div class="d"></div><div class="w">
<div class="logo">{LOGO.replace('<svg ', '<svg class="mono" ', 1)}{WORDMARK}</div>
<h1>Ihre Website soll Kunden bringen. <span>Nicht Arbeit machen.</span></h1>
<div class="f"><b>Website</b><b>Kundenmanagement</b><b>KI-Agent</b><b>Werbung</b></div>
</div></body></html>"""


async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1200, "height": 630})
        await pg.set_content(OG)
        await pg.evaluate("document.fonts.ready")
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
