#!/usr/bin/env python3
"""Baut die Medialyte-Website als statische Seiten.

Aufruf:
  python3 build.py                 # Live-Version nach dist/
  python3 build.py --mode preview  # Vorschau-Version (relative Links, Demo-Formular) nach preview/
  python3 build.py --mode staging --cname neu.entwurf.medialyte.de  # Testversion für GitHub Pages nach staging/

Inhalte stehen in pages.py, Gestaltung in src/css/*.css, Verhalten in src/js/*.js.
Die Teil-Dateien werden beim Bauen zu assets/css/site.css und assets/js/site.js zusammengefügt.
"""
import hashlib
import json
import posixpath
import re
import shutil
import sys
from datetime import date
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"

SITE = {
    "url": "https://medialyte.de",
    "name": "Medialyte",
    "legal": "Medialyte – Marketing & Management",
    "owner": "Daniel Dogan",  # nur fürs Impressum (gesetzlich vorgeschrieben)
    "phone": "0170 9647532",
    "phone_intl": "+491709647532",
    "wa": "https://wa.me/491709647532",
    "email": "info@medialyte.de",
    "street": "Schaaphusen 3",
    "zip": "21147",
    "city": "Hamburg",
    "hours": "Mo–Do 9–18 Uhr, Fr 9–16 Uhr",
    "instagram": "https://www.instagram.com/medialyte.de/",
    "linkedin": "https://www.linkedin.com/company/medialyte/",
    "youtube": "https://www.youtube.com/@medialyte.deutschland",
    "today": date(2026, 10, 27).isoformat(),
}

# Verfügbarkeit fürs Buchungsformular (Wochentag 1 = Montag)
BOOKING = {
    "duration": 30, "step": 30, "daysAhead": 42, "leadHours": 18,
    "hours": {"1": ["09:00", "18:00"], "2": ["09:00", "18:00"], "3": ["09:00", "18:00"],
              "4": ["09:00", "18:00"], "5": ["09:00", "16:00"]},
    "closed": [],
}

