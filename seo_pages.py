"""Zusätzliche Seiten für die Sichtbarkeit bei Google.

- /leistungen/ (Übersicht) und sechs weitere Leistungsseiten
- /branchen/ (Übersicht) und acht Branchenseiten
- /webdesign-hamburg/ (lokale Seite für Hamburg)
- /kontakt/ und /faq/
- /ratgeber/ (Übersicht) und Ratgeber-Artikel

Jede Seite beantwortet eine eigene Suchanfrage („Website für Handwerker“, „Google Ads Agentur“,
„Website Relaunch Checkliste“ …) und verlinkt auf passende Nachbarseiten. Inhalte bewusst nur mit
belegbaren Angaben: keine erfundenen Zahlen, Preise oder Kundenstimmen.
"""
from build import BRANCHEN, SERVICES, SERVICES_MORE, SITE, breadcrumb_schema, e, faq_schema, icon
import mocks
from parts import (FAQ_MAIN, btn_book, btn_wa, cases, closing, faq_block, feats, frame_img, page_hero, process, sh,
                   ticks)
import re

import pages


# ======================================================================= Bausteine
def tiles(ctx, items, cols=3):
    """Verlinkte Kacheln: (Pfad, Symbol, Farbe, Titel, Text)."""
    lis = "".join(
        f'<li data-reveal style="--rd:{i % cols}"><a class="tile" href="{ctx.u(p)}"><span class="ic{" ic--" + tn if tn else ""}">{icon(ic)}</span>'
        f'<b>{t}</b><small>{d}</small><span class="tile__go" aria-hidden="true">{icon("arrow")}</span></a></li>'
        for i, (p, ic, tn, t, d) in enumerate(items))
    return f'<ul class="tiles{" tiles--2" if cols == 2 else ""}">{lis}</ul>'


def related(ctx, title, items, lead="", deep=False):
    return (f'<section class="section{" section--deep" if deep else ""}"><div class="wrap">'
            f'{sh(title, lead, split=bool(lead))}{tiles(ctx, items)}</div></section>')


ALL_SERVICES = [  # Pfad, Symbol, Farbe, Titel, Kurztext
    ("/leistungen/website-erstellung/", "globe", "web", "Website-Erstellung", "Neue Website, gemacht für Ihre Kunden"),
    ("/leistungen/website-relaunch/", "refresh", "web", "Website-Relaunch", "Die alte Seite neu – ohne Google-Platzierungen zu verlieren"),
    ("/leistungen/online-shop/", "bag", "web", "Online-Shop", "Produkte online verkaufen, sauber angebunden"),
    ("/leistungen/landingpage/", "layout", "web", "Landingpage", "Eine Seite, eine Aufgabe: Anfragen"),
    ("/leistungen/kundenmanagement-system/", "db", "crm", "Kundenmanagement-System", "Eigenes CRM und Dashboard nach Maß"),
    ("/leistungen/ki-agent/", "bot", "ai", "KI-Agent", "Website ändern per WhatsApp oder im Dashboard"),
    ("/leistungen/online-marketing/", "mega", "ads", "Online-Marketing", "Werbung und Sichtbarkeit aus einer Hand"),
    ("/leistungen/seo/", "search", "ads", "SEO", "Bei Google gefunden werden – auch lokal"),
    ("/leistungen/google-ads/", "target", "ads", "Google Ads", "Anzeigen genau dann, wenn Kunden suchen"),
    ("/leistungen/social-media-marketing/", "camera", "ads", "Social-Media-Marketing", "Instagram, Facebook, TikTok und LinkedIn"),
]
_SVC = {p: (p, ic, tn, t, d) for p, ic, tn, t, d in ALL_SERVICES}
_SVC["/webdesign-hamburg/"] = ("/webdesign-hamburg/", "pin", "web", "Webdesign Hamburg", "Persönlich vor Ort im Raum Hamburg")


def svc_tiles(*paths):
    return [_SVC[p] for p in paths]


RELATED_CORE = {  # „Passt dazu“ auf den vier Hauptleistungsseiten
    "Website-Erstellung": svc_tiles("/leistungen/website-relaunch/", "/leistungen/online-shop/", "/leistungen/landingpage/",
                                    "/leistungen/seo/", "/webdesign-hamburg/", "/leistungen/ki-agent/"),
    "Kundenmanagement-System": svc_tiles("/leistungen/ki-agent/", "/leistungen/website-erstellung/", "/leistungen/online-shop/"),
    "KI-Agent": svc_tiles("/leistungen/website-erstellung/", "/leistungen/kundenmanagement-system/", "/leistungen/website-relaunch/"),
    "Online-Marketing": svc_tiles("/leistungen/google-ads/", "/leistungen/seo/", "/leistungen/social-media-marketing/",
                                  "/leistungen/landingpage/", "/leistungen/online-shop/", "/webdesign-hamburg/"),
}


def branch_tiles(skip=""):
    return [(p, ic, "", n, s) for p, n, s, ic in BRANCHEN if p != skip]


def svc_schema(name, path, desc, service_type=None):
    s = {"@context": "https://schema.org", "@type": "Service", "name": name, "description": desc,
         "provider": {"@id": SITE["url"] + "/#org"}, "areaServed": {"@type": "Country", "name": "Deutschland"},
         "url": SITE["url"] + path}
    if service_type:
        s["serviceType"] = service_type
    return s


def site_visual(key):
    """Beispiel-Website eines erfundenen Betriebs aus dem Cockpit (als Beispiel gekennzeichnet)."""
    b = mocks.BRANCHES[key]
    return f"""<figure class="bvis" aria-label="Beispiel-Website">
  <div class="st__frame"><div class="frame__bar"><i></i><i></i><i></i><span class="frame__url">{icon('lock')}{e(b['host'])}</span></div>
  <div class="cp-site__view bvis__view">{mocks.mini_site(key, " ms--on")}</div></div>
  <figcaption>Beispiel-Website eines erfundenen Betriebs</figcaption>
</figure>"""


def ref_visual(ctx, key, host, alt):
    return f'<div class="bvis">{frame_img(ctx, f"img/refs/{key}-long.webp", 1200, 2400, host, alt, lazy=False)}</div>'


# ======================================================================= Leistungen: Übersicht
def render_leistungen(ctx):
    core = [_SVC[p] for p, *_ in SERVICES]
    more = [s for s in ALL_SERVICES if s[0] not in {p for p, *_ in SERVICES}]
    return (page_hero(ctx, [("Start", "/"), ("Leistungen", "")], 'Alle Leistungen. <span class="quiet">Aus einer Hand.</span>',
                      "Website, Kundenmanagement-System, KI-Agent und Online-Marketing: Wir bauen, was Ihr Betrieb für neue Kunden braucht, und betreuen es danach weiter. Mit einem festen Ansprechpartner und einem Angebot innerhalb von 48 Stunden.",
                      btn_book(ctx) + btn_wa(ctx))
            + f'<section class="section section--flush"><div class="wrap">{sh("Die vier Bausteine", "Die meisten Kunden starten mit einer neuen Website. Danach bauen wir weiter – so weit, wie es sich für Ihren Betrieb lohnt.", split=True)}{tiles(ctx, core, 2)}</div></section>'
            + related(ctx, "Spezialisierte Leistungen", more, "Für einzelne Aufgaben gibt es eigene Seiten mit allen Details.", deep=True)
            + f'<section class="section"><div class="wrap">{sh("So läuft ein Projekt ab", "Klar geplant und ohne Fachchinesisch – vom Erstgespräch bis zur laufenden Betreuung.", split=True)}{process()}</div></section>'
            + related(ctx, "Leistungen für Ihre Branche", branch_tiles(), "Was eine Website leisten muss, hängt von der Branche ab. Für jede gibt es eine eigene Seite.", deep=True)
            + closing(ctx))


