"""Inhalte aller Seiten von medialyte.de.

Jede Seite ist ein Eintrag in PAGES mit Pfad, Titel, Beschreibung und einer render-Funktion.
Texte hier ändern, dann `python3 build.py` ausführen.
"""
import json
from pathlib import Path

from build import (LOGO, SITE, breadcrumb_schema, e, faq_schema, icon, org_schema)

ROOT = Path(__file__).resolve().parent
_REFS_META = json.loads((ROOT / "src/assets/img/refs/refs.json").read_text())


# ======================================================================= Daten
LOGOS = [
    ("rubin", "Juwelier Rubin"), ("fassadentrio", "FassadenTrio"), ("ritz", "RITZ Instrument Transformers"),
    ("rechnungsradar", "Rechnungsradar"), ("cv", "CV"), ("hubo-dmoran", "Hubo d'Moran"),
    ("deluxe-design", "Deluxe Design"), ("amore-eventdeko", "Amore Eventdeko"),
    ("ionos-agency-partner", "IONOS Agency Partner Official"), ("garee-beauty", "garée beauty"),
    ("glory-angels", "Glory Angels"), ("sabaai-thai", "Sabaai Thai Massage & Wellness"), ("gado-energie", "GADO Energie"),
]
_LOGO_DIMS = {d["file"].replace(".webp", ""): (d["w"], d["h"]) for d in json.loads((ROOT / "src/assets/img/logos/logos.json").read_text())}

REFS = {
    "rechnungsradar": {
        "title": "RechnungsRadar",
        "category": "App-Entwicklung · Rechnungsmanagement",
        "pill": "Digitales Produkt",
        "card": "Rechnungsmanagement-System, das Belege automatisch aus dem E-Mail-Postfach in die Buchhaltung bringt.",
        "summary": "RechnungsRadar findet Rechnungen im E-Mail-Postfach und überträgt sie automatisch in die Buchhaltung, etwa nach Lexware Office, BuchhaltungsButler oder DATEV. Medialyte hat die App-Entwicklung und den Webauftritt umgesetzt, der Unternehmen und Steuerberater überzeugt.",
        "facts": [["Kunde", "RechnungsRadar"], ["Branche", "Software für Buchhaltung"], ["Leistungen", "App-Entwicklung, Rechnungsmanagement-System, Website, Conversion-Optimierung"], ["Ergebnis", "Deutlich mehr Anfragen von Steuerberatern"]],
        "nums": [["+230 %", "Kundenanfragen"], ["+73 %", "Conversionrate"]],
        "url": "https://rechnungs-radar.de/", "urlLabel": "rechnungs-radar.de besuchen", "host": "rechnungs-radar.de",
    },
    "rubin": {
        "title": "Juwelier Rubin",
        "category": "Juwelierkette · 4 Filialen",
        "pill": "Juwelierkette",
        "card": "Website für eine Juwelierkette mit Filialen in Hamburg, Norderstedt und Lüneburg.",
        "summary": "Juwelier Rubin ist eine Juwelierkette mit vier Filialen in Hamburg, Norderstedt und Lüneburg. Die Website präsentiert Trauringe, Verlobungsringe, Brillantschmuck und Uhren, führt Kunden zur passenden Filiale und bündelt Services wie den Goldankauf.",
        "facts": [["Kunde", "Juwelier Rubin"], ["Branche", "Schmuck und Uhren"], ["Leistungen", "Webdesign, Entwicklung, Produktwelten, Filialfinder"], ["Standorte", "Hamburg, Norderstedt, Lüneburg"]],
        "nums": [["4", "Filialen"], ["3", "Städte"]],
        "url": "https://rubin-gold.de/", "urlLabel": "rubin-gold.de besuchen", "host": "rubin-gold.de",
    },
    "ritz": {
        "title": "RITZ Instrument Transformers",
        "category": "Großkonzern · Website-Entwurf",
        "pill": "Großkonzern",
        "card": "Neue Plattform, die Unternehmensseite und Produktfinder eines Industriekonzerns zusammenführt.",
        "summary": "RITZ entwickelt und fertigt seit 1945 Strom- und Spannungswandler, Sensoren und Stromschienen. Für den Relaunch hat Medialyte einen Entwurf gestaltet, der die Unternehmensseite und den Produktfinder auf einer modernen Plattform zusammenführt.",
        "facts": [["Kunde", "RITZ Instrument Transformers"], ["Branche", "Industrie und Energietechnik"], ["Leistungen", "Konzept, Design, Entwicklung, Produktfinder"], ["Status", "Entwurf"]],
        "nums": [["1945", "gegründet in Hamburg"], ["1.500+", "Mitarbeitende"], ["7", "Werke in 5 Ländern"], ["60", "Länder mit Vertretung"]],
        "url": "https://ritz.entwurf.medialyte.de/", "urlLabel": "Entwurf ansehen", "host": "ritz.entwurf.medialyte.de",
    },
}

TEAM = [
    ("Daniel", "D", "Gründer & Inhaber", "Ihr Ansprechpartner vom ersten Gespräch bis zum Livegang. Daniel versteht Ihr Geschäft, plant das Projekt und sorgt dafür, dass am Ende alles zusammenpasst."),
    ("Hannes", "H", "Entwicklung", "Hannes setzt Websites, Apps und Systeme technisch um: schnell, sauber und so gebaut, dass sie mit Ihrem Unternehmen wachsen."),
    ("Maximilian", "M", "Design", "Maximilian gestaltet Oberflächen, die Ihre Marke tragen und Ihre Kunden ohne Umwege zum Ziel führen."),
    ("Aurelia", "A", "Marketing", "Aurelia plant und betreut Kampagnen und Inhalte, damit die richtigen Menschen auf Ihr Unternehmen aufmerksam werden."),
    ("Finn", "F", "Buchhaltung & Management", "Finn hält im Hintergrund alles zusammen. Angebote, Abrechnung und Organisation laufen bei ihm klar und verlässlich."),
]

FAQ_MAIN = [
    ("Was kostet eine Website bei Medialyte?",
     "<p>Jedes Projekt ist individuell. Ihr Angebot besteht immer aus zwei Teilen: einer einmaligen Pauschale für Konzeption, Design und Entwicklung und einem monatlichen Abo für Hosting, Pflege, KI-Agent und Support.</p><p>Nach dem kostenfreien Erstgespräch erhalten Sie innerhalb von 48 Stunden ein transparentes Angebot ohne versteckte Kosten.</p>"),
    ("Wie lange dauert ein typisches Projekt?",
     "<p>Das hängt vom Umfang ab. Eine einfache Website ist in 2–4 Wochen fertig, komplexere Projekte mit Kundenmanagement-System dauern 6–12 Wochen. Wir halten Sie über jeden Meilenstein informiert.</p>"),
    ("Wie kann ich später Änderungen vornehmen?",
     "<p>Bei einfacheren Websites, zum Beispiel in der Gastronomie, schreiben Sie dem KI-Agenten einfach per WhatsApp, was sich ändern soll. Bei umfangreichen Systemen, etwa der Kundenverwaltung einer Kanzlei, erledigen Sie Änderungen direkt in Ihrem eigenen Dashboard.</p>"),
    ("Was ist der KI-Agent?",
     "<p>Der KI-Agent ist Ihr digitaler Helfer für Website und System. Er nimmt Änderungswünsche entgegen, pflegt Inhalte wie Öffnungszeiten, Preise oder Bilder und hält Ihre Seite aktuell. Für alles, was Planung und Gestaltung braucht, ist unser Team persönlich für Sie da.</p>"),
    ("Bieten Sie auch laufende Betreuung an?",
     "<p>Ja. Nach dem Launch betreuen wir Sie kontinuierlich, inklusive Monitoring, Wartung, Inhalts-Updates und technischem Support. So bleibt Ihre Lösung langfristig erfolgreich.</p>"),
    ("Für welche Branchen arbeiten Sie?",
     "<p>Für Betriebe aller Branchen in ganz Deutschland: von Gastronomie, Handwerk und Einzelhandel über Kanzleien, Praxen und Dienstleister bis zu Industrieunternehmen und gemeinnützigen Organisationen.</p>"),
    ("Arbeiten Sie nur in Hamburg?",
     "<p>Unser Sitz ist in Hamburg, wir arbeiten aber für Unternehmen in ganz Deutschland. Die Zusammenarbeit läuft per Video-Call, Telefon und WhatsApp, in Hamburg gern auch persönlich.</p>"),
    ("Ich habe schon eine Website. Lohnt sich ein Neustart?",
     "<p>Oft ja, vor allem wenn die Seite langsam ist, auf dem Handy schlecht aussieht oder kaum Anfragen bringt. Im Erstgespräch prüfen wir kostenfrei, ob sich eine Verbesserung oder ein kompletter Neustart mehr lohnt.</p>"),
    ("Kann ich meine Website selbst bearbeiten?",
     "<p>Ja. Inhalte wie Texte, Bilder oder Speisekarten können Sie jederzeit selbst ändern, ganz ohne technische Vorkenntnisse. Wenn Sie lieber nichts anfassen möchten, übernimmt das der KI-Agent für Sie.</p>"),
    ("Was ist die Zufriedenheitsgarantie?",
     "<p>Unsere Zufriedenheitsgarantie bedeutet, dass wir so lange an Ihrem Projekt arbeiten, bis Sie zu 100 % zufrieden sind.</p>"),
]

INDUSTRIES = [
    ("food", "Gastronomie & Hotellerie", "Speisekarte, Öffnungszeiten und Events halten Sie per WhatsApp aktuell.", "Website + KI-Agent"),
    ("hammer", "Handwerk & Bau", "Anfragen mit allen Details sammeln und Aufträge im Dashboard planen.", "Website + System"),
    ("bag", "Einzelhandel & E-Commerce", "Sortiment, Filialen und Online-Shop überzeugend präsentiert.", "z. B. Juwelier Rubin"),
    ("scale", "Kanzleien & Beratung", "Mandanten, Termine und Anfragen im eigenen System verwalten.", "Website + System"),
    ("health", "Praxen & Gesundheit", "Leistungen verständlich erklären und Terminanfragen einfach machen.", "Website + KI-Agent"),
    ("factory", "Industrie & Technik", "Produktfinder für tausende Artikel und Websites für internationale Märkte.", "z. B. RITZ"),
    ("brief", "Dienstleister", "Landingpages, Angebotsrechner und Kampagnen, die Anfragen bringen.", "z. B. FassadenTrio"),
    ("heart", "Vereine & Organisationen", "Projekte, Spenden und Termine klar und vertrauenswürdig zeigen.", "z. B. Hubo d'Moran"),
]


# ======================================================================= Bausteine
def checks(items, cls=""):
    c = f" {cls}" if cls else ""
    return f'<ul class="checks{c}">' + "".join(f"<li>{icon('check')}<span>{i}</span></li>" for i in items) + "</ul>"


def head(pill, h2, lead="", center=False, green=False, h1=False):
    tag = "h1" if h1 else "h2"
    cls = "h1" if h1 else "h2"
    p = f'<span class="pill{" pill--green" if green else ""}">{pill}</span>' if pill else ""
    ld = f'<p class="lead">{lead}</p>' if lead else ""
    return f'<div class="head{" head--center" if center else ""}">{p}<{tag} class="{cls}">{h2}</{tag}>{ld}</div>'


def img(ctx, src, w, h, alt, cls="", lazy=True, sizes="", srcset=""):
    extra = ""
    if srcset:
        extra += f' srcset="{srcset}" sizes="{sizes}"'
    if lazy:
        extra += ' loading="lazy" decoding="async"'
    else:
        extra += ' fetchpriority="high" decoding="async"'
    c = f' class="{cls}"' if cls else ""
    return f'<img{c} src="{ctx.a(src)}" width="{w}" height="{h}" alt="{e(alt)}"{extra}>'


def book_link(ctx, ask=""):
    """Link zur Terminbuchung: auf der Startseite zum Abschnitt, sonst zur Terminseite."""
    if ctx.path == "/":
        return ctx.u("/#beratung")
    return ctx.u("/termin/" + (f"?anliegen={ask}" if ask else ""))


def btn_book(ctx, text="Kostenfreie Beratung", ask="", cls="btn--primary"):
    data = f' data-ask="{ask}"' if ask and ctx.path == "/" else ""
    return f'<a class="btn {cls}" href="{book_link(ctx, ask)}"{data}>{text} {icon("send")}</a>'


def btn_wa(ctx, text="Per WhatsApp schreiben"):
    return f'<a class="btn btn--ghost" href="{SITE["wa"]}" target="_blank" rel="noopener">{icon("chat")} {text}</a>'


def _logo_h(f):
    """Optischer Ausgleich: breite Schriftzüge kleiner, kompakte Zeichen größer."""
    w, h = _LOGO_DIMS[f]
    return max(22, min(54, round(44 * (3.0 / (w / h)) ** 0.5)))


def logo_marquee(ctx):
    def one_set(hidden=False):
        imgs = "".join(
            f'<img src="{ctx.a("img/logos/" + f + ".webp")}" width="{_LOGO_DIMS[f][0]}" height="{_LOGO_DIMS[f][1]}" style="--h:{_logo_h(f)}px" alt="{"" if hidden else e(a)}" loading="lazy" decoding="async">'
            for f, a in LOGOS)
        aria = ' aria-hidden="true"' if hidden else ""
        return f'<div class="marquee__set"{aria}>{imgs}</div>'
    return f"""
<section class="logos" aria-label="Kunden und Partner">
  <p class="logos__label">Kunden &amp; Partner, die uns vertrauen</p>
  <div class="marquee"><div class="marquee__track">{one_set()}{one_set(True)}</div></div>
</section>"""


