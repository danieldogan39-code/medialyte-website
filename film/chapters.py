"""Kapitelmarken für die Website aus den Szenengrenzen der Bühne (window.__B) und die Filmlänge."""
import asyncio, functools, http.server, socketserver, threading
from playwright.async_api import async_playwright
class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
srv = socketserver.ThreadingTCPServer(("127.0.0.1", 0), functools.partial(Q, directory="stage"))
threading.Thread(target=srv.serve_forever, daemon=True).start()
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page()
        await pg.goto(f"http://127.0.0.1:{srv.server_address[1]}/index.html"); await pg.wait_for_function("window.__ready === true")
        B, dur = await pg.evaluate("[window.__B, window.__dur]")
        await b.close()
    print("Länge", dur, "->", f"{int(round(dur)) // 60}:{int(round(dur)) % 60:02d}")
    for name, k in [("Die Ausgangslage", None), ("Unser Ablauf", "C"), ("Der Unterschied", "EF"), ("Ihr KI-Agent", "HI")]:
        print(f"{name:18s}", 0 if k is None else round(max(0, B[k] - 0.1), 1))
asyncio.run(main())
