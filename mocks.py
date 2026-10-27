"""Gezeichnete Oberflächen für die Website: Cockpit mit Beispiel-Websites, Relaunch, Pipeline, Agent, Kampagne.

Alles ist HTML/CSS (keine Screenshots), damit es auf jedem Bildschirm scharf bleibt.
Die Beispiel-Betriebe sind erfunden und als Beispiel gekennzeichnet.
"""
import json

from build import LOGO, e, icon

# ---------------------------------------------------------------- Beispiel-Betriebe
BRANCHES = {
    "gastro": {
        "chip": "Restaurant", "name": "Trattoria Lume", "host": "trattoria-lume.de", "channel": "wa",
        "kpi": ["Reservierungen diese Woche", 37, "+12 % zur Vorwoche"],
        "feed": [["calendar", "Reservierung · 2 Personen", "Sa, 20:00 · über die Website", "09:12"],
                 ["phone", "Anruf über Google", "Frage zu glutenfreien Gerichten", "08:47"]],
        "new": ["calendar", "Reservierung · 4 Personen", "Fr, 19:30 · über Google", "09:41"],
        "me": "Heute gibt’s Kürbisrisotto als Mittagstisch, 12,50 €. Kannst du das auf die Website setzen?",
        "agent": "Erledigt. Der Mittagstisch ist online – so sieht es jetzt aus.",
    },
    "handwerk": {
        "chip": "Handwerk", "name": "Tischlerei Brandt", "host": "tischlerei-brandt.de", "channel": "wa",
        "kpi": ["Anfragen diesen Monat", 23, "+9 % zum Vormonat"],
        "feed": [["phone", "Rückruf gewünscht", "Küche nach Maß · Herr Kaya", "09:05"],
                 ["search", "Anfrage über Google Ads", "Treppengeländer aus Eiche", "08:31"]],
        "new": ["inbox", "Neue Anfrage mit 3 Fotos", "Einbauschrank im Dachgeschoss", "09:41"],
        "me": "Wir sind vom 23.12. bis 2.1. im Betriebsurlaub. Bitte einen Hinweis auf die Seite.",
        "agent": "Ist drin. Der Hinweis steht oben auf jeder Seite und verschwindet am 3.1. von selbst.",
    },
    "praxis": {
        "chip": "Praxis", "name": "Zahnarztpraxis am Park", "host": "praxis-am-park.de", "channel": "wa",
        "kpi": ["Online-Termine diese Woche", 51, "+18 % zur Vorwoche"],
        "feed": [["calendar", "Online-Termin · Kontrolle", "Do, 16:00 · Neupatientin", "09:02"],
                 ["layout", "Anamnesebogen ausgefüllt", "Digital, vor dem Termin", "08:50"]],
        "new": ["calendar", "Online-Termin · Prophylaxe", "Di, 08:30 · über die Website", "09:41"],
        "me": "Ab sofort ist Mittwochnachmittag geschlossen. Bitte die Sprechzeiten anpassen.",
        "agent": "Erledigt. Die neuen Sprechzeiten sind online, die Online-Termine sind angepasst.",
    },
    "kanzlei": {
        "chip": "Kanzlei", "name": "Kanzlei Lindqvist", "host": "kanzlei-lindqvist.de", "channel": "cockpit",
        "kpi": ["Neue Mandate diesen Monat", 16, "+6 % zum Vormonat"],
        "feed": [["inbox", "Unterlagen hochgeladen", "Mandant Meier · 4 Dokumente", "09:10"],
                 ["video", "Erstberatung gebucht", "Mi, 10:00 · Video-Call", "08:44"]],
        "new": ["brief", "Neue Mandatsanfrage", "Kündigungsschutz · über die Website", "09:41"],
        "task": ["Profil vorbereitet: Dr. Sara Yilmaz", "Foto, Schwerpunkte und Lebenslauf sind eingepflegt. Soll das Profil online gehen?"],
        "agent": "Veröffentlicht. Dr. Yilmaz steht jetzt im Team auf der Website.",
    },
}
ORDER = ["gastro", "handwerk", "praxis", "kanzlei"]

