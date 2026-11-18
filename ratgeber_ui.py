"""Gestaltung des Ratgebers: Titelbilder (gezeichnet als SVG), Karten, Kurzfassungen, Themen-Farben.

- COVER: je Artikel ein gezeichnetes Titelbild im Stil der Oberflächen auf der Startseite.
  Die Akzentfarbe kommt aus der Themenfarbe (CSS-Variable --tc), alles andere aus Stahl und Fläche.
- KURZ: „Das Wichtigste in Kürze“ – drei Sätze je Artikel, nur aus dem Artikel selbst.
- card()/featured(): Karten für die Übersicht und den Kopfbereich.
"""
from build import e, icon

# Thema -> (kurzer Name, Farbton der Leistungen)
THEMA_UI = {
    "website": ("Website", "web"),
    "gefunden": ("Google", "ads"),
    "kunden": ("Kunden & Abläufe", "crm"),
}

# ---------------------------------------------------------------- Titelbilder (viewBox 0 0 400 250)
def _win(x, y, w, h, cls="cv-s", bar=True):
    s = f'<rect class="{cls}" x="{x}" y="{y}" width="{w}" height="{h}" rx="10"/>'
    if bar:
        s += f'<path class="cv-l" d="M{x} {y + 18}h{w}"/>' + "".join(
            f'<circle class="cv-d" cx="{x + 12 + i * 9}" cy="{y + 9}" r="2.4"/>' for i in range(3))
    return s


def _lines(x, y, ws, gap=12, cls="cv-t"):
    return "".join(f'<rect class="{cls}" x="{x}" y="{y + i * gap}" width="{w}" height="5" rx="2.5"/>' for i, w in enumerate(ws))


