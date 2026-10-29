"""Seiten von medialyte.de.

Jede Seite ist ein Eintrag in PAGES mit Pfad, Titel, Beschreibung und einer render-Funktion.
Gemeinsame Bausteine und Texte stehen in parts.py, die gezeichneten Oberflächen in mocks.py.
Texte ändern, dann `python3 build.py` ausführen.
"""
import re

from build import SITE, breadcrumb_schema, e, faq_schema, icon, org_schema
import legal
import mocks
from parts import (FAQ_MAIN, PROCESS, REFS, LOGOS, _LOGO_DIMS, book_link, booking_widget, btn_book, btn_wa,
                   cases, closing, compare, faq_block, feats, film, svc_film, idea, img, impact, journey, logo_marquee, marquee_rows, page_hero, plans,
                   process, ref_dialog, results, sh, ticks)


# ======================================================================= Startseite
def render_home(ctx):
    hero = f"""
<section class="hero" id="start">
  <div class="hero__bg" aria-hidden="true"><span class="hero__glow"></span><span class="hero__glow hero__glow--2"></span><span class="hero__grid"></span></div>
  <div class="wrap hero__in">
    <p class="kicker hero__kicker" data-intro style="--i:0"><span class="kicker__dot" aria-hidden="true"></span>Digitalagentur aus Hamburg für Betriebe in ganz Deutschland</p>
    <h1 class="display hero__title"><span class="line"><span style="--i:1">Ihre Website soll Kunden bringen.</span></span><span class="line"><span style="--i:2">Nicht Arbeit machen.</span></span></h1>
    <p class="lead hero__lead" data-intro style="--i:3">Wir bauen die Website, die Ihre Zielgruppe überzeugt, und das System dahinter, in dem jede Anfrage landet. Änderungen schicken Sie einfach per WhatsApp – unser KI-Agent setzt sie um.</p>
    <div class="hero__actions" data-intro style="--i:4">{btn_book(ctx, cls='btn--primary btn--lg')}{btn_wa(ctx, cls='btn--ghost btn--lg')}</div>
    <ul class="hero__proof" data-intro style="--i:5">
      <li>{icon('trend')}<span><b>200+</b> erfolgreiche Kampagnen</span></li>
      <li><a href="#faq-kosten" data-faq-link>{icon('clock')}<span>Angebot in <b>48 Stunden</b></span></a></li>
      <li><a href="#faq-garantie" data-faq-link>{icon('shield')}<span><b>Zufriedenheitsgarantie</b></span></a></li>
    </ul>
  </div>
  <div class="wrap">{mocks.cockpit(ctx)}</div>
</section>"""

    idee = f"""
<section class="section" id="idee">
  <div class="wrap">
    {sh('Vermehrung.<br>Verbesserung.<br>Verwaltung.', 'Davon lebt jeder Betrieb: dass neue Kunden kommen, dass sie bleiben und dass dabei nichts verloren geht. Für alle drei bauen wir Lösungen, die genau zu Ihrem Betrieb passen.', split=True)}
    {idea(ctx)}
  </div>
</section>"""

    reise = f"""
<section class="section section--deep" id="leistungen">
  <span id="Leistungen" aria-hidden="true"></span>
  <div class="wrap">
    {sh('Es beginnt mit Ihrer Website. <span class="quiet">Und hört dort nicht auf.</span>', 'Die meisten Kunden starten mit einer neuen Website. Danach bauen wir weiter, Schritt für Schritt – so weit, wie es sich für Ihren Betrieb lohnt.', split=True)}
    {journey(ctx)}
  </div>
</section>"""

    referenzen = f"""
<section class="section" id="referenzen">
  <div class="wrap">
    {sh('Drei Projekte. <span class="quiet">Drei völlig verschiedene Welten.</span>', 'Ein Rechnungsmanagement-System, eine Juwelierkette mit vier Filialen und ein Industriekonzern mit über 1.500 Mitarbeitenden. Öffnen Sie ein Projekt und scrollen Sie durch die ganze Seite.', split=True)}
    {cases(ctx)}
    <div class="cases__more" data-reveal><span>Außerdem für Hubo d’Moran, FassadenTrio, DELUXE Design, GADO Energie und viele mehr.</span><a class="link" href="{ctx.u('/referenzen/')}">Alle Referenzen {icon('arrow')}</a></div>
  </div>
</section>"""

    ergebnisse = f"""
<section class="section section--deep" id="ergebnisse">
  <div class="wrap">
    {sh('Vorher, nachher – <span class="quiet">und was es gebracht hat.</span>', 'Aus einer schlichten Seite wurde für RechnungsRadar ein Auftritt, der verkauft. Das zeigen die Zahlen nach dem Relaunch.', split=True)}
    {results(ctx)}
  </div>
</section>"""

    vergleich = f"""
<section class="section" id="vergleich">
  <div class="wrap">
    {sh('Was uns von einer klassischen Agentur unterscheidet', 'Bei uns bekommen Sie Website, System, Pflege und Werbung aus einer Hand – mit einem festen Ansprechpartner und einem KI-Agenten, der Ihre Seite aktuell hält.', split=True)}
    {compare()}
  </div>
</section>"""

    pakete = f"""
<section class="section section--deep" id="pakete">
  <div class="wrap">
    {sh('Drei Wege, mit uns zu starten.', 'Jedes Angebot besteht aus einer einmaligen Pauschale und einem monatlichen Abo. Was genau dazugehört, richtet sich nach Ihrem Betrieb. Beschreiben Sie ihn in einem Satz – wir zeigen, welches Paket passt.', split=True)}
    {plans(ctx)}
  </div>
</section>"""

    ablauf = f"""
<section class="section" id="ablauf">
  <div class="wrap">
    {sh('In fünf Schritten zu Ihrer Lösung.', 'Klar geplant und ohne Fachchinesisch. Sie wissen jederzeit, wo Ihr Projekt steht und was als Nächstes passiert.', split=True)}
    {process()}
  </div>
</section>"""

    film_s = f"""
<section class="section section--deep" id="film">
  <div class="wrap">
    {sh('Medialyte in 100 Sekunden.', 'Wie wir arbeiten, was uns von anderen Agenturen unterscheidet und wie der KI-Agent Ihre Website aktuell hält.', split=True)}
    {film(ctx)}
  </div>
</section>"""

    faq = f"""
<section class="section" id="faq">
  <div class="wrap">{faq_block(ctx, FAQ_MAIN)}</div>
</section>"""

    termin = f"""
<section class="section section--deep" id="termin">
  <span id="beratung" aria-hidden="true"></span>
  <div class="wrap">
    {sh('Buchen Sie Ihr <span class="nowrap">kostenfreies</span> Erstgespräch.', '30 Minuten, per Video, Telefon oder im Raum Hamburg bei Ihnen vor Ort. Wir hören zu, schauen uns Ihre Situation an und sagen Ihnen, was sich lohnt. Ihr Angebot folgt innerhalb von 48 Stunden.', center=True)}
    <div data-reveal>{booking_widget(ctx)}</div>
  </div>
</section>"""

    # Der Film steht direkt nach den Leistungen; die Abschnitte wechseln sich danach hell und dunkel ab
    blocks = [idee, reise, film_s, referenzen, ergebnisse, vergleich, pakete, ablauf, faq, termin]
    blocks = [re.sub(r'<section class="section( section--deep)?"', '<section class="section' + (' section--deep' if i % 2 else '') + '"', b, count=1)
              for i, b in enumerate(blocks)]
    return hero + logo_marquee(ctx) + "".join(blocks)