_CHECK = icon("check")
_LOCK = icon("lock")


# ---------------------------------------------------------------- Zeichnungen für die Beispiel-Websites
ART = {
    "gastro": """<svg viewBox="0 0 200 150" preserveAspectRatio="xMidYMid slice" aria-hidden="true">
  <circle cx="104" cy="78" r="50" class="fb"/><circle cx="104" cy="78" r="50" class="sa" stroke-opacity=".55"/>
  <circle cx="104" cy="78" r="35" class="sa" stroke-opacity=".25"/>
  <path class="sg" d="M90 79c0-8 7-14 15-13s13 8 12 15-8 12-15 11-11-6-10-12 5-8 10-7 7 4 6 8-4 5-7 4"/>
  <path class="sg" d="M95 70c3-4 9-6 14-4M112 88c-3 3-8 4-12 3" stroke-opacity=".7"/>
  <path class="fa" d="M112 62c7-6 15-6 19-2-4 7-13 9-19 2z"/><path class="fa" d="M108 60c2-8 8-12 15-11-1 7-8 12-15 11z" opacity=".75"/>
  <path class="si" d="M38 30v18m-6-18v12a6 6 0 0 0 12 0V30M38 48v74"/>
  <path class="si" d="M168 30c-5 7-7 17-7 29 0 4 3 6 7 6v57"/>
</svg>""",
    "handwerk": """<svg viewBox="0 0 200 150" preserveAspectRatio="xMidYMid slice" aria-hidden="true">
  <g class="sa" stroke-opacity=".5">
    <path d="M-10 22c40-8 70 10 110 2s70-12 110-2"/><path d="M-10 40c38-6 72 12 112 4s70-14 108-4"/>
    <path d="M-10 58c36-4 70 6 98 2 10-2 18-14 30-14s20 12 32 14c18 2 36-4 50-2"/>
    <path d="M-10 76c34-4 66 6 96 2 12-2 18-18 32-18s22 16 34 18c16 2 34-4 48-2"/>
    <path d="M-10 94c38-6 70 8 104 4s76-12 116-2"/><path d="M-10 112c40-8 74 10 112 4s70-12 108-4"/>
    <path d="M-10 130c40-6 76 8 110 2s74-10 110-2"/>
  </g>
  <ellipse cx="118" cy="62" rx="11" ry="6" class="sa" stroke-opacity=".8"/><ellipse cx="118" cy="62" rx="4" ry="2" class="fa" opacity=".7"/>
</svg>""",
    "praxis": """<svg viewBox="0 0 200 150" preserveAspectRatio="xMidYMid slice" aria-hidden="true">
  <circle cx="100" cy="58" r="40" class="fb" opacity=".9"/>
  <path class="sa" stroke-width="2" d="M84 38c-9 0-15 7-15 17 0 12 5 18 7 28 2 9 3 17 8 17 6 0 5-14 10-20 2-3 6-3 8 0 5 6 4 20 10 20 5 0 6-8 8-17 2-10 7-16 7-28 0-10-6-17-15-17-6 0-9 3-12 3s-6-3-16-3z"/>
  <path class="sa" stroke-opacity=".5" d="M146 26l3 7 7 3-7 3-3 7-3-7-7-3 7-3z"/>
</svg>""",
    "kanzlei": """<svg viewBox="0 0 200 150" preserveAspectRatio="xMidYMid slice" aria-hidden="true">
  <g class="sa" stroke-opacity=".22"><path d="M20 128h160M30 120h140M40 50h120M100 18L36 46h128z"/><path d="M52 56v60M76 56v60M124 56v60M148 56v60"/></g>
  <text x="100" y="104" text-anchor="middle" class="fa" style="font:400 74px Georgia,'Times New Roman',serif">§</text>
</svg>""",
}


