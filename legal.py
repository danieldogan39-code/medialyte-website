"""Rechtstexte: Datenschutzerklärung und AGB.

Die Datenschutzerklärung beschreibt, was diese Website tatsächlich tut (Stand des Codes): kein Tracking, keine Cookies,
keine eingebetteten Fremdinhalte; Daten nur über Buchungsformular, E-Mail, Telefon und WhatsApp.
Wer etwas Neues einbaut (Analyse, Karten, Videos von YouTube, Chat …), muss diesen Text ergänzen.
Die AGB sind die AGB von Medialyte (Stand 01.01.2026), mit dem aktuellen Namen „Medialyte – Marketing & Management“.
"""
from build import SITE, e


def _toc(items):
    return '<nav class="prose__toc" aria-label="Inhalt"><ol>' + "".join(f'<li><a href="#{i}">{t}</a></li>' for i, t in items) + "</ol></nav>"


def _num(items):
    return [(i, f"{k}. {t}") for k, (i, t) in enumerate(items, 1)]


def datenschutz(ctx):
    S = SITE
    sections = [
        ("ueberblick", "Auf einen Blick"),
        ("verantwortlich", "Verantwortlicher"),
        ("hosting", "Hosting und Server-Protokolle"),
        ("buchung", "Erstgespräch buchen"),
        ("kontakt", "Kontakt per E-Mail, Telefon oder WhatsApp"),
        ("speicher", "Cookies und Speicher im Browser"),
        ("links", "Links zu sozialen Netzwerken und anderen Websites"),
        ("rechte", "Ihre Rechte"),
        ("aenderungen", "Änderungen dieser Erklärung"),
    ]
    return f"""
<section class="section section--flush"><div class="wrap"><div class="prose">
  <p class="prose__meta">Stand: Oktober 2026</p>
  {_toc(_num(sections))}

  <h2 id="ueberblick">1. Auf einen Blick</h2>
  <p>Auf dieser Website erheben wir so wenige Daten wie möglich. Es gibt keine Analyse- oder Tracking-Werkzeuge, keine Werbe-Cookies und keine eingebetteten Inhalte anderer Anbieter. Schriften, Bilder und Filme liegen auf unserem eigenen Server.</p>
  <p>Personenbezogene Daten verarbeiten wir nur in zwei Fällen: wenn Ihr Browser die Seite vom Server abruft (technisch notwendig) und wenn Sie uns von sich aus schreiben, anrufen oder ein Erstgespräch buchen.</p>

  <h2 id="verantwortlich">2. Verantwortlicher</h2>
  <p>Verantwortlich für die Datenverarbeitung auf dieser Website ist:</p>
  <p>{e(S['legal'])}<br>Inhaber und Anschrift: siehe <a href="{ctx.u('/impressum/')}">Impressum</a><br>
  Telefon: <a href="tel:{S['phone_intl']}">{e(S['phone'])}</a><br>E-Mail: <a href="mailto:{S['email']}">{e(S['email'])}</a></p>
  <p>Wir sind gesetzlich nicht verpflichtet, einen Datenschutzbeauftragten zu benennen. Bei Fragen zum Datenschutz schreiben Sie uns direkt an die oben genannte E-Mail-Adresse.</p>

  <h2 id="hosting">3. Hosting und Server-Protokolle</h2>
  <p>Diese Website liegt bei der IONOS SE, Elgendorfer Str. 57, 56410 Montabaur. Mit IONOS haben wir einen Vertrag zur Auftragsverarbeitung nach Art. 28 DSGVO geschlossen. Die Daten werden in Rechenzentren in der Europäischen Union verarbeitet.</p>
  <p>Bei jedem Aufruf einer Seite speichert der Server automatisch Informationen, die Ihr Browser übermittelt (Server-Protokolle):</p>
  <ul>
    <li>IP-Adresse des anfragenden Geräts</li>
    <li>Datum und Uhrzeit des Abrufs</li>
    <li>aufgerufene Seite oder Datei und übertragene Datenmenge</li>
    <li>Website, von der aus Sie zu uns gekommen sind (Referrer)</li>
    <li>verwendeter Browser und Betriebssystem</li>
  </ul>
  <p>Diese Daten brauchen wir, um die Website sicher und fehlerfrei auszuliefern und Angriffe zu erkennen. Rechtsgrundlage ist unser berechtigtes Interesse an einem sicheren und stabilen Betrieb (Art. 6 Abs. 1 lit. f DSGVO). Wir werten die Protokolle nicht für Statistiken oder Werbung aus und führen sie nicht mit anderen Daten zusammen. Sie werden nach kurzer Zeit automatisch gelöscht.</p>
  <p>Die Übertragung zwischen Ihrem Browser und unserem Server ist verschlüsselt (TLS). Das erkennen Sie am Schloss-Symbol und an „https://“ in der Adresszeile.</p>

  <h2 id="buchung">4. Erstgespräch buchen</h2>
  <h3>Welche Daten wir erheben</h3>
  <p>Wenn Sie über unser Formular ein Erstgespräch buchen oder einen Rückruf anfordern, verarbeiten wir die Angaben, die Sie eintragen:</p>
  <ul>
    <li>Ihr Anliegen, Ihr Unternehmen, Branche, Website, Ort und Unternehmensgröße</li>
    <li>die Gesprächsart (Video-Call, Telefon oder vor Ort) und Ihren Wunschtermin bzw. das Zeitfenster für den Rückruf</li>
    <li>Ihren Namen, Ihre E-Mail-Adresse und, falls angegeben, Ihre Telefonnummer sowie ob Sie eine Bestätigung per WhatsApp wünschen</li>
    <li>Ihre Nachricht, falls Sie eine schreiben</li>
  </ul>
  <p>Außerdem speichern wir, von welcher unserer Seiten Sie das Formular abgeschickt haben, die Website, von der Sie zu uns gekommen sind, und Kampagnenkennungen aus der Adresszeile (zum Beispiel „utm_source“ oder „gclid“), falls vorhanden. So sehen wir, über welchen Weg Anfragen zu uns kommen.</p>
  <h3>Wofür und auf welcher Grundlage</h3>
  <p>Wir nutzen die Angaben, um den Termin zu vereinbaren, das Gespräch vorzubereiten und Ihnen ein Angebot zu erstellen. Rechtsgrundlagen sind die Durchführung vorvertraglicher Maßnahmen auf Ihre Anfrage (Art. 6 Abs. 1 lit. b DSGVO) und Ihre Einwilligung, die Sie im Formular erteilen (Art. 6 Abs. 1 lit. a DSGVO). Die Einwilligung können Sie jederzeit mit Wirkung für die Zukunft widerrufen, etwa per E-Mail.</p>
  <h3>Was mit den Daten passiert</h3>
  <ul>
    <li>Die Anfrage wird in einem geschützten Bereich auf unserem Server bei IONOS gespeichert, der von außen nicht abrufbar ist.</li>
    <li>Wir erhalten die Anfrage per E-Mail. Sie bekommen eine Bestätigung per E-Mail, bei einem Termin mit einem Kalendereintrag im Anhang. Die E-Mails werden über die Server von IONOS versendet.</li>
    <li>Wir übertragen die Anfrage in unser eigenes Kundenmanagement-System, in dem wir Anfragen und Termine bearbeiten.</li>
  </ul>
  <p>Um freie Termine anzuzeigen, fragt das Formular beim Laden die belegten Zeiten von unserem Server ab. Dabei werden keine Angaben über Sie übertragen.</p>
  <h3>Schutz vor Missbrauch</h3>
  <p>Damit das Formular nicht massenhaft von Programmen genutzt wird, begrenzen wir die Zahl der Anfragen pro Anschluss und Stunde. Dafür speichern wir Ihre IP-Adresse nicht im Klartext, sondern nur als nicht umkehrbare Prüfsumme, und löschen sie nach einer Stunde. Rechtsgrundlage ist unser berechtigtes Interesse an einem funktionierenden, missbrauchsfreien Formular (Art. 6 Abs. 1 lit. f DSGVO).</p>
  <h3>Wie lange wir die Daten speichern</h3>
  <p>Kommt kein Auftrag zustande, löschen wir Ihre Anfrage, sobald sie erledigt ist, spätestens zwölf Monate nach unserem letzten Kontakt. Wird aus der Anfrage ein Auftrag, bewahren wir die Unterlagen so lange auf, wie es die gesetzlichen Aufbewahrungsfristen verlangen (bis zu zehn Jahre nach § 147 AO und § 257 HGB).</p>
  <p>Die Angabe Ihrer Daten ist freiwillig. Ohne Name, E-Mail-Adresse und Wunschtermin können wir den Termin allerdings nicht vereinbaren.</p>

  <h2 id="kontakt">5. Kontakt per E-Mail, Telefon oder WhatsApp</h2>
  <p>Wenn Sie uns per E-Mail oder Telefon kontaktieren, verarbeiten wir Ihre Angaben, um Ihr Anliegen zu bearbeiten. Rechtsgrundlage ist Art. 6 Abs. 1 lit. b DSGVO, wenn es um einen Auftrag oder ein Angebot geht, sonst unser berechtigtes Interesse, Anfragen zu beantworten (Art. 6 Abs. 1 lit. f DSGVO). Für die Speicherdauer gilt dasselbe wie beim Buchungsformular.</p>
  <p>Unsere WhatsApp-Links öffnen WhatsApp auf Ihrem Gerät oder im Browser. Erst wenn Sie uns schreiben, findet ein Austausch statt. Anbieter ist die WhatsApp Ireland Limited, Merrion Road, Dublin 4, D04 X2K5, Irland. Die Inhalte der Nachrichten sind Ende-zu-Ende-verschlüsselt. Meta, der Mutterkonzern von WhatsApp, erhält jedoch Metadaten wie Ihre Telefonnummer und den Zeitpunkt der Nachricht und kann diese auch in die USA übertragen. Meta ist nach dem EU-US Data Privacy Framework zertifiziert. Wir nutzen WhatsApp für die Kommunikation mit Kunden und Interessenten, weil viele Betriebe so am schnellsten erreichbar sind (Art. 6 Abs. 1 lit. b und f DSGVO). Wenn Sie das nicht möchten, erreichen Sie uns ebenso per E-Mail oder Telefon. Näheres finden Sie in der Datenschutzerklärung von WhatsApp.</p>

  <h2 id="speicher">6. Cookies und Speicher im Browser</h2>
  <p>Diese Website setzt keine Cookies. Deshalb sehen Sie auch kein Cookie-Banner.</p>
  <p>Zwei kleine Einträge legen wir im Sitzungsspeicher Ihres Browsers (sessionStorage) ab: einen Hinweis, damit eine neue Seite nach einem Klick oben beginnt, und Ihre Eingaben im Buchungsformular, damit beim versehentlichen Neuladen nichts verloren geht. Beide bleiben auf Ihrem Gerät, werden nicht an uns übertragen und beim Schließen des Tabs automatisch gelöscht. Sie sind für die von Ihnen gewünschte Funktion unbedingt erforderlich (§ 25 Abs. 2 Nr. 2 TDDDG).</p>

  <h2 id="links">7. Links zu sozialen Netzwerken und anderen Websites</h2>
  <p>Auf unsere Profile bei Instagram, LinkedIn und YouTube verweisen wir mit einfachen Links. Es sind keine Plugins oder Inhalte dieser Netzwerke eingebunden. Daten an die Anbieter fließen erst, wenn Sie einen Link anklicken. Dann gelten die Datenschutzbestimmungen des jeweiligen Anbieters: Meta Platforms Ireland Limited (Instagram), LinkedIn Ireland Unlimited Company (LinkedIn) und Google Ireland Limited (YouTube).</p>
  <p>Für die Statistiken, die Meta uns zu unserem Instagram-Profil bereitstellt, sind wir gemeinsam mit Meta verantwortlich (Art. 26 DSGVO). Meta hat sich dabei verpflichtet, die Hauptverantwortung zu übernehmen und Ihre Rechte zu erfüllen.</p>
  <p>Bei unseren Referenzen verlinken wir auf die Websites unserer Kunden. Auch hier werden erst beim Anklicken Daten an die jeweilige Website übertragen. Die Vorschaubilder auf unserer Seite liegen auf unserem eigenen Server.</p>

  <h2 id="rechte">8. Ihre Rechte</h2>
  <p>Sie haben das Recht,</p>
  <ul>
    <li>Auskunft über Ihre bei uns gespeicherten Daten zu erhalten (Art. 15 DSGVO),</li>
    <li>unrichtige Daten berichtigen zu lassen (Art. 16 DSGVO),</li>
    <li>Ihre Daten löschen zu lassen (Art. 17 DSGVO),</li>
    <li>die Verarbeitung einschränken zu lassen (Art. 18 DSGVO),</li>
    <li>Ihre Daten in einem gängigen Format zu erhalten (Art. 20 DSGVO),</li>
    <li>einer Verarbeitung auf Grundlage unseres berechtigten Interesses zu widersprechen (Art. 21 DSGVO) und</li>
    <li>eine erteilte Einwilligung jederzeit zu widerrufen (Art. 7 Abs. 3 DSGVO).</li>
  </ul>
  <p>Eine kurze E-Mail an <a href="mailto:{S['email']}">{e(S['email'])}</a> genügt. Eine automatisierte Entscheidungsfindung oder ein Profiling findet nicht statt.</p>
  <p>Außerdem können Sie sich bei einer Datenschutz-Aufsichtsbehörde beschweren (Art. 77 DSGVO). Für uns zuständig ist der Hamburgische Beauftragte für Datenschutz und Informationsfreiheit, Ludwig-Erhard-Str. 22, 20459 Hamburg, <a href="mailto:mailbox@datenschutz.hamburg.de">mailbox@datenschutz.hamburg.de</a>.</p>

  <h2 id="aenderungen">9. Änderungen dieser Erklärung</h2>
  <p>Wenn wir die Website um neue Funktionen erweitern oder sich die Rechtslage ändert, passen wir diese Datenschutzerklärung an. Es gilt die jeweils hier veröffentlichte Fassung.</p>
</div></div></section>"""