# ======================================================================= Weitere Leistungsseiten
SUB_SERVICES = {
    "/leistungen/website-relaunch/": {
        "crumb": "Website-Relaunch", "ask": "web-besser", "tone": "web", "icon": "refresh",
        "title": "Website-Relaunch ohne Ranking-Verlust | Medialyte",
        "desc": "Website-Relaunch: Ihre Seite wird modern, schnell und mobil – mit Übernahme der Inhalte und 301-Weiterleitungen, damit Platzierungen bleiben.",
        "h1": 'Website-Relaunch – <span class="quiet">neu, ohne bei Google zu verlieren.</span>',
        "lead": "Ihre Website ist in die Jahre gekommen, lädt langsam oder sieht auf dem Smartphone nicht gut aus? Wir bringen sie auf den neuesten Stand, übernehmen Ihre Inhalte und sorgen mit sauberen Weiterleitungen dafür, dass Sie bei Google nicht von vorn anfangen.",
        "visual": "relaunch",
        "why": ("Wann sich ein Relaunch lohnt", "Eine Website altert schneller, als man denkt. Diese Anzeichen sprechen für einen Neustart:"),
        "feats": [
            ("mobile", "Schwach auf dem Smartphone", "Texte zu klein, Knöpfe zu eng, Bilder verrutscht: Die meisten Besucher kommen über das Handy und springen ab."),
            ("clock", "Lange Ladezeiten", "Jede Sekunde Warten kostet Besucher. Alte Themes und viele Plugins bremsen die Seite aus."),
            ("inbox", "Kaum Anfragen", "Besucher kommen, aber melden sich nicht. Oft fehlt ein klarer Weg zur Anfrage."),
            ("lock", "Technik veraltet", "Ungepflegte Systeme und Plugins sind ein Sicherheitsrisiko und machen jede Änderung mühsam."),
            ("pen", "Passt nicht mehr zu Ihnen", "Ihr Betrieb hat sich weiterentwickelt, die Website ist stehen geblieben."),
            ("search", "Bei Google unsichtbar", "Fehlende Seitentitel, keine Struktur, keine lokalen Signale: Die Seite wird kaum gefunden."),
        ],
        "split": ("So bleiben Ihre Platzierungen erhalten", "Bei einem Relaunch steckt das Risiko nicht im Design, sondern in den Adressen. Ändern sich die Adressen Ihrer Seiten ohne Weiterleitung, laufen Links und Google-Platzierungen ins Leere. Deshalb planen wir den Umzug Seite für Seite.",
                  ["Bestandsaufnahme aller bisherigen Seiten und Adressen", "Inhalte übernehmen, überarbeiten und ergänzen", "301-Weiterleitungen von jeder alten auf die passende neue Adresse", "Testversion, die Google nicht sieht, bis alles passt", "Sitemap und Kontrolle in der Google Search Console nach dem Livegang"]),
        "process": [("Analyse", "Wir prüfen Ihre bisherige Seite, Ihre Mitbewerber und Ihre Google-Daten."),
                    ("Konzept und Design", "Neue Struktur, neues Design – Sie sehen den Entwurf, bevor wir bauen."),
                    ("Umsetzung und Umzug", "Inhalte, Weiterleitungen, Tests auf allen Geräten."),
                    ("Livegang und Kontrolle", "Wir beobachten Platzierungen und Fehlermeldungen in den ersten Wochen.")],
        "case": "rechnungsradar", "case_title": ("Ein Relaunch, der sich gelohnt hat", "Nach dem Relaunch von RechnungsRadar stiegen die Kundenanfragen um 230 Prozent."),
        "faqs": [
            ("Verliere ich bei einem Relaunch meine Google-Platzierungen?", "<p>Nicht, wenn der Umzug sauber geplant ist. Wir leiten jede alte Adresse per 301-Weiterleitung auf die passende neue Seite um, übernehmen gute Inhalte und reichen die neue Sitemap bei Google ein. Kurzfristige Schwankungen sind normal, der Grundstock bleibt erhalten.</p>"),
            ("Kann ich meine Domain und meine E-Mail-Adressen behalten?", "<p>Ja. Ihre Domain bleibt Ihre Domain. Wir stellen nur die Website um, Ihre E-Mail-Postfächer laufen weiter wie bisher.</p>"),
            ("Brauche ich wieder WordPress?", "<p>Nein. Wir bauen schlanke Websites ohne Plugin-Ballast. Änderungen erledigen Sie per WhatsApp über den KI-Agenten oder im eigenen Dashboard – ganz ohne Backend-Kenntnisse.</p>"),
            ("Wie lange dauert ein Relaunch?", "<p>Eine übersichtliche Website ist meist in zwei bis vier Wochen fertig. Bei vielen Unterseiten, einem Shop oder einem System dahinter planen wir den Zeitplan gemeinsam.</p>"),
        ],
        "rel": ["/leistungen/website-erstellung/", "/leistungen/seo/", "/leistungen/ki-agent/"],
        "rag": ["/ratgeber/website-relaunch-checkliste/", "/ratgeber/was-kostet-eine-website/"],
    },
    "/leistungen/online-shop/": {
        "crumb": "Online-Shop", "ask": "web-neu", "tone": "web", "icon": "bag",
        "title": "Online-Shop erstellen lassen | Medialyte",
        "desc": "Online-Shop erstellen lassen: hochwertig gestaltet, schnell und mobil – mit Zahlung, Versand, Produktverwaltung und Betreuung.",
        "h1": 'Online-Shop erstellen lassen – <span class="quiet">der verkauft, nicht nur zeigt.</span>',
        "lead": "Ihr Sortiment verdient mehr als einen Shop von der Stange. Wir gestalten und bauen Online-Shops, die Ihre Marke hochwertig zeigen, auf dem Smartphone einfach zu bedienen sind und sich ohne Aufwand pflegen lassen.",
        "why": ("Was ein guter Shop braucht", "Ein Shop verkauft nur, wenn Vertrauen, Tempo und Bedienung stimmen."),
        "feats": [
            ("pen", "Gestaltung mit Wiedererkennung", "Produktseiten, die so wirken wie Ihr Laden oder Ihre Marke – statt wie jedes andere Template."),
            ("mobile", "Einkaufen mit dem Daumen", "Filter, Warenkorb und Kasse sind auf dem Smartphone mit wenigen Tipps erledigt."),
            ("shield", "Zahlung und Vertrauen", "Gängige Zahlarten, klare Versandinfos und Rechtstexte an der richtigen Stelle."),
            ("layers", "Produkte zentral pflegen", "Varianten, Preise und Bestände an einem Ort – auf Wunsch angebunden an Ihr eigenes System."),
            ("zap", "Schnell geladen", "Schlanke Seiten und optimierte Bilder, damit niemand im Warenkorb wartet."),
            ("trend", "Bereit für Werbung", "Saubere Produktdaten und Messung, damit Google Ads und Social Media verkaufen statt nur Klicks bringen."),
        ],
        "split": ("Plattform nach Bedarf", "Nicht jeder Shop braucht dasselbe. Für viele Händler ist eine bewährte Shop-Plattform wie Shopify die beste Wahl. Wer besondere Abläufe hat, etwa Anfragen statt Kauf oder tausende technische Produkte, bekommt eine eigene Lösung – wie den Produktfinder in unserem Website-Entwurf für RITZ.",
                  ["Beratung, welche Lösung zu Sortiment und Abläufen passt", "Gestaltung und Einrichtung inklusive Produktimport", "Anbindung an Zahlung, Versand und Ihr System", "Betreuung und Kampagnen nach dem Start"]),
        "process": [("Erstgespräch", "Sortiment, Zielgruppe und Abläufe verstehen."),
                    ("Konzept und Design", "Startseite, Kategorien und Produktseiten im Entwurf."),
                    ("Einrichtung", "Produkte, Zahlung, Versand und Rechtstexte."),
                    ("Start und Wachstum", "Livegang, Kampagnen und laufende Optimierung.")],
        "case": "rubin", "case_title": ("Hochwertige Produktwelten", "Für Juwelier Rubin präsentieren wir Trauringe, Schmuck und Uhren so hochwertig wie in der Vitrine."),
        "extra_ref": ("DELUXE Design", "E-Commerce", "Hochwertiger Online-Shop auf Shopify für eine Luxusmarke."),
        "faqs": [
            ("Welche Shop-Plattform nutzen Sie?", "<p>Das hängt von Ihrem Sortiment und Ihren Abläufen ab. Für viele Händler empfehlen wir Shopify, für besondere Anforderungen bauen wir eigene Lösungen. Im Erstgespräch sagen wir Ihnen ehrlich, was für Sie sinnvoll ist.</p>"),
            ("Kann ich Produkte selbst pflegen?", "<p>Ja. Produkte, Preise und Bestände pflegen Sie selbst – oder Sie schicken Änderungen per WhatsApp an den KI-Agenten.</p>"),
            ("Übernehmen Sie Produkte aus meinem bisherigen Shop?", "<p>Ja. Wir übernehmen Produkte, Bilder und Texte und richten Weiterleitungen ein, damit bestehende Links und Platzierungen erhalten bleiben.</p>"),
            ("Machen Sie auch Werbung für den Shop?", "<p>Ja. Google Ads, Social-Media-Kampagnen und SEO gehören zu unseren Leistungen. Dafür bauen wir den Shop von Anfang an so, dass Verkäufe sauber gemessen werden.</p>"),
        ],
        "rel": ["/leistungen/google-ads/", "/leistungen/social-media-marketing/", "/leistungen/kundenmanagement-system/"],
        "rag": ["/ratgeber/was-kostet-eine-website/"],
    },
    "/leistungen/landingpage/": {
        "crumb": "Landingpage", "ask": "werbung", "tone": "web", "icon": "layout",
        "title": "Landingpage erstellen lassen | Medialyte",
        "desc": "Landingpage erstellen lassen: eine Seite für ein Ziel – Anfragen, Anrufe oder Buchungen. Abgestimmt auf Google Ads und Social Media.",
        "h1": 'Landingpages, <span class="quiet">die aus Klicks Anfragen machen.</span>',
        "lead": "Wer auf eine Anzeige klickt, will genau das finden, was die Anzeige verspricht. Eine Landingpage hat deshalb nur eine Aufgabe: aus Besuchern Anfragen, Anrufe oder Buchungen zu machen. Wir bauen sie passend zu Ihrer Kampagne – und messen, was sie bringt.",
        "why": ("Was eine gute Landingpage ausmacht", "Keine Ablenkung, ein klarer nächster Schritt und Argumente, die genau diese Zielgruppe überzeugen."),
        "feats": [
            ("target", "Ein Angebot, ein Ziel", "Die Seite spricht genau ein Angebot an und führt zu genau einer Handlung."),
            ("quote", "Die Sprache Ihrer Kunden", "Überschrift und Texte greifen auf, wonach Ihre Zielgruppe sucht und was sie zögern lässt."),
            ("sliders", "Interaktive Elemente", "Vorher-nachher-Regler, Rechner oder kurze Fragebögen machen Lust auf die Anfrage."),
            ("phone", "Kurzer Weg zum Kontakt", "Anruf, WhatsApp, Formular oder Terminbuchung – sichtbar ab dem ersten Blick."),
            ("pie", "Messbar bis zur Anfrage", "Sie sehen, welche Anzeige und welche Seite wirklich Anfragen bringt."),
            ("zap", "Schnell und mobil", "Werbeklicks kommen meist vom Handy. Die Seite ist sofort da und dort am besten."),
        ],
        "split": ("Beispiel: FassadenTrio", "Für den Fassadenreiniger FassadenTrio haben wir eine Google-Ads-Kampagne mit eigener Landingpage aufgebaut: mit Vorher-nachher-Regler, klarem Ablauf in vier Schritten, häufigen Fragen und einem Fassaden-Check-Rechner, der Interessenten direkt zur Anfrage führt.",
                  ["Kampagne und Seite aus einer Hand", "Vorher-nachher-Regler und Rechner", "Ablauf und Fragen, die Zweifel ausräumen", "Saubere Messung von Anrufen und Anfragen"]),
        "process": [("Ziel festlegen", "Welche Handlung soll die Seite auslösen – und bei wem?"),
                    ("Texte und Aufbau", "Argumente, Beweise und ein klarer nächster Schritt."),
                    ("Umsetzung und Messung", "Seite bauen, Messung einrichten, mit der Kampagne verbinden."),
                    ("Optimieren", "Anhand der Zahlen verbessern wir Texte, Aufbau und Anzeigen.")],
        "faqs": [
            ("Was ist der Unterschied zwischen Website und Landingpage?", "<p>Eine Website stellt Ihren ganzen Betrieb vor. Eine Landingpage konzentriert sich auf ein einziges Angebot und ein einziges Ziel, meist passend zu einer Werbekampagne. Viele Betriebe haben beides.</p>"),
            ("Brauche ich für jede Kampagne eine eigene Landingpage?", "<p>Für jedes Angebot mit eigener Zielgruppe lohnt sich meist eine eigene Seite. Wir sagen Ihnen im Erstgespräch, wie viele sinnvoll sind.</p>"),
            ("Kann die Landingpage unter meiner Domain laufen?", "<p>Ja, zum Beispiel als Unterseite Ihrer Website oder unter einer eigenen Adresse. Das stimmen wir mit Ihnen ab.</p>"),
        ],
        "rel": ["/leistungen/google-ads/", "/leistungen/social-media-marketing/", "/leistungen/online-marketing/"],
        "rag": [],
    },
    "/leistungen/seo/": {
        "crumb": "SEO", "ask": "werbung", "tone": "ads", "icon": "search",
        "title": "SEO & lokale Suchmaschinenoptimierung | Medialyte",
        "desc": "Suchmaschinenoptimierung: technisches SEO, Inhalte, Google-Unternehmensprofil und lokales SEO – damit Ihr Betrieb bei Google gefunden wird.",
        "h1": 'SEO – <span class="quiet">damit Kunden Sie bei Google finden.</span>',
        "lead": "Wer bei Google nicht auf der ersten Seite steht, wird kaum gefunden. Wir sorgen dafür, dass Ihre Website technisch sauber ist, die richtigen Suchbegriffe beantwortet und in Ihrer Region sichtbar wird – mit einem gepflegten Google-Unternehmensprofil.",
        "why": ("Was wir für Ihre Sichtbarkeit tun", "SEO ist kein Trick, sondern Handwerk: Technik, Inhalte und lokale Signale müssen zusammenpassen."),
        "feats": [
            ("code", "Technisches SEO", "Schnelle Ladezeiten, saubere Struktur, Sitemap, strukturierte Daten und fehlerfreie Weiterleitungen."),
            ("search", "Suchbegriffe und Inhalte", "Wir finden heraus, wonach Ihre Kunden suchen, und bauen Seiten, die genau diese Fragen beantworten."),
            ("pin", "Lokales SEO", "Gepflegtes Google-Unternehmensprofil, einheitliche Firmendaten und Seiten für Ihre Region."),
            ("star", "Bewertungen", "Ein einfacher Ablauf, mit dem zufriedene Kunden Sie bei Google bewerten – und Antworten, die Vertrauen schaffen."),
            ("layers", "Interne Verlinkung", "Eine klare Seitenstruktur, die Google zeigt, was wichtig ist – und die Chance auf Unterseiten in den Suchergebnissen erhöht."),
            ("pie", "Messen und nachsteuern", "Mit der Google Search Console sehen wir, für welche Begriffe Sie erscheinen, und verbessern gezielt."),
        ],
        "split": ("SEO beginnt mit der Website", "Viele SEO-Maßnahmen verpuffen, weil die Website selbst bremst: langsame Technik, fehlende Seiten für wichtige Leistungen, keine klare Struktur. Weil wir Websites selbst bauen, können wir genau dort ansetzen – statt nur Berichte zu schreiben.",
                  ["Eigene Seiten für Ihre wichtigsten Leistungen und Regionen", "Seitentitel und Beschreibungen, die zum Klicken einladen", "Strukturierte Daten für Leistungen, Fragen und Brotkrümel", "Pflege des Google-Unternehmensprofils"]),
        "process": [("SEO-Check", "Technik, Inhalte, Mitbewerber und Ihr Google-Unternehmensprofil."),
                    ("Plan", "Welche Seiten und Begriffe den größten Hebel haben."),
                    ("Umsetzung", "Technik verbessern, Seiten anlegen, Profil pflegen."),
                    ("Messen", "Regelmäßiger Bericht, der ohne Fachwissen verständlich ist.")],
        "faqs": [
            ("Wie lange dauert es, bis SEO wirkt?", "<p>Erste Verbesserungen zeigen sich oft nach einigen Wochen, wenn Google die neuen Seiten erfasst hat. Stabile Platzierungen für umkämpfte Begriffe brauchen meist mehrere Monate. Wer schneller sichtbar sein will, kombiniert SEO mit Google Ads.</p>"),
            ("Können Sie Platz 1 bei Google garantieren?", "<p>Nein – und niemand kann das seriös. Google entscheidet selbst über die Reihenfolge. Wir sorgen dafür, dass Ihre Website alle Voraussetzungen erfüllt, und messen transparent, wie sich Ihre Sichtbarkeit entwickelt.</p>"),
            ("Was ist lokales SEO?", "<p>Lokales SEO sorgt dafür, dass Sie bei Suchen wie „Tischler in der Nähe“ oder „Zahnarzt Eimsbüttel“ erscheinen – in den normalen Ergebnissen und in Google Maps. Wichtig sind ein vollständiges Google-Unternehmensprofil, einheitliche Firmendaten und Bewertungen.</p>"),
            ("Kann ich bestimmen, welche Unterseiten bei Google unter meinem Eintrag erscheinen?", "<p>Nicht direkt – Google wählt diese Unterseiten-Links selbst aus. Eine klare Seitenstruktur, aussagekräftige Seitentitel und gute interne Verlinkung erhöhen aber die Chance deutlich, dass Google mehrere Ihrer wichtigsten Seiten zeigt.</p>"),
        ],
        "rel": ["/leistungen/google-ads/", "/leistungen/website-relaunch/", "/webdesign-hamburg/"],
        "rag": ["/ratgeber/google-unternehmensprofil-optimieren/", "/ratgeber/website-relaunch-checkliste/"],
    },
    "/leistungen/google-ads/": {
        "crumb": "Google Ads", "ask": "werbung", "tone": "ads", "icon": "target",
        "title": "Google Ads Agentur – Anzeigen mit Anfragen | Medialyte",
        "desc": "Google Ads: Suchanzeigen, Performance Max und lokale Kampagnen mit Messung von Anrufen und Anfragen. Über 200 erfolgreiche Kampagnen.",
        "h1": 'Google Ads, <span class="quiet">die Anfragen bringen – nicht nur Klicks.</span>',
        "lead": "Mit Google Ads erscheinen Sie genau dann, wenn jemand nach Ihrer Leistung sucht. Wir planen, bauen und betreuen Ihre Kampagnen – mit klarer Zielgruppe, kontrolliertem Budget und sauberer Messung von Anrufen und Anfragen. Aus über 200 Kampagnen wissen wir, worauf es ankommt.",
        "visual": "campaign",
        "why": ("Was wir für Ihre Kampagne tun", "Gute Kampagnen entstehen aus drei Dingen: der richtigen Suche, der richtigen Seite und ehrlicher Messung."),
        "feats": [
            ("search", "Suchanzeigen", "Anzeigen für die Begriffe, mit denen Ihre Kunden nach Ihrer Leistung suchen."),
            ("pin", "Lokale Kampagnen", "Sichtbar in Ihrer Stadt oder Ihrem Einzugsgebiet – auch in Google Maps."),
            ("layers", "Performance Max", "Kampagnen über Suche, YouTube, Display und Maps hinweg, gesteuert über klare Ziele."),
            ("phone", "Anruf- und Anfragemessung", "Wir messen echte Anrufe, Formulare und Buchungen, nicht nur Klicks."),
            ("layout", "Passende Landingpages", "Jede Anzeige führt auf eine Seite, die genau ihr Versprechen hält."),
            ("sliders", "Laufende Optimierung", "Begriffe, Gebote und Anzeigen werden regelmäßig anhand der Zahlen verbessert."),
        ],
        "split": ("Erst messen, dann skalieren", "Viele Kampagnen verbrennen Budget, weil niemand weiß, welche Klicks zu Kunden werden. Deshalb richten wir zuerst die Messung ein – Anrufe, Formulare, Buchungen – und erhöhen das Budget erst dort, wo es nachweislich Anfragen bringt.",
                  ["Saubere Verknüpfung mit Google Analytics", "Anrufqualität prüfen statt nur Anrufe zählen", "Ausschlüsse für unpassende Suchbegriffe", "Monatlicher Bericht in verständlicher Sprache"]),
        "process": [("Analyse", "Zielgruppe, Suchbegriffe, Mitbewerber und Budget."),
                    ("Aufbau", "Kampagnen, Anzeigen, Landingpage und Messung."),
                    ("Start", "Kampagne geht live, wir beobachten die ersten Tage eng."),
                    ("Optimieren", "Laufende Verbesserung und monatlicher Bericht.")],
        "faqs": [
            ("Wie viel Budget brauche ich für Google Ads?", "<p>Das hängt von Ihrer Branche, Region und den Klickpreisen ab. Im Erstgespräch schätzen wir ein realistisches Startbudget. Das Werbebudget zahlen Sie direkt an Google, unsere Betreuung ist davon getrennt und steht transparent im Angebot.</p>"),
            ("Wie schnell bringt Google Ads Anfragen?", "<p>Anzeigen sind ab dem ersten Tag sichtbar. Die ersten Wochen nutzen wir, um zu lernen, welche Begriffe und Anzeigen wirklich Kunden bringen, und optimieren danach gezielt.</p>"),
            ("Was ist Performance Max?", "<p>Ein Kampagnentyp, bei dem Google Ihre Anzeigen automatisch über Suche, YouTube, Display, Gmail und Maps ausspielt. Er funktioniert gut, wenn Ziele und Messung sauber eingerichtet sind – genau darum kümmern wir uns.</p>"),
            ("Übernehmen Sie auch bestehende Kampagnen?", "<p>Ja. Wir prüfen Ihr bestehendes Konto, finden Budgetfresser und Messlücken und optimieren von dort aus weiter.</p>"),
        ],
        "rel": ["/leistungen/landingpage/", "/leistungen/seo/", "/leistungen/social-media-marketing/"],
        "rag": [],
    },
    "/leistungen/social-media-marketing/": {
        "crumb": "Social-Media-Marketing", "ask": "werbung", "tone": "ads", "icon": "camera",
        "title": "Social-Media-Marketing & Werbung | Medialyte",
        "desc": "Social-Media-Marketing: Strategie, Reels, Beiträge und Werbekampagnen auf Instagram, Facebook, TikTok und LinkedIn plus Community-Management.",
        "h1": 'Social Media, <span class="quiet">das Ihren Betrieb bekannt macht.</span>',
        "lead": "Instagram, Facebook, TikTok, LinkedIn und YouTube: Wir entwickeln Inhalte, die zu Ihrem Betrieb passen, schalten Kampagnen, die gezielt neue Kunden ansprechen, und kümmern uns um Ihre Community. Damit aus Reichweite Anfragen werden.",
        "why": ("Was wir übernehmen", "Von der Idee bis zur Auswertung – oder nur den Teil, der Ihnen fehlt."),
        "feats": [
            ("target", "Strategie und Redaktionsplan", "Welche Kanäle, welche Themen, wie oft – passend zu Ihrer Zielgruppe."),
            ("video", "Reels, Storys und Beiträge", "Kurze Videos mit starkem Einstieg, Motion Design und Bilder, die auffallen."),
            ("mega", "Werbekampagnen", "Anzeigen auf Instagram, Facebook, TikTok und LinkedIn, gezielt für neue Kunden."),
            ("users", "Community-Management", "Wir betreuen Kommentare und Nachrichten und bauen Beziehungen auf."),
            ("pen", "Einheitlicher Auftritt", "Ein Branding, an dem man Sie sofort erkennt – auf jedem Kanal."),
            ("pie", "Auswertung", "Sie sehen, welche Inhalte wirken und welche Kampagnen Anfragen bringen."),
        ],
        "split": ("Ein Video, viele Kanäle", "Ein gutes Reel funktioniert auch als YouTube Short, als TikTok und in Ihrem Google-Unternehmensprofil. Wir produzieren so, dass jeder Inhalt mehrfach arbeitet – im richtigen Format für Story, Beitrag und Anzeige.",
                  ["Hochkant- und Querformate aus einer Produktion", "Inhalte für Instagram, Facebook, TikTok, LinkedIn und YouTube", "Beiträge für Ihr Google-Unternehmensprofil", "Kampagnen, die auf Ihre Website oder Landingpage führen"]),
        "process": [("Kennenlernen", "Ihre Zielgruppe, Ihre Stärken, Ihre Kanäle."),
                    ("Plan", "Themen, Formate und Rhythmus."),
                    ("Produktion", "Videos, Bilder und Texte – Sie geben alles frei."),
                    ("Veröffentlichen und auswerten", "Posten, Kampagnen, Community und Bericht.")],
        "faqs": [
            ("Welche Social-Media-Kanäle lohnen sich für mich?", "<p>Das hängt von Ihrer Zielgruppe ab. Für Gastronomie und Handel sind oft Instagram und TikTok stark, für Industrie und Beratung eher LinkedIn. Wir empfehlen nur Kanäle, die zu Ihnen passen.</p>"),
            ("Muss ich selbst vor die Kamera?", "<p>Nein. Viele Inhalte funktionieren mit Produkten, Räumen, Animationen oder Ihrem Team. Wenn Sie möchten, begleiten wir Sie aber gern beim Dreh.</p>"),
            ("Ist das Werbebudget im Preis enthalten?", "<p>Nein. Das Werbebudget zahlen Sie direkt an die Plattform. Unsere Leistung für Inhalte, Kampagnen und Betreuung steht getrennt und transparent im Angebot.</p>"),
        ],
        "rel": ["/leistungen/online-marketing/", "/leistungen/google-ads/", "/leistungen/landingpage/"],
        "rag": [],
    },
}

