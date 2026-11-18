"""Erzeugt die Vorschaubilder für geteilte Links (Open Graph, 1200 x 630) mit Chromium.

og.jpg           – alle Seiten ohne eigenes Bild
og-check.jpg     – /website-check/
og-termin.jpg    – /termin/ (Erstgespräch)
og-ratgeber.jpg  – /ratgeber/ und alle Artikel (Zeitschrift statt Angebot)

WhatsApp zeigt in der kleinen Vorschau nur das mittlere Quadrat (x 285–915).
Alles Wichtige steht deshalb dort; links und rechts nur Beiwerk für die breite Vorschau.
Aufruf: python3 tools/og_images.py
"""
import asyncio
import base64
from pathlib import Path
from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "src/assets/img"


def font(p):
    return "data:font/woff2;base64," + base64.b64encode((ROOT / p).read_bytes()).decode()


LOGO = (ROOT / "tools/logo-inline.svg").read_text().replace("<svg ", '<svg class="mono" ', 1)
WORD = (ROOT / "tools/wordmark.svg").read_text()

BASE = """<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:Outfit;src:url('%OUTFIT%') format('woff2');font-weight:100 900}
@font-face{font-family:Fraunces;src:url('%FR9%') format('woff2');font-weight:900}
@font-face{font-family:Fraunces;src:url('%FR6%') format('woff2');font-weight:600}
@font-face{font-family:Fraunces;src:url('%FR6I%') format('woff2');font-weight:600;font-style:italic}
*{margin:0;padding:0;box-sizing:border-box}
body{width:1200px;height:630px;background:#0E192A;font-family:Outfit,sans-serif;color:#F3F5F9;position:relative;overflow:hidden}
.glow{position:absolute;left:50%;top:-560px;width:1600px;height:1060px;margin-left:-800px;border-radius:50%;background:radial-gradient(closest-side,rgba(64,98,158,.55),rgba(40,64,108,.18) 50%,transparent 74%)}
.grid{position:absolute;inset:0;background-image:linear-gradient(rgba(170,190,220,.055) 1px,transparent 1px),linear-gradient(90deg,rgba(170,190,220,.055) 1px,transparent 1px);background-size:70px 70px;background-position:-5px 0;-webkit-mask-image:radial-gradient(60% 75% at 50% 40%,#000,transparent 85%)}
.brand{display:flex;align-items:center;justify-content:center;gap:11px}
.brand .mono{height:36px;width:auto;color:#FF5757}
.brand .wordmark{height:26px;width:auto;color:#F3F5F9;margin-top:4px}
.mid{position:absolute;left:285px;width:630px;top:0;bottom:0;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center}
%CSS%
</style></head><body><div class="glow"></div><div class="grid"></div>%BODY%</body></html>"""

# ---------- Allgemein ----------
GEN_CSS = """
.mid{gap:34px}
.mid .brand .mono{height:58px}.mid .brand .wordmark{height:42px;margin-top:6px}
h1{font-size:62px;line-height:1.02;font-weight:600;letter-spacing:-.045em}
h1 span{display:block;color:#8A9BB4}
.tags{display:flex;gap:10px;font-size:19px;color:#C3CDDC}
.tags b{font-weight:500;padding:8px 16px;border-radius:999px;border:1px solid rgba(170,190,220,.24)}
.side{position:absolute;top:150px;width:220px;height:330px;border-radius:20px;background:linear-gradient(180deg,rgba(26,42,69,.9),rgba(20,34,58,.35));border:1px solid rgba(170,190,220,.12)}
.side i{position:absolute;left:22px;right:22px;height:12px;border-radius:6px;background:rgba(170,190,220,.12)}
.side.l{left:-60px;transform:rotate(-6deg)}.side.r{right:-60px;transform:rotate(6deg)}
.side .k{height:120px;top:24px;border-radius:12px;background:linear-gradient(135deg,rgba(255,87,87,.35),rgba(64,98,158,.3))}
"""
GEN = """<div class="side l"><i class="k"></i><i style="top:168px;right:60px"></i><i style="top:192px"></i><i style="top:216px;right:90px"></i><i style="top:262px;width:90px;height:30px;border-radius:15px;background:rgba(255,87,87,.45)"></i></div>
<div class="side r"><i class="k" style="background:linear-gradient(135deg,rgba(61,214,140,.3),rgba(64,98,158,.3))"></i><i style="top:168px"></i><i style="top:192px;right:70px"></i><i style="top:216px"></i><i style="top:262px;width:90px;height:30px;border-radius:15px;background:rgba(170,190,220,.2)"></i></div>
<div class="mid"><div class="brand">%LOGO%%WORD%</div>
<h1>Ihre Website soll<br>Kunden bringen. <span>Nicht Arbeit machen.</span></h1>
<div class="tags"><b>Website</b><b>Kunden&shy;management</b><b>KI-Agent</b><b>Werbung</b></div></div>"""

