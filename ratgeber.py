"""Ratgeber-Artikel, Teil 2 (Stand 18. November 2026).

Gleicher Aufbau wie ARTICLES in seo_pages.py, zusätzlich:
- "date"/"iso": Stand des Artikels (Anzeige und strukturierte Daten)
- "thema": Gruppe auf der Übersichtsseite (siehe THEMEN)
- "sources": Quellen als (Titel, Herausgeber/Stand, URL); erscheinen als eigener Abschnitt „Quellen“

Alle Zahlen, Fristen und Zitate stammen aus den angegebenen Quellen. Rechtliche Themen sind als
allgemeine Information formuliert, nicht als Rechtsberatung.
"""

THEMEN = [  # Schlüssel, Überschrift, Einleitung
    ("website", "Website planen und verbessern",
     "Kosten, Relaunch und Barrierefreiheit – und was zu tun ist, wenn eine gute Website trotzdem zu wenig bringt."),
    ("gefunden", "Bei Google gefunden werden",
     "Mehr Sichtbarkeit in Ihrer Region: mit einem gepflegten Unternehmensprofil und einer schnellen Website."),
    ("werbung", "Werbeanzeigen (Ads)",
     "Google Ads und Meta Ads auf Facebook und Instagram: wie Anzeigen Anfragen bringen statt Budget zu verbrennen."),
    ("kunden", "Kunden und Abläufe",
     "Was nach der Anfrage passiert: schnelle Antworten, Kundenmanagement und ein KI-Agent als Helfer."),
]

# Beitrag, der oben auf der Übersicht groß gezeigt wird
FEATURED = "/ratgeber/meta-ads-facebook-instagram/"

# Themen der vier bestehenden Artikel
THEMA_ALT = {
    "/ratgeber/was-kostet-eine-website/": "website",
    "/ratgeber/website-relaunch-checkliste/": "website",
    "/ratgeber/google-unternehmensprofil-optimieren/": "gefunden",
    "/ratgeber/crm-fuer-kleine-unternehmen/": "kunden",
}

_HINWEIS_RECHT = ('<p class="note">Dieser Beitrag gibt einen allgemeinen Überblick und ersetzt keine Rechtsberatung. '
                  'Ob und wie die Regeln für Ihren Betrieb gelten, klären Sie im Zweifel mit Ihrer Kammer oder einer Anwältin bzw. einem Anwalt.</p>')

