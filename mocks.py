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
        "agent": "Ist drin. Der Hinweis steht oben auf jeder Seite und verschwindet am 4.1. von selbst.",
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


# ---------------------------------------------------------------- Beispiel-Websites
# Jede Seite zeigt das, was sie für den Betrieb leisten soll: reservieren, anfragen, Termin buchen.
# Rechts steht deshalb kein Bild, sondern die wichtigste Funktion der Seite als Karte.
# Was ein Besucher auf der Beispiel-Website auswählen kann – und was danach im Cockpit ankommt.
# {v} wird durch die Auswahl ersetzt.
FORMS = {
    "gastro": {"groups": {"time": ("Uhrzeit", ["18:30", "19:00", "19:30", "20:00"], "19:30")},
               # Antippen wechselt den Tag; Personen über − und +
               "cycles": {"date": [{"label": "Fr, 20. Nov.", "dateShort": "Fr", "dateDay": "Freitag"},
                                   {"label": "Sa, 21. Nov.", "dateShort": "Sa", "dateDay": "Samstag"},
                                   {"label": "So, 22. Nov.", "dateShort": "So", "dateDay": "Sonntag"}]},
               "persons": 2,
               "feed": ["calendar", "Reservierung · {personsText}", "{dateShort}, {time} · gerade über die Website"],
               "done": "Reserviert: {label}, {time} Uhr, {personsText}", "again": "Noch einen Tisch reservieren",
               "agent": "Neue Reservierung für {dateDay}, {time} Uhr, {personsText}. Die Bestätigung ist schon beim Gast."},
    "handwerk": {"groups": {"topic": ("Projekt", ["Küche", "Einbauschrank", "Treppe"], "Einbauschrank")},
                 "feed": ["inbox", "Neue Anfrage mit 3 Fotos", "{topic} · gerade über die Website"],
                 "done": "Anfrage gesendet: {topic}", "again": "Weitere Anfrage stellen",
                 "agent": "Neue Anfrage zu „{topic}“ mit 3 Fotos. Ich habe einen Rückruf für morgen früh vorgeschlagen.",
                 "area": {"Küche": "Neue Küche, etwa 4 m Zeile mit Insel, Eiche hell.",
                          "Einbauschrank": "Einbauschrank unter der Dachschräge, ca. 3 m breit, Eiche hell.",
                          "Treppe": "Treppe mit Stahlwange, 14 Stufen, Esche geölt."}},
    "praxis": {"groups": {"day": ("Tag", ["Di 17", "Mi 18", "Do 19", "Fr 20"], "Mi 18"),
                          "time": ("Uhrzeit", ["08:30", "10:00", "15:30"], "10:00")},
               "cycles": {"treat": [{"label": "Kontrolle und Beratung", "treat": "Kontrolle"},
                                    {"label": "Professionelle Zahnreinigung", "treat": "Zahnreinigung"},
                                    {"label": "Beschwerden oder Schmerzen", "treat": "Akuttermin"}]},
               "feed": ["calendar", "Online-Termin · {treat}", "{dayShort}, {time} · gerade über die Website"],
               "done": "Termin gebucht: {dayLong}, {time} Uhr", "again": "Weiteren Termin buchen",
               "agent": "Neuer Online-Termin am {dayShort} um {time} Uhr. Die Erinnerung geht am Vortag raus.",
               "days": {"Di 17": ["Di, 17.11.", "Dienstag, 17. November"], "Mi 18": ["Mi, 18.11.", "Mittwoch, 18. November"],
                        "Do 19": ["Do, 19.11.", "Donnerstag, 19. November"], "Fr 20": ["Fr, 20.11.", "Freitag, 20. November"]}},
    "kanzlei": {"groups": {"topic": ("Anliegen", ["Kündigung erhalten", "Abfindung verhandeln", "Arbeitsvertrag prüfen"], "Kündigung erhalten")},
                "feed": ["brief", "Neue Mandatsanfrage", "{topic} · gerade über die Website"],
                "done": "Anfrage gesendet: {topic}", "again": "Weitere Anfrage stellen",
                "agent": "Neue Mandatsanfrage: {topic}. Ich habe drei Termine für die Erstberatung vorgeschlagen."},
}