# ======================================================================= Leistungsseiten
FAQ_WEB = [
    ("Was kostet es, eine Website erstellen zu lassen?", "<p>Ihr Angebot besteht aus einer einmaligen Pauschale für Konzept, Design und Entwicklung und einem monatlichen Abo für Hosting, Domain, SSL, Pflege durch den KI-Agenten und Support. Den genauen Preis erhalten Sie nach dem kostenfreien Erstgespräch innerhalb von 48 Stunden.</p>"),
    ("Wie lange dauert es bis zur fertigen Website?", "<p>Eine übersichtliche Website ist in zwei bis vier Wochen online. Bei größeren Projekten mit vielen Unterseiten, Shop oder System planen wir gemeinsam einen Zeitplan.</p>"),
    ("Übernehmen Sie Inhalte von meiner alten Website?", "<p>Ja. Bei einem Relaunch übernehmen wir Ihre Inhalte, überarbeiten sie bei Bedarf und richten Weiterleitungen ein, damit Ihre Google-Platzierungen erhalten bleiben.</p>"),
    ("Wird meine Website bei Google gefunden?", "<p>Jede Website bauen wir suchmaschinenfreundlich: schnelle Ladezeiten, saubere Struktur, passende Seitentitel und Beschreibungen. Für mehr Sichtbarkeit gibt es zusätzlich gezielte SEO-Arbeit und Kampagnen.</p>"),
]
FAQ_SYS = [
    ("Was ist ein Kundenmanagement-System?", "<p>Ein Kundenmanagement-System, oft CRM genannt, bündelt alles rund um Ihre Kunden an einem Ort: Kontaktdaten, Anfragen, Termine, Angebote, Aufträge und Notizen. Ihr Team sieht jederzeit, was zu tun ist.</p>"),
    ("Warum ein eigenes System statt einer Standardsoftware?", "<p>Standardsoftware zwingt Sie oft in fremde Abläufe. Ein eigenes System bildet genau Ihre Prozesse ab, ist mit Ihrer Website verbunden und wächst mit Ihrem Betrieb.</p>"),
    ("Kann das System mit meiner Website verbunden werden?", "<p>Ja, das ist der Kern. Anfragen, Terminbuchungen und Formulare von Ihrer Website landen direkt im Dashboard – ohne Abtippen und ohne verlorene E-Mails.</p>"),
    ("Wie lange dauert die Entwicklung?", "<p>Je nach Umfang sechs bis zwölf Wochen. Wir starten mit den wichtigsten Funktionen und bauen das System Schritt für Schritt aus.</p>"),
]
FAQ_AGENT = [
    ("Wie gebe ich dem KI-Agenten eine Änderung durch?", "<p>Bei einfacheren Websites schreiben Sie per WhatsApp, was sich ändern soll, zum Beispiel neue Öffnungszeiten oder ein neues Gericht. Bei umfangreichen Systemen erledigen Sie Änderungen direkt im eigenen Dashboard.</p>"),
    ("Welche Änderungen übernimmt der Agent?", "<p>Laufende Änderungen wie Öffnungszeiten, Preise, Speisekarten, Bilder, kurze Texte, Termine und Ankündigungen. Neue Bereiche, Funktionen oder ein neues Design setzt unser Team persönlich um.</p>"),
    ("Brauche ich technische Kenntnisse?", "<p>Nein. Sie beschreiben in eigenen Worten, was sich ändern soll. Den Rest erledigt der Agent.</p>"),
    ("Ist der KI-Agent im Preis enthalten?", "<p>Der KI-Agent ist Teil des monatlichen Abos. Welche Leistungen genau enthalten sind, steht transparent in Ihrem Angebot.</p>"),
]
FAQ_MKT = [
    ("Welche Werbekanäle nutzen Sie?", "<p>Vor allem Google Ads und Social Media wie Instagram und Facebook. Welche Kanäle für Sie sinnvoll sind, hängt von Ihrer Zielgruppe ab – das klären wir im Erstgespräch.</p>"),
    ("Wie messen Sie den Erfolg einer Kampagne?", "<p>Mit sauberer Messung von Anfragen, Anrufen und Buchungen, nicht nur von Klicks. Sie erhalten regelmäßig einen Bericht, den man ohne Fachwissen versteht.</p>"),
    ("Was ist mit dem Werbebudget?", "<p>Das Werbebudget zahlen Sie direkt an die Plattform, etwa Google. Unsere Betreuung ist davon getrennt und steht transparent im Angebot.</p>"),
    ("Lohnt sich Werbung ohne gute Website?", "<p>Meist nicht. Deshalb prüfen wir zuerst, ob Ihre Website Besucher in Anfragen verwandelt. Wenn nicht, verbessern wir sie, bevor wir Budget in Werbung stecken.</p>"),
]