# ---------------------------------------------------------------- Icons
_P = 'viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"'
ICONS = {
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "out": '<path d="M7 17L17 7M8.5 7H17v8.5"/>',
    "check": '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
    "x": '<path d="M6 6l12 12M18 6L6 18"/>',
    "minus": '<path d="M6 12h12"/>',
    "down": '<path d="M6 9l6 6 6-6"/>',
    "left": '<path d="M15 6l-6 6 6 6"/>',
    "right": '<path d="M9 6l6 6-6 6"/>',
    "phone": '<path d="M21.5 16.6v2.9a2 2 0 0 1-2.2 2 19.6 19.6 0 0 1-8.6-3.1 19.3 19.3 0 0 1-6-6A19.6 19.6 0 0 1 1.6 3.7 2 2 0 0 1 3.6 1.5h2.9a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.6a2 2 0 0 1-.5 2.1L7.5 9.1a16 16 0 0 0 6 6l1.2-1.2a2 2 0 0 1 2.1-.5c.8.3 1.7.6 2.6.7a2 2 0 0 1 1.7 2z"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2.5"/><path d="M3.5 7l8.5 6 8.5-6"/>',
    "pin": '<path d="M20 10c0 6.5-8 12-8 12s-8-5.5-8-12a8 8 0 1 1 16 0z"/><circle cx="12" cy="10" r="3"/>',
    "video": '<rect x="2.5" y="6" width="13" height="12" rx="2.5"/><path d="M15.5 10.5l6-3.5v10l-6-3.5"/>',
    "calendar": '<rect x="3" y="4.5" width="18" height="16" rx="3"/><path d="M3 9.5h18M8 2.5v4M16 2.5v4"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/>',
    "layout": '<rect x="3" y="4" width="18" height="16" rx="2.5"/><path d="M3 9h18M9 9v11"/>',
    "trend": '<path d="M3 17l6-6 4 4 8-8"/><path d="M15 7h6v6"/>',
    "db": '<ellipse cx="12" cy="5.5" rx="8" ry="3"/><path d="M4 5.5v6c0 1.7 3.6 3 8 3s8-1.3 8-3v-6M4 11.5v6c0 1.7 3.6 3 8 3s8-1.3 8-3v-6"/>',
    "bot": '<rect x="4" y="8" width="16" height="12" rx="3.5"/><path d="M12 4.5V8M9 13.5h.01M15 13.5h.01M9.5 17h5" stroke-width="2"/><circle cx="12" cy="3.5" r="1"/>',
    "mega": '<path d="M3 10.5v3a1 1 0 0 0 1 1h2.5l6 4.5v-14l-6 4.5H4a1 1 0 0 0-1 1z"/><path d="M16 8.5a5 5 0 0 1 0 7M18.8 5.8a9 9 0 0 1 0 12.4"/>',
    "users": '<path d="M16 20v-1.5a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4V20"/><circle cx="9" cy="7.5" r="3.5"/><path d="M22 20v-1.5a4 4 0 0 0-3-3.9M16 4.1a4 4 0 0 1 0 7.8"/>',
    "spark": '<path d="M12 3l1.9 5.1L19 10l-5.1 1.9L12 17l-1.9-5.1L5 10l5.1-1.9z"/>',
    "shield": '<path d="M12 21.5s8-3.8 8-10V5.2L12 2.5 4 5.2v6.3c0 6.2 8 10 8 10z"/><path d="M8.5 12l2.5 2.5 4.5-5"/>',
    "zap": '<path d="M13 2L4 14h7l-1 8 9-12h-7z"/>',
    "search": '<circle cx="11" cy="11" r="7"/><path d="M20.5 20.5L16 16"/>',
    "mobile": '<rect x="6.5" y="2" width="11" height="20" rx="2.8"/><path d="M11 18.5h2"/>',
    "monitor": '<rect x="2.5" y="3.5" width="19" height="13" rx="2.5"/><path d="M8 20.5h8M12 16.5v4"/>',
    "lock": '<rect x="4.5" y="10.5" width="15" height="10.5" rx="2.5"/><path d="M8 10.5V7.5a4 4 0 0 1 8 0v3"/>',
    "code": '<path d="M16 18l6-6-6-6M8 6l-6 6 6 6"/>',
    "pen": '<path d="M12 20h9"/><path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4z"/>',
    "pie": '<path d="M21.2 15.9A10 10 0 1 1 8 2.8"/><path d="M22 12A10 10 0 0 0 12 2v10z"/>',
    "rocket": '<path d="M4.5 16.5c-1.5 1.3-2 5-2 5s3.7-.5 5-2c.7-.8.7-2.1-.1-2.9a2.2 2.2 0 0 0-2.9-.1z"/><path d="M12 15l-3-3a22 22 0 0 1 2-3.9A12.9 12.9 0 0 1 22 2c0 2.7-.8 7.5-6 11a22.4 22.4 0 0 1-4 2z"/><path d="M9 12H4s.6-3 2-4c1.6-1.1 5 0 5 0M12 15v5s3-.6 4-2c1.1-1.6 0-5 0-5"/>',
    "food": '<path d="M3 2v7a2 2 0 0 0 2 2h4a2 2 0 0 0 2-2V2M7 2v20M21 15V2a5 5 0 0 0-5 5v6a2 2 0 0 0 2 2h3zm0 0v7"/>',
    "hammer": '<path d="M15 12l-8.5 8.5a2.1 2.1 0 0 1-3-3L12 9"/><path d="M17.6 15L22 10.6M20.9 11.7l-1.3-1.3a3.2 3.2 0 0 1-.9-2.2v-.9L16 4.6A5.6 5.6 0 0 0 12.1 3H9l.9.8A6.2 6.2 0 0 1 12 8.4V10l2 2h2.5l2.3 1.9"/>',
    "bag": '<path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"/><path d="M3 6h18M16 10a4 4 0 0 1-8 0"/>',
    "scale": '<path d="M12 3v18M7 21h10M3 7h2c2 0 5-1 7-2 2 1 5 2 7 2h2"/><path d="M16 16l3-8 3 8a4.6 4.6 0 0 1-6 0zM2 16l3-8 3 8a4.6 4.6 0 0 1-6 0z"/>',
    "health": '<path d="M19 14c1.5-1.5 3-3.2 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.8 0-3 .5-4.5 2-1.5-1.5-2.7-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4 3 5.5l7 7z"/>',
    "factory": '<path d="M2 20a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V8l-7 5V8l-7 5V4a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2z"/><path d="M7 18h1M12 18h1M17 18h1"/>',
    "brief": '<rect x="2.5" y="7" width="19" height="14" rx="2.5"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/>',
    "heart": '<path d="M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.7l-1-1.1a5.5 5.5 0 0 0-7.8 7.8l1 1.1L12 21l7.8-7.8 1-1.1a5.5 5.5 0 0 0 0-7.8z"/>',
    "refresh": '<path d="M21 12a9 9 0 1 1-2.6-6.4L21 8"/><path d="M21 3v5h-5"/>',
    "eye": '<path d="M1.5 12S5.5 4.5 12 4.5 22.5 12 22.5 12 18.5 19.5 12 19.5 1.5 12 1.5 12z"/><circle cx="12" cy="12" r="3"/>',
    "target": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.2"/>',
    "sliders": '<path d="M4 21v-7M4 10V3M12 21v-9M12 8V3M20 21v-5M20 12V3M1.5 14h5M9.5 8h5M17.5 16h5"/>',
    "inbox": '<path d="M22 12h-6l-2 3h-4l-2-3H2"/><path d="M5.5 5h13l3.5 7v6a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2v-6z"/>',
    "layers": '<path d="M12 2.5l9.5 5-9.5 5-9.5-5z"/><path d="M2.5 12.5l9.5 5 9.5-5M2.5 17l9.5 5 9.5-5"/>',
    "camera": '<path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/><circle cx="12" cy="13" r="4"/>',
    "play": '<path d="M7 4.5v15l12.5-7.5z" fill="currentColor" stroke="none"/>',
    "pause": '<path d="M8 5v14M16 5v14" stroke-width="2.4"/>',
    "replay": '<path d="M3 12a9 9 0 1 0 2.6-6.4L3 8"/><path d="M3 3v5h5"/>',
    "drag": '<path d="M9 7l-5 5 5 5M15 7l5 5-5 5"/>',
    "send": '<path d="M22 2L11 13"/><path d="M22 2l-7 20-4-9-9-4 20-7z"/>',
    "plus": '<path d="M12 5v14M5 12h14"/>',
    "quote": '<path d="M10 7H6a2 2 0 0 0-2 2v4a2 2 0 0 0 2 2h2v2a2 2 0 0 1-2 2M20 7h-4a2 2 0 0 0-2 2v4a2 2 0 0 0 2 2h2v2a2 2 0 0 1-2 2"/>',
    "star": '<path d="M12 2.5l2.9 6 6.6.9-4.8 4.6 1.2 6.5L12 17.3l-5.9 3.2 1.2-6.5L2.5 9.4l6.6-.9z"/>',
    "wa": '<path d="M20.5 11.6a8.4 8.4 0 0 1-12.3 7.5L3.5 20.5l1.4-4.4A8.4 8.4 0 1 1 20.5 11.6z"/><path d="M9 8.5c.3 2.6 2.2 5 5.4 6.4l1.2-1.4-1.9-1-.8.8c-1-.5-1.9-1.4-2.4-2.4l.8-.8-1-1.9z" fill="currentColor" stroke="none"/>',
}