def mini_site(key, extra_cls=""):
    """Kleine Beispiel-Website eines Betriebs. Der Block .ms__info wird vom KI-Agenten „geändert“."""
    b = BRANCHES[key]
    flag = f'<span class="ms__flag">{_CHECK} Aktualisiert</span>'
    if key == "gastro":
        nav = "<i>Speisekarte</i><i>Mittagstisch</i><i>Kontakt</i>"
        copy = ("Italienische Küche in Ottensen", "Pasta wie in Bologna. Mitten in Hamburg.",
                "Hausgemacht, jeden Tag frisch – und mittags ein Gericht, das wechselt.", "Tisch reservieren", "Reservieren")
        info = f'<span class="ms__k">Mittagstisch heute</span><span class="ms__v"><span class="v-old">Tagliatelle al ragù · 11,90 €</span><span class="v-new">Kürbisrisotto · 12,50 €</span></span>{flag}'
        notice, art_extra = "", ""
    elif key == "handwerk":
        nav = "<i>Leistungen</i><i>Projekte</i><i>Werkstatt</i>"
        copy = ("Tischlerei in Lüneburg", "Möbel nach Maß. Aus der eigenen Werkstatt.",
                "Küchen, Einbauschränke und Treppen – geplant mit Ihnen, gebaut für Jahrzehnte.", "Projekt anfragen", "Anfragen")
        info = f'<span class="ms__k">Aktuell</span><span class="ms__v"><span class="v-old">Termine für Aufmaß ab 4. November</span><span class="v-new">Betriebsurlaub 23.12. bis 2.1.</span></span>{flag}'
        notice = '<div class="ms__notice"><span>Betriebsurlaub vom 23.12. bis 2.1. – ab dem 5.1. sind wir wieder für Sie da.</span></div>'
        art_extra = ""
    elif key == "praxis":
        nav = "<i>Leistungen</i><i>Team</i><i>Kontakt</i>"
        copy = ("Zahnarztpraxis in Eimsbüttel", "Gesunde Zähne. Termine in zwei Klicks.",
                "Moderne Zahnmedizin mit Zeit für Sie – und Online-Terminen rund um die Uhr.", "Termin buchen", "Termin")
        info = f'<span class="ms__k">Sprechzeiten Mittwoch</span><span class="ms__v"><span class="v-old">8–13 und 14–18 Uhr</span><span class="v-new">8–13 Uhr</span></span>{flag}'
        notice = ""
        art_extra = '<div class="ms__slots"><span>Di 08:30</span><span class="is-on">Mi 10:00</span><span>Do 16:00</span></div>'
    else:
        nav = "<i>Schwerpunkte</i><i>Team</i><i>Kontakt</i>"
        copy = ("Fachanwälte für Arbeitsrecht", "Arbeitsrecht, klar erklärt. Und konsequent vertreten.",
                "Kündigung, Abfindung, Arbeitsvertrag: Wir prüfen Ihren Fall und sagen ehrlich, was möglich ist.", "Erstberatung anfragen", "Kontakt")
        info = (f'<span class="ms__k">Ihr Team</span><span class="ms__v"><span class="v-old">4 Anwältinnen und Anwälte</span><span class="v-new">5 Anwältinnen und Anwälte</span></span>'
                f'<span class="ms__avatars"><i>KL</i><i>JM</i><i>AB</i><i>TS</i><i class="is-add">SY</i></span>')
        notice, art_extra = "", ""
    eyebrow, title, sub, cta, btn = copy
    return f"""<div class="ms ms--{key}{extra_cls}" aria-hidden="true">
  {notice}<div class="ms__nav"><span class="ms__logo">{e(b['name'])}</span><span class="ms__links">{nav}</span><span class="ms__btn">{btn}</span><span class="ms__burger"></span></div>
  <div class="ms__hero">
    <div class="ms__copy"><span class="ms__eyebrow">{eyebrow}</span><b class="ms__title">{title}</b><span class="ms__sub">{sub}</span><span class="ms__cta">{cta}</span></div>
    <div class="ms__art">{ART[key]}{art_extra}</div>
  </div>
  <div class="ms__info">{info}</div>
</div>"""