def _svc_page(ctx, crumb, h1, lead, visual, sections, faqs, ask, close=None):
    actions = btn_book(ctx, "Erstgespräch buchen", ask) + btn_wa(ctx)
    out = page_hero(ctx, [("Start", "/"), ("Leistungen", "/#leistungen"), (crumb, "")], h1, lead, actions, visual)
    out += sections
    title = {"Website-Erstellung": "Fragen zur Website-Erstellung", "KI-Agent": "Fragen zum KI-Agenten", "Kundenmanagement-System": "Fragen zum System"}.get(crumb, "Fragen zum " + e(crumb))
    out += f'<section class="section section--deep"><div class="wrap">{faq_block(ctx, faqs, title)}</div></section>'
    out += closing(ctx, *close) if close else closing(ctx)
    return out


def render_web(ctx):
    sections = svc_film(ctx, "web") + f"""
<section class="section">
  <div class="wrap">
    {sh('Eine Website, die für Sie arbeitet.', 'Kein Baukasten, keine Vorlage von der Stange. Ihre Website wird für Ihre Zielgruppe gemacht – und danach gepflegt, ohne dass Sie sich darum kümmern müssen.', split=True)}
    {feats(tone="web", items=[
        ('target', 'Gemacht für Ihre Zielgruppe', 'Wir analysieren, wen Sie erreichen wollen, und richten Aufbau, Texte und Gestaltung genau danach aus.'),
        ('mobile', 'Perfekt auf dem Smartphone', 'Die meisten Besucher kommen über das Handy. Dort muss Ihre Seite am besten funktionieren – und das tut sie.'),
        ('zap', 'Schnell geladen', 'Schlanke Technik ohne Plugin-Ballast. Kurze Ladezeiten halten Besucher und helfen bei Google.'),
        ('search', 'Bei Google gefunden', 'Saubere Struktur, passende Seitentitel, strukturierte Daten und lokale Signale: SEO von Anfang an.'),
        ('calendar', 'Kurze Wege zur Anfrage', 'Anruf, WhatsApp, Terminbuchung oder Formular: Ihre Kunden erreichen Sie mit einem Tipp.'),
        ('lock', 'Hosting, Domain und SSL', 'Ihre eigene Adresse, verschlüsselt und sicher gehostet. Um die Technik kümmern wir uns.'),
    ])}
  </div>
</section>
<section class="section section--deep">
  <div class="wrap split">
    <div class="split__text" data-reveal>
      <h2 class="h2">Keine Website? <span class="quiet">Oder eine alte?</span></h2>
      <p>Viele Betriebe haben gar keine Website oder eine, die vor Jahren gebaut wurde und heute weder auf dem Handy noch bei Google überzeugt. Beides lösen wir: Wir bauen neu oder bringen Ihre Seite auf den aktuellen Stand – und übernehmen dabei Ihre Inhalte.</p>
      {ticks(['Analyse Ihrer bisherigen Seite und Ihrer Mitbewerber', 'Übernahme und Überarbeitung Ihrer Inhalte', 'Weiterleitungen, damit Google-Platzierungen erhalten bleiben', 'Pflege danach einfach per WhatsApp'])}
      {btn_book(ctx, 'Erstgespräch buchen', 'web-neu')}
    </div>
    <div data-reveal="scale">{impact(ctx)}<p class="deltas__note">Veränderung bei RechnungsRadar nach dem Relaunch, im Vergleich zur vorherigen Website.</p></div>
  </div>
</section>
<section class="section">
  <div class="wrap">
    {sh('In vier Schritten zur neuen Website.', 'Vom ersten Gespräch bis zum Livegang in meist zwei bis vier Wochen.', split=True)}
    {process([
        ('Erstgespräch', 'Wir lernen Ihren Betrieb und Ihre Ziele kennen. Kostenfrei und unverbindlich.', []),
        ('Konzept und Design', 'Sie erhalten einen Entwurf, den wir gemeinsam verfeinern, bis er passt.', []),
        ('Entwicklung', 'Wir setzen die Website um, testen alles und kümmern uns um Domain und Hosting.', []),
        ('Livegang und Pflege', 'Ihre Seite geht online. Danach hält der KI-Agent sie aktuell.', []),
    ], 'proc--n')}
  </div>
</section>
<section class="section section--deep">
  <div class="wrap">
    {sh('Projekte, die schon für ihre Kunden arbeiten.', 'Öffnen Sie ein Projekt und scrollen Sie durch die ganze Seite.', split=True)}
    {cases(ctx)}
  </div>
</section>"""
    return _svc_page(ctx, "Website-Erstellung", 'Website erstellen lassen – <span class="quiet">gemacht für Ihre Kunden.</span>',
                     "Wir bauen Ihre neue Website oder bringen die bestehende auf den neuesten Stand: individuell gestaltet, schnell, auf dem Smartphone perfekt und bei Google gut auffindbar. Hosting, Pflege und ein KI-Agent für Änderungen sind inklusive.",
                     mocks.relaunch(), sections, FAQ_WEB, "web-neu")