def _opts(key, name, live, render):
    """Auswahlknöpfe einer Gruppe. Im Cockpit echte Knöpfe, sonst nur Darstellung."""
    label, values, default = FORMS[key]["groups"][name]
    out = ""
    for v in values:
        on = v == default
        inner = render(v)
        pm = ' mc__pm' if (key == "praxis" and v == "15:30") else ""
        if live:
            out += (f'<button type="button" class="mc__o{" is-on" if on else ""}{pm}" role="radio" aria-checked="{"true" if on else "false"}" '
                    f'tabindex="{0 if on else -1}" data-v="{e(v)}">{inner}</button>')
        else:
            out += f'<span class="mc__o{" is-on" if on else ""}{pm}">{inner}</span>'
    attrs = f' role="radiogroup" aria-label="{label}" data-msgroup="{name}"' if live else ""
    return attrs, out


def _widget(key, live=False):
    """Funktionskarte der Beispiel-Website. live=True: bedienbar, das Ergebnis landet im Cockpit."""
    f = FORMS[key]
    def btn(text, cls="mc__btn", data=" data-mssubmit"):
        return f'<button type="button" class="{cls}"{data}>{text}</button>' if live else f'<span class="{cls}">{text}</span>'
    done = (f'<div class="mc__done" aria-live="polite"><span class="mc__ok">{_CHECK}</span><b data-msdone></b>'
            f'<small data-mswhere>Steht jetzt im Dashboard bei den Anfragen.</small>{btn(f["again"], "mc__again", " data-msagain")}</div>') if live else ""
    region = f' role="group" aria-label="Beispiel zum Ausprobieren" data-msform="{key}"' if live else ""
    def cycle(name, label):
        first = f["cycles"][name][0]["label"]
        if live:
            return (f'<button type="button" class="mc__f mc__f--sel mc__f--pick" data-mscycle="{name}" aria-label="{label}: {e(first)} – antippen zum Ändern">'
                    f'<small>{label}</small><span data-mscyclev>{e(first)}</span></button>')
        return f'<span class="mc__f mc__f--sel"><small>{label}</small>{e(first)}</span>'
    if key == "gastro":
        ga, go = _opts(key, "time", live, lambda v: v)
        n = f["persons"]
        persons = (f'<span class="mc__f mc__f--step"><small>Personen</small><span class="mc__step">'
                   f'<button type="button" data-msstep="-1" aria-label="Eine Person weniger">−</button><b data-mspersons aria-live="polite">{n}</b>'
                   f'<button type="button" data-msstep="1" aria-label="Eine Person mehr">+</button></span></span>') if live else f'<span class="mc__f"><small>Personen</small>{n}</span>'
        body = f"""<b class="mc__h">Tisch reservieren</b>
      <div class="mc__row">{cycle("date", "Datum")}{persons}</div>
      <div class="mc__slots"{ga}>{go}</div>
      {btn("Jetzt reservieren")}
      <span class="mc__meta"><i class="mc__dot"></i>Heute noch 4 Tische frei</span>"""
    elif key == "handwerk":
        ga, go = _opts(key, "topic", live, lambda v: v)
        body = f"""<b class="mc__h">Projekt anfragen</b>
      <div class="mc__chips"{ga}>{go}</div>
      <span class="mc__area" data-msarea>{f["area"]["Einbauschrank"]}</span>
      <div class="mc__photos"><i class="p1"></i><i class="p2"></i><i class="p3"></i><span>3 Fotos angehängt</span></div>
      {btn("Anfrage senden")}"""
    elif key == "praxis":
        da, do = _opts(key, "day", live, lambda v: f"<small>{v[:2]}</small>{v[3:]}")
        ta, to = _opts(key, "time", live, lambda v: v)
        body = f"""<b class="mc__h">Online-Termin</b>
      {cycle("treat", "Behandlung")}
      <div class="mc__days"{da}>{do}</div>
      <div class="mc__slots mc__slots--3"{ta}>{to}</div>
      {btn("Termin buchen")}"""
    else:
        ga, go = _opts(key, "topic", live, lambda v: f"<i></i>{v}")
        body = f"""<b class="mc__h">Erstberatung anfragen</b>
      <span class="mc__q">Worum geht es?</span>
      <div class="mc__opts"{ga}>{go}</div>
      {btn("Anfrage senden")}
      <span class="mc__meta">Antwort innerhalb von 24 Stunden</span>"""
    return f'<div class="ms__card"{region}><div class="mc__form">{body}</div>{done}</div>'