# ---------- Website-Check ----------
CHECK_CSS = """
.mid{gap:0}
.pill{display:inline-flex;align-items:center;gap:8px;padding:8px 16px;border-radius:999px;background:rgba(245,185,66,.12);box-shadow:inset 0 0 0 1px rgba(245,185,66,.38);color:#F7C65E;font-size:20px;font-weight:600}
.pill svg{width:18px;height:18px}
.ring{position:relative;width:212px;height:212px;margin:26px 0 22px}
.ring svg{width:212px;height:212px;transform:rotate(-90deg)}
.ring b{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;font-size:76px;font-weight:600;letter-spacing:-.04em;line-height:1}
.ring b small{font-size:18px;font-weight:500;color:#8A9BB4;letter-spacing:0;margin-top:6px}
h1{font-size:60px;line-height:1;font-weight:600;letter-spacing:-.045em}
p{font-size:23px;color:#C3CDDC;margin-top:14px}
.foot{margin-top:26px}
.card{position:absolute;top:130px;width:230px;padding:22px;border-radius:20px;background:rgba(20,34,58,.85);border:1px solid rgba(170,190,220,.14)}
.card.l{left:22px;transform:rotate(-4deg)}.card.r{right:22px;transform:rotate(4deg)}
.met{margin-bottom:20px;font-size:17px;color:#C3CDDC}.met:last-child{margin-bottom:0}
.met div{display:flex;justify-content:space-between;margin-bottom:8px}.met div b{color:#F3F5F9;font-weight:600}
.bar{height:8px;border-radius:4px;background:rgba(170,190,220,.14);overflow:hidden}.bar i{display:block;height:100%;border-radius:4px;background:#3DD68C}
.mini{display:grid;grid-template-columns:1fr 1fr;gap:18px 10px;text-align:center;font-size:15px;color:#C3CDDC}
.mini span{display:block;width:74px;height:74px;margin:0 auto 8px;border-radius:50%;display:grid;place-items:center;font-size:24px;font-weight:600;color:#F3F5F9;background:radial-gradient(closest-side,#14223A 78%,transparent 80% 100%),conic-gradient(#3DD68C var(--p),rgba(170,190,220,.16) 0)}
"""
BOLT = '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M13 2 4 14h7l-1 8 9-12h-7z"/></svg>'
CHECK = """<div class="card l">
<div class="met"><div>Ladezeit<b>1,6 s</b></div><div class="bar"><i style="width:82%"></i></div></div>
<div class="met"><div>Stabilität<b>0,02</b></div><div class="bar"><i style="width:94%"></i></div></div>
<div class="met"><div>Reaktion<b>90 ms</b></div><div class="bar"><i style="width:88%"></i></div></div>
<div class="met"><div>Erster Inhalt<b>1,1 s</b></div><div class="bar"><i style="width:86%"></i></div></div></div>
<div class="card r"><div class="mini">
<div><span style="--p:93%">93</span>Ladezeit</div><div><span style="--p:100%">100</span>Barriere&shy;freiheit</div>
<div><span style="--p:96%">96</span>Technik</div><div><span style="--p:100%">100</span>Google</div></div></div>
<div class="mid"><div class="pill">%BOLT%Kostenlos</div>
<div class="ring"><svg viewBox="0 0 120 120"><circle cx="60" cy="60" r="52" fill="none" stroke="rgba(170,190,220,.14)" stroke-width="9"/><circle cx="60" cy="60" r="52" fill="none" stroke="#3DD68C" stroke-width="9" stroke-linecap="round" stroke-dasharray="326.7" stroke-dashoffset="19.6"/></svg><b>94<small>von 100</small></b></div>
<h1>Website-Check</h1>
<p>Ladezeit, Handy und Google<br>in unter einer Minute geprüft</p>
<div class="foot brand">%LOGO%%WORD%</div></div>"""