def render_sub(path):
    d = SUB_SERVICES[path]

    def r(ctx):
        vis = {"relaunch": mocks.relaunch, "campaign": mocks.campaign}.get(d.get("visual"), lambda: "")()
        out = page_hero(ctx, [("Start", "/"), ("Leistungen", "/leistungen/"), (d["crumb"], "")], d["h1"], d["lead"],
                        btn_book(ctx, "Erstgespräch buchen", d["ask"]) + btn_wa(ctx), vis)
        out += f'<section class="section"><div class="wrap">{sh(d["why"][0], d["why"][1], split=True)}{feats(d["feats"], tone=d["tone"])}</div></section>'
        st, sp, sl = d["split"]
        out += (f'<section class="section section--deep"><div class="wrap split"><div class="split__text" data-reveal>'
                f'<h2 class="h2">{st}</h2><p>{sp}</p>{btn_book(ctx, "Erstgespräch buchen", d["ask"])}</div>'
                f'<div data-reveal>{ticks(sl)}</div></div></section>')
        out += f'<section class="section"><div class="wrap">{sh("So gehen wir vor", "Klar geplant, mit festem Ansprechpartner und ohne Fachchinesisch.", split=True)}{process([(t, x, []) for t, x in d["process"]], "proc--n")}</div></section>'
        if d.get("case"):
            ct, cl = d["case_title"]
            extra = ""
            if d.get("extra_ref"):
                n, c, x = d["extra_ref"]
                extra = f'<div class="more more--1"><article data-reveal><span class="case__cat">{e(c)}</span><h3>{e(n)}</h3><p>{e(x)}</p></article></div>'
            out += f'<section class="section section--deep"><div class="wrap">{sh(ct, cl, split=True)}{cases(ctx, (d["case"],))}{extra}</div></section>'
        out += f'<section class="section{"" if d.get("case") else " section--deep"}"><div class="wrap">{faq_block(ctx, d["faqs"], "Fragen zu " + d["crumb"])}</div></section>'
        rel = svc_tiles(*d["rel"]) + [rag_tile(p) for p in d.get("rag", [])]
        out += related(ctx, "Passt dazu", rel, deep=not d.get("case"))
        out += closing(ctx)
        return out
    return r


