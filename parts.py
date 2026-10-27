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
    ("rechnungsradar", "RechnungsRadar"), ("cv", "CV"), ("hubo-dmoran", "Hubo d'Moran"),
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

TEAM = [
    ("Daniel", "D", "Inhaber · Kunden und Projekte", "Ihr Ansprechpartner vom ersten Gespräch bis lange nach dem Livegang. Daniel hört zu, plant Ihr Projekt und sorgt dafür, dass am Ende alles zusammenpasst."),
    ("Hannes", "H", "Entwicklung", "Hannes baut Websites, Apps und Systeme, die schnell laden, sicher laufen und mit Ihrem Betrieb mitwachsen."),
    ("Maximilian", "M", "Design", "Maximilian gestaltet Oberflächen, die Ihre Marke tragen und Ihre Kunden ohne Umwege ans Ziel bringen."),
    ("Aurelia", "A", "Marketing", "Aurelia plant Kampagnen und Inhalte, damit genau die richtigen Menschen auf Sie aufmerksam werden."),
    ("Finn", "F", "Buchhaltung und Management", "Finn hält im Hintergrund alles zusammen: Angebote, Abrechnung und Organisation – klar und verlässlich."),
]

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
     "<p>Ja. Texte, Bilder oder Speisekarten können Sie jederzeit selbst ändern, ganz ohne Technikkenntnisse. Wenn Sie lieber nichts anfassen möchten, übernimmt das der KI-Agent.</p>"),
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
IDEA = [
    ("vermehrung", "Vermehrung", "Neue Kunden gewinnen",
     "Wir sorgen dafür, dass die richtigen Menschen Sie finden: mit einer Website, die bei Google gefunden wird, und Werbung, die genau Ihre Zielgruppe erreicht. Aus Besuchern werden Anfragen.",
     [("/leistungen/website-erstellung/", "Website-Erstellung"), ("/leistungen/online-marketing/", "Online-Marketing")], -90),
    ("verbesserung", "Verbesserung", "Kunden überzeugen und halten",
     "Ein Auftritt, der Vertrauen schafft, schnelle Antworten und Informationen, die immer stimmen. Der KI-Agent hält Ihre Seite aktuell, damit kein Kunde vor veralteten Öffnungszeiten steht.",
     [("/leistungen/website-erstellung/", "Website-Erstellung"), ("/leistungen/ki-agent/", "KI-Agent")], 30),
    ("verwaltung", "Verwaltung", "Den Überblick behalten",
     "Anfragen, Termine, Angebote und Kunden laufen in Ihrem eigenen System zusammen. Nichts geht verloren, und Ihr Team sieht jederzeit, was als Nächstes zu tun ist.",
     [("/leistungen/kundenmanagement-system/", "Kundenmanagement-System"), ("/leistungen/ki-agent/", "KI-Agent")], 150),
]


