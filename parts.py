"""Bausteine und gemeinsame Inhalte der Seiten (Referenzen, Team, FAQ, Pakete, Ablauf, Buchung …)."""
import json
import math
from pathlib import Path

from build import BRAND, LOGO, SITE, book_href, e, icon
import mocks

ROOT = Path(__file__).resolve().parent
_REFS_META = json.loads((ROOT / "src/assets/img/refs/refs.json").read_text())
_LOGO_DIMS = {d["file"].replace(".webp", ""): (d["w"], d["h"]) for d in json.loads((ROOT / "src/assets/img/logos/logos.json").read_text())}

# ======================================================================= Daten
LOGOS = [
    ("rubin", "Juwelier Rubin"), ("fassadentrio", "FassadenTrio"), ("ritz", "RITZ Instrument Transformers"),
    ("rechnungsradar", "RechnungsRadar"), ("cv", "CV"), ("hubo-dmoran", "Hubo d’Moran"),
    ("deluxe-design", "DELUXE Design"), ("amore-eventdeko", "Amore Eventdeko"),
    ("ionos-agency-partner", "IONOS Agency Partner Official"), ("garee-beauty", "garée beauty"),
    ("glory-angels", "Glory Angels"), ("sabaai-thai", "Sabaai Thai Massage & Wellness"), ("gado-energie", "GADO Energie"),
]

REFS = {
    "rechnungsradar": {
        "title": "RechnungsRadar", "cat": "Software · App-Entwicklung und Website",
        "h": "Rechnungen, die sich von selbst ablegen",
        "text": "RechnungsRadar holt Rechnungen automatisch aus dem E-Mail-Postfach und legt sie in der Buchhaltung ab – in Lexware Office, BuchhaltungsButler oder DATEV. Wir haben die App entwickelt und den Auftritt gebaut, der Unternehmen und Steuerberater überzeugt.",
        "facts": [["Kunde", "RechnungsRadar"], ["Branche", "Software für Buchhaltung"], ["Leistungen", "App-Entwicklung, Rechnungsmanagement-System, Website, Conversion-Optimierung"], ["Ergebnis", "Deutlich mehr Anfragen von Steuerberatern"]],
        "nums": [["+230 %", "Kundenanfragen"], ["+73 %", "Conversionrate"]], "nums_label": "Ergebnis nach dem Relaunch",
        "url": "https://rechnungs-radar.de/", "host": "rechnungs-radar.de", "visit": "rechnungs-radar.de besuchen",
    },
    "rubin": {
        "title": "Juwelier Rubin", "cat": "Handel · Juwelierkette mit vier Filialen",
        "h": "Schmuck, der online so wirkt wie im Laden",
        "text": "Trauringe, Verlobungsringe, Brillantschmuck und Uhren – präsentiert so hochwertig wie in der Vitrine. Kundinnen und Kunden finden mit einem Klick ihre Filiale in Hamburg, Norderstedt oder Lüneburg und alle Services vom Goldankauf bis zur Reparatur.",
        "facts": [["Kunde", "Juwelier Rubin"], ["Branche", "Schmuck und Uhren"], ["Leistungen", "Webdesign, Entwicklung, Produktwelten, Filialfinder"], ["Standorte", "Hamburg, Norderstedt, Lüneburg"]],
        "nums": [["4", "Filialen"], ["3", "Städte"]], "nums_label": "Der Kunde",
        "url": "https://rubin-gold.de/", "host": "rubin-gold.de", "visit": "rubin-gold.de besuchen",
    },
    "ritz": {
        "title": "RITZ Instrument Transformers", "cat": "Industrie · Website-Entwurf für einen Konzern",
        "h": "Ein Industriekonzern auf einer Plattform",
        "text": "RITZ entwickelt und fertigt seit 1945 Strom- und Spannungswandler für Netze, Industrie und Bahn. Unser Entwurf führt Unternehmensseite und Produktfinder zusammen – für Kunden in 60 Ländern.",
        "facts": [["Kunde", "RITZ Instrument Transformers"], ["Branche", "Industrie und Energietechnik"], ["Leistungen", "Konzept, Design, Entwicklung, Produktfinder"], ["Status", "Entwurf"]],
        "nums": [["1.500+", "Mitarbeitende"], ["60", "Länder mit Vertretung"]], "nums_label": "Der Kunde",
        "url": "https://ritz.entwurf.medialyte.de/", "host": "ritz.entwurf.medialyte.de", "visit": "Entwurf ansehen",
    },
}

FAQ_MAIN = [
    ("Was kostet eine Website bei Medialyte?",
     "<p>Jedes Angebot besteht aus zwei Teilen: einer einmaligen Pauschale für Konzept, Design und Entwicklung und einem monatlichen Abo für Hosting, Pflege, KI-Agent und Support. Wie hoch beides ist, hängt davon ab, was Ihr Betrieb braucht.</p><p>Nach dem kostenfreien Erstgespräch erhalten Sie innerhalb von 48 Stunden ein Angebot – transparent und ohne versteckte Kosten.</p>"),
    ("Wie lange dauert ein Projekt?",
     "<p>Eine übersichtliche Website ist meist in zwei bis vier Wochen online. Projekte mit eigenem Kundenmanagement-System brauchen sechs bis zwölf Wochen. Sie kennen jeden Meilenstein vorab.</p>"),
    ("Wie ändere ich später etwas auf meiner Website?",
     "<p>Bei einfacheren Websites, etwa in der Gastronomie, schreiben Sie dem KI-Agenten per WhatsApp, was sich ändern soll. Bei umfangreichen Systemen, etwa der Mandantenverwaltung einer Kanzlei, erledigen Sie Änderungen direkt in Ihrem eigenen Dashboard. Größere Wünsche setzt unser Team um.</p>"),
    ("Was genau ist der KI-Agent?",
     "<p>Ihr digitaler Helfer für Website und System. Er nimmt Änderungswünsche entgegen, pflegt Öffnungszeiten, Preise, Texte und Bilder ein und hält Ihre Seite aktuell. Für Planung, Gestaltung und neue Funktionen ist unser Team persönlich für Sie da.</p>"),
    ("Werde ich nach dem Livegang betreut?",
     "<p>Ja. Pflege, Wartung, Updates und Support sind Teil Ihres Abos. Wir überwachen die Technik, halten alles aktuell und sind erreichbar, wenn Sie uns brauchen.</p>"),
    ("Für welche Branchen arbeiten Sie?",
     "<p>Für Betriebe jeder Branche in ganz Deutschland: Gastronomie, Handwerk, Handel, Kanzleien, Praxen, Dienstleister, Industrie und Vereine. Entscheidend ist nicht die Branche, sondern dass Ihre Website mehr für Sie tun soll.</p>"),
    ("Arbeiten Sie nur in Hamburg?",
     "<p>Nein. Unser Sitz ist in Hamburg, unsere Kunden sitzen in ganz Deutschland. Wir arbeiten per Video-Call, Telefon und WhatsApp – in Hamburg gern auch persönlich.</p>"),
    ("Lohnt sich ein Neustart, wenn ich schon eine Website habe?",
     "<p>Oft ja – besonders, wenn die Seite langsam lädt, auf dem Smartphone schlecht aussieht oder kaum Anfragen bringt. Im Erstgespräch schauen wir sie uns an und sagen Ihnen ehrlich, ob sich eine Überarbeitung oder ein Neustart mehr lohnt.</p>"),
    ("Kann ich Inhalte auch selbst bearbeiten?",
     "<p>Ja. Am einfachsten schreiben Sie dem KI-Agenten per WhatsApp, was sich ändern soll – das geht meist schneller, als es selbst zu machen. Haben Sie ein eigenes Dashboard, ändern Sie Texte, Bilder und Preise dort auch direkt selbst, ganz ohne Technikkenntnisse.</p>"),
    ("Was bedeutet die Zufriedenheitsgarantie?",
     "<p>Sie sehen jeden Entwurf, bevor wir ihn umsetzen, und geben jede Seite frei, bevor sie online geht. Passt etwas nicht, überarbeiten wir es – so lange, bis Sie zufrieden sind.</p><p>Was genau dazugehört, steht schriftlich in Ihrem Angebot.</p>"),
]