def stats_band():
    return """
<div class="stats">
  <div class="stat"><span class="stat__v"><span data-count="200">200</span><span>+</span></span><span class="stat__l">Erfolgreiche Kampagnen</span></div>
  <div class="stat"><span class="stat__v"><span data-count="48">48</span> h</span><span class="stat__l">Bis zu Ihrem individuellen Angebot</span></div>
  <div class="stat"><span class="stat__v">2–4</span><span class="stat__l">Wochen bis zur neuen Website</span></div>
  <div class="stat"><span class="stat__v"><span data-count="100">100</span><span>%</span></span><span class="stat__l">Zufriedenheitsgarantie</span></div>
</div>"""


def ref_cards(ctx, keys=("rechnungsradar", "rubin", "ritz")):
    out = []
    for k in keys:
        r = REFS[k]
        srcset = f'{ctx.a("img/refs/" + k + "-desktop-sm.webp")} 640w, {ctx.a("img/refs/" + k + "-desktop.webp")} 1200w'
        shot = img(ctx, f"img/refs/{k}-desktop.webp", 1200, 750, f"Website {r['title']}", srcset=srcset,
                   sizes="(max-width: 980px) 92vw, 400px")
        out.append(f"""
<button class="ref" type="button" data-ref="{k}" aria-haspopup="dialog">
  <span class="ref__shot"><span class="chrome"><i></i><i></i><i></i><span>{e(r['host'])}</span></span>{shot}
    <span class="pill">{e(r['pill'])}</span>
    <span class="ref__open">{icon('eye')} Live-Vorschau</span>
  </span>
  <span class="ref__body"><h3>{e(r['title'])}</h3><p>{e(r['card'])}</p><span class="link link--accent">Vorschau ansehen {icon('arrow')}</span></span>
</button>""")
    return '<div class="refs">' + "".join(out) + "</div>"


def ref_dialog(ctx):
    data = {}
    for k, r in REFS.items():
        data[k] = {
            "title": r["title"], "category": r["category"], "summary": r["summary"], "facts": r["facts"],
            "nums": r["nums"], "url": r["url"], "urlLabel": r["urlLabel"], "host": r["host"],
            "desktop": ctx.a(f"img/refs/{k}-desktop-full.webp"), "mobile": ctx.a(f"img/refs/{k}-mobile-full.webp"),
            "desktopH": _REFS_META[k]["desktop_full_h"], "mobileH": _REFS_META[k]["mobile_full_h"],
        }
    return f"""
<dialog class="rd" id="ref-dialog" aria-labelledby="rd-title">
  <div class="rd__in">
    <button class="rd__close" type="button" aria-label="Vorschau schließen">{icon('x')}</button>
    <div class="rd__stage">
      <div class="rd__bar">
        <div class="seg" role="group" aria-label="Ansicht wählen">
          <button type="button" data-view="desktop" aria-pressed="true">{icon('monitor')} Desktop</button>
          <button type="button" data-view="mobile" aria-pressed="false">{icon('mobile')} Smartphone</button>
        </div>
        <span class="rd__hint">Scrollen Sie durch die Seite</span>
      </div>
      <div class="rd__view">
        <div class="rd__frame">
          <div class="chrome"><i></i><i></i><i></i><span></span></div>
          <div class="rd__scroll" tabindex="0"><img src="" alt="" width="1000" height="1000" decoding="async"></div>
        </div>
      </div>
    </div>
    <div class="rd__info">
      <span class="pill rd__cat"></span>
      <h2 class="rd__title" id="rd-title"></h2>
      <p class="rd__text"></p>
      <div class="rd__actions">
        <a class="btn btn--primary rd__link" href="#" target="_blank" rel="noopener"><span></span> {icon('out')}</a>
        <a class="btn btn--ghost" href="{book_link(ctx)}" data-close-dialog>Ähnliches Projekt anfragen</a>
      </div>
      <dl class="rd__facts"></dl>
      <div class="rd__nums"></div>
    </div>
  </div>
</dialog>
<script type="application/json" id="refs-data">{json.dumps(data, ensure_ascii=False)}</script>"""


def before_after(ctx):
    return f"""
<div class="results">
  <figure class="quote">
    <span class="quote__mark" aria-hidden="true">&ldquo;</span>
    <div style="display:grid;gap:18px">
      <div class="stars" aria-label="5 von 5 Sternen">{icon('star')}{icon('star')}{icon('star')}{icon('star')}{icon('star')}</div>
      <blockquote>
        <p>Dank Medialyte hat meine Website für RechnungsRadar einen echten Qualitätssprung gemacht. Aus einer eher schlichten Seite ist ein professioneller Auftritt geworden, der Vertrauen schafft.</p>
        <p>Seitdem erreichen mich deutlich mehr Anfragen von Steuerberatern. Die Zusammenarbeit war reibungslos, schnell und absolut zuverlässig – sehr empfehlenswert!</p>
      </blockquote>
    </div>
    <figcaption>{img(ctx, 'img/logos/avatar-rechnungsradar.webp', 112, 112, 'Logo RechnungsRadar')}<span><b>Hannes Diedrichsen</b><small>Gründer von RechnungsRadar</small></span></figcaption>
  </figure>
  {_ba_only(ctx)}
</div>
<div class="deltas">
  <div class="delta"><b><span class="p">+</span><span data-count="230">230</span><span class="u">%</span></b><small>Kundenanfragen</small></div>
  <div class="delta"><b><span class="m">−</span><span data-count="67">67</span><span class="u">%</span></b><small>Absprungrate</small></div>
  <div class="delta"><b><span class="p">+</span><span data-count="73">73</span><span class="u">%</span></b><small>Conversionrate</small></div>
  <div class="delta"><b><span class="m">−</span><span data-count="15">15</span><span class="u">%</span></b><small>Marketingkosten</small></div>
</div>"""


def faq_block(ctx, qas, title="Alles, was Sie <span class=\"hl\">wissen müssen</span>", h1=False):
    items = "".join(
        f'<details class="qa"{" open" if i == 0 else ""}><summary>{e(q)}<span class="qa__ic" aria-hidden="true"></span></summary><div class="qa__a">{a}</div></details>'
        for i, (q, a) in enumerate(qas))
    return f"""
<div class="faq">
  <div class="faq__intro">
    <span class="kicker">Häufige Fragen</span>
    <h2 class="h2">{title}</h2>
    <p>Hier finden Sie Antworten auf die häufigsten Fragen. Für individuelle Anliegen sind wir gern persönlich für Sie da.</p>
    <div class="hero__actions" style="margin-top:6px;animation:none">{btn_book(ctx)}{btn_wa(ctx, 'WhatsApp')}</div>
  </div>
  <div class="faq__list">{items}</div>
</div>"""


def cta_band(ctx, title="Bereit für Ihren <span class=\"hl\">digitalen Erfolg?</span>",
             text="Vereinbaren Sie jetzt Ihre kostenfreie Erstberatung und erfahren Sie, wie wir Ihr Unternehmen aufs nächste Level bringen."):
    return f"""
<section class="section section--tight">
  <div class="wrap">
    <div class="cta">
      <div>
        <span class="kicker">Jetzt starten</span>
        <h2 style="margin-top:16px">{title}</h2>
        <p>{text}</p>
        <div class="cta__actions">{btn_book(ctx, 'Termin buchen')}{btn_wa(ctx)}</div>
      </div>
      {checks(['Unverbindlich &amp; kostenfrei', 'Individuelle Strategieberatung', 'Transparentes Angebot innerhalb von 48 h', '100 % Zufriedenheitsgarantie'])}
    </div>
  </div>
</section>"""


def team_grid(ctx):
    cards = "".join(f"""
<article class="member">
  <div class="member__pic"><span aria-hidden="true">{e(ini)}</span></div>
  <div><h3>{e(n)}</h3><span class="member__role">{e(r)}</span></div>
  <p>{e(t)}</p>
</article>""" for n, ini, r, t in TEAM)
    return f'<div class="team">{cards}</div>'


def timeline():
    steps = [
        ("pie", "Strategische Analyse", "Wir verstehen Ihr Geschäft, analysieren Ihre Ziele und Ihre Zielgruppe und entwickeln eine fundierte Strategie für Ihren digitalen Erfolg.", ["Zielgruppenanalyse", "Marktforschung", "Konkurrenzanalyse"]),
        ("pen", "Design &amp; Konzept", "Kreative Konzepte und modernes Design, das Ihre Marke repräsentiert und Ihre Kunden begeistert.", ["UX/UI-Design", "Brand Identity", "Prototyping"]),
        ("code", "Entwicklung", "Technische Umsetzung nach modernen Standards: schnell, sicher und bereit, mit Ihrem Unternehmen zu wachsen.", ["Frontend-Entwicklung", "Backend-Integration", "Mobile Optimierung"]),
        ("shield", "Testing &amp; QA", "Umfassende Tests und Qualitätssicherung sorgen für eine fehlerfreie Nutzung auf allen Geräten.", ["Funktionstests", "Performance-Tests", "Cross-Browser-Tests"]),
        ("rocket", "Launch &amp; Support", "Erfolgreicher Go-live und laufende Betreuung durch unser Team und den KI-Agenten, damit Ihre Lösung langfristig wirkt.", ["Live-Deployment", "Monitoring &amp; Wartung", "Kontinuierlicher Support"]),
    ]
    items = "".join(f"""
<li class="tl__item">
  <div class="tl__card">
    <div><h3>{t}</h3><p>{d}</p>{checks(c)}</div>
    <span class="tl__icon">{icon(i)}</span>
  </div>
  <span class="tl__dot">{n + 1}</span>
</li>""" for n, (i, t, d, c) in enumerate(steps))
    return f'<ol class="tl">{items}</ol>'


def industries():
    return '<div class="inds">' + "".join(f"""
<article class="ind"><span class="ibox">{icon(i)}</span><h3>{t}</h3><p>{d}</p><small>{s}</small></article>""" for i, t, d, s in INDUSTRIES) + "</div>"


def comparison():
    Y = f'<span class="v yes">{icon("check")}'
    P = f'<span class="v part">{icon("minus")}'
    N = f'<span class="v no">{icon("x")}'
    rows = [
        ("Website auf Ihre Zielgruppe zugeschnitten", Y + "Ja</span>", Y + "Ja</span>", P + "Vorlage</span>"),
        ("Kunden- und Produktmanagement aus einer Hand", Y + "Ja</span>", P + "Selten</span>", N + "Nein</span>"),
        ("Änderungen per WhatsApp oder Dashboard", Y + "Mit KI-Agent</span>", P + "Per Auftrag</span>", N + "Selbst machen</span>"),
        ("Website, SEO und Werbung abgestimmt", Y + "Ja</span>", P + "Oft getrennt</span>", N + "Nein</span>"),
        ("Laufende Pflege inklusive", Y + "Im Abo enthalten</span>", P + "Meist extra</span>", N + "Selbst machen</span>"),
        ("Fester Ansprechpartner", Y + "Persönlich</span>", P + "Wechselnd</span>", N + "Support-Hotline</span>"),
        ("Transparentes Angebot", Y + "Innerhalb von 48 h</span>", P + "Unterschiedlich</span>", Y + "Festpreis-Tarif</span>"),
    ]
    body = "".join(f'<tr><th scope="row">{a}</th><td class="is-us">{b}</td><td>{c}</td><td>{d}</td></tr>' for a, b, c, d in rows)
    return f"""
<div class="cmp-wrap"><table class="cmp">
  <caption class="sr-only">Vergleich: Medialyte, klassische Agentur und Website-Baukasten</caption>
  <thead><tr><th scope="col">Typischer Vergleich</th><th scope="col" class="is-us">Medialyte</th><th scope="col">Klassische Agentur</th><th scope="col">Website-Baukasten</th></tr></thead>
  <tbody>{body}</tbody>
</table></div>
<p class="cmp-note">Typische Merkmale. Im Einzelfall kann es je nach Anbieter abweichen.</p>"""


def video_block():
    return f"""
<div class="video">
  <div class="video__frame">
    <span class="video__logo">{LOGO}</span>
    <button class="video__play" type="button" data-video-soon aria-label="Video abspielen (folgt in Kürze)">{icon('play')}</button>
    <div class="video__soon"><b>Video folgt in Kürze</b><span>ca. 90 Sekunden</span></div>
  </div>
  <ol class="chapters">
    <li><b>Die Ausgangslage</b><span>Warum viele Websites Kunden verlieren statt gewinnen</span></li>
    <li><b>Unser Ablauf</b><span>Vom Erstgespräch über den Entwurf bis zum Livegang</span></li>
    <li><b>Der Unterschied</b><span>Was Medialyte anders macht als klassische Agenturen</span></li>
    <li><b>Ihr KI-Agent</b><span>So bleiben Website und System ohne Aufwand aktuell</span></li>
  </ol>
</div>"""