# ======================================================================= Branchen
BRANCH_PAGES = {
    "/branchen/gastronomie/": {
        "key": "gastro", "name": "Gastronomie", "crumb": "Gastronomie", "ask": "web-neu",
        "title": "Website für Restaurants, Cafés & Bars | Medialyte",
        "desc": "Website für Restaurants, Cafés und Bars: Speisekarte und Öffnungszeiten immer aktuell, Reservierung mit einem Tipp, Änderungen per WhatsApp.",
        "h1": 'Website für Restaurants, Cafés und Bars – <span class="quiet">aktuell ohne Aufwand.</span>',
        "lead": "Ihre Gäste suchen Sie bei Google, schauen auf die Speisekarte und wollen reservieren – meistens vom Handy. Wir bauen Ihnen eine Website, die genau das in Sekunden möglich macht. Und wenn sich der Mittagstisch ändert, schicken Sie einfach eine WhatsApp.",
        "pain": ("Was Gäste auf Ihrer Website suchen", "Speisekarte, Öffnungszeiten, Lage und ein Tisch – mehr braucht es nicht. Aber genau das muss stimmen."),
        "feats": [
            ("food", "Speisekarte, die immer stimmt", "Gerichte, Preise und Allergene übersichtlich, auf dem Handy gut lesbar – und schnell geändert."),
            ("calendar", "Reservieren mit einem Tipp", "Tisch, Uhrzeit, Personen: Gäste reservieren direkt auf Ihrer Website, Sie bekommen alles gebündelt."),
            ("clock", "Öffnungszeiten ohne Rätsel", "Ruhetage, Feiertage und Betriebsferien stehen richtig auf der Website und bei Google."),
            ("camera", "Bilder, die Appetit machen", "Ihre Gerichte und Ihre Räume, groß und schnell geladen."),
            ("pin", "Gefunden werden in Ihrer Gegend", "Lokales SEO und ein gepflegtes Google-Unternehmensprofil für Suchen wie „Italiener in der Nähe“."),
            ("spark", "Events und Aktionen", "Weinabend, Brunch, Mittagstisch: Ankündigungen sind in einer Nachricht online."),
        ],
        "sys": ("Reservierungen an einem Ort", "Reservierungen von der Website, Anrufe über Google und Anfragen für Feiern landen gesammelt in Ihrem Dashboard. Gäste erhalten automatisch eine Bestätigung – Sie sehen auf einen Blick, wie voll der Abend wird.",
                ["Reservierungen und Anfragen gebündelt", "Automatische Bestätigung für Ihre Gäste", "Anfragen für Feiern und Catering im Überblick", "Wochenzahlen auf einen Blick"]),
        "msgs": [("food", "Mittagstisch", "Heute gibt’s Kürbisrisotto als Mittagstisch, 12,50 €. Kannst du das auf die Website setzen?"),
                 ("clock", "Ruhetag", "Am Montag, 24.12., haben wir geschlossen. Bitte bei den Öffnungszeiten eintragen."),
                 ("spark", "Event", "Am Freitag ist Weinabend ab 19 Uhr, bitte groß auf die Startseite.")],
        "faqs": [
            ("Kann ich die Speisekarte selbst ändern?", "<p>Ja – am einfachsten per WhatsApp: Schicken Sie dem KI-Agenten die neue Karte als Foto oder Text, er setzt sie auf der Website um. Auch ein neuer Mittagstisch ist so in einer Nachricht online.</p>"),
            ("Brauche ich ein Reservierungssystem eines Anbieters?", "<p>Nicht unbedingt. Wir bauen die Reservierung direkt in Ihre Website ein, Anfragen landen in Ihrem Dashboard. Nutzen Sie bereits ein Reservierungssystem, binden wir es ein.</p>"),
            ("Reicht nicht ein Google-Eintrag?", "<p>Ein gepflegter Google-Eintrag ist wichtig, ersetzt aber keine eigene Website. Auf Ihrer Seite bestimmen Sie, wie Ihr Restaurant wirkt, zeigen die ganze Karte und nehmen Reservierungen ohne Provision entgegen. Und beides zusammen wird besser gefunden.</p>"),
            ("Wie schnell ist die Website online?", "<p>Eine Restaurant-Website ist meist in zwei bis vier Wochen fertig – inklusive Domain, Hosting und SSL.</p>"),
        ],
    },
    "/branchen/handwerk/": {
        "key": "handwerk", "name": "Handwerk", "crumb": "Handwerk", "ask": "web-neu",
        "title": "Website für Handwerker – mehr Anfragen | Medialyte",
        "desc": "Website für Handwerksbetriebe: Projekte zeigen, Anfragen mit Fotos bekommen und in Ihrer Region bei Google gefunden werden. Pflege per WhatsApp.",
        "h1": 'Website für Handwerker – <span class="quiet">Anfragen mit Fotos, nicht nur Anrufe.</span>',
        "lead": "Ihre Arbeit spricht für sich – wenn man sie sieht. Wir bauen Websites für Handwerksbetriebe, die Ihre Projekte zeigen, in Ihrer Region gefunden werden und Anfragen so aufnehmen, dass Sie gleich wissen, worum es geht: mit Fotos, Maßen und Wunschtermin.",
        "pain": ("Was Ihre Kunden wissen wollen", "Machen die das, was ich brauche? Sind die gut? Sind die in meiner Nähe? Ihre Website beantwortet das in Sekunden."),
        "feats": [
            ("camera", "Projekte, die überzeugen", "Referenzen mit Bildern aus Ihrer Werkstatt und von der Baustelle – sortiert nach Leistung."),
            ("inbox", "Anfragen mit allen Angaben", "Kunden schicken Fotos, Maße und Wunschtermin gleich mit. Weniger Rückfragen, schnelleres Angebot."),
            ("pin", "Sichtbar in Ihrer Region", "Lokales SEO und Seiten für Ihr Einzugsgebiet – für Suchen wie „Tischler Lüneburg“."),
            ("phone", "Rückruf statt verpasster Anruf", "Wer Sie auf der Baustelle nicht erreicht, bucht einen Rückruf."),
            ("users", "Auch für Bewerber", "Ein Bereich für Ausbildung und Stellen – Fachkräfte suchen auch online."),
            ("star", "Bewertungen sichtbar", "Gute Bewertungen bei Google bauen Vertrauen auf, bevor der erste Anruf kommt."),
        ],
        "sys": ("Vom Anruf zum Auftrag – ohne Zettel", "Anfragen, Aufmaß-Termine, Angebote und Aufträge landen in Ihrem eigenen Dashboard. Sie sehen, was offen ist, Kunden bekommen Termine automatisch bestätigt und nichts geht mehr auf dem Beifahrersitz verloren.",
                ["Anfragen mit Fotos direkt im System", "Aufmaß-Termine mit automatischer Bestätigung", "Angebote mit wenigen Klicks", "Erinnerungen an offene Rückrufe"]),
        "msgs": [("hammer", "Betriebsurlaub", "Wir sind vom 23.12. bis 2.1. im Betriebsurlaub. Bitte einen Hinweis auf die Seite."),
                 ("camera", "Neues Projekt", "Hier sind fünf Fotos von der neuen Treppe in Eiche, bitte bei den Projekten ergänzen."),
                 ("users", "Stelle", "Wir suchen ab sofort einen Gesellen, bitte eine Stellenanzeige auf die Website.")],
        "faqs": [
            ("Lohnt sich eine Website, wenn wir eh ausgelastet sind?", "<p>Gerade dann: Eine gute Website bringt nicht nur mehr, sondern bessere Anfragen – mit allen Angaben und von Kunden, die zu Ihnen passen. Und sie hilft bei der Suche nach Fachkräften und Azubis.</p>"),
            ("Ich habe kaum Zeit für die Website. Wer pflegt sie?", "<p>Sie schicken Änderungen per WhatsApp – zum Beispiel neue Projektfotos von der Baustelle. Der KI-Agent setzt sie um. Um Technik, Updates und Sicherheit kümmern wir uns.</p>"),
            ("Werden wir in unserer Region gefunden?", "<p>Dafür sorgen wir mit lokalem SEO: Seitentitel mit Ihrer Region, ein gepflegtes Google-Unternehmensprofil und auf Wunsch Google Ads für Ihr Einzugsgebiet.</p>"),
            ("Können Anfragen direkt in unser System?", "<p>Ja. Mit einem Kundenmanagement-System landen Anfragen samt Fotos direkt im Dashboard – inklusive Terminplanung und Angeboten.</p>"),
        ],
    },
    "/branchen/praxen/": {
        "key": "praxis", "name": "Praxen", "crumb": "Praxen", "ask": "web-neu",
        "title": "Website für Arztpraxen & Zahnärzte | Medialyte",
        "desc": "Praxis-Website für Ärzte, Zahnärzte und Therapeuten: Sprechzeiten immer aktuell, Online-Termine rund um die Uhr, weniger Telefonate.",
        "h1": 'Website für Praxen – <span class="quiet">weniger Telefon, mehr Zeit für Patienten.</span>',
        "lead": "Das Telefon klingelt ständig, weil Patienten Sprechzeiten erfragen oder einen Termin wollen? Eine gute Praxis-Website nimmt Ihrem Team diese Arbeit ab: mit Sprechzeiten, die immer stimmen, Online-Terminen rund um die Uhr und allen Infos für neue Patientinnen und Patienten.",
        "pain": ("Was eine Praxis-Website leisten muss", "Sie entlastet die Anmeldung, schafft Vertrauen bei neuen Patienten und ist auf jedem Handy sofort verständlich."),
        "feats": [
            ("calendar", "Online-Termine", "Patienten buchen rund um die Uhr – bestehende Terminsysteme binden wir ein."),
            ("clock", "Sprechzeiten, die stimmen", "Urlaub, Vertretung und geänderte Zeiten sind in einer Nachricht aktualisiert."),
            ("users", "Team und Leistungen", "Wer behandelt was? Klare Seiten zu Ihren Schwerpunkten und Ihrem Team."),
            ("layout", "Formulare vorab", "Anamnesebogen und Unterlagen digital, bevor der Patient in der Praxis ist."),
            ("pin", "Gefunden im Stadtteil", "Lokales SEO für Suchen wie „Zahnarzt Eimsbüttel“ – plus gepflegtes Google-Profil."),
            ("shield", "Barrierearm und verständlich", "Gut lesbar, mit klaren Kontrasten und einfacher Sprache – für alle Altersgruppen."),
        ],
        "sys": ("Termine und Erinnerungen automatisch", "Online-Termine, Erinnerungen am Vortag und digitale Unterlagen laufen in einem System zusammen. Ihr Team sieht alles an einem Ort und muss weniger telefonieren.",
                ["Online-Termine mit automatischer Erinnerung", "Digitale Formulare vor dem Termin", "Hinweise bei Urlaub und Vertretung", "Weniger Anrufe an der Anmeldung"]),
        "msgs": [("clock", "Sprechzeiten", "Ab sofort ist Mittwochnachmittag geschlossen. Bitte die Sprechzeiten anpassen."),
                 ("calendar", "Urlaub", "Vom 2. bis 13. März sind wir im Urlaub, Vertretung macht die Praxis Dr. Lange."),
                 ("users", "Team", "Unsere neue Kollegin beginnt am 1. April, hier sind Foto und Schwerpunkte.")],
        "faqs": [
            ("Können Patienten direkt online Termine buchen?", "<p>Ja. Entweder über eine Terminbuchung, die wir in Ihre Website einbauen, oder über Ihr bestehendes Terminsystem, das wir einbinden.</p>"),
            ("Was ist bei einer Praxis-Website rechtlich zu beachten?", "<p>Für Heilberufe gelten besondere Regeln für Werbung und Pflichtangaben. Wir stimmen alle Inhalte mit Ihnen ab und bauen Impressum, Datenschutz und Formulare sauber ein. Die rechtliche Prüfung im Einzelfall ersetzt das nicht.</p>"),
            ("Wie halte ich Sprechzeiten und Urlaub aktuell?", "<p>Mit einer kurzen Nachricht an den KI-Agenten per WhatsApp. Er ändert die Zeiten auf der Website, auf Wunsch mit einem Hinweis, der nach dem Urlaub von selbst verschwindet.</p>"),
        ],
    },
    "/branchen/kanzleien/": {
        "key": "kanzlei", "name": "Kanzleien", "crumb": "Kanzleien", "ask": "web-neu",
        "title": "Website für Kanzleien & Steuerberater | Medialyte",
        "desc": "Kanzlei-Website für Rechtsanwälte und Steuerberater: Schwerpunkte klar erklärt, Erstberatung in wenigen Klicks, Mandate im eigenen Dashboard.",
        "h1": 'Website für Kanzleien – <span class="quiet">Kompetenz, die man in Sekunden versteht.</span>',
        "lead": "Mandantinnen und Mandanten suchen nicht nach einer Kanzlei, sondern nach einer Lösung für ihr Problem. Wir bauen Websites für Rechtsanwälte und Steuerberater, die Ihre Schwerpunkte verständlich erklären, Vertrauen schaffen und die Erstberatung so einfach machen wie möglich.",
        "pain": ("Was Mandanten überzeugt", "Klarheit statt Juristendeutsch, Gesichter statt Stockfotos und ein kurzer Weg zur Erstberatung."),
        "feats": [
            ("scale", "Schwerpunkte verständlich", "Für jedes Rechtsgebiet eine eigene Seite, die das Problem des Mandanten aufgreift – und bei Google gefunden wird."),
            ("users", "Ihr Team mit Gesicht", "Profile mit Foto, Schwerpunkten und Werdegang schaffen Vertrauen."),
            ("video", "Erstberatung anfragen", "Anliegen wählen, Termin vorschlagen, Video oder vor Ort – in wenigen Klicks."),
            ("lock", "Unterlagen sicher übermitteln", "Mandanten laden Dokumente direkt hoch, statt sie per E-Mail zu schicken."),
            ("pen", "Ratgeber-Inhalte", "Beiträge zu häufigen Fragen zeigen Kompetenz und bringen Besucher über Google."),
            ("search", "Gefunden für Ihr Fachgebiet", "Seiten und Begriffe für Suchen wie „Fachanwalt Arbeitsrecht Hamburg“."),
        ],
        "sys": ("Ihre eigene Mandantenverwaltung", "Bei umfangreicheren Abläufen bauen wir Ihnen ein eigenes Dashboard: Mandatsanfragen, Termine, Fristen und Unterlagen an einem Ort. Änderungen an der Website erledigen Sie dort ebenfalls – unterstützt vom KI-Agenten.",
                ["Mandatsanfragen strukturiert im System", "Termine für Erstberatungen mit Bestätigung", "Unterlagen sicher hochladen lassen", "Website-Änderungen direkt im Dashboard"]),
        "msgs": [("users", "Neue Kollegin", "Frau Becker ist neu im Team, bitte mit Foto und Schwerpunkten ergänzen."),
                 ("pen", "Ratgeber", "Hier ist ein Text zur neuen Rechtsprechung, bitte als Beitrag veröffentlichen."),
                 ("calendar", "Termine", "Erstberatungen gibt es ab sofort auch dienstags per Video.")],
        "case_ref": "rechnungsradar", "case_title": ("Überzeugt auch Steuerberater", "Für RechnungsRadar haben wir App und Website gebaut – mit deutlich mehr Anfragen von Steuerberatern nach dem Relaunch."),
        "faqs": [
            ("Dürfen Kanzleien überhaupt werben?", "<p>Ja, sachliche Information über Ihre Tätigkeit ist erlaubt. Für Rechtsanwälte und Steuerberater gelten aber berufsrechtliche Grenzen. Wir formulieren sachlich und stimmen jede Seite mit Ihnen ab – die berufsrechtliche Prüfung liegt bei Ihnen.</p>"),
            ("Wie bekomme ich Mandanten für bestimmte Rechtsgebiete?", "<p>Mit eigenen Seiten für jeden Schwerpunkt, die genau die Fragen Ihrer Zielgruppe beantworten. Ergänzend sorgen Google Ads für sofortige Sichtbarkeit bei passenden Suchen.</p>"),
            ("Können Mandanten Unterlagen über die Website schicken?", "<p>Ja. Wir bauen einen Upload ein, über den Dokumente direkt in Ihrem System landen – übersichtlicher und sicherer als unverschlüsselte E-Mails.</p>"),
        ],
    },
    "/branchen/einzelhandel/": {
        "key": "handel", "name": "Einzelhandel", "crumb": "Einzelhandel", "ask": "web-neu",
        "title": "Website für Einzelhandel & Geschäfte | Medialyte",
        "desc": "Website für Einzelhändler: Sortiment, Filialen und Aktionen immer aktuell, lokal bei Google gefunden, auf Wunsch mit Online-Shop.",
        "h1": 'Website für Einzelhändler – <span class="quiet">die Kunden in den Laden holt.</span>',
        "lead": "Bevor Kunden zu Ihnen kommen, schauen sie online nach: Was gibt es, wann ist geöffnet, wo ist die nächste Filiale? Wir bauen Websites und Online-Shops für den Handel, die Ihr Sortiment hochwertig zeigen und den Weg in den Laden so kurz wie möglich machen.",
        "visual_ref": ("rubin", "rubin-gold.de", "Website von Juwelier Rubin"),
        "pain": ("Was Ihre Kunden online erwarten", "Ein Blick ins Sortiment, aktuelle Öffnungszeiten und der schnellste Weg zu Ihnen."),
        "feats": [
            ("bag", "Sortiment in Szene gesetzt", "Produktwelten, die so wirken wie Ihr Schaufenster – mit Bildern in bester Qualität."),
            ("pin", "Filialfinder", "Mehrere Standorte? Kunden finden mit einem Klick die nächste Filiale mit Öffnungszeiten."),
            ("spark", "Aktionen und Neuheiten", "Neue Kollektion, Rabattaktion, verkaufsoffener Sonntag – in einer Nachricht online."),
            ("search", "Lokal gefunden", "Gepflegte Google-Unternehmensprofile für jede Filiale und Seiten für Ihre Stadt."),
            ("layers", "Auf Wunsch mit Shop", "Online verkaufen oder reservieren und im Laden abholen – je nach Sortiment."),
            ("calendar", "Termine für Beratung", "Für erklärungsbedürftige Produkte: Beratungstermine direkt online buchen."),
        ],
        "sys": ("Produkte zentral pflegen", "Für größere Sortimente bauen wir ein Produktmanagement: Artikel, Varianten und Bestände an einem Ort pflegen und auf der Website ausspielen – statt in mehreren Listen.",
                ["Produkte, Preise und Varianten zentral", "Aktionen planen und automatisch beenden", "Anfragen und Reservierungen im Überblick", "Anbindung an einen Online-Shop"]),
        "msgs": [("bag", "Neue Kollektion", "Die Herbstkollektion ist da. Hier sind sechs Fotos für die Startseite."),
                 ("clock", "Öffnungszeiten", "Am Sonntag haben wir verkaufsoffen von 13 bis 18 Uhr, bitte ankündigen."),
                 ("pin", "Filiale", "Die Filiale in Lüneburg hat ab Montag neue Öffnungszeiten, 10 bis 19 Uhr.")],
        "case_ref": "rubin", "case_title": ("Juwelier Rubin: vier Filialen, eine Website", "Trauringe, Schmuck und Uhren so hochwertig wie in der Vitrine – mit Filialfinder für Hamburg, Norderstedt und Lüneburg."),
        "faqs": [
            ("Brauche ich als Händler einen Online-Shop?", "<p>Nicht immer. Viele Händler profitieren schon davon, ihr Sortiment zu zeigen und Kunden in den Laden zu holen. Ein Shop lohnt sich, wenn Ihre Produkte gut versendbar sind und online gesucht werden. Wir beraten Sie ehrlich.</p>"),
            ("Wie zeige ich mehrere Filialen?", "<p>Mit einem Filialfinder und einer eigenen Seite je Standort – mit Adresse, Öffnungszeiten und Anfahrt. Jede Filiale bekommt außerdem ein gepflegtes Google-Unternehmensprofil.</p>"),
            ("Kann ich Aktionen selbst einstellen?", "<p>Ja. Schicken Sie dem KI-Agenten Bilder und Text per WhatsApp – die Aktion ist online und verschwindet auf Wunsch am Enddatum von selbst.</p>"),
        ],
    },
    "/branchen/dienstleister/": {
        "key": "dienst", "name": "Dienstleister", "crumb": "Dienstleister", "ask": "web-neu",
        "title": "Website für Dienstleister | Medialyte",
        "desc": "Website für Dienstleister wie Reinigung, Beauty, Events oder Beratung: Leistungen klar erklärt, Anfragen und Termine in wenigen Klicks.",
        "h1": 'Website für Dienstleister – <span class="quiet">vom ersten Klick zur Anfrage.</span>',
        "lead": "Ob Reinigung, Kosmetik, Eventdekoration oder Beratung: Wer eine Dienstleistung sucht, vergleicht schnell und entscheidet nach Gefühl. Wir bauen Websites, die Ihre Leistung auf den Punkt bringen, Vertrauen aufbauen und die Anfrage so einfach machen wie eine Nachricht.",
        "pain": ("Was Interessenten überzeugt", "Was genau bekomme ich, wie läuft es ab, was sagen andere – und wie erreiche ich Sie am schnellsten?"),
        "feats": [
            ("layout", "Leistungen auf den Punkt", "Jede Leistung mit eigener Seite, Ablauf und Antworten auf typische Fragen."),
            ("eye", "Vorher und nachher", "Ergebnisse zeigen statt beschreiben – zum Beispiel mit einem Vorher-nachher-Regler."),
            ("calendar", "Termine online buchen", "Für Termine wie Kosmetik oder Beratung: Kunden buchen direkt auf Ihrer Website."),
            ("sliders", "Rechner und Fragebögen", "Ein kurzer Check oder Rechner macht Lust auf die Anfrage und liefert Ihnen alle Angaben."),
            ("star", "Bewertungen und Referenzen", "Stimmen zufriedener Kunden an den Stellen, an denen gezögert wird."),
            ("wa", "WhatsApp, Anruf, Formular", "Der Kontaktweg, den Ihre Kunden bevorzugen – sichtbar auf jedem Bildschirm."),
        ],
        "sys": ("Anfragen, Termine und Aufträge im Griff", "Anfragen aus Website, Anzeigen und WhatsApp landen gesammelt in Ihrem Dashboard. Termine werden automatisch bestätigt, Angebote entstehen mit wenigen Klicks.",
                ["Alle Anfragen an einem Ort", "Termine mit Bestätigung und Erinnerung", "Angebote und Aufträge nachvollziehbar", "Auswertung, welche Werbung Kunden bringt"]),
        "msgs": [("spark", "Angebot", "Im Mai gibt es 10 % auf die Grundreinigung, bitte als Hinweis auf die Startseite."),
                 ("camera", "Ergebnis", "Hier sind Vorher-nachher-Bilder vom letzten Auftrag, bitte in die Galerie."),
                 ("clock", "Zeiten", "Samstags sind wir ab sofort von 9 bis 14 Uhr erreichbar.")],
        "ref_text": ("FassadenTrio", "Dienstleister", "Google-Ads-Kampagne und Landingpage mit Vorher-nachher-Regler, Ablauf in vier Schritten und Fassaden-Check-Rechner."),
        "faqs": [
            ("Ich bekomme viele Anfragen über Empfehlungen. Brauche ich trotzdem eine Website?", "<p>Ja – denn auch wer empfohlen wird, schaut zuerst online nach. Findet er dort nichts Überzeugendes, ruft er oft gar nicht erst an. Ihre Website macht aus Empfehlungen Aufträge.</p>"),
            ("Können Kunden direkt Termine buchen?", "<p>Ja. Wir bauen die Terminbuchung in Ihre Website ein oder binden Ihr bestehendes System an. Termine landen in Ihrem Dashboard und werden automatisch bestätigt.</p>"),
            ("Lohnt sich Google Ads für Dienstleister?", "<p>Oft sehr – weil Menschen gezielt nach Ihrer Leistung suchen. Entscheidend ist eine passende Landingpage und eine Messung von echten Anfragen, nicht nur von Klicks.</p>"),
        ],
    },
    "/branchen/industrie/": {
        "key": "industrie", "name": "Industrie", "crumb": "Industrie & Mittelstand", "ask": "system",
        "title": "Website für Industrie & Mittelstand | Medialyte",
        "desc": "Websites für Industrie und Mittelstand: Produktfinder für tausende Artikel, mehrsprachig, vollständige B2B-Anfragen und Karriere-Bereich.",
        "h1": 'Websites für Industrie und Mittelstand – <span class="quiet">auch für tausende Produkte.</span>',
        "lead": "Ihre Website ist solide, aber Einkäufer finden das passende Produkt nicht, Anfragen kommen unvollständig und Bewerber springen ab? Wir bauen Websites und Produktfinder für Industrieunternehmen, die komplexe Sortimente verständlich machen – auch international.",
        "visual_ref": ("ritz", "ritz.entwurf.medialyte.de", "Website-Entwurf für RITZ Instrument Transformers"),
        "pain": ("Was B2B-Kunden brauchen", "Technische Daten schnell finden, Datenblätter laden, die richtige Ansprechperson erreichen – in ihrer Sprache."),
        "feats": [
            ("layers", "Produktfinder", "Tausende Artikel nach Merkmalen filtern, Varianten vergleichen, Datenblätter laden."),
            ("globe", "Mehrsprachig", "Für Kunden und Vertretungen in vielen Ländern – mit sauberer Struktur je Sprache."),
            ("brief", "Anfragen mit Spezifikation", "Anfragen mit Artikel, Menge und Anforderungen kommen vollständig bei Ihnen an."),
            ("users", "Karriere", "Ein Bereich, der Fachkräfte und Auszubildende überzeugt – mit echten Einblicken."),
            ("db", "Daten aus Ihrem System", "Produktdaten zentral pflegen und automatisch auf der Website ausspielen."),
            ("search", "Gefunden für Fachbegriffe", "Seiten für Produktgruppen und Anwendungen, die Ingenieure und Einkäufer suchen."),
        ],
        "sys": ("Produktmanagement statt Excel-Listen", "Unser Website-Entwurf für RITZ führt Unternehmensseite und Produktfinder für tausende Produkte zusammen. Dahinter steht ein Produktmanagement, in dem Daten einmal gepflegt und überall aktuell ausgespielt werden.",
                ["Produktdaten zentral gepflegt", "Filter nach technischen Merkmalen", "Datenblätter und Anfragen pro Artikel", "Erweiterbar zum Kunden- und Anfragemanagement"]),
        "msgs": [("brief", "Messe", "Wir sind im Juni auf der Messe, Halle 4 Stand 210. Bitte einen Hinweis auf die Startseite."),
                 ("users", "Stellen", "Bitte die Stelle als Prüffeldtechniker ausschreiben, Text kommt im Anhang."),
                 ("layers", "Produkte", "Die neue Baureihe ist freigegeben, bitte die Datenblätter im Produktfinder ergänzen.")],
        "case_ref": "ritz", "case_title": ("RITZ Instrument Transformers", "Unser Entwurf führt Unternehmensseite und Produktfinder eines Konzerns mit über 1.500 Mitarbeitenden zusammen."),
        "faqs": [
            ("Unsere Website ist eigentlich gut. Was bringt ein Neubau?", "<p>Oft liegt das Problem nicht im Design, sondern in den Nebenschauplätzen: Produkte schwer zu finden, Anfragen unvollständig, Daten doppelt gepflegt, Karriere-Seite ohne Wirkung. Genau dort setzen wir an – auch ohne kompletten Neubau.</p>"),
            ("Können Sie Produktdaten aus unserem System übernehmen?", "<p>Ja. Wir übernehmen Produktdaten aus bestehenden Listen oder Systemen und bauen ein Produktmanagement, aus dem die Website automatisch gespeist wird.</p>"),
            ("Arbeiten Sie auch mehrsprachig?", "<p>Ja. Wir planen Struktur, Adressen und Inhalte so, dass jede Sprache sauber bei Google erscheint.</p>"),
        ],
    },
    "/branchen/vereine/": {
        "key": "verein", "name": "Vereine", "crumb": "Vereine & Organisationen", "ask": "web-neu",
        "title": "Website für Vereine & Organisationen | Medialyte",
        "desc": "Website für Vereine und gemeinnützige Organisationen: Termine, Neuigkeiten, Mitgliedsanträge und Spenden an einem Ort – gepflegt per WhatsApp.",
        "h1": 'Website für Vereine – <span class="quiet">Ehrenamt ohne Technik-Ärger.</span>',
        "lead": "Im Verein fehlt selten das Engagement, aber oft die Zeit für die Website. Wir bauen Vereinen und gemeinnützigen Organisationen eine Seite, die Termine, Neuigkeiten und Mitgliedsanträge an einem Ort bündelt – und die sich per WhatsApp pflegen lässt, ohne dass jemand ein Backend lernen muss.",
        "pain": ("Was eine Vereins-Website leisten muss", "Informieren, neue Mitglieder gewinnen, Unterstützer überzeugen – und das ohne eigenen Webmaster."),
        "feats": [
            ("calendar", "Termine und Veranstaltungen", "Training, Proben, Feste: Alle Termine übersichtlich und immer aktuell."),
            ("users", "Mitglied werden", "Mitgliedsantrag online, ohne Ausdrucken und Einscannen."),
            ("heart", "Spenden", "Ein Spendenbereich, der erklärt, wofür das Geld gebraucht wird."),
            ("globe", "Mehrsprachig", "Für Gemeinschaften mit mehreren Sprachen – wie bei Hubo d’Moran zweisprachig."),
            ("camera", "Neuigkeiten mit Bildern", "Berichte und Fotos vom letzten Fest, in einer Nachricht online."),
            ("wa", "Pflege per WhatsApp", "Jedes Vorstandsmitglied kann Änderungen schicken – der KI-Agent setzt sie um."),
        ],
        "sys": ("Mitglieder und Termine verwalten", "Auf Wunsch bauen wir ein kleines System dahinter: Mitglieder, Anmeldungen zu Veranstaltungen und Beiträge übersichtlich verwaltet, statt in verstreuten Listen.",
                ["Mitgliedsanträge direkt im System", "Anmeldungen zu Veranstaltungen", "Übersicht über Mitglieder und Beiträge", "Rundschreiben an alle Mitglieder"]),
        "msgs": [("heart", "Sommerfest", "Das Sommerfest ist am 12. Juli, bitte als Termin auf die Website stellen."),
                 ("camera", "Bericht", "Hier sind Fotos vom Konzert am Sonntag, bitte als Neuigkeit veröffentlichen."),
                 ("calendar", "Training", "Das Training am Donnerstag fällt in den Ferien aus.")],
        "ref_text": ("Hubo d’Moran", "Gemeinnütziger Verein", "Zweisprachige Website für einen gemeinnützigen Verein mit Spendenbereich und Buchprojekt."),
        "ref_url": "https://hubodmoran.com/",
        "faqs": [
            ("Wer pflegt die Website, wenn der Vorstand wechselt?", "<p>Niemand muss ein System lernen: Änderungen gehen per WhatsApp an den KI-Agenten. Wechselt der Vorstand, geben Sie einfach neue Nummern frei.</p>"),
            ("Können wir Spenden über die Website sammeln?", "<p>Ja. Wir bauen einen Spendenbereich mit Erklärung, Bankverbindung und auf Wunsch einer Online-Zahlung ein.</p>"),
            ("Geht die Website auch zweisprachig?", "<p>Ja. Wie bei Hubo d’Moran bauen wir die Seite in mehreren Sprachen, sauber getrennt und für Google lesbar.</p>"),
        ],
    },
}