# ---------- Erstgespräch ----------
TERMIN_CSS = """
.mid{gap:0}
h1{font-size:60px;line-height:1;font-weight:600;letter-spacing:-.045em;margin-top:30px}
h1 span{color:#8A9BB4}
.cal{margin-top:30px;width:560px;padding:22px;border-radius:24px;background:rgba(20,34,58,.92);border:1px solid rgba(170,190,220,.16);box-shadow:0 30px 60px -30px rgba(0,0,0,.7)}
.days{display:grid;grid-template-columns:repeat(5,1fr);gap:8px;margin-bottom:16px}
.days div{padding:10px 0;border-radius:14px;font-size:15px;color:#8A9BB4;border:1px solid rgba(170,190,220,.12)}
.days div b{display:block;font-size:24px;color:#F3F5F9;font-weight:600;margin-top:2px}
.days .on{background:#F44C4C;border-color:#F44C4C;color:rgba(255,255,255,.8)}
.days .on b{color:#fff}
.slots{display:grid;grid-template-columns:repeat(4,1fr);gap:8px}
.slots div{padding:11px 0;border-radius:12px;background:rgba(170,190,220,.07);font-size:19px;font-weight:500;color:#C3CDDC;font-variant-numeric:tabular-nums}
.slots .on{background:rgba(255,87,87,.16);box-shadow:inset 0 0 0 1.5px #FF6E6E;color:#fff}
.ways{display:flex;justify-content:center;gap:12px;margin-top:24px;font-size:19px;color:#C3CDDC}
.ways span{display:inline-flex;align-items:center;gap:8px}
.ways svg{width:20px;height:20px;color:#8A9BB4}
.bub{position:absolute;top:180px;display:flex;align-items:center;gap:14px;padding:16px 20px;border-radius:20px;background:rgba(20,34,58,.85);border:1px solid rgba(170,190,220,.14);font-size:18px;color:#C3CDDC;text-align:left;line-height:1.3}
.bub b{display:block;color:#F3F5F9;font-weight:600}
.bub i{width:46px;height:46px;border-radius:12px;display:grid;place-items:center;flex:none}
.bub svg{width:24px;height:24px}
.bub.l{left:-24px;transform:rotate(-4deg)}.bub.r{right:14px;top:330px;transform:rotate(4deg)}
"""
I_VID = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2.5" y="6" width="13" height="12" rx="2.5"/><path d="m15.5 10.5 6-3.5v10l-6-3.5"/></svg>'
I_TEL = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 3h4l2 5-2.5 1.5a11 11 0 0 0 6 6L16 13l5 2v4a2 2 0 0 1-2 2A17 17 0 0 1 3 5a2 2 0 0 1 2-2z"/></svg>'
I_PIN = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 21s-7-6.2-7-11.5a7 7 0 0 1 14 0C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/></svg>'
I_OK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>'
TERMIN = """<div class="bub l"><i style="background:rgba(61,214,140,.16);color:#3DD68C">%OK%</i><div><b>Termin bestätigt</b>Sie erhalten eine E-Mail</div></div>
<div class="bub r"><i style="background:rgba(255,87,87,.16);color:#FF6E6E">%VID%</i><div><b>Ihr Anliegen</b>Website, Werbung, KI</div></div>
<div class="mid"><div class="brand">%LOGO%%WORD%</div>
<h1>Erstgespräch <span>buchen</span></h1>
<div class="cal"><div class="days"><div>Mo<b>16</b></div><div>Di<b>17</b></div><div class="on">Mi<b>18</b></div><div>Do<b>19</b></div><div>Fr<b>20</b></div></div>
<div class="slots"><div>09:30</div><div class="on">11:00</div><div>14:00</div><div>16:30</div></div></div>
<div class="ways"><span>%VID%Video-Call</span><span>%TEL%Telefon</span><span>%PIN%vor Ort</span></div></div>"""