def _flow():
    steps = [("globe", "Anfrage über die Website", "Formular, Terminbuchung oder Rückruf"),
             ("db", "Automatisch im Kundensystem", "Mit allen Angaben, ohne Abtippen"),
             ("calendar", "Termin und Erinnerung", "Für Sie und Ihren Kunden"),
             ("brief", "Angebot und Auftrag", "Jederzeit nachvollziehbar")]
    lis = "".join(f'<li class="proc__item" data-reveal style="--rd:{i}"><span class="num">{i + 1}</span><h3>{t}</h3><p>{d}</p></li>' for i, (ic, t, d) in enumerate(steps))
    return f'<ol class="proc proc--n proc--stack" data-proc style="--n:4"><li class="proc__line" aria-hidden="true"><i></i></li>{lis}</ol>'


def render_sys(ctx):
    sections = svc_film(ctx, "sys") + f"""
<section class="section">
  <div class="wrap">
    {sh('Kundendaten in Excel, Zetteln <span class="quiet">und E-Mails?</span>', 'Wenn Anfragen in verschiedenen Postfächern landen, Termine im Kopf stehen und Angebote in Ordnern verschwinden, gehen Kunden verloren. Ein eigenes System bringt alles an einen Ort.', split=True)}
    {feats(tone="crm", items=[
        ('inbox', 'Alle Anfragen an einem Ort', 'Anfragen von Website, Telefon, E-Mail und WhatsApp landen gesammelt in Ihrem Dashboard.'),
        ('users', 'Kunden im Überblick', 'Kontaktdaten, Verlauf, Notizen und Dokumente zu jedem Kunden – für das ganze Team sichtbar.'),
        ('calendar', 'Termine und Erinnerungen', 'Terminbuchungen von der Website, automatische Erinnerungen und keine vergessenen Rückrufe.'),
        ('brief', 'Angebote und Aufträge', 'Vom ersten Kontakt bis zum Auftrag: Sie sehen jederzeit, was offen ist und was als Nächstes kommt.'),
        ('layers', 'Produktmanagement', 'Für Händler und Industrie: Produkte, Varianten und Datenblätter zentral pflegen und auf der Website ausspielen.'),
        ('bot', 'KI-Agent im Dashboard', 'Der Agent erinnert an offene Anfragen, fasst zusammen und übernimmt Routineaufgaben.'),
    ])}
  </div>
</section>
<section class="section section--deep">
  <div class="wrap split">
    <div class="split__text" data-reveal>
      <h2 class="h2">Ein Dashboard, <span class="quiet">gebaut für Ihre Abläufe.</span></h2>
      <p>Wir entwickeln Ihr System nicht von der Stange, sondern genau für die Art, wie Ihr Betrieb arbeitet: Mandantenverwaltung für eine Kanzlei, Auftragsplanung im Handwerk oder ein Produktfinder für tausende Artikel wie bei RITZ.</p>
      {ticks(['Direkt mit Ihrer Website verbunden', 'Zugriff für Ihr ganzes Team, auch mobil', 'Automatisierte Abläufe statt Fleißarbeit', 'Wächst mit Ihrem Betrieb'])}
      {btn_book(ctx, 'System anfragen', 'system')}
    </div>
    <div>{_flow()}</div>
  </div>
</section>
<section class="section">
  <div class="wrap">
    {sh('App-Entwicklung für RechnungsRadar', 'Ein Rechnungsmanagement-System, das Rechnungen automatisch aus dem E-Mail-Postfach in die Buchhaltung überträgt.', split=True)}
    {cases(ctx, ("rechnungsradar",))}
  </div>
</section>"""
    return _svc_page(ctx, "Kundenmanagement-System", 'Ihr eigenes Kundensystem. <span class="quiet">Verbunden mit Ihrer Website.</span>',
                     "Schluss mit Excel, Zetteln und verlorenen E-Mails. Wir entwickeln Kunden- und Produktmanagement-Systeme, die genau zu Ihren Abläufen passen: Anfragen, Termine, Angebote und Aufträge an einem Ort.",
                     mocks.pipeline(), sections, FAQ_SYS, "system",
                     ("Schluss mit Zettelwirtschaft?", "Sprechen wir über Ihre Abläufe.",
                      "Im kostenfreien Erstgespräch schauen wir uns an, wie Ihr Betrieb heute arbeitet, und zeigen, was ein eigenes System verändern würde. Ihr Angebot erhalten Sie innerhalb von 48 Stunden."))