COVER = {
    "was-kostet-eine-website": (
        _win(70, 34, 170, 182, bar=False) + _lines(90, 58, [92, 70, 110, 80]) +
        '<path class="cv-l" d="M90 128h130" stroke-dasharray="4 5"/>' + _lines(90, 146, [60, 74, 52]) +
        '<rect class="cv-af" x="90" y="186" width="130" height="14" rx="7"/>' +
        "".join(f'<ellipse class="cv-coin" cx="300" cy="{196 - i * 13}" rx="38" ry="10"/>' for i in range(5)) +
        '<ellipse class="cv-a cv-top" cx="300" cy="134" rx="38" ry="10"/><text class="cv-n" x="300" y="139" text-anchor="middle">€</text>'),
    "website-relaunch-checkliste": (
        _win(40, 56, 150, 120, cls="cv-s cv-old") + _lines(56, 92, [70, 100, 56], cls="cv-t cv-old") +
        _win(214, 40, 150, 150) + '<rect class="cv-af" x="228" y="70" width="70" height="8" rx="4"/>' + _lines(228, 88, [110, 90]) +
        '<rect class="cv-a" x="228" y="120" width="122" height="54" rx="8"/>' +
        '<path class="cv-a cv-w" d="M120 196c40 34 120 34 160 4"/><path class="cv-a cv-w" d="M268 192l14 6-4 15"/>'),
    "google-unternehmensprofil-optimieren": (
        '<path class="cv-l" d="M30 70h340M30 125h340M30 180h340M110 20v220M220 20v220M310 20v220"/>' +
        '<path class="cv-road" d="M20 200C120 160 180 210 260 120S360 60 390 50"/>' +
        '<path class="cv-af" d="M200 52a34 34 0 0 1 34 34c0 26-34 58-34 58s-34-32-34-58a34 34 0 0 1 34-34z"/><circle class="cv-hole" cx="200" cy="86" r="12"/>' +
        _win(222, 150, 150, 70, bar=False) + _lines(238, 166, [80]) +
        "".join(f'<path class="cv-star" transform="translate({240 + i * 22} 192) scale(.62)" d="M12 2.5l2.9 6 6.6.9-4.8 4.6 1.2 6.5L12 17.3l-5.9 3.2 1.2-6.5L2.5 9.4l6.6-.9z"/>' for i in range(5))),
    "crm-fuer-kleine-unternehmen": (
        "".join(f'<rect class="cv-s" x="{40 + i * 112}" y="36" width="100" height="178" rx="12"/>' + _lines(54 + i * 112, 52, [44]) for i in range(3)) +
        "".join(f'<rect class="cv-card" x="{50 + c * 112}" y="{74 + r * 46}" width="80" height="36" rx="7"/>' for c, r in [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (2, 0)]) +
        '<rect class="cv-a" x="168" y="164" width="80" height="36" rx="7" transform="rotate(-6 208 182)"/>' +
        '<path class="cv-a cv-w" d="M258 176c18-4 30-14 38-30"/><path class="cv-a cv-w" d="M286 144l11 1 1 11"/>'),
    "barrierefreie-website-bfsg": (
        _win(36, 40, 196, 170) + '<text class="cv-big" x="62" y="140">Aa</text>' +
        '<rect class="cv-af" x="168" y="74" width="44" height="22" rx="5"/><rect class="cv-t" x="168" y="104" width="44" height="22" rx="5" opacity=".5"/>' +
        '<rect class="cv-t" x="56" y="168" width="156" height="22" rx="11" opacity=".35"/>' +
        '<rect class="cv-key" x="258" y="64" width="110" height="64" rx="12"/><text class="cv-k" x="313" y="104" text-anchor="middle">Tab ⇥</text>' +
        '<rect class="cv-ring" x="252" y="58" width="122" height="76" rx="16"/>' +
        '<path class="cv-a cv-w" d="M260 178s18-24 53-24 53 24 53 24-18 24-53 24-53-24-53-24z"/><circle class="cv-af" cx="313" cy="178" r="11"/>'),
    "website-ladezeit-core-web-vitals": (
        "".join(
            f'<path class="cv-arc" d="M{x - 46} 150a46 46 0 0 1 92 0"/><path class="cv-a cv-w" d="M{x - 46} 150a46 46 0 0 1 {46 + 46 * c:.1f} {-46 * s:.1f}"/>'
            f'<path class="cv-needle" d="M{x} 150L{x + 34 * c:.1f} {150 - 34 * s:.1f}"/><circle class="cv-af" cx="{x}" cy="150" r="5"/>'
            f'<text class="cv-lab" x="{x}" y="186" text-anchor="middle">{lab}</text>'
            for x, c, s, lab in [(84, -.62, .78, "LCP"), (200, -.2, .98, "INP"), (316, -.78, .62, "CLS")])),
    "gute-website-wenig-anfragen": (
        _win(40, 30, 320, 190) + '<path class="cv-l" d="M66 190h272M66 70v120"/>' +
        '<path class="cv-old cv-w" d="M70 170c40-4 70-2 100-6"/>' +
        '<path class="cv-a cv-w" d="M170 164c40-8 60-30 84-56s44-38 76-44"/>' +
        '<circle class="cv-af" cx="330" cy="64" r="7"/><circle class="cv-ringc" cx="330" cy="64" r="16"/>' + _lines(70, 52, [70])),
    "google-ads-fuer-kleine-unternehmen": (
        '<rect class="cv-s" x="40" y="36" width="320" height="40" rx="20"/><circle class="cv-a cv-w" cx="66" cy="56" r="8"/><path class="cv-a cv-w" d="M72 62l7 7"/>' +
        _lines(92, 54, [130]) +
        '<rect class="cv-hl" x="40" y="94" width="320" height="56" rx="10"/><rect class="cv-af" x="56" y="106" width="52" height="14" rx="4"/>' +
        '<text class="cv-tag" x="82" y="117" text-anchor="middle">Anzeige</text>' + _lines(118, 108, [150]) + _lines(56, 130, [230], cls="cv-t") +
        _lines(56, 172, [180, 240], gap=14) + _lines(56, 212, [160], gap=14)),
    "ki-agent-im-betrieb": (
        '<rect class="cv-s" x="40" y="40" width="210" height="52" rx="18"/>' + _lines(60, 58, [150, 110]) +
        '<rect class="cv-a" x="120" y="110" width="240" height="72" rx="18"/>' + _lines(140, 128, [170, 190, 120], cls="cv-at") +
        '<rect class="cv-key" x="70" y="132" width="34" height="30" rx="8"/><circle class="cv-af" cx="81" cy="147" r="3"/><circle class="cv-af" cx="93" cy="147" r="3"/><path class="cv-l" d="M87 124v8"/>' +
        '<circle class="cv-okc" cx="340" cy="206" r="16"/><path class="cv-ok" d="M332 206l6 6 11-12"/>'),
    "anfragen-schneller-beantworten": (
        '<path class="cv-s" d="M60 132l34-68h212l34 68v62a14 14 0 0 1-14 14H74a14 14 0 0 1-14-14z"/>' +
        '<path class="cv-l" d="M60 132h80l16 24h88l16-24h80"/>' +
        '<rect class="cv-card" x="126" y="40" width="148" height="92" rx="8" transform="rotate(-4 200 86)"/><path class="cv-l" d="M130 50l70 44 70-44" transform="rotate(-4 200 86)"/>' +
        '<circle class="cv-af" cx="314" cy="62" r="30"/><path class="cv-hand" d="M314 46v16l10 8"/>'),
}