def idea(ctx):
    r = 44
    arcs, nodes, panels, dots = "", "", "", ""
    for i, (key, name, h, text, uses, ang) in enumerate(IDEA):
        a0, a1 = math.radians(ang - 46), math.radians(ang + 46)
        x0, y0 = 50 + r * math.cos(a0), 50 + r * math.sin(a0)
        x1, y1 = 50 + r * math.cos(a1), 50 + r * math.sin(a1)
        arcs += f'<path class="orb__arc{" is-on" if i == 0 else ""}" data-arc="{i}" d="M{x0:.2f} {y0:.2f}A{r} {r} 0 0 1 {x1:.2f} {y1:.2f}"/>'
        nx, ny = 50 + r * math.cos(math.radians(ang)), 50 + r * math.sin(math.radians(ang))
        nodes += (f'<button class="orb__node" type="button" role="tab" id="idea-t{i}" aria-controls="idea-p{i}" aria-selected="{"true" if i == 0 else "false"}" '
                  f'tabindex="{0 if i == 0 else -1}" style="--x:{nx:.1f}%;--y:{ny:.1f}%">{name}</button>')
        tags = "".join(f'<li><a href="{ctx.u(p)}">{e(t)}</a></li>' for p, t in uses)
        panels += f"""
<div class="idea__panel{' is-on' if i == 0 else ''}" role="tabpanel" id="idea-p{i}" aria-labelledby="idea-t{i}"{'' if i == 0 else ' aria-hidden="true"'}>
  <span class="idea__label">{name}</span>
  <h3>{h}</h3>
  <p>{text}</p>
  <div class="idea__uses"><small>Dafür bauen wir</small><ul class="tags">{tags}</ul></div>
</div>"""
        dots += f'<i class="{"is-on" if i == 0 else ""}"></i>'
    return f"""
<div class="idea" data-idea>
  <div class="orb" data-reveal="scale">
    <svg class="orb__svg" viewBox="0 0 100 100" aria-hidden="true"><circle class="orb__ring" cx="50" cy="50" r="{r}"/><circle class="orb__ring orb__ring--in" cx="50" cy="50" r="34"/>{arcs}</svg>
    <div class="orb__spin" aria-hidden="true"><i></i></div>
    <div class="orb__center" aria-hidden="true">{LOGO}<b>Ihr Betrieb</b><small>und seine Kundenbeziehungen</small></div>
    <div role="tablist" aria-label="Die drei Bereiche">{nodes}</div>
  </div>
  <div data-reveal>
    <div class="idea__panels">{panels}</div>
    <div class="idea__dots" aria-hidden="true">{dots}</div>
  </div>
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
<article class="st{" is-active" if i == 0 else ""}" id="st-{i}" data-station="{i}" aria-labelledby="st-h{i}">
  <div class="st__text">
    <span class="st__name"><span class="jr__n" aria-hidden="true">{i + 1}</span>{name}</span>
    <h3 id="st-h{i}">{h}</h3>
    <p>{text}</p>
    {ticks(items)}
    <a class="link" href="{ctx.u(link)}">{link_t} {icon('arrow')}</a>
  </div>
  <div class="st__vis"><div class="st__fit">{vis[v]()}<p class="st__cap">{cap}</p></div></div>
</article>"""
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
  <button class="case__media" type="button" data-ref="{k}" aria-haspopup="dialog" aria-label="Vorschau von {e(r['title'])} öffnen">
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
      <h2 id="rd-title" data-rd="title"></h2>
      <p data-rd="text"></p>
      <div class="rd__nums" data-rd="nums"></div>
      <div class="rd__actions">
        <a class="btn btn--light" href="#" target="_blank" rel="noopener" data-rd="link"><span></span> {icon('out')}</a>
        <a class="btn btn--ghost" href="{book_link(ctx)}" data-close-dialog>Ähnliches Projekt anfragen</a>
      </div>
      <dl class="rd__facts" data-rd="facts"></dl>
    </div>
  </div>
</dialog>
<script type="application/json" id="refs-data">{json.dumps(data, ensure_ascii=False)}</script>"""


# ======================================================================= Vorher/Nachher
def ba_slider(ctx):
    return f"""
<div class="ba" data-ba role="group" aria-label="Vorher-Nachher-Vergleich der Website RechnungsRadar">
  {img(ctx, 'img/refs/rechnungsradar-nachher.webp', 1280, 560, 'Website RechnungsRadar nach dem Relaunch')}
  {img(ctx, 'img/refs/rechnungsradar-vorher.webp', 1280, 560, 'Website RechnungsRadar vor dem Relaunch', cls='ba__before')}
  <input type="range" min="0" max="100" value="50" step="1" aria-label="Vergleich verschieben: links vorher, rechts nachher">
  <span class="ba__line" aria-hidden="true"><span class="ba__knob">{icon('drag')}</span></span>
  <span class="ba__tag ba__tag--before" aria-hidden="true">Vorher</span>
  <span class="ba__tag ba__tag--after" aria-hidden="true">Nachher</span>
</div>"""


def results(ctx):
    return f"""
