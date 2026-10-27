# medialyte.de

Neue Website von Medialyte – ohne WordPress, als schnelle statische Seiten plus ein kleines PHP-Skript für die Terminbuchung.

## Aufbau

| Pfad | Inhalt |
|---|---|
| `pages.py` | Seiten (Startseite, Leistungen, Referenzen, Über uns, Termin, Rechtliches) mit Titeln, Beschreibungen und Texten |
| `parts.py` | Gemeinsame Bausteine und Inhalte: Referenzen, Team, FAQ, Pakete und Paket-Finder, Ablauf, Kundenreise, Buchungsformular |
| `mocks.py` | Gezeichnete Oberflächen: Cockpit mit vier Beispiel-Betrieben (jede Beispiel-Website zeigt ihre wichtigste Funktion: reservieren, anfragen, Termin buchen), Relaunch alt → neu, Pipeline, KI-Agent zum Ausprobieren, Kampagne, Monatsbericht, KI-Agent im Dashboard |
| `build.py` | Kopfzeile, mobiles Menü, Fußzeile, Meta-Daten und SEO, Kontaktdaten, Verfügbarkeit fürs Buchungsformular |
| `src/css/*.css` | Gestaltung in Teilen (Grundlage, Raster, Bausteine, Kopfzeile, Startbereich, Abschnitte, Oberflächen, Buchung, Unterseiten, Bewegung) |
| `src/js/*.js` | Verhalten in Modulen; jedes Modul läuft gekapselt, ein Fehler legt nie die ganze Seite lahm |
| `src/assets/` | Schrift Outfit, Logos, Referenz-Screenshots, Favicons, Vorschaubild `og.jpg` |
| `api/` | PHP-Endpunkte für die Terminbuchung (`termin.php`, `slots.php`) |
| `deploy/.htaccess` | HTTPS, Weiterleitungen alter WordPress-Adressen, Caching, Sicherheits-Header |
| `tools/` | Hilfsskripte (Screenshots, Funktionstest, Referenzbilder, Wortmarke, Vorschaubild) |

CSS- und JS-Teile werden beim Bauen zu `assets/css/site.css` und `assets/js/site.js` zusammengefügt (mit Prüfsumme gegen alte Browser-Caches).

## Gestaltung in Kürze

- Nachtblau `#0E192A` als Grund, Stahlblau und Weiß für alles Informative.
- Korallrot `#FF5757` für das Logo, die wichtigste Aktion je Ansicht („Erstgespräch buchen“, immer mit weißer Schrift) und sparsam für aktive Zustände (Kundenreise, Ablauf, Paket-Empfehlung, geöffnete Frage).
- Schrift Outfit; Wortmarke „medialyte“ in Red Hat Display Italic (SIL OFL, `tools/fonts/`) als Pfad in `tools/wordmark.svg` (neu erzeugen: `python3 tools/wordmark.py`).
- Bewegung nur über `transform` und `opacity`, keine Layoutsprünge; bei „Bewegung reduzieren“ stehen alle Darstellungen sofort im Endzustand. Ohne JavaScript bleibt alles lesbar.
- Kundenreise (`journey()` in `parts.py`, Skript `src/js/28-stage.js`): ab 1000 × 640 px eine angeheftete Bühne, Scrollen schaltet die vier Stationen um, die Darstellungen werden passend skaliert. Müsste eine Darstellung stärker als auf 84 % verkleinert werden (z. B. 1366 × 657), stehen die Stationen untereinander – genauso wie mobil, ohne Skript und bei reduzierter Bewegung.
- Partner-Logos laufen als Laufband (`marquee_rows()` in `parts.py`; Startseite eine Reihe, Referenzen zwei gegenläufig versetzte Reihen). Neue Logos in `LOGOS` ergänzen.
- Antworten in den Häufigen Fragen lassen sich verlinken (`FAQ_IDS` in `parts.py`, Links mit `data-faq-link` klappen die Antwort auf).
- Demos starten erst, wenn sie wirklich zu sehen sind (`ML.presence` in `src/js/00-core.js`, berücksichtigt die aktive Station).

## Bauen

```bash
python3 build.py                 # Live-Version nach dist/
python3 build.py --mode preview  # Vorschau mit relativen Links und Demo-Formular nach preview/
python3 build.py --mode staging --cname neu.entwurf.medialyte.de  # Testversion für GitHub Pages nach staging/
```