# ---------- Ratgeber: Zeitschrift ----------
RAT_CSS = """
body{background:#0A1220}
.glow{background:radial-gradient(closest-side,rgba(64,98,158,.45),rgba(40,64,108,.15) 50%,transparent 74%)}
.mag{position:absolute;top:38px;left:50%;width:412px;height:556px;margin-left:-206px;border-radius:6px;overflow:hidden;box-shadow:0 40px 80px -30px rgba(0,0,0,.85),0 0 0 1px rgba(0,0,0,.2)}
.mag.back{width:380px;height:512px;top:70px;margin-left:-190px;filter:brightness(.62) saturate(.9)}
.mag.b1{transform:translateX(-330px) rotate(-7deg)}
.mag.b2{transform:translateX(330px) rotate(7deg)}
.paper{background:#F6F4EF;color:#0E192A}
.cov{position:absolute;inset:0;padding:24px 26px;display:flex;flex-direction:column}
.top{display:flex;justify-content:space-between;align-items:center;font-size:13px;font-weight:600;letter-spacing:.02em}
.top .brand{gap:7px}.top .brand .mono{height:20px}.top .brand .wordmark{height:14px;color:#0E192A;margin-top:2px}
.mast{font-family:Fraunces,serif;font-weight:900;font-size:80px;line-height:.9;letter-spacing:-.035em;margin-top:12px}
.sub{font-size:14px;font-weight:500;color:#4A5B74;margin-top:8px;padding-bottom:12px;border-bottom:2px solid #0E192A}
.art{position:relative;height:178px;margin:16px 0 14px;border-radius:4px;overflow:hidden;background:#0E192A}
.art .c1{position:absolute;width:170px;height:170px;border-radius:50%;background:#FF5757;left:44px;top:34px}
.art .c2{position:absolute;width:150px;height:150px;border-radius:50%;background:#3A568A;right:52px;top:-12px;mix-blend-mode:screen}
.art .c3{position:absolute;left:0;right:0;bottom:0;height:46px;background:repeating-linear-gradient(90deg,rgba(243,245,249,.9) 0 2px,transparent 2px 14px);opacity:.25}
.art .vs{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);font-family:Fraunces,serif;font-style:italic;font-weight:600;font-size:40px;color:#F6F4EF}
.lead small{display:block;font-size:12.5px;font-weight:600;color:#E94343;letter-spacing:.02em;margin-bottom:4px}
.lead b{display:block;font-family:Fraunces,serif;font-weight:900;font-size:29px;text-wrap:balance;line-height:1.02;letter-spacing:-.02em}
.lines{margin-top:auto;display:grid;gap:9px}
.lines div{padding-right:66px;font-size:14.5px;line-height:1.25;font-weight:500;padding-top:9px;border-top:1px solid rgba(14,25,42,.16)}
.lines div b{font-weight:700}
.bc{position:absolute;right:26px;bottom:22px;width:54px;height:30px;background:repeating-linear-gradient(90deg,#0E192A 0 2px,transparent 2px 4px,#0E192A 4px 5px,transparent 5px 8px);opacity:.75}
.navy{background:#14223A;color:#F3F5F9}.navy .sub{color:#8A9BB4;border-color:#F3F5F9}.navy .top .wordmark{color:#F3F5F9}
.coral{background:#FF5757;color:#fff}.coral .sub{color:rgba(255,255,255,.8);border-color:#fff}.coral .top .wordmark{color:#fff}.coral .top .mono{color:#fff}
.blk{height:150px;margin-top:16px;border-radius:4px;background:rgba(255,255,255,.12)}
"""
RAT = """<div class="mag back b1 navy"><div class="cov"><div class="top"><span class="brand">%LOGO%%WORD%</span></div>
<div class="mast">Ratgeber</div><div class="sub">Werbung, die Anfragen bringt</div><div class="blk"></div>
<div class="lead" style="margin-top:14px"><b>Meta Ads erklärt</b></div></div></div>
<div class="mag back b2 coral"><div class="cov"><div class="top"><span class="brand">%LOGO%%WORD%</span></div>
<div class="mast">Ratgeber</div><div class="sub">Schnelle Websites</div><div class="blk"></div>
<div class="lead" style="margin-top:14px"><b>Core Web Vitals verständlich</b></div></div></div>
<div class="mag paper"><div class="cov">
<div class="top"><span class="brand">%LOGO%%WORD%</span><span>Wissen für Betriebe</span></div>
<div class="mast">Ratgeber</div>
<div class="sub">Websites, Google, Werbung und Kunden – verständlich erklärt</div>
<div class="art"><i class="c1"></i><i class="c2"></i><i class="c3"></i><span class="vs">oder</span></div>
<div class="lead"><small>Der Vergleich</small><b>Google Ads oder Meta Ads?</b></div>
<div class="lines">
<div><b>Barrierefreiheit:</b> Was das BFSG von Betrieben verlangt</div>
<div><b>Wenig Anfragen?</b> Sieben Ursachen, die man leicht übersieht</div>
</div></div><i class="bc"></i></div>"""


def page(css, body):
    h = BASE.replace("%CSS%", css).replace("%BODY%", body)
    for k, v in {"%OUTFIT%": font("src/assets/fonts/outfit-latin-wght-normal.woff2"),
                 "%FR9%": font("tools/fonts/fraunces-latin-900-normal.woff2"),
                 "%FR6%": font("tools/fonts/fraunces-latin-600-normal.woff2"),
                 "%FR6I%": font("tools/fonts/fraunces-latin-600-italic.woff2"),
                 "%LOGO%": LOGO, "%WORD%": WORD, "%BOLT%": BOLT, "%VID%": I_VID, "%TEL%": I_TEL,
                 "%PIN%": I_PIN, "%OK%": I_OK}.items():
        h = h.replace(k, v)
    return h


JOBS = [("og.jpg", GEN_CSS, GEN), ("og-check.jpg", CHECK_CSS, CHECK),
        ("og-termin.jpg", TERMIN_CSS, TERMIN), ("og-ratgeber.jpg", RAT_CSS, RAT)]


async def main(out=IMG):
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1200, "height": 630})
        for name, css, body in JOBS:
            await pg.set_content(page(css, body))
            await pg.evaluate("document.fonts.ready")
            await pg.wait_for_timeout(300)
            await pg.screenshot(path=str(Path(out) / name), type="jpeg", quality=88)
        await b.close()
    print("Vorschaubilder erstellt:", ", ".join(j[0] for j in JOBS))

if __name__ == "__main__":
    import sys
    asyncio.run(main(sys.argv[1] if len(sys.argv) > 1 else IMG))