AGB = [
    ("Geltungsbereich und Zielgruppe", [
        "Die nachfolgenden Allgemeinen Geschäftsbedingungen gelten für alle Verträge, Lieferungen und sonstigen Leistungen zwischen Medialyte – Marketing &amp; Management (nachfolgend „Agentur“ genannt) und ihren Auftraggebern (nachfolgend „Kunde“ genannt).",
        "Das Angebot der Agentur richtet sich ausschließlich an Unternehmer (§ 14 BGB), juristische Personen des öffentlichen Rechts oder öffentlich-rechtliche Sondervermögen. Ein Vertragsschluss mit Verbrauchern (§ 13 BGB) ist ausgeschlossen.",
        "Entgegenstehende oder von diesen AGB abweichende Bedingungen des Kunden werden nicht anerkannt, es sei denn, die Agentur stimmt ihrer Geltung ausdrücklich schriftlich zu.",
    ]),
    ("Vertragsschluss", [
        "Angebote der Agentur sind freibleibend und unverbindlich, sofern sie nicht ausdrücklich als verbindlich gekennzeichnet sind.",
        "Der Vertrag kommt zustande, indem die Agentur dem Kunden einen Vertrag zusendet und der Kunde diesen unterschrieben (digital oder postalisch) an die Agentur zurücksendet.",
        "Nachträgliche Änderungen oder Ergänzungen des Auftrags bedürfen der Textform (z. B. E-Mail).",
    ]),
    ("Leistungsumfang", [
        "Die konkreten Leistungen ergeben sich aus dem individuellen Vertrag oder der Auftragsbestätigung. Der Fokus der Agentur liegt auf individuellen Lösungen zur Verbesserung, Verwaltung und Vermehrung von Kundenbeziehungen (z. B. Websites, CRM-Integrationen, Funnels, Automatisierungen).",
        "<b>Drittanbieter und Werbeanzeigen:</b> Soweit die Agentur Werbeanzeigen (z. B. Meta Ads, Google Ads) betreut, schuldet die Agentur die reine Betreuungsleistung (Setup, Optimierung). Das Werbebudget ist nicht im Honorar enthalten und wird vom Kunden direkt an den Plattformbetreiber gezahlt.",
        "Die Agentur ist berechtigt, sich zur Erfüllung der Leistungen qualifizierter Dritter (Subunternehmer) zu bedienen.",
    ]),
    ("Mitwirkungspflichten des Kunden", [
        "Der Kunde ist verpflichtet, der Agentur alle für die Durchführung des Projekts benötigten Daten, Zugänge, Informationen und Inhalte (Texte, Bilder, Logos) zeitnah und in digital verwertbarer Form zur Verfügung zu stellen.",
        "Kommt der Kunde seiner Mitwirkungspflicht nicht nach, ist die Agentur berechtigt, dem Kunden die Erstellung der fehlenden Inhalte (z. B. Copywriting, Bildersuche) gesondert anzubieten und nach Annahme gegen Aufpreis in Rechnung zu stellen.",
        "Verzögerungen, die durch fehlende Mitwirkung des Kunden entstehen, gehen nicht zu Lasten der Agentur und können vereinbarte Zeitpläne verschieben.",
    ]),
    ("Abnahme und Gewährleistung (Projektgeschäft)", [
        "Nach Fertigstellung von Werkleistungen (z. B. Website, Setup einer Softwarelösung) legt die Agentur dem Kunden das Ergebnis zur Abnahme vor oder schaltet es online.",
        "Der Kunde hat 10 Tage Zeit, das Ergebnis zu prüfen.",
        "<b>Abnahmefiktion:</b> Meldet der Kunde innerhalb dieser 10-Tages-Frist keine wesentlichen Mängel in Textform, gilt das Werk als abgenommen. Ebenso gilt das Werk als abgenommen, sobald der Kunde es operativ nutzt (z. B. Live-Schaltung der Website, Nutzung des CRM-Systems für echte Kundendaten).",
        "Unwesentliche Mängel berechtigen nicht zur Verweigerung der Abnahme.",
    ]),
    ("Vergütung und Zahlungsbedingungen", [
        "Es gelten die vertraglich vereinbarten Preise. Alle Preise verstehen sich in Euro zuzüglich der gesetzlichen Umsatzsteuer.",
        "<b>Einmalige Leistungen:</b> Für einmalige Projekterstellungen (Festpreis) ist die Vergütung nach Rechnungsstellung sofort fällig, sofern im Vertrag kein Zahlungsplan (z. B. 50 % Anzahlung / 50 % Schlussrate) vereinbart wurde.",
        "<b>Laufende Betreuung (Abo-Modell):</b> Vergütungen für laufende Wartungs-, Hosting- oder Betreuungsverträge sind, sofern nicht anders vereinbart, monatlich im Voraus fällig.",
    ]),
    ("Laufzeit und Kündigung (Dauerschuldverhältnisse)", [
        "Für Verträge über laufende Leistungen (z. B. Wartungspakete, Social-Media-Betreuung) gilt die im Vertrag vereinbarte Mindestlaufzeit.",
        "Das Recht zur außerordentlichen Kündigung aus wichtigem Grund bleibt unberührt. Ein wichtiger Grund liegt für die Agentur insbesondere vor, wenn der Kunde mit fälligen Zahlungen mehr als 4 Wochen in Verzug ist.",
    ]),
    ("Nutzungsrechte und „Buy-out“", [
        "<b>Einfaches Nutzungsrecht (Standard):</b> Mit vollständiger Zahlung der vereinbarten Vergütung erhält der Kunde an den von der Agentur erstellten Werken (Websites, Grafiken, Texte, Automations-Setups) ein einfaches, nicht ausschließliches Nutzungsrecht für den vertraglich vereinbarten Zweck. Das Urheberrecht und die weitergehenden Verwertungsrechte verbleiben bei der Agentur.",
        "<b>Buy-out (ausschließliches Nutzungsrecht):</b> Wünscht der Kunde das ausschließliche, uneingeschränkte Nutzungsrecht (z. B. um sich aus einem Abo-Modell herauszulösen oder die Software bzw. das Design unabhängig von der Agentur weiterzuentwickeln oder zu veräußern), kann dieses gegen eine gesonderte „Buy-out“-Gebühr erworben werden. Die Höhe der Gebühr wird individuell vereinbart. Erst mit Zahlung dieser Gebühr gehen die ausschließlichen Rechte auf den Kunden über.",
        "<b>Referenznutzung:</b> Die Agentur ist berechtigt, die für den Kunden erstellten Leistungen sowie dessen Namen und Logo als Referenz auf der eigenen Website und in Präsentationen zu verwenden.",
    ]),
    ("Haftung", [
        "Die Agentur haftet unbeschränkt bei Vorsatz und grober Fahrlässigkeit.",
        "Bei leichter Fahrlässigkeit haftet die Agentur nur bei Verletzung vertragswesentlicher Pflichten (Kardinalpflichten), deren Erfüllung die ordnungsgemäße Durchführung des Vertrages erst ermöglicht. In diesem Fall ist die Haftung auf den typischerweise vorhersehbaren Schaden begrenzt.",
        "Für die wettbewerbs-, marken- und urheberrechtliche Zulässigkeit und Eintragungsfähigkeit der Arbeiten haftet die Agentur nicht. Der Kunde ist selbst dafür verantwortlich, die Inhalte rechtlich (z. B. Impressum, Datenschutzerklärung) prüfen zu lassen.",
        "Die Agentur haftet nicht für Datenverluste oder Fehler, die durch Updates von Drittanbieter-Plattformen (z. B. WordPress, CRM-Tools, Social-Media-Plattformen) entstehen, sofern diese nicht grob fahrlässig durch die Agentur verursacht wurden.",
    ]),
    ("Schlussbestimmungen", [
        "Es gilt das Recht der Bundesrepublik Deutschland.",
        "Erfüllungsort und ausschließlicher Gerichtsstand für alle Streitigkeiten aus diesem Vertrag ist der Geschäftssitz der Agentur (Hamburg), sofern sich aus der Auftragsbestätigung nichts anderes ergibt.",
        "Sollten einzelne Bestimmungen dieses Vertrages unwirksam sein oder werden, so berührt dies die Gültigkeit der übrigen Bestimmungen nicht.",
    ]),
]


def agb(ctx):
    body = "".join(f'<h2 id="p{i}">§ {i} {t}</h2>' + "".join(f"<p>{p}</p>" for p in ps) for i, (t, ps) in enumerate(AGB, 1))
    toc = _toc([(f"p{i}", f"§ {i} {t}") for i, (t, _) in enumerate(AGB, 1)])
    return f"""
<section class="section section--flush"><div class="wrap"><div class="prose">
  <p class="prose__meta">Stand: 01.01.2026</p>
  {toc}
  {body}
</div></div></section>"""