def dashboard_mock(note=True):
    n = '<span class="mock-note">Demo-Daten</span>' if note else ""
    return f"""
<div class="dash" aria-label="Beispiel eines Kunden-Dashboards">
  {n}
  <aside class="dash__side" aria-hidden="true">
    <span class="dash__logo">{LOGO} Cockpit</span>
    <span class="dash__nav is-on">{icon('layout')} Übersicht</span>
    <span class="dash__nav">{icon('users')} Kunden</span>
    <span class="dash__nav">{icon('calendar')} Termine</span>
    <span class="dash__nav">{icon('brief')} Aufträge</span>
    <span class="dash__nav">{icon('bot')} KI-Agent</span>
  </aside>
  <div class="dash__main">
    <div class="dash__top"><b>Guten Morgen!</b><small class="muted">Heute, 08:30</small></div>
    <div class="dash__kpis">
      <div class="kpi"><small>Neue Anfragen</small><b>12</b><em>+3 seit gestern</em></div>
      <div class="kpi"><small>Termine</small><b>8</b><em>nächster 14:00</em></div>
      <div class="kpi"><small>Offene Angebote</small><b>5</b><em>2 warten auf Antwort</em></div>
    </div>
    <div class="dash__cols">
      <div class="dcol"><span class="dcol__h"><span>Neu</span><span>3</span></span>
        <div class="dcard"><b>Bäckerei Hansen</b><small>Website-Anfrage · vor 2 Std.</small></div>
        <div class="dcard"><b>Kanzlei Weber</b><small>Erstgespräch · gestern</small></div></div>
      <div class="dcol"><span class="dcol__h"><span>Termin</span><span>2</span></span>
        <div class="dcard"><b>Autohaus Nord</b><small>Do, 10:30 · Video</small></div>
        <div class="dcard"><b>Praxis am Park</b><small>Fr, 09:00 · Telefon</small></div></div>
      <div class="dcol"><span class="dcol__h"><span>Angebot</span><span>1</span></span>
        <div class="dcard"><b>Café Elbblick</b><small>Angebot gesendet</small></div></div>
    </div>
    <div class="dash__agent">{icon('bot')}<span><b>KI-Agent:</b> 2 Anfragen warten seit 24 Std. auf Antwort. Erinnerung senden?</span><button type="button" tabindex="-1">Senden</button></div>
  </div>
</div>"""


def chat_mock(ctx):
    ok = '<svg viewBox="0 0 16 11" width="16" height="11" fill="none" stroke="#53BDEB" stroke-width="1.6" aria-hidden="true" style="display:inline-block;vertical-align:-1px"><path d="M1 6l3 3 6-7M6 9l1 .8L14 2"/></svg>'
    return f"""
<div class="phone" aria-label="Beispiel-Chat mit dem Medialyte KI-Agenten">
  <div class="phone__top"><span class="phone__ava">{LOGO}</span><span><b>Medialyte Agent</b><small>online</small></span></div>
  <div class="chat">
    <div class="msg msg--out">Hallo! Am 24.12. haben wir nur bis 14 Uhr geöffnet. Kannst du das auf die Website setzen?<time>09:38 {ok}</time></div>
    <span class="typing" aria-hidden="true"><i></i><i></i><i></i></span>
    <div class="msg msg--agent">Gern! Die Öffnungszeiten für Heiligabend sind angepasst. So sieht es jetzt aus:
      <span class="msg__card"><span style="display:grid;gap:2px;padding:10px 10px 4px;color:#E9EDEF"><b style="color:#E9EDEF;font-size:.8rem">Öffnungszeiten</b><small style="color:#8696A0;font-size:.74rem">24.12. · 11:00–14:00 Uhr</small><small style="color:#8696A0;font-size:.74rem">25.12. · geschlossen</small></span><span>trattoria-sole.de</span></span>
      <time>09:39</time></div>
    <div class="msg msg--out">Perfekt. Und bitte das Wildgericht von der Karte nehmen.<time>09:40 {ok}</time></div>
    <div class="msg msg--agent">Erledigt ✓ Die Speisekarte ist aktualisiert und online.<time>09:40</time></div>
    <div class="msg msg--out">Super, danke dir!<time>09:41 {ok}</time></div>
  </div>
</div>"""


def ads_mock():
    return f"""
<div class="adwrap" style="position:relative">
  <span class="mock-note">Beispiel</span>
  <div class="serp">
    <div class="serp__bar">{icon('search')} italienisches restaurant altona</div>
    <div class="serp__ad">
      <small><b>Gesponsert</b>trattoria-sole.de</small>
      <strong>Trattoria Sole – Echte italienische Küche in Altona</strong>
      <p>Frische Pasta, Holzofenpizza und Mittagstisch. Jetzt online einen Tisch reservieren.</p>
      <div class="serp__links"><span>Speisekarte</span><span>Reservieren</span><span>Mittagstisch</span></div>
    </div>
    <div class="serp__org" aria-hidden="true"><i style="width:40%"></i><i style="width:85%"></i><i style="width:70%"></i></div>
    <div class="serp__org" aria-hidden="true"><i style="width:35%"></i><i style="width:90%"></i><i style="width:60%"></i></div>
  </div>
  <div class="camp">
    <div class="camp__h"><b>Kampagne Mittagstisch</b><span class="camp__badge"><span class="dot-live"></span>Aktiv</span></div>
    <svg class="chart" viewBox="0 0 300 110" preserveAspectRatio="none" aria-hidden="true">
      <defs><linearGradient id="adfill" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#FF5757" stop-opacity=".35"/><stop offset="1" stop-color="#FF5757" stop-opacity="0"/></linearGradient></defs>
      <g stroke="rgba(255,255,255,.06)"><path d="M0 27h300M0 55h300M0 83h300"/></g>
      <path d="M0 92 L30 88 L60 84 L90 86 L120 72 L150 70 L180 58 L210 52 L240 40 L270 34 L300 22 L300 110 L0 110Z" fill="url(#adfill)"/>
      <path d="M0 92 L30 88 L60 84 L90 86 L120 72 L150 70 L180 58 L210 52 L240 40 L270 34 L300 22" fill="none" stroke="#FF5757" stroke-width="2.5" stroke-linejoin="round"/>
      <circle cx="300" cy="22" r="4" fill="#FF5757"/>
    </svg>
    <div class="camp__rows">
      <div class="camp__row"><span>Klicks diese Woche</span><b>1.248</b></div>
      <div class="camp__row"><span>Anrufe über die Anzeige</span><b>64</b></div>
      <div class="camp__row"><span>Reservierungen</span><b>37</b></div>
    </div>
  </div>
</div>"""


def booking_widget(ctx):
    demo = "0" if ctx.mode == "prod" else "1"
    endpoint = "/api/termin.php"
    slots = "/api/slots.php"

    def opt(name, value, ic, title, sub, typ="checkbox", box=""):
        i = f"bk-{name}-{value}"
        return f'<div class="opt"><input type="{typ}" name="{name}" value="{value}" id="{i}"><label for="{i}"><span class="ibox {box}">{icon(ic)}</span><b>{title}</b><small>{sub}</small></label></div>'

    def simple(name, value, text):
        i = f"bk-{name}-{value}"
        return f'<div class="opt opt--simple"><input type="radio" name="{name}" value="{value}" id="{i}"><label for="{i}"><b>{text}</b></label></div>'

    anliegen = "".join([
        opt("anliegen", "web-neu", "globe", "Neue Website", "Noch keine oder eine veraltete Website"),
        opt("anliegen", "web-besser", "trend", "Website verbessern", "Mehr Anfragen aus Ihrer Seite"),
        opt("anliegen", "system", "db", "Kunden- oder Produktmanagement", "Eigenes System mit Dashboard", box="ibox--blue"),
        opt("anliegen", "werbung", "mega", "Werbung &amp; Online-Marketing", "Google Ads, Social Media, SEO", box="ibox--amber"),
        opt("anliegen", "agent", "bot", "KI-Agent &amp; Pflege", "Website aktuell halten ohne Aufwand", box="ibox--green"),
        opt("anliegen", "brief", "mail", "Brief von Medialyte erhalten", "Es gibt schon einen Entwurf für mich"),
    ])
    formate = "".join([
        opt("format", "video", "video", "Video-Call", "Bequem von überall", typ="radio"),
        opt("format", "telefon", "phone", "Telefon", "Wir rufen Sie an", typ="radio"),
        opt("format", "vor-ort", "pin", "Vor Ort", "In Hamburg", typ="radio"),
    ])
    branchen = ["Gastronomie & Hotellerie", "Handwerk & Bau", "Einzelhandel & E-Commerce", "Kanzlei & Beratung",
                "Praxis & Gesundheit", "Industrie & Technik", "Dienstleistung", "Immobilien", "Verein & Organisation", "Andere Branche"]
    bopts = '<option value="">Bitte wählen</option>' + "".join(f"<option>{e(b)}</option>" for b in branchen)
    groesse = "".join(simple("groesse", v, t) for v, t in [("1-5", "1–5"), ("6-20", "6–20"), ("21-100", "21–100"), ("100+", "über 100")])
    zeit = "".join(simple("zeitfenster", v, t) for v, t in [("vormittags", "Vormittags"), ("nachmittags", "Nachmittags"), ("flexibel", "Egal")])
    return f"""
<div class="bk" id="booking" data-demo="{demo}" data-endpoint="{endpoint}" data-slots="{slots}">
  <aside class="bk__aside">
    <div class="bk__host"><span class="ava"><span>D</span></span><span><b>Daniel</b><small>Inhaber · Ihr Ansprechpartner</small></span></div>
    <h3>Kostenfreie Erstberatung</h3>
    <ul class="bk__meta">
      <li>{icon('clock')} 30 Minuten</li>
      <li>{icon('video')} Video-Call, Telefon oder vor Ort in Hamburg</li>
      <li>{icon('shield')} Unverbindlich und kostenfrei</li>
    </ul>
    <div class="bk__get"><b>Das erwartet Sie</b>{checks(['Analyse Ihrer aktuellen Situation', 'Konkrete Empfehlungen für Ihr Unternehmen', 'Transparentes Angebot innerhalb von 48 h'], 'checks--green')}</div>
    <div class="bk__alt"><span>Lieber direkt sprechen?</span><a class="link" href="{SITE['wa']}" target="_blank" rel="noopener">{icon('chat')} WhatsApp schreiben</a><a class="link" href="tel:{SITE['phone_intl']}">{icon('phone')} {e(SITE['phone'])}</a></div>
  </aside>
  <form class="bk__main" novalidate>
    <ol class="bk__progress" aria-label="Fortschritt">
      <li data-p="1"><span>Anliegen</span></li><li data-p="2"><span>Unternehmen</span></li><li data-p="3"><span>Termin</span></li><li data-p="4"><span>Kontakt</span></li>
    </ol>
    <div class="bk__body">
      <section class="bk__step" data-step="1" aria-labelledby="bk-h1">
        <h3 id="bk-h1">Worum geht es?</h3>
        <p>Mehrfachauswahl möglich. So können wir uns gezielt vorbereiten.</p>
        <div class="opts">{anliegen}</div>
      </section>
      <section class="bk__step" data-step="2" aria-labelledby="bk-h2" hidden>
        <h3 id="bk-h2">Ihr Unternehmen</h3>
        <p>Ein paar Eckdaten, damit wir uns Ihre Situation vorher ansehen können.</p>
        <div class="fields">
          <div class="field"><label for="bk-firma">Unternehmen <i>*</i></label><input id="bk-firma" name="firma" autocomplete="organization" placeholder="z. B. Café Elbblick"></div>
          <div class="field"><label for="bk-branche">Branche <i>*</i></label><select id="bk-branche" name="branche">{bopts}</select></div>
          <div class="field"><label for="bk-website">Aktuelle Website</label><input id="bk-website" name="website" inputmode="url" autocomplete="url" placeholder="falls vorhanden, z. B. beispiel.de"></div>
          <div class="field"><label for="bk-ort">Ort oder PLZ</label><input id="bk-ort" name="ort" autocomplete="address-level2" placeholder="z. B. Hamburg"></div>
          <div class="field field--full"><span class="bk__sub">Mitarbeitende</span><div class="opts opts--3" style="grid-template-columns:repeat(4,minmax(0,1fr))">{groesse}</div></div>
        </div>
      </section>
      <section class="bk__step" data-step="3" aria-labelledby="bk-h3" hidden>
        <h3 id="bk-h3">Wann passt es Ihnen?</h3>
        <p>Wählen Sie, wie wir sprechen, und einen freien Termin.</p>
        <div class="opts opts--3">{formate}</div>
        <div class="cal">
          <div class="cal__box">
            <div class="cal__head"><button type="button" data-cal-prev aria-label="Vorheriger Monat">{icon('left')}</button><b></b><button type="button" data-cal-next aria-label="Nächster Monat">{icon('right')}</button></div>
            <div class="cal__grid"></div>
          </div>
          <div class="slots" aria-live="polite"></div>
        </div>
        <label class="checkline"><input type="checkbox" id="bk-callback" name="rueckruf" value="1"><span>Kein passender Termin dabei? <b>Rückruf anfordern</b>, wir melden uns.</span></label>
        <div class="bk__cb" hidden><span class="bk__sub">Wann erreichen wir Sie am besten?</span><div class="opts opts--3">{zeit}</div></div>
      </section>
      <section class="bk__step" data-step="4" aria-labelledby="bk-h4" hidden>
        <h3 id="bk-h4">Ihre Kontaktdaten</h3>
        <p>Fast geschafft. Wir bestätigen Ihren Termin per E-Mail.</p>
        <div class="bk__pick"></div>
        <div class="fields">
          <div class="field"><label for="bk-name">Vor- und Nachname <i>*</i></label><input id="bk-name" name="name" autocomplete="name" placeholder="Max Mustermann"></div>
          <div class="field"><label for="bk-email">E-Mail <i>*</i></label><input id="bk-email" name="email" type="email" autocomplete="email" placeholder="name@firma.de"></div>
          <div class="field"><label for="bk-tel">Telefon</label><input id="bk-tel" name="telefon" type="tel" autocomplete="tel" placeholder="Für Telefonat, Rückruf oder WhatsApp"></div>
          <div class="field" style="align-content:end"><label class="checkline" style="min-height:50px;align-items:center"><input type="checkbox" id="bk-wa" name="whatsapp" value="1"><span>Bestätigung zusätzlich per WhatsApp</span></label></div>
          <div class="field field--full"><label for="bk-msg">Ihre Nachricht</label><textarea id="bk-msg" name="nachricht" placeholder="Was ist Ihnen wichtig? Gibt es einen Termin, bis wann alles fertig sein soll?"></textarea></div>
          <div class="field--full hp" aria-hidden="true"><label for="bk-hp">Bitte leer lassen</label><input id="bk-hp" name="firma_url" tabindex="-1" autocomplete="off"></div>
          <label class="checkline field--full"><input type="checkbox" id="bk-consent" name="einwilligung" value="1"><span>Ich bin einverstanden, dass Medialyte meine Angaben zur Bearbeitung meiner Anfrage speichert und mich kontaktiert. Details in der <a href="{ctx.u('/datenschutz/')}">Datenschutzerklärung</a>. <i style="font-style:normal;color:var(--accent)">*</i></span></label>
        </div>
      </section>
      <section class="bk__step" data-step="5" aria-labelledby="bk-h5" hidden>
        <div class="done">
          <span class="done__ic">{icon('check')}</span>
          <h3 id="bk-h5">Vielen Dank<span class="done__name"></span>!</h3>
          <p>Ihre Anfrage für <b class="done__when"></b> ist bei uns eingegangen. Sie erhalten in Kürze eine Bestätigung per E-Mail.</p>
          <dl class="summary" style="width:100%;text-align:left"></dl>
          <div class="done__actions">
            <button class="btn btn--ghost" type="button" data-ics hidden>{icon('calendar')} In Kalender eintragen</button>
            <a class="btn btn--wa" href="{SITE['wa']}" target="_blank" rel="noopener" data-wa-done>{icon('chat')} Per WhatsApp schreiben</a>
          </div>
          <p class="demo-note" hidden>Vorschau-Modus: In dieser Vorschau wird nichts gesendet. Auf der Live-Seite geht die Anfrage direkt an das Medialyte-Dashboard.</p>
        </div>
      </section>
      <p class="bk__err" role="alert"></p>
    </div>
    <div class="bk__nav">
      <button class="btn btn--ghost" type="button" data-back hidden>{icon('left')} Zurück</button>
      <button class="btn btn--primary" type="submit" data-next style="margin-left:auto">Weiter {icon('arrow')}</button>
    </div>
  </form>
</div>"""