def icon(name, cls=""):
    c = f' class="{cls}"' if cls else ""
    return f"<svg{c} {_P}>{ICONS[name]}</svg>"


def _logo_svg():
    raw = (ROOT / "tools/logo-inline.svg").read_text()
    raw = re.sub(r'\s(id|xmlns:xlink|preserveAspectRatio)="[^"]*"', "", raw)
    raw = raw.replace("<defs></defs>", "")
    raw = re.sub(r"\s+", " ", raw)
    return raw.replace("<svg ", '<svg class="mono" aria-hidden="true" focusable="false" ', 1)


LOGO = _logo_svg()                                   # Monogramm „ML“ (Handschrift)
WORDMARK = (ROOT / "tools/wordmark.svg").read_text()  # Wortmarke „MEDIALYTE“ als Pfad
BRAND = LOGO + WORDMARK


def e(s):
    return escape(str(s), quote=True)


# ---------------------------------------------------------------- Zusammenfügen von CSS und JS
VERSIONS = {}


def bundle(out):
    """CSS- und JS-Teile zu je einer Datei zusammenfügen, Kommentare kürzen, Prüfsumme merken."""
    css = "\n".join(p.read_text(encoding="utf-8") for p in sorted((SRC / "css").glob("[0-9]*.css")))
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    css = re.sub(r"\n\s*\n+", "\n", css).strip() + "\n"
    js_parts = []
    for p in sorted((SRC / "js").glob("[0-9]*.js")):
        js_parts.append(f"/* {p.name} */\n" + p.read_text(encoding="utf-8"))
    js = "\n".join(js_parts)
    (out / "assets/css").mkdir(parents=True, exist_ok=True)
    (out / "assets/js").mkdir(parents=True, exist_ok=True)
    (out / "assets/css/site.css").write_text(css, encoding="utf-8")
    (out / "assets/js/site.js").write_text(js, encoding="utf-8")
    VERSIONS["css/site.css"] = hashlib.md5(css.encode()).hexdigest()[:8]
    VERSIONS["js/site.js"] = hashlib.md5(js.encode()).hexdigest()[:8]


