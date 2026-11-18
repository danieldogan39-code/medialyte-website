"""Zwei kostenlose Angebote: Website-Check und kostenfreier Website-Entwurf.

- gratis_band(): ein kompakter Abschnitt auf der Startseite mit beiden Angeboten
- render_check(): die Seite /website-check/ – misst eine Website mit Google PageSpeed Insights
  (im Browser des Besuchers, nur nach Klick auf „Prüfen“). Ergebnisse werden nirgends gespeichert.
  Optionaler API-Schlüssel: GitHub-Secret PSI_API_KEY (Browser-Schlüssel, auf medialyte.de beschränkt).
"""
from build import e, icon
from parts import btn_book, btn_wa, closing, feats, page_hero, sh
import ratgeber_ui as rui

CHECK_PATH = "/website-check/"


def _check_form(ctx, big=False, auto=False):
    return (f'<form class="wcf{" wcf--big" if big else ""}" action="{ctx.u(CHECK_PATH)}" method="get" data-wcheck-form{" data-wcheck-page" if auto else ""} novalidate>'
            f'<label class="sr-only" for="wcf-url{"-p" if big else ""}">Adresse Ihrer Website</label>'
            f'<span class="wcf__ic" aria-hidden="true">{icon("globe")}</span>'
            f'<input id="wcf-url{"-p" if big else ""}" name="url" type="text" inputmode="url" autocomplete="url" spellcheck="false" placeholder="ihre-website.de" required>'
            f'<button class="btn btn--primary" type="submit">Prüfen</button></form>')


def gratis_band(ctx):
    """Startseite: zwei Angebote nebeneinander, bewusst knapp gehalten."""
    return f"""
<section class="section" id="kostenlos">
  <div class="wrap">
    {sh('Zwei Dinge, <span class="quiet">die Sie nichts kosten.</span>', 'Sehen Sie, wo Ihre Website steht – und wie Ihre neue aussehen wird, bevor sie gebaut wird.', split=True)}
    <div class="gratis">
      <article class="gcard" data-reveal style="--rd:0">
        <span class="ic ic--ads">{icon("zap")}</span>
        <h3>Website-Check</h3>
        <p>Ladezeit, Handy, Google-Grundlagen und Barrierefreiheit: In unter einer Minute sehen Sie, wie Ihre Website abschneidet. Ohne Anmeldung.</p>
        {_check_form(ctx)}
      </article>
      <article class="gcard" data-reveal style="--rd:1">
        <span class="ic ic--web">{icon("layout")}</span>
        <h3>Kostenfreier Website-Entwurf</h3>
        <p>Bevor wir bauen, sehen Sie Ihre neue Website: Wir gestalten einen Entwurf, der zu Ihrem Betrieb und Ihren Kunden passt – ohne Extrakosten.</p>
        <p class="gcard__fine">Der Entwurf entsteht nach Ihrer Auftragsbestätigung. Erstgespräch kostenfrei, Angebot innerhalb von 48 Stunden.</p>
        <div class="gcard__act">{btn_book(ctx, "Erstgespräch buchen", "web-neu")}</div>
      </article>
    </div>
  </div>
</section>"""