def page_hero(ctx, crumbs, pill, h1, lead, actions="", visual="", single=False):
    cr = "".join(f'<li><a href="{ctx.u(p)}">{e(n)}</a></li>' if p else f'<li aria-current="page">{e(n)}</li>' for n, p in crumbs)
    vis = f'<div class="phero__visual">{visual}</div>' if visual else ""
    return f"""
<section class="phero">
  <div class="hero__bg" aria-hidden="true"></div>
  <div class="wrap phero__grid{' phero__grid--single' if single or not visual else ''}">
    <div class="phero__copy">
      <ol class="crumbs" aria-label="Brotkrümelnavigation">{cr}</ol>
      <span class="pill">{pill}</span>
      <h1>{h1}</h1>
      <p class="lead">{lead}</p>
      {f'<div class="phero__actions">{actions}</div>' if actions else ''}
    </div>
    {vis}
  </div>
</section>"""


def feat_grid(items, cols=3):
    cls = "feat" if cols == 3 else "feat feat--2"
    return f'<div class="{cls}">' + "".join(f'<article class="feat__item"><span class="ibox {b}">{icon(i)}</span><h3>{t}</h3><p>{d}</p></article>' for i, t, d, b in items) + "</div>"


def steps_list(items):
    return f'<ol class="steps" style="--n:{len(items)}">' + "".join(f"<li><h3>{t}</h3><p>{d}</p></li>" for t, d in items) + "</ol>"


def browser(ctx, src, w, h, host, alt, lazy=True):
    return f'<div class="browser"><div class="chrome"><i></i><i></i><i></i><span>{e(host)}</span></div>{img(ctx, src, w, h, alt, lazy=lazy)}</div>'