<div class="res">
  <div data-reveal>{ba_slider(ctx)}</div>
  <figure class="quote" data-reveal style="--rd:1">
    <svg class="quote__mark" viewBox="0 0 40 30" aria-hidden="true"><path fill="currentColor" d="M0 30V17.6C0 7.9 5.3 1.6 15.9 0l1.6 4.3C11.6 5.9 8.6 9.1 8.3 14h7.3v16zm22.4 0V17.6c0-9.7 5.3-16 15.9-17.6L40 4.3C34 5.9 31 9.1 30.7 14H38v16z"/></svg>
    <blockquote>
      <p>Dank Medialyte hat meine Website für RechnungsRadar einen echten Qualitätssprung gemacht. Aus einer eher schlichten Seite ist ein professioneller Auftritt geworden, der Vertrauen schafft.</p>
      <p>Seitdem erreichen mich deutlich mehr Anfragen von Steuerberatern. Die Zusammenarbeit war reibungslos, schnell und absolut zuverlässig – sehr empfehlenswert!</p>
    </blockquote>
    <figcaption>{img(ctx, 'img/logos/avatar-rechnungsradar.webp', 112, 112, 'Logo RechnungsRadar')}<span><b>Hannes Diedrichsen</b><small>Gründer von RechnungsRadar</small></span></figcaption>
  </figure>
</div>
<div class="deltas" data-reveal>
  <div class="delta"><b>+<span data-count="230">230</span> %</b><small>Kundenanfragen</small></div>
  <div class="delta"><b>−<span data-count="67">67</span> %</b><small>Absprungrate</small></div>
  <div class="delta"><b>+<span data-count="73">73</span> %</b><small>Conversionrate</small></div>
  <div class="delta"><b>−<span data-count="15">15</span> %</b><small>Marketingkosten</small></div>
</div>
<p class="deltas__note">Veränderung bei RechnungsRadar nach dem Relaunch, im Vergleich zur vorherigen Website.</p>"""


# ======================================================================= Vergleich
def compare():
    Y = f'<span class="v yes">{icon("check")}'
    P = f'<span class="v part">{icon("minus")}'
    N = f'<span class="v no">{icon("x")}'
    rows = [
        ("Website für Ihre Zielgruppe gemacht", Y + "Ja</span>", Y + "Ja</span>", P + "Vorlage</span>"),
        ("Kundenmanagement-System aus einer Hand", Y + "Ja</span>", P + "Selten</span>", N + "Nein</span>"),
        ("Änderungen per WhatsApp oder Dashboard", Y + "Mit KI-Agent</span>", P + "Per Auftrag</span>", N + "Selbst machen</span>"),
        ("Website, SEO und Werbung abgestimmt", Y + "Ja</span>", P + "Oft getrennt</span>", N + "Nein</span>"),
        ("Laufende Pflege", Y + "Im Abo enthalten</span>", P + "Meist extra</span>", N + "Selbst machen</span>"),
        ("Ansprechpartner", Y + "Fest und persönlich</span>", P + "Wechselnd</span>", N + "Hotline</span>"),
        ("Angebot", Y + "Innerhalb von 48 h</span>", P + "Unterschiedlich</span>", Y + "Festpreis-Tarif</span>"),
    ]
    body = "".join(f'<tr><th scope="row">{a}</th><td class="is-us">{b}</td><td>{c}</td><td>{d}</td></tr>' for a, b, c, d in rows)
    return f"""
<div data-reveal>
  <div class="cmp-tabs chips" role="group" aria-label="Vergleich wählen"><button class="chip" type="button" data-vs="agentur" aria-pressed="true">vs. Agentur</button><button class="chip" type="button" data-vs="baukasten" aria-pressed="false">vs. Baukasten</button></div>
  <table class="cmp" data-vs="agentur">
    <caption class="sr-only">Vergleich: Medialyte, klassische Agentur und Website-Baukasten</caption>
    <thead><tr><th scope="col"><span class="sr-only">Merkmal</span></th><th scope="col" class="is-us">Medialyte</th><th scope="col">Klassische Agentur</th><th scope="col">Website-Baukasten</th></tr></thead>
    <tbody>{body}</tbody>
  </table>
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
    <div class="plan__price"><b>Pauschale + monatliches Abo</b><small>Ihr Preis steht im Angebot, innerhalb von 48 h</small></div>
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
    return f'<ol class="proc{(" " + cls) if cls else ""}" data-proc style="--n:{len(items)}"><span class="proc__line" aria-hidden="true"><i></i></span>{lis}</ol>'