def _asset_version(asset):
    v = VERSIONS.get(asset)
    return f"?v={v}" if v else ""


# ---------------------------------------------------------------- Kontext: Links je nach Modus
class Ctx:
    def __init__(self, mode, path):
        self.mode = mode
        self.path = path  # z. B. "/" oder "/leistungen/website-erstellung/"

    @property
    def _dir(self):
        p = self.path.lstrip("/")
        if not p.endswith("/"):
            p = posixpath.dirname(p)
        return p or "."

    def u(self, target):
        """Interner Link. target immer root-relativ, z. B. '/referenzen/' oder '/#beratung'."""
        if target.startswith(("http:", "https:", "mailto:", "tel:")):
            return target
        path, frag, query = target, "", ""
        if "#" in path:
            path, frag = path.split("#", 1)
            frag = "#" + frag
        if "?" in path:
            path, query = path.split("?", 1)
            query = "?" + query
        if path in ("", self.path) and not query:
            return frag or "#top"  # gleiche Seite: nach oben
        if self.mode == "prod":
            return path + query + frag
        file = path.lstrip("/") + "index.html"
        return posixpath.relpath(file, self._dir) + query + frag

    def a(self, asset):
        ver = _asset_version(asset)
        if self.mode == "prod":
            return "/assets/" + asset + ver
        return posixpath.relpath("assets/" + asset, self._dir) + ver

    def abs(self, path):
        return SITE["url"] + path


# ---------------------------------------------------------------- Layout-Bausteine
SERVICES = [
    ("/leistungen/website-erstellung/", "Website-Erstellung", "Neue Website oder Relaunch, gemacht für Ihre Kunden", "globe"),
    ("/leistungen/kundenmanagement-system/", "Kundenmanagement-System", "Ihr eigenes Dashboard für Anfragen, Kunden und Aufträge", "db"),
    ("/leistungen/ki-agent/", "KI-Agent", "Website ändern per WhatsApp oder im Dashboard", "bot"),
    ("/leistungen/online-marketing/", "Online-Marketing", "Google Ads, Social Media und SEO, die Anfragen bringen", "mega"),
]


def book_href(ctx):
    return ctx.u("/#termin") if ctx.path == "/" else ctx.u("/termin/")