`dist/` enthält alles, was auf den Server gehört, inklusive `sitemap.xml`, `robots.txt`, `.htaccess` und `api/`.

## Prüfen

```bash
python3 tools/flow_test.py /tmp/flow        # alle Interaktionen, Skriptfehler, Layoutsprünge (CLS), seitliches Scrollen
python3 tools/shots.py /tmp/shots 1440x900 390x844   # Bildschirmfotos aller Bereiche der Startseite
```

## Veröffentlichen bei IONOS

**Testversion:** Jeder Push auf `main` baut automatisch die Testversion (`staging.yml`) und veröffentlicht sie über GitHub Pages unter neu.entwurf.medialyte.de. Sie ist für Google gesperrt (noindex) und das Buchungsformular läuft dort im Demo-Modus.

**Variante A – automatisch (empfohlen):** Die vier Secrets aus `.github/workflows/deploy.yml` im Repository eintragen. Der Upload zu IONOS läuft zunächst nur manuell (Actions → Deploy medialyte.de → Run workflow). Zum Livegang im Workflow `push: branches: [main]` ergänzen, dann geht jede Änderung automatisch live.

**Variante B – manuell:** `python3 build.py` ausführen und den Inhalt von `dist/` per SFTP (z. B. FileZilla) in den Ordner laden, auf den medialyte.de zeigt.

Vor dem Umstieg: WordPress-Ordner sichern, dann die neue Seite in einen eigenen Ordner laden und im IONOS-Domain-Bereich auf diesen Ordner umstellen. So ist ein Zurückschalten jederzeit möglich.

## Terminbuchung einrichten

1. Auf dem Server `api/config.example.php` nach `api/config.php` kopieren und anpassen.
2. `mail_from` muss eine bei IONOS existierende Adresse sein (z. B. `termine@medialyte.de`).
3. Verfügbarkeit in `build.py` (`BOOKING`) und `api/config.php` (`hours`) gleich halten.
4. Buchungen werden in `api/data/bookings.jsonl` gespeichert (per `.htaccess` gesperrt), per E-Mail an Medialyte geschickt, der Kunde erhält eine Bestätigung mit Kalendereintrag.

### Anbindung an das Dashboard

Ist `webhook_url` gesetzt, wird jede Buchung als JSON per `POST` an das Dashboard geschickt:

- Header `X-Medialyte-Event: booking.created`
- Header `X-Medialyte-Signature: sha256=<HMAC-SHA256 des Body mit webhook_secret>`
- Body: `id, erstellt, status, anliegen[], anliegen_text[], firma, branche, website, ort, groesse, format, format_text, termin{datum, uhrzeit, start, dauer_min} | null, rueckruf{zeitfenster} | null, name, email, telefon, whatsapp_ok, nachricht, einwilligung, quelle{seite, referrer, utm}`

Das Dashboard prüft die Signatur und legt daraus einen Lead an. `slots.php` liefert belegte Termine (ohne personenbezogene Daten), damit das Formular sie ausblendet.

## Vor dem Livegang offen

- [ ] Datenschutzerklärung und AGB einfügen (`render_legal_placeholder` in `pages.py` ersetzen)
- [ ] Teamfotos ergänzen (`TEAM` in `parts.py`, Bilder nach `src/assets/img/team/`; `team()` zeigt bis dahin eine Liste mit Name, Aufgabe und einem Satz)
- [ ] Film einbauen (Platzhalter `film()` in `parts.py`, derzeit ohne Abspiel-Knopf)
- [ ] Optional: echte Fotos für die Beispiel-Websites im Cockpit (derzeit bewusst ohne Bilder, mit Funktionskarten)
- [ ] `api/config.php` auf dem Server anlegen, Webhook zum Dashboard setzen
- [ ] Nach dem Livegang: Sitemap in der Google Search Console einreichen

Bestätigt am 27.10.2026: Termin-Zeiten (Mo–Do 9–18 Uhr, Fr 9–16 Uhr, 30 Minuten), WhatsApp-Nummer, Kennzahlen im Vorher/Nachher-Bereich, Freigabe des RITZ-Entwurfs als Referenz. Die Beispiel-Betriebe im Cockpit (Trattoria Lume, Tischlerei Brandt, Zahnarztpraxis am Park, Kanzlei Lindqvist) sind erfunden und als Beispiel gekennzeichnet.
