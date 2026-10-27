"""Funktionstest der Vorschau: Buchung komplett durchklicken, Referenz-Popup, Kundenreise."""
import asyncio, sys, threading, http.server, functools, socketserver
from pathlib import Path
from playwright.async_api import async_playwright
ROOT = Path(__file__).resolve().parent.parent; PREV = ROOT / "preview"; OUT = Path(sys.argv[1])
(PREV / "_qa.html").write_text('<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"></head><body>' + (PREV / "index.html").read_text() + '</body></html>')
class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
srv = socketserver.TCPServer(("127.0.0.1", 0), functools.partial(Q, directory=str(PREV))); port = srv.server_address[1]
threading.Thread(target=srv.serve_forever, daemon=True).start()
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        ctx = await b.new_context(viewport={"width": 1440, "height": 900}, locale="de-DE")
        pg = await ctx.new_page(); errs = []
        pg.on("pageerror", lambda e: errs.append(str(e))); pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
        await pg.goto(f"http://127.0.0.1:{port}/_qa.html", wait_until="networkidle")
        # Kundenreise: Station 3 (Chat)
        await pg.click("#jt-2"); await pg.wait_for_timeout(5500)
        vis = await pg.is_visible("#jp-2 .chat")
        await pg.locator("#reise").screenshot(path=str(OUT / "flow-journey.png"))
        print("journey chat visible:", vis)
        # Vorher/Nachher-Regler
        await pg.locator(".ba input").first.fill("25")
        print("ba pos:", await pg.evaluate("getComputedStyle(document.querySelector('.ba')).getPropertyValue('--pos')"))
        # Buchung
        await pg.locator("#beratung").scroll_into_view_if_needed()
        await pg.click("label[for=bk-anliegen-web-neu]"); await pg.click("[data-next]")
        await pg.fill("#bk-firma", "Testfirma GmbH"); await pg.select_option("#bk-branche", index=2); await pg.click("[data-next]")
        await pg.click("label[for=bk-format-video]")
        await pg.click(".cal__day.is-avail >> nth=0"); await pg.click(".slot >> nth=1")
        await pg.locator("#booking").screenshot(path=str(OUT / "flow-cal.png"))
        await pg.click("[data-next]")
        await pg.fill("#bk-name", "Max Mustermann"); await pg.fill("#bk-email", "max@example.com")
        await pg.click("#bk-consent"); await pg.click("[data-next]")
        await pg.wait_for_timeout(1500)
        done = await pg.is_visible(".done")
        print("booking done visible:", done, "| when:", await pg.text_content(".done__when"))
        await pg.locator("#booking").screenshot(path=str(OUT / "flow-done.png"))
        # Referenz-Popup
        await pg.locator("#referenzen").scroll_into_view_if_needed()
        await pg.click(".ref >> nth=2"); await pg.wait_for_timeout(2500)
        print("dialog open:", await pg.evaluate("document.getElementById('ref-dialog').open"), "| img:", await pg.get_attribute(".rd__scroll img", "src"))
        await pg.screenshot(path=str(OUT / "flow-dialog.png"))
        await pg.click(".seg button[data-view=mobile]"); await pg.wait_for_timeout(1500)
        await pg.screenshot(path=str(OUT / "flow-dialog-m.png"))
        await pg.keyboard.press("Escape")
        print("errors:", errs)
        await b.close()
asyncio.run(main()); srv.shutdown()
