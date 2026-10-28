# Erklärfilm „Medialyte in 100 Sekunden“

Animierter Film im Look der Website (1920 × 1080, 30 Bilder/s, 1:37). Jede Bewegung hängt an einem Wort des Sprechers,
deshalb steuert der Zeitplan `timing.json` die ganze Animation.

| Datei | Inhalt |
|---|---|
| `src/index.html`, `src/film.css`, `src/film.js` | Bühne mit allen Szenen und die Zeitleiste (GSAP, per Bild ansteuerbar) |
| `audio/vo_take1.mp3` | Sprecher: ElevenLabs, Stimme „Helmut – Warm Trustworthy Narrator“ (`TUKJhQmz3RPYBNAgC5A1`), Modell eleven_v4 |
| `audio/music1.mp3` | Musik: ElevenLabs Music v2.5, instrumental, 95,7 BPM |
| `audio/vo_take1.words.json` | Wortzeiten des Sprechers (faster-whisper) |
| `timing.json` | Sätze und Wörter in der Zeit des fertigen Films (nach `retime.py`) |

Die fertigen Dateien liegen in `src/assets/video/` der Website (MP4, WebM, Vorschaubild, Untertitel).

## Neu bauen

```bash
cd film
python3 align.py vo_take1          # Wortzeiten (nur nach neuem Sprecher; braucht faster-whisper)
python3 retime.py                  # Pausen an den Kapitelgrenzen, schreibt audio/vo_timed.wav und timing.json
python3 mix.py                     # Musik auf Länge schneiden und mischen -> audio/mix.wav (-16 LUFS)
python3 build_stage.py             # Bühne nach stage/
python3 render.py stills 12.5 44.6 # einzelne Standbilder prüfen
python3 render.py video out/film_silent.mp4 30
python3 captions.py                # Untertitel out/medialyte-film.de.vtt
```

Danach kodieren:

```bash
ffmpeg -i out/film_silent.mp4 -i audio/mix.wav -map 0:v -map 1:a -c:v libx264 -preset veryfast -crf 23 -profile:v high \
  -pix_fmt yuv420p -tune animation -c:a aac -b:a 128k -shortest -movflags +faststart ../src/assets/video/medialyte-film.mp4
ffmpeg -i out/film_silent.mp4 -i audio/mix.wav -map 0:v -map 1:a -c:v libvpx-vp9 -b:v 0 -crf 38 -deadline good -cpu-used 4 \
  -row-mt 1 -c:a libopus -b:a 96k -shortest ../src/assets/video/medialyte-film.webm
ffmpeg -ss 44.8 -i out/film_silent.mp4 -frames:v 1 -vf scale=1280:720 -q:v 3 ../src/assets/video/medialyte-film.jpg
```

Kapitel-Startzeiten für die Website stehen in `FILM_CHAPTERS` in `parts.py`.
Die Beispiel-Betriebe im Film (Tischlerei Brandt und ihre Kunden) sind erfunden; die Kennzahlen von RechnungsRadar sind echt.