# ======================================================================= Kleine Bausteine
def sh(title, lead="", split=False, center=False, more="", tag="h2"):
    cls = "sh" + (" sh--split" if split else "") + (" sh--center" if center else "")
    ld = f'<p class="lead">{lead}</p>' if lead else ""
    mr = f'<div class="sh__more">{more}</div>' if more else ""
    return f'<div class="{cls}" data-reveal><{tag} class="h2">{title}</{tag}>{ld}{mr}</div>'


def ticks(items, cls=""):
    c = f" {cls}" if cls else ""
    return f'<ul class="ticks{c}">' + "".join(f"<li>{icon('check')}<span>{i}</span></li>" for i in items) + "</ul>"


def img(ctx, src, w, h, alt, cls="", lazy=True, sizes="", srcset="", style=""):
    extra = ""
    if srcset:
        extra += f' srcset="{srcset}" sizes="{sizes}"'
    extra += ' loading="lazy" decoding="async"' if lazy else ' fetchpriority="high" decoding="async"'
    c = f' class="{cls}"' if cls else ""
    s = f' style="{style}"' if style else ""
    return f'<img{c} src="{ctx.a(src)}" width="{w}" height="{h}" alt="{e(alt)}"{extra}{s}>'


def book_link(ctx, ask=""):
    if ctx.path == "/":
        return ctx.u("/#termin")
    return ctx.u("/termin/" + (f"?anliegen={ask}" if ask else ""))


def btn_book(ctx, text="Erstgespräch buchen", ask="", cls="btn--primary"):
    data = f' data-ask="{ask}"' if ask and ctx.path == "/" else ""
    return f'<a class="btn {cls}" href="{book_link(ctx, ask)}"{data}>{text}</a>'


def btn_wa(ctx, text="Per WhatsApp schreiben", cls="btn--ghost"):
    return f'<a class="btn {cls}" href="{SITE["wa"]}" target="_blank" rel="noopener">{icon("wa")} {text}</a>'


def _logo_h(f):
    """Optischer Ausgleich: breite Schriftzüge kleiner, kompakte Zeichen größer."""
    w, h = _LOGO_DIMS[f]
    return max(20, min(50, round(40 * (3.0 / (w / h)) ** 0.5)))


