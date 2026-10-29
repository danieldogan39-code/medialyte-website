"""Musikplan: Aufbruch der Musik (erste volle Zählzeit, Quelle 39,965 s) fällt auf die Wende T1; der letzte Schlag
(Quelle 139,965 s) fällt auf das Logo kurz vor „Medialyte“ (cJ, auf einem Taktanfang des Rumpfs)."""
import json, re, sys
BEAT0, BEAT = 0.590, 0.625; BAR = 4 * BEAT; DOWN = BEAT0 + 63 * BEAT; FINAL = DOWN + 40 * BAR
TURN = {"1": ("deshalb", 1), "2": ("in", None), "3": ("heute", 1), "4": ("bei", 1)}
def norm(s): return re.sub(r"[^\wäöüß]", "", s.lower())
for n in sys.argv[1:]:
    T = json.load(open(f"f{n}/timing.json")); W = T["words"]
    w0, k0 = TURN[n]
    if n == "2":
        T1 = next(W[i]["s"] for i in range(len(W) - 2) if [norm(W[i + j]["w"]) for j in range(3)] == ["in", "ihrem", "system"])
    else:
        T1 = [w["s"] for w in W if norm(w["w"]) == w0][k0 - 1]
    tm = next(w["s"] for w in W if norm(w["w"]) == "medialyte")
    A = DOWN - (T1 - 0.01)
    downs = [T1 - 0.01 + k * BAR for k in range(0, 40)]
    beats = [T1 - 0.01 + k * BEAT for k in range(0, 160)]
    c = [d for d in downs if tm - 0.9 <= d <= tm + 0.25]
    cJ = min(c, key=lambda d: abs(d - (tm - 0.15))) if c else min(beats, key=lambda d: abs(d - (tm - 0.15)))
    src_at_cJ = cJ + A
    assert src_at_cJ < 119.0, src_at_cJ
    T["music"] = {"T1": round(T1, 3), "A": round(A, 4), "cJ": round(cJ, 4), "tMedialyte": tm, "downbeat": bool(c)}
    json.dump(T, open(f"f{n}/timing.json", "w"), ensure_ascii=False)
    print(n, T["music"], "Quelle bei cJ", round(src_at_cJ, 2))