def render_agent(ctx):
    sections = svc_film(ctx, "agent") + f"""
<section class="section">
  <div class="wrap">
    {sh('Änderungen in einer Nachricht.', 'Ihre Website soll aktuell sein, aber im Alltag fehlt die Zeit. Genau dafür gibt es den KI-Agenten.', split=True)}
    {process([
        ('Bescheid geben', 'Sie schreiben per WhatsApp oder im Dashboard, was sich ändern soll – in eigenen Worten.', []),
        ('Agent setzt um', 'Der KI-Agent pflegt die Änderung auf Ihrer Website ein und gibt Ihnen Bescheid.', []),
        ('Seite ist aktuell', 'Ihre Kunden sehen sofort den neuesten Stand. Größeres übernimmt unser Team.', []),
    ], 'proc--n')}
  </div>
</section>
<section class="section section--deep">
  <div class="wrap duo">
    <div class="duo__col" data-reveal>
      <h3><span class="ic ic--ai">{icon('bot')}</span>Das übernimmt der Agent</h3>
      {ticks(['Öffnungszeiten, Feiertage und Ruhetage', 'Preise, Speisekarten und Preislisten', 'Bilder austauschen und ergänzen', 'Kurze Texte, Termine und Ankündigungen', 'Laufende Pflege Ihrer Seite'])}
    </div>
    <div class="duo__col" data-reveal style="--rd:1">
      <h3><span class="ic ic--web">{icon('users')}</span>Das macht unser Team persönlich</h3>
      {ticks(['Neue Bereiche und Funktionen', 'Design-Anpassungen', 'Beratung zu Google, Werbung und Marketing', 'Größere Umbauten und Sonderwünsche'])}
    </div>
  </div>
</section>
<section class="section">
  <div class="wrap split">
    <div class="split__text" data-reveal>
      <h2 class="h2">WhatsApp <span class="quiet">oder Dashboard.</span></h2>
      <p>Wie Sie mit dem Agenten arbeiten, hängt davon ab, wie umfangreich Ihr System ist. Ein Restaurant schreibt einfach per WhatsApp. Eine Kanzlei mit Mandantenverwaltung erledigt dasselbe im eigenen Dashboard. Beides funktioniert ohne Technikkenntnisse.</p>
      {ticks(['Einfache Websites: Nachricht per WhatsApp', 'Komplexe Systeme: Änderungen im Dashboard', 'Laufende Pflege und Betreuung inklusive'])}
    </div>
    <div data-reveal="scale">{mocks.agent_dashboard()}</div>
  </div>
</section>
<section class="section section--deep">
  <div class="wrap">
    {sh('Was Kunden dem Agenten schreiben', 'Typische Nachrichten aus dem Alltag, aus ganz verschiedenen Branchen.', split=True)}
    {feats(tone="ai", items=[
        ('food', 'Gastronomie', '<q>Diese Woche gibt es Kürbissuppe als Mittagstisch, bitte auf die Karte setzen.</q>'),
        ('hammer', 'Handwerk', '<q>Wir sind vom 23.12. bis 2.1. im Betriebsurlaub, bitte einen Hinweis einbauen.</q>'),
        ('bag', 'Einzelhandel', '<q>Die Herbstkollektion ist da. Hier sind sechs Fotos für die Startseite.</q>'),
        ('scale', 'Kanzleien', '<q>Frau Becker ist neu im Team, bitte mit Foto und Schwerpunkten ergänzen.</q>'),
        ('health', 'Praxen', '<q>Mittwochnachmittag sind wir ab sofort geschlossen, bitte Sprechzeiten anpassen.</q>'),
        ('heart', 'Vereine', '<q>Das Sommerfest ist am 12. Juli, bitte als Termin auf die Website stellen.</q>'),
    ])}
  </div>
</section>"""
    return _svc_page(ctx, "KI-Agent", 'Der KI-Agent, <span class="quiet">der Ihre Website aktuell hält.</span>',
                     "Wird meine Seite gepflegt? Und wie ändere ich etwas, ohne mich mit Technik zu beschäftigen? Der Medialyte KI-Agent löst beides: Sie schreiben per WhatsApp oder im Dashboard, er setzt es um. Probieren Sie es gleich hier aus.",
                     mocks.agent_demo(), sections, FAQ_AGENT, "agent",
                     ("Nie wieder eine veraltete Website.", "Wir zeigen Ihnen, wie es geht.",
                      "Im kostenfreien Erstgespräch zeigen wir, wie der KI-Agent bei Ihrem Betrieb arbeiten würde – per WhatsApp oder im Dashboard. Ihr Angebot erhalten Sie innerhalb von 48 Stunden."))