def _feed_item(it, slot, new=False):
    ic, t, s, time = it
    return (f'<div class="cp-feed__item{" is-new" if new else ""}" style="--slot:{slot}"><span class="ic">{icon(ic)}</span>'
            f'<b>{e(t)}</b><small>{e(s)}</small><time>{e(time)}</time></div>')


def cockpit(ctx):
    """Startseite: Cockpit mit Branchen-Umschalter. Ohne JavaScript steht der Endzustand „Restaurant“ da."""
    g = BRANCHES["gastro"]
    chips = "".join(
        f'<button class="chip" type="button" role="tab" id="cpt-{k}" aria-controls="cockpit" aria-selected="{"true" if k == "gastro" else "false"}" data-branch="{k}" tabindex="{0 if k == "gastro" else -1}">{BRANCHES[k]["chip"]}</button>'
        for k in ORDER)
    sites = "".join(mini_site(k) for k in ORDER)
    feed = _feed_item(g["new"], 0, True) + _feed_item(g["feed"][0], 1) + _feed_item(g["feed"][1], 2)
    data = {k: {kk: vv for kk, vv in v.items() if kk != "chip"} for k, v in BRANCHES.items()}
    icons = {n: icon(n) for n in ["calendar", "phone", "search", "inbox", "layout", "video", "brief"]}
    return f"""
<div class="hero__stage" data-intro style="--i:6">
  <div class="cp-ctl">
    <span class="cp-ctl__label" id="cp-label">Ihre Branche:</span>
    <div class="chips" role="tablist" aria-labelledby="cp-label">{chips}</div>
  </div>
  <div class="cockpit" id="cockpit" role="tabpanel" data-branch="gastro" data-cockpit aria-label="Beispiel: Cockpit eines Betriebs mit Website, Anfragen und KI-Agent">
    <div class="cp-bar">
      <span class="cp-bar__dots" aria-hidden="true"><i></i><i></i><i></i></span>
      <span class="cp-bar__app">{LOGO}Cockpit <span class="cp-bar__crumb" data-cp="name">/ {e(g['name'])}</span></span>
      <span class="cp-bar__right"><button class="cp-pause" type="button" aria-pressed="false" aria-label="Animation anhalten">{icon('pause', 'i-pause')}{icon('play', 'i-play')}</button><span class="badge badge--ok"><span class="live" aria-hidden="true"></span>Live</span><span class="cp-time tnum">09:41</span></span>
    </div>
    <div class="cp-body">
      <div class="cp-site">
        <div class="cp-site__bar">{_LOCK}<span data-cp="host">{e(g['host'])}</span><span class="badge">Ihre Website</span></div>
        <div class="cp-site__view">{sites}</div>
      </div>
      <div class="cp-side">
        <div class="cp-card">
          <div class="cp-card__h"><span data-cp="kpil">{e(g['kpi'][0])}</span></div>
          <div class="cp-kpi"><span class="cp-kpi__v" data-cp="kpi"><span>{g['kpi'][1] + 1}</span><span></span></span><span class="cp-kpi__d" data-cp="kpid">{e(g['kpi'][2])}</span></div>
        </div>
        <div class="cp-card">
          <div class="cp-card__h"><span>Neue Anfragen</span><span class="badge" data-cp="count">Heute 3</span></div>
          <div class="cp-feed" data-cp="feed">{feed}</div>
        </div>
        <div class="cp-card cp-agent">
          <div class="cp-card__h cp-agent__h"><span data-cp="ch">KI-Agent · per WhatsApp</span>{icon('bot')}</div>
          <div class="cp-msgs" data-cp="msgs">
            <div class="cp-msg cp-msg--me">{e(g['me'])}<time>09:38</time></div>
            <div class="cp-msg cp-msg--agent">{e(g['agent'])}<time>09:39</time></div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <p class="cp-note">Beispiel: So arbeiten Website, Kundensystem und KI-Agent bei einem Betrieb zusammen.</p>
  <script type="application/json" id="cockpit-data">{json.dumps({"b": data, "order": ORDER, "icons": icons, "check": _CHECK}, ensure_ascii=False)}</script>
</div>"""


