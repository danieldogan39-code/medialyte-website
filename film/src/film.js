/* Medialyte Erklärfilm v3 – Zeitleiste.
   Jede Bewegung hängt an einem Wort des Sprechers (timing.json). Gerendert wird Bild für Bild über window.__seek(t, ft):
   t ist der Abtastzeitpunkt (für Bewegungsunschärfe wird ein Bild mehrmals abgetastet), ft die Bildzeit, nach der sich
   Texte, Zähler, Klassen und Sichtbarkeit richten – so bleiben Ziffern und Buchstaben in jedem Bild scharf.
   Regeln: Szenen überblenden nie ineinander (Kamerafahrten, Wischen, Anschlussbewegungen), kein Dauer-Zoom,
   bewegt wird über transform und opacity, und jede Szene steht vor dem Wechsel mindestens 0,3 s still. */
(function () {
  "use strict";
  var TM = window.TM, DUR = TM.duration;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  /* ---------- Wörter in Masken legen (bewegte Schrift) ---------- */
  $$("[data-kt]").forEach(function (el) {
    el.innerHTML = el.textContent.trim().split(/\s+/).map(function (w) { return '<span class="w"><i>' + w + "</i></span>"; }).join(" ");
  });

  /* Layout-Modus: Endzustand einer Szene ansehen (?layout=scA) */
  var lay = (location.search + location.hash).match(/layout=(\w+)/);
  if (lay) { document.getElementById(lay[1]).style.visibility = "visible"; window.__ready = true; return; }

  /* Erst messen, wenn die Schrift geladen ist – sonst stimmen Breiten und Höhen nicht */
  Promise.all([document.fonts.load('620 100px "Outfit"'), document.fonts.load('500 20px "Outfit"'), document.fonts.load('700 20px "Outfit"')])
    .then(function () { return document.fonts.ready; }).then(build);
  function build() {

  /* ---------- Wortzeiten ---------- */
  var norm = function (s) { return String(s).toLowerCase().replace(/[.,!?:;„“"()–…%]/g, "").replace(/^-+/, "").trim(); };
  var WN = TM.words.map(function (w) { return norm(w.w); });
  function t(word, n, edge) {
    n = n || 1; edge = edge || "s";
    var c = 0, k = norm(word);
    for (var i = 0; i < WN.length; i++) if (WN[i] === k && ++c === n) return TM.words[i][edge];
    throw new Error("Wort fehlt: " + word + " #" + n);
  }
  function p(phrase, edge) {
    var ks = phrase.split(" ").map(norm);
    for (var i = 0; i + ks.length <= WN.length; i++) {
      var ok = true;
      for (var j = 0; j < ks.length; j++) if (WN[i + j] !== ks[j]) { ok = false; break; }
      if (ok) return edge === "e" ? TM.words[i + ks.length - 1].e : TM.words[i].s;
    }
    throw new Error("Wortfolge fehlt: " + phrase);
  }

  /* ---------- Werkzeuge ---------- */
  gsap.defaults({ ease: "power3.out", duration: 0.7, lazy: false });
  var tl = gsap.timeline({ paused: true });
  var D = [];                 /* Zustände nach Bildzeit: function(ft) */
  var SFX = [];               /* Geräusche: {name, at, gain, v, align} */
  function sfx(name, at, gain, v, dir) { SFX.push({ name: name, at: Math.round(at * 1000) / 1000, gain: gain || 0, v: v || 0, dir: dir || "c" }); }
  var stageR = $("#stage").getBoundingClientRect();
  function rect(el) { el = typeof el === "string" ? $(el) : el; var r = el.getBoundingClientRect(); return { x: r.left - stageR.left, y: r.top - stageR.top, w: r.width, h: r.height }; }
  function el$(x) { return typeof x === "string" ? $(x) : x; }

  function pick(list, ft) { var v = list[0][1]; for (var i = 0; i < list.length; i++) if (ft >= list[i][0]) v = list[i][1]; return v; }
  function vis(el, t0, t1) {
    el = el$(el);
    D.push(function (ft) { var v = (ft >= t0 && (t1 == null || ft < t1)) ? "visible" : "hidden"; if (el.style.visibility !== v) el.style.visibility = v; });
  }
  function text(el, list) { el = el$(el); D.push(function (ft) { var v = pick(list, ft); if (el.textContent !== v) el.textContent = v; }); }
  function cls(el, name, t0, t1) { el = el$(el); D.push(function (ft) { el.classList.toggle(name, ft >= t0 && (t1 == null || ft < t1)); }); }
  function typeText(el, s, t0, dur, tClear) {
    el = el$(el);
    D.push(function (ft) {
      var n = Math.max(0, Math.min(s.length, Math.floor((ft - t0) / dur * s.length + 1e-6)));
      var v = (ft < t0 || (tClear != null && ft >= tClear)) ? "" : s.slice(0, n);
      if (el.textContent !== v) el.textContent = v;
    });
  }
  function count(el, a, b, t0, dur, fmt, ease) {
    el = el$(el); var e = gsap.parseEase(ease || "power2.out");
    fmt = fmt || function (v) { return String(Math.round(v)); };
    D.push(function (ft) { var k = Math.max(0, Math.min(1, (ft - t0) / dur)); var v = fmt(a + (b - a) * e(k)); if (el.textContent !== v) el.textContent = v; });
  }
  function blink(el, t0, t1) {
    el = el$(el);
    D.push(function (ft) { var on = ft >= t0 && ft < t1 && Math.floor((ft - t0) / 0.53) % 2 === 0; el.style.opacity = on ? "1" : "0"; });
  }
  /* Element erscheint (Startzustand -> Endzustand aus dem CSS) */
  function pop(el, at, from, dur, ease) {
    el = el$(el);
    var f = Object.assign({ autoAlpha: 0, y: 30 }, from || {}), to = { autoAlpha: 1, duration: dur || 0.7, ease: ease || "power3.out" };
    ["x", "y", "xPercent", "yPercent", "rotation", "rotationX", "rotationY"].forEach(function (k) { if (k in f) to[k] = 0; });
    ["scale", "scaleX", "scaleY"].forEach(function (k) { if (k in f) to[k] = 1; });
    if (f.to) { Object.assign(to, f.to); delete f.to; }
    tl.fromTo(el, f, to, at);
    return el;
  }
  function leave(el, at, to, dur, ease) { tl.to(el$(el), Object.assign({ autoAlpha: 0, duration: dur || 0.4, ease: ease || "power2.in" }, to || {}), at); }
  /* bewegte Schrift: Wörter steigen aus ihrer Maske */
  function words(el) { return $$(".w > i", el$(el)); }
  function reveal(el, at, dur, stagger) {
    words(el).forEach(function (w, i) {
      var t0 = Array.isArray(at) ? at[i] : at + i * (stagger == null ? 0.07 : stagger);
      tl.fromTo(w, { yPercent: 140 }, { yPercent: 0, duration: dur || 0.75, ease: "power4.out" }, t0);
    });
  }
  function conceal(el, at, stagger, dur) {
    words(el).forEach(function (w, i) { tl.to(w, { yPercent: -140, duration: dur || 0.42, ease: "power3.in" }, at + i * (stagger == null ? 0.03 : stagger)); });
  }
  /* Element zieht seinen Platz auf; Höhe wird vorher gemessen (box: Innen- und Außenabstände [von, bis]) */
  function grow(el, at, dur, box, h) {
    el = el$(el); h = h || el.offsetHeight;
    var from = { height: 0, autoAlpha: 0 }, to = { height: h, autoAlpha: 1, duration: dur || 0.5, ease: "power2.out" };
    Object.keys(box || {}).forEach(function (k) { from[k] = box[k][0]; to[k] = box[k][1]; });
    tl.fromTo(el, from, to, at);
  }
  /* Farbwechsel eines Zustands (gewählt, aktiv, abgesprungen) weich statt hart */
  var MORPH = ["color", "backgroundColor", "borderColor"];
  function morph(owner, name, targets, at, dur) {
    owner = el$(owner); targets = (targets || [owner]).map(el$);
    var get = function (e) { var cs = getComputedStyle(e), o = {}; MORPH.forEach(function (k) { o[k] = cs[k]; }); return o; };
    var from = targets.map(get); owner.classList.add(name); var to = targets.map(get); owner.classList.remove(name);
    cls(owner, name, at);
    targets.forEach(function (e, k) { tl.fromTo(e, from[k], Object.assign({ duration: dur || 0.25, ease: "power1.out", immediateRender: false }, to[k]), at); });
  }
  function pulse(el, at, k, dur) { tl.fromTo(el$(el), { scale: 1 }, { scale: k || 1.06, duration: dur || 0.16, yoyo: true, repeat: 1, ease: "sine.inOut", immediateRender: false }, at); }
  /* Linie zeichnen (SVG) */
  function draw(path, at, dur, ease) {
    path = el$(path); var L = path.getTotalLength();
    path.style.strokeDasharray = L + " " + (L + 10);
    tl.fromTo(path, { strokeDashoffset: L }, { strokeDashoffset: 0, duration: dur || 0.6, ease: ease || "power2.inOut" }, at);
    return L;
  }
  /* Mauszeiger: Spitze auf (x, y) */
  function cursorTo(cur, at, x, y, dur) { tl.to(el$(cur), { x: x - 6, y: y - 4, duration: dur || 0.6, ease: "power3.inOut" }, at); }
  function click(cur, at) { tl.fromTo(el$(cur), { scale: 1 }, { scale: 0.86, duration: 0.09, yoyo: true, repeat: 1, ease: "power1.inOut", immediateRender: false, transformOrigin: "6px 4px" }, at); sfx("click", at, -12, 0); }

  /* ---------- Kamera: Fahrt zur nächsten Szene (Punktraster zieht langsamer mit) ---------- */
  var grid = $("#grid"), cam = { x: 0, y: 0 }, PANS = 0, GK = 0.3;
  function pan(at, dur, dx, dy, outs, ins) {
    outs.forEach(function (s) { tl.fromTo(el$(s), { x: 0, y: 0 }, { x: -dx, y: -dy, duration: dur, ease: "power3.inOut", immediateRender: false }, at); });
    ins.forEach(function (s) { tl.fromTo(el$(s), { x: dx, y: dy }, { x: 0, y: 0, duration: dur, ease: "power3.inOut", immediateRender: false }, at); });
    var from = (-cam.x * GK) + "px " + (-cam.y * GK) + "px";
    cam.x += dx; cam.y += dy;
    tl.fromTo(grid, { backgroundPosition: from }, { backgroundPosition: (-cam.x * GK) + "px " + (-cam.y * GK) + "px", duration: dur, ease: "power3.inOut", immediateRender: false }, at);
    sfx("whoosh", at + dur * 0.5, dx ? -15 : -16, PANS++ % 2, dx ? "rl" : "c");
  }
  var PH = 1.0, PV = 0.9;   /* Dauer waagerechter und senkrechter Fahrten */

  /* ---------- Szenengrenzen (alle an Wörtern) ---------- */
  var B = {};
  B.AB = t("jahr", 1, "e") - 0.02;                    /* Fahrt A -> B */
  B.Bout = p("genau hier") - 0.95;                    /* Tagesplan sinkt weg */
  B.C = p("genau hier") - 0.32;
  B.Cout = p("am anfang") - 0.33;                     /* Logo fliegt in die Buchungskarte */
  B.D12 = p("innerhalb") - 0.3;                      /* Fahrt D1 -> D2 */
  B.D2E = p("dann lernen") - 0.48;                    /* Fahrt nach oben */
  B.flip = p("dahinter") - 0.16;
  B.EF = p("das alles") - 0.58;                       /* Dashboard wird zur Kachel */
  B.FG = p("aus über") - 0.55;
  B.GH = p("bei rechnungsradar") - 0.52;
  B.HI = p("und wenn sich") - 0.5;
  B.IJ = p("schreiben sie") - 0.5;
  B.JK = p("bei umfangreichen") - 0.27;
  B.Kout = t("medialyte") - 0.6;
  B.L = t("medialyte") - 0.2;

  /* Sichtbarkeit der Szenen */
  vis("#scA", 0, B.AB + PH);
  vis("#scB", B.AB, B.Bout + 0.7);
  vis("#scC", B.C - 0.05, B.Cout + 1.2);
  vis("#scD1", B.Cout, B.D12 + PH);
  vis("#scD2", B.D12, B.D2E + PV);
  vis("#scE", B.D2E, B.FG + PH);
  vis("#scF", B.EF, B.FG + PH);
  vis("#scG", B.FG, B.GH + PV);
  vis("#scH", B.GH, B.HI + PH);
  vis("#scI", B.HI, B.IJ + PV);
  vis("#scJ", B.IJ, B.JK + PH);
  vis("#scK", B.JK, B.Kout + 0.5);
  vis("#scL", B.L, null);

  /* ---------- Hintergrund: Licht wandert langsam ---------- */
  tl.fromTo("#lt1", { x: 0, y: 0 }, { x: 240, y: 160, duration: DUR, ease: "sine.inOut" }, 0);
  tl.fromTo("#lt2", { x: 0, y: 0 }, { x: -260, y: -140, duration: DUR, ease: "sine.inOut" }, 0);

  /* ---------- Kapitelanzeige ---------- */
  (function () {
    var chap = $("#chap"), CH = [[0.5, "1", "Die Ausgangslage"], [B.C + 0.55, "2", "Unser Ablauf"], [B.EF + 0.8, "3", "Der Unterschied"], [B.HI + 0.95, "4", "Ihr KI-Agent"]];
    text($("#chapN"), CH.map(function (c) { return [c[0] - 0.01, c[1]]; }));
    text($("#chapT"), CH.map(function (c) { return [c[0] - 0.01, c[2]]; }));
    vis(chap, 0.45, null);
    CH.forEach(function (c, i) {
      var a = c[0], b = a + 4.1;
      tl.fromTo(chap, { opacity: 0, x: -18 }, { opacity: 1, x: 0, duration: 0.6, ease: "power3.out", immediateRender: i === 0 }, a);
      if (i > 0) tl.set("#chapB", { scaleX: 0 }, a - 0.05);
      tl.fromTo("#chapB", { scaleX: 0 }, { scaleX: 1, duration: 3.4, ease: "power1.inOut", immediateRender: i === 0 }, a + 0.15);
      tl.to(chap, { opacity: 0, x: -18, duration: 0.45, ease: "power2.in" }, b);
    });
  })();

  /* =================================================================== A · Suche, Besuch, Absprung, Mängel */
  (function () {
    var ph = $("#ph1"), scr = rect("#ph1s"), ss = rect("#scrSearch"), hit = rect("#hit");
    var tap = $("#tap");
    tap.style.left = (hit.x - ss.x + hit.w * 0.46) + "px"; tap.style.top = (hit.y - ss.y + hit.h * 0.42) + "px";
    /* Markierungen an den echten Stellen der alten Seite (Bildschirmkoordinaten) */
    var W = scr.w;
    function box(sel, it, ib, ol, orr) {
      var r = rect(sel), l = Math.max(10, r.x - scr.x - ol), rr = Math.min(W - 26, r.x - scr.x + r.w + orr);
      return { l: l, t: r.y - scr.y + it, w: rr - l, h: r.h - it - ib };
    }
    var MB = [box("#oldTop", 8, 7, 0, 0), box("#oldNav", 3, 3, 0, 0), box("#oldHours", -7, -7, 7, 7)];
    MB.forEach(function (m, i) { Object.assign($("#mk" + (i + 1)).style, { left: m.l + "px", top: m.t + "px", width: m.w + "px", height: m.h + "px" }); });
    /* Führungslinien: vom Ende der Überschrift zur linken Kante der Markierung */
    var LD = [1, 2, 3].map(function (i) {
      var ws = $$("#co" + i + " b .w"), last = rect(ws[ws.length - 1]), b = rect("#co" + i + " b"), m = MB[i - 1];
      var x0 = last.x + last.w + 26, y0 = b.y + b.h * 0.5, x1 = scr.x + m.l - 3, y1 = scr.y + m.t + m.h / 2, xm = Math.max(x0 + 20, x1 - 200);
      $("#ld" + i).setAttribute("d", "M" + x0 + " " + y0 + " L" + xm + " " + y0 + " L" + x1 + " " + y1);
      $("#ls" + i).setAttribute("cx", x0); $("#ls" + i).setAttribute("cy", y0);
      $("#le" + i).setAttribute("cx", x1); $("#le" + i).setAttribute("cy", y1);
      return { x0: x0, y0: y0 };
    });

    /* Telefon kommt */
    tl.fromTo(ph, { y: 170, autoAlpha: 0 }, { y: 0, autoAlpha: 1, duration: 1.35, ease: "power3.out" }, 0.1);
    tl.fromTo("#glowA", { autoAlpha: 0, scale: 0.85 }, { autoAlpha: 1, scale: 1, duration: 1.8, ease: "power2.out" }, 0.15);
    sfx("swoosh", 0.32, -19, 0);
    /* Suche wird getippt */
    var q0 = t("jemand") + 0.02, q1 = t("anbieten") - 0.2;
    typeText("#q", "Tischlerei in der Nähe", q0, q1 - q0);
    blink("#caret1", 0.7, q1 + 0.75);
    sfx("typing", q0, -23, 0);
    pop("#sugg", q0 + 0.42, { y: -8 }, 0.35, "power2.out");
    leave("#sugg", q1 - 0.02, { y: -6 }, 0.18, "power1.in");
    $$(".res li").forEach(function (li, i) { pop(li, q1 + 0.1 + i * 0.1, { y: 22 }, 0.55); });
    sfx("blips", q1 + 0.1, -24, 1);
    var L = $$("#ktA .ln");
    reveal(L[0], t("sucht") - 0.05);
    /* Antippen und laden */
    var tapT = t("findet") - 0.1;
    tl.fromTo(tap, { autoAlpha: 0, scale: 0.4 }, { autoAlpha: 1, scale: 1.15, duration: 0.2, ease: "power2.out" }, tapT);
    tl.to(tap, { autoAlpha: 0, scale: 1.45, duration: 0.32, ease: "power1.out" }, tapT + 0.2);
    tl.fromTo("#hit", { backgroundColor: "rgb(255,255,255)" }, { backgroundColor: "rgb(228,235,247)", duration: 0.14, ease: "none", immediateRender: false }, tapT);
    sfx("tap", tapT, -11, 0);
    reveal(L[1], t("findet") - 0.02);
    var ld = tapT + 0.24, shown = t("website", 1, "e") - 0.06;
    tl.fromTo("#scrLoad", { autoAlpha: 0, x: 430 }, { autoAlpha: 1, x: 0, duration: 0.42, ease: "power3.out" }, ld);
    tl.fromTo("#loadbar", { scaleX: 0 }, { scaleX: 0.86, duration: shown - ld, ease: "power1.out" }, ld);
    tl.fromTo("#spin", { rotation: 0 }, { rotation: 560, duration: shown - ld + 0.3, ease: "none" }, ld);
    tl.fromTo("#scrOld", { autoAlpha: 0 }, { autoAlpha: 1, duration: 0.24, ease: "power1.out" }, shown);
    tl.to("#scrLoad", { autoAlpha: 0, duration: 0.05, ease: "none" }, shown + 0.3);
    sfx("pop", shown, -22, 0);
    /* Besucher sieht sich um … */
    tl.fromTo("#old", { y: 0 }, { y: -160, duration: 1.75, ease: "power2.inOut" }, shown + 0.35);
    pop("#visit", ld + 0.08, { y: 34 }, 0.7);
    var gone = t("weg");
    count("#tm", 0, 4, ld, gone - ld, function (v) { return "0:0" + Math.min(4, Math.floor(v)); }, "none");
    text("#vstx", [[0, "Seite lädt"], [shown, "Sieht sich um"], [gone, "Abgesprungen"]]);
    morph("#vst", "is-gone", ["#vst", "#vstDot"], gone, 0.25);
    pulse("#vst", gone, 1.07);
    /* … und ist wieder weg */
    reveal(L[2], t("wieder") + 0.05, 0.6, 0.09);
    sfx("swoosh", gone - 0.02, -17, 1);
    /* Blick auf die Mängel: Schrift geht, Seite scrollt nach oben */
    var an = Math.max(gone + 0.48, t("veraltet") - 0.5);
    L.forEach(function (l, i) { conceal(l, an + i * 0.05, 0.03, 0.4); });
    leave("#visit", an + 0.12, { y: 24 }, 0.38);
    tl.to("#old", { y: 0, duration: 0.75, ease: "power2.inOut" }, an - 0.05);
    var hits = [t("veraltet"), t("handy"), t("öffnungszeiten", 1)];
    [1, 2, 3].forEach(function (i) {
      var h = hits[i - 1];
      pop("#co" + i + " .num", h - 0.08, { scale: 0.4, y: 0 }, 0.45, "back.out(2)");
      reveal("#co" + i + " b", h - 0.04, 0.7, 0.06);
      pop("#co" + i + " small", h + 0.22, { y: 14 }, 0.55);
      tl.fromTo("#ls" + i, { autoAlpha: 0, scale: 0 }, { autoAlpha: 1, scale: 1, duration: 0.25, ease: "power2.out", transformOrigin: "50% 50%" }, h + 0.12);
      draw("#ld" + i, h + 0.16, 0.5);
      tl.fromTo("#le" + i, { autoAlpha: 0, scale: 0 }, { autoAlpha: 1, scale: 1, duration: 0.3, ease: "back.out(2.5)", transformOrigin: "50% 50%" }, h + 0.6);
      tl.fromTo("#mk" + i, { autoAlpha: 0, scale: 1.08 }, { autoAlpha: 1, scale: 1, duration: 0.4, ease: "power3.out" }, h + 0.6);
      sfx("pop", h - 0.06, -17, i);
    });
    pan(B.AB, PH, 1920, 0, ["#scA"], ["#scB"]);
  })();

  /* =================================================================== B · Anfragen verteilen sich und gehen unter */
  (function () {
    var cards = ["#n1", "#n2", "#n3", "#n4", "#n5", "#n6", "#n7", "#n8", "#n9"].map(el$);
    cards.forEach(function (c) { gsap.set(c, { rotation: +c.getAttribute("data-r") }); });
    /* n1 und n2 kommen mit der Kamerafahrt, die übrigen fallen nacheinander ein */
    var times = { n5: t("anfragen", 1) + 0.02, n4: t("trotzdem") - 0.02, n3: t("kommen") - 0.02,
      n6: t("verteilen") - 0.05, n7: t("verteilen") + 0.2, n8: t("sich", 1) + 0.12, n9: t("auf", 2) + 0.12 };
    Object.keys(times).forEach(function (id, i) {
      var c = $("#" + id), r = +c.getAttribute("data-r");
      pop(c, times[id], { y: -46, scale: 0.94, rotation: r - 7, to: { rotation: r } }, 0.6, "back.out(1.4)");
      sfx("ping", times[id] + 0.03, -24 - (i % 3), i % 4);
    });
    /* Kanäle zählen mit */
    var ch = [["#chTel", "#nTel", 3, "telefon", [3, 7]], ["#chMail", "#nMail", 14, "e-mail", [2, 5, 9]], ["#chWa", "#nWa", 6, "whatsapp", [4, 8]]];
    ch.forEach(function (c) {
      var at = t(c[3], 1);
      count(c[1], 0, c[2], at - 0.05, 0.6, null, "power1.out");
      pulse(c[0], at - 0.02, 1.06, 0.18);
      c[4].forEach(function (n, k) { pulse("#n" + n, at + k * 0.06, 1.035, 0.16); });
      sfx("blips", at, -25, 2);
    });
    /* … und gehen im Alltag unter */
    var g = p("und gehen");
    tl.set("#planner", { autoAlpha: 0 }, 0); tl.set("#planner", { autoAlpha: 1 }, g - 0.15);
    tl.fromTo("#planner", { y: 960 }, { y: 0, duration: 0.95, ease: "power3.out" }, g - 0.15);
    $$("#planner .slot").forEach(function (s, i) { pop(s, g + 0.25 + i * 0.07, { y: 18 }, 0.5); });
    sfx("paper", g - 0.05, -17, 0);
    cards.forEach(function (c, i) {
      tl.to(c, { y: "+=120", autoAlpha: 0.28, duration: 1.0, ease: "power2.in" }, t("gehen") + i * 0.025);
      tl.fromTo(c, { filter: "blur(0px)" }, { filter: "blur(4px)", duration: 1.0, ease: "power2.in", immediateRender: false }, t("gehen") + i * 0.025);
    });
    tl.to("#chans", { y: -24, autoAlpha: 0.3, duration: 0.8, ease: "power2.in" }, t("gehen") + 0.1);
    /* alles sinkt weg – Bühne frei für die Wende */
    var o = B.Bout;
    cards.forEach(function (c) { tl.to(c, { y: "+=420", autoAlpha: 0, duration: 0.5, ease: "power2.in" }, o - 0.05); });
    leave("#chans", o - 0.05, { y: -60 }, 0.4);
    tl.to("#planner", { y: 1000, duration: 0.6, ease: "power3.in" }, o);
    sfx("riser", p("genau hier") - 0.02, -14, 0);
  })();

  /* =================================================================== C · Wende */
  (function () {
    var at = B.C;
    tl.fromTo("#lt3", { autoAlpha: 0, scale: 0.8 }, { autoAlpha: 1, scale: 1, duration: 1.0, ease: "power2.out" }, at);
    tl.to("#lt3", { autoAlpha: 0, duration: 1.0, ease: "power1.inOut" }, B.Cout + 0.2);
    pop("#turnMk", at, { y: 0, scale: 0.82 }, 0.9, "power3.out");
    tl.fromTo("#sweep", { x: 0, autoAlpha: 1 }, { x: 3000, duration: 1.3, ease: "power2.inOut" }, at + 0.15);
    var ws = [t("genau", 2), t("hier", 1), t("setzen"), t("wir", 1), t("an")].map(function (x) { return x - 0.06; });
    var all = words("#turnHl");
    all.forEach(function (w, i) { tl.fromTo(w, { yPercent: 140 }, { yPercent: 0, duration: 0.6, ease: "power4.out" }, ws[i]); });
    sfx("impact", t("genau", 2) - 0.01, -10, 0);
    /* Ausgang: Wörter fallen, das Logo fliegt in die Buchungskarte */
    all.forEach(function (w, i) { tl.to(w, { yPercent: 140, duration: 0.3, ease: "power3.in" }, B.Cout + i * 0.02); });
  })();

  /* =================================================================== D1 · Erstgespräch */
  (function () {
    var mk = rect("#turnMk svg"), av = rect("#bkMk svg"), day = rect("#day"), slot = rect("#slot");
    var o = B.Cout;
    /* Logo fliegt vom Wende-Bild an seinen Platz in der Karte */
    var dx = (av.x + av.w / 2) - (mk.x + mk.w / 2), dy = (av.y + av.h / 2) - (mk.y + mk.h / 2), k = av.w / mk.w;
    tl.to("#turnMk", { x: dx, y: dy, scale: k, duration: 0.95, ease: "power3.inOut" }, o + 0.08);
    sfx("swoosh", o + 0.45, -16, 2);
    var land = o + 1.03;
    tl.set("#turnMk", { autoAlpha: 0 }, land);
    tl.fromTo("#bkMk", { autoAlpha: 0 }, { autoAlpha: 1, duration: 0.01, ease: "none" }, land - 0.01);
    pop("#bk", o + 0.38, { y: 70 }, 0.7, "power3.out");
    tl.fromTo("#bkAv", { backgroundColor: "rgba(255,87,87,0)", borderColor: "rgba(255,87,87,0)" }, { backgroundColor: "rgba(255,87,87,0.16)", borderColor: "rgba(255,87,87,0.42)", duration: 0.4, ease: "power1.out" }, land - 0.1);
    /* rechte Spalte */
    reveal($$("#d1 .ln")[0], t("kostenfreies", 1) - 0.06);
    reveal($$("#d1 .ln")[1], t("erstgespräch", 1) - 0.06);
    pop("#d1sub", t("erstgespräch", 1) + 0.25, { y: 18 }, 0.6);
    pop("#d1chips", t("erstgespräch", 1) + 0.4, { y: 16 }, 0.5);
    /* Termin wird gewählt */
    var cur = "#cur1", c0 = t("steht", 1) - 0.1;
    tl.set(cur, { x: 1010, y: 900 }, 0);
    tl.fromTo(cur, { autoAlpha: 0 }, { autoAlpha: 1, duration: 0.3, ease: "power1.out" }, c0);
    var dT = t("kostenfreies", 1) - 0.02, sT = t("erstgespräch", 1) + 0.05;
    cursorTo(cur, c0, day.x + day.w * 0.55, day.y + day.h * 0.58, dT - c0 - 0.06);
    click(cur, dT); morph("#day", "sel", null, dT + 0.04, 0.2);
    cursorTo(cur, dT + 0.25, slot.x + slot.w * 0.55, slot.y + slot.h * 0.58, sT - dT - 0.32);
    click(cur, sT); morph("#slot", "sel", null, sT + 0.04, 0.2);
    tl.to(cur, { x: "+=80", y: "+=120", autoAlpha: 0, duration: 0.5, ease: "power2.in" }, sT + 0.35);
    grow("#bkok", sT + 0.28, 0.45);
    sfx("success", sT + 0.32, -18, 0);
    pan(B.D12, PH, 1920, 0, ["#scD1"], ["#scD2"]);
  })();

  /* =================================================================== D2 · Angebot in 48 Stunden */
  (function () {
    /* 48 Stundenstriche */
    var g = $("#ticks"), NS = "http://www.w3.org/2000/svg", ticks = [];
    for (var i = 0; i < 48; i++) {
      var a = (i / 48) * Math.PI * 2 - Math.PI / 2, r0 = 250, r1 = i % 6 === 0 ? 272 : 264;
      var ln = document.createElementNS(NS, "line");
      ln.setAttribute("x1", 320 + r0 * Math.cos(a)); ln.setAttribute("y1", 320 + r0 * Math.sin(a));
      ln.setAttribute("x2", 320 + r1 * Math.cos(a)); ln.setAttribute("y2", 320 + r1 * Math.sin(a));
      g.appendChild(ln); ticks.push(ln);
    }
    var C = 2 * Math.PI * 296, pr = $("#r48p");
    pr.style.strokeDasharray = C + " " + (C + 10);
    var r0 = t("48") - 0.2, dur = 1.45, E = gsap.parseEase("power2.inOut");
    tl.fromTo(pr, { strokeDashoffset: C }, { strokeDashoffset: 0, duration: dur, ease: "power2.inOut" }, r0);
    count("#n48", 0, 48, r0, dur, null, "power2.inOut");
    D.push(function (ft) { var k = E(Math.max(0, Math.min(1, (ft - r0) / dur))); ticks.forEach(function (l, i) { l.classList.toggle("on", k * 48 >= i + 0.5); }); });
    sfx("blips", r0 + 0.1, -22, 3);
    /* Angebot füllt sich, während die Uhr läuft */
    var lis = $$("#offer li");
    lis.forEach(function (li, i) { pop(li, r0 + 0.35 + i * 0.32, { x: 24, y: 0 }, 0.5); sfx("pop", r0 + 0.38 + i * 0.32, -25, i % 4); });
    pop(".offer__note", r0 + 1.65, { y: 12 }, 0.5);
    var st = t("angebot", 1) - 0.12;
    pop("#stamp", st, { scale: 1.6, rotation: -14, to: { rotation: -4 } }, 0.42, "power4.out");
    sfx("impact", st + 0.08, -18, 1);
    pan(B.D2E, PV, 0, 1080, ["#scD2"], ["#scE"]);
  })();

  /* =================================================================== E · Ablauf, Website, System */
  (function () {
    /* Maße vor allen Startzuständen nehmen */
    var pub = rect("#pub"), ang = rect("#pcAng"), auf = rect("#slotAuf"), tagO = $("#tagO");
    var tagH = tagO.offsetHeight + 10;     /* Hinweis + Abstand, solange er zu ist */
    var lis = $$("#rail li"), on = function (i, at) {
      morph(lis[i], "on", [lis[i], $("i", lis[i])], at, 0.25);
      pulse($("i", lis[i]), at, 1.14);
      if (i > 0) tl.to("#railFill", { scaleX: i / 4, duration: 0.6, ease: "power2.inOut" }, at - 0.18);
    };
    tl.set("#railFill", { scaleX: 0 }, 0);
    var s1 = t("lernen"), s2 = t("gestalten"), s3 = t("bauen"), s4 = t("testen"), s5 = t("live");
    /* 1 · Ihre Kunden */
    on(0, B.D2E + PV - 0.1);
    ["#rb1", "#rb2", "#rb3"].forEach(function (s, i) { pop(s, B.D2E + PV - 0.2 + i * 0.12, { y: 30 }, 0.6); });
    $$(".term u i").forEach(function (b, i) { tl.fromTo(b, { scaleX: 0 }, { scaleX: 1, duration: 0.8, ease: "power2.out" }, t("kunden") - 0.2 + i * 0.1); });
    $$(".dev div").forEach(function (b, i) { tl.fromTo(b, { scaleY: 0 }, { scaleY: 1, duration: 0.8, ease: "power3.out" }, t("kunden") + i * 0.12); });
    pop(".rb__note", t("kennen") + 0.1, { y: 12 }, 0.5);
    /* 2 · Gestaltung: Zielgruppe wischt weg, Skizze, dann das Design */
    on(1, s2);
    tl.fromTo("#rboard", { clipPath: "inset(0% 0% 0% 0%)" }, { clipPath: "inset(0% 0% 0% 100%)", duration: 0.6, ease: "power2.inOut" }, s2 - 0.2);
    var w0 = t("neue") - 0.05, wd = 0.85;
    tl.fromTo("#wf", { clipPath: "inset(0% 0% 0% 0%)" }, { clipPath: "inset(0% 0% 0% 100%)", duration: wd, ease: "power2.inOut" }, w0);
    tl.fromTo("#wipe", { x: 0, autoAlpha: 1 }, { x: 1420, duration: wd, ease: "power2.inOut" }, w0);
    tl.set("#wipe", { autoAlpha: 0 }, w0 + wd);
    sfx("swoosh", w0 + 0.3, -18, 3);
    /* 3 · Entwicklung: Formular und Galerie setzen sich ein */
    on(2, s3);
    pop("#nsForm", s3 - 0.05, { y: 40, scale: 0.94 }, 0.6, "back.out(1.3)");
    $$("#nsGal div").forEach(function (d, i) { pop(d, s3 + 0.1 + i * 0.09, { y: 46 }, 0.55); });
    sfx("pop", s3, -20, 2);
    /* 4 · Test: Geräte und Prüfpunkte */
    on(3, s4);
    pop("#mtab", s4 - 0.1, { x: -140, y: 0, rotation: -3 }, 0.7);
    pop("#mph", s4 + 0.05, { x: 140, y: 0, rotation: 3 }, 0.7);
    $$("#checks span").forEach(function (c, i) { pop(c, s4 + 0.2 + i * 0.16, { y: 18, scale: 0.95 }, 0.45); sfx("blips", s4 + 0.25 + i * 0.16, -25, i % 4); });
    /* 5 · Live: Klick auf Veröffentlichen */
    var cur = "#cur2", c0 = s5 - 1.0;
    tl.set(cur, { x: 1480, y: 780 }, 0);
    tl.fromTo(cur, { autoAlpha: 0 }, { autoAlpha: 1, duration: 0.25 }, c0);
    cursorTo(cur, c0, pub.x + pub.w * 0.5, pub.y + pub.h * 0.6, 0.72);
    click(cur, s5 - 0.16);
    tl.to("#pub", { autoAlpha: 0, scale: 0.9, duration: 0.2, ease: "power2.in" }, s5 - 0.1);
    pop("#live", s5, { scale: 0.7, y: 0 }, 0.45, "back.out(2)");
    tl.to(cur, { autoAlpha: 0, x: "+=60", y: "+=80", duration: 0.4, ease: "power2.in" }, s5 + 0.3);
    tl.fromTo("#urlA", { yPercent: 0 }, { yPercent: -120, duration: 0.35, ease: "power2.in" }, s5);
    tl.fromTo("#urlB", { yPercent: 120 }, { yPercent: 0, duration: 0.45, ease: "power3.out" }, s5 + 0.2);
    on(4, s5);
    sfx("success", s5 + 0.02, -15, 1);
    leave("#mtab", s5 + 0.35, { x: -110 }, 0.45);
    leave("#mph", s5 + 0.35, { x: 110 }, 0.45);
    $$("#checks span").forEach(function (c, i) { leave(c, s5 + 0.3 + i * 0.04, { y: 16 }, 0.3); });
    /* Dahinter: Website dreht sich um, dahinter das eigene System */
    var f = B.flip;
    leave("#rail", f - 0.2, { y: -30 }, 0.4);
    tl.fromTo("#brw", { rotationY: 0, y: 0, transformPerspective: 2600 }, { rotationY: 90, y: -43, transformPerspective: 2600, duration: 0.5, ease: "power2.in", immediateRender: false }, f);
    tl.set("#brw", { autoAlpha: 0 }, f + 0.5);
    tl.fromTo("#dash", { rotationY: -90, y: -43, autoAlpha: 1, transformPerspective: 2600 }, { rotationY: 0, y: -86, autoAlpha: 1, transformPerspective: 2600, duration: 0.6, ease: "power2.out", immediateRender: false }, f + 0.5);
    tl.set("#dash", { autoAlpha: 0 }, 0);
    sfx("whoosh", f + 0.48, -15, 1);
    /* jede Anfrage */
    var aT = t("anfrage");
    pop("#toast", aT - 0.12, { x: 40, y: 0 }, 0.5);
    leave("#toast", aT + 1.9, { x: 30 }, 0.35);
    grow("#pcNew", aT, 0.55, { paddingTop: [0, 15], paddingBottom: [0, 15], marginBottom: [-12, 0], borderTopWidth: [0, 1], borderBottomWidth: [0, 1] });
    text("#kA", [[0, "2"], [aT + 0.25, "3"]]); text("#nNeu", [[0, "1"], [aT + 0.25, "2"]]);
    pop("#kAd", aT + 0.3, { y: 8 }, 0.4);
    pulse("#kA", aT + 0.25, 1.12);
    sfx("ping", aT, -16, 1);
    /* jeder Termin */
    var tT = t("termin");
    grow("#tagT", tT - 0.05, 0.45, { marginTop: [-4, 6], paddingTop: [0, 4], paddingBottom: [0, 4] });
    text("#kT", [[0, "3"], [tT + 0.2, "4"]]); pulse("#kT", tT + 0.2, 1.12);
    sfx("pop", tT, -19, 3);
    /* jeder Auftrag: Karte wandert nach „Auftrag“ */
    var oT = t("auftrag");
    grow("#slotAuf", oT - 0.3, 0.55, { paddingTop: [0, 15], paddingBottom: [0, 15], marginBottom: [-12, 0], borderTopWidth: [0, 1], borderBottomWidth: [0, 1] });
    tl.to("#pcAng", { x: auf.x - ang.x, y: auf.y - ang.y, duration: 0.8, ease: "power3.inOut" }, oT - 0.3);
    tl.fromTo("#pcAng", { boxShadow: "0 0 0 0 rgba(0,0,0,0)" }, { boxShadow: "0 22px 40px -12px rgba(0,0,0,0.6)", duration: 0.4, yoyo: true, repeat: 1, ease: "sine.inOut", immediateRender: false }, oT - 0.3);
    tl.to("#pcY", { y: -(ang.h - tagH + 12), duration: 0.6, ease: "power3.inOut" }, oT);
    grow(tagO, oT + 0.35, 0.4, { marginTop: [-4, 6], paddingTop: [0, 4], paddingBottom: [0, 4] });
    text("#nAng", [[0, "2"], [oT + 0.35, "1"]]); text("#nAuf", [[0, "1"], [oT + 0.35, "2"]]); text("#kO", [[0, "5"], [oT + 0.5, "6"]]);
    pulse("#kO", oT + 0.5, 1.12);
    sfx("swoosh", oT - 0.05, -21, 0); sfx("success", oT + 0.5, -17, 2);
  })();

  /* =================================================================== F · Alles aus einer Hand */
  (function () {
    var v = rect("#tSv"), dash = rect("#dash"), TR = ["#tW", "#tS", "#tP", "#tA"].map(rect);
    var k = v.w / dash.w, ty = v.y + (v.h - dash.h * k) / 2;
    var z = B.EF;
    /* das Dashboard wird kleiner und landet in seiner Kachel */
    tl.fromTo("#dash", { x: 0, y: -86, scale: 1, transformOrigin: "0 0" }, { x: v.x - dash.x, y: ty - dash.y, scale: k, duration: 1.1, ease: "power3.inOut", immediateRender: false }, z);
    sfx("whoosh", z + 0.5, -16, 2);
    pop("#tS", z + 0.75, { y: 0, scale: 0.97 }, 0.6);
    reveal("#hlF", [t("alles", 1), t("aus", 1), t("einer", 1), t("hand", 1)].map(function (x) { return x - 0.05; }));
    /* die vier Bausteine */
    var W = t("website", 3), S = t("system", 2), P = t("pflege"), A = t("werbung");
    /* alle vier Kacheln stehen gleich nach der Landung bereit (gedämpft) und leuchten auf, wenn sie genannt werden */
    var DIM = 0.4;
    ["#tW", "#tP", "#tA"].forEach(function (s, i) { pop(s, z + 0.82 + i * 0.09, { y: 40, scale: 0.97, to: { autoAlpha: DIM } }, 0.7); });
    function wake(s, at) {
      tl.to(s, { autoAlpha: 1, duration: 0.3, ease: "power1.out" }, at);
      tl.fromTo(s, { borderColor: "rgba(150,178,224,0.22)" }, { borderColor: "rgba(255,87,87,0.85)", duration: 0.22, yoyo: true, repeat: 1, repeatDelay: 0.35, ease: "power1.inOut", immediateRender: false }, at);
      pop(s + " .tile__v", at + 0.05, { y: 18, scale: 0.97 }, 0.55);
    }
    wake("#tW", W - 0.08);
    tl.fromTo("#tS", { borderColor: "rgba(150,178,224,0.22)" }, { borderColor: "rgba(255,87,87,0.85)", duration: 0.25, yoyo: true, repeat: 1, repeatDelay: 0.3, ease: "power1.inOut", immediateRender: false }, S - 0.05);
    pulse("#tS", S - 0.05, 1.03, 0.2);
    wake("#tP", P - 0.08);
    $$("#tP .bub").forEach(function (b, i) { pop(b, P + 0.2 + i * 0.22, { y: 14, scale: 0.96 }, 0.4); });
    wake("#tA", A - 0.08);
    $$("#tA .tva__bars i").forEach(function (b, i) { tl.fromTo(b, { scaleY: 0 }, { scaleY: 1, duration: 0.6, ease: "power3.out" }, A + 0.15 + i * 0.05); });
    [W, P, A].forEach(function (x, i) { sfx("pop", x - 0.06, -18, i); });
    sfx("pop", S - 0.04, -20, 3);
    /* aufeinander abgestimmt: Verbindungen zum gemeinsamen Ansprechpartner */
    var nx = 960, ny = 812;
    TR.forEach(function (r, i) {
      var x0 = r.x + r.w / 2, y0 = r.y + r.h;
      var d = "M" + x0 + " " + y0 + " C" + x0 + " " + (y0 + 88) + " " + nx + " " + (ny - 82) + " " + nx + " " + ny;
      $("#lk" + (i + 1)).setAttribute("d", d); $("#lp" + (i + 1)).setAttribute("d", d);
    });
    var ab = t("aufeinander");
    [1, 2, 3, 4].forEach(function (i) {
      draw("#lk" + i, ab - 0.1 + i * 0.05, 0.7);
      var lp = $("#lp" + i), L = lp.getTotalLength();
      lp.style.strokeDasharray = "80 " + (L + 200);
      tl.fromTo(lp, { strokeDashoffset: 80, autoAlpha: 1 }, { strokeDashoffset: -L, duration: 0.85, ease: "power1.in" }, t("abgestimmt") - 0.2 + i * 0.06);
      tl.set(lp, { autoAlpha: 0 }, t("abgestimmt") + 0.75 + i * 0.06);
    });
    tl.fromTo("#node", { autoAlpha: 0, scale: 0, transformOrigin: "50% 50%" }, { autoAlpha: 1, scale: 1, duration: 0.4, ease: "back.out(2)" }, ab + 0.5);
    pulse("#node", t("abgestimmt") + 0.62, 1.5, 0.18);
    sfx("blips", t("abgestimmt") - 0.1, -22, 0);
    /* mit einem festen Ansprechpartner */
    var hb = t("festen") - 0.25;
    pop("#hub", hb, { y: 0, scaleX: 0.3, scaleY: 0.7 }, 0.65, "power3.out");
    $$("#hub > *").forEach(function (c, i) { pop(c, hb + 0.18 + i * 0.08, { y: 10 }, 0.45); });
    leave("#node", hb + 0.2, { scale: 0.6 }, 0.25);
    sfx("pop", hb + 0.05, -17, 1);
    pan(B.FG, PH, 1920, 0, ["#scF", "#scE"], ["#scG"]);
  })();

  /* =================================================================== G · Erfahrung */
  (function () {
    var m = $("#matrix"), cells = [];
    for (var i = 0; i < 200; i++) { var c = document.createElement("i"); c.innerHTML = "<u></u><s></s>"; m.appendChild(c); cells.push(c); }
    var c0 = t("200") - 0.35, cd = 1.15;
    count("#n200", 0, 200, c0, cd, null, "power2.out");
    var E = gsap.parseEase("power2.out");
    /* Kacheln füllen sich in einer schrägen Welle, im Takt mit der Zahl */
    var order = cells.map(function (c, i) { return { c: c, k: (i % 20) + Math.floor(i / 20) * 1.6 }; }).sort(function (a, b) { return a.k - b.k; });
    order.forEach(function (o, j) {
      var tj = c0 + cd * inv(j / 199);
      tl.fromTo($("u", o.c), { autoAlpha: 0, scale: 0.4 }, { autoAlpha: 1, scale: 1, duration: 0.35, ease: "power2.out" }, tj);
    });
    function inv(y) { var lo = 0, hi = 1; for (var n = 0; n < 30; n++) { var mid = (lo + hi) / 2; if (E(mid) < y) lo = mid; else hi = mid; } return lo; }
    sfx("blips", c0 + 0.05, -21, 1);
    reveal("#big small", t("kampagnen") - 0.05);
    $$("#mtags span").forEach(function (s, i) { pop(s, t("kampagnen") + 0.1 + i * 0.1, { y: 16 }, 0.5); });
    /* was wirkt: einige Kacheln leuchten auf */
    reveal("#big em", t("wissen") - 0.04, 0.7, 0.06);
    var hot = [23, 47, 52, 68, 91, 104, 117, 126, 139, 158, 163, 172, 186, 194];
    var wk = t("wissen") + 0.3;
    hot.forEach(function (n, i) { tl.fromTo($("s", cells[n]), { autoAlpha: 0, scale: 0.6 }, { autoAlpha: 1, scale: 1, duration: 0.4, ease: "back.out(2)" }, wk + i * 0.025); });
    sfx("success", wk + 0.05, -19, 3);
    pan(B.GH, PV, 0, 1080, ["#scG"], ["#scH"]);
  })();

  /* =================================================================== H · Ergebnis RechnungsRadar */
  (function () {
    var n0 = B.GH + PV + 0.05, n1 = t("prozent") - 0.05;
    tl.fromTo("#rb0 u i", { scaleX: 0 }, { scaleX: 1, duration: 0.8, ease: "power2.out" }, n0 - 0.1);
    pop("#rrBig b", n0 - 0.2, { y: 26 }, 0.6);
    count("#n230", 0, 230, n0, n1 - n0, function (v) { return "+" + Math.round(v); }, "power3.inOut");
    tl.fromTo("#rb1x u i", { scaleX: 0.303 }, { scaleX: 1, duration: n1 - n0, ease: "power3.inOut" }, n0);
    sfx("riser", n1 + 0.05, -22, 1);
    reveal("#rrBig small", t("mehr", 1) - 0.05, 0.7, 0.07);
    var kc = t("neuen", 1) - 0.1;
    $$("#kpirow .kc").forEach(function (c, i) { pop(c, kc + i * 0.12, { y: 30 }, 0.6); sfx("pop", kc + 0.02 + i * 0.12, -23, i); });
    pop("#rrSrc", kc + 0.5, { y: 8 }, 0.5);
    pan(B.HI, PH, 1920, 0, ["#scH"], ["#scI"]);
  })();

  /* =================================================================== I · Und wenn sich etwas ändert? */
  (function () {
    var ws = [p("und wenn sich"), t("wenn", 1), t("sich", 2), t("etwas"), t("ändert")];
    var lns = $$("#qI .ln"), all = words(lns[0]).concat(words(lns[1]));
    var qw = Math.max(rect(lns[0]).w, rect(lns[1]).w), qoff = (1920 - qw) / 2 - 150;
    all.forEach(function (w, i) { tl.fromTo(w, { yPercent: 140 }, { yPercent: 0, duration: 0.75, ease: "power4.out" }, ws[i] - 0.06); });
    var cg = [t("öffnungszeiten", 2) - 0.1, t("angebot", 2) - 0.12, t("frische") - 0.02];
    tl.fromTo("#qI", { x: qoff }, { x: 0, duration: 0.8, ease: "power3.inOut" }, cg[0] - 0.62);
    ["#cg1", "#cg2", "#cg3"].forEach(function (s, i) { pop(s, cg[i], { x: 70, y: 0 }, 0.6); sfx("pop", cg[i] + 0.02, -18, i); });
    pan(B.IJ, PV, 0, 1080, ["#scI"], ["#scJ"]);
  })();

  /* =================================================================== J · KI-Agent per WhatsApp */
  (function () {
    /* Maße der fertigen Unterhaltung */
    var bIn = rect("#bIn"), info = rect("#info");
    var x0 = bIn.x + bIn.w - 30, y0 = bIn.y + bIn.h * 0.5, x1 = info.x + 30, y1 = info.y + info.h * 0.5;
    $("#flowP").setAttribute("d", "M" + x0 + " " + y0 + " C" + (x0 + 160) + " " + (y0 - 30) + " " + (x1 - 170) + " " + (y1 + 40) + " " + x1 + " " + y1);
    var bub = { marginTop: [0, 10], paddingTop: [0, 12], paddingBottom: [0, 9] };
    var w0 = t("schreiben") - 0.05, msg = "Ab Montag haben wir 8–18 Uhr geöffnet. Und bitte das neue Foto in die Galerie.";
    var tw = 1.45, sent = w0 + tw + 0.12;
    typeText("#waTx", msg, w0, tw, sent);
    sfx("typing", w0, -22, 1);
    grow("#bMe", sent, 0.45, bub);
    sfx("pop", sent, -17, 0);
    grow("#bImg", sent + 0.32, 0.5, { marginTop: [0, 10], paddingTop: [0, 5], paddingBottom: [0, 7] });
    sfx("pop", sent + 0.33, -20, 1);
    var ty = sent + 0.75, done = t("pflegt") - 0.3;
    tl.set("#waTy", { autoAlpha: 0 }, 0);
    tl.set("#waOn", { autoAlpha: 1 }, 0);
    tl.set("#waOn", { autoAlpha: 0 }, ty); tl.set("#waTy", { autoAlpha: 1 }, ty);
    tl.set("#waTy", { autoAlpha: 0 }, done); tl.set("#waOn", { autoAlpha: 1 }, done);
    /* der Agent tippt: die Antwortblase beginnt klein mit drei Punkten und zieht dann zur fertigen Antwort auf */
    var bi = $("#bIn"), bW = bi.offsetWidth, bH = bi.offsetHeight, btx = $("#bInTx");
    btx.style.width = btx.offsetWidth + "px";          /* Text steht gleich in seiner fertigen Breite – kein Umbrechen beim Aufziehen */
    tl.fromTo(bi, { autoAlpha: 0, height: 0, width: 82, marginTop: 0, paddingTop: 0, paddingBottom: 0 },
      { autoAlpha: 1, height: 44, width: 82, marginTop: 10, paddingTop: 12, paddingBottom: 9, duration: 0.3, ease: "power2.out" }, ty);
    tl.fromTo("#bInTx", { autoAlpha: 0 }, { autoAlpha: 1, duration: 0.3, ease: "power1.out" }, done + 0.18);
    tl.to("#dots", { autoAlpha: 0, duration: 0.15, ease: "power1.in" }, done - 0.02);
    tl.to(bi, { height: bH, width: bW, duration: 0.5, ease: "power3.out" }, done);
    $$("#dots i").forEach(function (d, i) {
      var n = Math.max(1, Math.floor((done - ty - 0.55) / 0.2)); if (n % 2 === 0) n -= 1;
      tl.fromTo(d, { y: 0 }, { y: -6, duration: 0.2, yoyo: true, repeat: n, ease: "sine.inOut", immediateRender: false }, ty + 0.15 + i * 0.1);
    });

    sfx("ping", done + 0.05, -15, 2);
    /* Daten fließen zur Website */
    var fl = done + 0.3, P = $("#flowP"), L = draw(P, fl, 0.45, "power2.out"), D0 = $("#flowD");
    tl.fromTo("#flowD", { autoAlpha: 0 }, { autoAlpha: 1, duration: 0.15 }, fl);
    D.push(function (ft) { var k = gsap.parseEase("power2.inOut")(Math.max(0, Math.min(1, (ft - fl) / 0.6))); var pt = P.getPointAtLength(k * L); D0.setAttribute("cx", pt.x); D0.setAttribute("cy", pt.y); });
    tl.to("#flowD", { autoAlpha: 0, duration: 0.2 }, fl + 0.6);
    tl.to("#flowP", { autoAlpha: 0, duration: 0.4 }, fl + 0.8);
    /* Website zeigt die Änderung */
    var up = fl + 0.45;
    tl.fromTo("#flash", { autoAlpha: 0 }, { autoAlpha: 1, duration: 0.22, yoyo: true, repeat: 1, ease: "power1.inOut" }, up);
    tl.fromTo("#hOld", { yPercent: 0 }, { yPercent: -110, duration: 0.32, ease: "power2.in" }, up);
    tl.fromTo("#hNew", { yPercent: 110 }, { yPercent: 0, duration: 0.42, ease: "power3.out" }, up + 0.22);
    pop("#upd", up + 0.35, { scale: 0.7, y: 0 }, 0.4, "back.out(2)");
    sfx("success", up + 0.05, -16, 0);
    var gl = up + 0.1;
    tl.fromTo("#galT", { x: -222 }, { x: 0, duration: 0.65, ease: "power3.inOut" }, gl);
    sfx("swoosh", gl + 0.2, -21, 1);
    pan(B.JK, PH, 1920, 0, ["#scJ"], ["#scK"]);
  })();

  /* =================================================================== K · Dashboard und Team */
  (function () {
    var c0 = B.JK + PH - 0.15, cmd = "Neue Leistung „Treppen nach Maß“ auf die Website", cd = 1.3;
    typeText("#cmd", cmd, c0, cd);
    blink("#caret2", B.JK, c0 + cd + 0.2);
    sfx("typing", c0, -23, 2);
    var go = c0 + cd + 0.12;
    pulse("#cmdGo", go, 0.9, 0.1);
    sfx("click", go, -14, 1);
    grow("#ans", go + 0.2, 0.5);
    sfx("success", go + 0.25, -17, 1);
    grow("#add", go + 0.5, 0.45, { paddingTop: [0, 16], paddingBottom: [0, 16], marginBottom: [0, 10], borderTopWidth: [0, 1], borderBottomWidth: [0, 1] });
    grow("#pgNew", go + 0.6, 0.55, { paddingTop: [0, 12], paddingBottom: [0, 12], marginBottom: [0, 14] });
    sfx("pop", go + 0.62, -19, 2);
    /* persönlich: das Team */
    var tm = t("team") - 0.25;
    leave("#pg", tm - 0.25, { y: -40, scale: 0.96 }, 0.4);
    pop("#team", tm, { y: 60 }, 0.75);
    $$("#team li").forEach(function (li, i) { pop(li, tm + 0.3 + i * 0.14, { x: 24, y: 0 }, 0.45); });
    sfx("swoosh", tm + 0.1, -19, 3);
    /* Abgang vor dem Logo */
    tl.to(["#db2", "#team"], { autoAlpha: 0, scale: 0.97, duration: 0.45, ease: "sine.inOut" }, B.Kout);
  })();

  /* =================================================================== L · Abschluss */
  (function () {
    var cta = rect("#endCta");
    var ring = $("#ctaRing"); Object.assign(ring.style, { left: cta.x + "px", top: cta.y + "px", width: cta.w + "px", height: cta.h + "px" });
    var a = B.L;
    tl.fromTo("#endGlow", { autoAlpha: 0, scale: 0.8 }, { autoAlpha: 1, scale: 1, duration: 2.2, ease: "power2.out" }, a);
    var lk = rect("#lock"), mk = rect("#endMk"), mx = (960 - (mk.x + mk.w / 2));
    pop("#endMk", a, { y: 0, scale: 0.8, x: mx, to: { x: mx } }, 0.8, "power3.out");
    tl.to("#endMk", { x: 0, duration: 0.72, ease: "power3.inOut" }, t("medialyte") + 0.03);
    tl.fromTo("#endWm", { clipPath: "inset(-10% -2% 100% -2%)", y: 70 }, { clipPath: "inset(-10% -2% -12% -2%)", y: 0, duration: 0.8, ease: "power4.out" }, t("medialyte") + 0.46);
    sfx("impact", t("medialyte") - 0.02, -15, 2);
    reveal("#endTag", [t("damit"), t("aus", 3), t("besuchern"), t("kunden", 2), t("werden")].map(function (x) { return x - 0.05; }), 0.7);
    pop("#endCta", t("buchen") - 0.08, { y: 20, scale: 0.94 }, 0.6);
    pop("#endUrl", t("buchen") + 0.4, { y: 10 }, 0.5);
    sfx("pop", t("buchen") - 0.06, -18, 2);
    /* Klick auf den Termin-Knopf */
    var cur = "#cur3", ck = t("erstgespräch", 2) + 0.05;
    tl.set(cur, { x: 1450, y: 980 }, 0);
    tl.fromTo(cur, { autoAlpha: 0 }, { autoAlpha: 1, duration: 0.3 }, ck - 1.0);
    cursorTo(cur, ck - 1.0, cta.x + cta.w * 0.62, cta.y + cta.h * 0.6, 0.85);
    click(cur, ck);
    tl.fromTo("#endCta", { scale: 1 }, { scale: 0.965, duration: 0.1, yoyo: true, repeat: 1, ease: "power1.inOut", immediateRender: false }, ck);
    tl.fromTo(ring, { autoAlpha: 0.9, scale: 1 }, { autoAlpha: 0, scale: 1.18, duration: 0.8, ease: "power2.out", immediateRender: false }, ck + 0.05);
    tl.to(cur, { autoAlpha: 0, duration: 0.5, ease: "power1.in" }, ck + 1.1);
    tl.set(ring, { autoAlpha: 0 }, 0);
  })();

  tl.set({}, {}, DUR);

  /* ---------- Schnittstelle für Rendern und Prüfen ---------- */
  window.__dur = DUR;
  window.__B = B;
  window.__sfx = SFX;
  window.__seek = function (s, ft) {
    var f = ft == null ? s : ft, i;
    /* Zustände zuerst: Szenen müssen sichtbar sein, bevor Tweens ihre Startwerte lesen (autoAlpha liest sonst 0) */
    for (i = 0; i < D.length; i++) D[i](f);
    tl.seek(s, true);
    for (i = 0; i < D.length; i++) D[i](f);
    return true;
  };
  /* Bewegung je Bild messen (für die Bewegungsunschärfe): größte Verschiebung einer Kante gegenüber dem letzten Aufruf */
  var TRACK = [], prev = null;
  (function () {
    var seen = new Set();
    tl.getChildren(true, true, false).forEach(function (tw) {
      (tw.targets ? tw.targets() : []).forEach(function (x) { if (x instanceof Element && !seen.has(x)) { seen.add(x); TRACK.push(x); } });
    });
  })();
  window.__probe = function (s) {
    window.__seek(s);
    var cur = TRACK.map(function (e) {
      if (!e.checkVisibility({ opacityProperty: true, visibilityProperty: true, checkOpacity: true, checkVisibilityCSS: true })) return null;
      var r = e.getBoundingClientRect(); return [r.left, r.top, r.right, r.bottom];
    });
    var m = 0;
    if (prev) for (var i = 0; i < cur.length; i++) {
      var a = cur[i], b = prev[i]; if (!a || !b) continue;
      for (var j = 0; j < 4; j++) { var d = Math.abs(a[j] - b[j]); if (d > m) m = d; }
    }
    prev = cur; return m;
  };
  window.__probeReset = function () { prev = null; };
  window.__tl = tl;
  window.__seek(0);
  /* alle Bilder vorab dekodieren, damit kein Bild beim ersten Auftauchen fehlt */
  var urls = new Set();
  $$("*").forEach(function (e) { var m = getComputedStyle(e).backgroundImage.match(/url\("?([^")]+)"?\)/g); if (m) m.forEach(function (u) { urls.add(u.replace(/^url\("?|"?\)$/g, "")); }); });
  $$("img").forEach(function (i) { urls.add(i.src); });
  Promise.all(Array.from(urls).map(function (u) { var im = new Image(); im.src = u; return im.decode().catch(function () {}); })).then(function () { window.__ready = true; });
  }
})();