def render_mkt(ctx):
    sections = svc_film(ctx, "mkt") + f"""
<section class="section">
  <div class="wrap">
    {sh('Marketing, das messbar wirkt.', 'Wir erreichen Ihre Zielgruppe dort, wo sie sucht – und machen aus Aufmerksamkeit Anfragen.', split=True)}
    {feats(tone="ads", items=[
        ('search', 'Google Ads', 'Anzeigen genau dann, wenn Kunden nach Ihrer Leistung suchen. Mit klarer Zielgruppe und kontrolliertem Budget.'),
        ('camera', 'Social-Media-Werbung', 'Kampagnen auf Instagram und Facebook, die zu Ihrer Marke passen und gezielt neue Kunden ansprechen.'),
        ('trend', 'SEO und lokale Sichtbarkeit', 'Bessere Platzierungen bei Google, gepflegte Unternehmensprofile und Inhalte, die gefunden werden.'),
        ('layout', 'Landingpages', 'Eigene Seiten für Ihre Angebote, gebaut für eine Aufgabe: aus Besuchern Anfragen machen.'),
        ('spark', 'KI-gestützte Marketing-Agenten', 'Automatisierte Abläufe für Inhalte, Auswertung und Nachfassen, damit kein Kontakt verloren geht.'),
        ('video', 'Foto- und Video-Shootings', 'Professionelle Bilder und Videos für Website, Anzeigen und Social Media.'),
    ])}
  </div>
</section>
<section class="section section--deep">
  <div class="wrap split">
    <div class="split__text" data-reveal>
      <h2 class="h2">Erst das Fundament, <span class="quiet">dann die Reichweite.</span></h2>
      <p>Werbung bringt Besucher. Ob daraus Kunden werden, entscheidet Ihre Website. Deshalb prüfen wir zuerst, ob Ihre Seite überzeugt, und stimmen Website, Landingpage und Kampagne aufeinander ab. So wird aus Budget Umsatz.</p>
      {ticks(['Messung von Anfragen, Anrufen und Buchungen', 'Berichte, die man ohne Fachwissen versteht', 'Laufende Optimierung Ihrer Kampagnen'])}
      {btn_book(ctx, 'Kampagne anfragen', 'werbung')}
    </div>
    <div data-reveal="scale">{mocks.report()}</div>
  </div>
</section>
<section class="section">
  <div class="wrap">
    {sh('Reichweite, die organisch wächst.', 'Authentische Inhalte, ein starkes Branding und eine Community, die sich für Ihren Betrieb begeistert.', split=True)}
    {feats(tone="ads", items=[
        ('trend', 'Organische Reichweite', 'Strategie, Redaktionsplan und Inhalte, die zu Ihrer Zielgruppe passen.'),
        ('pen', 'Brand-Building', 'Ein einheitlicher Auftritt, an dem man Sie sofort erkennt.'),
        ('users', 'Community-Management', 'Wir betreuen Kommentare und Nachrichten und bauen Beziehungen auf.'),
    ])}
  </div>
</section>"""
    return _svc_page(ctx, "Online-Marketing", 'Online-Marketing, <span class="quiet">das neue Kunden bringt.</span>',
                     "Google Ads, Social Media und SEO aus einer Hand – abgestimmt auf Ihre Website. Aus über 200 Kampagnen wissen wir, wie aus Reichweite echte Anfragen werden.",
                     mocks.campaign(), sections, FAQ_MKT, "werbung",
                     ("Mehr Anfragen statt nur mehr Klicks?", "Sprechen wir über Ihre Ziele.",
                      "Im kostenfreien Erstgespräch prüfen wir, ob Ihre Website bereit für Werbung ist, und sagen ehrlich, welche Kanäle sich für Sie lohnen. Ihr Angebot erhalten Sie innerhalb von 48 Stunden."))


# ======================================================================= Weitere Seiten
def render_refs(ctx):
    more = [
        ("Hubo d’Moran", "Gemeinnütziger Verein", "Zweisprachige Website für einen gemeinnützigen Verein mit Spendenbereich und Buchprojekt.", "https://hubodmoran.com/"),
        ("FassadenTrio", "Dienstleister", "Google-Ads-Kampagne und Landingpage mit Vorher-Nachher-Regler, Ablauf und Fassaden-Check-Rechner.", ""),
        ("DELUXE Design", "E-Commerce", "Hochwertiger Online-Shop auf Shopify für eine Luxusmarke.", ""),
    ]
    mcards = "".join(f"""
<article data-reveal style="--rd:{i}"><span class="case__cat">{e(c)}</span><h3>{e(n)}</h3><p>{e(d)}</p>{f'<a class="link" href="{u}" target="_blank" rel="noopener">Website ansehen {icon("out")}</a>' if u else ''}</article>""" for i, (n, c, d, u) in enumerate(more))
    return (page_hero(ctx, [("Start", "/"), ("Referenzen", "")], 'Projekte, <span class="quiet">die Kunden gewinnen.</span>',
                      "Vom digitalen Produkt über die Juwelierkette bis zum Industriekonzern – eine Auswahl unserer Arbeiten. Öffnen Sie ein Projekt und scrollen Sie durch die ganze Seite.",
                      btn_book(ctx) + btn_wa(ctx))
            + f'<section class="section section--flush"><div class="wrap">{cases(ctx)}</div></section>'
            + f'<section class="section section--deep"><div class="wrap">{sh("Mehr aus unserer Arbeit", split=True)}<div class="more">{mcards}</div></div></section>'
            + f'<section class="section"><div class="wrap">{sh('Vorher, nachher – <span class="quiet">und was es gebracht hat.</span>', 'Was der Relaunch für RechnungsRadar gebracht hat.', split=True)}{results(ctx)}</div></section>'
            + f'<section class="section section--deep section--marquee"><div class="wrap">{sh("Kunden und Partner", "Unternehmen, die mit Medialyte arbeiten – vom Restaurant bis zum Industriekonzern.", split=True)}</div><div data-reveal>{marquee_rows(ctx, 2)}</div></section>'
            + closing(ctx, "Ihr Projekt als nächste Referenz?", "Erzählen Sie uns davon.", "Im kostenfreien Erstgespräch hören wir zu und sagen Ihnen, was sich lohnt. Ihr Angebot erhalten Sie innerhalb von 48 Stunden."))


