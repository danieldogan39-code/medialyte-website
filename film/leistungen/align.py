import json, sys, subprocess, numpy as np
from faster_whisper import WhisperModel
m = WhisperModel('small', device='cpu', compute_type='int8', cpu_threads=2)
for name in sys.argv[1:]:
    raw = subprocess.run(["ffmpeg","-v","error","-i",f"audio/{name}.mp3","-f","f32le","-ac","1","-ar","16000","-"], capture_output=True).stdout
    audio = np.frombuffer(raw, np.float32)
    segs, info = m.transcribe(audio, language="de", word_timestamps=True, beam_size=5, vad_filter=False,
                              initial_prompt="Medialyte, Sophia, KI-Agent, WhatsApp, Kanzlei, Zielgruppe.")
    words, text = [], []
    for s in segs:
        text.append(s.text.strip())
        for w in s.words:
            words.append({"w": w.word.strip(), "s": round(w.start, 3), "e": round(w.end, 3), "p": round(w.probability, 3)})
    json.dump({"text": " ".join(text), "words": words}, open(f"audio/{name}.words.json", "w"), ensure_ascii=False, indent=0)
    print("==", name, round(len(audio)/16000,2), flush=True); print(" ".join(text)); print("unsicher:", [(x["w"], x["s"], x["p"]) for x in words if x["p"] < 0.5], flush=True)