# ---------------------------------------------------------------- Kundenreise: Relaunch alt → neu
def relaunch():
    chair = """<svg viewBox="0 0 200 160" preserveAspectRatio="xMidYMid slice" aria-hidden="true">
  <g fill="none" stroke="#8A5A2B" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" stroke-opacity=".7">
    <path d="M-10 26c40-8 70 10 110 2s70-12 110-2"/><path d="M-10 46c38-6 72 12 112 4s70-14 108-4" stroke-opacity=".45"/>
    <path d="M-10 136c40-6 76 8 110 2s74-10 110-2" stroke-opacity=".45"/>
  </g>
  <g fill="none" stroke="#1F1A15" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
    <path d="M78 44v44M122 44v44M78 50h44M78 64h44"/><path d="M70 88h60l-4 10H74z"/><path d="M76 98l-4 36M124 98l4 36M84 98l-2 26M116 98l2 26"/>
  </g>
</svg>"""
    return f"""
<div class="st__frame">
  <div class="frame__bar"><i></i><i></i><i></i><span class="frame__url">{_LOCK}tischlerei-brandt.de</span></div>
  <div class="rl" data-relaunch style="--p:100%" aria-hidden="true">
    <div class="rl__old">
      <div class="o-head"><span class="o-logo">Tischlerei Brandt</span><span class="o-tel">Tel. 04131 / 12 34 5</span></div>
      <div class="o-nav"><span>Home</span><span>Über uns</span><span>Leistungen</span><span>Galerie</span><span>Kontakt</span><span>Impressum</span></div>
      <div class="o-main">
        <div class="o-side"><b>Aktuelles</b><span>Unsere neue Homepage ist online!</span><span>Öffnungszeiten: Mo–Fr 7–16 Uhr</span><div class="o-counter">004711</div></div>
        <div class="o-content"><h4>Herzlich Willkommen!</h4><div class="o-img">[ Bild wird geladen … ]</div>
          <p>Auf unserer Homepage finden Sie Informationen über unsere Firma. Wir sind ein Handwerksbetrieb und fertigen Möbel aller Art.</p>
          <span class="o-link">» Hier klicken für mehr Infos</span></div>
      </div>
      <div class="o-marquee">+++ Besuchen Sie uns auch auf unserer Facebook-Seite +++ Optimiert für Internet Explorer +++</div>
    </div>
    <div class="rl__new">
      <div class="n-nav"><span class="n-logo">Tischlerei Brandt</span><span class="n-links"><span>Leistungen</span><span>Projekte</span><span>Werkstatt</span></span><span class="n-btn">Projekt anfragen</span></div>
      <div class="n-hero">
        <div class="n-copy"><span class="n-eyebrow">Tischlerei in Lüneburg</span><b class="n-title">Möbel nach Maß. Aus der eigenen Werkstatt.</b>
          <span class="n-sub">Küchen, Einbauschränke und Treppen – geplant mit Ihnen, gebaut für Jahrzehnte.</span>
          <span class="n-ctas"><span class="n-cta">Projekt anfragen</span><span class="n-cta n-cta--ghost">Rückruf</span></span></div>
        <div class="n-art">{chair}<span class="n-trust"><i></i>Antwort innerhalb von 24 h</span></div>
      </div>
    </div>
    <span class="rl__scan"></span>
  </div>
  <div class="rl-ctl">
    <div class="chips" role="group" aria-label="Ansicht"><button class="chip" type="button" data-rl="0" aria-pressed="false">Vorher</button><button class="chip" type="button" data-rl="100" aria-pressed="true">Nachher</button></div>
    <span class="rl-ctl__hint">Beispiel eines Relaunchs</span>
  </div>
</div>"""


