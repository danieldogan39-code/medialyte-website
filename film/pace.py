"""Sprechtempo eines Takes: Silben pro Sekunde (gesamt und reines Sprechen) und Zahl der langen Pausen.
python3 pace.py <take> [<take> ...]   liest audio/<take>.align.json (ElevenLabs) oder audio/<take>.words.json (Whisper)"""
import json, os, re, sys
def syl(t): return len(re.findall(r"[aeiouäöüy]+", t.lower().replace("48", "achtundvierzig").replace("200", "zweihundert").replace("230", "zweihundertdreißig").replace("%", "prozent")))
for name in sys.argv[1:]:
    if os.path.exists(f"audio/{name}.align.json"):
        W = [{"w": w["text"], "s": w["start"], "e": w["end"]} for w in json.load(open(f"audio/{name}.align.json"))["words"]
             if not w["text"].startswith(("<", "time=", "/>"))]
    else:
        W = json.load(open(f"audio/{name}.words.json"))["words"]
    sp = sum(w["e"] - w["s"] for w in W)
    gaps = [b["s"] - a["e"] for a, b in zip(W, W[1:])]
    tot = W[-1]["e"] - W[0]["s"]
    n = sum(syl(w["w"]) for w in W)
    long = [g for g in gaps if g > 0.3]
    print(f"{name}: Dauer {tot:5.1f}s, Silben {n}, Tempo gesamt {n/tot:4.2f}/s, reines Sprechen {n/sp:4.2f}/s, Pausen>0.3s: {len(long)} (Summe {sum(long):4.1f}s), Pausen>0.6s: {sum(1 for g in gaps if g>0.6)}")