def render_about(ctx):
    stats = f"""
<div class="deltas deltas--grid">
  <div class="delta"><b><span data-count="200">200</span>+</b><small>erfolgreiche Kampagnen</small></div>
  <div class="delta"><b><span data-count="48">48</span> h</b><small>bis zu Ihrem Angebot</small></div>
  <div class="delta"><b>2–4</b><small>Wochen bis zur neuen Website</small></div>
  <div class="delta"><b>1</b><small>fester Ansprechpartner für Ihr Projekt</small></div>
</div>"""
    values = [
        ("target", "Erst verstehen, dann bauen", "Jede Lösung beginnt mit Ihrer Zielgruppe und Ihren Abläufen, nicht mit einer Vorlage."),
        ("users", "Ein fester Ansprechpartner", "Sie sprechen immer mit Menschen, die Ihr Projekt kennen."),
        ("shield", "Klare Angebote", "Pauschale plus Abo, transparent aufgeschlüsselt und ohne versteckte Kosten."),
        ("spark", "Technik mit Zukunft", "Eigene KI-Agenten und moderne Technik ohne Plugin-Ballast."),
    ]
    ionos = (f'<p class="trustline" data-reveal>{img(ctx, "img/logos/ionos-agency-partner.webp", 185, 100, "IONOS Agency Partner Official")}'
             '<span><b>Offizieller IONOS Agency Partner.</b> Ihre Website läuft auf der Infrastruktur von IONOS – betreut von uns, Sie müssen sich um nichts kümmern.</span></p>')
    return (page_hero(ctx, [("Start", "/"), ("Über uns", "")], 'Damit aus Besuchern Kunden werden. <span class="quiet">Und Kunden bleiben.</span>',
                      "Medialyte ist eine Digitalagentur aus Hamburg. Wir bauen Websites, Kundenmanagement-Systeme und Kampagnen für Betriebe in ganz Deutschland – und stellen jedem Kunden einen KI-Agenten zur Seite, der alles aktuell hält.",
                      btn_book(ctx) + btn_wa(ctx), stats)
            + f"""
<section class="section section--deep">
  <div class="wrap">
    {sh('Unsere Idee: Vermehrung, Verbesserung, Verwaltung.', 'Ein Betrieb lebt von seinen Kundenbeziehungen. Deshalb sehen wir Website, System und Werbung nicht als einzelne Aufträge, sondern als Weg, den wir mit unseren Kunden gehen. Meist beginnt er mit einer neuen Website.', split=True)}
    {idea(ctx)}
  </div>
</section>
<section class="section"><div class="wrap">{sh('Wofür wir stehen', split=True)}{feats(values, 2, tone=["web", "crm", "ads", "ai"])}{ionos}</div></section>
""" + closing(ctx, "Lernen wir uns kennen.", "Im kostenfreien Erstgespräch.", "30 Minuten per Video, Telefon oder im Raum Hamburg bei Ihnen vor Ort. Sie erzählen von Ihrem Betrieb, wir sagen ehrlich, was sich lohnt. Ihr Angebot folgt innerhalb von 48 Stunden."))


def render_termin(ctx):
    return (page_hero(ctx, [("Start", "/"), ("Erstgespräch", "")], 'Buchen Sie Ihr <span class="quiet"><span class="nowrap">kostenfreies</span> Erstgespräch.</span>',
                      "Wählen Sie Ihr Anliegen und einen passenden Termin. Wir bereiten uns vor, bestätigen den Termin per E-Mail und schicken Ihnen danach innerhalb von 48 Stunden ein Angebot.")
            + f'<section class="section section--flush" id="termin"><div class="wrap">{booking_widget(ctx)}</div></section>')


def render_impressum(ctx):
    return page_hero(ctx, [("Start", "/"), ("Impressum", "")], "Impressum", "Angaben zum Anbieter dieser Website.") + f"""
<section class="section section--flush"><div class="wrap"><div class="prose">
  <h2>Angaben gemäß § 5 DDG</h2>
  <p>Medialyte – Marketing &amp; Management<br>Inhaber: {e(SITE['owner'])}<br>{e(SITE['street'])}<br>{e(SITE['zip'])} {e(SITE['city'])}</p>
  <h2>Kontakt</h2>
  <p>Telefon: <a href="tel:{SITE['phone_intl']}">{e(SITE['phone'])}</a><br>E-Mail: <a href="mailto:{SITE['email']}">{e(SITE['email'])}</a></p>
  <h2>Verbraucherstreitbeilegung / Universalschlichtungsstelle</h2>
  <p>Wir nehmen an einem Streitbeilegungsverfahren vor einer Verbraucherschlichtungsstelle teil. Zuständig ist die Universalschlichtungsstelle des Zentrums für Schlichtung e.V., Straßburger Straße 8, 77694 Kehl am Rhein (<a href="https://www.verbraucher-schlichter.de" target="_blank" rel="noopener">www.verbraucher-schlichter.de</a>).</p>
</div></div></section>"""


def render_legal(title, what, body):
    def r(ctx):
        return page_hero(ctx, [("Start", "/"), (title, "")], title, what) + body(ctx)
    return r


def render_404(ctx):
    return f"""
<section class="section"><div class="wrap notfound"><div style="display:grid;gap:20px;justify-items:center">
  <span class="notfound__n">404</span><h1 class="h2">Diese Seite gibt es nicht <span class="quiet">(mehr).</span></h1>
  <p class="lead">Vielleicht hilft Ihnen einer dieser Wege weiter.</p>
  <div class="hero__actions"><a class="btn btn--light" href="{ctx.u('/')}">Zur Startseite</a><a class="btn btn--ghost" href="{ctx.u('/termin/')}">Erstgespräch buchen</a></div>
</div></div></section>"""


def _svc_schema(name, path, desc):
    return {"@context": "https://schema.org", "@type": "Service", "name": name, "description": desc,
            "provider": {"@id": SITE["url"] + "/#org"}, "areaServed": {"@type": "Country", "name": "Deutschland"},
            "url": SITE["url"] + path}