_MORE = {
    "gastro": ("Aus der Karte", [("Primi", "Tagliatelle al ragù", "11,90 €"), ("Primi", "Risotto ai funghi", "13,50 €"), ("Dolci", "Tiramisù della casa", "6,50 €")]),
    "handwerk": ("Aus der Werkstatt", [("w1", "Einbauküche", "Eiche, geölt"), ("w2", "Treppe mit Stahlwange", "Esche, lackiert"), ("w3", "Garderobe nach Maß", "Nussbaum, gewachst")]),
    "praxis": ("Unsere Leistungen", [("spark", "Prophylaxe", "Professionelle Zahnreinigung"), ("shield", "Implantate", "Beratung und Planung"), ("heart", "Kinder", "Mit viel Zeit und Ruhe")]),
    "kanzlei": ("Schwerpunkte", [("§", "Kündigungsschutz", "Fristen sicher wahren"), ("§", "Abfindung", "Verhandeln statt verlieren"), ("§", "Arbeitsverträge", "Prüfen vor dem Unterschreiben")]),
}


_STRIP = {
    "gastro": [("Mittags", "Di–Fr 12–15 Uhr"), ("Abends", "Di–So 18–23 Uhr"), ("Adresse", "Hamburg-Ottensen")],
    "handwerk": [("Werkstatt", "Mo–Fr 7–16 Uhr"), ("Aufmaß", "Kostenfrei vor Ort"), ("Region", "Lüneburg und Umgebung")],
    "praxis": [("Sprechzeiten", "Mo–Fr ab 8 Uhr"), ("Online-Termine", "Rund um die Uhr"), ("Adresse", "Hamburg-Eimsbüttel")],
    "kanzlei": [("Erstberatung", "Telefon oder Video"), ("Antwort", "Innerhalb von 24 Stunden"), ("Standort", "Hamburg")],
}


def _more(key):
    h, items = _MORE[key]
    tiles = ""
    for a, t, s in items:
        if key == "handwerk":
            top = f'<i class="ms__sw ms__sw--{a}"></i>'
        elif key == "praxis":
            top = f'<span class="ms__ic">{icon(a)}</span>'
        elif key == "kanzlei":
            top = '<span class="ms__par">§</span>'
        else:
            top = f'<small class="ms__cat">{e(a)}</small>'
        tiles += f"<div>{top}<b>{e(t)}</b><small>{e(s)}</small></div>"
    strip = "".join(f"<span><small>{e(a)}</small>{e(b)}</span>" for a, b in _STRIP[key])
    return f'<div class="ms__more"><b class="ms__more-h">{h}</b><div class="ms__tiles">{tiles}</div><div class="ms__strip">{strip}</div></div>'


_EVENT = ('<div class="ms__event"><small data-ev="k"></small><b data-ev="t"></b><span data-ev="p"></span>'
          '<span class="ms__event-btn" data-ev="b"></span><span class="ms__event-new">Neu</span></div>')