# ======================================================================= Startseite
def render_home(ctx):
    hero = f"""
<section class="hero" id="start">
  <div class="hero__bg" aria-hidden="true"></div>
  <div class="wrap hero__grid">
    <div class="hero__copy">
      <span class="pill">Digitalagentur aus Hamburg · bundesweit für alle Branchen</span>
      <h1>Individuelle Lösungen zur <span class="hl">Entwicklung</span> von Kundenbeziehungen</h1>
      <p class="hero__lead">Wir gewinnen neue Kunden für Ihr Unternehmen, überzeugen sie mit einer Website, die genau auf Ihre Zielgruppe zugeschnitten ist, und bauen das System, mit dem Sie alles im Griff behalten. <strong>Ein KI-Agent hält dabei alles aktuell.</strong></p>
      <div class="hero__actions">
        {btn_book(ctx)}
        <a class="btn btn--ghost" href="#referenzen">Referenzen ansehen</a>
        <a class="btn btn--round" href="#video" aria-label="Zum Video: Medialyte in 90 Sekunden">{icon('play')}</a>
      </div>
      <div class="hero__proof">
        <div class="proof">
          <span class="avatars" aria-hidden="true">{img(ctx, 'img/logos/avatar-gado.webp', 112, 112, '', lazy=False)}{img(ctx, 'img/logos/avatar-cv.webp', 112, 112, '', lazy=False)}{img(ctx, 'img/logos/avatar-rechnungsradar.webp', 112, 112, '', lazy=False)}<span>+</span></span>
          <span><b>200+ erfolgreiche Kampagnen</b><small>für Unternehmen in ganz Deutschland</small></span>
        </div>
        <div class="proof"><span class="proof__icon">{icon('clock')}</span><span><b>Angebot in 48 h</b><small>nach dem Erstgespräch</small></span></div>
        <div class="proof"><span class="proof__icon">{icon('shield')}</span><span><b>100 % Zufriedenheit</b><small>garantiert</small></span></div>
      </div>
    </div>
    <div class="hero__visual">
      <div class="hv">
        <div class="hv__browser"><div class="chrome"><i></i><i></i><i></i><span>ritz.entwurf.medialyte.de</span></div>{img(ctx, 'img/refs/ritz-desktop.webp', 1200, 750, 'Website-Entwurf für RITZ Instrument Transformers', lazy=False)}</div>
        <div class="hv__phone">{img(ctx, 'img/refs/rechnungsradar-mobile.webp', 390, 844, 'Website RechnungsRadar auf dem Smartphone', lazy=False)}</div>
        <div class="hv__card hv__card--ads" aria-hidden="true">
          <div class="hv__row"><span class="dot-live"></span><b>Kampagne aktiv</b></div>
          <small>Neue Anfragen über Google Ads</small>
          <svg class="hv__spark" viewBox="0 0 200 38" preserveAspectRatio="none"><path d="M0 34 L25 30 L50 31 L75 24 L100 22 L125 15 L150 16 L175 8 L200 4" fill="none" stroke="#FF5757" stroke-width="2.5" stroke-linejoin="round"/></svg>
        </div>
        <div class="hv__card hv__card--chat" aria-hidden="true">
          <div class="hv__row"><span class="hv__ava">{LOGO}</span><span><b>Medialyte Agent</b><br><small>per WhatsApp · 09:41</small></span></div>
          <div class="hv__bubble">{icon('check')} Erledigt! Die Öffnungszeiten für Heiligabend sind online.</div>
        </div>
      </div>
    </div>
  </div>
</section>"""

    ansatz = f"""
<section class="section" id="ansatz">
  <div class="wrap">
    {head('Unser Ansatz', 'Vermehrung, Verbesserung und <span class="hl">Verwaltung</span> Ihrer Kundenbeziehungen', 'Gute Kundenbeziehungen entstehen nicht durch ein einzelnes Werkzeug. Deshalb denken wir Website, System, KI-Agent und Werbung zusammen und setzen genau das um, was Ihr Unternehmen gerade braucht.')}
    <div class="pillars">
      <article class="pillar" style="--glow:rgba(245,185,66,.16)">
        <div class="pillar__top"><span class="ibox ibox--amber">{icon('mega')}</span><span class="pillar__k">01 · Vermehrung</span></div>
        <h3>Neue Kunden gewinnen</h3>
        <p>Wir sorgen dafür, dass die richtigen Menschen Sie finden: mit Kampagnen, Suchmaschinenoptimierung und Landingpages, die aus Besuchern Anfragen machen.</p>
        {checks(['Google Ads und Social-Media-Kampagnen', 'SEO und lokale Sichtbarkeit', 'Landingpages mit klarem Ziel'])}
        <a class="link" href="{ctx.u('/leistungen/online-marketing/')}">Online-Marketing {icon('arrow')}</a>
      </article>
      <article class="pillar">
        <div class="pillar__top"><span class="ibox">{icon('globe')}</span><span class="pillar__k">02 · Verbesserung</span></div>
        <h3>Kunden überzeugen</h3>
        <p>Ihre Website ist oft der erste Eindruck. Wir gestalten sie für genau Ihre Zielgruppe: schnell, mobil, verständlich und mit klaren Wegen zur Anfrage.</p>
        {checks(['Individuelles Design statt Baukasten', 'Optimiert für Smartphone und Google', 'Neue Website oder Relaunch'])}
        <a class="link" href="{ctx.u('/leistungen/website-erstellung/')}">Website-Erstellung {icon('arrow')}</a>
      </article>
      <article class="pillar" style="--glow:rgba(91,140,255,.16)">
        <div class="pillar__top"><span class="ibox ibox--blue">{icon('db')}</span><span class="pillar__k">03 · Verwaltung</span></div>
        <h3>Kunden im Griff behalten</h3>
        <p>Hinter der Website bauen wir auf Wunsch Ihr eigenes Kunden- oder Produktmanagement-System. Alle Anfragen, Termine und Aufträge an einem Ort, unterstützt von einem KI-Agenten.</p>
        {checks(['Eigenes Dashboard für Ihr Team', 'Automatisierte Abläufe', 'KI-Agent für Pflege und Änderungen'])}
        <a class="link" href="{ctx.u('/leistungen/kundenmanagement-system/')}">Kundenmanagement-System {icon('arrow')}</a>
      </article>
    </div>
  </div>
</section>"""

    agent_points = f"""
<div class="agent-points">
  <div class="agent-point"><span class="ibox ibox--green">{icon('chat')}</span><b>Einfache Websites: per WhatsApp</b><p>Schreiben Sie dem Agenten, was sich ändern soll. Er kümmert sich um den Rest.</p></div>
  <div class="agent-point"><span class="ibox ibox--blue">{icon('sliders')}</span><b>Komplexe Systeme: im Dashboard</b><p>Kanzleien, Händler oder Industrie pflegen Kunden, Produkte und Inhalte im eigenen Cockpit.</p></div>
  <div class="agent-point"><span class="ibox">{icon('refresh')}</span><b>Gepflegt und betreut</b><p>Ihre Seite bleibt aktuell und technisch auf dem neuesten Stand. Für Größeres ist unser Team da.</p></div>
</div>"""

    jsteps = [
        ("Website", "Das Fundament für Ihre Kundenbeziehungen"),
        ("System", "Kunden und Aufträge an einem Ort"),
        ("KI-Agent", "Änderungen ohne Aufwand"),
        ("Werbung", "Neue Kunden, planbar"),
    ]
    jbtn = "".join(f"""
<button class="jstep" type="button" role="tab" id="jt-{i}" aria-controls="jp-{i}" aria-selected="{'true' if i == 0 else 'false'}" tabindex="{0 if i == 0 else -1}">
  <span class="jstep__n">{i + 1}</span><span class="jstep__t">{t}</span><span class="jstep__d">{d}</span><span class="jstep__bar"><i></i></span>
</button>""" for i, (t, d) in enumerate(jsteps))
    panels = [
        ("Eine Website, die Ihre Zielgruppe überzeugt",
         "Wir analysieren, wen Sie erreichen wollen, und bauen Ihre Website genau dafür. Schnell, mobil, suchmaschinenoptimiert und mit klaren Wegen zu Anruf, Termin oder Anfrage.",
         browser(ctx, 'img/refs/rubin-desktop.webp', 1200, 750, 'rubin-gold.de', 'Website Juwelier Rubin') +
         f'<ul class="tags" style="margin-top:16px"><li>Zielgruppen-Analyse</li><li>Individuelles Design</li><li>Entwicklung</li><li>SEO</li><li>Hosting &amp; SSL</li></ul>',
         ctx.u('/leistungen/website-erstellung/'), "Mehr zur Website-Erstellung"),
        ("Ihr eigenes Kunden- und Produktmanagement",
         "Anfragen aus der Website landen direkt in Ihrem Dashboard. Dort sehen Sie Kunden, Termine, Angebote und Aufträge und behalten jederzeit den Überblick.",
         dashboard_mock(), ctx.u('/leistungen/kundenmanagement-system/'), "Mehr zum Kundenmanagement-System"),
        ("Änderungen? Einfach per WhatsApp.",
         "Neue Öffnungszeiten, ein anderes Gericht, frische Bilder: Bei einfachen Websites schreiben Sie dem KI-Agenten. Bei umfangreichen Systemen erledigen Sie alles direkt im Dashboard.",
         f'<div class="chatwrap">{chat_mock(ctx)}{agent_points}</div>', ctx.u('/leistungen/ki-agent/'), "Mehr zum KI-Agenten"),
        ("Werbung, die Anfragen bringt",
         "Wenn das Fundament steht, bringen wir gezielt neue Kunden auf Ihre Website: mit Google Ads, Social Media und Landingpages. Über 200 erfolgreiche Kampagnen zeigen, wie das geht.",
         ads_mock(), ctx.u('/leistungen/online-marketing/'), "Mehr zum Online-Marketing"),
    ]
    jpanels = "".join(f"""
<div class="jpanel" role="tabpanel" id="jp-{i}" aria-labelledby="jt-{i}"{'' if i == 0 else ' hidden'}>
  <div class="jpanel__head"><div><h3>{t}</h3><p>{d}</p></div><a class="link link--accent" href="{lk}">{lt} {icon('arrow')}</a></div>
  <div class="jpanel__stage">{stage}</div>
</div>""" for i, (t, d, stage, lk, lt) in enumerate(panels))
    reise = f"""
<section class="section section--deep" id="reise">
  <div class="wrap">
    {head('Ihre Reise mit Medialyte', 'Es beginnt mit Ihrer Website. <span class="hl">Und wächst mit Ihrem Unternehmen.</span>', 'Die meisten Kunden starten mit einer neuen oder besseren Website. Danach gehen wir Schritt für Schritt weiter, genau so weit, wie es für Sie sinnvoll ist.')}
    <div class="journey">
      <div class="jsteps" role="tablist" aria-label="Stationen der Zusammenarbeit">{jbtn}</div>
      <div>{jpanels}</div>
    </div>
  </div>
</section>"""

    plans = [
        ("Präsenz", "Der Einstieg", "globe", "", "Für Betriebe ohne Website oder mit einer Website, die nicht mehr zu ihnen passt.",
         ["Analyse Ihrer Zielgruppe", "Individuelles Design und Texte", "Website für alle Geräte, schnell und SEO-optimiert", "Domain, Hosting und SSL inklusive", "Änderungen per WhatsApp über den KI-Agenten", "Wartung und persönlicher Support"],
         "web-neu,agent", False),
        ("Wachstum", "Mehr Anfragen", "trend", "ibox--amber", "Für Unternehmen, die gezielt neue Kunden gewinnen wollen.",
         ["Alles aus Präsenz", "Google Ads und Social-Media-Kampagnen", "Landingpages für Ihre wichtigsten Angebote", "SEO-Ausbau und lokale Sichtbarkeit", "Conversion-Tracking und monatlicher Bericht", "Laufende Optimierung Ihrer Kampagnen"],
         "web-neu,werbung", True),
        ("System", "Alles im Griff", "db", "ibox--blue", "Für Betriebe mit vielen Kunden, Aufträgen oder Produkten, etwa Kanzleien, Händler oder Industrie.",
         ["Alles aus Präsenz", "Individuelles Kunden- oder Produktmanagement-System", "Eigenes Dashboard für Anfragen, Termine und Aufträge", "Automatisierte Abläufe und Erinnerungen", "KI-Agent direkt im Dashboard", "Einweisung für Ihr Team"],
         "system", False),
    ]
    pcards = "".join(f"""
<article class="plan{' plan--feature' if f else ''}">
  <div class="plan__top"><span class="ibox {b}">{icon(i)}</span><span class="plan__tag">{tag}</span></div>
  <h3>{n}</h3>
  <p class="plan__for">{w}</p>
  {checks(items)}
  <div class="plan__foot">
    <div class="plan__price"><b>Pauschale + monatliches Abo</b><small>Preis im Angebot innerhalb von 48 h</small></div>
    {btn_book(ctx, n + ' anfragen', ask, 'btn--primary btn--block' if f else 'btn--ghost btn--block')}
  </div>
</article>""" for n, tag, i, b, w, items, ask, f in plans)
    pakete = f"""
<section class="section" id="leistungen">
  <span id="Leistungen" aria-hidden="true"></span>
  <div class="wrap">
    {head('Pakete', 'Maßgeschneiderte Lösungen für Ihr <span class="hl">Unternehmenswachstum</span>', 'Drei Pakete als Ausgangspunkt. Was genau Sie brauchen, klären wir im Erstgespräch, und Ihr Angebot richtet sich danach.', center=True)}
    <div class="plans">{pcards}</div>
    <div class="plans-note">
      <span>{icon('check')} Kostenfreie Erstberatung</span><span>{icon('check')} Angebot innerhalb von 48 h</span><span>{icon('check')} Pakete frei kombinierbar</span><span>{icon('check')} 100 % Zufriedenheitsgarantie</span>
    </div>
  </div>
</section>"""

    services = [
        ("Webentwicklung", "globe", "Unsere Webentwicklung ist darauf ausgelegt, Ihre Online-Präsenz zu stärken. Von der Konzeption bis zur Umsetzung erstellen wir maßgeschneiderte Websites, die nicht nur gut aussehen, sondern technisch einwandfrei funktionieren und für Suchmaschinen optimiert sind.",
         ["Responsive Website-Erstellung", "SEO-Optimierung von Grund auf", "Mobile-First-Design", "Performance-Optimierung", "Benutzerfreundliche Navigation"],
         "/leistungen/website-erstellung/", "web-neu",
         '<div class="tv-code" aria-hidden="true"><div class="chrome"><i></i><i></i><i></i><span>ihre-website.de</span></div><pre><span class="c">&lt;!-- Startseite --&gt;</span>\n<span class="k">&lt;section</span> class=<span class="s">"hero"</span><span class="k">&gt;</span>\n  <span class="k">&lt;h1&gt;</span>Ihr Angebot,\n  klar auf den Punkt<span class="k">&lt;/h1&gt;</span>\n  <span class="k">&lt;a</span> href=<span class="s">"#termin"</span><span class="k">&gt;</span>Termin buchen<span class="k">&lt;/a&gt;</span>\n<span class="k">&lt;/section&gt;</span></pre></div><span class="tv-badge" style="right:10%;bottom:14%">' + icon('check') + ' Mobil optimiert</span><span class="tv-badge" style="left:8%;top:12%;animation-delay:-3s">' + icon('zap') + ' Schnell geladen</span>'),
        ("Digitale Systeme", "db", "Optimieren Sie Ihre Geschäftsprozesse mit unseren digitalen Systemlösungen. Wir entwickeln CRM-Systeme, Management-Tools und Automatisierungen, die Ihre Effizienz steigern und Ihnen Zeit sparen, damit Sie sich auf Ihr Kerngeschäft konzentrieren können.",
         ["Maßgeschneiderte CRM-Systeme", "Prozess-Management-Tools", "Workflow-Automatisierung", "Datenintegration und -analyse", "Cloud-basierte Lösungen"],
         "/leistungen/kundenmanagement-system/", "system",
         f'<div class="tv-flow" aria-hidden="true"><div class="tv-node"><span class="ibox">{icon("globe")}</span>Anfrage über die Website</div><span class="tv-arrow"></span><div class="tv-node"><span class="ibox ibox--blue">{icon("db")}</span>Automatisch im Kundenmanagement</div><span class="tv-arrow"></span><div class="tv-node"><span class="ibox ibox--green">{icon("calendar")}</span>Termin und Erinnerung</div><span class="tv-arrow"></span><div class="tv-node"><span class="ibox ibox--amber">{icon("brief")}</span>Angebot und Auftrag</div></div>'),
        ("Marketing", "mega", "Erreichen Sie Ihre Zielgruppe mit durchdachten Marketingstrategien. Von gezielten Werbekampagnen über KI-Agenten bis zu professionellen Shootings sorgen wir dafür, dass Ihre Marke die Aufmerksamkeit bekommt, die sie verdient.",
         ["Zielgerichtete Werbekampagnen", "KI-gestützte Marketing-Agenten", "Professionelle Foto- und Video-Shootings", "Performance-Monitoring und Analytics", "Multi-Channel-Strategien"],
         "/leistungen/online-marketing/", "werbung",
         '<div class="tv-bars" aria-hidden="true"><i style="height:28%"></i><i style="height:36%"></i><i style="height:33%"></i><i style="height:52%"></i><i style="height:61%"></i><i style="height:74%"></i><i style="height:92%"></i></div><span class="tv-badge" style="right:9%;top:13%">' + icon('trend') + ' 200+ Kampagnen</span>'),
        ("Social Media", "camera", "Bauen Sie eine starke Social-Media-Präsenz auf und vergrößern Sie Ihre Reichweite organisch. Wir entwickeln authentische Content-Strategien, stärken Ihr Branding und erstellen Creatives, die Ihre Community begeistern.",
         ["Organische Reichweitensteigerung", "Konsistentes Brand-Building", "Kreative Content-Erstellung", "Community-Management", "Influencer-Kooperationen"],
         "/leistungen/online-marketing/", "werbung",
         '<div class="tv-grid" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i></div><span class="tv-badge" style="left:9%;bottom:12%">' + icon('heart') + ' Community wächst</span>'),
    ]
    tabs = "".join(f'<button class="tab" type="button" role="tab" id="st-{i}" aria-controls="sp-{i}" aria-selected="{"true" if i == 0 else "false"}" tabindex="{0 if i == 0 else -1}">{n}</button>' for i, (n, *_r) in enumerate(services))
    tpanels = "".join(f"""
<div class="tpanel" role="tabpanel" id="sp-{i}" aria-labelledby="st-{i}"{'' if i == 0 else ' hidden'}>
  <div class="tvis">{vis}</div>
  <div class="tpanel__text">
    <span class="ibox">{icon(ic)}</span>
    <h3>{n}</h3>
    <p>{d}</p>
    {checks(items)}
    <div class="hero__actions" style="margin-top:4px;animation:none">{btn_book(ctx, 'Jetzt anfragen', ask)}<a class="btn btn--ghost" href="{ctx.u(lk)}">Mehr erfahren</a></div>
  </div>
</div>""" for i, (n, ic, d, items, lk, ask, vis) in enumerate(services))
    leistungen_detail = f"""
<section class="section section--deep" id="services">
  <div class="wrap">
    {head('Services', 'Unsere Leistungen <span class="hl">im Detail</span>', 'Alles, was Ihre Kundenbeziehungen voranbringt, aus einer Hand und aufeinander abgestimmt.', center=True)}
    <div class="tabs" role="tablist" aria-label="Leistungen" data-tabs>{tabs}</div>
    {tpanels}
  </div>
</section>"""

    referenzen = f"""
<section class="section" id="referenzen">
  <div class="wrap">
    {head('Referenzen', 'Neueste <span class="hl">Projekte</span>', 'Vom digitalen Produkt über die Juwelierkette bis zum Industriekonzern. Klicken Sie auf ein Projekt für die Live-Vorschau.', center=True)}
    {ref_cards(ctx)}
    <div class="ref-more"><span>Außerdem für Hubo d'Moran, FassadenTrio, DELUXE Design, GADO Energie und viele mehr.</span><a class="link link--accent" href="{ctx.u('/referenzen/')}">Alle Referenzen {icon('arrow')}</a></div>
  </div>
</section>"""

    ergebnisse = f"""
<section class="section section--deep" id="ergebnisse">
  <div class="wrap">
    {head('Vorher vs. Nachher', 'Sichtbare <span class="hl">Ergebnisse</span>', 'Ziehen Sie den Regler und sehen Sie, was aus einer schlichten Seite geworden ist. Hinter jeder Zahl steht eine Strategie, die genau auf das Unternehmen zugeschnitten ist.', center=True, green=True)}
    {before_after(ctx)}
    <div style="display:flex;justify-content:center;margin-top:36px">{btn_book(ctx, 'Jetzt kostenfrei beraten lassen', cls='btn--ghost')}</div>
  </div>
</section>"""

    vergleich = f"""
<section class="section" id="vergleich">
  <div class="wrap">
    {head('Der Unterschied', 'Warum Medialyte statt <span class="hl">klassischer Agentur?</span>', 'Website, System, Pflege und Werbung aus einer Hand, mit einem festen Ansprechpartner und einem KI-Agenten, der Ihre Seite aktuell hält.', center=True)}
    {comparison()}
  </div>
</section>"""

    video = f"""
<section class="section section--deep" id="video">
  <div class="wrap">
    {head('Video', 'Medialyte in <span class="hl">90 Sekunden</span>', 'Wie wir arbeiten, was uns von anderen Agenturen unterscheidet und wie der KI-Agent Ihre Website aktuell hält.')}
    {video_block()}
  </div>
</section>"""

    ablauf = f"""
<section class="section" id="ablauf">
  <div class="wrap">
    {head('Ablauf', 'Unser <span class="hl">Prozess</span>', '5 Schritte zu Ihrer individuellen Lösung.', center=True)}
    {timeline()}
    <div style="display:flex;justify-content:center;margin-top:48px">{btn_book(ctx, 'Jetzt kostenfrei beraten lassen', cls='btn--ghost')}</div>
  </div>
</section>"""

    branchen = f"""
<section class="section section--deep" id="branchen">
  <div class="wrap">
    {head('Branchen', 'Für Betriebe aller Branchen, <span class="hl">bundesweit</span>', 'Ob mit alter oder ganz ohne Website: Wir finden für jedes Unternehmen die passende Lösung.')}
    {industries()}
  </div>
</section>"""

    team = f"""
<section class="section" id="team">
  <div class="wrap">
    {head('Team', 'Die Menschen hinter <span class="hl">Medialyte</span>', 'Ein festes Team, das Ihr Projekt vom ersten Gespräch bis weit nach dem Livegang begleitet.', center=True)}
    {team_grid(ctx)}
    <div style="display:flex;justify-content:center;margin-top:36px"><a class="link link--accent" href="{ctx.u('/ueber-uns/')}">Mehr über Medialyte {icon('arrow')}</a></div>
  </div>
</section>"""

    faq = f"""
<section class="section" id="faq">
  <div class="wrap">{faq_block(ctx, FAQ_MAIN)}</div>
</section>"""

    buchung = f"""
<section class="section section--deep" id="beratung">
  <div class="wrap">
    {head('Kostenfreie Erstberatung', 'Buchen Sie Ihr <span class="hl">Erstgespräch</span>', 'Wählen Sie Ihr Anliegen und einen passenden Termin. Wir bereiten uns vor und bestätigen den Termin per E-Mail.', center=True)}
    {booking_widget(ctx)}
  </div>
</section>"""

    stats = f'<section class="section--tight" style="padding-top:8px"><div class="wrap">{stats_band()}</div></section>'

    return (hero + logo_marquee(ctx) + stats + ansatz + reise + pakete + leistungen_detail + referenzen + ergebnisse
            + vergleich + video + ablauf + branchen + team + cta_band(ctx) + faq + buchung)