def cover(path, extra_cls=""):
    slug = path.strip("/").split("/")[-1]
    inner = COVER.get(slug, "")
    return (f'<svg class="cover{extra_cls}" viewBox="0 0 400 250" aria-hidden="true" focusable="false">'
            f'<rect class="cv-bg" width="400" height="250"/>{inner}</svg>')


# ---------------------------------------------------------------- Kurzfassungen
KURZ = {
    "/ratgeber/was-kostet-eine-website/": [
        "Rechnen Sie einmalige und laufende Kosten immer zusammen.",
        "Umfang, eigenes Design, Texte und Funktionen bestimmen den Preis am stärksten.",
        "Fragen Sie jede Agentur, was Änderungen nach dem Livegang kosten und wem die Domain gehört."],
    "/ratgeber/website-relaunch-checkliste/": [
        "Sichern Sie vor dem Relaunch alle bisherigen Adressen und erkennen Sie die wichtigen Seiten.",
        "Jede alte Adresse braucht eine 301-Weiterleitung auf die passende neue Seite.",
        "Nach dem Livegang: Sitemap einreichen, Fehlerseiten prüfen, nachsteuern."],
    "/ratgeber/google-unternehmensprofil-optimieren/": [
        "Die Hauptkategorie ist eines der wichtigsten Signale im Profil.",
        "Name, Adresse und Telefonnummer sollten überall identisch sein.",
        "Echte Fotos, regelmäßige Beiträge und Antworten auf Bewertungen zeigen einen aktiven Betrieb."],
    "/ratgeber/crm-fuer-kleine-unternehmen/": [
        "Ein CRM bündelt Anfragen, Termine, Angebote und Notizen an einem Ort.",
        "Spätestens wenn Anfragen über viele Kanäle verstreut sind, lohnt es sich.",
        "Starten Sie mit dem größten Schmerz – meist der Frage, wo Anfragen landen."],
    "/ratgeber/barrierefreie-website-bfsg/": [
        "Betroffen sind vor allem Websites, über die Verbraucher einen Vertrag abschließen – etwa Shops und Online-Buchungen.",
        "Kleinstunternehmen sind bei Dienstleistungen ausgenommen: weniger als zehn Beschäftigte und höchstens 2 Mio. Euro Umsatz oder Bilanzsumme.",
        "Bei Verstößen sind Bußgelder bis 100.000 Euro möglich."],
    "/ratgeber/website-ladezeit-core-web-vitals/": [
        "Gut sind: Ladezeit (LCP) bis 2,5 Sekunden, Reaktion (INP) bis 200 Millisekunden, Stabilität (CLS) bis 0,1.",
        "Messen Sie mit PageSpeed Insights und der Search Console – am besten auf dem Handy.",
        "Die häufigsten Bremsen: große Bilder, viele Skripte und Inhalte ohne feste Maße."],
    "/ratgeber/gute-website-wenig-anfragen/": [
        "Oft liegt es nicht am Design, sondern an Text, Struktur und einem unklaren nächsten Schritt.",
        "Anfragen gehen auch nach dem Absenden verloren, wenn sich niemand zuständig fühlt.",
        "Am Anfang steht eine ehrliche Bestandsaufnahme – was funktioniert, bleibt."],
    "/ratgeber/google-ads-fuer-kleine-unternehmen/": [
        "Bezahlt wird bei Suchanzeigen in der Regel erst beim Klick.",
        "Rechnen Sie Ihr Budget rückwärts: Klickpreis und Anfragequote ergeben den Preis pro Anfrage.",
        "Passende Zielseite, ausschließende Keywords und Messung sparen das meiste Geld."],
    "/ratgeber/ki-agent-im-betrieb/": [
        "Ein KI-Agent erledigt Aufgaben, statt nur Fragen zu beantworten.",
        "Routine darf er selbst erledigen, Wichtiges bereitet er vor, ein Mensch gibt frei.",
        "Seit dem 2. August 2026 müssen KI-Chats als solche erkennbar sein."],
    "/ratgeber/anfragen-schneller-beantworten/": [
        "Wer zuerst kompetent antwortet, setzt den Maßstab für alle anderen.",
        "Eine sofortige Eingangsbestätigung überbrückt die Zeit bis zur Antwort.",
        "Ein Ort für alle Anfragen, klare Zuständigkeit und automatische Erinnerungen."],
}