def mini_site(key, extra_cls="", live=False, event=False):
    """Kleine Beispiel-Website eines Betriebs. Der Block .ms__info wird vom KI-Agenten „geändert“.
    live=True (Cockpit): Die Funktionskarte ist bedienbar, der Rest bleibt Darstellung.
    event=True (Agent-Demo): Platz für eine Veranstaltung, die groß im Startbereich erscheint."""
    b = BRANCHES[key]
    flag = f'<span class="ms__flag">{_CHECK} Aktualisiert</span>'
    notice = ""
    if key == "gastro":
        nav = "<i>Speisekarte</i><i>Mittagstisch</i><i>Kontakt</i>"
        copy = ("Italienische Küche in Ottensen", "Pasta wie in Bologna. Mitten in Hamburg.",
                "Hausgemacht, jeden Tag frisch – und mittags ein Gericht, das wechselt.", "Tisch reservieren", "Reservieren")
        info = f'<span class="ms__k">Mittagstisch heute</span><span class="ms__v"><span class="v-old">Tagliatelle al ragù · 11,90 €</span><span class="v-new">Kürbisrisotto · 12,50 €</span></span>{flag}'
    elif key == "handwerk":
        nav = "<i>Leistungen</i><i>Projekte</i><i>Werkstatt</i>"
        copy = ("Tischlerei in Lüneburg", "Möbel nach Maß. Aus der eigenen Werkstatt.",
                "Küchen, Einbauschränke und Treppen – geplant mit Ihnen, gebaut für Jahrzehnte.", "Projekt anfragen", "Anfragen")
        info = f'<span class="ms__k">Aktuell</span><span class="ms__v"><span class="v-old">Termine für das Aufmaß ab 9. November</span><span class="v-new">Betriebsurlaub 23.12. bis 2.1.</span></span>{flag}'
        notice = '<div class="ms__notice"><span>Betriebsurlaub vom 23.12. bis 2.1. – ab dem 4.1. sind wir wieder für Sie da.</span></div>'
    elif key == "praxis":
        nav = "<i>Leistungen</i><i>Team</i><i>Kontakt</i>"
        copy = ("Zahnarztpraxis in Eimsbüttel", "Gesunde Zähne. Termine in zwei Klicks.",
                "Moderne Zahnmedizin mit Zeit für Sie – und Online-Terminen rund um die Uhr.", "Termin buchen", "Termin")
        info = f'<span class="ms__k">Sprechzeiten Mittwoch</span><span class="ms__v"><span class="v-old">8–13 und 14–18 Uhr</span><span class="v-new">8–13 Uhr</span></span>{flag}'
    else:
        nav = "<i>Schwerpunkte</i><i>Team</i><i>Ratgeber</i>"
        copy = ("Fachanwälte für Arbeitsrecht", "Arbeitsrecht, klar erklärt. Und konsequent vertreten.",
                "Kündigung, Abfindung, Arbeitsvertrag: Wir prüfen Ihren Fall und sagen ehrlich, was möglich ist.", "Erstberatung anfragen", "Kontakt")
        info = (f'<span class="ms__k">Ihr Team</span><span class="ms__v"><span class="v-old">4 Anwältinnen und Anwälte</span><span class="v-new">5 Anwältinnen und Anwälte</span></span>'
                f'<span class="ms__avatars"><i>KL</i><i>JM</i><i>AB</i><i>TS</i><i class="is-add">SY</i></span>')
    eyebrow, title, sub, cta, btn = copy
    h = ' aria-hidden="true"'
    root_h = ("" if key == "gastro" else " inert") if live else h   # Cockpit: nur der gewählte Betrieb ist bedienbar (JS schaltet um)
    part_h = h if live else ""
    cta_el = (f'<button type="button" class="ms__cta" data-mscta>{cta}</button>' if live else f'<span class="ms__cta">{cta}</span>')
    nav_btn = (f'<button type="button" class="ms__btn" data-mscta tabindex="-1">{btn}</button>' if live else f'<span class="ms__btn">{btn}</span>')
    return f"""<div class="ms ms--{key}{extra_cls}"{root_h}>
  {notice}<div class="ms__page">
  <div class="ms__nav"><span class="ms__logo"{part_h}>{e(b['name'])}</span><span class="ms__links"{part_h}>{nav}</span>{nav_btn}<span class="ms__burger"{part_h}></span></div>
  <div class="ms__hero">
    <div class="ms__copy"><span class="ms__eyebrow"{part_h}>{eyebrow}</span><b class="ms__title"{part_h}>{title}</b><span class="ms__sub"{part_h}>{sub}</span>{cta_el}</div>
    {_EVENT if event else ""}{_widget(key, live)}
  </div>
  <div class="ms__info"{part_h}>{info}</div>
  <div{part_h}>{_more(key)}</div>
  </div>
  {'<p class="ms__toast" role="status" data-mstoast></p>' if live else ''}
</div>"""


def _feed_item(it, slot, new=False):
    ic, t, s, time = it
    return (f'<div class="cp-feed__item{" is-new" if new else ""}" style="--slot:{slot}"><span class="ic">{icon(ic)}</span>'
            f'<b>{e(t)}</b><small>{e(s)}</small><time>{e(time)}</time></div>')


