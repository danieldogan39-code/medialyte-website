import asyncio, sys
from playwright.async_api import async_playwright
SVG = open(sys.argv[1]).read()
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page()
        await pg.set_content(f"<body style='margin:0'>{SVG}</body>")
        bb = await pg.evaluate("(()=>{const g=document.querySelector('svg > g'); const r=g.getBBox(); return [r.x,r.y,r.width,r.height]})()")
        print(*bb)
        await b.close()
asyncio.run(main())