def header(ctx, active=""):
    cta = book_href(ctx)

    def cur(key):
        return ' aria-current="page"' if key == active else ""

    drop = "".join(
        f'<a class="drop__link" href="{ctx.u(p)}"{cur("svc:" + p)}><span class="ic">{icon(i)}</span><b>{e(t)}</b><small>{e(d)}</small></a>'
        for p, t, d, i in SERVICES)
    msub = "".join(
        f'<a href="{ctx.u(p)}"><span class="ic ic--sm">{icon(i)}</span><b>{e(t)}</b><small>{e(d)}</small></a>'
        for p, t, d, i in SERVICES)
    return f"""
<a class="skip" href="#main">Zum Inhalt springen</a>
<header class="header" data-header>
  <div class="wrap header__in">
    <a class="brand" href="{ctx.u('/')}" aria-label="Medialyte – zur Startseite">{BRAND}</a>
    <nav class="nav" aria-label="Hauptnavigation">
      <div class="nav__item" data-drop>
        <button class="nav__link" type="button" aria-expanded="false" aria-controls="drop-leistungen"{cur('leistungen')}>Leistungen {icon('down')}</button>
        <div class="drop" id="drop-leistungen">
          {drop}
          <div class="drop__foot"><span>Nicht sicher, was Sie brauchen?</span><a class="link" href="{ctx.u('/#pakete')}">Paket finden {icon('arrow')}</a></div>
        </div>
      </div>
      <a class="nav__link" href="{ctx.u('/referenzen/')}"{cur('referenzen')}>Referenzen</a>
      <a class="nav__link" href="{ctx.u('/#ablauf')}">Ablauf</a>
      <a class="nav__link" href="{ctx.u('/ueber-uns/')}"{cur('ueber-uns')}>Über uns</a>
      <a class="nav__link" href="{ctx.u('/#faq')}">FAQ</a>
    </nav>
    <div class="header__actions">
      <a class="icon-btn header__wa" href="{SITE['wa']}" target="_blank" rel="noopener" aria-label="Per WhatsApp schreiben">{icon('wa')}</a>
      <a class="btn btn--light btn--sm header__cta" href="{cta}">Erstgespräch buchen</a>
      <button class="burger" type="button" aria-expanded="false" aria-controls="mnav" aria-label="Menü öffnen"><span></span><span></span></button>
    </div>
  </div>
</header>
<div class="mnav" id="mnav" role="dialog" aria-modal="true" aria-label="Menü" inert>
  <nav class="mnav__nav" aria-label="Menü">
    <a class="mnav__link" href="{ctx.u('/')}" data-m style="--d:0"{' aria-current="page"' if ctx.path == '/' else ''}>Start</a>
    <div data-m style="--d:1">
      <button class="mnav__link" type="button" aria-expanded="false" aria-controls="mnav-sub" data-msub>Leistungen<span class="pm" aria-hidden="true"></span></button>
      <div class="mnav__sub" id="mnav-sub"><div>{msub}</div></div>
    </div>
    <a class="mnav__link" href="{ctx.u('/referenzen/')}" data-m style="--d:2"{cur('referenzen')}>Referenzen</a>
    <a class="mnav__link" href="{ctx.u('/#ablauf')}" data-m style="--d:3">Ablauf</a>
    <a class="mnav__link" href="{ctx.u('/ueber-uns/')}" data-m style="--d:4"{cur('ueber-uns')}>Über uns</a>
    <a class="mnav__link" href="{ctx.u('/#faq')}" data-m style="--d:5">FAQ</a>
  </nav>
  <div class="mnav__foot" data-m style="--d:6">
    <a class="btn btn--primary btn--lg btn--block" href="{cta}">Erstgespräch buchen</a>
    <a class="btn btn--ghost btn--lg btn--block" href="{SITE['wa']}" target="_blank" rel="noopener">{icon('wa')} Per WhatsApp schreiben</a>
    <div class="mnav__meta"><a href="tel:{SITE['phone_intl']}">{e(SITE['phone'])}</a><a href="mailto:{SITE['email']}">{e(SITE['email'])}</a><span>{e(SITE['hours'])}</span></div>
  </div>
</div>"""