def cockpit(ctx):
    """Startseite: Cockpit mit Branchen-Umschalter. Ohne JavaScript steht der Endzustand „Restaurant“ da."""
    g = BRANCHES["gastro"]
    tabs = "".join(
        f'<button class="cp-tab" type="button" role="tab" id="cpt-{k}" aria-controls="cp-panel" aria-selected="{"true" if k == "gastro" else "false"}" data-branch="{k}" tabindex="{0 if k == "gastro" else -1}">{BRANCHES[k]["chip"]}</button>'
        for k in ORDER)
    sites = "".join(mini_site(k, live=True) for k in ORDER)
    feed = _feed_item(g["new"], 0, True) + _feed_item(g["feed"][0], 1) + _feed_item(g["feed"][1], 2)
    data = {k: {**{kk: vv for kk, vv in v.items() if kk != "chip"}, "form": {"feed": FORMS[k]["feed"], "done": FORMS[k]["done"], "agent": FORMS[k]["agent"], "area": FORMS[k].get("area"), "days": FORMS[k].get("days"), "cycles": FORMS[k].get("cycles"), "persons": FORMS[k].get("persons")}} for k, v in BRANCHES.items()}
    icons = {n: icon(n) for n in ["calendar", "phone", "search", "inbox", "layout", "video", "brief"]}
    return f"""
<figure class="hero__stage" data-intro style="--i:6">
  <div class="cockpit" id="cockpit" data-branch="gastro" data-cockpit>
    <div class="cp-bar">
      <span class="cp-bar__lead"><span class="cp-bar__dots" aria-hidden="true"><i></i><i></i><i></i></span><span class="cp-bar__app">{LOGO}Dashboard</span></span>
      <div class="cp-tabs" role="tablist" aria-label="Beispiel-Betrieb wählen">{tabs}<i class="cp-tabs__ind" aria-hidden="true"></i></div>
      <span class="cp-bar__right"><button class="cp-pause" type="button" aria-pressed="false" aria-label="Animation anhalten">{icon('pause', 'i-pause')}{icon('play', 'i-play')}</button><span class="badge badge--ok"><span class="live" aria-hidden="true"></span>Live</span><span class="cp-time tnum" data-cp="time">09:41</span></span>
    </div>
    <div class="cp-body" id="cp-panel" role="tabpanel" aria-labelledby="cpt-gastro" data-cp="panel">
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
  <p class="sr-only" aria-live="polite" data-cp-live></p>
  <script type="application/json" id="cockpit-data">{json.dumps({"b": data, "order": ORDER, "icons": icons, "check": _CHECK}, ensure_ascii=False)}</script>
  <figcaption class="cp-note">Beispiel mit erfundenen Betrieben. Probieren Sie es aus: Schicken Sie auf der Beispiel-Website eine Reservierung oder Anfrage ab – sie landet sofort im Dashboard. Oben wechseln Sie die Branche.</figcaption>
</figure>"""


# ---------------------------------------------------------------- Kundenreise: Relaunch alt → neu
def relaunch():
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
    <div class="rl__new">{mini_site("handwerk", " ms--on ms--rl")}</div>
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
    names = dict(cols)
    colhtml = ""
    for k, name in cols:
        inner = "".join(
            f'<button type="button" class="pl__card" data-card="{cid}" data-st="{k}" ><b>{e(n)}</b><small>{e(s)}</small><span class="pl__tag">{e(t)}</span><span class="pl__st">{names[k]}</span><span class="sr-only">, in den nächsten Schritt schieben</span></button>'
            for cid, _, n, s, t in by[k])
        colhtml += f'<div class="pl__col" data-col="{k}"><h5>{name}<span data-colcount>{len(by[k])}</span></h5>{inner}</div>'
    return f"""
<div class="st__frame">
  <div class="frame__bar"><i></i><i></i><i></i><span class="frame__url">{_LOCK}dashboard.tischlerei-brandt.de</span></div>
  <div class="pl" data-pipeline>
    <div class="pl__kpis">
      <div class="pl__kpi"><small>Offene Anfragen</small><b data-plk="open">6</b></div>
      <div class="pl__kpi"><small>Termine diese Woche</small><b>9</b></div>
      <div class="pl__kpi"><small>Angebote offen</small><b data-plk="offers">3</b></div>
    </div>
    <div class="pl__board">{colhtml}</div>
    <div class="pl__agent">{icon('bot')}<span aria-live="polite"><b>KI-Agent:</b> <span data-plmsg>Das Angebot für Frau Lindner läuft am Freitag ab. Soll ich nachfassen?</span></span><button type="button" class="pl__reply" data-plreply>Ja, nachfassen</button></div>
  </div>
</div>"""