# ======================================================================= Team
def team():
    """Team als ruhige Liste: Name, Aufgabe, ein Satz. Fotos folgen (dann als <img> in .member__pic)."""
    rows = "".join(f"""
<li class="member" data-reveal style="--rd:{i}">
  <h3 class="member__name">{e(n)}</h3>
  <span class="member__role">{e(r)}</span>
  <p>{e(t)}</p>
</li>""" for i, (n, ini, r, t) in enumerate(TEAM))
    return f'<ul class="team" role="list">{rows}</ul>'


# ======================================================================= Film (Platzhalter)
def film():
    """Platzhalter für den Film: Die vier Kapitel laufen als Titelkarten durch, die Liste daneben
    springt zu einem Kapitel. Ehrlich beschriftet – der Film selbst folgt."""
    chapters = [
        ("Die Ausgangslage", "Warum viele Websites Kunden verlieren statt gewinnen"),
        ("Unser Ablauf", "Vom Erstgespräch über den Entwurf bis zum Livegang"),
        ("Der Unterschied", "Was Medialyte anders macht als eine klassische Agentur"),
        ("Ihr KI-Agent", "So bleiben Website und System ohne Aufwand aktuell"),
    ]
    scenes = "".join(
        f'<div class="film__scene{" is-on" if i == 0 else ""}" data-scene="{i}"><small>Kapitel {i + 1}</small><b>{t}</b><span>{d}</span></div>'
        for i, (t, d) in enumerate(chapters))
    bars = "".join(f"<i{' class="is-on"' if i == 0 else ''}></i>" for i in range(len(chapters)))
    lis = "".join(
        f'<li><button type="button" class="film__ch{" is-on" if i == 0 else ""}" data-go="{i}" aria-pressed="{"true" if i == 0 else "false"}"><span class="num">{i + 1}</span><b>{t}</b><span>{d}</span></button></li>'
        for i, (t, d) in enumerate(chapters))
    return f"""
<div class="film" data-film>
  <div class="film__frame" data-reveal="scale" aria-hidden="true">
    {LOGO.replace('class="mono"', 'class="film__mono"')}
    <div class="film__scenes">{scenes}</div>
    <div class="film__foot"><span class="film__bars">{bars}</span><span>Der Film entsteht gerade · etwa 90 Sekunden</span></div>
  </div>
  <ol class="film__chapters" data-reveal aria-label="Kapitel des Films">{lis}</ol>
</div>"""


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

    def opt(name, value, ic, title, sub, typ="checkbox"):
        i = f"bk-{name}-{value}"
        return f'<div class="opt"><input type="{typ}" name="{name}" value="{value}" id="{i}"><label for="{i}"><span class="ic">{icon(ic)}</span><b>{title}</b><small>{sub}</small></label></div>'

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
        opt("format", "vor-ort", "pin", "Vor Ort", "In Hamburg", typ="radio"),
    ])
    branchen = ["Gastronomie & Hotellerie", "Handwerk & Bau", "Einzelhandel & E-Commerce", "Kanzlei & Beratung",
                "Praxis & Gesundheit", "Industrie & Technik", "Dienstleistung", "Immobilien", "Verein & Organisation", "Andere Branche"]
    bopts = '<option value="">Bitte wählen</option>' + "".join(f"<option>{e(b)}</option>" for b in branchen)
    groesse = "".join(simple("groesse", v, t) for v, t in [("1-5", "1–5"), ("6-20", "6–20"), ("21-100", "21–100"), ("100+", "über 100")])
    zeit = "".join(simple("zeitfenster", v, t) for v, t in [("vormittags", "Vormittags"), ("nachmittags", "Nachmittags"), ("flexibel", "Flexibel")])
    return f"""
<div class="bk" id="booking" data-demo="{demo}" data-endpoint="/api/termin.php" data-slots="/api/slots.php">
  <aside class="bk__aside">
    <div class="bk__host"><span class="ava" aria-hidden="true">D</span><span><b>Daniel</b><small>Inhaber · Ihr Ansprechpartner</small></span></div>
    <h3>Kostenfreies Erstgespräch</h3>
    <ul class="bk__meta">
      <li>{icon('clock')} 30 Minuten</li>
      <li>{icon('video')} Video-Call, Telefon oder vor Ort in Hamburg</li>
      <li>{icon('shield')} Unverbindlich und kostenfrei</li>
    </ul>
    <div class="bk__get"><b>Das erwartet Sie</b>{ticks(['Wir schauen uns Ihre Situation an', 'Sie bekommen konkrete Empfehlungen', 'Ihr Angebot folgt innerhalb von 48 Stunden'])}</div>
    <div class="bk__alt"><span>Lieber direkt sprechen?</span><a class="link" href="{SITE['wa']}" target="_blank" rel="noopener">{icon('wa')} WhatsApp schreiben</a><a class="link" href="tel:{SITE['phone_intl']}">{icon('phone')} {e(SITE['phone'])}</a></div>
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
          <div class="field"><label for="bk-firma">Unternehmen <i>(Pflichtfeld)</i></label><input id="bk-firma" name="firma" autocomplete="organization" placeholder="z. B. Café Elbblick"></div>
          <div class="field"><label for="bk-branche">Branche <i>(Pflichtfeld)</i></label><select id="bk-branche" name="branche">{bopts}</select></div>
          <div class="field"><label for="bk-website">Aktuelle Website</label><input id="bk-website" name="website" inputmode="url" autocomplete="url" placeholder="falls vorhanden, z. B. beispiel.de"></div>
          <div class="field"><label for="bk-ort">Ort oder PLZ</label><input id="bk-ort" name="ort" autocomplete="address-level2" placeholder="z. B. Hamburg"></div>
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
          <div class="field"><label for="bk-name">Vor- und Nachname <i>(Pflichtfeld)</i></label><input id="bk-name" name="name" autocomplete="name" placeholder="Max Mustermann"></div>
          <div class="field"><label for="bk-email">E-Mail <i>(Pflichtfeld)</i></label><input id="bk-email" name="email" type="email" autocomplete="email" placeholder="name@firma.de"></div>
          <div class="field"><label for="bk-tel">Telefon</label><input id="bk-tel" name="telefon" type="tel" autocomplete="tel" placeholder="Für Telefonat, Rückruf oder WhatsApp"></div>
          <div class="field" style="align-content:end"><label class="checkline" style="min-height:52px;align-items:center"><input type="checkbox" id="bk-wa" name="whatsapp" value="1"><span>Bestätigung zusätzlich per WhatsApp</span></label></div>
          <div class="field field--full"><label for="bk-msg">Ihre Nachricht</label><textarea id="bk-msg" name="nachricht" placeholder="Was ist Ihnen wichtig? Gibt es einen Termin, bis wann alles fertig sein soll?"></textarea></div>
          <div class="field--full hp" aria-hidden="true"><label for="bk-hp">Bitte leer lassen</label><input id="bk-hp" name="firma_url" tabindex="-1" autocomplete="off"></div>
          <label class="checkline field--full"><input type="checkbox" id="bk-consent" name="einwilligung" value="1"><span>Ich bin einverstanden, dass Medialyte meine Angaben zur Bearbeitung meiner Anfrage speichert und mich kontaktiert. Details in der <a href="{ctx.u('/datenschutz/')}">Datenschutzerklärung</a>. (Pflichtfeld)</span></label>
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
      <ol class="crumbs" aria-label="Brotkrümelnavigation" data-intro style="--i:0">{cr}</ol>
      <h1 data-intro style="--i:1">{h1}</h1>
      <p class="lead" data-intro style="--i:2">{lead}</p>
      {f'<div class="phero__actions" data-intro style="--i:3">{actions}</div>' if actions else ''}
    </div>
    {vis}
  </div>
</section>"""


def feats(items, cols=3):
    cls = "feats" if cols == 3 else "feats feats--2"
    return f'<ul class="{cls}">' + "".join(
        f'<li data-reveal style="--rd:{i % cols}"><span class="ic">{icon(ic)}</span><h3>{t}</h3><p>{d}</p></li>' for i, (ic, t, d) in enumerate(items)) + "</ul>"


def frame_img(ctx, src, w, h, host, alt, lazy=True):
    return f'<div class="frame"><div class="frame__bar"><i></i><i></i><i></i><span class="frame__url">{icon("lock")}{e(host)}</span></div>{img(ctx, src, w, h, alt, lazy=lazy)}</div>'