# ======================================================================= Leistungsseiten
def _flow_visual():
    return (f'<div class="tv-flow" aria-hidden="true"><div class="tv-node"><span class="ibox">{icon("globe")}</span>Anfrage über die Website</div><span class="tv-arrow"></span>'
            f'<div class="tv-node"><span class="ibox ibox--blue">{icon("db")}</span>Automatisch im Kundenmanagement</div><span class="tv-arrow"></span>'
            f'<div class="tv-node"><span class="ibox ibox--green">{icon("calendar")}</span>Termin und Erinnerung</div><span class="tv-arrow"></span>'
            f'<div class="tv-node"><span class="ibox ibox--amber">{icon("brief")}</span>Angebot und Auftrag</div></div>')


def svc_page(ctx, crumb, pill, h1, lead, visual, sections, faqs, ask):
    actions = btn_book(ctx, "Kostenfreie Beratung", ask) + btn_wa(ctx, "WhatsApp")
    out = page_hero(ctx, [("Start", "/"), ("Leistungen", "/#leistungen"), (crumb, "")], pill, h1, lead, actions, visual)
    out += sections
    out += f'<section class="section"><div class="wrap">{faq_block(ctx, faqs, "Fragen zu <span class=hl>" + e(crumb) + "</span>")}</div></section>'
    out += cta_band(ctx)
    return out


FAQ_WEB = [
    ("Was kostet es, eine Website erstellen zu lassen?", "<p>Ihr Angebot besteht aus einer einmaligen Pauschale für Konzeption, Design und Entwicklung und einem monatlichen Abo für Hosting, Domain, SSL, Pflege durch den KI-Agenten und Support. Den genauen Preis erhalten Sie nach dem kostenfreien Erstgespräch innerhalb von 48 Stunden.</p>"),
    ("Wie lange dauert es bis zur fertigen Website?", "<p>Eine übersichtliche Website ist in 2–4 Wochen online. Bei größeren Projekten mit vielen Unterseiten, Shop oder System planen wir gemeinsam einen Zeitplan.</p>"),
    ("Übernehmen Sie Inhalte von meiner alten Website?", "<p>Ja. Bei einem Relaunch übernehmen wir Ihre bestehenden Inhalte, überarbeiten sie bei Bedarf und richten Weiterleitungen ein, damit Ihre Google-Rankings erhalten bleiben.</p>"),
    ("Wird meine Website bei Google gefunden?", "<p>Jede Website bauen wir suchmaschinenfreundlich: schnelle Ladezeiten, saubere Struktur, passende Seitentitel und Beschreibungen. Für mehr Sichtbarkeit bieten wir zusätzlich gezielte SEO-Arbeit und Kampagnen an.</p>"),
]
FAQ_SYS = [
    ("Was ist ein Kundenmanagement-System?", "<p>Ein Kundenmanagement-System, oft CRM genannt, bündelt alles rund um Ihre Kunden an einem Ort: Kontaktdaten, Anfragen, Termine, Angebote, Aufträge und Notizen. Ihr Team sieht jederzeit, was zu tun ist.</p>"),
    ("Warum ein eigenes System statt einer Standardsoftware?", "<p>Standardsoftware zwingt Sie oft in fremde Abläufe. Ein eigenes System bildet genau Ihre Prozesse ab, ist mit Ihrer Website verbunden und wächst mit Ihrem Unternehmen.</p>"),
    ("Kann das System mit meiner Website verbunden werden?", "<p>Ja, das ist der Kern. Anfragen, Terminbuchungen und Formulare von Ihrer Website landen direkt im Dashboard, ohne Abtippen und ohne verlorene E-Mails.</p>"),
    ("Wie lange dauert die Entwicklung?", "<p>Je nach Umfang 6–12 Wochen. Wir starten mit den wichtigsten Funktionen und bauen das System Schritt für Schritt aus.</p>"),
]
FAQ_AGENT = [
    ("Wie gebe ich dem KI-Agenten eine Änderung durch?", "<p>Bei einfacheren Websites schreiben Sie per WhatsApp, was sich ändern soll, zum Beispiel neue Öffnungszeiten oder ein neues Gericht. Bei umfangreichen Systemen erledigen Sie Änderungen direkt im eigenen Dashboard.</p>"),
    ("Welche Änderungen übernimmt der Agent?", "<p>Typische laufende Änderungen wie Öffnungszeiten, Preise, Speisekarten, Bilder, kurze Texte, Termine und Ankündigungen. Neue Bereiche, Funktionen oder ein neues Design setzt unser Team persönlich um.</p>"),
    ("Brauche ich technische Kenntnisse?", "<p>Nein. Sie beschreiben einfach in eigenen Worten, was sich ändern soll. Den Rest erledigt der Agent.</p>"),
    ("Ist der KI-Agent im Preis enthalten?", "<p>Der KI-Agent ist Teil des monatlichen Abos. Welche Leistungen genau enthalten sind, steht transparent in Ihrem Angebot.</p>"),
]
FAQ_MKT = [
    ("Welche Werbekanäle nutzen Sie?", "<p>Vor allem Google Ads und Social Media wie Instagram und Facebook. Welche Kanäle für Sie sinnvoll sind, hängt von Ihrer Zielgruppe ab und klären wir im Erstgespräch.</p>"),
    ("Wie messen Sie den Erfolg einer Kampagne?", "<p>Mit sauberem Conversion-Tracking: Wir messen Anfragen, Anrufe und Buchungen, nicht nur Klicks. Sie erhalten regelmäßig einen verständlichen Bericht.</p>"),
    ("Was ist mit dem Werbebudget?", "<p>Das Werbebudget zahlen Sie direkt an die Plattform, etwa Google. Unsere Betreuung ist davon getrennt und steht transparent im Angebot.</p>"),
    ("Lohnt sich Werbung ohne gute Website?", "<p>Meist nicht. Deshalb prüfen wir zuerst, ob Ihre Website Besucher in Anfragen verwandelt. Wenn nicht, verbessern wir sie, bevor wir Budget in Werbung stecken.</p>"),
]


def render_web(ctx):
    visual = browser(ctx, "img/refs/ritz-desktop.webp", 1200, 750, "ritz.entwurf.medialyte.de", "Website-Entwurf für RITZ", lazy=False)
    sections = f"""
<section class="section">
  <div class="wrap">
    {head('Was Sie bekommen', 'Eine Website, die <span class="hl">für Sie arbeitet</span>', 'Kein Baukasten, keine Vorlage von der Stange. Ihre Website wird für Ihre Zielgruppe gemacht und rund um die Uhr gepflegt.')}
    {feat_grid([
        ('target', 'Auf Ihre Zielgruppe zugeschnitten', 'Wir analysieren, wen Sie erreichen wollen, und richten Aufbau, Texte und Gestaltung genau danach aus.', ''),
        ('mobile', 'Perfekt auf dem Smartphone', 'Mobile-First: Viele Besucher kommen über das Handy. Dort muss Ihre Seite am besten funktionieren.', 'ibox--blue'),
        ('zap', 'Schnell geladen', 'Schlanke Technik ohne Plugin-Ballast. Kurze Ladezeiten halten Besucher und helfen bei Google.', 'ibox--amber'),
        ('search', 'Bei Google auffindbar', 'Saubere Struktur, passende Seitentitel und Beschreibungen, strukturierte Daten und SEO von Grund auf.', 'ibox--green'),
        ('calendar', 'Klare Wege zur Anfrage', 'Anruf, WhatsApp, Terminbuchung oder Formular: Ihre Kunden kommen mit einem Tipp zu Ihnen.', ''),
        ('lock', 'Hosting, Domain und SSL', 'Ihre eigene Adresse, verschlüsselt und sicher gehostet. Technik ist unsere Sache.', 'ibox--blue'),
    ])}
  </div>
</section>
<section class="section section--deep">
  <div class="wrap split">
    <div class="split__text">
      <span class="pill">Neu oder Relaunch</span>
      <h2 class="h2">Keine Website? <span class="hl">Oder eine alte?</span></h2>
      <p>Viele Betriebe haben gar keine Website oder eine, die vor Jahren gebaut wurde und heute weder auf dem Handy noch bei Google überzeugt. Beides lösen wir: Wir bauen neu oder bringen Ihre bestehende Seite auf den aktuellen Stand und übernehmen dabei Ihre Inhalte.</p>
      {checks(['Analyse Ihrer bisherigen Seite und Ihrer Mitbewerber', 'Übernahme und Überarbeitung Ihrer Inhalte', 'Weiterleitungen, damit Google-Rankings erhalten bleiben', 'Pflege danach einfach per WhatsApp'])}
      {btn_book(ctx, 'Kostenfreie Beratung', 'web-neu')}
    </div>
    <div>{_ba_only(ctx)}</div>
  </div>
</section>
<section class="section">
  <div class="wrap">
    {head('Ablauf', 'In vier Schritten zur <span class="hl">neuen Website</span>', '', center=True)}
    {steps_list([
        ('Erstgespräch', 'Wir lernen Ihr Unternehmen und Ihre Ziele kennen. Kostenfrei und unverbindlich.'),
        ('Konzept &amp; Design', 'Sie erhalten einen Entwurf, den wir gemeinsam verfeinern, bis er passt.'),
        ('Entwicklung', 'Wir setzen die Website technisch um, testen alles und kümmern uns um Domain und Hosting.'),
        ('Livegang &amp; Pflege', 'Ihre Seite geht online. Danach hält der KI-Agent sie aktuell.'),
    ])}
  </div>
</section>
<section class="section section--deep">
  <div class="wrap">
    {head('Referenzen', 'Websites, die <span class="hl">online sind</span>', 'Klicken Sie auf ein Projekt für die Live-Vorschau.', center=True)}
    {ref_cards(ctx)}
  </div>
</section>"""
    return svc_page(ctx, "Website-Erstellung", "Website-Erstellung",
                    'Website erstellen lassen, die Ihre <span class="hl">Zielgruppe überzeugt</span>',
                    "Wir erstellen Ihre neue Website oder bringen die bestehende auf den neuesten Stand: individuell gestaltet, schnell, für Smartphone und Google optimiert. Hosting, Pflege und ein KI-Agent für Änderungen sind inklusive.",
                    visual, sections, FAQ_WEB, "web-neu")


def _ba_only(ctx):
    return f"""
<div class="ba" role="group" aria-label="Vorher-Nachher-Vergleich der Website RechnungsRadar">
  {img(ctx, 'img/refs/rechnungsradar-nachher.webp', 1280, 724, 'Website RechnungsRadar nach dem Relaunch')}
  {img(ctx, 'img/refs/rechnungsradar-vorher.webp', 1280, 629, 'Website RechnungsRadar vor dem Relaunch', cls='ba__before')}
  <input type="range" min="0" max="100" value="50" aria-label="Regler: links Vorher, rechts Nachher">
  <span class="ba__line" aria-hidden="true"><span class="ba__knob">{icon('drag')}</span></span>
  <span class="ba__tag ba__tag--before">Vorher</span>
  <span class="ba__tag ba__tag--after">Nachher</span>
</div>"""