# ---------------------------------------------------------------- Kundenreise: KI-Agent zum Ausprobieren
AGENT_ASKS = [
    # Jede Nachricht hat Varianten: Ein zweiter Klick zeigt eine neue Änderung statt derselben noch einmal.
    {"id": "mittag", "label": "Mittagstisch ändern", "variants": [
        {"me": "Heute gibt’s Kürbisrisotto als Mittagstisch, 12,50 €. Bitte auf die Website.",
         "agent": "Erledigt. Der Mittagstisch ist online.", "type": "info", "k": "Mittagstisch heute", "v": "Kürbisrisotto · 12,50 €"},
        {"me": "Morgen gibt’s Saltimbocca mit Rosmarinkartoffeln, 14,90 €. Kannst du das schon eintragen?",
         "agent": "Ist eingetragen – steht ab morgen früh auf der Website.", "type": "info", "k": "Mittagstisch morgen", "v": "Saltimbocca · 14,90 €"}]},
    {"id": "zeiten", "label": "Öffnungszeiten anpassen", "variants": [
        {"me": "Am 24.12. haben wir nur bis 14 Uhr geöffnet. Kannst du das eintragen?",
         "agent": "Ist eingetragen. Heiligabend: 11–14 Uhr.", "type": "info", "k": "Heiligabend", "v": "Geöffnet 11–14 Uhr"},
        {"me": "Silvester sind wir komplett ausgebucht. Bitte einen Hinweis auf die Seite.",
         "agent": "Steht drauf. Reservierungen gibt es wieder ab dem 2.1.", "type": "info", "k": "Silvester", "v": "Ausgebucht – ab 2.1. wieder frei"}]},
    {"id": "event", "label": "Veranstaltung ankündigen", "variants": [
        {"me": "Am Samstag, 14.11., ist Weinabend mit Menü für 49 €. Bitte groß auf die Startseite.",
         "agent": "Steht groß auf der Startseite – mit Button zum Reservieren.", "type": "event",
         "ek": "Weinabend · Sa, 14.11.", "et": "4-Gänge-Menü mit Weinbegleitung", "ep": "49 € pro Person", "eb": "Platz reservieren"},
        {"me": "Der Weinabend ist ausgebucht. Der nächste ist am 12.12. – kannst du das ändern?",
         "agent": "Geändert: ausgebucht, der 12.12. ist schon buchbar.", "type": "event",
         "ek": "Weinabend · Sa, 14.11. ausgebucht", "et": "Nächster Weinabend am 12.12.", "ep": "4 Gänge mit Wein · 49 €", "eb": "Jetzt vormerken"}]},
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
        <div class="cp-site__view">{mini_site("gastro", " ms--on ms--demo", event=True)}</div>
      </div>
      <p class="sr-only" aria-live="polite" data-agent-live></p>
    </div>
  </div>
  <script type="application/json" id="agent-data">{json.dumps(AGENT_ASKS, ensure_ascii=False)}</script>
</div>"""


# ---------------------------------------------------------------- Kundenreise: Kampagne
def campaign():
    # flache Kurve (300 × 84), damit die Kampagne auch auf kleineren Laptops ohne Verkleinern passt
    pts = [(0, 70), (30, 67), (60, 64), (90, 66), (120, 53), (150, 52), (180, 43), (210, 38), (240, 29), (270, 24), (300, 15)]
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
      <svg class="cg__chart" viewBox="0 0 300 84">
        <defs><linearGradient id="cgfill" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#C3CDDC" stop-opacity=".22"/><stop offset="1" stop-color="#C3CDDC" stop-opacity="0"/></linearGradient></defs>
        <g stroke="rgba(170,190,220,.1)"><path d="M0 21h300M0 42h300M0 63h300"/></g>
        <path class="area" d="{line} L300 84 L0 84Z" fill="url(#cgfill)"/>
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



# ---------------------------------------------------------------- Online-Marketing: Monatsbericht in klarer Sprache
def report():
    rows = [("Google-Anzeige", 37), ("Google Maps", 21), ("Direkt über die Website", 18), ("Instagram", 12)]
    top = max(v for _, v in rows)
    bars = "".join(
        f'<li><span class="rp__k">{e(k)}</span><span class="rp__bar"><i style="--w:{v / top:.3f}"></i></span><b data-count-to="{v}">{v}</b></li>'
        for k, v in rows)
    return f"""
<div class="st__frame">
  <div class="frame__bar"><i></i><i></i><i></i><span class="frame__url">{_LOCK}dashboard.trattoria-lume.de/bericht</span></div>
  <div class="rp" data-report aria-hidden="true">
    <div class="rp__head"><span><small>Monatsbericht Oktober</small><b>Trattoria Lume</b></span><span class="rp__stamp">Stand 31.10.</span></div>
    <div class="rp__sum"><small>Kurz gesagt</small><p>Die Anzeige für den Mittagstisch bringt die meisten Reservierungen. Freitags ist am meisten los – dort setzen wir im November mehr Budget ein.</p></div>
    <div class="rp__kpis">
      <div><small>Reservierungen</small><b data-count-to="88">88</b><span class="rp__d">+24 % zum Vormonat</span></div>
      <div><small>Anrufe über Google</small><b data-count-to="64">64</b><span class="rp__d">+11 % zum Vormonat</span></div>
      <div><small>Kosten je Reservierung</small><b>3,40 €</b><span class="rp__d">−18 % zum Vormonat</span></div>
    </div>
    <div class="rp__ch"><small>Woher die Reservierungen kommen</small><ul>{bars}</ul></div>
  </div>
</div>"""


# ---------------------------------------------------------------- KI-Agent: Änderungen im Dashboard (umfangreiche Systeme)
AGENT_DONE = [("Sprechzeiten zwischen den Jahren eingetragen", "gestern"),
              ("Ratgeber „Kündigung – was jetzt?“ veröffentlicht", "Mo"),
              ("Stellenanzeige fürs Sekretariat veröffentlicht", "12.11.")]


def agent_dashboard():
    k = BRANCHES["kanzlei"]
    rows = "".join(f'<div class="adb__row" style="--slot:{i}"><span class="adb__ok">{_CHECK}</span><b>{e(t)}</b><time>{e(w)}</time></div>'
                   for i, (t, w) in enumerate(AGENT_DONE))
    nav = "".join(f'<span class="adb__nav{" is-on" if n == "Website" else ""}">{icon(ic)}{n}</span>'
                  for ic, n in [("layout", "Übersicht"), ("inbox", "Anfragen"), ("brief", "Mandate"), ("globe", "Website"), ("bot", "KI-Agent")])
    return f"""
<div class="st__frame">
  <div class="frame__bar"><i></i><i></i><i></i><span class="frame__url">{_LOCK}dashboard.kanzlei-lindqvist.de</span></div>
  <div class="adb" data-agentdash>
    <div class="adb__side"><span class="adb__brand">{LOGO}Dashboard</span>{nav}</div>
    <div class="adb__main">
      <div class="adb__h"><b>Website</b><span class="badge badge--ok"><span class="live"></span>KI-Agent aktiv</span></div>
      <div class="adb__task">
        <span class="adb__who">{icon('bot')} KI-Agent · vor 2 Minuten</span>
        <b>{e(k['task'][0])}</b>
        <p>{e(k['task'][1])}</p>
        <div class="adb__btns"><button type="button" class="adb__btn" data-adb-go>{_CHECK}<span>Veröffentlichen</span></button><span class="adb__hint">Ein Klick – und das Profil ist online.</span></div>
      </div>
      <div class="adb__done"><small>Zuletzt erledigt</small><div class="adb__list" data-adb-list>{rows}</div></div>
    </div>
  </div>
</div>"""