# ---------------------------------------------------------------- Kundenreise: Pipeline im Kundensystem
def pipeline():
    cols = [("neu", "Neu"), ("gespraech", "Im Gespräch"), ("angebot", "Angebot"), ("auftrag", "Auftrag")]
    cards = [
        ("c1", "neu", "Familie Petersen", "Einbauküche · Website", "heute"),
        ("c2", "neu", "Herr Kaya", "Rückruf · Telefon", "heute"),
        ("c3", "gespraech", "Weber GmbH", "Büroausbau · Google Ads", "Termin Do"),
        ("c4", "angebot", "Frau Lindner", "Treppe Eiche · Empfehlung", "läuft ab Fr"),
        ("c5", "auftrag", "Praxis Nord", "Empfangstresen", "in Arbeit"),
    ]
    by = {k: [] for k, _ in cols}
    for c in cards:
        by[c[1]].append(c)
    colhtml = ""
    for k, name in cols:
        inner = "".join(
            f'<div class="pl__card" data-card="{cid}"><b>{e(n)}</b><small>{e(s)}</small><span class="pl__tag">{e(t)}</span></div>'
            for cid, _, n, s, t in by[k])
        colhtml += f'<div class="pl__col" data-col="{k}"><h5>{name}<span data-colcount>{len(by[k])}</span></h5>{inner}</div>'
    return f"""
<div class="st__frame">
  <div class="frame__bar"><i></i><i></i><i></i><span class="frame__url">{_LOCK}cockpit.tischlerei-brandt.de</span></div>
  <div class="pl" data-pipeline aria-hidden="true">
    <div class="pl__kpis">
      <div class="pl__kpi"><small>Offene Anfragen</small><b data-plk="open">6</b></div>
      <div class="pl__kpi"><small>Termine diese Woche</small><b>9</b></div>
      <div class="pl__kpi"><small>Angebote unterwegs</small><b data-plk="offers">3</b></div>
    </div>
    <div class="pl__board">{colhtml}</div>
    <div class="pl__agent">{icon('bot')}<span><b>KI-Agent:</b> <span data-plmsg>Das Angebot für Frau Lindner läuft am Freitag ab. Soll ich nachfassen?</span></span></div>
  </div>
</div>"""


# ---------------------------------------------------------------- Kundenreise: KI-Agent zum Ausprobieren
AGENT_ASKS = [
    {"id": "mittag", "label": "Mittagstisch ändern", "me": "Heute gibt’s Kürbisrisotto als Mittagstisch, 12,50 €. Bitte auf die Website.",
     "agent": "Erledigt. Der Mittagstisch ist online.", "k": "Mittagstisch heute", "v": "Kürbisrisotto · 12,50 €"},
    {"id": "zeiten", "label": "Öffnungszeiten anpassen", "me": "Am 24.12. haben wir nur bis 14 Uhr geöffnet. Kannst du das eintragen?",
     "agent": "Ist eingetragen. Heiligabend: 11–14 Uhr.", "k": "Heiligabend", "v": "Geöffnet 11–14 Uhr"},
    {"id": "event", "label": "Veranstaltung ankündigen", "me": "Am 15.11. ist Weinabend mit Menü für 49 €. Bitte groß auf die Startseite.",
     "agent": "Steht drauf, inklusive Button zum Reservieren.", "k": "Weinabend am 15.11.", "v": "4-Gänge-Menü · 49 €"},
]