def _after_dialog(ctx):
    return ref_dialog(ctx)


PAGES = [
    {"path": "/", "title": "Medialyte | Website, Kundenmanagement & KI-Agent – Digitalagentur Hamburg",
     "desc": "Medialyte baut Websites, die Kunden bringen, das Kundenmanagement-System dahinter und einen KI-Agenten für Änderungen per WhatsApp. Plus Werbung mit 200+ erfolgreichen Kampagnen. Für Betriebe in ganz Deutschland.",
     "og_title": "Medialyte | Ihre Website soll Kunden bringen. Nicht Arbeit machen.",
     "render": render_home, "after": _after_dialog, "priority": "1.0",
     "schema": [org_schema(), {"@context": "https://schema.org", "@type": "WebSite", "name": "Medialyte", "url": SITE["url"] + "/", "inLanguage": "de-DE", "publisher": {"@id": SITE["url"] + "/#org"}}, faq_schema(FAQ_MAIN)]},
    {"path": "/leistungen/website-erstellung/", "active": "leistungen",
     "title": "Website erstellen lassen – individuell, schnell & bei Google sichtbar | Medialyte",
     "desc": "Website erstellen lassen oder Relaunch: individuell für Ihre Zielgruppe, schnell, mobil und SEO-optimiert. Inklusive Hosting, Domain, SSL und KI-Agent für Änderungen per WhatsApp.",
     "render": render_web, "after": _after_dialog, "priority": "0.9",
     "schema": [_svc_schema("Website-Erstellung", "/leistungen/website-erstellung/", "Individuelle Websites und Relaunches für Betriebe aller Branchen."),
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
     "title": "Online-Marketing & Google Ads – 200+ erfolgreiche Kampagnen | Medialyte",
     "desc": "Google Ads, Social-Media-Werbung, SEO und Landingpages aus einer Hand, abgestimmt auf Ihre Website. Über 200 erfolgreiche Kampagnen. Jetzt kostenfreies Erstgespräch buchen.",
     "render": render_mkt, "priority": "0.8",
     "schema": [_svc_schema("Online-Marketing", "/leistungen/online-marketing/", "Google Ads, Social Media, SEO und Landingpages."),
                breadcrumb_schema([("Start", "/"), ("Online-Marketing", "/leistungen/online-marketing/")]), faq_schema(FAQ_MKT)]},
    {"path": "/referenzen/", "active": "referenzen",
     "title": "Referenzen & Projekte | Medialyte Digitalagentur",
     "desc": "Referenzen von Medialyte: RechnungsRadar, Juwelier Rubin, RITZ Instrument Transformers, Hubo d’Moran, FassadenTrio und mehr – mit Vorschau der ganzen Seite.",
     "render": render_refs, "after": _after_dialog, "priority": "0.8",
     "schema": [breadcrumb_schema([("Start", "/"), ("Referenzen", "/referenzen/")])]},
    {"path": "/ueber-uns/", "active": "ueber-uns",
     "title": "Über uns – wie Medialyte arbeitet | Digitalagentur Hamburg",
     "desc": "Medialyte ist eine Digitalagentur aus Hamburg für Websites, Kundenmanagement-Systeme, KI-Agenten und Online-Marketing. Wofür wir stehen und wie wir mit Ihnen arbeiten.",
     "render": render_about, "priority": "0.6",
     "schema": [breadcrumb_schema([("Start", "/"), ("Über uns", "/ueber-uns/")])]},
    {"path": "/termin/",
     "title": "Kostenfreies Erstgespräch buchen | Medialyte",
     "desc": "Buchen Sie Ihr kostenfreies Erstgespräch mit Medialyte: Anliegen wählen, Termin aussuchen, fertig. Per Video-Call, Telefon oder im Raum Hamburg bei Ihnen vor Ort.",
     "render": render_termin, "priority": "0.9",
     "schema": [breadcrumb_schema([("Start", "/"), ("Erstgespräch buchen", "/termin/")])]},
    {"path": "/impressum/", "title": "Impressum | Medialyte", "desc": "Impressum von Medialyte – Marketing & Management, Hamburg.",
     "render": render_impressum, "priority": "0.2", "robots": "noindex, follow"},
    {"path": "/datenschutz/", "title": "Datenschutzerklärung | Medialyte", "desc": "Datenschutzerklärung von Medialyte: kein Tracking, keine Cookies. Welche Daten wir beim Buchen eines Erstgesprächs und bei Kontakt per E-Mail, Telefon oder WhatsApp verarbeiten.",
     "render": render_legal("Datenschutzerklärung", "Welche Daten diese Website verarbeitet, wofür und welche Rechte Sie haben. Kurz gesagt: kein Tracking, keine Cookies.", legal.datenschutz), "priority": "0.2", "robots": "noindex, follow"},
    {"path": "/agb/", "title": "AGB | Medialyte", "desc": "Allgemeine Geschäftsbedingungen von Medialyte – Marketing & Management für Websites, Kundenmanagement-Systeme, KI-Agent und Online-Marketing.",
     "render": render_legal("Allgemeine Geschäftsbedingungen", "Die Bedingungen für alle Aufträge an Medialyte. Was genau Sie bekommen, steht zusätzlich in Ihrem persönlichen Angebot.", legal.agb), "priority": "0.2", "robots": "noindex, follow"},
    {"path": "/404.html", "title": "Seite nicht gefunden | Medialyte", "desc": "Diese Seite existiert nicht.",
     "render": render_404, "sitemap": False, "robots": "noindex, follow"},
]