def render_branch(path):
    d = BRANCH_PAGES[path]

    def r(ctx):
        k = d["key"]
        if k in mocks.BRANCHES:
            vis = site_visual(k)
        elif d.get("visual_ref"):
            vis = ref_visual(ctx, *d["visual_ref"])
        else:
            vis = ""
        out = page_hero(ctx, [("Start", "/"), ("Branchen", "/branchen/"), (d["crumb"], "")], d["h1"], d["lead"],
                        btn_book(ctx, "Erstgespräch buchen", d["ask"]) + btn_wa(ctx), vis)
        out += f'<section class="section"><div class="wrap">{sh(d["pain"][0], d["pain"][1], split=True)}{feats(d["feats"], tone="web")}</div></section>'
        st, sp, sl = d["sys"]
        out += (f'<section class="section section--deep"><div class="wrap split"><div class="split__text" data-reveal>'
                f'<h2 class="h2">{st}</h2><p>{sp}</p>{btn_book(ctx, "System anfragen", "system")}</div>'
                f'<div data-reveal>{ticks(sl)}<p class="bnote"><a class="link" href="{ctx.u("/leistungen/kundenmanagement-system/")}">Mehr zum Kundenmanagement-System {icon("arrow")}</a></p></div></div></section>')
        msgs = [(ic, t, f"<q>{e(q)}</q>") for ic, t, q in d["msgs"]]
        out += (f'<section class="section"><div class="wrap">{sh("Änderungen per WhatsApp", "So schreiben Betriebe aus Ihrer Branche dem KI-Agenten. Ein paar Minuten später ist die Website aktuell.", split=True, more=ctx_link(ctx, "/leistungen/ki-agent/", "Mehr zum KI-Agenten"))}'
                f'{feats(msgs, tone="ai")}</div></section>')
        if d.get("case_ref"):
            ct, cl = d["case_title"]
            out += f'<section class="section section--deep"><div class="wrap">{sh(ct, cl, split=True)}{cases(ctx, (d["case_ref"],))}</div></section>'
        elif d.get("ref_text"):
            n, c, x = d["ref_text"]
            link = f'<a class="link" href="{d["ref_url"]}" target="_blank" rel="noopener">Website ansehen {icon("out")}</a>' if d.get("ref_url") else f'<a class="link" href="{ctx.u("/referenzen/")}">Alle Referenzen {icon("arrow")}</a>'
            out += (f'<section class="section section--deep"><div class="wrap">{sh("Aus unserer Arbeit", split=True)}'
                    f'<div class="more more--1"><article data-reveal><span class="case__cat">{e(c)}</span><h3>{e(n)}</h3><p>{e(x)}</p>{link}</article></div></div></section>')
        deep = not (d.get("case_ref") or d.get("ref_text"))
        out += f'<section class="section{" section--deep" if deep else ""}"><div class="wrap">{faq_block(ctx, d["faqs"], "Häufige Fragen")}</div></section>'
        out += related(ctx, "Passende Leistungen", svc_tiles("/leistungen/website-erstellung/", "/leistungen/kundenmanagement-system/", "/leistungen/ki-agent/",
                                                            "/leistungen/seo/", "/leistungen/google-ads/", "/leistungen/website-relaunch/"), deep=not deep)
        out += related(ctx, "Weitere Branchen", branch_tiles(path), deep=deep)
        out += closing(ctx, f"Eine Website für Ihren Betrieb?", "Sprechen wir darüber.",
                       "Im kostenfreien Erstgespräch schauen wir uns Ihren Betrieb an und sagen Ihnen ehrlich, was sich lohnt. Ihr Angebot erhalten Sie innerhalb von 48 Stunden.")
        return out
    return r