def render_sys(ctx):
    sections = f"""
<section class="section">
  <div class="wrap">
    {head('Das Problem', 'Kundendaten in Excel, Zetteln <span class="hl">und E-Mails?</span>', 'Wenn Anfragen in verschiedenen Postfächern landen, Termine im Kopf stehen und Angebote in Ordnern verschwinden, gehen Kunden verloren. Ein eigenes System bringt alles an einen Ort.')}
    {feat_grid([
        ('inbox', 'Alle Anfragen an einem Ort', 'Anfragen von Website, Telefon, E-Mail und WhatsApp landen gesammelt in Ihrem Dashboard.', ''),
        ('users', 'Kunden im Überblick', 'Kontaktdaten, Verlauf, Notizen und Dokumente zu jedem Kunden, für das ganze Team sichtbar.', 'ibox--blue'),
        ('calendar', 'Termine und Erinnerungen', 'Terminbuchungen von der Website, automatische Erinnerungen und keine vergessenen Rückrufe.', 'ibox--green'),
        ('brief', 'Angebote und Aufträge', 'Vom ersten Kontakt bis zum Auftrag: Sie sehen jederzeit, was offen ist und was als Nächstes kommt.', 'ibox--amber'),
        ('layers', 'Produktmanagement', 'Für Händler und Industrie: Produkte, Varianten und Datenblätter zentral pflegen und auf der Website ausspielen.', ''),
        ('bot', 'KI-Agent im Dashboard', 'Der Agent erinnert an offene Anfragen, fasst zusammen und übernimmt Routineaufgaben.', 'ibox--green'),
    ])}
  </div>
</section>
<section class="section section--deep">
  <div class="wrap split">
    <div class="split__text">
      <span class="pill">Ihr Cockpit</span>
      <h2 class="h2">Ein Dashboard, <span class="hl">gebaut für Ihre Abläufe</span></h2>
      <p>Wir entwickeln Ihr System nicht von der Stange, sondern genau für die Art, wie Ihr Unternehmen arbeitet. Ob Mandantenverwaltung für eine Kanzlei, Auftragsplanung im Handwerk oder Produktfinder für tausende Artikel wie bei RITZ.</p>
      {checks(['Direkt mit Ihrer Website verbunden', 'Zugriff für Ihr ganzes Team, auch mobil', 'Automatisierte Abläufe statt Fleißarbeit', 'Wächst mit Ihrem Unternehmen'])}
      {btn_book(ctx, 'System anfragen', 'system')}
    </div>
    <div class="tvis">{_flow_visual()}</div>
  </div>
</section>
<section class="section">
  <div class="wrap">
    {head('Referenz', 'App-Entwicklung für <span class="hl">RechnungsRadar</span>', 'Ein Rechnungsmanagement-System, das Rechnungen automatisch aus dem E-Mail-Postfach in die Buchhaltung überträgt.')}
    <div class="split">
      <div>{browser(ctx, 'img/refs/rechnungsradar-desktop.webp', 1200, 750, 'rechnungs-radar.de', 'Website RechnungsRadar')}</div>
      <div class="split__text">
        <p>RechnungsRadar verbindet E-Mail-Postfächer mit Buchhaltungsprogrammen wie Lexware Office, BuchhaltungsButler oder DATEV. Medialyte hat die App-Entwicklung und den Webauftritt umgesetzt.</p>
        <button class="btn btn--ghost" type="button" data-ref="rechnungsradar">{icon('eye')} Live-Vorschau öffnen</button>
      </div>
    </div>
  </div>
</section>
<section class="section section--deep">
  <div class="wrap">
    {head('Ablauf', 'Vom Gespräch zum <span class="hl">fertigen System</span>', '', center=True)}
    {steps_list([
        ('Analyse', 'Wir schauen uns Ihre Abläufe an und klären, was das System können muss.'),
        ('Konzept', 'Sie sehen vorab, wie Dashboard und Abläufe aussehen werden.'),
        ('Entwicklung', 'Wir bauen das System in Etappen und binden Ihre Website an.'),
        ('Einführung', 'Wir richten alles ein, weisen Ihr Team ein und betreuen Sie danach weiter.'),
    ])}
  </div>
</section>"""
    return svc_page(ctx, "Kundenmanagement-System", "Kundenmanagement-System &amp; Dashboard",
                    'Ihr eigenes <span class="hl">Kundenmanagement-System</span> mit Dashboard',
                    "Wir entwickeln Kunden- und Produktmanagement-Systeme, die genau zu Ihren Abläufen passen und direkt mit Ihrer Website verbunden sind. Alle Anfragen, Termine, Angebote und Aufträge an einem Ort.",
                    dashboard_mock(), sections, FAQ_SYS, "system")


def render_agent(ctx):
    agent_points_big = f"""
<div class="agent-points">
  <div class="agent-point"><span class="ibox ibox--green">{icon('chat')}</span><b>Einfache Websites: per WhatsApp</b><p>Gastronomie, Handwerk oder Dienstleister schreiben dem Agenten einfach, was sich ändern soll.</p></div>
  <div class="agent-point"><span class="ibox ibox--blue">{icon('sliders')}</span><b>Komplexe Systeme: im Dashboard</b><p>Kanzleien, Händler oder Industrie pflegen Kunden, Produkte und Inhalte im eigenen Cockpit.</p></div>
  <div class="agent-point"><span class="ibox">{icon('refresh')}</span><b>Gepflegt und betreut</b><p>Ihre Seite bleibt aktuell und technisch auf dem neuesten Stand.</p></div>
</div>"""
    sections = f"""
<section class="section">
  <div class="wrap">
    {head('So funktioniert es', 'Änderungen in <span class="hl">einer Nachricht</span>', 'Ihre Website soll aktuell sein, aber im Alltag fehlt die Zeit. Genau dafür gibt es den KI-Agenten.', center=True)}
    {steps_list([
        ('Bescheid geben', 'Sie schreiben per WhatsApp oder im Dashboard, was sich ändern soll. In eigenen Worten.'),
        ('Agent setzt um', 'Der KI-Agent pflegt die Änderung auf Ihrer Website ein.'),
        ('Seite ist aktuell', 'Ihre Kunden sehen sofort den neuesten Stand.'),
    ])}
  </div>
</section>
<section class="section section--deep">
  <div class="wrap duo">
    <div class="duo__col">
      <h3><span class="ibox ibox--green">{icon('bot')}</span> Das übernimmt der Agent</h3>
      {checks(['Öffnungszeiten, Feiertage und Ruhetage', 'Preise, Speisekarten und Preislisten', 'Bilder austauschen und ergänzen', 'Kurze Texte, Termine und Ankündigungen', 'Laufende Betreuung Ihrer Seite'], 'checks--green')}
    </div>
    <div class="duo__col">
      <h3><span class="ibox">{icon('users')}</span> Das macht unser Team persönlich</h3>
      {checks(['Neue Bereiche und Funktionen', 'Design-Anpassungen', 'Beratung zu Google, Werbung und Marketing', 'Größere Umbauten und Sonderwünsche'])}
    </div>
  </div>
</section>
<section class="section">
  <div class="wrap split">
    <div class="split__text">
      <span class="pill">Zwei Wege</span>
      <h2 class="h2">WhatsApp oder <span class="hl">Dashboard</span></h2>
      <p>Wie Sie mit dem Agenten arbeiten, hängt davon ab, wie umfangreich Ihr System ist. Beides ist ohne technische Kenntnisse nutzbar.</p>
      {agent_points_big}
    </div>
    <div>{dashboard_mock()}</div>
  </div>
</section>
<section class="section section--deep">
  <div class="wrap">
    {head('Beispiele', 'Was Kunden dem Agenten <span class="hl">schreiben</span>', 'Typische Nachrichten aus dem Alltag, für jede Branche.')}
    {feat_grid([
        ('food', 'Gastronomie', '„Diese Woche gibt es Kürbissuppe als Mittagstisch, bitte auf die Karte setzen.“', ''),
        ('hammer', 'Handwerk', '„Wir sind vom 23.12. bis 2.1. im Betriebsurlaub, bitte einen Hinweis einbauen.“', 'ibox--amber'),
        ('bag', 'Einzelhandel', '„Neue Herbstkollektion ist da. Hier sind sechs Fotos für die Startseite.“', 'ibox--blue'),
        ('scale', 'Kanzleien', '„Frau Becker ist neu im Team, bitte mit Foto und Schwerpunkten ergänzen.“', ''),
        ('health', 'Praxen', '„Mittwochnachmittag sind wir ab sofort geschlossen, bitte Sprechzeiten anpassen.“', 'ibox--green'),
        ('heart', 'Vereine', '„Das Sommerfest ist am 12. Juli, bitte als Termin auf die Website stellen.“', 'ibox--amber'),
    ])}
  </div>
</section>"""
    visual = f'<div style="display:grid;justify-items:center">{chat_mock(ctx)}</div>'
    return svc_page(ctx, "KI-Agent", "KI-Agent für Ihre Website",
                    'Der KI-Agent, der Ihre <span class="hl">Website aktuell hält</span>',
                    "Wird meine Seite gepflegt? Und wie ändere ich etwas, ohne mich mit Technik zu beschäftigen? Der Medialyte KI-Agent beantwortet beides: Änderungen per WhatsApp oder im Dashboard, laufende Pflege inklusive.",
                    visual, sections, FAQ_AGENT, "agent")


def render_mkt(ctx):
    sections = f"""
<section class="section">
  <div class="wrap">
    {head('Leistungen', 'Marketing, das <span class="hl">messbar wirkt</span>', 'Wir erreichen Ihre Zielgruppe dort, wo sie sucht, und machen aus Aufmerksamkeit Anfragen.')}
    {feat_grid([
        ('search', 'Google Ads', 'Anzeigen genau dann, wenn Kunden nach Ihrer Leistung suchen. Mit klarer Zielgruppe und kontrolliertem Budget.', ''),
        ('camera', 'Social-Media-Werbung', 'Kampagnen auf Instagram und Facebook, die zu Ihrer Marke passen und gezielt neue Kunden ansprechen.', 'ibox--blue'),
        ('trend', 'SEO und lokale Sichtbarkeit', 'Bessere Platzierungen bei Google, gepflegte Unternehmensprofile und Inhalte, die gefunden werden.', 'ibox--green'),
        ('layout', 'Landingpages', 'Eigene Seiten für Ihre Angebote, gebaut für eine Aufgabe: aus Besuchern Anfragen machen.', 'ibox--amber'),
        ('spark', 'KI-gestützte Marketing-Agenten', 'Automatisierte Abläufe für Inhalte, Auswertung und Nachfassen, damit kein Kontakt verloren geht.', ''),
        ('video', 'Foto- und Video-Shootings', 'Professionelle Bilder und Videos für Website, Anzeigen und Social Media.', 'ibox--blue'),
    ])}
  </div>
</section>
<section class="section section--deep">
  <div class="wrap split">
    <div class="split__text">
      <span class="pill pill--green">200+ erfolgreiche Kampagnen</span>
      <h2 class="h2">Erst das Fundament, <span class="hl">dann die Reichweite</span></h2>
      <p>Werbung bringt Besucher. Ob daraus Kunden werden, entscheidet Ihre Website. Deshalb prüfen wir zuerst, ob Ihre Seite überzeugt, und stimmen Website, Landingpage und Kampagne aufeinander ab. So wird aus Budget Umsatz.</p>
      {checks(['Saubere Conversion-Messung: Anfragen, Anrufe, Buchungen', 'Verständliche Berichte statt Zahlenfriedhof', 'Laufende Optimierung Ihrer Kampagnen'])}
      {btn_book(ctx, 'Kampagne anfragen', 'werbung')}
    </div>
    <div class="tvis"><div class="tv-bars" aria-hidden="true"><i style="height:28%"></i><i style="height:36%"></i><i style="height:33%"></i><i style="height:52%"></i><i style="height:61%"></i><i style="height:74%"></i><i style="height:92%"></i></div><span class="tv-badge" style="right:9%;top:13%">{icon('trend')} 200+ Kampagnen</span><span class="tv-badge" style="left:8%;bottom:12%;animation-delay:-3s">{icon('target')} Anfragen statt Klicks</span></div>
  </div>
</section>
<section class="section">
  <div class="wrap">
    {head('Social Media', 'Reichweite, die <span class="hl">organisch wächst</span>', 'Authentische Inhalte, ein starkes Branding und eine Community, die sich für Ihr Unternehmen begeistert.')}
    {feat_grid([
        ('trend', 'Organische Reichweite', 'Strategie, Redaktionsplan und Inhalte, die zu Ihrer Zielgruppe passen.', ''),
        ('pen', 'Brand-Building', 'Ein konsistenter Auftritt, an dem man Sie sofort erkennt.', 'ibox--blue'),
        ('users', 'Community-Management', 'Wir betreuen Kommentare und Nachrichten und bauen Beziehungen auf.', 'ibox--green'),
    ])}
  </div>
</section>"""
    visual = ads_mock()
    return svc_page(ctx, "Online-Marketing", "Online-Marketing &amp; Werbung",
                    'Werbung, die <span class="hl">neue Kunden bringt</span>',
                    "Google Ads, Social Media und SEO aus einer Hand, abgestimmt auf Ihre Website. Über 200 erfolgreiche Kampagnen zeigen, wie aus Reichweite echte Anfragen werden.",
                    visual, sections, FAQ_MKT, "werbung")


# ======================================================================= Weitere Seiten
def render_refs(ctx):
    wall = "".join(f'<div>{img(ctx, "img/logos/" + f + ".webp", _LOGO_DIMS[f][0], _LOGO_DIMS[f][1], a)}</div>' for f, a in LOGOS)
    more = [
        ("Hubo d'Moran", "Gemeinnütziger Verein", "Zweisprachige Website für einen gemeinnützigen Verein mit Spendenbereich und Buchprojekt.", "https://hubodmoran.com/"),
        ("FassadenTrio", "Dienstleister", "Google-Ads-Kampagne und Conversion-Landingpage mit Vorher-Nachher-Regler, Ablauf und Fassaden-Check-Rechner.", ""),
        ("DELUXE Design", "E-Commerce", "Hochwertiger Online-Shop auf Shopify für eine Luxusmarke.", ""),
    ]
    mcards = "".join(f"""
<article class="feat__item"><span class="pill pill--plain">{e(c)}</span><h3>{e(n)}</h3><p>{e(d)}</p>{f'<a class="link link--accent" href="{u}" target="_blank" rel="noopener">Website ansehen {icon("out")}</a>' if u else ''}</article>""" for n, c, d, u in more)
    return (page_hero(ctx, [("Start", "/"), ("Referenzen", "")], "Referenzen", 'Projekte, die <span class="hl">Kunden gewinnen</span>',
                      "Vom digitalen Produkt über die Juwelierkette bis zum Industriekonzern: Eine Auswahl unserer Arbeiten. Klicken Sie auf ein Projekt für die Live-Vorschau.",
                      btn_book(ctx) + btn_wa(ctx, "WhatsApp"))
            + f'<section class="section section--flush-top"><div class="wrap">{ref_cards(ctx)}</div></section>'
            + f'<section class="section section--deep"><div class="wrap">{head("Weitere Projekte", "Mehr aus unserer <span class=hl>Arbeit</span>")}<div class="feat">{mcards}</div></div></section>'
            + f'<section class="section"><div class="wrap">{head("Vorher vs. Nachher", "Sichtbare <span class=hl>Ergebnisse</span>", "Ziehen Sie den Regler: So hat sich der Webauftritt von RechnungsRadar verändert.", center=True, green=True)}{before_after(ctx)}</div></section>'
            + f'<section class="section section--deep"><div class="wrap">{head("Kunden &amp; Partner", "Unternehmen, die uns <span class=hl>vertrauen</span>", center=True)}<div class="logo-wall">{wall}</div></div></section>'
            + cta_band(ctx, 'Ihr Projekt als <span class="hl">nächste Referenz?</span>', "Erzählen Sie uns im kostenfreien Erstgespräch, was Sie vorhaben. Ihr Angebot erhalten Sie innerhalb von 48 Stunden."))