def footer(ctx):
    svc = "".join(f'<li><a href="{ctx.u(p)}">{e(t)}</a></li>' for p, t, *_ in SERVICES)
    return f"""
<footer class="footer">
  <div class="wrap">
    <div class="footer__grid">
      <div class="footer__brand">
        <a class="brand brand--lg" href="{ctx.u('/')}" aria-label="Medialyte – zur Startseite">{BRAND}</a>
        <p>Individuelle Lösungen zur Vermehrung, Verbesserung und Verwaltung von Kundenbeziehungen. Aus Hamburg, für Betriebe in ganz Deutschland.</p>
        <div class="footer__social">
          <a href="{SITE['instagram']}" target="_blank" rel="noopener">Instagram {icon('out')}</a>
          <a href="{SITE['linkedin']}" target="_blank" rel="noopener">LinkedIn {icon('out')}</a>
          <a href="{SITE['youtube']}" target="_blank" rel="noopener">YouTube {icon('out')}</a>
        </div>
        <div class="footer__partner"><img src="{ctx.a('img/logos/ionos-agency-partner.webp')}" width="185" height="100" alt="IONOS Agency Partner Official" loading="lazy" decoding="async"></div>
      </div>
      <div>
        <h4>Leistungen</h4>
        <ul>{svc}</ul>
      </div>
      <div>
        <h4>Medialyte</h4>
        <ul>
          <li><a href="{ctx.u('/referenzen/')}">Referenzen</a></li>
          <li><a href="{ctx.u('/ueber-uns/')}">Über uns</a></li>
          <li><a href="{ctx.u('/#ablauf')}">Ablauf</a></li>
          <li><a href="{ctx.u('/#faq')}">Häufige Fragen</a></li>
          <li><a href="{ctx.u('/termin/')}">Erstgespräch buchen</a></li>
        </ul>
      </div>
      <div>
        <h4>Kontakt</h4>
        <ul class="footer__contact">
          <li>{icon('pin')}<span>{e(SITE['street'])}<br>{e(SITE['zip'])} {e(SITE['city'])}</span></li>
          <li>{icon('phone')}<a href="tel:{SITE['phone_intl']}">{e(SITE['phone'])}</a></li>
          <li>{icon('wa')}<a href="{SITE['wa']}" target="_blank" rel="noopener">WhatsApp</a></li>
          <li>{icon('mail')}<a href="mailto:{SITE['email']}">{e(SITE['email'])}</a></li>
          <li>{icon('clock')}<span>{e(SITE['hours'])}</span></li>
        </ul>
      </div>
    </div>
    <div class="footer__bottom">
      <span>© 2026 Medialyte – Marketing &amp; Management</span>
      <nav aria-label="Rechtliches">
        <a href="{ctx.u('/impressum/')}">Impressum</a>
        <a href="{ctx.u('/datenschutz/')}">Datenschutz</a>
        <a href="{ctx.u('/agb/')}">AGB</a>
      </nav>
    </div>
  </div>
</footer>
<a class="fab" href="{SITE['wa']}" target="_blank" rel="noopener" aria-label="Per WhatsApp schreiben">{icon('wa')}<span class="fab__tip" aria-hidden="true">Per WhatsApp schreiben</span></a>"""


def org_schema():
    return {
        "@context": "https://schema.org",
        "@type": "ProfessionalService",
        "@id": SITE["url"] + "/#org",
        "name": "Medialyte",
        "alternateName": SITE["legal"],
        "url": SITE["url"] + "/",
        "logo": SITE["url"] + "/assets/img/logo-ml.svg",
        "image": SITE["url"] + "/assets/img/og.jpg",
        "description": "Digitalagentur für individuelle Lösungen zur Vermehrung, Verbesserung und Verwaltung von Kundenbeziehungen: Websites, Kundenmanagement-Systeme, KI-Agent und Online-Marketing für Betriebe in ganz Deutschland.",
        "telephone": SITE["phone_intl"],
        "email": SITE["email"],
        "address": {"@type": "PostalAddress", "streetAddress": SITE["street"], "postalCode": SITE["zip"],
                    "addressLocality": SITE["city"], "addressCountry": "DE"},
        "openingHoursSpecification": [
            {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday"], "opens": "09:00", "closes": "18:00"},
            {"@type": "OpeningHoursSpecification", "dayOfWeek": "Friday", "opens": "09:00", "closes": "16:00"},
        ],
        "areaServed": {"@type": "Country", "name": "Deutschland"},
        "sameAs": [SITE["instagram"], SITE["linkedin"], SITE["youtube"]],
        "knowsAbout": ["Webdesign", "Website-Erstellung", "CRM-Entwicklung", "Dashboards", "KI-Agenten", "Google Ads", "Suchmaschinenoptimierung", "Social Media Marketing"],
    }


def breadcrumb_schema(items):
    return {
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": SITE["url"] + p}
                            for i, (n, p) in enumerate(items)],
    }


def faq_schema(qas):
    def strip(h):
        return re.sub(r"<[^>]+>", "", h).strip()
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q,
                            "acceptedAnswer": {"@type": "Answer", "text": strip(a)}} for q, a in qas]}


