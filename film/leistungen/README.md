# Leistungsfilme (hochkant, je etwa 50 Sekunden)

Vier Filme, je einer für jede Leistung. Sie laufen auf den Leistungsseiten (Abschnitt `#film`, `svc_film()` in `parts.py`) und als Reels, TikToks oder Shorts.
Jeder Film folgt dem Muster Hook → Problem → Lösung. Durch alle vier Filme zieht sich eine Figur: Sophia Brandt, Tischlerin in Lüneburg (ein ausgedachtes Beispiel).

| Film | Leistungsseite | Länge | Hook |
|---|---|---|---|
| f1 | /leistungen/website-erstellung/ | 0:56 | „Ihre Website spricht mit allen?“ |
| f2 | /leistungen/kundenmanagement-system/ | 0:54 | „Wie viele Anfragen sind bei Ihnen diesen Monat verloren gegangen?“ |
| f3 | /leistungen/ki-agent/ | 0:45 | „Was kostet Sie eine kleine Änderung an Ihrer Website?“ |
| f4 | /leistungen/online-marketing/ | 0:53 | „Viele Anzeigen kosten Geld – und bringen nur Klicks.“ |

## Dateien

| Pfad | Inhalt |
|---|---|
| `scripts.json`, `*.txt`, `*.tts.txt` | Sprechertexte: Schreibweise für Untertitel bzw. so, wie sie an ElevenLabs gingen |
| `audio/` | Sprecher Helmut (ElevenLabs v4), je zwei Takes mit Wortzeiten |
| `f<n>/timing.json` | Wortzeiten im fertigen Film und Musikplan (Aufbruch auf dem Wendewort, letzter Schlag auf dem Logo) |
| `f<n>/hide.json` | Sätze, bei denen die Untertitel zurücktreten, weil die Bühne sie groß zeigt |
| `src/` | Bühnen: `f<n>.html/.css/.js` je Film, gemeinsame Bausteine in `svc.css`, `lib.js`, `common.js` |
| `medialyte-leistungsfilme-texte.md` | Texte zum Posten in den sozialen Medien |

## Ablauf beim Bauen

1. `timing.py` wählt den Take und legt die Zeiten an. `musicplan.py` setzt den Musiksprung auf das Schlagraster.
2. `build.py <n>` baut die Bühne. `stills.py <n> <t…>` erzeugt Standbilder zur Kontrolle.
3. Gerendert wird mit Bewegungsunschärfe über `../render.py` im Ordner `f<n>`: `cues --v`, `probe 60 --v`, `video out/film.mkv 60 2 --v`. Danach mischt `mix.py <n>` den Ton auf −14 LUFS.
4. `captions.py` (mit `FD=f<n>`) brennt die Untertitel ein, `encode.py <n>` erzeugt die MP4s für Social Media, `cover.py <n> <t>` das Titelbild.
5. `web.py <n>` erzeugt die Website-Fassung: 720 × 1280, 60 Bilder/s, etwa 6,6 MB. Sie liegt in `src/assets/video/leistung-*.mp4` und als Standbild `.webp`.

`mix.py` nutzt die Geräusch-Bausteine aus der Arbeitsumgebung der Social-Clips. Für einen Neubau den Pfad in `mix.py` anpassen.