def ctx_link(ctx, path, text):
    return f'<a class="link" href="{ctx.u(path)}">{text} {icon("arrow")}</a>'


def render_branchen(ctx):
    return (page_hero(ctx, [("Start", "/"), ("Branchen", "")], 'Websites für jede Branche. <span class="quiet">Gemacht für Ihre Kunden.</span>',
                      "Ein Restaurant braucht die Reservierung, ein Handwerksbetrieb Anfragen mit Fotos, eine Praxis Online-Termine. Deshalb beginnen wir jedes Projekt mit Ihrer Branche und Ihrer Zielgruppe – nicht mit einer Vorlage. Wählen Sie Ihre Branche:",
                      btn_book(ctx) + btn_wa(ctx))
            + f'<section class="section section--flush"><div class="wrap">{tiles(ctx, branch_tiles())}</div></section>'
            + f'<section class="section section--deep"><div class="wrap">{sh("Was alle Branchen gemeinsam haben", "Egal, was Sie anbieten: Ihre Website soll gefunden werden, überzeugen und Anfragen bringen – und danach ohne Aufwand aktuell bleiben.", split=True)}'
            + feats([("search", "Gefunden werden", "Schnelle Technik, klare Struktur und lokales SEO, damit Kunden Sie bei Google finden."),
                     ("target", "Überzeugen", "Texte und Gestaltung, die genau Ihre Zielgruppe ansprechen."),
                     ("inbox", "Anfragen bekommen", "Reservierung, Anfrage, Termin oder Anruf – der passende Weg für Ihre Kunden."),
                     ("db", "Alles an einem Ort", "Auf Wunsch mit eigenem System, in dem jede Anfrage landet."),
                     ("bot", "Aktuell bleiben", "Änderungen per WhatsApp an den KI-Agenten – ohne Technikkenntnisse."),
                     ("users", "Ein fester Ansprechpartner", "Persönliche Betreuung statt Ticketsystem.")], tone=["ads", "web", "web", "crm", "ai", "web"])
            + '</div></section>'
            + f'<section class="section"><div class="wrap">{sh("Projekte aus verschiedenen Branchen", "Software, Juwelierkette und Industriekonzern – öffnen Sie ein Projekt und scrollen Sie durch die ganze Seite.", split=True)}{cases(ctx)}</div></section>'
            + closing(ctx))


# ======================================================================= Webdesign Hamburg
FAQ_HH = [
    ("Kommen Sie für das Erstgespräch auch zu uns?", "<p>Ja. Im Raum Hamburg kommen wir gern zu Ihnen in den Betrieb. Alternativ sprechen wir per Video-Call oder Telefon – ganz wie es Ihnen passt.</p>"),
    ("Arbeiten Sie nur für Hamburger Betriebe?", "<p>Nein. Unser Sitz ist in Hamburg, unsere Kunden sitzen in ganz Deutschland. Für Betriebe aus Hamburg und dem Umland sind persönliche Termine aber besonders einfach.</p>"),
    ("Wie werde ich in Hamburg bei Google gefunden?", "<p>Mit lokalem SEO: Seitentitel und Inhalte, die Ihren Stadtteil oder Ihre Region nennen, ein vollständiges Google-Unternehmensprofil, einheitliche Firmendaten und echte Bewertungen. Für schnelle Sichtbarkeit kommen lokale Google-Ads-Kampagnen dazu.</p>"),
    ("Was kostet eine Website bei einer Hamburger Agentur?", "<p>Bei Medialyte besteht jedes Angebot aus einer einmaligen Pauschale und einem monatlichen Abo für Hosting, Pflege, KI-Agent und Support. Den genauen Preis erhalten Sie nach dem kostenfreien Erstgespräch innerhalb von 48 Stunden.</p>"),
]


def render_hamburg(ctx):
    return (page_hero(ctx, [("Start", "/"), ("Webdesign Hamburg", "")], 'Webdesign aus Hamburg – <span class="quiet">für Betriebe, die gefunden werden wollen.</span>',
                      "Medialyte ist eine Digitalagentur aus Hamburg. Wir bauen Websites, Kundenmanagement-Systeme und Kampagnen für Restaurants, Handwerksbetriebe, Praxen, Kanzleien, Händler und Industrie – in Hamburg persönlich vor Ort, deutschlandweit per Video-Call.",
                      btn_book(ctx) + btn_wa(ctx), ref_visual(ctx, "rubin", "rubin-gold.de", "Website von Juwelier Rubin"))
            + f'<section class="section"><div class="wrap">{sh("Warum eine Agentur aus Hamburg?", "Weil kurze Wege die Zusammenarbeit leichter machen – und weil wir wissen, wie Kunden in Hamburg suchen.", split=True)}'
            + feats([("users", "Persönlich vor Ort", "Erstgespräch und Abstimmungen im Raum Hamburg gern bei Ihnen im Betrieb."),
                     ("pin", "Lokales SEO für Hamburg", "Sichtbar bei Suchen mit Stadtteil oder „in der Nähe“ – in den Ergebnissen und in Google Maps."),
                     ("search", "Google-Unternehmensprofil", "Vollständig, mit Leistungen, Fotos und Bewertungen – damit Sie im Kartenbereich auftauchen."),
                     ("target", "Lokale Kampagnen", "Google Ads nur für Ihr Einzugsgebiet, ohne Streuverluste."),
                     ("clock", "Angebot in 48 Stunden", "Nach dem Erstgespräch wissen Sie schnell, woran Sie sind."),
                     ("bot", "Pflege per WhatsApp", "Änderungen schicken Sie einfach per Nachricht – der KI-Agent setzt sie um.")], tone="web")
            + '</div></section>'
            + f'<section class="section section--deep"><div class="wrap">{sh("Projekte aus Hamburg und dem Norden", "Eine Juwelierkette mit Filialen in Hamburg, Norderstedt und Lüneburg und ein Hamburger Industriekonzern mit über 1.500 Mitarbeitenden.", split=True)}{cases(ctx, ("rubin", "ritz"))}</div></section>'
            + related(ctx, "Unsere Leistungen", svc_tiles("/leistungen/website-erstellung/", "/leistungen/website-relaunch/", "/leistungen/kundenmanagement-system/",
                                                       "/leistungen/seo/", "/leistungen/google-ads/", "/leistungen/social-media-marketing/"))
            + f'<section class="section section--deep"><div class="wrap">{faq_block(ctx, FAQ_HH, "Fragen zu Webdesign in Hamburg")}</div></section>'
            + related(ctx, "Für Ihre Branche", branch_tiles())
            + closing(ctx, "Webdesign aus Hamburg?", "Lernen wir uns kennen.",
                      "30 Minuten per Video, Telefon oder bei Ihnen vor Ort im Raum Hamburg. Ihr Angebot folgt innerhalb von 48 Stunden."))


# ======================================================================= Kontakt
def render_kontakt(ctx):
    t = [("wa", "ftile--wa", "WhatsApp", "Nachricht schreiben", SITE["wa"], True),
         ("phone", "", "Telefon", SITE["phone"], "tel:" + SITE["phone_intl"], False),
         ("mail", "", "E-Mail", SITE["email"], "mailto:" + SITE["email"], False),
         ("calendar", "", "Erstgespräch", "Termin online buchen", ctx.u("/termin/"), False)]
    lis = "".join(f'<li><a class="ftile {c}" href="{h}"{" target=\"_blank\" rel=\"noopener\"" if ext else ""}><span class="ftile__ic">{icon(ic)}</span><span><small>{s}</small><b>{e(b)}</b></span></a></li>'
                  for ic, c, s, b, h, ext in t)
    return (page_hero(ctx, [("Start", "/"), ("Kontakt", "")], 'Kontakt – <span class="quiet">so erreichen Sie uns.</span>',
                      f"Schreiben Sie uns per WhatsApp, rufen Sie an oder buchen Sie direkt ein kostenfreies Erstgespräch. Wir sind {e(SITE['hours'])} für Sie da und antworten persönlich.")
            + f'<section class="section section--flush"><div class="wrap"><ul class="footer__tiles kontakt__tiles">{lis}</ul>'
            + f'<p class="kontakt__note" data-reveal>Erreichbar {e(SITE["hours"])}. Termine per Video-Call, Telefon oder im Raum Hamburg bei Ihnen vor Ort. Einen Besuch in unserem Büro bieten wir nicht an.</p></div></section>'
            + f'<section class="section section--deep"><div class="wrap">{faq_block(ctx, [FAQ_MAIN[0], FAQ_MAIN[1], FAQ_MAIN[6]], "Vorab beantwortet")}</div></section>'
            + closing(ctx, "Lieber gleich einen Termin?", "30 Minuten, kostenfrei.",
                      "Wählen Sie Ihr Anliegen und einen passenden Termin. Ihr Angebot erhalten Sie innerhalb von 48 Stunden nach dem Gespräch."))


# ======================================================================= FAQ
FAQ_GROUPS = [
    ("allgemein", "Allgemein", FAQ_MAIN),
    ("website", "Website-Erstellung", pages.FAQ_WEB),
    ("system", "Kundenmanagement-System", pages.FAQ_SYS),
    ("agent", "KI-Agent", pages.FAQ_AGENT),
    ("marketing", "Online-Marketing", pages.FAQ_MKT),
]


def _all_faqs():
    seen, out = set(), []
    for _, _, qas in FAQ_GROUPS:
        for q, a in qas:
            if q not in seen:
                seen.add(q)
                out.append((q, a))
    return out


def render_faq(ctx):
    toc = "".join(f'<li><a href="#{k}">{t}</a></li>' for k, t, _ in FAQ_GROUPS)
    out = page_hero(ctx, [("Start", "/"), ("Häufige Fragen", "")], 'Häufige Fragen – <span class="quiet">ehrlich beantwortet.</span>',
                    "Was kostet eine Website? Wie lange dauert es? Wie ändere ich später etwas? Hier finden Sie die Antworten auf die Fragen, die uns am häufigsten gestellt werden.",
                    btn_book(ctx) + btn_wa(ctx))
    out += f'<section class="section section--flush"><div class="wrap"><nav class="prose__toc faq-toc" aria-label="Themen"><p>Themen</p><ol>{toc}</ol></nav></div></section>'
    for i, (k, t, qas) in enumerate(FAQ_GROUPS):
        out += f'<section class="section{" section--deep" if i % 2 == 0 else ""}" id="{k}"><div class="wrap">{faq_block(ctx, qas, t)}</div></section>'
    return out + closing(ctx)


# ======================================================================= Ratgeber
def _toc(sections):
    return '<nav class="prose__toc" aria-label="Inhalt"><p>Inhalt</p><ol>' + "".join(f'<li><a href="#{a}">{t}</a></li>' for a, t, _ in sections) + "</ol></nav>"


