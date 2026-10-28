"""Funktionstest der Vorschau: alle Interaktionen durchklicken, Fehler und Layout-Verschiebungen messen.

Aufruf: python3 tools/flow_test.py <ausgabeordner>
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
import os
PREV = Path(os.environ.get("ML_PREVIEW", ROOT / "preview"))
OUT = Path(sys.argv[1]); OUT.mkdir(parents=True, exist_ok=True)
(PREV / "_qa.html").write_text('<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"></head><body>' + (PREV / "index.html").read_text() + '</body></html>')


sys.path.insert(0, str(ROOT / "tools"))
from qa_server import serve  # noqa: E402  (Server mit Byte-Bereichen, damit der Film springen kann)

srv, BASE = serve(PREV)
fails = []


def check(name, ok, info=""):
    print(("OK   " if ok else "FAIL ") + name + (f"  ({info})" if info else ""))
    if not ok:
        fails.append(name)


CLS_JS = """window.__cls=0;window.__shifts=[];new PerformanceObserver(function(l){l.getEntries().forEach(function(e){if(!e.hadRecentInput){window.__cls+=e.value;
 window.__shifts.push({v:e.value,src:(e.sources||[]).map(function(s){return s.node?(s.node.className||s.node.nodeName):''}).join('|')})}})}).observe({type:'layout-shift',buffered:true});"""


async def desktop(b):
    ctx = await b.new_context(viewport={"width": 1440, "height": 900}, locale="de-DE")
    await ctx.add_init_script(CLS_JS)
    pg = await ctx.new_page()
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
    await pg.goto(BASE + "/_qa.html", wait_until="networkidle")
    await pg.wait_for_timeout(1500)

    # Leistungen-Menü
    await pg.click("[data-drop] .nav__link")
    check("Menü Leistungen öffnet", await pg.get_attribute("[data-drop] .nav__link", "aria-expanded") == "true")
    await pg.keyboard.press("Escape")
    check("Menü Leistungen schließt mit Esc", await pg.get_attribute("[data-drop] .nav__link", "aria-expanded") == "false")

    # Cockpit
    await pg.evaluate("window.scrollTo(0, document.querySelector('.cockpit').getBoundingClientRect().top + scrollY - 90)")
    await pg.click(".cp-tab[data-branch=praxis]")
    check("Cockpit wechselt Branche", await pg.get_attribute("[data-cockpit]", "data-branch") == "praxis")
    await pg.wait_for_timeout(5600)
    upd = await pg.evaluate("document.querySelector('.ms--praxis .ms__info').classList.contains('is-upd')")
    check("Cockpit: Agent ändert Website", upd)
    feed = await pg.evaluate("document.querySelectorAll('[data-cp=feed] .cp-feed__item').length")
    check("Cockpit: drei Anfragen im Verlauf", feed == 3, f"{feed}")
    await pg.click(".cp-pause")
    check("Cockpit: Pause", await pg.get_attribute(".cp-pause", "aria-pressed") == "true")
    await pg.click(".cp-tab[data-branch=kanzlei]")
    k = await pg.evaluate("document.querySelector('.ms--kanzlei .ms__info').classList.contains('is-upd')")
    check("Cockpit: angehalten zeigt Endzustand", k)
    await pg.click(".cp-pause")

    # Idee: Selbstcheck → Ergebnis → Buchung mit Vorauswahl
    await pg.evaluate("document.getElementById('idee').scrollIntoView()")
    await pg.wait_for_timeout(600)
    await pg.click(".pillar[data-pillar=vermehrung] .chip[data-a=gap]")
    await pg.click(".pillar[data-pillar=verbesserung] .chip[data-a=ok]")
    await pg.click(".pillar[data-pillar=verwaltung] .chip[data-a=gap]")
    await pg.wait_for_timeout(250)
    ask = await pg.get_attribute("[data-po-cta]", "data-ask")
    check("Idee: Selbstcheck ergibt die Hebel", sorted((ask or "").split(",")) == ["system", "web-besser", "werbung"], ask)
    txt = await pg.text_content("[data-po-text]")
    check("Idee: Ergebnis nennt beide Hebel", "Vermehrung und Verwaltung" in txt, txt)
    check("Idee: Karten zeigen den Stand", await pg.evaluate("document.querySelector('[data-pillar=vermehrung]').classList.contains('is-gap') && document.querySelector('[data-pillar=verbesserung]').classList.contains('is-ok')"))
    await pg.screenshot(path=str(OUT / "flow-idee.png"))
    await pg.click(".pillar[data-pillar=verwaltung] .chip[data-a=gap]")
    await pg.wait_for_timeout(150)
    check("Idee: zweiter Klick nimmt die Antwort zurück", await pg.get_attribute("[data-po-cta]", "data-ask") == "werbung,web-besser" and "Noch eine Frage" not in (await pg.text_content("[data-po-text]")))
    await pg.click(".pillar[data-pillar=verwaltung] .chip[data-a=gap]")
    await pg.click("[data-po-cta]")
    await pg.wait_for_timeout(1400)
    pre = await pg.evaluate("['werbung','web-besser','system','agent'].map(function(v){var i=document.getElementById('bk-anliegen-'+v);return i?i.checked:null})")
    check("Idee: Buchung mit Vorauswahl", pre == [True, True, True, False], str(pre))

    # Startbereich: „Zufriedenheitsgarantie“ führt zur aufgeklappten Antwort
    await pg.evaluate("window.scrollTo(0,0)")
    await pg.wait_for_timeout(400)
    await pg.click(".hero__proof a[href='#faq-garantie']")
    await pg.wait_for_timeout(1800)
    g = await pg.evaluate("(function(){var d=document.getElementById('faq-garantie'),r=d.getBoundingClientRect();return d.open&&r.top>60&&r.top<innerHeight*0.5})()")
    check("Garantie-Link öffnet die Antwort", g)

    # Kundenreise: angeheftete Bühne, Leiste, Relaunch, Pipeline, Agent
    check("Kundenreise: Bühne auf großem Bildschirm", await pg.evaluate("document.querySelector('[data-journey]').classList.contains('journey--pin') && !document.querySelector('.jr__rail').hidden"))
    await pg.evaluate("window.scrollTo(0, document.querySelector('[data-journey]').getBoundingClientRect().top + scrollY + 20)")
    await pg.wait_for_timeout(700)
    check("Kundenreise: Station 1 aktiv", await pg.evaluate("document.querySelector('.st.is-active').id") == "st-0")
    await pg.click(".jr__step[data-go='1']")
    await pg.wait_for_timeout(1500)
    check("Kundenreise: Leiste springt zu Station 2", await pg.evaluate("document.querySelector('.st.is-active').id") == "st-1" and await pg.get_attribute(".jr__step[data-go='1']", "aria-selected") == "true")
    await pg.wait_for_timeout(2400)
    moved = await pg.evaluate("!!document.querySelector('[data-col=gespraech] [data-card=c1]')")
    check("Pipeline: Karte wandert weiter", moved)
    await pg.click(".jr__step[data-go='2']")
    await pg.wait_for_timeout(3800)
    await pg.click(".ad__ask[data-ask-id=zeiten]")
    await pg.wait_for_timeout(2600)
    v = await pg.evaluate("document.querySelector('[data-agent] .v-new').textContent")
    check("Agent-Demo setzt Änderung um", v == "Geöffnet 11–14 Uhr", v)
    n = await pg.evaluate("document.querySelectorAll('[data-wa] .cp-msg').length")
    check("Agent-Demo: höchstens drei Nachrichten", n >= 2 and n <= 3, f"{n} Nachrichten")
    vis = await pg.evaluate("""(function(){var s=document.querySelector('.ad__screen').getBoundingClientRect(),m=document.querySelectorAll('[data-wa] .cp-msg'),l=m[m.length-1].getBoundingClientRect();return l.bottom<=s.bottom+1&&l.top>=s.top-1;})()""")
    check("Agent-Demo: neueste Antwort ganz zu sehen", vis)
    t = await pg.evaluate("Array.from(document.querySelectorAll('[data-wa] .cp-msg time')).map(function(x){return x.textContent.trim()})")
    check("Agent-Demo: feste Uhrzeiten", all(x.startswith("09:") for x in t), str(t))
    await pg.click(".ad__ask[data-ask-id=event]")
    await pg.wait_for_timeout(4800)
    check("Agent-Demo: Veranstaltung erscheint groß mit Button", await pg.evaluate("document.querySelector('[data-agent] .ms').classList.contains('is-event') && !!document.querySelector('[data-ev=b]').textContent"))
    await pg.click(".ad__ask[data-ask-id=zeiten]")
    await pg.wait_for_timeout(2700)
    v2 = await pg.evaluate("document.querySelector('[data-agent] .v-new').textContent")
    check("Agent-Demo: zweiter Klick zeigt eine neue Änderung", v2 != "Geöffnet 11–14 Uhr", v2)
    await pg.screenshot(path=str(OUT / "flow-agent.png"))
    await pg.click(".jr__step[data-go='0']")
    await pg.wait_for_timeout(1500)
    check("Kundenreise: zurück zu Station 1, Relaunch fertig", await pg.evaluate("document.querySelector('.st.is-active').id") == "st-0" and await pg.evaluate("parseFloat(document.querySelector('[data-relaunch]').style.getPropertyValue('--p'))") >= 99)
    await pg.click("[data-rl='0']")
    await pg.wait_for_timeout(1600)
    check("Relaunch: Vorher-Ansicht", await pg.evaluate("document.querySelector('[data-relaunch]').style.getPropertyValue('--p')") == "0%")

    # Ergebnisse: Wirkungskarte mit aktuellem Logo
    await pg.evaluate("document.getElementById('ergebnisse').scrollIntoView()")
    await pg.wait_for_timeout(4000)   # weiches Scrollen (~1 s) plus Hochzählen (1,5 s)
    imp = await pg.evaluate("(function(){var c=document.querySelector('.impact');if(!c)return 'fehlt';var im=c.querySelector('.impact__h img');return c.querySelectorAll('.impact__row').length+'|'+!!(im&&im.complete&&im.naturalWidth)+'|'+c.querySelector('[data-count]').textContent.trim()})()")
    check("Ergebnisse: Wirkungskarte mit Logo", imp == "4|true|230", imp)

    # Paket-Finder → Buchung
    await pg.evaluate("document.getElementById('pakete').scrollIntoView()")
    await pg.select_option("[data-finder] select[name=branche]", "kanzlei")
    await pg.select_option("[data-finder] select[name=ziel]", "verwaltung")
    check("Finder empfiehlt System", await pg.text_content("[data-fr=name]") == "System")
    check("Finder markiert Paket", await pg.evaluate("document.querySelector('[data-plan=system]').classList.contains('is-match')"))
    check("Finder zeigt Auswahl", (await pg.text_content(".finder__sel:nth-of-type(1) .finder__val")) == "eine Kanzlei")
    await pg.click("[data-fr=cta]")
    await pg.wait_for_timeout(1200)
    check("Finder füllt Buchung vor", await pg.evaluate("document.getElementById('bk-anliegen-system').checked && document.getElementById('bk-branche').value === 'Kanzlei & Beratung'"))

    # Buchung komplett
    await pg.click("[data-next]")
    await pg.fill("#bk-firma", "Testfirma GmbH")
    await pg.click("[data-next]")
    await pg.click("label[for=bk-format-video]")
    # zweiter freier Tag: Der erste hat spätabends wegen der Vorlaufzeit oft nur einen Termin
    await pg.click(".cal__day.is-avail >> nth=1")
    await pg.click(".slot >> nth=1")
    await pg.click("[data-next]")
    await pg.fill("#bk-name", "Max Mustermann")
    await pg.fill("#bk-email", "max@example.com")
    await pg.click("#bk-consent")
    await pg.click("[data-next]")
    await pg.wait_for_timeout(1500)
    check("Buchung abgeschlossen", await pg.is_visible(".done"), await pg.text_content(".done__when"))
    await pg.locator("#booking").screenshot(path=str(OUT / "flow-done.png"))

    # FAQ: nur eine Antwort offen
    await pg.evaluate("document.getElementById('faq').scrollIntoView()")
    await pg.click(".qa >> nth=2 >> summary")
    await pg.wait_for_timeout(300)
    opened = await pg.evaluate("Array.from(document.querySelectorAll('.qa')).map(function(d){return d.open})")
    check("FAQ: eine Antwort offen", opened.count(True) == 1 and opened[2], str(opened[:4]))

    # Film: Kapitel springt an die Stelle und spielt
    await pg.evaluate("document.getElementById('film').scrollIntoView()")
    await pg.wait_for_timeout(700)
    await pg.click(".film__ch >> nth=2")
    await pg.wait_for_timeout(3000)
    st = await pg.evaluate("(function(){var v=document.querySelector('.film__video');return [document.querySelector('[data-film]').classList.contains('is-started'), Math.round(v.currentTime), document.querySelector('.film__ch.is-on b').textContent, v.currentSrc.split('/').pop().split('?')[0], v.paused, parseFloat(document.querySelectorAll('.film__ch')[2].getAttribute('data-at'))]})()")
    check("Film: Kapitel springt an die Stelle", st[0] and st[5] <= st[1] <= st[5] + 5 and st[2] == "Der Unterschied" and not st[4], str(st))
    await pg.evaluate("document.querySelector('.film__video').pause()")

    # Referenz-Vorschau
    await pg.evaluate("document.getElementById('referenzen').scrollIntoView()")
    await pg.wait_for_timeout(600)
    await pg.click(".case__media[data-ref=ritz]")
    await pg.wait_for_timeout(1500)
    check("Vorschau öffnet", await pg.evaluate("document.getElementById('ref-dialog').open"))
    await pg.screenshot(path=str(OUT / "flow-dialog.png"))
    await pg.click("#ref-dialog [data-view=mobile]")
    await pg.wait_for_timeout(1200)
    check("Vorschau: Handy-Ansicht", await pg.evaluate("document.querySelector('.rd__frame').classList.contains('rd__frame--mobile')"))
    await pg.screenshot(path=str(OUT / "flow-dialog-m.png"))
    await pg.keyboard.press("Escape")
    await pg.wait_for_timeout(300)
    check("Vorschau schließt, Fokus zurück", await pg.evaluate("!document.getElementById('ref-dialog').open && document.activeElement && document.activeElement.getAttribute('data-ref') === 'ritz'"))

    cls = await pg.evaluate("window.__cls")
    shifts = await pg.evaluate("window.__shifts.slice(0,6)")
    check("Layout-Verschiebung (CLS) Desktop < 0.05", cls < 0.05, f"{cls:.4f} {shifts}")
    check("Keine Skriptfehler Desktop", not errs, str(errs[:5]))
    await ctx.close()


async def mobile(b):
    ctx = await b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2, is_mobile=True, has_touch=True, locale="de-DE")
    await ctx.add_init_script(CLS_JS)
    pg = await ctx.new_page()
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
    await pg.goto(BASE + "/_qa.html", wait_until="networkidle")
    await pg.wait_for_timeout(1200)
    await pg.click(".burger")
    await pg.wait_for_timeout(700)
    check("Handy-Menü öffnet", await pg.evaluate("document.getElementById('mnav').classList.contains('is-open') && !document.getElementById('mnav').hasAttribute('inert') && document.body.classList.contains('menu-open')"))
    await pg.click("[data-msub]")
    await pg.wait_for_timeout(500)
    check("Handy-Menü: Leistungen aufklappen", await pg.get_attribute("[data-msub]", "aria-expanded") == "true")
    for _ in range(14):
        await pg.keyboard.press("Tab")
    inside = await pg.evaluate("document.getElementById('mnav').contains(document.activeElement) || document.activeElement.classList.contains('burger')")
    check("Handy-Menü: Fokus bleibt im Menü", inside)
    await pg.keyboard.press("Escape")
    await pg.wait_for_timeout(500)
    check("Handy-Menü schließt mit Esc", await pg.evaluate("!document.getElementById('mnav').classList.contains('is-open') && document.getElementById('mnav').hasAttribute('inert')"))
    await pg.click(".burger")
    await pg.wait_for_timeout(600)
    await pg.click("#mnav a[href*='#faq']")
    await pg.wait_for_timeout(1200)
    check("Handy-Menü: Link schließt Menü", await pg.evaluate("!document.getElementById('mnav').classList.contains('is-open')"))

    check("Handy: Kundenreise untereinander", await pg.evaluate("!document.querySelector('[data-journey]').classList.contains('journey--pin') && document.querySelector('.jr__rail').hidden"))
    await pg.evaluate("document.getElementById('st-1').scrollIntoView()")
    await pg.wait_for_timeout(4200)
    hidden = await pg.evaluate("Array.from(document.querySelectorAll('#st-1 .pl__card')).filter(function(c){return !c.offsetWidth}).length")
    check("Handy: Pipeline zeigt alle Karten", hidden == 0, f"{hidden} versteckt")
    await pg.evaluate("document.getElementById('referenzen').scrollIntoView()")
    await pg.wait_for_timeout(500)
    await pg.tap(".case__media[data-ref=rechnungsradar]")
    await pg.wait_for_timeout(1300)
    await pg.evaluate("document.querySelector('.rd__in').scrollTop = 99999")
    await pg.wait_for_timeout(400)
    reach = await pg.evaluate("(function(){var a=document.querySelector('#ref-dialog [data-close-dialog]').getBoundingClientRect(),c=document.querySelector('.rd__close').getBoundingClientRect();return a.bottom<=innerHeight&&a.top>=0&&c.top>=0&&c.top<80})()")
    check("Handy: Vorschau bis zum Ende erreichbar, Schließen sichtbar", reach)
    await pg.tap(".rd__close")
    await pg.wait_for_timeout(400)
    await pg.evaluate("document.getElementById('vergleich').scrollIntoView()")
    await pg.click(".cmp-tabs [data-vs=baukasten]")
    check("Vergleich: Umschalter", await pg.get_attribute(".cmp", "data-vs") == "baukasten")

    h = await pg.evaluate("document.documentElement.scrollHeight")
    for y in range(0, h, 500):
        await pg.evaluate(f"window.scrollTo(0,{y})")
        await pg.wait_for_timeout(40)
    ow = await pg.evaluate("[document.documentElement.scrollWidth, document.documentElement.clientWidth]")
    check("Handy: kein seitliches Scrollen", ow[0] <= ow[1], str(ow))
    cls = await pg.evaluate("window.__cls")
    check("Layout-Verschiebung (CLS) Handy < 0.05", cls < 0.05, f"{cls:.4f} {await pg.evaluate('window.__shifts.slice(0,6)')}")
    check("Keine Skriptfehler Handy", not errs, str(errs[:5]))
    await ctx.close()


async def pages(b):
    ctx = await b.new_context(viewport={"width": 1280, "height": 800}, locale="de-DE")
    for path in ["/leistungen/website-erstellung/", "/leistungen/kundenmanagement-system/", "/leistungen/ki-agent/",
                 "/leistungen/online-marketing/", "/referenzen/", "/ueber-uns/", "/termin/", "/impressum/", "/datenschutz/", "/agb/", "/404.html"]:
        pg = await ctx.new_page()
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
        pg.on("requestfailed", lambda r: errs.append("failed " + r.url))
        file = path + ("index.html" if path.endswith("/") else "")
        await pg.goto(BASE + file, wait_until="networkidle")
        await pg.wait_for_timeout(400)
        ow = await pg.evaluate("[document.documentElement.scrollWidth, document.documentElement.clientWidth]")
        check(f"Seite {path}", not errs and ow[0] <= ow[1], f"{errs[:3]} {ow}")
        await pg.close()
    await ctx.close()


async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        await desktop(b)
        await mobile(b)
        await pages(b)
        await b.close()
    print("\n" + ("ALLES OK" if not fails else f"{len(fails)} FEHLER: {fails}"))


asyncio.run(main())
srv.shutdown()