def render_check(ctx):
    vis = rui.hero_cover("/ratgeber/website-ladezeit-core-web-vitals/", {"thema": "gefunden"})
    out = page_hero(ctx, [("Start", "/"), ("Website-Check", "")],
                    'Website-Check: <span class="quiet">Wo steht Ihre Website?</span>',
                    "Geben Sie Ihre Adresse ein. Wir messen Ladezeit, Darstellung auf dem Handy, Google-Grundlagen und Barrierefreiheit – kostenlos, ohne Anmeldung, in unter einer Minute.",
                    _check_form(ctx, big=True, auto=True)
                    + '<p class="wcf__note">Gemessen mit Google PageSpeed Insights in der Handy-Ansicht. Wir speichern weder Ihre Adresse noch das Ergebnis.</p>', vis)
    out += f"""
<section class="section section--flush" id="ergebnis" data-wcheck hidden aria-live="polite">
  <div class="wrap">
    <div class="wcr" data-wcheck-state="idle">
      <div class="wcr__load" data-wc-load>
        <span class="wcr__spin" aria-hidden="true"></span>
        <p><b data-wc-step>Ihre Website wird geladen …</b><br><span class="quiet">Das dauert meist 20 bis 40 Sekunden.</span></p>
      </div>
      <div class="wcr__err" data-wc-err hidden>
        <h2 class="h3" data-wc-errt>Die Prüfung hat nicht geklappt.</h2>
        <p data-wc-errp></p>
        <div class="wcr__act">{btn_book(ctx, "Persönlich prüfen lassen", "web-besser")}{btn_wa(ctx)}</div>
      </div>
      <div class="wcr__done" data-wc-done hidden>
        <div class="wcr__head"><p class="wcr__k">Ergebnis für <b data-wc-host></b></p><h2 class="h3" data-wc-verdict></h2></div>
        <ul class="wcr__scores" data-wc-scores></ul>
        <div class="wcr__grid">
          <div class="wcr__box"><h3>Ladezeit und Stabilität</h3><p class="wcr__src" data-wc-src></p><ul class="wcr__vit" data-wc-vitals></ul></div>
          <div class="wcr__box"><h3>Grundlagen</h3><ul class="wcr__basics" data-wc-basics></ul></div>
        </div>
        <div class="wcr__box wcr__box--wide" data-wc-findbox><h3>Das bremst Ihre Website am meisten</h3><ol class="wcr__find" data-wc-find></ol></div>
        <div class="wcr__cta">
          <div><h3>Was bedeutet das für Ihre Anfragen?</h3><p>Zahlen sind der Anfang. Im kostenfreien Erstgespräch zeigen wir Ihnen, was sich bei Ihrer Website am meisten lohnt – ehrlich und ohne Fachchinesisch.</p></div>
          <div class="wcr__act"><a class="btn btn--primary" data-wc-book href="{ctx.u("/termin/?anliegen=web-besser")}">Auswertung besprechen</a>{btn_wa(ctx)}</div>
        </div>
      </div>
    </div>
    <noscript><p class="wcr__nojs">Für den Website-Check wird JavaScript benötigt. Gern prüfen wir Ihre Website auch persönlich – schreiben Sie uns einfach per WhatsApp.</p></noscript>
  </div>
</section>"""
    out += (f'<section class="section"><div class="wrap">{sh("Was wir prüfen", "Vier Bereiche, die entscheiden, ob aus Besuchern Anfragen werden.", split=True)}'
            + feats([("zap", "Ladezeit", "Wie schnell der wichtigste Inhalt erscheint und ob beim Laden etwas verrutscht."),
                     ("mobile", "Handy", "Ob Ihre Seite auf dem Smartphone gut lesbar und bedienbar ist."),
                     ("search", "Google-Grundlagen", "Seitentitel, Beschreibung, Verschlüsselung und weitere Punkte, die Google auswertet."),
                     ("eye", "Barrierefreiheit", "Kontraste, Beschriftungen und Alternativtexte – wichtig für alle Besucher.")], tone="ads")
            + "</div></section>")
    cards = "".join(rui.card(ctx, p, _art(p), i=i) for i, p in enumerate(
        ["/ratgeber/website-ladezeit-core-web-vitals/", "/ratgeber/barrierefreie-website-bfsg/", "/ratgeber/gute-website-wenig-anfragen/"]))
    out += f'<section class="section section--deep"><div class="wrap">{sh("Mehr dazu im Ratgeber")}<ul class="rgrid">{cards}</ul></div></section>'
    out += closing(ctx, "Lieber gleich persönlich?", "Das Erstgespräch ist kostenfrei.",
                   "Wir schauen uns Ihre Website gemeinsam an und sagen Ihnen ehrlich, was sich lohnt. Ihr Angebot erhalten Sie innerhalb von 48 Stunden.")
    return out


def _art(path):
    from seo_pages import ARTICLES  # spät importieren: seo_pages importiert dieses Modul
    return ARTICLES[path]