def _article(ctx, a):
    body = "".join(f'<h2 id="{aid}">{t}</h2>{html}' for aid, t, html in a["sections"])
    body = re.sub(r"\{u:([^}]+)\}", lambda m: ctx.u(m.group(1)), body)
    meta = f'<p class="prose__meta">Stand: 4. November 2026 · {a["read"]} Minuten Lesezeit · Von Daniel, Medialyte</p>'
    out = page_hero(ctx, [("Start", "/"), ("Ratgeber", "/ratgeber/"), (a["crumb"], "")], a["h1"], a["lead"])
    out += (f'<section class="section section--flush"><div class="wrap"><div class="legal">{_toc(a["sections"])}'
            f'<article class="prose">{meta}{body}</article></div></div></section>')
    rel = [rag_tile(p) for p in a.get("rel_rag", [])] + svc_tiles(*a["rel"])
    out += related(ctx, "Weiterlesen", rel, deep=True)
    out += closing(ctx, a.get("close", "Lieber gleich mit Profis sprechen?"), "Das Erstgespräch ist kostenfrei.",
                   "Wir schauen uns Ihre Situation an und sagen Ihnen ehrlich, was sich lohnt. Ihr Angebot erhalten Sie innerhalb von 48 Stunden.")
    return out


ARTICLES = {
    "/ratgeber/was-kostet-eine-website/": {
        "teaser": "Einmalige und laufende Kosten, Preistreiber, versteckte Kosten und die richtigen Fragen an jede Agentur.",
        "crumb": "Was kostet eine Website?", "icon": "pie", "read": 6,
        "title": "Was kostet eine Website? Kosten erklärt (2026)",
        "desc": "Was kostet eine Website wirklich? Einmalige und laufende Kosten, Preistreiber, versteckte Kosten und die richtigen Fragen an eine Agentur.",
        "h1": 'Was kostet eine Website? <span class="quiet">Die Kostenfaktoren erklärt.</span>',
        "lead": "Die ehrliche Antwort lautet: Es kommt darauf an. Damit Sie trotzdem einschätzen können, womit Sie rechnen müssen, erklären wir hier, woraus sich der Preis einer Website zusammensetzt, welche Kosten oft vergessen werden und welche Fragen Sie jeder Agentur stellen sollten.",
        "sections": [
            ("einmalig-laufend", "Einmalige und laufende Kosten", "<p>Jede Website verursacht zwei Arten von Kosten. <b>Einmalig</b> fallen Konzept, Gestaltung, Texte, Entwicklung und der Umzug Ihrer Inhalte an. <b>Laufend</b> kommen Domain, Hosting, SSL-Zertifikat, Wartung, Sicherheitsupdates und Änderungen hinzu.</p><p>Viele Angebote nennen nur den einmaligen Preis. Wer die laufenden Kosten nicht mitrechnet, erlebt nach dem Livegang Überraschungen – oder eine Website, die nach zwei Jahren veraltet ist, weil sich niemand um sie kümmert.</p>"),
            ("preistreiber", "Was den Preis bestimmt", "<p>Diese Punkte haben den größten Einfluss auf die Kosten:</p><ul><li><b>Umfang:</b> Eine Seite mit fünf Unterseiten ist etwas anderes als eine Website mit fünfzig Leistungs- und Standortseiten.</li><li><b>Individuelles Design:</b> Eine Vorlage ist günstiger, sieht aber aus wie bei vielen anderen. Ein eigenes Design passt zu Ihrer Marke und Zielgruppe.</li><li><b>Texte und Bilder:</b> Liefern Sie Texte und Fotos selbst oder sollen sie neu entstehen? Gute Texte sind einer der größten Hebel für Anfragen.</li><li><b>Funktionen:</b> Terminbuchung, Reservierung, Shop, Mehrsprachigkeit, Produktfinder oder eine Anbindung an Ihr Kundensystem.</li><li><b>Inhaltsübernahme:</b> Bei einem Relaunch müssen Inhalte übertragen und Weiterleitungen eingerichtet werden.</li><li><b>Betreuung:</b> Wie schnell werden Änderungen umgesetzt, und was kosten sie?</li></ul>"),
            ("versteckt", "Kosten, die oft vergessen werden", "<ul><li><b>Änderungen nach dem Livegang:</b> Viele Agenturen rechnen jede kleine Änderung einzeln ab. Über die Jahre kommt so einiges zusammen.</li><li><b>Plugins und Lizenzen:</b> Baukästen und Content-Management-Systeme brauchen oft kostenpflichtige Erweiterungen, die jährlich verlängert werden.</li><li><b>Sicherheit und Updates:</b> Ohne regelmäßige Updates wird eine Website angreifbar. Wer kümmert sich darum?</li><li><b>Rechtstexte:</b> Impressum und Datenschutzerklärung müssen zur Website passen und aktuell bleiben.</li><li><b>Ihre eigene Zeit:</b> Wenn Sie Inhalte selbst pflegen, kostet das Stunden, die im Betrieb fehlen.</li></ul>"),
            ("baukasten", "Baukasten, Freelancer oder Agentur?", "<p><b>Baukästen</b> sind günstig im Einstieg, aber Sie bauen und pflegen alles selbst. Für einen einfachen Auftritt kann das reichen. <b>Freelancer</b> sind flexibel, aber oft allein – bei Urlaub oder Krankheit steht das Projekt. <b>Agenturen</b> sind meist teurer im Einstieg, bieten aber Konzept, Design, Technik und Betreuung aus einer Hand.</p><p>Entscheidend ist nicht der günstigste Preis, sondern was die Website für Ihren Betrieb bringt: Eine Seite, die jeden Monat zusätzliche Anfragen erzeugt, ist ein Gewinn – eine billige Seite, die niemand findet, ist teuer.</p>"),
            ("fragen", "Diese Fragen sollten Sie jeder Agentur stellen", "<ul><li>Was ist im Preis enthalten – und was nicht?</li><li>Welche laufenden Kosten kommen auf mich zu?</li><li>Was kostet eine Änderung nach dem Livegang?</li><li>Gehört mir die Domain, und kann ich jederzeit wechseln?</li><li>Wer kümmert sich um Updates und Sicherheit?</li><li>Wird die Website für Google und das Smartphone optimiert?</li><li>Bleiben bei einem Relaunch meine Google-Platzierungen erhalten?</li></ul>"),
            ("medialyte", "So rechnet Medialyte ab", "<p>Bei uns besteht jedes Angebot aus zwei klaren Teilen: einer <b>einmaligen Pauschale</b> für Konzept, Design und Entwicklung und einem <b>monatlichen Abo</b> für Hosting, Domain, SSL, Pflege, Support und den KI-Agenten. Laufende Änderungen wie Öffnungszeiten, Preise oder Bilder schicken Sie per WhatsApp – sie sind im Abo enthalten.</p><p>Den genauen Preis nennen wir nach dem <a href=\"{u:/termin/}\">kostenfreien Erstgespräch</a>, innerhalb von 48 Stunden. So zahlen Sie nur für das, was Ihr Betrieb wirklich braucht. Mehr dazu auf der Seite <a href=\"{u:/leistungen/website-erstellung/}\">Website erstellen lassen</a>.</p>"),
        ],
        "rel": ["/leistungen/website-erstellung/", "/leistungen/website-relaunch/"], "rel_rag": ["/ratgeber/website-relaunch-checkliste/"],
        "close": "Sie möchten wissen, was Ihre Website kostet?",
    },
    "/ratgeber/website-relaunch-checkliste/": {
        "teaser": "12 Schritte von der Bestandsaufnahme bis zur Search Console – damit Ihre Google-Platzierungen bleiben.",
        "crumb": "Website-Relaunch: Checkliste", "icon": "refresh", "read": 7,
        "title": "Website-Relaunch-Checkliste: 12 Schritte | Medialyte",
        "desc": "Website-Relaunch ohne Google-Verlust: alle Schritte von der Bestandsaufnahme über 301-Weiterleitungen bis zur Search Console.",
        "h1": 'Website-Relaunch: <span class="quiet">die Checkliste ohne Ranking-Verlust.</span>',
        "lead": "Ein Relaunch ist die Chance, Ihre Website auf den neuesten Stand zu bringen. Er ist aber auch der Moment, in dem viele Betriebe ihre Google-Platzierungen verlieren. Mit diesen Schritten passiert das nicht.",
        "sections": [
            ("vorher", "Vor dem Relaunch: Bestandsaufnahme", "<ul><li><b>1. Alle Adressen sichern:</b> Erstellen Sie eine Liste aller bisherigen Seiten – aus der Sitemap, der Google Search Console und einem Crawl der Website.</li><li><b>2. Wichtige Seiten erkennen:</b> Welche Seiten bringen Besucher, Anfragen und Links von anderen Websites? Diese müssen erhalten bleiben oder ein gleichwertiges Ziel bekommen.</li><li><b>3. Ziele festlegen:</b> Was soll die neue Website besser machen – mehr Anfragen, bessere Darstellung auf dem Handy, einfachere Pflege?</li></ul>"),
            ("planung", "Planung: Struktur und Inhalte", "<ul><li><b>4. Neue Struktur planen:</b> Für jede wichtige Leistung, Branche oder Region eine eigene Seite. Eine klare Struktur hilft Besuchern und Google.</li><li><b>5. Inhalte übernehmen und verbessern:</b> Gute Texte nicht wegwerfen, sondern überarbeiten. Dünne oder doppelte Seiten zusammenführen.</li><li><b>6. Seitentitel und Beschreibungen:</b> Jede Seite bekommt einen eigenen, aussagekräftigen Titel und eine Beschreibung, die zum Klicken einlädt.</li></ul>"),
            ("weiterleitungen", "Das Wichtigste: 301-Weiterleitungen", "<p><b>7. Weiterleitungsplan erstellen:</b> Jede alte Adresse wird dauerhaft (Statuscode 301) auf die inhaltlich passende neue Seite umgeleitet – nicht pauschal auf die Startseite. So erkennt Google, wo die Inhalte jetzt stehen, und überträgt die Signale der alten Seite.</p><p>Fehlen Weiterleitungen, landen Besucher und Google auf Fehlerseiten. Genau das ist der häufigste Grund für Einbrüche nach einem Relaunch.</p>"),
            ("test", "Testen vor dem Livegang", "<ul><li><b>8. Testversion sperren:</b> Die Testversion darf nicht bei Google erscheinen (noindex), sonst entsteht doppelter Inhalt.</li><li><b>9. Alles prüfen:</b> Formulare, Terminbuchung, Ladezeit, Darstellung auf Handy, Tablet und Desktop, Rechtstexte.</li><li><b>10. Sperre aufheben:</b> Beim Livegang die noindex-Sperre entfernen – ein Klassiker, der gern vergessen wird.</li></ul>"),
            ("nachher", "Nach dem Livegang", "<ul><li><b>11. Sitemap einreichen:</b> Die neue Sitemap in der Google Search Console einreichen und die wichtigsten Seiten zur Indexierung anmelden.</li><li><b>12. Beobachten und nachsteuern:</b> In den ersten Wochen Fehlerseiten, Indexierung und Platzierungen kontrollieren und fehlende Weiterleitungen ergänzen. Das Google-Unternehmensprofil auf die neue Website verlinken.</li></ul><p>Kurzfristige Schwankungen sind normal, während Google die neue Website erfasst. Mit sauberen Weiterleitungen pendelt sich die Sichtbarkeit wieder ein – und steigt mit der besseren Website oft über das alte Niveau.</p>"),
            ("hilfe", "Relaunch mit Medialyte", "<p>Wir übernehmen den kompletten Umzug: Bestandsaufnahme, neue Struktur, Inhalte, Weiterleitungen, Testversion und Kontrolle nach dem Livegang. Mehr dazu auf der Seite <a href=\"{u:/leistungen/website-relaunch/}\">Website-Relaunch</a>.</p>"),
        ],
        "rel": ["/leistungen/website-relaunch/", "/leistungen/seo/"], "rel_rag": ["/ratgeber/was-kostet-eine-website/"],
        "close": "Relaunch geplant?",
    },
    "/ratgeber/google-unternehmensprofil-optimieren/": {
        "teaser": "Kategorie, Einzugsgebiet, Fotos, Beiträge und Bewertungen: 10 Tipps für mehr Kunden aus Ihrer Region.",
        "crumb": "Google-Unternehmensprofil optimieren", "icon": "pin", "read": 6,
        "title": "Google-Unternehmensprofil optimieren: 10 Tipps",
        "desc": "So optimieren Sie Ihr Google-Unternehmensprofil: Kategorie, Angaben, Leistungen, Fotos, Beiträge und Bewertungen – für mehr lokale Kunden.",
        "h1": 'Google-Unternehmensprofil optimieren: <span class="quiet">10 Tipps für mehr lokale Kunden.</span>',
        "lead": "Wer „in der Nähe“ sucht, sieht zuerst die Karte mit drei Betrieben. Ob Ihrer dabei ist, hängt stark vom Google-Unternehmensprofil ab. Diese zehn Punkte machen den Unterschied.",
        "sections": [
            ("kategorie", "1. Die richtige Hauptkategorie", "<p>Die Hauptkategorie ist eines der wichtigsten Signale. Wählen Sie die Kategorie, die Ihre Kernleistung am genauesten beschreibt, und ergänzen Sie passende Nebenkategorien. Ein Restaurant ist besser als „Italienisches Restaurant“ eingetragen als nur als „Restaurant“.</p>"),
            ("daten", "2. Einheitliche Firmendaten", "<p>Name, Adresse und Telefonnummer sollten überall identisch sein: im Profil, auf Ihrer Website, in Branchenverzeichnissen und sozialen Netzwerken. Widersprüche verunsichern Google und Kunden.</p>"),
            ("gebiet", "3. Einzugsgebiet statt Adresse", "<p>Empfangen Sie keine Kunden vor Ort, etwa als Handwerker oder Dienstleister, können Sie die Adresse ausblenden und stattdessen ein Einzugsgebiet angeben. So erscheinen Sie dort, wo Ihre Kunden sind.</p>"),
            ("zeiten", "4. Öffnungszeiten – auch an Feiertagen", "<p>Hinterlegen Sie reguläre Zeiten und Sonderöffnungszeiten für Feiertage und Betriebsferien. Nichts ärgert Kunden mehr als eine verschlossene Tür, obwohl Google „geöffnet“ anzeigt.</p>"),
            ("leistungen", "5. Leistungen und Beschreibung", "<p>Tragen Sie Ihre Leistungen einzeln ein und schreiben Sie eine Beschreibung, die in den ersten Sätzen sagt, was Sie tun und für wen. Verlinken Sie das Profil auf die passende Seite Ihrer Website.</p>"),
            ("fotos", "6. Echte Fotos", "<p>Profile mit aktuellen Fotos von Räumen, Team und Arbeit wirken vertrauenswürdiger. Laden Sie regelmäßig neue Bilder hoch – Stockfotos helfen nicht.</p>"),
            ("beitraege", "7. Regelmäßige Beiträge", "<p>Neuigkeiten, Angebote und Veranstaltungen lassen sich als Beitrag veröffentlichen. Ein kurzes Video oder Bild pro Woche zeigt, dass Ihr Betrieb aktiv ist.</p>"),
            ("bewertungen", "8. Bewertungen aktiv anfragen", "<p>Bitten Sie zufriedene Kunden direkt nach dem Auftrag um eine Bewertung – am einfachsten mit einem Link oder QR-Code. Viele aktuelle, echte Bewertungen sind ein starkes Signal. Gekaufte oder gefälschte Bewertungen verstoßen gegen die Richtlinien von Google.</p>"),
            ("antworten", "9. Auf jede Bewertung antworten", "<p>Bedanken Sie sich für positive Bewertungen und reagieren Sie sachlich auf Kritik. Ihre Antworten lesen auch alle zukünftigen Kunden.</p>"),
            ("website", "10. Eine Website, die das Profil stärkt", "<p>Das Profil und Ihre Website verstärken sich gegenseitig: Seiten für Ihre Leistungen und Ihre Region, schnelle Ladezeiten und einheitliche Firmendaten helfen beiden. Ein Profil ohne gute Website verschenkt Anfragen, weil viele Nutzer vor dem Anruf noch einmal auf die Website schauen.</p><p>Wir pflegen Unternehmensprofile als Teil unserer <a href=\"{u:/leistungen/seo/}\">SEO-Leistungen</a> und bauen <a href=\"{u:/leistungen/website-erstellung/}\">Websites</a>, die lokal gefunden werden.</p>"),
        ],
        "rel": ["/leistungen/seo/", "/leistungen/google-ads/"], "rel_rag": ["/ratgeber/website-relaunch-checkliste/"],
        "close": "Mehr Kunden aus Ihrer Region?",
    },
    "/ratgeber/crm-fuer-kleine-unternehmen/": {
        "teaser": "Woran Sie erkennen, dass Excel und Zettel nicht mehr reichen – und worauf es bei einem CRM ankommt.",
        "crumb": "CRM für kleine Unternehmen", "icon": "db", "read": 6,
        "title": "CRM für kleine Unternehmen: Wann es sich lohnt",
        "desc": "Braucht mein Betrieb ein CRM? Woran Sie erkennen, dass Excel nicht mehr reicht, Standard vs. eigenes System und worauf es ankommt.",
        "h1": 'CRM für kleine Unternehmen: <span class="quiet">Wann es sich lohnt.</span>',
        "lead": "Ein CRM, also ein Kundenmanagement-System, klingt nach Konzern. Dabei profitieren gerade kleine Betriebe davon, wenn Anfragen, Termine und Angebote nicht mehr in verschiedenen Postfächern, Notizbüchern und Tabellen verstreut sind.",
        "sections": [
            ("was", "Was ist ein CRM?", "<p>CRM steht für Customer Relationship Management. Gemeint ist ein System, in dem alles rund um Ihre Kunden an einem Ort liegt: Kontaktdaten, Anfragen, Gesprächsnotizen, Termine, Angebote, Aufträge und Dokumente. Jeder im Team sieht, was zu tun ist – auch mobil.</p>"),
            ("anzeichen", "Fünf Anzeichen, dass Sie eins brauchen", "<ul><li>Anfragen kommen über Telefon, E-Mail, WhatsApp und Website – und landen an verschiedenen Stellen.</li><li>Rückrufe werden vergessen, weil sie auf einem Zettel stehen.</li><li>Angebote schreiben Sie abends, weil Sie dafür alles zusammensuchen müssen.</li><li>Nur eine Person im Betrieb weiß, wie der Stand bei einem Kunden ist.</li><li>Sie wissen nicht genau, woher Ihre Kunden kommen und welche Werbung sich lohnt.</li></ul><p>Trifft mehr als einer dieser Punkte zu, kostet Sie das fehlende System wahrscheinlich schon heute Aufträge.</p>"),
            ("standard", "Standardsoftware oder eigenes System?", "<p><b>Standardsoftware</b> ist schnell eingerichtet und bietet viele Funktionen. Dafür passen Sie Ihre Abläufe an die Software an, zahlen oft pro Nutzer und brauchen Zeit für die Einarbeitung. Für viele Betriebe ist sie zu groß oder an den falschen Stellen zu klein.</p><p>Ein <b>eigenes System</b> bildet genau Ihre Abläufe ab: die Felder, die Sie brauchen, die Schritte, die bei Ihnen vorkommen, und die direkte Verbindung zu Ihrer Website. Es startet schlank und wächst mit.</p>"),
            ("worauf", "Worauf Sie achten sollten", "<ul><li><b>Verbindung zur Website:</b> Anfragen und Terminbuchungen sollten ohne Abtippen im System landen.</li><li><b>Einfache Bedienung:</b> Ein System, das niemand nutzt, bringt nichts. Weniger ist oft mehr.</li><li><b>Mobil nutzbar:</b> Auf der Baustelle, im Laden oder unterwegs.</li><li><b>Datenschutz:</b> Wo liegen die Daten, wer hat Zugriff, gibt es einen Vertrag zur Auftragsverarbeitung?</li><li><b>Automatisierung:</b> Bestätigungen, Erinnerungen und Nachfassen sollten von selbst laufen.</li></ul>"),
            ("start", "So starten Sie", "<p>Beginnen Sie mit dem größten Schmerz – meist der Frage, wo Anfragen landen. Bündeln Sie zuerst alle Anfragen an einem Ort, dann kommen Termine, Angebote und Auswertungen dazu. So ist das System vom ersten Tag an nützlich.</p><p>Wir entwickeln <a href=\"{u:/leistungen/kundenmanagement-system/}\">Kundenmanagement-Systeme</a>, die direkt mit Ihrer Website verbunden sind – auf Wunsch mit einem <a href=\"{u:/leistungen/ki-agent/}\">KI-Agenten</a>, der an offene Anfragen erinnert und Routineaufgaben übernimmt.</p>"),
        ],
        "rel": ["/leistungen/kundenmanagement-system/", "/leistungen/ki-agent/"], "rel_rag": ["/ratgeber/was-kostet-eine-website/"],
        "close": "Schluss mit Zettelwirtschaft?",
    },
}
def rag_tile(path):
    a = ARTICLES[path]
    return (path, a["icon"], "", a["crumb"], f'Ratgeber · {a["read"]} Minuten Lesezeit')