def marquee_rows(ctx, rows=1):
    """Logo-Laufband. Mehrere Reihen laufen gegeneinander und beginnen an verschiedenen Stellen,
    so wirkt die Auswahl größer, als wenn alle Logos auf einmal nebeneinander stehen."""
    def one_set(order, hidden=False):
        imgs = "".join(
            f'<img src="{ctx.a("img/logos/" + f + ".webp")}" width="{_LOGO_DIMS[f][0]}" height="{_LOGO_DIMS[f][1]}" style="--h:{_logo_h(f)}px" alt="{"" if hidden else e(a)}" loading="lazy" decoding="async">'
            for f, a in order)
        aria = ' aria-hidden="true"' if hidden else ""
        return f'<div class="marquee__set"{aria}>{imgs}</div>'
    out = ""
    for r in range(rows):
        # jede weitere Reihe beginnt etwa in der Mitte der Liste: oben und unten stehen nie dieselben Logos
        k = ((len(LOGOS) + 1) // 2 * r) % len(LOGOS)
        order = LOGOS[k:] + LOGOS[:k]
        cls = "marquee" + (" marquee--rev" if r % 2 else "")
        # Nur die erste Reihe wird vorgelesen, weitere Reihen sind Wiederholungen
        hide = r > 0
        out += f'<div class="{cls}" data-marquee{" aria-hidden=\"true\"" if hide else ""}><div class="marquee__track">{one_set(order, hide)}{one_set(order, True)}</div></div>'
    return f'<div class="marquees{" marquees--multi" if rows > 1 else ""}">{out}</div>'


def logo_marquee(ctx, label="Kunden und Partner von Medialyte"):
    return f"""
<section class="logos" aria-label="{e(label)}">
  <p class="logos__label">{e(label)}</p>
  {marquee_rows(ctx, 1)}
</section>"""


def closing(ctx, title="Bereit für eine Website, die Kunden bringt?", quiet="Wir freuen uns auf Ihr Projekt.",
            lead="Im kostenfreien Erstgespräch schauen wir uns Ihren Betrieb an und sagen Ihnen, was sich lohnt. Ihr Angebot erhalten Sie innerhalb von 48 Stunden."):
    q = f' <span class="quiet">{quiet}</span>' if quiet else ""
    return f"""
<section class="closing">
  <div class="wrap" data-reveal>
    <h2 class="display">{title}{q}</h2>
    <p class="lead">{lead}</p>
    <div class="closing__actions">{btn_book(ctx, cls='btn--primary btn--lg')}{btn_wa(ctx, cls='btn--ghost btn--lg')}</div>
  </div>
</section>"""


# ======================================================================= Die Idee (3V)
# Die Idee: drei Säulen, jede mit Nutzen, Leistungen und einer Frage zum Selbstcheck.
# (Schlüssel, Säule, Farbe, Titel, Text, Leistungen, Frage, Antwort „passt“, Antwort „Hebel“, Anliegen für die Buchung)
IDEA = [
    ("vermehrung", "Vermehrung", "ads", "Neue Kunden gewinnen",
     "Damit die richtigen Menschen Sie finden: eine Website, die bei Google gefunden wird, und Werbung, die genau Ihre Zielgruppe erreicht.",
     [("/leistungen/website-erstellung/", "Website-Erstellung"), ("/leistungen/online-marketing/", "Online-Marketing")],
     "Kommen genug neue Anfragen über Ihre Website?", "Ja, genug", "Zu wenige", ["werbung", "web-besser"]),
    ("verbesserung", "Verbesserung", "ai", "Kunden überzeugen und halten",
     "Ein Auftritt, der Vertrauen schafft, und Informationen, die immer stimmen. Der KI-Agent hält Ihre Seite aktuell – per WhatsApp.",
     [("/leistungen/website-erstellung/", "Website-Erstellung"), ("/leistungen/ki-agent/", "KI-Agent")],
     "Ist Ihre Website aktuell – auch auf dem Handy?", "Ja", "Eher nicht", ["web-besser", "agent"]),
    ("verwaltung", "Verwaltung", "crm", "Alles an einem Ort",
     "Anfragen, Termine, Angebote und Aufträge laufen in Ihrem eigenen System zusammen. Nichts geht verloren, Ihr Team sieht, was zu tun ist.",
     [("/leistungen/kundenmanagement-system/", "Kundenmanagement-System")],
     "Landen alle Anfragen an einem Ort?", "Ja", "Nein, verstreut", ["system"]),
]

# Kleine Bilder je Säule (gezeichnet, keine Fotos)
_PILLAR_VIS = {
    "vermehrung": '<span class="pv pv--bars" aria-hidden="true">' + "".join(f'<i style="--h:{h}%;--d:{i}"></i>' for i, h in enumerate([26, 34, 31, 48, 57, 72, 94])) + '<b>Anfragen</b></span>',
    "verbesserung": ('<span class="pv pv--site" aria-hidden="true"><span class="pv__win"><span class="pv__bar"><i></i><i></i><i></i></span>'
                     '<span class="pv__line"></span><span class="pv__line pv__line--s"></span>'
                     '<span class="pv__row"><span>Öffnungszeiten</span><em>Aktualisiert</em></span></span>'
                     '<span class="pv__msg">Ab Montag: 8–18 Uhr</span></span>'),
    "verwaltung": ('<span class="pv pv--flow" aria-hidden="true"><span class="pv__src"><i>Website</i><i>WhatsApp</i><i>Telefon</i></span>'
                   '<svg viewBox="0 0 60 88" preserveAspectRatio="none"><path d="M0 12 C30 12 30 44 60 44 M0 44 H60 M0 76 C30 76 30 44 60 44"/></svg>'
                   '<span class="pv__hub">Dashboard</span></span>'),
}


def idea(ctx):
    ICN = {"vermehrung": "trend", "verbesserung": "spark", "verwaltung": "inbox"}
    cards, dots = "", ""
    for i, (key, name, tone, h, text, uses, qn, ok, gap, asks) in enumerate(IDEA):
        tags = "".join(f'<li><a href="{ctx.u(p)}">{e(t)}</a></li>' for p, t in uses)
        dots += f'<i class="po__dot po__dot--{tone}" data-k="{key}" title="{name}"></i>'
        cards += f"""
<article class="pillar pillar--{tone}" data-pillar="{key}" data-name="{name}" data-asks="{','.join(asks)}" data-reveal style="--rd:{i}">
  <div class="pillar__vis">{_PILLAR_VIS[key]}</div>
  <div class="pillar__body">
    <span class="pillar__name"><span class="ic ic--sm ic--{tone}">{icon(ICN[key])}</span>{name}</span>
    <h3>{h}</h3>
    <p>{text}</p>
    <ul class="tags">{tags}</ul>
  </div>
  <div class="pillar__check" role="group" aria-labelledby="pq-{key}">
    <span class="pillar__q" id="pq-{key}">{qn}</span>
    <span class="pillar__ans chips"><button type="button" class="chip" data-a="ok" aria-pressed="false">{ok}</button><button type="button" class="chip" data-a="gap" aria-pressed="false">{gap}</button></span>
  </div>
</article>"""
    return f"""
<div class="pillars" data-pillars>{cards}
</div>
<div class="po" data-pillars-out data-reveal>
  <span class="po__dots" aria-hidden="true">{dots}</span>
  <p class="po__text" data-po-text aria-live="polite"><b>Wo liegt Ihr größter Hebel?</b> <span>Beantworten Sie die drei Fragen oben – das Ergebnis nehmen wir direkt ins Erstgespräch mit.</span></p>
  <a class="btn btn--primary" href="{book_link(ctx)}" data-po-cta data-ask="">Erstgespräch buchen</a>
</div>"""


# ======================================================================= Kundenreise (Leistungen)
STATIONS = [
    ("Website", "Eine Website, die für Ihre Kunden gemacht ist",
     "Wir finden heraus, wer Ihre Kunden sind und was sie wissen wollen – und bauen die Website genau dafür. Schnell, klar und auf dem Smartphone so gut wie am Rechner. Mit einem kurzen Weg zu Anruf, Termin oder Anfrage.",
     ["Individuelles Design statt Vorlage", "Texte, die Ihre Kunden überzeugen", "Bei Google gut auffindbar", "Hosting, Domain und SSL inklusive"],
     "/leistungen/website-erstellung/", "Mehr zur Website-Erstellung", "relaunch", "Beispiel: So wird aus einer alten Seite eine, die Anfragen bringt."),
    ("Kundensystem", "Ein System, in dem jede Anfrage landet",
     "Hinter der Website bauen wir Ihr eigenes Kunden- oder Produktmanagement. Anfragen, Termine, Angebote und Aufträge laufen an einem Ort zusammen – für Sie und Ihr Team, auch unterwegs.",
     ["Eigenes Dashboard statt Excel und Zettelwirtschaft", "Direkt mit Ihrer Website verbunden", "Erinnerungen und Abläufe automatisiert", "Wächst mit Ihrem Betrieb"],
     "/leistungen/kundenmanagement-system/", "Mehr zum Kundenmanagement-System", "pipeline", "Beispiel: Anfragen wandern von „Neu“ bis „Auftrag“. Tippen Sie eine Karte an, um sie weiterzuschieben."),
    ("KI-Agent", "Ändern Sie Ihre Website per WhatsApp",
     "Neue Öffnungszeiten, ein anderes Gericht, frische Fotos: Sie schreiben es unserem KI-Agenten, er pflegt es ein. Bei umfangreichen Systemen erledigen Sie dasselbe direkt im Dashboard. Für Größeres ist unser Team persönlich da.",
     ["Änderungen in eigenen Worten, ohne Technik", "Bei einfachen Websites per WhatsApp", "Bei großen Systemen direkt im Dashboard", "Laufende Pflege inklusive"],
     "/leistungen/ki-agent/", "Mehr zum KI-Agenten", "agent", "Wählen Sie eine Nachricht – der Agent setzt sie auf der Beispiel-Website um."),
    ("Werbung", "Werbung, die Anfragen bringt – nicht nur Klicks",
     "Wenn das Fundament steht, bringen wir gezielt neue Kunden auf Ihre Seite: mit Google Ads, Social Media und Landingpages. Aus über 200 Kampagnen wissen wir, worauf es ankommt.",
     ["Google Ads und Social-Media-Kampagnen", "Landingpages für Ihre wichtigsten Angebote", "SEO und lokale Sichtbarkeit", "Messbar: Anfragen, Anrufe, Buchungen"],
     "/leistungen/online-marketing/", "Mehr zum Online-Marketing", "campaign", "Beispiel: Anzeige bei Google und die Kampagne dahinter."),
]


def journey(ctx):
    """Kundenreise in vier Stationen. Auf großen Bildschirmen macht das Skript daraus eine angeheftete Bühne
    mit Leiste und Überblendung; sonst (mobil, ohne Skript, reduzierte Bewegung) stehen die Stationen untereinander."""
    vis = {"relaunch": mocks.relaunch, "pipeline": mocks.pipeline, "agent": mocks.agent_demo, "campaign": mocks.campaign}
    n = len(STATIONS)
    rail = "".join(
        f'<button class="jr__step{" is-on" if i == 0 else ""}" type="button" id="jr-t{i}" aria-controls="st-{i}" aria-selected="{"true" if i == 0 else "false"}" tabindex="{0 if i == 0 else -1}" data-go="{i}">'
        f'<span class="jr__n" aria-hidden="true">{i + 1}</span>{name}</button>'
        for i, (name, *_rest) in enumerate(STATIONS))
    out = ""
    for i, (name, h, text, items, link, link_t, v, cap) in enumerate(STATIONS):
        out += f"""
<div class="st{" is-active" if i == 0 else ""}" id="st-{i}" role="group" data-station="{i}" aria-labelledby="st-h{i}">
  <div class="st__text">
    <span class="st__name"><span class="jr__n" aria-hidden="true">{i + 1}</span>{name}</span>
    <h3 id="st-h{i}">{h}</h3>
    <p>{text}</p>
    {ticks(items)}
    <a class="link" href="{ctx.u(link)}">{link_t} {icon('arrow')}</a>
  </div>
  <div class="st__vis"><div class="st__fit">{vis[v]()}<p class="st__cap">{cap}</p></div></div>
</div>"""
    return f"""<div class="journey" data-journey style="--n:{n}">
  <div class="jr__stage">
    <div class="jr__rail" hidden aria-label="Stationen der Kundenreise">{rail}<span class="jr__bar" aria-hidden="true"><i></i></span></div>
    <div class="jr__stations">{out}
    </div>
  </div>
</div>"""


# ======================================================================= Referenzen
def cases(ctx, keys=("rechnungsradar", "rubin", "ritz")):
    out = ""
    for k in keys:
        r = REFS[k]
        lh = _REFS_META[k]["long_h"]
        facts = "".join(f"<div><b>{e(v)}</b><small>{e(l)}</small></div>" for v, l in r["nums"])
        out += f"""
<article class="case" data-reveal>
  <button class="case__media" type="button" data-ref="{k}" aria-haspopup="dialog" aria-label="Vorschau öffnen: {e(r['title'])}">
    <span class="frame case__browser"><span class="frame__bar"><i></i><i></i><i></i><span class="frame__url">{icon('lock')}{e(r['host'])}</span></span>
      <span class="case__shot" data-scrub><img src="{ctx.a('img/refs/' + k + '-long.webp')}" srcset="{ctx.a('img/refs/' + k + '-long-sm.webp')} 640w, {ctx.a('img/refs/' + k + '-long.webp')} 1200w" sizes="(max-width: 900px) 92vw, 760px" width="1200" height="{lh}" alt="Website {e(r['title'])}" loading="lazy" decoding="async"></span></span>
    <span class="phone case__phone"><span class="phone__screen">{img(ctx, 'img/refs/' + k + '-mobile.webp', 600, 1299, '')}</span></span>
    <span class="case__open">{icon('eye')} Vorschau öffnen</span>
  </button>
  <div class="case__text">
    <span class="case__cat">{e(r['cat'])}</span>
    <h3>{e(r['h'])}</h3>
    <p>{e(r['text'])}</p>
    <div class="case__facts"><small class="case__facts-l">{e(r['nums_label'])}</small>{facts}</div>
    <div class="case__actions"><button class="btn btn--light btn--sm" type="button" data-ref="{k}">Vorschau öffnen</button><a class="btn btn--ghost btn--sm" href="{r['url']}" target="_blank" rel="noopener">{e(r['visit'])} {icon('out')}</a></div>
  </div>
</article>"""
    return f'<div class="cases">{out}</div>'


def ref_dialog(ctx):
    data = {}
    for k, r in REFS.items():
        data[k] = {
            "title": r["title"], "cat": r["cat"], "text": r["text"], "facts": r["facts"], "nums": r["nums"], "numsLabel": r["nums_label"],
            "url": r["url"], "visit": r["visit"], "host": r["host"],
            "desktop": ctx.a(f"img/refs/{k}-full.webp"), "mobile": ctx.a(f"img/refs/{k}-mobile-full.webp"),
            "desktopH": _REFS_META[k]["full_h"], "mobileH": _REFS_META[k]["mobile_full_h"],
        }
    return f"""
<dialog class="rd" id="ref-dialog" aria-labelledby="rd-title">
  <div class="rd__in">
    <button class="rd__close" type="button" aria-label="Vorschau schließen">{icon('x')}</button>
    <div class="rd__stage">
      <div class="rd__bar">
        <div class="chips" role="group" aria-label="Ansicht wählen">
          <button class="chip" type="button" data-view="desktop" aria-pressed="true">{icon('monitor')}Desktop</button>
          <button class="chip" type="button" data-view="mobile" aria-pressed="false">{icon('mobile')}Smartphone</button>
        </div>
        <span class="rd__hint">Scrollen Sie durch die ganze Seite</span>
      </div>
      <div class="rd__view">
        <div class="frame rd__frame">
          <div class="frame__bar"><i></i><i></i><i></i><span class="frame__url">{icon('lock')}<span data-rd="host"></span></span></div>
          <div class="rd__scroll" tabindex="0"><img src="data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==" alt="" width="1200" height="1200" decoding="async"></div>
        </div>
      </div>
    </div>
    <div class="rd__info">
      <span class="rd__cat" data-rd="cat"></span>
      <h2 id="rd-title" data-rd="title">Projekt</h2>
      <p data-rd="text"></p>
      <div class="rd__nums" data-rd="nums"></div>
      <div class="rd__actions">
        <a class="btn btn--light" href="#" target="_blank" rel="noopener" data-rd="link"><span>Website besuchen</span> {icon('out')}</a>
        <a class="btn btn--ghost" href="{book_link(ctx)}" data-close-dialog>Ähnliches Projekt anfragen</a>
      </div>
      <dl class="rd__facts" data-rd="facts"></dl>
    </div>
  </div>
</dialog>
<script type="application/json" id="refs-data">{json.dumps(data, ensure_ascii=False)}</script>"""


# ======================================================================= Ergebnisse
# Ergebnis nach dem Relaunch: die vier echten Kennzahlen von RechnungsRadar, je Zeile vorher und nachher.
# Balken je Kennzahl auf den größeren Wert bezogen (vorher = 100): 330, 33, 173 und 85.
IMPACT = [("Kundenanfragen", "+", 230, 30.3, 100), ("Absprungrate", "−", 67, 100, 33),
          ("Conversionrate", "+", 73, 57.8, 100), ("Marketingkosten", "−", 15, 100, 85)]


def impact(ctx):
    rows = "".join(f"""
    <li class="impact__row" style="--i:{i}"><span class="impact__k">{k}</span><b class="impact__v">{sign}<span data-count="{v}">{v}</span> %</b>
      <span class="impact__bars" aria-hidden="true"><span class="impact__bar"><small>vorher</small><i style="--w:{b0}%"></i></span><span class="impact__bar impact__bar--after"><small>nachher</small><i style="--w:{b1}%"></i></span></span></li>"""
        for i, (k, sign, v, b0, b1) in enumerate(IMPACT))
    return f"""
<div class="impact">
  <div class="impact__h"><span class="impact__brand">{img(ctx, 'img/logos/rechnungsradar.webp', _LOGO_DIMS['rechnungsradar'][0], _LOGO_DIMS['rechnungsradar'][1], 'RechnungsRadar')}</span><span class="badge">Nach dem Relaunch</span></div>
  <ul class="impact__rows" role="list">{rows}
  </ul>
</div>"""


def results(ctx):
    return f"""
<div class="res">
  <div data-reveal>{impact(ctx)}</div>
  <figure class="quote" data-reveal style="--rd:1">
    <svg class="quote__mark" viewBox="0 0 40 30" aria-hidden="true"><path fill="currentColor" d="M0 30V17.6C0 7.9 5.3 1.6 15.9 0l1.6 4.3C11.6 5.9 8.6 9.1 8.3 14h7.3v16zm22.4 0V17.6c0-9.7 5.3-16 15.9-17.6L40 4.3C34 5.9 31 9.1 30.7 14H38v16z"/></svg>
    <blockquote>
      <p>Dank Medialyte hat meine Website für RechnungsRadar einen echten Qualitätssprung gemacht. Aus einer eher schlichten Seite ist ein professioneller Auftritt geworden, der Vertrauen schafft.</p>
      <p>Seitdem erreichen mich deutlich mehr Anfragen von Steuerberatern. Die Zusammenarbeit war reibungslos, schnell und absolut zuverlässig – sehr empfehlenswert!</p>
    </blockquote>
    <figcaption>{img(ctx, 'img/logos/avatar-rechnungsradar.svg', 48, 48, 'Logo RechnungsRadar')}<span><b>Hannes Diedrichsen</b><small>Gründer von RechnungsRadar</small></span></figcaption>
  </figure>
</div>
<p class="deltas__note">Veränderung bei RechnungsRadar nach dem Relaunch, im Vergleich zur vorherigen Website.</p>"""


# ======================================================================= Vergleich
def compare():
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
<div data-reveal>
  <div class="cmp-tabs chips" role="group" aria-label="Vergleich wählen"><button class="chip" type="button" data-vs="agentur" aria-pressed="true">vs. Agentur</button><button class="chip" type="button" data-vs="baukasten" aria-pressed="false">vs. Baukasten</button></div>
  <div class="cmp-wrap"><table class="cmp" data-vs="agentur">
    <caption class="sr-only">Vergleich: Medialyte, klassische Agentur und Website-Baukasten</caption>
    <thead><tr><th scope="col">Typischer Vergleich</th><th scope="col" class="is-us">Medialyte</th><th scope="col">Klassische Agentur</th><th scope="col">Website-Baukasten</th></tr></thead>
    <tbody>{body}</tbody>
  </table></div>
  <p class="cmp-note">Typische Merkmale. Im Einzelfall kann das je nach Anbieter abweichen.</p>
</div>"""


# ======================================================================= Pakete und Paket-Finder
PLANS = [
    ("praesenz", "Präsenz", "Für Betriebe ohne Website oder mit einer, die nicht mehr zu ihnen passt.",
     ["Analyse Ihrer Zielgruppe", "Design und Texte, individuell für Sie", "Schnell, mobil und bei Google auffindbar", "Domain, Hosting und SSL", "Änderungen per WhatsApp über den KI-Agenten", "Wartung und persönlicher Support"],
     "web-neu,agent"),
    ("wachstum", "Wachstum", "Für Betriebe, die gezielt neue Kunden gewinnen wollen.",
     ["Alles aus Präsenz", "Google Ads und Social-Media-Kampagnen", "Landingpages für Ihre wichtigsten Angebote", "SEO und lokale Sichtbarkeit", "Messung von Anfragen, Anrufen und Buchungen", "Monatlicher Bericht und laufende Optimierung"],
     "web-neu,werbung"),
    ("system", "System", "Für Betriebe mit vielen Kunden, Aufträgen oder Produkten.",
     ["Alles aus Präsenz", "Eigenes Kunden- oder Produktmanagement", "Dashboard für Anfragen, Termine und Aufträge", "Automatisierte Abläufe und Erinnerungen", "KI-Agent direkt im Dashboard", "Einweisung für Ihr Team"],
     "system"),
]
FINDER = {
    "branche": [("gastro", "ein Restaurant oder Café", "Gastronomie & Hotellerie"), ("handwerk", "ein Handwerksbetrieb", "Handwerk & Bau"),
                ("praxis", "eine Praxis", "Praxis & Gesundheit"), ("kanzlei", "eine Kanzlei", "Kanzlei & Beratung"),
                ("handel", "ein Händler", "Einzelhandel & E-Commerce"), ("dienst", "ein Dienstleister", "Dienstleistung"),
                ("industrie", "ein Industriebetrieb", "Industrie & Technik"), ("verein", "ein Verein", "Verein & Organisation")],
    "web": [("ohne", "ohne Website"), ("alt", "mit veralteter Website"), ("gut", "mit guter Website")],
    "ziel": [("gefunden", "gefunden werden"), ("anfragen", "mehr Anfragen"), ("verwaltung", "weniger Verwaltungsaufwand")],
}


# Ein Satz je Branche und Paket: Was die Empfehlung für genau diesen Betrieb bedeutet
FINDER_FIT = {
    "gastro": {"praesenz": "Für Ihr Restaurant heißt das: Speisekarte und Öffnungszeiten stimmen immer, reserviert wird mit einem Tipp.",
               "wachstum": "Für Ihr Restaurant heißt das: Anzeigen für Gäste in der Nähe und Reservierungen direkt über die Website.",
               "system": "Für Ihr Restaurant heißt das: Reservierungen, Gästewünsche und Veranstaltungen an einem Ort."},
    "handwerk": {"praesenz": "Für Ihren Betrieb heißt das: Projekte zeigen und Anfragen gleich mit Fotos bekommen.",
                 "wachstum": "Für Ihren Betrieb heißt das: Anfragen aus Ihrer Region – mit Fotos und allen Angaben.",
                 "system": "Für Ihren Betrieb heißt das: Anfragen, Aufmaß-Termine, Angebote und Aufträge in einem Dashboard."},
    "praxis": {"praesenz": "Für Ihre Praxis heißt das: Sprechzeiten, die immer stimmen, und Online-Termine rund um die Uhr.",
               "wachstum": "Für Ihre Praxis heißt das: neue Patientinnen und Patienten aus der Umgebung, die direkt online buchen.",
               "system": "Für Ihre Praxis heißt das: Termine, Erinnerungen und Unterlagen digital an einem Ort."},
    "kanzlei": {"praesenz": "Für Ihre Kanzlei heißt das: Schwerpunkte klar erklärt und die Erstberatung in wenigen Klicks angefragt.",
                "wachstum": "Für Ihre Kanzlei heißt das: Mandantinnen und Mandanten, die genau Ihre Schwerpunkte suchen.",
                "system": "Für Ihre Kanzlei heißt das: Mandate, Fristen und Unterlagen in Ihrer eigenen Mandantenverwaltung."},
    "handel": {"praesenz": "Für Ihr Geschäft heißt das: Sortiment, Öffnungszeiten und Aktionen sind immer aktuell.",
               "wachstum": "Für Ihr Geschäft heißt das: mehr Besucher im Laden und im Online-Shop.",
               "system": "Für Ihr Geschäft heißt das: Produkte, Bestände und Bestellungen zentral gepflegt."},
    "dienst": {"praesenz": "Für Ihr Unternehmen heißt das: Leistungen klar erklärt und ein kurzer Weg zur Anfrage.",
               "wachstum": "Für Ihr Unternehmen heißt das: Anfragen genau von den Kunden, die Sie suchen.",
               "system": "Für Ihr Unternehmen heißt das: Anfragen, Termine und Aufträge an einem Ort."},
    "industrie": {"praesenz": "Für Ihr Unternehmen heißt das: ein Auftritt, der Kunden und Bewerber gleichermaßen überzeugt.",
                  "wachstum": "Für Ihr Unternehmen heißt das: Anfragen von Einkäufern und Planern, auch international.",
                  "system": "Für Ihr Unternehmen heißt das: Produktdaten und Anfragen zentral – wie beim Produktfinder für RITZ."},
    "verein": {"praesenz": "Für Ihren Verein heißt das: Termine, Neuigkeiten und Mitgliedsanträge an einem Ort.",
               "wachstum": "Für Ihren Verein heißt das: neue Mitglieder, Unterstützer und Spenden.",
               "system": "Für Ihren Verein heißt das: Mitglieder, Termine und Beiträge übersichtlich verwaltet."},
}


def plans(ctx):
    def sel(name, opts, default):
        o = "".join(f'<option value="{v}"{" selected" if v == default else ""}>{t}</option>' for v, t, *_ in opts)
        label = {"branche": "Ihr Betrieb", "web": "Ihre Website", "ziel": "Ihr wichtigstes Ziel"}[name]
        shown = [t for v, t, *_ in opts if v == default][0]
        return f'<span class="finder__sel"><span class="finder__val" aria-hidden="true">{shown}</span><select name="{name}" aria-label="{label}">{o}</select></span>'
    bmap = {v: b for v, _, b in FINDER["branche"]}
    cards = ""
    for key, name, who, items, ask in PLANS:
        cards += f"""
<article class="plan" data-plan="{key}">
  <div class="plan__head"><div class="plan__name"><h3>{name}</h3><span class="badge plan__match">Passt zu Ihnen</span></div><p class="plan__for">{who}</p></div>
  {ticks(items)}
  <div></div>
  <div class="plan__foot">
    <div class="plan__price"><b>Pauschale + monatliches Abo</b><small>Ihr Preis steht in Ihrem persönlichen Angebot</small></div>
    {btn_book(ctx, name + ' anfragen', ask, 'btn--ghost btn--block')}
  </div>
</article>"""
    return f"""
<form class="finder" data-finder data-reveal onsubmit="return false" data-branchen="{e(json.dumps(bmap, ensure_ascii=False))}" data-fit="{e(json.dumps(FINDER_FIT, ensure_ascii=False))}">
  <p class="finder__q">Wir sind {sel('branche', FINDER['branche'], 'gastro')} {sel('web', FINDER['web'], 'alt')} und wollen vor allem {sel('ziel', FINDER['ziel'], 'anfragen')}.</p>
  <div class="finder__out" aria-live="polite">
    <div class="finder__res"><small>Unsere Empfehlung</small><b data-fr="name">Wachstum</b><p data-fr="why">Eine Website, die überzeugt, und Kampagnen, die gezielt neue Anfragen bringen – messbar bis zur Buchung.</p><p class="finder__fit" data-fr="fit">{FINDER_FIT["gastro"]["wachstum"]}</p></div>
    <a class="btn btn--primary" href="{book_link(ctx)}" data-fr="cta">Erstgespräch mit dieser Auswahl</a>
  </div>
</form>
<div class="plans" data-plans>{cards}</div>
<div class="plans-note" data-reveal><span>{icon('check')} Kostenfreies Erstgespräch</span><span>{icon('check')} Angebot innerhalb von 48 Stunden</span><span>{icon('check')} Pakete frei kombinierbar</span><a href="#faq-garantie" data-faq-link>{icon('check')} Zufriedenheitsgarantie</a></div>"""


# ======================================================================= Ablauf
PROCESS = [
    ("Strategische Analyse", "Wir lernen Ihren Betrieb kennen: Ihre Kunden, Ihre Mitbewerber, Ihre Ziele. Daraus entsteht der Plan.", ["Zielgruppe", "Wettbewerb", "Ziele"]),
    ("Konzept und Design", "Sie sehen früh, wie alles aussehen wird, und entscheiden mit. Wir verfeinern, bis es passt.", ["Struktur", "Entwurf", "Texte"]),
    ("Entwicklung", "Wir setzen Website und System um: schnell, sicher und so, dass beides mit Ihrem Betrieb wachsen kann.", ["Website", "System", "Anbindungen"]),
    ("Test und Feinschliff", "Jede Seite, jedes Formular, jedes Gerät: Wir prüfen alles, bevor Ihre Kunden es sehen.", ["Funktion", "Tempo", "Alle Geräte"]),
    ("Livegang und Betreuung", "Ihre Lösung geht online. Danach bleiben wir an Ihrer Seite – mit unserem Team und dem KI-Agenten.", ["Livegang", "Pflege", "Service"]),
]


def process(items=None, cls=""):
    items = items or PROCESS
    lis = "".join(
        f'<li class="proc__item" data-reveal style="--rd:{i}"><span class="num">{i + 1}</span><h3>{t}</h3><p>{d}</p>'
        + (f'<ul class="tags">{"".join(f"<li>{x}</li>" for x in tags)}</ul>' if tags else "") + "</li>"
        for i, (t, d, tags) in enumerate(items))
    return f'<ol class="proc{(" " + cls) if cls else ""}" data-proc style="--n:{len(items)}"><li class="proc__line" aria-hidden="true"><i></i></li>{lis}</ol>'


# ======================================================================= Film (Platzhalter)
# Kapitel des Films: Startzeit in Sekunden (Szenengrenzen aus film/chapters.py), Titel, kurze Beschreibung
FILM_CHAPTERS = [
    (0, "Die Ausgangslage", "Warum viele Websites Kunden verlieren statt gewinnen"),
    (23.4, "Unser Ablauf", "Vom Erstgespräch über den Entwurf bis zum Livegang"),
    (48.7, "Der Unterschied", "Was Medialyte anders macht als eine klassische Agentur"),
    (69.8, "Ihr KI-Agent", "So bleiben Website und System ohne Aufwand aktuell"),
]
FILM_LENGTH = "1:41"


def film(ctx):
    """Der Erklärfilm: Vorschaubild mit großem Abspiel-Knopf, daneben die Kapitel – ein Klick springt an die Stelle.
    Ohne Skript bleibt der normale Videoplayer mit Bedienelementen."""
    def mmss(s):
        return f"{int(s) // 60}:{int(s) % 60:02d}"
    lis = "".join(
        f'<li><button type="button" class="film__ch{" is-on" if i == 0 else ""}" data-at="{at}" aria-pressed="{"true" if i == 0 else "false"}">'
        f'<span class="num">{i + 1}</span><b>{t}</b><time>{mmss(at)}</time><span>{d}</span></button></li>'
        for i, (at, t, d) in enumerate(FILM_CHAPTERS))
    return f"""
<div class="film" data-film>
  <div class="film__frame" data-reveal="scale">
    <video class="film__video" controls preload="none" playsinline poster="{ctx.a('video/medialyte-film.webp')}" width="1920" height="1080"
      aria-label="Film: Medialyte in {FILM_LENGTH} Minuten, mit Untertiteln">
      <source src="{ctx.a('video/medialyte-film.mp4')}" type="video/mp4">
      <source src="{ctx.a('video/medialyte-film.webm')}" type="video/webm">
      <track kind="captions" srclang="de" label="Deutsch" default src="{ctx.a('video/medialyte-film.de.vtt')}">
    </video>
    <button class="film__play" type="button">
      <span class="film__btn">{icon('play')}</span><span class="film__lbl"><b>Film abspielen</b><small>{FILM_LENGTH} Min. · mit Ton und Untertiteln</small></span>
    </button>
  </div>
  <ol class="film__chapters" data-reveal aria-label="Kapitel des Films">{lis}</ol>
</div>"""


# Leistungsfilme (hochkant, eingebrannte Untertitel): Datei, Länge, Überschrift, Text, Punkte, Anliegen fürs Erstgespräch
SVC_FILMS = {
    "web": ("leistung-website-erstellung", "0:56", 'Erst Ihr Unternehmen, <span class="quiet">dann das Design.</span>',
            "Bevor wir gestalten, lernen wir Ihren Betrieb und Ihre Kunden kennen. Der Film zeigt am Beispiel einer Tischlerei, was daraus entsteht: eine Website, die genau die richtigen Kunden anspricht.",
            ["Wir arbeiten uns in Ihr Unternehmen ein", "Wir analysieren Ihre Zielgruppe ganz genau", "Ihre Website spricht die Sprache Ihrer Kunden"], "web-neu"),
    "sys": ("leistung-kundenmanagement", "0:54", 'Fünf Probleme, <span class="quiet">ein System.</span>',
            "Verstreute Anfragen, Angebote am Abend, Termine auf Zetteln: Der Film zeigt am Beispiel einer Tischlerei, wie ein eigenes System den Alltag ordnet.",
            ["Alle Anfragen an einem Ort", "Angebote mit wenigen Klicks", "Termine mit automatischer Bestätigung", "Erinnerungen und Briefe ganz von selbst", "Alle Zahlen auf einen Blick"], "system"),
    "agent": ("leistung-ki-agent", "0:45", 'Früher ein Auftrag, <span class="quiet">heute eine Nachricht.</span>',
              "Selbst im System einarbeiten oder die Agentur jede Änderung einzeln abrechnen lassen? Der Film zeigt, wie es mit dem KI-Agenten geht: per WhatsApp, in eigenen Worten.",
              ["Keine Fachbegriffe", "Kein Warten", "Keine Extrakosten: im Abo enthalten"], "agent"),
    "mkt": ("leistung-online-marketing", "0:53", 'Werbung, die nicht <span class="quiet">bei null beginnt.</span>',
            "Ihre Zielgruppe kennen wir schon aus der Analyse für Ihre Website. Der Film zeigt, warum Ihre Anzeigen deshalb die richtigen Menschen erreichen und Anfragen statt nur Klicks bringen.",
            ["Anzeigen bei Google und in den sozialen Medien", "Seiten, die für Ihre Zielgruppe gebaut sind", "Sie sehen, welche Anzeige wirklich Kunden bringt"], "werbung"),
}


def svc_film(ctx, key):
    """Leistungsfilm als eigener Abschnitt: Text links, hochkant abspielbarer Film rechts (gleicher Spieler wie der Erklärfilm)."""
    f, length, title, text, points, ask = SVC_FILMS[key]
    return f"""
<section class="section section--deep" id="film">
  <div class="wrap split split--film">
    <div class="split__text" data-reveal>
      <h2 class="h2">{title}</h2>
      <p>{text}</p>
      {ticks(points)}
      {btn_book(ctx, 'Erstgespräch buchen', ask)}
    </div>
    <div class="film film--v" data-film>
      <div class="film__frame film__frame--v" data-reveal="scale">
        <video class="film__video" controls preload="none" playsinline poster="{ctx.a(f'video/{f}.webp')}" width="720" height="1280"
          aria-label="Film, {length} Minuten, mit Ton und eingeblendeten Untertiteln">
          <source src="{ctx.a(f'video/{f}.mp4')}" type="video/mp4">
        </video>
        <button class="film__play" type="button">
          <span class="film__btn">{icon('play')}</span><span class="film__lbl"><b>Film abspielen</b><small>{length} Min. · mit Ton und Untertiteln</small></span>
        </button>
      </div>
    </div>
  </div>
</section>"""


# ======================================================================= Häufige Fragen
# Antworten, auf die an anderer Stelle verlinkt wird (z. B. „Zufriedenheitsgarantie“ im Startbereich)
FAQ_IDS = {"Was kostet eine Website bei Medialyte?": "faq-kosten", "Was bedeutet die Zufriedenheitsgarantie?": "faq-garantie"}


def faq_block(ctx, qas, title="Häufige Fragen", lead="Ihre Frage ist nicht dabei? Schreiben Sie uns per WhatsApp – wir antworten persönlich."):
    def item(i, q, a):
        attrs = (f' id="{FAQ_IDS[q]}"' if q in FAQ_IDS else "") + (" open" if i == 0 else "")
        return f'<details class="qa"{attrs}><summary>{e(q)}<span class="qa__ic" aria-hidden="true"></span></summary><div class="qa__a">{a}</div></details>'
    items = "".join(item(i, q, a) for i, (q, a) in enumerate(qas))
    return f"""
<div class="faq">
  <div class="faq__intro" data-reveal>
    <h2 class="h2">{title}</h2>
    <p class="lead">{lead}</p>
    {btn_wa(ctx, cls='btn--ghost')}
  </div>
  <div class="faq__list" data-faq data-reveal>{items}</div>
</div>"""


# ======================================================================= Terminbuchung
def booking_widget(ctx):
    demo = "0" if ctx.mode == "prod" else "1"

    TONES = {"web-neu": "web", "web-besser": "web", "system": "crm", "werbung": "ads", "agent": "ai"}

    def opt(name, value, ic, title, sub, typ="checkbox"):
        i = f"bk-{name}-{value}"
        tn = f" ic--{TONES[value]}" if name == "anliegen" and value in TONES else ""
        return f'<div class="opt"><input type="{typ}" name="{name}" value="{value}" id="{i}"><label for="{i}"><span class="ic{tn}">{icon(ic)}</span><b>{title}</b><small>{sub}</small></label></div>'

    def simple(name, value, text):
        i = f"bk-{name}-{value}"
        return f'<div class="opt opt--simple"><input type="radio" name="{name}" value="{value}" id="{i}"><label for="{i}"><b>{text}</b></label></div>'

    anliegen = "".join([
        opt("anliegen", "web-neu", "globe", "Neue Website", "Noch keine oder eine veraltete Website"),
        opt("anliegen", "web-besser", "trend", "Website verbessern", "Mehr Anfragen über Ihre Website"),
        opt("anliegen", "system", "db", "Kunden- oder Produktmanagement", "Eigenes System mit Dashboard"),
        opt("anliegen", "werbung", "mega", "Werbung und Online-Marketing", "Google Ads, Social Media, SEO"),
        opt("anliegen", "agent", "bot", "KI-Agent und Pflege", "Website aktuell halten ohne Aufwand"),
        opt("anliegen", "brief", "mail", "Brief von Medialyte erhalten", "Es gibt schon einen Entwurf für mich"),
    ])
    formate = "".join([
        opt("format", "video", "video", "Video-Call", "Bequem von überall", typ="radio"),
        opt("format", "telefon", "phone", "Telefon", "Wir rufen Sie an", typ="radio"),
        opt("format", "vor-ort", "pin", "Vor Ort", "Bei Ihnen, im Raum Hamburg", typ="radio"),
    ])
    branchen = ["Gastronomie & Hotellerie", "Handwerk & Bau", "Einzelhandel & E-Commerce", "Kanzlei & Beratung",
                "Praxis & Gesundheit", "Industrie & Technik", "Dienstleistung", "Immobilien", "Verein & Organisation", "Andere Branche"]
    bopts = '<option value="">Bitte wählen</option>' + "".join(f"<option>{e(b)}</option>" for b in branchen)
    groesse = "".join(simple("groesse", v, t) for v, t in [("1-5", "1–5"), ("6-20", "6–20"), ("21-100", "21–100"), ("100+", "über 100")])
    zeit = "".join(simple("zeitfenster", v, t) for v, t in [("vormittags", "Vormittags"), ("nachmittags", "Nachmittags"), ("flexibel", "Flexibel")])
    return f"""
<div class="bk" id="booking" data-demo="{demo}" data-endpoint="/api/termin.php" data-slots="/api/slots.php">
  <aside class="bk__aside">
    <div class="bk__host"><span class="ava" aria-hidden="true">{LOGO}</span><span><b>Medialyte</b><small>Ihr fester Ansprechpartner</small></span></div>
    <h3>Kostenfreies Erstgespräch</h3>
    <ul class="bk__meta">
      <li>{icon('clock')} 30 Minuten</li>
      <li>{icon('video')} Video-Call, Telefon oder im Raum Hamburg bei Ihnen vor Ort</li>
      <li>{icon('shield')} Unverbindlich und kostenfrei</li>
    </ul>
    <div class="bk__get"><b>Das erwartet Sie</b>{ticks(['Wir schauen uns Ihre Situation an', 'Sie bekommen konkrete Empfehlungen', 'Danach ein Angebot, das genau passt'])}</div>
    <div class="bk__alt"><span>Lieber direkt sprechen?</span><a class="link" href="{SITE['wa']}" target="_blank" rel="noopener">{icon('wa')} WhatsApp schreiben</a><a class="link" href="tel:{SITE['phone_intl']}">{icon('phone')} {e(SITE['phone'])}</a></div>
  </aside>
  <form class="bk__main" novalidate aria-labelledby="bk-title">
    <h2 class="sr-only" id="bk-title">Erstgespräch buchen</h2>
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
          <div class="field"><label for="bk-firma">Unternehmen <i>(Pflichtfeld)</i></label><input id="bk-firma" name="firma" type="text" autocomplete="organization" placeholder="z. B. Café Elbblick"></div>
          <div class="field"><label for="bk-branche">Branche <i>(Pflichtfeld)</i></label><select id="bk-branche" name="branche">{bopts}</select></div>
          <div class="field"><label for="bk-website">Aktuelle Website</label><input id="bk-website" name="website" type="text" inputmode="url" autocomplete="url" placeholder="falls vorhanden, z. B. beispiel.de"></div>
          <div class="field"><label for="bk-ort">Ort oder PLZ</label><input id="bk-ort" name="ort" type="text" autocomplete="address-level2" placeholder="z. B. Hamburg"></div>
          <div class="field field--full"><span class="bk__sub">Mitarbeitende</span><div class="opts opts--4">{groesse}</div></div>
        </div>
      </section>
      <section class="bk__step" data-step="3" aria-labelledby="bk-h3" hidden>
        <h3 id="bk-h3">Wann passt es Ihnen?</h3>
        <p>Wählen Sie Gesprächsart und Termin.</p>
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
          <div class="field"><label for="bk-name">Vor- und Nachname <i>(Pflichtfeld)</i></label><input id="bk-name" name="name" type="text" autocomplete="name" placeholder="Max Mustermann"></div>
          <div class="field"><label for="bk-email">E-Mail <i>(Pflichtfeld)</i></label><input id="bk-email" name="email" type="email" autocomplete="email" placeholder="name@firma.de"></div>
          <div class="field"><label for="bk-tel">Telefon</label><input id="bk-tel" name="telefon" type="tel" autocomplete="tel" placeholder="Für Telefonat, Rückruf oder WhatsApp"></div>
          <div class="field" style="align-content:end"><label class="checkline" style="min-height:52px;align-items:center"><input type="checkbox" id="bk-wa" name="whatsapp" value="1"><span>Bestätigung zusätzlich per WhatsApp</span></label></div>
          <div class="field field--full"><label for="bk-msg">Ihre Nachricht</label><textarea id="bk-msg" name="nachricht" placeholder="Was ist Ihnen wichtig? Gibt es einen Termin, bis wann alles fertig sein soll?"></textarea></div>
          <div class="field--full hp" aria-hidden="true"><label for="bk-hp">Dieses Feld bitte nicht ausfüllen</label><input id="bk-hp" name="ml_zx" type="text" tabindex="-1" autocomplete="off" data-lpignore="true" data-1p-ignore data-form-type="other"></div>
          <label class="checkline field--full"><input type="checkbox" id="bk-consent" name="einwilligung" value="1"><span>Ich bin einverstanden, dass Medialyte meine Angaben zur Bearbeitung meiner Anfrage speichert und mich kontaktiert. Details in der <a href="{ctx.u('/datenschutz/')}">Datenschutzerklärung</a>. (Pflichtfeld)</span></label>
        </div>
      </section>
      <section class="bk__step" data-step="5" aria-labelledby="bk-h5" hidden>
        <div class="done">
          <span class="done__ic">{icon('check')}</span>
          <h3 id="bk-h5">Vielen Dank<span class="done__name"></span>!</h3>
          <p class="done__line">Ihre Anfrage für <b class="done__when"></b> ist bei uns eingegangen. Sie erhalten in Kürze eine Bestätigung per E-Mail.</p>
          <dl class="summary" style="width:100%;text-align:left"></dl>
          <div class="done__actions">
            <button class="btn btn--ghost" type="button" data-ics hidden>{icon('calendar')} In Kalender eintragen</button>
            <a class="btn btn--wa" href="{SITE['wa']}" target="_blank" rel="noopener" data-wa-done>{icon('wa')} Per WhatsApp schreiben</a>
          </div>
          <p class="demo-note" hidden>Vorschau: Hier wird nichts gesendet. Auf der Live-Seite geht die Anfrage direkt an das Medialyte-Dashboard.</p>
        </div>
      </section>
      <p class="bk__err" role="alert"></p>
    </div>
    <div class="bk__nav">
      <button class="btn btn--ghost" type="button" data-back hidden>{icon('left')} Zurück</button>
      <button class="btn btn--primary" type="submit" data-next style="margin-left:auto">Weiter</button>
    </div>
  </form>
</div>"""


# ======================================================================= Unterseiten-Bausteine
def page_hero(ctx, crumbs, h1, lead, actions="", visual=""):
    cr = "".join(f'<li><a href="{ctx.u(p)}">{e(n)}</a></li>' if p else f'<li aria-current="page">{e(n)}</li>' for n, p in crumbs)
    vis = f'<div class="phero__visual" data-intro style="--i:4">{visual}</div>' if visual else ""
    return f"""
<section class="phero hero">
  <div class="hero__bg" aria-hidden="true"><span class="hero__glow"></span><span class="hero__grid"></span></div>
  <div class="wrap phero__grid{'' if visual else ' phero__grid--single'}">
    <div class="phero__copy">
      <nav aria-label="Brotkrümelnavigation" data-intro style="--i:0"><ol class="crumbs">{cr}</ol></nav>
      <h1 data-intro style="--i:1">{h1}</h1>
      <p class="lead" data-intro style="--i:2">{lead}</p>
      {f'<div class="phero__actions" data-intro style="--i:3">{actions}</div>' if actions else ''}
    </div>
    {vis}
  </div>
</section>"""


def feats(items, cols=3, tone=None):
    """Raster mit Symbol, Titel, Text. tone: Farbe der Leistung (web, crm, ai, ads) oder eine Liste, die reihum gilt."""
    cls = "feats" if cols == 3 else "feats feats--2"
    def tc(i):
        tn = tone[i % len(tone)] if isinstance(tone, (list, tuple)) else tone
        return f" ic--{tn}" if tn else ""
    return f'<ul class="{cls}">' + "".join(
        f'<li data-reveal style="--rd:{i % cols}"><span class="ic{tc(i)}">{icon(ic)}</span><h3>{t}</h3><p>{d}</p></li>' for i, (ic, t, d) in enumerate(items)) + "</ul>"


def frame_img(ctx, src, w, h, host, alt, lazy=True):
    return f'<div class="frame"><div class="frame__bar"><i></i><i></i><i></i><span class="frame__url">{icon("lock")}{e(host)}</span></div>{img(ctx, src, w, h, alt, lazy=lazy)}</div>'