def agent_demo():
    asks = "".join(
        f'<button class="ad__ask" type="button" data-ask-id="{a["id"]}" aria-pressed="false">{icon("send")}<span>{e(a["label"])}</span></button>'
        for a in AGENT_ASKS)
    return f"""
<div class="st__frame">
  <div class="ad" data-agent>
    <div class="ad__phone" aria-hidden="true">
      <div class="ad__screen">
        <div class="wa">
          <div class="wa__top"><span class="wa__ava">{LOGO}</span><span><b>Medialyte KI-Agent</b><small>online</small></span></div>
          <div class="wa__body" data-wa><span class="wa__day">Heute</span></div>
        </div>
      </div>
    </div>
    <div class="ad__side">
      <span class="ad__label" id="ad-label">Probieren Sie es aus – schicken Sie eine Änderung:</span>
      <div class="ad__asks" role="group" aria-labelledby="ad-label">{asks}</div>
      <div class="ad__site" aria-hidden="true">
        <div class="cp-site__bar">{_LOCK}<span>trattoria-lume.de</span><span class="badge">Live</span></div>
        <div class="cp-site__view">{mini_site("gastro", " ms--demo")}</div>
      </div>
      <p class="sr-only" aria-live="polite" data-agent-live></p>
    </div>
  </div>
  <script type="application/json" id="agent-data">{json.dumps(AGENT_ASKS, ensure_ascii=False)}</script>
</div>"""


# ---------------------------------------------------------------- Kundenreise: Kampagne
def campaign():
    pts = [(0, 92), (30, 88), (60, 84), (90, 86), (120, 70), (150, 68), (180, 56), (210, 50), (240, 38), (270, 32), (300, 20)]
    line = " ".join(f"{'M' if i == 0 else 'L'}{x} {y}" for i, (x, y) in enumerate(pts))
    return f"""
<div class="st__frame">
  <div class="cg" data-campaign aria-hidden="true">
    <div class="serp">
      <div class="serp__q">{icon('search')}italienisches restaurant ottensen</div>
      <div class="serp__ad"><small><b>Gesponsert</b>trattoria-lume.de</small><strong>Trattoria Lume – Pasta wie in Bologna, mitten in Ottensen</strong>
        <p>Hausgemachte Pasta und täglich wechselnder Mittagstisch. Jetzt online einen Tisch reservieren.</p>
        <div class="serp__links"><span>Speisekarte</span><span>Tisch reservieren</span><span>Mittagstisch</span></div></div>
      <div class="serp__org"><i style="width:38%"></i><i style="width:86%"></i><i style="width:64%"></i></div>
    </div>
    <div class="cg__panel">
      <div class="cg__head"><b>Kampagne „Mittagstisch“</b><span class="badge badge--ok"><span class="live"></span>Aktiv</span></div>
      <svg class="cg__chart" viewBox="0 0 300 110">
        <defs><linearGradient id="cgfill" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#C3CDDC" stop-opacity=".22"/><stop offset="1" stop-color="#C3CDDC" stop-opacity="0"/></linearGradient></defs>
        <g stroke="rgba(170,190,220,.1)"><path d="M0 27h300M0 55h300M0 83h300"/></g>
        <path class="area" d="{line} L300 110 L0 110Z" fill="url(#cgfill)"/>
        <path class="line" d="{line}" fill="none" stroke="#F3F5F9" stroke-width="2" stroke-linejoin="round" stroke-linecap="round" pathLength="1"/>
      </svg>
      <div class="cg__rows">
        <div><small>Klicks diese Woche</small><b data-count-to="1248">1.248</b></div>
        <div><small>Anrufe über die Anzeige</small><b data-count-to="64">64</b></div>
        <div><small>Reservierungen</small><b data-count-to="37">37</b></div>
      </div>
    </div>
  </div>
</div>"""