def render_about(ctx):
    values = [
        ("target", "Erst verstehen, dann bauen", "Jede Lösung beginnt mit Ihrer Zielgruppe und Ihren Abläufen, nicht mit einer Vorlage.", ""),
        ("users", "Ein fester Ansprechpartner", "Sie sprechen immer mit Menschen, die Ihr Projekt kennen.", "ibox--blue"),
        ("shield", "Klare Angebote", "Pauschale plus Abo, transparent aufgeschlüsselt und ohne versteckte Kosten.", "ibox--green"),
        ("spark", "Technik mit Zukunft", "Eigene KI-Agenten und moderne Technik ohne Plugin-Ballast.", "ibox--amber"),
    ]
    vgrid = '<div class="values">' + "".join(f'<article class="feat__item"><span class="ibox {b}">{icon(i)}</span><h3>{t}</h3><p>{d}</p></article>' for i, t, d, b in values) + "</div>"
    return (page_hero(ctx, [("Start", "/"), ("Über uns", "")], "Über Medialyte",
                      'Wir entwickeln <span class="hl">Kundenbeziehungen</span>',
                      "Medialyte ist eine Digitalagentur aus Hamburg. Wir bauen Websites, Kundenmanagement-Systeme und Kampagnen für Betriebe in ganz Deutschland und stellen jedem Kunden einen KI-Agenten zur Seite, der alles aktuell hält.",
                      btn_book(ctx) + btn_wa(ctx, "WhatsApp"))
            + f"""
<section class="section section--flush-top"><div class="wrap">{stats_band()}</div></section>
<section class="section">
  <div class="wrap split">
    <div class="split__text">
      <span class="pill">Unsere Idee</span>
      <h2 class="h2">Vermehrung, Verbesserung, <span class="hl">Verwaltung</span></h2>
      <p>Ein Unternehmen lebt von seinen Kundenbeziehungen. Deshalb sehen wir Website, System und Werbung nicht als einzelne Aufträge, sondern als Reise, die wir gemeinsam mit unseren Kunden gehen. Meist beginnt sie mit einer neuen Website. Danach kommen, wenn es passt, das eigene Kundenmanagement, der KI-Agent und gezielte Werbung dazu.</p>
      <p>So entsteht Schritt für Schritt ein System, das neue Kunden gewinnt, sie überzeugt und dafür sorgt, dass keiner verloren geht.</p>
    </div>
    <div>{browser(ctx, 'img/refs/ritz-desktop.webp', 1200, 750, 'ritz.entwurf.medialyte.de', 'Website-Entwurf für RITZ')}</div>
  </div>
</section>
<section class="section section--deep"><div class="wrap">{head('Team', 'Die Menschen hinter <span class="hl">Medialyte</span>', 'Ein festes Team, das Ihr Projekt vom ersten Gespräch bis weit nach dem Livegang begleitet.', center=True)}{team_grid(ctx)}</div></section>
<section class="section"><div class="wrap">{head('Werte', 'Wofür wir <span class="hl">stehen</span>', '')}{vgrid}</div></section>
<section class="section section--deep"><div class="wrap">{head('Partner', 'Offizieller <span class="hl">IONOS Agency Partner</span>', 'Ihre Website läuft auf der zuverlässigen Infrastruktur von IONOS, betreut von uns.')}<div class="partner" style="margin-top:0">{img(ctx, 'img/logos/ionos-agency-partner.webp', 142, 100, 'IONOS Agency Partner Official')}</div></div></section>
""" + cta_band(ctx))


def render_termin(ctx):
    return (page_hero(ctx, [("Start", "/"), ("Termin", "")], "Kostenfreie Erstberatung",
                      'Buchen Sie Ihr <span class="hl">Erstgespräch</span>',
                      "Wählen Sie Ihr Anliegen und einen passenden Termin. Wir bereiten uns vor, bestätigen den Termin per E-Mail und erstellen Ihnen danach innerhalb von 48 Stunden ein transparentes Angebot.")
            + f'<section class="section section--flush-top" id="beratung"><div class="wrap">{booking_widget(ctx)}</div></section>')


def render_impressum(ctx):
    return page_hero(ctx, [("Start", "/"), ("Impressum", "")], "Rechtliches", "Impressum", "Angaben zum Anbieter dieser Website.") + f"""
<section class="section section--flush-top"><div class="wrap"><div class="prose">
  <h2>Angaben gemäß § 5 DDG</h2>
  <p>Medialyte – Marketing &amp; Management<br>Inhaber: {e(SITE['owner'])}<br>{e(SITE['street'])}<br>{e(SITE['zip'])} {e(SITE['city'])}</p>
  <h2>Kontakt</h2>
  <p>Telefon: <a href="tel:{SITE['phone_intl']}">{e(SITE['phone'])}</a><br>E-Mail: <a href="mailto:{SITE['email']}">{e(SITE['email'])}</a></p>
  <h2>Verbraucherstreitbeilegung / Universalschlichtungsstelle</h2>
  <p>Wir nehmen an einem Streitbeilegungsverfahren vor einer Verbraucherschlichtungsstelle teil. Zuständig ist die Universalschlichtungsstelle des Zentrums für Schlichtung e.V., Straßburger Straße 8, 77694 Kehl am Rhein (<a href="https://www.verbraucher-schlichter.de" target="_blank" rel="noopener">www.verbraucher-schlichter.de</a>).</p>
</div></div></section>"""


def render_legal_placeholder(title, what):
    def r(ctx):
        return page_hero(ctx, [("Start", "/"), (title, "")], "Rechtliches", title, f"{what}") + """
<section class="section section--flush-top"><div class="wrap"><div class="prose">
  <p class="todo">Dieser Text wird vor dem Livegang eingefügt.</p>
</div></div></section>"""
    return r


def render_404(ctx):
    return f"""
<section class="section"><div class="wrap notfound"><div style="display:grid;gap:18px;justify-items:center">
  <b>404</b><h1 class="h2">Diese Seite gibt es nicht <span class="hl">(mehr)</span></h1>
  <p class="lead">Vielleicht hilft Ihnen einer dieser Wege weiter.</p>
  <div class="hero__actions" style="justify-content:center;animation:none"><a class="btn btn--primary" href="{ctx.u('/')}">Zur Startseite</a><a class="btn btn--ghost" href="{ctx.u('/termin/')}">Termin buchen</a></div>
</div></div></section>"""


def _svc_schema(name, path, desc):
    return {"@context": "https://schema.org", "@type": "Service", "name": name, "description": desc,
            "provider": {"@id": SITE["url"] + "/#org"}, "areaServed": {"@type": "Country", "name": "Deutschland"},
            "url": SITE["url"] + path}


def _after_dialog(ctx):
    return ref_dialog(ctx)


PAGES = [
    {"path": "/", "title": "Medialyte | Websites, Kundenmanagement & KI-Agent – Digitalagentur Hamburg",
     "desc": "Medialyte entwickelt Ihre Kundenbeziehungen: individuelle Websites, eigene Kundenmanagement-Systeme, ein KI-Agent für Änderungen per WhatsApp und Werbung mit 200+ erfolgreichen Kampagnen. Bundesweit, aus Hamburg.",
     "og_title": "Medialyte | Hamburgs Spezialagentur für Kundenbeziehungen",
     "render": render_home, "after": _after_dialog, "priority": "1.0",
     "schema": [org_schema(), {"@context": "https://schema.org", "@type": "WebSite", "name": "Medialyte", "url": SITE["url"] + "/", "inLanguage": "de-DE", "publisher": {"@id": SITE["url"] + "/#org"}}, faq_schema(FAQ_MAIN)]},
    {"path": "/leistungen/website-erstellung/", "active": "leistungen",
     "title": "Website erstellen lassen – individuell & SEO-optimiert | Medialyte",
     "desc": "Website erstellen lassen oder Relaunch: individuelles Design für Ihre Zielgruppe, schnell, mobil und SEO-optimiert. Inklusive Hosting, Domain, SSL und KI-Agent für Änderungen per WhatsApp.",
     "render": render_web, "after": _after_dialog, "priority": "0.9",
     "schema": [_svc_schema("Website-Erstellung", "/leistungen/website-erstellung/", "Individuelle Websites und Relaunches für Unternehmen aller Branchen."),
                breadcrumb_schema([("Start", "/"), ("Website-Erstellung", "/leistungen/website-erstellung/")]), faq_schema(FAQ_WEB)]},
    {"path": "/leistungen/kundenmanagement-system/", "active": "leistungen",
     "title": "Kundenmanagement-System & Dashboard entwickeln lassen | Medialyte",
     "desc": "Eigenes CRM und Dashboard nach Maß: Anfragen, Kunden, Termine, Angebote und Aufträge an einem Ort, direkt mit Ihrer Website verbunden. Kunden- und Produktmanagement-Systeme von Medialyte.",
     "render": render_sys, "after": _after_dialog, "priority": "0.9",
     "schema": [_svc_schema("Kundenmanagement-System", "/leistungen/kundenmanagement-system/", "Individuelle Kunden- und Produktmanagement-Systeme mit Dashboard."),
                breadcrumb_schema([("Start", "/"), ("Kundenmanagement-System", "/leistungen/kundenmanagement-system/")]), faq_schema(FAQ_SYS)]},
    {"path": "/leistungen/ki-agent/", "active": "leistungen",
     "title": "KI-Agent für Ihre Website – Änderungen per WhatsApp | Medialyte",
     "desc": "Der Medialyte KI-Agent hält Ihre Website aktuell: Öffnungszeiten, Preise, Speisekarten und Bilder ändern Sie per WhatsApp oder im Dashboard. Laufende Pflege inklusive.",
     "render": render_agent, "priority": "0.8",
     "schema": [_svc_schema("KI-Agent für Websites", "/leistungen/ki-agent/", "KI-Agent für Website-Pflege und Änderungen per WhatsApp oder Dashboard."),
                breadcrumb_schema([("Start", "/"), ("KI-Agent", "/leistungen/ki-agent/")]), faq_schema(FAQ_AGENT)]},
    {"path": "/leistungen/online-marketing/", "active": "leistungen",
     "title": "Online-Marketing & Google Ads Agentur – 200+ Kampagnen | Medialyte",
     "desc": "Google Ads, Social-Media-Werbung, SEO und Landingpages aus einer Hand, abgestimmt auf Ihre Website. Über 200 erfolgreiche Kampagnen. Jetzt kostenfreie Beratung buchen.",
     "render": render_mkt, "priority": "0.8",
     "schema": [_svc_schema("Online-Marketing", "/leistungen/online-marketing/", "Google Ads, Social Media, SEO und Landingpages."),
                breadcrumb_schema([("Start", "/"), ("Online-Marketing", "/leistungen/online-marketing/")]), faq_schema(FAQ_MKT)]},
    {"path": "/referenzen/", "active": "referenzen",
     "title": "Referenzen & Projekte | Medialyte Digitalagentur",
     "desc": "Referenzen von Medialyte: RechnungsRadar, Juwelier Rubin, RITZ Instrument Transformers, Hubo d'Moran, FassadenTrio und mehr. Mit Live-Vorschau.",
     "render": render_refs, "after": _after_dialog, "priority": "0.8",
     "schema": [breadcrumb_schema([("Start", "/"), ("Referenzen", "/referenzen/")])]},
    {"path": "/ueber-uns/", "active": "ueber-uns",
     "title": "Über uns – das Team hinter Medialyte | Hamburg",
     "desc": "Medialyte ist eine Digitalagentur aus Hamburg für Websites, Kundenmanagement-Systeme, KI-Agenten und Online-Marketing. Lernen Sie unser Team kennen.",
     "render": render_about, "priority": "0.6",
     "schema": [breadcrumb_schema([("Start", "/"), ("Über uns", "/ueber-uns/")])]},
    {"path": "/termin/",
     "title": "Kostenfreie Erstberatung buchen | Medialyte",
     "desc": "Buchen Sie Ihr kostenfreies Erstgespräch mit Medialyte: Anliegen wählen, Termin aussuchen, fertig. Per Video-Call, Telefon oder vor Ort in Hamburg.",
     "render": render_termin, "priority": "0.9",
     "schema": [breadcrumb_schema([("Start", "/"), ("Termin buchen", "/termin/")])]},
    {"path": "/impressum/", "title": "Impressum | Medialyte", "desc": "Impressum von Medialyte – Marketing & Management, Hamburg.",
     "render": render_impressum, "priority": "0.2", "robots": "noindex, follow"},
    {"path": "/datenschutz/", "title": "Datenschutzerklärung | Medialyte", "desc": "Datenschutzerklärung von Medialyte.",
     "render": render_legal_placeholder("Datenschutzerklärung", "Informationen zum Umgang mit Ihren Daten."), "priority": "0.2", "robots": "noindex, follow"},
    {"path": "/agb/", "title": "AGB | Medialyte", "desc": "Allgemeine Geschäftsbedingungen von Medialyte.",
     "render": render_legal_placeholder("Allgemeine Geschäftsbedingungen", "Unsere Allgemeinen Geschäftsbedingungen."), "priority": "0.2", "robots": "noindex, follow"},
    {"path": "/404.html", "title": "Seite nicht gefunden | Medialyte", "desc": "Diese Seite existiert nicht.",
     "render": render_404, "sitemap": False, "robots": "noindex, follow"},
]