def render_ratgeber(ctx):
    items = [(p, a["icon"], "", a["crumb"], e(a["teaser"])) for p, a in ARTICLES.items()]
    return (page_hero(ctx, [("Start", "/"), ("Ratgeber", "")], 'Ratgeber – <span class="quiet">Wissen für Ihren Auftritt.</span>',
                      "Was kostet eine Website? Wie gelingt ein Relaunch ohne Google-Verlust? Wann lohnt sich ein CRM? Hier beantworten wir die Fragen, die Betriebe uns am häufigsten stellen – verständlich und ohne Fachchinesisch.",
                      btn_book(ctx) + btn_wa(ctx))
            + f'<section class="section section--flush"><div class="wrap">{tiles(ctx, items, 2)}</div></section>'
            + related(ctx, "Unsere Leistungen", svc_tiles("/leistungen/website-erstellung/", "/leistungen/kundenmanagement-system/", "/leistungen/seo/"), deep=True)
            + closing(ctx))


def article_schema(path, a):
    return {"@context": "https://schema.org", "@type": "Article", "headline": a["crumb"], "description": a["desc"],
            "datePublished": "2026-11-04", "dateModified": "2026-11-04", "inLanguage": "de-DE",
            "mainEntityOfPage": SITE["url"] + path, "image": SITE["url"] + "/assets/img/og.jpg",
            "author": {"@type": "Organization", "name": "Medialyte", "url": SITE["url"] + "/"},
            "publisher": {"@id": SITE["url"] + "/#org"}}


# ======================================================================= Seitenliste
def extra_pages(after_dialog):
    out = [{"path": "/leistungen/", "active": "leistungen",
            "title": "Leistungen – Website, CRM, KI-Agent & Marketing | Medialyte",
            "desc": "Alle Leistungen im Überblick: Website, Relaunch, Online-Shop, Landingpage, Kundenmanagement-System, KI-Agent, SEO, Google Ads und Social Media.",
            "render": render_leistungen, "priority": "0.9",
            "schema": [breadcrumb_schema([("Start", "/"), ("Leistungen", "/leistungen/")])]}]
    for p, d in SUB_SERVICES.items():
        out.append({"path": p, "active": "leistungen", "title": d["title"], "desc": d["desc"], "render": render_sub(p),
                    "after": after_dialog if d.get("case") else (lambda c: ""), "priority": "0.8",
                    "schema": [svc_schema(d["crumb"], p, d["desc"]),
                               breadcrumb_schema([("Start", "/"), ("Leistungen", "/leistungen/"), (d["crumb"], p)]), faq_schema(d["faqs"])]})
    out.append({"path": "/branchen/", "active": "branchen",
                "title": "Branchen – Websites für jede Branche | Medialyte",
                "desc": "Websites für Gastronomie, Handwerk, Praxen, Kanzleien, Einzelhandel, Dienstleister, Industrie und Vereine – gemacht für Ihre Kunden.",
                "render": render_branchen, "after": after_dialog, "priority": "0.9",
                "schema": [breadcrumb_schema([("Start", "/"), ("Branchen", "/branchen/")])]})
    for p, d in BRANCH_PAGES.items():
        out.append({"path": p, "active": "branchen", "title": d["title"], "desc": d["desc"], "render": render_branch(p),
                    "after": after_dialog if d.get("case_ref") else (lambda c: ""), "priority": "0.8",
                    "schema": [svc_schema("Website für " + d["crumb"], p, d["desc"], "Webdesign"),
                               breadcrumb_schema([("Start", "/"), ("Branchen", "/branchen/"), (d["crumb"], p)]), faq_schema(d["faqs"])]})
    out.append({"path": "/webdesign-hamburg/", "active": "",
                "title": "Webdesign Hamburg – Website erstellen lassen | Medialyte",
                "desc": "Webdesign-Agentur aus Hamburg: Websites, Relaunch, SEO und Google Ads – Erstgespräch vor Ort im Raum Hamburg oder per Video. Angebot in 48 h.",
                "render": render_hamburg, "after": after_dialog, "priority": "0.9",
                "schema": [svc_schema("Webdesign Hamburg", "/webdesign-hamburg/", "Websites, Relaunch, SEO und Google Ads für Betriebe in Hamburg.", "Webdesign")
                           | {"areaServed": {"@type": "City", "name": "Hamburg"}},
                           breadcrumb_schema([("Start", "/"), ("Webdesign Hamburg", "/webdesign-hamburg/")]), faq_schema(FAQ_HH)]})
    out.append({"path": "/kontakt/", "active": "kontakt",
                "title": "Kontakt | Medialyte",
                "desc": f"So erreichen Sie Medialyte: WhatsApp, Telefon {SITE['phone']} oder {SITE['email']}. {SITE['hours']}. Oder direkt ein Erstgespräch buchen.",
                "render": render_kontakt, "priority": "0.7",
                "schema": [{"@context": "https://schema.org", "@type": "ContactPage", "url": SITE["url"] + "/kontakt/", "about": {"@id": SITE["url"] + "/#org"}},
                           breadcrumb_schema([("Start", "/"), ("Kontakt", "/kontakt/")])]})
    out.append({"path": "/faq/", "active": "faq",
                "title": "Häufige Fragen (FAQ) | Medialyte",
                "desc": "Was kostet eine Website bei Medialyte, wie lange dauert ein Projekt, wie ändere ich Inhalte per WhatsApp? Die häufigsten Fragen beantwortet.",
                "render": render_faq, "priority": "0.7",
                "schema": [breadcrumb_schema([("Start", "/"), ("Häufige Fragen", "/faq/")]), faq_schema(_all_faqs())]})
    out.append({"path": "/ratgeber/", "active": "ratgeber",
                "title": "Ratgeber – Website, SEO & CRM | Medialyte",
                "desc": "Was kostet eine Website, wie gelingt ein Relaunch, wie optimiere ich mein Google-Profil? Der Medialyte-Ratgeber – verständlich erklärt.",
                "render": render_ratgeber, "priority": "0.7",
                "schema": [breadcrumb_schema([("Start", "/"), ("Ratgeber", "/ratgeber/")])]})
    for p, a in ARTICLES.items():
        out.append({"path": p, "active": "ratgeber", "title": a["title"], "desc": a["desc"],
                    "render": (lambda a: lambda ctx: _article(ctx, a))(a), "priority": "0.7",
                    "schema": [article_schema(p, a), breadcrumb_schema([("Start", "/"), ("Ratgeber", "/ratgeber/"), (a["crumb"], p)])]})
    return out