def kurz(path):
    pts = KURZ.get(path)
    if not pts:
        return ""
    lis = "".join(f'<li>{icon("check")}<span>{e(p)}</span></li>' for p in pts)
    return f'<aside class="rkurz" aria-label="Das Wichtigste in Kürze"><p class="rkurz__t">Das Wichtigste in Kürze</p><ul>{lis}</ul></aside>'


# ---------------------------------------------------------------- Karten
def _meta(a, neu=False):
    name, _ = THEMA_UI[a["thema"]]
    nb = '<span class="badge badge--coral">Neu</span>' if neu else ""
    return f'<p class="rcard__meta"><span class="rtag">{e(name)}</span><span>{a["read"]} Min. Lesezeit</span>{nb}</p>'


def card(ctx, path, a, neu=False, i=0, cls=""):
    tone = THEMA_UI[a["thema"]][1]
    return (f'<li class="rcard tone--{tone}{cls}" data-thema="{a["thema"]}" data-reveal style="--rd:{i % 3}">'
            f'<a href="{ctx.u(path)}"><div class="rcard__cover">{cover(path)}</div><div class="rcard__body">{_meta(a, neu)}'
            f'<h3>{e(a["crumb"])}</h3><p>{e(a["teaser"])}</p><span class="rcard__go">Weiterlesen {icon("arrow")}</span></div></a></li>')


def featured(ctx, path, a):
    tone = THEMA_UI[a["thema"]][1]
    return (f'<a class="rfeat tone--{tone}" href="{ctx.u(path)}"><div class="rcard__cover">{cover(path)}</div>'
            f'<div class="rfeat__body"><p class="rfeat__k">Neu im Ratgeber</p>{_meta(a)}<h2>{e(a["crumb"])}</h2><p>{e(a["teaser"])}</p>'
            f'<span class="rcard__go">Beitrag lesen {icon("arrow")}</span></div></a>')


def hero_meta(a):
    name, tone = THEMA_UI[a["thema"]]
    return (f'<div class="rhmeta tone--{tone}"><span class="rtag">{e(name)}</span>'
            f'<span>{icon("clock")}{a["read"]} Min. Lesezeit</span><span>{icon("calendar")}Stand {e(a.get("date", "4. November 2026"))}</span></div>')


def hero_cover(path, a):
    tone = THEMA_UI[a["thema"]][1]
    return f'<div class="rhcover tone--{tone}">{cover(path)}</div>'
