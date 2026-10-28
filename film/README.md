# Erklärfilm „Medialyte in 90 Sekunden“

Animierter Film im Look der Website (1920 × 1080, 60 Bilder/s, 1:26). Jede Bewegung hängt an einem Wort des Sprechers,
deshalb steuert der Zeitplan `timing.json` die ganze Animation.

| Datei | Inhalt |
|---|---|
| `src/index.html`, `src/film.css`, `src/film.js` | Bühne mit allen Szenen und die Zeitleiste (GSAP, per Bild ansteuerbar) |
| `script.txt`, `script_tts.txt` | Sprechertext: Schreibweise für Untertitel bzw. so, wie er an ElevenLabs ging (Zahlen ausgeschrieben, Pausen, „Medialeit“) |
| `audio/vo3_take2.mp3` | Sprecher: ElevenLabs, Stimme „Helmut – Warm Trustworthy Narrator“ (`TUKJhQmz3RPYBNAgC5A1`), eleven_multilingual_v2, Tempo 1,15, Stabilität 0,6 |
| `audio/vo3_take2.align.json` | Wortzeiten dieses Takes von ElevenLabs |
| `audio/music1.mp3` | Musik: ElevenLabs Music v2.5, instrumental, 95,7 BPM |
| `timing.json` | Sätze und Wörter in der Zeit des fertigen Films (nach `retime.py`) |

Die fertigen Dateien liegen in `src/assets/video/` der Website (MP4, WebM, Vorschaubild, Untertitel).

## Regeln für saubere Bewegung

- Szenen überblenden nie ineinander: die alte ist ganz weg, bevor die neue kommt (`scene()` in `film.js`).
- Kein Dauer-Zoom auf ganze Szenen – Schrift würde flimmern. Bewegt wird über `transform` und `opacity`.
- Wechsel innerhalb eines Bildschirms wischen (`clip-path`) oder schieben deckend, statt zwei Inhalte zu überblenden.
- Jede Szene steht am Ende mindestens eine Drittelsekunde still, bevor sie geht.
- Der Sprecher wird nie mitten im Ton geschnitten: `retime.py` kürzt oder verlängert nur echte Stille.

## Neu bauen

```bash
cd film
python3 retime.py vo3_take2        # Pausen formen (nur in Stille), schreibt audio/vo_timed.wav und timing.json
python3 mix.py                     # Musik auf Länge schneiden und mischen -> audio/mix.wav (-16 LUFS)
python3 build_stage.py             # Bühne nach stage/
python3 render.py stills 12.5 44.6 # einzelne Standbilder prüfen (Zeiten aufsteigend)
python3 render.py video out/film60.mkv 60 2   # verlustfreie Zwischendatei, zwei Abschnitte parallel
python3 qa_motion.py out/film60.mkv          # Sprünge, Aufploppen und Flackern finden
python3 captions.py                # Untertitel out/medialyte-film.de.vtt und .srt
python3 encode.py                  # MP4 (Web), Master-MP4 und WebM nach out/
python3 chapters.py                # Kapitelmarken und Länge für FILM_CHAPTERS in parts.py
```

Danach `out/medialyte-film.mp4`, `.webm`, `.de.vtt` und ein Standbild als `medialyte-film.jpg` nach `src/assets/video/` kopieren.
Neuer Sprecher-Take: Wortzeiten von ElevenLabs als `audio/<take>.align.json` ablegen (oder ersatzweise
`python3 align.py <take>` mit faster-whisper); `python3 pace.py <take>` zeigt Sprechtempo und Pausen.

Die Beispiel-Betriebe im Film (Tischlerei Brandt und ihre Kunden) sind erfunden; die Kennzahlen von RechnungsRadar sind echt.