NEW_ARTICLES = {
    # ------------------------------------------------------------------ Barrierefreiheit
    "/ratgeber/barrierefreie-website-bfsg/": {
        "thema": "website", "date": "18. November 2026", "iso": "2026-11-18",
        "teaser": "Seit Juni 2025 gilt das BFSG. Welche Websites betroffen sind, wer ausgenommen ist und wie Sie selbst prüfen.",
        "crumb": "Barrierefreie Website (BFSG)", "icon": "eye", "read": 6,
        "title": "Barrierefreie Website: Was das BFSG verlangt",
        "desc": "Seit dem 28. Juni 2025 gilt das Barrierefreiheitsstärkungsgesetz. Welche Websites betroffen sind, wer ausgenommen ist und wie Sie Ihre Seite prüfen.",
        "h1": 'Barrierefreie Website: <span class="quiet">Was das BFSG von Betrieben verlangt.</span>',
        "lead": "Seit dem 28. Juni 2025 gilt das Barrierefreiheitsstärkungsgesetz, kurz BFSG. Seitdem fragen sich viele Betriebe, ob ihre Website darunter fällt. Die gute Nachricht: längst nicht jede. Hier lesen Sie, worauf es ankommt und wie Sie Ihre Website selbst einschätzen.",
        "sections": [
            ("worum", "Worum es geht",
             "<p>Das BFSG setzt eine EU-Richtlinie in deutsches Recht um. Menschen mit Behinderungen, aber auch ältere Menschen sollen bestimmte Produkte und Dienstleistungen ohne Hürden nutzen können. Für Websites heißt das zum Beispiel: Sie lassen sich ohne Maus bedienen, werden von Screenreadern vorgelesen und sind auch bei eingeschränktem Sehen gut lesbar.</p>"),
            ("wer", "Welche Websites betroffen sind",
             "<p>Das Gesetz gilt unter anderem für <b>Dienstleistungen im elektronischen Geschäftsverkehr</b>, die nach dem 28. Juni 2025 für Verbraucherinnen und Verbraucher erbracht werden. Gemeint sind Websites und Apps, über die Verbraucher einen Vertrag abschließen können. Geschäfte nur zwischen Unternehmen sind nicht gemeint.</p>"
             "<p>Der Zentralverband des Deutschen Handwerks ordnet das in seinem Leitfaden (Stand August 2026) so ein:</p>"
             "<ul><li><b>Betroffen:</b> Onlineshops und andere Websites, über die Verbraucher Produkte oder Dienstleistungen kaufen.</li>"
             "<li><b>Eher betroffen:</b> Online-Buchungen. Mit Bezahlung im Netz gelten die Vorgaben, und auch bei Bezahlung vor Ort „spricht einiges dafür“, dass das Gesetz greift.</li>"
             "<li><b>In der Regel nicht betroffen:</b> reine Informationsseiten, auf denen ein Betrieb sich und seine Leistungen vorstellt – auch mit Kontaktformular, Kontaktdaten, Newsletter oder Stellenanzeigen.</li></ul>"
             "<p>Hat Ihre Website einen Shop oder eine Buchung, empfiehlt der Leitfaden, auch Startseite, Kontakt und Impressum barrierefrei zu gestalten.</p>"),
            ("ausnahme", "Die Ausnahme für Kleinstunternehmen",
             "<p>Ausgenommen sind Kleinstunternehmen, die Dienstleistungen anbieten. Dazu zählt ein Betrieb mit <b>weniger als zehn Beschäftigten</b> und einem <b>Jahresumsatz oder einer Jahresbilanzsumme von höchstens 2 Millionen Euro</b>. Für Produkte gilt diese Ausnahme nicht.</p>"
             "<p>Unabhängig von der Pflicht lohnt sich Barrierefreiheit trotzdem: Klare Überschriften, gut lesbare Kontraste und verständlich beschriftete Formulare machen eine Website für alle Besucher angenehmer.</p>"),
            ("anforderungen", "Was eine barrierefreie Website ausmacht",
             "<p>Als technischer Maßstab gilt die europäische Norm EN 301 549, die auf die international verbreiteten Web-Richtlinien WCAG verweist. In der Praxis bedeutet das vor allem:</p>"
             "<ul><li><b>Kontraste:</b> Text hebt sich deutlich vom Hintergrund ab.</li>"
             "<li><b>Tastatur:</b> Alles lässt sich mit der Tabulatortaste erreichen, und man sieht jederzeit, wo man gerade ist.</li>"
             "<li><b>Bilder:</b> Inhaltlich wichtige Bilder haben einen Alternativtext, den Screenreader vorlesen.</li>"
             "<li><b>Struktur:</b> Überschriften sind sauber gegliedert, Links und Knöpfe sagen, wohin sie führen.</li>"
             "<li><b>Formulare:</b> Jedes Feld ist beschriftet, Fehlermeldungen erklären, was zu tun ist.</li>"
             "<li><b>Zoom:</b> Die Seite bleibt auch bei starker Vergrößerung lesbar.</li>"
             "<li><b>Medien:</b> Videos haben Untertitel, Bewegungen lassen sich reduzieren.</li></ul>"
             "<p>Dazu kommt eine Informationspflicht: Betroffene Anbieter müssen beschreiben, wie ihre Dienstleistung die Anforderungen erfüllt, und die zuständige Marktüberwachungsbehörde nennen. Viele Websites tun das in einer eigenen Erklärung zur Barrierefreiheit.</p>"),
            ("folgen", "Was bei Verstößen droht",
             "<p>Das BFSG sieht Bußgelder von bis zu 100.000 Euro vor. Hinzu kommen nach Angaben der IHK mögliche Abmahnungen durch Wettbewerber und Klagen von Verbänden.</p>"),
            ("pruefen", "So schätzen Sie Ihre Website selbst ein",
             "<ul><li><b>1. Kann man bei Ihnen online einen Vertrag abschließen?</b> Shop, Buchung oder Bestellung – oder nur Informationen und Kontakt?</li>"
             "<li><b>2. Sind Sie ein Kleinstunternehmen</b> im Sinne des Gesetzes?</li>"
             "<li><b>3. Der Fünf-Minuten-Test:</b> Legen Sie die Maus weg und bedienen Sie Ihre Website nur mit der Tastatur. Vergrößern Sie die Ansicht auf 200 Prozent. Lassen Sie sich die Startseite einmal vom Screenreader Ihres Handys vorlesen.</li></ul>"
             "<p>Automatische Prüfwerkzeuge helfen beim Einstieg, finden aber nicht alle Probleme. Ob ein Alternativtext sinnvoll ist oder eine Fehlermeldung verständlich, muss ein Mensch beurteilen.</p>"),
            ("medialyte", "Barrierefreiheit mit Medialyte",
             "<p>Bei neuen Websites und bei einem <a href=\"{u:/leistungen/website-relaunch/}\">Relaunch</a> planen wir Barrierefreiheit von Anfang an mit ein: Kontraste, Tastaturbedienung, saubere Struktur und beschriftete Formulare. Haben Sie bereits eine Website mit Shop oder Buchung, schauen wir sie uns im <a href=\"{u:/termin/}\">kostenfreien Erstgespräch</a> an und sagen Ihnen, wo es hakt.</p>"
             + _HINWEIS_RECHT),
        ],
        "sources": [
            ("Barrierefreiheitsstärkungsgesetz (BFSG), §§ 1, 2, 3 und 37", "gesetze-im-internet.de", "https://www.gesetze-im-internet.de/bfsg/BJNR297010021.html"),
            ("Praxis Recht: Barrierefreiheit von Webseiten", "Zentralverband des Deutschen Handwerks, Stand 18.08.2026", "https://www.zdh.de/ueber-uns/fachbereich-organisation-und-recht/praxis-recht-/-leitfaeden/praxis-recht-barrierefreiheit-von-webseiten/"),
            ("Websites, Produkte und Dienstleistungen: Neue Regeln zur Barrierefreiheit", "IHK Hagen", "https://www.ihk.de/hagen/recht/rechtsthemen/aktuelles/barrierefreiheit-von-dienstleistungen-und-produkten-6335916"),
        ],
        "rel": ["/leistungen/website-relaunch/", "/leistungen/online-shop/"], "rel_rag": ["/ratgeber/website-ladezeit-core-web-vitals/"],
        "close": "Ist Ihre Website betroffen?",
    },
    # ------------------------------------------------------------------ Ladezeit
    "/ratgeber/website-ladezeit-core-web-vitals/": {
        "thema": "gefunden", "date": "18. November 2026", "iso": "2026-11-18",
        "teaser": "Die drei Werte, mit denen Google die Nutzererfahrung misst, die Grenzwerte und die häufigsten Bremsen.",
        "crumb": "Website-Ladezeit verbessern", "icon": "zap", "read": 5,
        "title": "Website-Ladezeit verbessern: Core Web Vitals erklärt",
        "desc": "Wie schnell muss eine Website laden? Die drei Core Web Vitals, die Grenzwerte von Google, die häufigsten Bremsen und was wirklich hilft.",
        "h1": 'Website-Ladezeit: <span class="quiet">die Core Web Vitals verständlich erklärt.</span>',
        "lead": "Eine langsame Website kostet Geduld – und damit Anfragen. Google bewertet die Nutzererfahrung mit drei Messwerten, den Core Web Vitals. Was sie bedeuten, welche Werte als gut gelten und was Ihre Website ausbremst.",
        "sections": [
            ("warum", "Warum die Ladezeit zählt",
             "<p>Viele Besucher kommen über das Handy, oft unterwegs und mit wechselndem Empfang. Baut sich eine Seite zäh auf, springt sie beim Laden hin und her oder reagiert ein Knopf nicht sofort, ist der Eindruck schnell verdorben – egal wie gut das Angebot ist.</p>"
             "<p>Auch Google legt Wert darauf. In der offiziellen Dokumentation heißt es: „Wir empfehlen Websiteinhabern dringend, gute Core Web Vitals zu erreichen, um in der Google Suche erfolgreich zu sein.“ Gute Werte ersetzen keine guten Inhalte. Sie sorgen aber dafür, dass gute Inhalte nicht an der Technik scheitern.</p>"),
            ("werte", "Die drei Werte und ihre Grenzen",
             "<ul><li><b>Largest Contentful Paint (LCP) – Ladezeit:</b> Wann ist der größte sichtbare Inhalt da, meist ein Bild oder die Überschrift? Gut sind höchstens <b>2,5 Sekunden</b>.</li>"
             "<li><b>Interaction to Next Paint (INP) – Reaktion:</b> Wie schnell reagiert die Seite, wenn jemand tippt oder klickt? Gut sind höchstens <b>200 Millisekunden</b>.</li>"
             "<li><b>Cumulative Layout Shift (CLS) – Stabilität:</b> Wie stark verrutschen Inhalte beim Laden? Gut ist ein Wert von höchstens <b>0,1</b>.</li></ul>"
             "<p>Google empfiehlt, die Werte an echten Besuchen zu messen, getrennt nach Handy und Computer. Maßstab ist das 75. Perzentil: Drei von vier Seitenaufrufen sollten die Grenzen einhalten.</p>"),
            ("messen", "So messen Sie Ihre Website",
             "<ul><li><b>Unser <a href=\"{u:/website-check/}\">Website-Check</a>:</b> misst Ihre Seite kostenlos und ohne Anmeldung in unter einer Minute und erklärt die Ergebnisse verständlich.</li>"
             "<li><b>PageSpeed Insights:</b> Adresse eingeben, und das kostenlose Werkzeug von Google zeigt die Werte – aus echten Besuchen, wenn genug Daten vorhanden sind, sonst aus einer Testmessung.</li>"
             "<li><b>Google Search Console:</b> Der Bericht zu den Core Web Vitals zeigt, welche Seitengruppen Probleme haben.</li>"
             "<li><b>Selbsttest am Handy:</b> Rufen Sie Ihre Website im Mobilfunknetz auf, nicht im Büro-WLAN.</li></ul>"),
            ("bremsen", "Die häufigsten Bremsen",
             "<ul><li>Große Bilder, die ungeschrumpft hochgeladen wurden</li>"
             "<li>Viele Erweiterungen und Skripte: Slider, Chat-Fenster, Tracking, Social-Media-Einbindungen</li>"
             "<li>Bilder und Werbeflächen ohne feste Maße – sie schieben beim Laden den Text nach unten</li>"
             "<li>Schriften und Dienste, die von fremden Servern nachgeladen werden</li>"
             "<li>Günstiges Hosting, das bei Besuch in die Knie geht</li>"
             "<li>Große Videos direkt im sichtbaren Startbereich</li></ul>"),
            ("massnahmen", "Was wirklich hilft",
             "<ul><li><b>Bilder optimieren:</b> moderne Formate wie WebP oder AVIF, passende Größe für jedes Gerät, Bilder weiter unten erst bei Bedarf laden.</li>"
             "<li><b>Platz reservieren:</b> Bilder, Videos und Einbettungen bekommen feste Maße, damit nichts verrutscht.</li>"
             "<li><b>Ausmisten:</b> Jedes Skript und jede Erweiterung muss ihren Platz verdienen.</li>"
             "<li><b>Schriften lokal einbinden</b> und auf die nötigen Schnitte beschränken.</li>"
             "<li><b>Zwischenspeichern und komprimieren:</b> Der Server liefert Dateien gepackt aus, der Browser merkt sich, was er schon kennt.</li></ul>"
             "<p>Oft bringt ein schlanker Neuaufbau mehr als das Flicken einer überladenen Website. Das ist einer der häufigsten Gründe für einen <a href=\"{u:/ratgeber/website-relaunch-checkliste/}\">Relaunch</a>.</p>"),
            ("medialyte", "Schnelle Websites mit Medialyte",
             "<p>Unsere eigene Website läuft ohne Baukasten und ohne WordPress-Erweiterungen, und genauso schlank bauen wir für unsere Kunden. Im <a href=\"{u:/termin/}\">kostenfreien Erstgespräch</a> messen wir gern Ihre aktuelle Website und sagen Ihnen, was sie ausbremst. Mehr zu Sichtbarkeit bei Google auf der Seite <a href=\"{u:/leistungen/seo/}\">Suchmaschinenoptimierung</a>.</p>"),
        ],
        "sources": [
            ("Web Vitals", "web.dev (Google)", "https://web.dev/articles/vitals"),
            ("Core Web Vitals und Google-Suchergebnisse", "Google Search Central", "https://developers.google.com/search/docs/appearance/core-web-vitals"),
        ],
        "rel": ["/leistungen/seo/", "/leistungen/website-relaunch/"], "rel_rag": ["/ratgeber/website-relaunch-checkliste/"],
        "close": "Wie schnell ist Ihre Website?",
    },
    # ------------------------------------------------------------------ Gute Website, wenig Anfragen
    "/ratgeber/gute-website-wenig-anfragen/": {
        "thema": "website", "date": "18. November 2026", "iso": "2026-11-18",
        "teaser": "Solide gebaut, ordentlich gestaltet – und trotzdem kaum Anfragen? Sieben Ursachen, die man leicht übersieht.",
        "crumb": "Gute Website, wenig Anfragen?", "icon": "trend", "read": 5,
        "title": "Gute Website, aber wenig Anfragen? 7 Ursachen",
        "desc": "Ihre Website ist solide, bringt aber kaum Anfragen? Sieben Ursachen, die auch bei guten Websites vorkommen – und was dagegen hilft.",
        "h1": 'Gute Website, wenig Anfragen? <span class="quiet">Sieben Ursachen, die man leicht übersieht.</span>',
        "lead": "Viele Unternehmen haben längst eine solide Website von einer Agentur. Sie sieht ordentlich aus, funktioniert auf dem Handy und ist rechtlich sauber. Trotzdem kommen über sie kaum Anfragen. Meist liegt es nicht am Design, sondern an Dingen, die man erst auf den zweiten Blick sieht.",
        "sections": [
            ("kunde", "1. Die Website spricht über sich statt über den Kunden",
             "<p>„Seit über 30 Jahren …“, „Unser Team …“, „Wir sind …“: Viele Websites erzählen zuerst vom eigenen Betrieb. Besucher wollen aber wissen, ob Sie ihr Problem lösen. Dazu kommt: In größeren Betrieben suchen Einkäufer, Technikerinnen und Geschäftsführer ganz Unterschiedliches. Wer alle mit demselben Text anspricht, erreicht keinen richtig.</p>"),
            ("finden", "2. Besucher finden nicht, was sie suchen",
             "<p>Die wichtigste Leistung steckt drei Klicks tief im Menü, das passende Produkt in einer langen Liste. Je größer das Angebot, desto wichtiger werden eine klare Gliederung, eine gute Suche und – bei vielen Produkten – ein Produktfinder mit Filtern.</p>"),
            ("schritt", "3. Der nächste Schritt ist unklar",
             "<p>Jede Seite braucht ein klares Ziel: anrufen, ein Angebot anfragen, einen Termin buchen. Fehlt es, lesen Besucher und gehen wieder. Auch zu lange Formulare mit vielen Pflichtfeldern oder eine Telefonnummer, die man auf dem Handy nicht antippen kann, kosten Anfragen.</p>"),
            ("versanden", "4. Anfragen versanden nach dem Absenden",
             "<p>Manchmal kommen die Anfragen – aber sie landen in einem allgemeinen Postfach, niemand fühlt sich zuständig, und die Antwort kommt nach Tagen. Dann liegt das Problem nicht auf der Website, sondern dahinter. Wie sich das ändern lässt, steht im Beitrag <a href=\"{u:/ratgeber/anfragen-schneller-beantworten/}\">Anfragen schneller beantworten</a>.</p>"),
            ("pflege", "5. Die Pflege ist zu umständlich",
             "<p>Jede Änderung ist ein Auftrag an die Agentur, mit Wartezeit und Rechnung. Also wird nichts geändert: Ansprechpartner sind veraltet, Messetermine vorbei, Stellenanzeigen längst besetzt. Besucher merken das und fragen sich, ob der Betrieb noch aktiv ist.</p>"),
            ("messen", "6. Niemand weiß, was funktioniert",
             "<p>Wie viele Anfragen kamen im letzten Monat über die Website? Über welche Seite, nach welcher Suche, aus welcher Anzeige? Ohne saubere und datenschutzkonforme Messung wird nach Bauchgefühl entschieden – und Budget fließt in Kanäle, die nichts bringen.</p>"),
            ("technik", "7. Die Technik bremst",
             "<p>Eine Website, die vor einigen Jahren modern war, kann heute zu langsam sein, auf neuen Geräten haken oder bei der Barrierefreiheit Lücken haben. Mehr dazu in den Beiträgen zur <a href=\"{u:/ratgeber/website-ladezeit-core-web-vitals/}\">Ladezeit</a> und zur <a href=\"{u:/ratgeber/barrierefreie-website-bfsg/}\">barrierefreien Website</a>.</p>"),
            ("medialyte", "Gut wird besser: So gehen wir vor",
             "<p>Wir werfen nichts weg, was funktioniert. Am Anfang steht eine ehrliche Bestandsaufnahme: Was bringt Ihre Website heute, wo verlieren Sie Besucher, und was passiert mit den Anfragen? Danach verbessern wir gezielt – vom Text über die Struktur bis zum <a href=\"{u:/leistungen/website-relaunch/}\">Relaunch</a>. Auf Wunsch verbinden wir die Website mit einem <a href=\"{u:/leistungen/kundenmanagement-system/}\">Kundenmanagement-System</a>, damit keine Anfrage mehr liegen bleibt.</p>"),
        ],
        "rel": ["/leistungen/website-relaunch/", "/leistungen/kundenmanagement-system/"], "rel_rag": ["/ratgeber/anfragen-schneller-beantworten/"],
        "close": "Ihre Website kann mehr?",
    },
    # ------------------------------------------------------------------ Google Ads
    "/ratgeber/google-ads-fuer-kleine-unternehmen/": {
        "thema": "werbung", "date": "18. November 2026", "iso": "2026-11-18",
        "teaser": "Wie Google Ads funktioniert, wie Sie Ihr Budget berechnen und welche Fehler am meisten Geld kosten.",
        "crumb": "Google Ads für kleine Unternehmen", "icon": "target", "read": 6,
        "title": "Google Ads für kleine Unternehmen: Start und Budget",
        "desc": "Wie funktioniert Google Ads, wie viel Budget brauche ich und welche Fehler kosten am meisten? Der Einstieg für kleine und mittlere Betriebe.",
        "h1": 'Google Ads für kleine Unternehmen: <span class="quiet">So starten Sie ohne Lehrgeld.</span>',
        "lead": "Mit Google Ads erscheinen Sie genau dann, wenn jemand nach Ihrer Leistung sucht – ohne monatelang auf bessere Platzierungen zu warten. Gleichzeitig lässt sich mit schlecht eingerichteten Anzeigen schnell Geld verbrennen. Worauf es beim Start ankommt.",
        "sections": [
            ("funktion", "So funktioniert Google Ads",
             "<p>Sie legen fest, bei welchen Suchbegriffen, in welcher Region und zu welchen Zeiten Ihre Anzeige erscheinen soll. Bezahlt wird bei Suchanzeigen in der Regel erst, wenn jemand auf die Anzeige klickt. Ob und wo Ihre Anzeige erscheint, hängt unter anderem von Ihrem Gebot ab und davon, wie gut Anzeige und Zielseite zur Suche passen.</p>"),
            ("budget", "Wie viel Budget brauche ich?",
             "<p>Eine feste Summe, die für alle passt, gibt es nicht. Der Preis eines Klicks hängt von Branche, Region und Wettbewerb ab. Rechnen Sie deshalb rückwärts: Wie viele Anfragen brauchen Sie, wie viele Besucher fragen erfahrungsgemäß an, und was kostet ein Klick?</p>"
             "<p><b>Ein Rechenbeispiel mit angenommenen Werten:</b> Kostet ein Klick 2 Euro und fragt jeder 20. Besucher an, kostet eine Anfrage 40 Euro. Für 10 Anfragen im Monat bräuchten Sie dann rund 400 Euro Werbebudget. Ob sich das lohnt, zeigt der Vergleich mit dem Wert eines Auftrags.</p>"
             "<p>Gut zu wissen: Das Tagesbudget ist bei Google ein Durchschnittswert. An einzelnen Tagen kann eine Kampagne bis zum Doppelten ausgeben. Im Monat berechnet Google aber höchstens das 30,4-Fache des durchschnittlichen Tagesbudgets.</p>"),
            ("keywords", "Die richtigen Suchbegriffe",
             "<p>Entscheidend ist die Absicht hinter der Suche. „Elektriker Notdienst Hamburg“ sucht jemand, der jetzt Hilfe braucht. „Steckdose selbst anschließen“ sucht jemand, der es allein versuchen will. Konzentrieren Sie Ihr Budget auf Suchen mit klarer Kaufabsicht.</p>"
             "<p>Mindestens genauso wichtig sind <b>ausschließende Keywords</b>: Begriffe wie „kostenlos“, „Ausbildung“, „Job“ oder „Anleitung“ verhindern, dass Ihre Anzeige bei unpassenden Suchen erscheint und Klicks kostet.</p>"),
            ("zielseite", "Die Zielseite entscheidet",
             "<p>Wer auf eine Anzeige für „Badsanierung“ klickt, sollte auf einer Seite über Badsanierung landen – nicht auf der Startseite. Die Zielseite greift das Versprechen der Anzeige auf, beantwortet die wichtigsten Fragen und macht die Kontaktaufnahme so einfach wie möglich. Genau dafür gibt es <a href=\"{u:/leistungen/landingpage/}\">Landingpages</a>.</p>"),
            ("messen", "Ohne Messung kein Erfolg",
             "<p>Richten Sie vor dem Start ein, dass Anfragen, Anrufe und Buchungen als Erfolg gezählt werden – datenschutzkonform und mit Einwilligung. Erst dann sehen Sie, welche Suchbegriffe Anfragen bringen und welche nur Geld kosten, und erst dann kann Google die Auslieferung gezielt verbessern.</p>"),
            ("fehler", "Die teuersten Fehler",
             "<ul><li>Zu allgemeine Suchbegriffe ohne ausschließende Keywords</li>"
             "<li>Alle Anzeigen führen auf die Startseite</li>"
             "<li>Kein Tracking, also keine Ahnung, was Anfragen bringt</li>"
             "<li>Eine zu große Region für einen Betrieb, der nur lokal arbeitet</li>"
             "<li>Ständiges Umstellen nach wenigen Tagen – Kampagnen brauchen Zeit und Daten</li>"
             "<li>Niemand schaut regelmäßig auf die Suchbegriffe, bei denen die Anzeige tatsächlich erschien</li></ul>"),
            ("medialyte", "Google Ads mit Medialyte",
             "<p>Wir haben über 200 Kampagnen betreut und kennen die typischen Stolperfallen. Wir richten Kampagne, Tracking und Zielseite zusammen ein und zeigen Ihnen jeden Monat in einem verständlichen Bericht, was Ihr Budget gebracht hat. Mehr dazu auf der Seite <a href=\"{u:/leistungen/google-ads/}\">Google Ads</a>.</p>"),
        ],
        "sources": [
            ("Warum die täglichen Kosten das durchschnittliche Tagesbudget überschreiten können", "Google Ads-Hilfe", "https://support.google.com/google-ads/answer/2375423?hl=de"),
        ],
        "rel": ["/leistungen/google-ads/", "/leistungen/meta-ads/"], "rel_rag": ["/ratgeber/google-ads-oder-meta-ads/", "/ratgeber/meta-ads-facebook-instagram/"],
        "close": "Google Ads richtig aufsetzen?",
    },
    # ------------------------------------------------------------------ KI-Agent
    "/ratgeber/ki-agent-im-betrieb/": {
        "thema": "kunden", "date": "18. November 2026", "iso": "2026-11-18",
        "teaser": "Welche Aufgaben ein KI-Agent heute zuverlässig übernimmt, wo die Grenzen liegen und was der AI Act verlangt.",
        "crumb": "KI-Agent im Betrieb", "icon": "bot", "read": 6,
        "title": "KI-Agent im Betrieb: Was er kann und was gilt",
        "desc": "Was ein KI-Agent im Alltag kleiner und mittlerer Betriebe übernehmen kann, wo die Grenzen liegen und was der AI Act seit August 2026 verlangt.",
        "h1": 'KI-Agent im Betrieb: <span class="quiet">Was er kann und wo die Grenzen liegen.</span>',
        "lead": "Künstliche Intelligenz ist im Alltag vieler Betriebe angekommen. Ein KI-Agent geht dabei über einen Chatbot hinaus: Er beantwortet nicht nur Fragen, sondern erledigt Aufgaben. Was heute sinnvoll ist, worauf Sie achten sollten und was rechtlich gilt.",
        "sections": [
            ("was", "Was ist ein KI-Agent?",
             "<p>Ein Chatbot antwortet. Ein KI-Agent handelt: Er liest eine Nachricht, versteht das Anliegen, führt die nötigen Schritte aus und meldet das Ergebnis. Er trägt zum Beispiel einen Termin ein, ändert die Öffnungszeiten auf der Website oder erinnert an eine Anfrage, die seit drei Tagen offen ist. Was er darf, legen Sie fest.</p>"),
            ("aufgaben", "Aufgaben, die sich lohnen",
             "<ul><li><b>Anfragen vorsortieren:</b> Anliegen erkennen, zusammenfassen und an die richtige Person geben.</li>"
             "<li><b>Erinnern und nachfassen:</b> an offene Anfragen, fällige Rückrufe und Angebote ohne Antwort.</li>"
             "<li><b>Website pflegen:</b> Öffnungszeiten, Preise, Speisekarte oder Termine per Nachricht ändern lassen.</li>"
             "<li><b>Entwürfe schreiben:</b> Antworten, Angebotstexte oder Beiträge – zum Prüfen und Freigeben.</li>"
             "<li><b>Wiederkehrende Fragen beantworten:</b> Anfahrt, Ablauf, Unterlagen.</li>"
             "<li><b>Überblick verschaffen:</b> Was ist diese Woche reingekommen, was ist liegen geblieben?</li></ul>"),
            ("grenzen", "Wo die Grenzen liegen",
             "<p>KI kann sich irren und dabei sehr überzeugend klingen. Verbindliche Zusagen, individuelle Preise, rechtliche oder medizinische Auskünfte gehören deshalb in menschliche Hände. Bewährt hat sich ein einfacher Grundsatz: Routine darf der Agent selbst erledigen, alles Wichtige bereitet er vor, und ein Mensch gibt es frei.</p>"),
            ("ai-act", "Was der AI Act verlangt",
             "<p>Seit dem 2. August 2026 gelten die Transparenzpflichten der europäischen KI-Verordnung, auch AI Act genannt. Für Betriebe besonders wichtig: KI-Systeme, die direkt mit Menschen sprechen oder schreiben, müssen so gestaltet sein, dass die Nutzer erfahren, dass sie mit einer KI kommunizieren – es sei denn, das ist ohnehin offensichtlich. Die im Jahr 2026 beschlossenen Erleichterungen der EU (der sogenannte Digital Omnibus) haben diese Pflicht nicht verschoben.</p>"
             "<p>Für einen Chat auf Ihrer Website heißt das in der Praxis: ein klarer Hinweis wie „Sie schreiben mit unserem KI-Assistenten“. Weitere Pflichten betreffen etwa KI-erzeugte Bilder und Videos.</p>"
             + _HINWEIS_RECHT),
            ("datenschutz", "Datenschutz nicht vergessen",
             "<p>Sobald ein KI-Agent mit Kundendaten arbeitet, gilt die Datenschutz-Grundverordnung. Klären Sie, wo die Daten verarbeitet werden, schließen Sie mit dem Anbieter einen Vertrag zur Auftragsverarbeitung, geben Sie dem Agenten nur die Daten, die er wirklich braucht, und ergänzen Sie Ihre Datenschutzerklärung.</p>"),
            ("start", "So fangen Sie an",
             "<ul><li><b>Eine Aufgabe wählen,</b> die regelmäßig Zeit kostet und klaren Regeln folgt.</li>"
             "<li><b>Regeln festlegen:</b> Was darf der Agent selbst, was nur mit Freigabe, was nie?</li>"
             "<li><b>Mit Freigabe starten</b> und die Ergebnisse ein paar Wochen prüfen.</li>"
             "<li><b>Erweitern,</b> wenn es zuverlässig läuft.</li></ul>"),
            ("medialyte", "Der KI-Agent von Medialyte",
             "<p>Unser <a href=\"{u:/leistungen/ki-agent/}\">KI-Agent</a> arbeitet mit Ihrer Website und Ihrem <a href=\"{u:/leistungen/kundenmanagement-system/}\">Kundenmanagement-System</a> zusammen: Änderungen an der Website schicken Sie per WhatsApp, offene Anfragen meldet er von selbst. Er ist ein Helfer im Hintergrund – die Entscheidungen bleiben bei Ihnen.</p>"),
        ],
        "sources": [
            ("AI Act: Neue Transparenzpflichten gelten ab dem 2. August", "IHK Hannover, Stand 29.07.2026", "https://www.ihk.de/hannover/hauptnavigation/digitalisierung/aktuell-digitalisierung/ai-act-neue-transparenzpflichten-gelten-ab-dem-2-august-7129608"),
            ("EU AI Act: Was am 2.8.2026 wirklich gilt (Digital Omnibus)", "r.at", "https://r.at/blog/digital-omnibus-final-eu-ai-act-2-august-2026"),
            ("Verordnung (EU) 2024/1689 (KI-Verordnung), Artikel 50", "EUR-Lex", "https://eur-lex.europa.eu/eli/reg/2024/1689/oj"),
        ],
        "rel": ["/leistungen/ki-agent/", "/leistungen/kundenmanagement-system/"], "rel_rag": ["/ratgeber/crm-fuer-kleine-unternehmen/"],
        "close": "Neugierig auf den KI-Agenten?",
    },
    # ------------------------------------------------------------------ Anfragen schneller beantworten
    "/ratgeber/anfragen-schneller-beantworten/": {
        "thema": "kunden", "date": "18. November 2026", "iso": "2026-11-18",
        "teaser": "Wer zuerst kompetent antwortet, hat oft die besten Karten. So werden Sie schneller – ohne ständig aufs Handy zu schauen.",
        "crumb": "Anfragen schneller beantworten", "icon": "inbox", "read": 5,
        "title": "Anfragen schneller beantworten: Warum Tempo zählt",
        "desc": "Warum die Reaktionszeit auf Anfragen über Aufträge entscheidet und wie Sie schneller antworten – mit klaren Abläufen statt Überstunden.",
        "h1": 'Anfragen schneller beantworten: <span class="quiet">Warum die ersten Stunden zählen.</span>',
        "lead": "Eine Anfrage über die Website ist ein Moment echten Interesses. Wer Tage braucht, um zu antworten, trifft oft auf jemanden, der sich längst anders entschieden hat. Warum Tempo zählt und wie Sie schneller werden, ohne ständig aufs Handy zu schauen.",
        "sections": [
            ("warum", "Warum Tempo zählt",
             "<p>Wer online anfragt, vergleicht meist mehrere Anbieter und schreibt oft mehrere gleichzeitig an. Wer zuerst kompetent antwortet, setzt den Maßstab für alle anderen. Dass hier viel Potenzial liegt, zeigte schon eine viel beachtete Untersuchung in der Harvard Business Review zu Reaktionszeiten auf Online-Anfragen. Das Fazit der Autoren: „Die meisten Unternehmen antworten nicht annähernd schnell genug.“</p>"),
            ("haengen", "Wo Anfragen hängen bleiben",
             "<ul><li>Anfragen kommen über Telefon, E-Mail, WhatsApp, Formular und Social Media – und landen an verschiedenen Stellen.</li>"
             "<li>Ein allgemeines Postfach, für das sich niemand richtig zuständig fühlt.</li>"
             "<li>Wichtige Angaben fehlen, also ist erst eine Rückfrage nötig.</li>"
             "<li>Das Angebot braucht Zeit, und bis dahin hört der Kunde nichts.</li></ul>"),
            ("sofort", "Sofort reagieren, ohne sofort zu antworten",
             "<p>Nicht jede Anfrage lässt sich in Minuten beantworten. Aber jede lässt sich sofort bestätigen: Eine automatische Eingangsbestätigung sagt, dass die Anfrage angekommen ist, bis wann sich jemand meldet und was als Nächstes passiert. Wer einen Termin braucht, kann ihn direkt auf der Website buchen. Häufige Fragen beantwortet die Website, bevor sie gestellt werden.</p>"),
            ("formular", "Bessere Anfragen durch bessere Formulare",
             "<p>Ein Freitextfeld „Ihre Nachricht“ führt oft zu Rückfragen. Ein Formular, das gezielt nach den wichtigen Angaben fragt – Leistung, Umfang, Ort, Wunschtermin –, liefert alles, was Sie für ein Angebot brauchen. In mehreren kurzen Schritten wirkt es dabei nicht abschreckend.</p>"),
            ("ablauf", "Ein klarer Ablauf im Team",
             "<ul><li><b>Ein Ort für alle Anfragen,</b> egal über welchen Weg sie kommen.</li>"
             "<li><b>Klare Zuständigkeit:</b> Jede Anfrage hat eine verantwortliche Person.</li>"
             "<li><b>Sichtbarer Stand:</b> neu, in Bearbeitung, Angebot verschickt, nachfassen.</li>"
             "<li><b>Vorlagen</b> für wiederkehrende Antworten, die Sie nur noch anpassen.</li>"
             "<li><b>Erinnerungen,</b> bevor eine Anfrage liegen bleibt.</li></ul>"),
            ("nachfassen", "Nachfassen nicht vergessen",
             "<p>Ein verschicktes Angebot ist noch kein Auftrag. Eine kurze, freundliche Nachfrage nach einigen Tagen klärt offene Fragen und zeigt, dass Ihnen der Auftrag wichtig ist. Damit das nicht vom Gedächtnis abhängt, sollte die Erinnerung automatisch kommen.</p>"),
            ("medialyte", "So hilft Medialyte",
             "<p>Wir bauen Formulare, die direkt in Ihrem <a href=\"{u:/leistungen/kundenmanagement-system/}\">Kundenmanagement-System</a> landen – mit automatischer Bestätigung, klarer Zuständigkeit und Erinnerungen. Unser <a href=\"{u:/leistungen/ki-agent/}\">KI-Agent</a> fasst neue Anfragen zusammen und meldet sich, wenn etwas liegen bleibt.</p>"),
        ],
        "sources": [
            ("The Short Life of Online Sales Leads (J. B. Oldroyd, K. McElheran, D. Elkington)", "Harvard Business Review, März 2011", "https://hbr.org/2011/03/the-short-life-of-online-sales-leads"),
        ],
        "rel": ["/leistungen/kundenmanagement-system/", "/leistungen/ki-agent/"], "rel_rag": ["/ratgeber/crm-fuer-kleine-unternehmen/"],
        "close": "Keine Anfrage mehr verlieren?",
    },
    # ------------------------------------------------------------------ Meta Ads
    "/ratgeber/meta-ads-facebook-instagram/": {
        "thema": "werbung", "date": "18. November 2026", "iso": "2026-11-18",
        "teaser": "Wie Werbung auf Facebook und Instagram funktioniert, was ein gutes Motiv ausmacht und welche Sonderregeln gelten.",
        "crumb": "Meta Ads: Facebook & Instagram", "icon": "camera", "read": 6,
        "title": "Meta Ads: Werbung auf Facebook & Instagram erklärt",
        "desc": "Wie Meta Ads funktionieren, wen Sie auf Facebook und Instagram erreichen, was ein gutes Motiv ausmacht und welche Sonderregeln für Stellenanzeigen gelten.",
        "h1": 'Meta Ads: <span class="quiet">Werbung auf Facebook und Instagram, die Anfragen bringt.</span>',
        "lead": "Auf Facebook und Instagram verbringen Ihre Kunden jeden Tag Zeit – auch die, die noch gar nicht nach Ihnen suchen. Mit Meta Ads erreichen Sie genau diese Menschen in Ihrer Region. Wie das funktioniert und worauf es ankommt.",
        "sections": [
            ("was", "Was sind Meta Ads?",
             "<p>Meta ist das Unternehmen hinter Facebook, Instagram, Messenger und WhatsApp. Über den Werbeanzeigenmanager von Meta schalten Sie Anzeigen vor allem auf Facebook und Instagram: im Feed, in Stories und in Reels. Möglich sind Bilder, Videos und Karussells mit mehreren Bildern hintereinander.</p>"),
            ("unterschied", "Der große Unterschied zu Google",
             "<p>Bei <a href=\"{u:/ratgeber/google-ads-fuer-kleine-unternehmen/}\">Google Ads</a> sucht der Kunde bereits nach Ihrer Leistung. Bei Meta Ads scrollt er durch seinen Feed und wird auf etwas aufmerksam, wonach er noch gar nicht gesucht hat. Meta Ads wecken also Bedarf, statt ihn abzufangen.</p>"
             "<p>Deshalb eignen sie sich besonders, um in der Region bekannt zu werden, ein neues Angebot vorzustellen, für eine Veranstaltung zu werben oder neue Mitarbeiter zu finden. Einen ausführlichen Vergleich finden Sie im Beitrag <a href=\"{u:/ratgeber/google-ads-oder-meta-ads/}\">Google Ads oder Meta Ads?</a></p>"),
            ("zielgruppe", "Wen Sie erreichen",
             "<ul><li><b>Region:</b> ein Umkreis um Ihren Betrieb, einzelne Städte oder ganz Deutschland.</li>"
             "<li><b>Alter und Interessen:</b> etwa Menschen, die sich für Einrichtung, Sport oder Gastronomie interessieren.</li>"
             "<li><b>Eigene Zielgruppen:</b> zum Beispiel Besucher Ihrer Website, die noch nicht angefragt haben – nur mit deren Einwilligung.</li></ul>"
             "<p>Meta findet passende Menschen zunehmend selbst. Umso wichtiger wird das Motiv: Es entscheidet, wer stehen bleibt.</p>"),
            ("motiv", "Das Motiv entscheidet",
             "<ul><li><b>Die ersten Sekunden zählen:</b> Im Feed wird schnell weitergewischt. Zeigen Sie sofort, worum es geht.</li>"
             "<li><b>Hochkant denken:</b> Stories und Reels füllen den ganzen Bildschirm des Handys.</li>"
             "<li><b>Echt statt Hochglanz:</b> Ihr Team, Ihre Arbeit, Ihre Räume wirken oft stärker als Stockfotos.</li>"
             "<li><b>Untertitel:</b> Damit das Video auch ohne Ton verstanden wird.</li>"
             "<li><b>Eine klare Botschaft</b> und ein klarer nächster Schritt pro Anzeige.</li>"
             "<li><b>Mehrere Varianten testen:</b> Zwei oder drei Motive zeigen schnell, was ankommt.</li></ul>"),
            ("ziel", "Anfragen statt Likes",
             "<p>Beim Anlegen einer Kampagne wählen Sie ein Ziel, etwa Leads, Umsätze oder Besuche auf der Website. Meta liefert die Anzeige dann vor allem an Menschen aus, die dieses Ziel wahrscheinlich erfüllen. Wer „Interaktionen“ wählt, bekommt Likes – aber nicht unbedingt Kunden. Auch der Knopf „Beitrag hervorheben“ ist bequem, bietet aber weniger Steuerung als der Werbeanzeigenmanager.</p>"
             "<p>Für Anfragen gibt es zwei Wege: ein <b>Formular direkt in Facebook oder Instagram</b>, das schnell ausgefüllt ist, oder eine <b><a href=\"{u:/leistungen/landingpage/}\">Landingpage</a></b> auf Ihrer Website, die mehr erklärt und gezielter fragt. Welcher Weg besser passt, hängt von Ihrem Angebot ab.</p>"),
            ("messen", "Messen mit Pixel und Conversions API",
             "<p>Damit Meta weiß, welche Anzeigen zu Anfragen führen, braucht es eine Messung. Der <b>Meta-Pixel</b> erfasst Ereignisse im Browser, die <b>Conversions API</b> überträgt sie direkt von Ihrem Server oder Kundensystem. Laut Meta werden diese Server-Ereignisse wie Pixel-Ereignisse verarbeitet und für Auswertung und Optimierung genutzt.</p>"
             "<p>Wichtig in Deutschland: Die Messung muss datenschutzkonform eingerichtet sein, in der Regel mit Einwilligung der Besucher über Ihr Cookie-Banner.</p>"),
            ("sonderregeln", "Sonderregeln: Stellenanzeigen, Wohnungen, Finanzen, Politik",
             "<p>Für Anzeigen zu <b>Jobs, Wohnraum und Finanzprodukten</b> gelten bei Meta besondere Anzeigenkategorien. Wer Werbung für eine offene Stelle schaltet, muss die Kampagne entsprechend kennzeichnen. Dann ist die Auswahl der Zielgruppe eingeschränkt: Alle Geschlechter, Alter grundsätzlich von 18 bis über 65, in Europa ein Umkreis von mindestens 15 Kilometern und keine ähnlichen Zielgruppen (Lookalikes).</p>"
             "<p>Anzeigen zu <b>politischen und gesellschaftlichen Themen</b> lässt Meta in der EU seit dem 6. Oktober 2025 nicht mehr zu.</p>"),
            ("budget", "Budget und Geduld",
             "<p>Sie legen ein Tagesbudget oder ein Gesamtbudget für die Laufzeit fest und können es jederzeit ändern. Starten Sie lieber mit einem überschaubaren Budget und wenigen, guten Motiven, als das Geld auf viele Anzeigen zu verteilen. Die Auslieferung braucht ein paar Tage, um zu lernen – wer täglich alles umstellt, bremst sie aus.</p>"),
            ("medialyte", "Meta Ads mit Medialyte",
             "<p>Wir planen Ihre Kampagnen, produzieren die Motive – von Fotos bis zu Reels mit Motion Design –, bauen die passende Landingpage und richten die Messung ein. Jeden Monat sehen Sie in einem verständlichen Bericht, was Ihr Budget gebracht hat. Mehr auf der Seite <a href=\"{u:/leistungen/meta-ads/}\">Meta Ads</a>.</p>"),
        ],
        "sources": [
            ("Special Ad Categories (besondere Anzeigenkategorien)", "Meta for Developers, Marketing API", "https://developers.facebook.com/documentation/ads-commerce/marketing-api/audiences/special-ad-category"),
            ("Conversions API", "Meta for Developers", "https://developers.facebook.com/documentation/ads-commerce/conversions-api"),
        ],
        "rel": ["/leistungen/meta-ads/", "/leistungen/social-media-marketing/"], "rel_rag": ["/ratgeber/google-ads-oder-meta-ads/", "/ratgeber/google-ads-fuer-kleine-unternehmen/"],
        "close": "Werbung auf Facebook und Instagram?",
    },
    # ------------------------------------------------------------------ Google oder Meta
    "/ratgeber/google-ads-oder-meta-ads/": {
        "thema": "werbung", "date": "18. November 2026", "iso": "2026-11-18",
        "teaser": "Nachfrage abfangen oder Nachfrage wecken? Welcher Kanal zu Ihrem Betrieb passt – und wann sich beide lohnen.",
        "crumb": "Google Ads oder Meta Ads?", "icon": "sliders", "read": 4,
        "title": "Google Ads oder Meta Ads? Der Vergleich",
        "desc": "Google Ads oder Werbung auf Facebook und Instagram? Die Unterschiede, typische Einsatzbereiche je Branche und wann sich beide Kanäle zusammen lohnen.",
        "h1": 'Google Ads oder Meta Ads? <span class="quiet">Was zu Ihrem Betrieb passt.</span>',
        "lead": "Beide Kanäle können Kunden bringen – aber auf ganz unterschiedliche Weise. Wer den Unterschied kennt, setzt sein Werbebudget dort ein, wo es am meisten bewirkt.",
        "sections": [
            ("kern", "Der Kern: abfangen oder wecken",
             "<p><b>Google Ads fangen Nachfrage ab.</b> Ihre Anzeige erscheint, wenn jemand aktiv nach Ihrer Leistung sucht – „Dachdecker Hamburg“, „Steuerberater in der Nähe“. Der Bedarf ist schon da.</p>"
             "<p><b>Meta Ads wecken Nachfrage.</b> Ihre Anzeige erscheint auf Facebook und Instagram, während jemand durch seinen Feed scrollt. Er hat nicht nach Ihnen gesucht, wird aber aufmerksam – weil das Motiv ihn anspricht.</p>"),
            ("vergleich", "Der Vergleich auf einen Blick",
             "<div class=\"rtable\"><table><thead><tr><th></th><th>Google Ads</th><th>Meta Ads</th></tr></thead><tbody>"
             "<tr><th>Situation des Kunden</th><td>sucht aktiv nach einer Lösung</td><td>scrollt und ist offen für Neues</td></tr>"
             "<tr><th>Stärke</th><td>dringender, konkreter Bedarf</td><td>Bekanntheit, neue Angebote, Emotionen</td></tr>"
             "<tr><th>Was zählt</th><td>Suchbegriffe und Zielseite</td><td>Motiv, Video und Zielgruppe</td></tr>"
             "<tr><th>Typische Ziele</th><td>Anrufe, Anfragen, Buchungen</td><td>Reichweite, Anfragen, Bewerbungen</td></tr>"
             "<tr><th>Passt oft zu</th><td>Handwerk, Kanzleien, Praxen, Notdienste, B2B</td><td>Gastronomie, Handel, Beauty, Events, Recruiting</td></tr>"
             "</tbody></table></div>"),
            ("google", "Wann Google Ads die bessere Wahl ist",
             "<ul><li>Kunden suchen bereits aktiv nach Ihrer Leistung.</li><li>Der Bedarf ist dringend: Rohrbruch, Schlüsseldienst, Termin beim Anwalt.</li>"
             "<li>Ihre Leistung lässt sich schlecht in einem Bild zeigen, aber gut in Worten suchen.</li><li>Sie verkaufen an Unternehmen, die gezielt nach Anbietern suchen.</li></ul>"),
            ("meta", "Wann Meta Ads die bessere Wahl ist",
             "<ul><li>Ihr Angebot ist neu oder noch wenig bekannt – danach sucht noch niemand.</li><li>Ihre Leistung lebt von Bildern: Essen, Mode, Einrichtung, Vorher-Nachher.</li>"
             "<li>Sie möchten in Ihrer Region bekannt werden oder für eine Veranstaltung werben.</li><li>Sie suchen Mitarbeiter, die gerade gar nicht aktiv nach einem Job suchen.</li></ul>"),
            ("beides", "Am stärksten: beide zusammen",
             "<p>Oft ergänzen sich die Kanäle. Meta Ads machen Ihren Betrieb in der Region bekannt. Wenn diese Menschen später Bedarf haben, suchen sie bei Google – und finden Sie dort wieder, über Anzeigen und Ihr <a href=\"{u:/ratgeber/google-unternehmensprofil-optimieren/}\">Unternehmensprofil</a>. Wichtig ist, beide Kanäle gemeinsam auszuwerten, damit Sie sehen, was am Ende wirklich Anfragen bringt.</p>"),
            ("start", "Mit begrenztem Budget: Wo anfangen?",
             "<p>Starten Sie dort, wo die Nachfrage schon ist. Suchen Ihre Kunden aktiv nach Ihrer Leistung, beginnen Sie mit Google Ads. Ist Ihr Angebot neu, sehr visuell oder suchen Sie Personal, beginnen Sie mit Meta Ads. Wichtiger als der Kanal ist in beiden Fällen eine Zielseite, die überzeugt, und eine Messung, die zeigt, was wirkt.</p>"),
            ("medialyte", "Google und Meta mit Medialyte",
             "<p>Wir betreuen <a href=\"{u:/leistungen/google-ads/}\">Google Ads</a> und <a href=\"{u:/leistungen/meta-ads/}\">Meta Ads</a> aus einer Hand, abgestimmt auf Ihre Website und mit einem gemeinsamen Monatsbericht. Im Erstgespräch sagen wir Ihnen ehrlich, welcher Kanal für Ihren Betrieb am meisten verspricht.</p>"),
        ],
        "rel": ["/leistungen/google-ads/", "/leistungen/meta-ads/"], "rel_rag": ["/ratgeber/meta-ads-facebook-instagram/", "/ratgeber/google-ads-fuer-kleine-unternehmen/"],
        "close": "Welcher Kanal passt zu Ihnen?",
    },
}
