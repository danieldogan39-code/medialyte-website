# Erklärfilm „Medialyte in 100 Sekunden“

Animierter Film im Look der Website (1:41, 60 Bilder/s) in zwei Fassungen:

- **Breitbild 1920 × 1080** für die Website (Startseite, mit Kapiteln und Untertiteln)
- **Hochkant 1080 × 1920** für Reels, TikTok, YouTube Shorts und LinkedIn – jede Szene für das Hochformat neu angeordnet,
  mit eingebrannten Untertiteln und eigenem Titelbild

Jede Bewegung hängt an einem Wort des Sprechers, deshalb steuert der Zeitplan `timing.json` beide Fassungen.
Kamerafahrten werden mit Bewegungsunschärfe gerendert.

| Datei | Inhalt |
|---|---|
| `src/index.html`, `src/film.css`, `src/film.js` | Bühne mit allen Szenen und die Zeitleiste (GSAP, per Bild ansteuerbar) |
| `src/film_v.css` | Hochkant-Layout (nur mit `<body class="v">`); sichere Fläche für die Bedienelemente der Apps |
| `src/cover.html` | Titelbild der Hochkant-Fassung |
| `src/img/` | Fotos der Beispiel-Tischlerei (KI-generiert, ElevenLabs Images), Bild der alten Website, Körnung |
| `script.txt`, `script_tts.txt` | Sprechertext: Schreibweise für Untertitel bzw. so, wie er an ElevenLabs ging (Pausen, Lautschrift für „Medialyte“) |
| `audio/vo5_take1.mp3` | Sprecher: ElevenLabs v4, Stimme „Helmut – Warm Trustworthy Narrator“ (`TUKJhQmz3RPYBNAgC5A1`), Markenname /ˈmeːdi̯aˌlaɪ̯t/ |
| `audio/vo5_take1.align.json` | Wortzeiten dieses Takes von ElevenLabs |
| `audio/music1.mp3` | Musik: ElevenLabs Music, instrumental, 96 BPM (gemessen) |
| `sfx/` | Geräusche (ElevenLabs Sound Effects) und `sfx_map.json` |
| `timing.json` | Sätze und Wörter in der Zeit des fertigen Films (nach `voice_timing.py`) |

Die fertigen Breitbild-Dateien liegen in `src/assets/video/` der Website (MP4, WebM, Vorschaubild, Untertitel).

## Regeln für saubere Bewegung

- Szenen überblenden nie ineinander: Kamerafahrten, Wischen oder Anschlussbewegungen (das Logo fliegt in die Buchungskarte,
  das Dashboard wird zur Kachel). Die alte Szene ist weg, bevor die neue steht.
- Kein Dauer-Zoom auf ganze Szenen – Schrift würde flimmern. Bewegt wird über `transform` und `opacity`.
- Jede Szene steht vor dem Wechsel mindestens eine Drittelsekunde still.
- Texte, Zähler und Zustände richten sich nach der Bildzeit, nicht nach den Abtastungen der Bewegungsunschärfe – Ziffern bleiben scharf.
- Gemessen wird erst, wenn die Schrift geladen ist; sonst stimmen Breiten und Höhen nicht.
- Der Sprecher wird nie geschnitten: `voice_timing.py` verlängert nur vorhandene Stille an Szenenwechseln.
- Die Musik wird nur auf dem gemessenen Schlagraster geschnitten (`mix.py` gleicht den Sprung zusätzlich an den Einsätzen ab).

## Neu bauen

```bash
cd film
python3 voice_timing.py vo5_take1  # Wortzeiten eichen, Luft an Szenenwechseln, schreibt audio/vo_timed.wav und timing.json
python3 build_stage.py             # Bühne nach stage/ (Breitbild)
python3 stills.py 12.5 44.6        # einzelne Standbilder prüfen (Zeiten aufsteigend)
python3 render.py cues             # Geräusche und Szenengrenzen nach cues.json
python3 mix.py                     # Musik im Takt schneiden, Sprecher, Musik und Geräusche mischen -> out/mix.wav (-16 LUFS)
python3 render.py probe 60         # Bewegung je Bild messen -> motion.json
python3 render.py video out/film60.mkv 60 2   # verlustfreie Zwischendatei mit Bewegungsunschärfe, zwei Abschnitte parallel
python3 qa_motion.py out/film60.mkv          # Sprünge, Aufploppen und Flackern finden
python3 determinism.py             # gleiche Bilder, egal ob die Seite springt oder vorwärts läuft
python3 captions.py                # Untertitel out/medialyte-film.de.vtt und .srt
python3 encode.py                  # MP4 (Web), Master-MP4 und WebM nach out/
python3 chapters.py                # Kapitelmarken und Länge für FILM_CHAPTERS in parts.py
```

Danach `out/medialyte-film.mp4`, `.webm`, `.de.vtt` und ein Standbild als `medialyte-film.jpg` nach `src/assets/video/` kopieren.

### Hochkant-Fassung

```bash
python3 build_stage.py --v                    # Bühne nach stage_v/ (mit Titelbild cover.html)
python3 stills.py --v 12.5 44.6               # Standbilder nach stills_v/
python3 render.py cues --v                    # Szenengrenzen (gleich wie im Breitbild)
python3 render.py probe 60 --v
python3 render.py video out/film_v60.mkv 60 2 --v
python3 captions_v.py states                  # Untertitel-Zustände mit der Filmschrift rendern -> capcache/
python3 encode_v.py                           # out/medialyte-film-hochkant.mp4 (mit Untertiteln) und ohne Untertitel, Ton -14 LUFS
```

Die Untertitel stehen bei y 1380–1500, über den Bedienelementen der Apps. Wo die Bühne denselben Satz schon groß zeigt
(Wende, Frage, Abschluss), treten sie zurück.

Die Beispiel-Betriebe im Film (Tischlerei Brandt und ihre Kunden) sind erfunden; die Kennzahlen von RechnungsRadar sind echt.
