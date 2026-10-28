"""Prüft, ob ein Bild gleich aussieht – egal ob die Seite direkt dorthin springt oder vorwärts dorthin läuft."""
import asyncio, sys, numpy as np

import render
from playwright.async_api import async_playwright
TS = [5.6, 14.5, 21.0, 26.4, 31.2, 38.9, 44.0, 46.6, 50.8, 60.9, 64.8, 72.0, 78.6, 82.9, 90.5]
async def main():
    async with async_playwright() as p:
        b1, pg1, c1, e1 = await render.open_page(p)
        seq = {}
        t = 0.0
        while t < max(TS) + 0.01:
            await pg1.evaluate(f"window.__seek({t:.4f})")
            for x in TS:
                if abs(x - t) < 1e-6: seq[x] = await render.shot(pg1, c1, x, x)
            t = round(t + 0.1, 4)
        await b1.close()
        for x in TS:
            b2, pg2, c2, e2 = await render.open_page(p)
            d = await render.shot(pg2, c2, x, x)
            await b2.close()
            diff = np.abs(d.astype(int) - seq[x].astype(int))
            print(f"{x:6.2f}s  größte Abweichung {diff.max():3d}, Pixel >8: {(diff.max(2) > 8).sum()}")
asyncio.run(main())
