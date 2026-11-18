"""Zwei kostenlose Angebote: Website-Check und kostenfreier Website-Entwurf.

- gratis_band(): ein Abschnitt auf der Startseite; der Website-Check steht darin bewusst im Vordergrund
- render_check(): die Seite /website-check/ (auch im Kopfmenü) – misst eine Website mit Google PageSpeed Insights
  im Browser des Besuchers, erst nach Klick auf „Website prüfen“. Ergebnisse werden nirgends gespeichert.
  API-Schlüssel: GitHub-Secret PSI_API_KEY (Browser-Schlüssel, auf medialyte.de beschränkt).
  Das Verhalten steckt in src/js/85-check.js, die Gestaltung in src/css/86-extras.css.
"""
from build import e, icon
from parts import btn_book, btn_wa, closing, faq_block, feats, process, sh
import ratgeber_ui as rui

CHECK_PATH = "/website-check/"


def _check_form(ctx, variant="", auto=False, label="Website prüfen"):
    uid = "wcf-" + (variant or "s")
    return (f'<form class="wcf{" wcf--" + variant if variant else ""}" action="{ctx.u(CHECK_PATH)}" method="get" data-wcheck-form'
            f'{" data-wcheck-page" if auto else ""} novalidate>'
            f'<label class="sr-only" for="{uid}">Adresse Ihrer Website</label>'
            f'<span class="wcf__ic" aria-hidden="true">{icon("globe")}</span><span class="wcf__pre" aria-hidden="true">https://</span>'
            f'<input id="{uid}" name="url" type="text" inputmode="url" autocomplete="url" spellcheck="false" autocapitalize="off" placeholder="ihre-website.de" required>'
            f'<button class="btn btn--primary" type="submit"><span>{label}</span>{icon("arrow")}</button></form>')


def _trust():
    items = [("clock", "Ergebnis in rund 30 Sekunden"), ("lock", "Ohne Anmeldung"), ("shield", "Wir speichern nichts")]
    return '<ul class="wtrust">' + "".join(f'<li>{icon(i)}<span>{t}</span></li>' for i, t in items) + "</ul>"


def _stage():
    """Gezeichnete Prüfstation: Browser und Handy mit Scanlinie und schwebenden Messwerten (rein dekorativ)."""
    sk = lambda w, cls="": f'<i class="sk{cls}" style="--w:{w}%"></i>'
    browser = (f'<div class="wst__browser"><div class="wst__bar"><i></i><i></i><i></i><span data-wst-host>ihre-website.de</span></div>'
               f'<div class="wst__page"><div class="wst__hero">{sk(62, " sk--h")}{sk(44)}{sk(30, " sk--btn")}</div>'
               f'<div class="wst__cols"><div>{sk(90)}{sk(70)}</div><div>{sk(80)}{sk(60)}</div><div>{sk(85)}{sk(50)}</div></div></div></div>')
    phone = (f'<div class="wst__phone"><div class="wst__notch"></div><div class="wst__screen">'
             f'<div class="wst__img"></div>{sk(80, " sk--h")}{sk(64)}{sk(72)}{sk(48, " sk--btn")}<span class="wst__beam"></span></div></div>')
    chips = [("zap", "Ladezeit", "c1"), ("eye", "Barrierefreiheit", "c2"), ("search", "Google", "c3"), ("shield", "Technik", "c4")]
    ch = "".join(f'<span class="wst__chip wst__chip--{c}">{icon(i)}{t}</span>' for i, t, c in chips)
    return f'<div class="wst" data-wst aria-hidden="true"><div class="wst__glow"></div>{browser}{phone}{ch}</div>'


