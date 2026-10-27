# medialyte.de

Neue Website von Medialyte – ohne WordPress, als schnelle statische Seiten plus ein kleines PHP-Skript für die Terminbuchung.

## Aufbau

| Pfad | Inhalt |
|---|---|
| `pages.py` | **Alle Texte und Inhalte** der Seiten (Startseite, Leistungen, Referenzen, Team, FAQ …) |
| `build.py` | Layout (Header, Footer, Meta-Daten, SEO), Kontaktdaten, Verfügbarkeit fürs Buchungsformular |
| `src/assets/css/site.css` | Gestaltung (Farben, Schrift Outfit, alle Bausteine) |
| `src/assets/js/site.js` | Interaktionen (Menü, Kundenreise, Referenz-Popup, Vorher/Nachher, Buchungsformular) |
| `src/assets/img/` | Logos, Referenz-Screenshots, Favicons, Vorschaubild `og.jpg` |
| `api/` | PHP-Endpunkte für die Terminbuchung (`termin.php`, `slots.php`) |
| `deploy/.htaccess` | HTTPS, Weiterleitungen alter WordPress-Adressen, Caching, Sicherheits-Header |
| `tools/` | Hilfsskripte (Bilder aufbereiten, Icons/OG-Bild erzeugen, Sichtprüfung) |

## Bauen

```bash
python3 build.py                 # Live-Version nach dist/
python3 build.py --mode preview  # Vorschau mit relativen Links und Demo-Formular nach preview/
python3 build.py --mode staging --cname neu.entwurf.medialyte.de  # Testversion für GitHub Pages nach staging/
```

`dist/` enthält alles, was auf den Server gehört, inklusive `sitemap.xml`, `robots.txt`, `.htaccess` und `api/`.

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
- [ ] Teamfotos ergänzen (`TEAM` in `pages.py`, Bilder nach `src/assets/img/team/`)
- [ ] Video einbauen (Platzhalter `video_block()` in `pages.py`)
- [ ] `api/config.php` auf dem Server anlegen, Webhook zum Dashboard setzen

Bestätigt am 27.10.2026: Termin-Zeiten (Mo–Do 9–18 Uhr, Fr 9–16 Uhr, 30 Minuten), WhatsApp-Nummer, Kennzahlen im Vorher/Nachher-Bereich, Freigabe des RITZ-Entwurfs als Referenz.
- [ ] Nach dem Livegang: Sitemap in der Google Search Console einreichen