def document(ctx, page, body):
    title = page["title"]
    if ctx.mode == "preview" and page["path"] == "/":
        title = "Medialyte"  # Name der Vorschau in der Artifact-Galerie
    desc = page["desc"]
    canonical = ctx.abs(page["path"])
    og_img = SITE["url"] + "/assets/img/og.jpg"
    schemas = page.get("schema", [])
    ld = "".join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>' for s in schemas)
    cfg = {"whatsapp": SITE["wa"], "booking": BOOKING}
    robots = page.get("robots", "index, follow, max-image-preview:large")
    if ctx.mode == "staging":
        robots = "noindex, nofollow"  # Testversion nicht bei Google
    head = f"""<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:locale" content="de_DE">
<meta property="og:site_name" content="Medialyte">
<meta property="og:title" content="{e(page.get('og_title', title))}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{og_img}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0E192A">
<meta name="color-scheme" content="dark">
<link rel="icon" href="{ctx.a('img/favicon.svg')}" type="image/svg+xml">
<link rel="icon" href="{ctx.a('img/favicon-32.png')}" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="{ctx.a('img/apple-touch-icon.png')}">
<link rel="preload" href="{ctx.a('fonts/outfit-latin-wght-normal.woff2')}" as="font" type="font/woff2" crossorigin>
<script>document.documentElement.classList.add("js")</script>
<link rel="stylesheet" href="{ctx.a('css/site.css')}">
<script>window.ML_CONFIG={json.dumps(cfg)};</script>
<script src="{ctx.a('js/site.js')}" defer></script>
{page.get('head_extra', '')}{ld}"""
    if ctx.mode == "preview" and page["path"] == "/":
        # Vorschau-Hauptseite: Das Artifact-Gerüst liefert doctype, head und body selbst.
        first, rest = head.split("\n", 1)
        return f'{first}\n<meta name="claude:viewport-fit-sides" content="cover">\n{rest}\n{body}\n'
    return f"""<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
{head}
</head>
<body>
{body}
</body>
</html>
"""


# ---------------------------------------------------------------- Ausgabe
def build(mode="prod", out=None, cname=None):
    import pages  # noqa: E402  (Inhalte)
    out = Path(out or (ROOT / {"prod": "dist", "preview": "preview", "staging": "staging"}[mode]))
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    shutil.copytree(SRC / "assets", out / "assets", ignore=shutil.ignore_patterns("*.json", "css", "js"))
    bundle(out)
    built = []
    for page in pages.PAGES:
        ctx = Ctx(mode, page["path"])
        body = (header(ctx, page.get("active", "")) + "\n<main id=\"main\">" + page["render"](ctx) + "</main>\n"
                + footer(ctx) + page.get("after", lambda c: "")(ctx))
        html = document(ctx, page, body)
        target = out / (page["path"].lstrip("/") + "index.html") if page["path"].endswith("/") else out / page["path"].lstrip("/")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(html, encoding="utf-8")
        built.append(page)
    if mode == "prod":
        urls = "".join(
            f"<url><loc>{SITE['url']}{p['path']}</loc><lastmod>{SITE['today']}</lastmod><priority>{p.get('priority', '0.6')}</priority></url>"
            for p in built if p.get("sitemap", True))
        (out / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n', encoding="utf-8")
        (out / "robots.txt").write_text(f"User-agent: *\nAllow: /\nDisallow: /api/\n\nSitemap: {SITE['url']}/sitemap.xml\n", encoding="utf-8")
        shutil.copy(ROOT / "deploy/.htaccess", out / ".htaccess")
        if (ROOT / "api").exists():
            shutil.copytree(ROOT / "api", out / "api", ignore=shutil.ignore_patterns("config.php", "data"))
    if mode == "staging":
        # Testversion für GitHub Pages: nicht indexieren, Ordner unverändert ausliefern
        (out / "robots.txt").write_text("User-agent: *\nDisallow: /\n", encoding="utf-8")
        (out / ".nojekyll").write_text("", encoding="utf-8")
        if cname:
            (out / "CNAME").write_text(cname + "\n", encoding="utf-8")
    print(f"{len(built)} Seiten gebaut ({mode}) → {out}")
    return out


if __name__ == "__main__":
    mode = "prod"
    if "--mode" in sys.argv:
        mode = sys.argv[sys.argv.index("--mode") + 1]
    outdir = None
    if "--out" in sys.argv:
        outdir = sys.argv[sys.argv.index("--out") + 1]
    cname = sys.argv[sys.argv.index("--cname") + 1] if "--cname" in sys.argv else None
    sys.path.insert(0, str(ROOT))
    build(mode, outdir, cname)