def gratis_band(ctx):
    """Startseite: Website-Check groß, kostenfreier Entwurf daneben."""
    return f"""
<section class="section" id="kostenlos">
  <div class="wrap">
    {sh('Zwei Dinge, <span class="quiet">die Sie nichts kosten.</span>', 'Sehen Sie, wo Ihre Website heute steht – und wie Ihre neue aussehen wird, bevor sie gebaut wird.', split=True)}
    <div class="gratis">
      <article class="gcard gcard--check" data-reveal style="--rd:0">
        <div class="gcard__top"><span class="ic ic--ads">{icon("zap")}</span><span class="badge badge--ok">Kostenlos</span></div>
        <h3>Website-Check</h3>
        <p>Ladezeit, Handy, Google-Grundlagen und Barrierefreiheit – mit echten Messdaten von Google. Sie sehen sofort, wo Ihre Website Anfragen verschenkt.</p>
        {_check_form(ctx, "band")}
        {_trust()}
      </article>
      <article class="gcard" data-reveal style="--rd:1">
        <div class="gcard__top"><span class="ic ic--web">{icon("layout")}</span></div>
        <h3>Kostenfreier Website-Entwurf</h3>
        <p>Bevor wir bauen, sehen Sie Ihre neue Website: Wir gestalten einen Entwurf, der zu Ihrem Betrieb und Ihren Kunden passt – ohne Extrakosten.</p>
        <p class="gcard__fine">Der Entwurf entsteht nach Ihrer Auftragsbestätigung. Erstgespräch kostenfrei, Angebot innerhalb von 48 Stunden.</p>
        <div class="gcard__act">{btn_book(ctx, "Erstgespräch buchen", "web-neu", cls="btn--ghost")}</div>
      </article>
    </div>
  </div>
</section>"""


CHECK_FAQ = [
    ("Kostet der Website-Check etwas?", "<p>Nein. Der Check ist kostenlos und ohne Anmeldung. Sie können beliebig viele Websites prüfen – auch die Ihrer Mitbewerber.</p>"),
    ("Woher kommen die Werte?", "<p>Gemessen wird mit Google PageSpeed Insights, demselben Werkzeug, das Google Website-Betreibern empfiehlt. Liegen für Ihre Seite genug Daten echter Besuche vor, zeigen wir zusätzlich diese Werte aus den letzten 28 Tagen.</p>"),
    ("Warum unterscheiden sich die Werte von Prüfung zu Prüfung?", "<p>Jede Testmessung lädt Ihre Seite neu – Serverauslastung, Netz und Werbung von Drittanbietern schwanken. Kleine Unterschiede sind normal. Aussagekräftig ist die Größenordnung und ob ein Wert im grünen, gelben oder roten Bereich liegt.</p>"),
    ("Was passiert mit meinen Daten?", "<p>Die Adresse wird nur zur Messung an Google übertragen. Wir speichern weder die Adresse noch das Ergebnis. Mehr dazu in unserer Datenschutzerklärung.</p>"),
]


def render_check(ctx):
    out = f"""
<section class="wch hero">
  <div class="hero__bg" aria-hidden="true"><span class="hero__glow"></span><span class="hero__grid"></span></div>
  <div class="wrap">
    <nav aria-label="Brotkrümelnavigation" data-intro style="--i:0"><ol class="crumbs"><li><a href="{ctx.u('/')}">Start</a></li><li aria-current="page">Website-Check</li></ol></nav>
    <div class="wch__grid">
      <div class="wch__copy">
        <p class="wch__pill" data-intro style="--i:0"><span class="wch__dot" aria-hidden="true"></span>Kostenlos, mit Messdaten von Google</p>
        <h1 data-intro style="--i:1">Wie gut ist Ihre Website <span class="quiet">wirklich?</span></h1>
        <p class="lead" data-intro style="--i:2">Ladezeit, Darstellung auf dem Handy, Google-Grundlagen und Barrierefreiheit: Geben Sie Ihre Adresse ein und sehen Sie in rund 30 Sekunden, wo Ihre Website Anfragen verschenkt.</p>
        <div class="wch__form" data-intro style="--i:3">{_check_form(ctx, "hero", auto=True)}{_trust()}</div>
      </div>
      <div class="wch__visual" data-intro style="--i:4">{_stage()}</div>
    </div>
  </div>
</section>
<section class="section section--flush wres" id="ergebnis" data-wcheck hidden>
  <div class="wrap">
    <div class="wrun" data-wc-load aria-live="polite">
      <div class="wrun__head"><span class="wrun__spin" aria-hidden="true"></span><div><p class="wrun__k">Prüfung läuft – alle Bereiche werden gleichzeitig gemessen</p><h2 class="h3" data-wc-runhost>Ihre Website</h2></div><span class="wrun__t tnum" data-wc-timer>0 s</span></div>
      <div class="wrun__bar" aria-hidden="true"><i data-wc-prog></i></div>
      <ol class="wrun__steps" data-wc-steps>
        <li data-part="performance">Ladezeit und Stabilität messen</li><li data-part="accessibility">Barrierefreiheit prüfen</li><li data-part="best-practices">Technik und Sicherheit prüfen</li><li data-part="seo">Google-Grundlagen prüfen</li><li data-final>Ergebnis zusammenstellen</li>
      </ol>
    </div>
    <div class="werr" data-wc-err hidden role="alert">
      <span class="werr__ic" aria-hidden="true">{icon("x")}</span>
      <div><h2 class="h3" data-wc-errt>Die Prüfung hat nicht geklappt.</h2><p data-wc-errp></p>
        <div class="wact">{btn_book(ctx, "Persönlich prüfen lassen", "web-besser")}{btn_wa(ctx)}</div>
        <p class="werr__alt">Oder direkt bei Google messen: <a data-wc-google href="https://pagespeed.web.dev/" target="_blank" rel="noopener">PageSpeed Insights öffnen {icon("out")}</a></p></div>
    </div>
    <div class="wdone" data-wc-done hidden>
      <div class="wbar">
        <p class="wbar__host">{icon("globe")}<span>Ergebnis für <b data-wc-host></b></span></p>
        <div class="chips wbar__view" role="group" aria-label="Ansicht">
          <button class="chip" type="button" data-wc-view="mobile" aria-pressed="true">{icon("mobile")} Handy</button>
          <button class="chip" type="button" data-wc-view="desktop" aria-pressed="false">{icon("monitor")} Computer</button>
        </div>
        <div class="wbar__act"><button class="btn btn--ghost btn--sm" type="button" data-wc-copy>{icon("send")} <span>Link kopieren</span></button><button class="btn btn--ghost btn--sm" type="button" data-wc-again>{icon("refresh")} Andere Website</button></div>
      </div>
      <div class="wsum">
        <div class="wsum__main">
          <div class="wgrade" data-wc-grade><svg viewBox="0 0 120 120" aria-hidden="true"><circle class="wgrade__bg" cx="60" cy="60" r="52"/><circle class="wgrade__fg" cx="60" cy="60" r="52"/></svg><div><b class="tnum" data-wc-total>–</b><span>von 100</span></div></div>
          <div class="wsum__txt"><p class="wsum__label" data-wc-label></p><h2 class="h3" data-wc-verdict></h2><p data-wc-explain></p><p class="wsum__src" data-wc-src></p></div>
        </div>
        <figure class="wshot" data-wc-shotbox><div class="wshot__frame" data-wc-frame><img data-wc-shot alt="So sieht die geprüfte Website in der Messung aus" decoding="async"></div><figcaption data-wc-shotcap>So sah Ihre Seite in der Messung aus</figcaption></figure>
      </div>
      <ul class="wcats" data-wc-cats></ul>
      <div class="wpanel" data-wc-filmbox><div class="wpanel__h"><h3>So baut sich Ihre Seite auf</h3><p>Momentaufnahmen während des Ladens</p></div><ol class="wfilm" data-wc-film></ol></div>
      <div class="wgrid2">
        <div class="wpanel"><div class="wpanel__h"><h3>Ladezeit und Stabilität</h3><p data-wc-vsrc></p></div><ul class="wmet" data-wc-metrics></ul></div>
        <div class="wpanel"><div class="wpanel__h"><h3>Grundlagen</h3><p>Was jede Website erfüllen sollte</p></div><ul class="wbasic" data-wc-basics></ul></div>
      </div>
      <div class="wpanel" data-wc-findbox><div class="wpanel__h"><h3 data-wc-findt>Das bremst Ihre Website am meisten</h3><p>Nach Wirkung sortiert – zum Aufklappen</p></div><ol class="wfind" data-wc-find></ol></div>
      <div class="wcta">
        <div class="wcta__txt"><h3>Was bedeutet das für Ihre Anfragen?</h3><p>Zahlen sind der Anfang. Im kostenfreien Erstgespräch zeigen wir Ihnen, was sich bei Ihrer Website am meisten lohnt – ehrlich und ohne Fachchinesisch.</p>
          <ol class="wcta__steps"><li><b>Erstgespräch</b><span>kostenfrei, 30 Minuten</span></li><li><b>Angebot</b><span>innerhalb von 48 Stunden</span></li><li><b>Entwurf</b><span>kostenfrei nach Auftrag</span></li></ol></div>
        <div class="wact wact--col"><a class="btn btn--primary btn--lg" data-wc-book href="{ctx.u('/termin/?anliegen=web-besser')}">Auswertung besprechen</a>{btn_wa(ctx, cls="btn--ghost btn--lg")}</div>
      </div>
    </div>
    <noscript><p class="wnojs">Für den Website-Check wird JavaScript benötigt. Gern prüfen wir Ihre Website auch persönlich – schreiben Sie uns einfach per WhatsApp.</p></noscript>
  </div>
</section>"""
    out += (f'<section class="section"><div class="wrap">{sh("Was wir prüfen", "Vier Bereiche, die entscheiden, ob aus Besuchern Anfragen werden.", split=True)}'
            + feats([("zap", "Ladezeit", "Wie schnell der wichtigste Inhalt erscheint, wie schnell die Seite reagiert und ob beim Laden etwas verrutscht."),
                     ("mobile", "Handy", "Ob Ihre Seite auf dem Smartphone gut lesbar und bedienbar ist – dort, wo die meisten Ihrer Kunden suchen."),
                     ("search", "Google-Grundlagen", "Seitentitel, Beschreibung, Verschlüsselung, Indexierung und weitere Punkte, die Google auswertet."),
                     ("eye", "Barrierefreiheit", "Kontraste, Beschriftungen und Alternativtexte – wichtig für alle Besucher und für Shops und Buchungen Pflicht.")], cols=2, tone="ads")
            + "</div></section>")
    out += (f'<section class="section section--deep"><div class="wrap">{sh("Vom Check zur besseren Website", "Der Check zeigt, wo es hakt. Wenn Sie möchten, machen wir daraus einen Plan.", split=True)}'
            + process([("Website prüfen", "In rund 30 Sekunden sehen Sie, wo Ihre Seite steht – kostenlos und ohne Anmeldung.", []),
                       ("Erstgespräch", "Wir gehen das Ergebnis gemeinsam durch und sagen ehrlich, was sich lohnt. Ihr Angebot kommt innerhalb von 48 Stunden.", []),
                       ("Kostenfreier Entwurf", "Nach Ihrer Auftragsbestätigung gestalten wir zuerst einen Entwurf – Sie sehen die neue Website, bevor sie gebaut wird.", [])], "proc--n")
            + "</div></section>")
    out += f'<section class="section"><div class="wrap">{faq_block(ctx, CHECK_FAQ, "Fragen zum Website-Check")}</div></section>'
    cards = "".join(rui.card(ctx, p, _art(p), i=i) for i, p in enumerate(
        ["/ratgeber/website-ladezeit-core-web-vitals/", "/ratgeber/barrierefreie-website-bfsg/", "/ratgeber/gute-website-wenig-anfragen/"]))
    out += f'<section class="section section--deep"><div class="wrap">{sh("Mehr dazu im Ratgeber")}<ul class="rgrid">{cards}</ul></div></section>'
    out += closing(ctx, "Lieber gleich persönlich?", "Das Erstgespräch ist kostenfrei.",
                   "Wir schauen uns Ihre Website gemeinsam an und sagen Ihnen ehrlich, was sich lohnt. Ihr Angebot erhalten Sie innerhalb von 48 Stunden.")
    return out


def _art(path):
    from seo_pages import ARTICLES  # spät importieren: seo_pages importiert dieses Modul
    return ARTICLES[path]
