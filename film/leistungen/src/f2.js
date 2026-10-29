/* Film 2 · Kundenmanagement-System – Zeitleiste */
FILM(function (K) {
  var tl = K.tl, t = K.t, p = K.p, $ = K.$, $$ = K.$$, pop = K.pop, leave = K.leave, sfx = K.sfx, vis = K.vis, cls = K.cls;
  var M = window.TM.music, T1 = M.T1, cJ = M.cJ, W = window.TM.words;

  var tB = t("sophias"), tC = p("anfragen kommen"), tD = p("wir bauen");
  var t2 = p("angebote schreibt"), t3 = p("termine stehen"), t4 = t("nachfassen"), t5 = p("und wie");
  vis("#scA", 0, tB); vis("#scB", tB - 0.5, tC + 0.1); vis("#scC", tC - 0.5, tD + 0.1); vis("#scD", tD - 0.5, cJ);
  vis("#bt1", 0, t2 + 0.1); vis("#bt2", t2 - 0.5, t3 + 0.1); vis("#bt3", t3 - 0.5, t4 + 0.1); vis("#bt4", t4 - 0.5, t5 + 0.1); vis("#bt5", t5 - 0.5, null);
  SVC.chap(K, "2", "Kundenmanagement", 0, cJ - 0.7);

  /* ---------- A · Einstieg ---------- */
  SVC.hook(K, "#hkA", [0, t("sind") - 0.05, t("diesen") - 0.05, t("verloren") - 0.05]);
  pop("#lq1", 0.0, { y: 30 }, 0.5); pop("#lq2", 0.4, { y: 40 }, 0.55); pop("#lq3", 0.8, { y: 40 }, 0.55);
  sfx("impact", 0.0, -16, 0); sfx("pop", 0.42, -20, 1); sfx("pop", 0.82, -20, 2);
  var tV = t("verloren");
  ["#lq1", "#lq2", "#lq3"].forEach(function (s, k) {
    tl.to(s, { y: 260 + k * 30, rotation: (k % 2 ? 9 : -9), filter: "grayscale(1) brightness(.6)", autoAlpha: 0, duration: 0.85, ease: "power2.in" }, tV + 0.05 + k * 0.12);
  });
  sfx("swoosh", tV + 0.1, -19, 0);
  K.conceal("#hkA", tB - 0.45, 0.02);

  /* ---------- B · Sophia ---------- */
  pop("#perB", tB - 0.2, { y: 70, scale: 0.94 }, 0.75); sfx("whoosh", tB - 0.15, -18, 0);
  var tN = t("anfragen", 2);
  ["#bn1", "#bn2", "#bn3"].forEach(function (s, k) { pop(s, tN - 0.25 + k * 0.24, { x: 60, y: 0 }, 0.5); sfx("ping", tN - 0.23 + k * 0.24, -21 - k, k); });
  var tP = t("problem");
  K.D.push(function (ft) {
    var n = ft < tN - 0.25 ? 0 : ft < tP - 0.1 ? Math.min(3, 1 + Math.floor((ft - tN + 0.25) / 0.24)) : Math.min(14, 3 + Math.floor((ft - tP + 0.1) / 0.09));
    var e = $("#bCntN"), v = String(n); if (e.textContent !== v) e.textContent = v;
  });
  tl.to("#perEve", { opacity: 1, duration: 0.9, ease: "power1.inOut" }, t("alltag") - 0.3);
  ["#bn1", "#bn2", "#bn3"].forEach(function (s, k) { tl.to(s, { x: (k - 1) * 26, rotation: (k - 1) * 3, duration: 0.5, ease: "power2.out" }, tP - 0.1 + k * 0.05); });
  K.pulse("#bCnt", tP + 0.6, 1.12, 0.14); sfx("blips", tP - 0.1, -20, 0);
  leave("#perB", tC - 0.45, { y: -40, scale: 0.96 }, 0.4);
  ["#bn1", "#bn2", "#bn3"].forEach(function (s, k) { leave(s, tC - 0.45 + k * 0.03, { x: 80 }, 0.35); });

  /* ---------- C · Fünf Schritte ---------- */
  pop("#steps", tC - 0.1, { y: -10 }, 0.4);
  var stepT = [[tC, T1], [t2, p("jetzt entstehen")], [t3, p("jetzt im")], [t4, p("jetzt verschickt")], [t5, p("alle zahlen")]];
  stepT.forEach(function (st, k) { cls("#sd" + (k + 1), "on", st[0] - 0.1); cls("#sd" + (k + 1), "ok", st[1]); });
  function swap(k, at) {           /* Problem-Etikett weicht dem Lösungs-Etikett */
    leave("#p" + k, at - 0.12, { y: -24 }, 0.25);
    pop("#s" + k, at + 0.05, { y: 24 }, 0.45);
    sfx("success", at + 0.05, -19, k % 3);
  }

  /* 1 · Anfragen */
  pop("#p1", tC - 0.1, { x: -30, y: 0 }, 0.45); sfx("swoosh", tC - 0.08, -21, 1);
  [["#chT", "telefon"], ["#chM", "e-mail"], ["#chW", "whatsapp"]].forEach(function (c, k) {
    pop(c[0], t(c[1]) - 0.3, { y: 60, scale: 0.92 }, 0.55); sfx("pop", t(c[1]) - 0.28, -18, k);
  });
  /* Aufbruch der Musik: alle Kanäle fliegen in den gemeinsamen Eingang */
  tl.fromTo("#lt3", { opacity: 0 }, { opacity: 1, duration: 0.35 }, T1 - 0.04); tl.to("#lt3", { opacity: 0, duration: 2.2, ease: "power1.inOut" }, T1 + 0.5);
  sfx("riser", T1 - 0.02, -16, 0); sfx("impact", T1 - 0.01, -11, 0);
  [["#chT", 260, 280], ["#chM", -260, 220], ["#chW", 80, -60]].forEach(function (c, k) {
    tl.to(c[0], { x: c[1], y: c[2], scale: 0.35, autoAlpha: 0, duration: 0.42, ease: "power3.in" }, T1 - 0.3 + k * 0.05);
  });
  swap(1, T1);
  pop("#inbox", T1 + 0.08, { y: 60, scale: 0.96 }, 0.65);
  $$("#inbox .ir").forEach(function (r, k) { pop(r, T1 + 0.4 + k * 0.3, { x: -40, y: 0 }, 0.45); sfx("pop", T1 + 0.42 + k * 0.3, -21, k % 3); });
  K.pulse("#inbox h6", t("ort") - 0.05, 1.05, 0.14);
  leave("#inbox", t2 - 0.45, { y: -40 }, 0.38); leave("#s1", t2 - 0.45, { y: -20 }, 0.3);

  /* 2 · Angebote */
  pop("#p2", t2 - 0.1, { x: -30, y: 0 }, 0.45);
  pop("#late", t2 + 0.0, { y: 60 }, 0.6); sfx("whoosh", t2 + 0.02, -19, 0);
  K.count(".late__clk b", 0, 71, t2 + 0.2, 2.0, function (v) { var m = 22 * 60 + 47 + Math.round(v); return Math.floor(m / 60) % 24 + ":" + ("0" + (m % 60)).slice(-2); }, "power1.in");
  $$("#late .doc i").forEach(function (l, k) { tl.fromTo(l, { scaleX: 0, transformOrigin: "0 50%" }, { scaleX: 1, duration: 0.45, ease: "none" }, t2 + 0.3 + k * 0.45); });
  K.blink("#lateC", t2 + 0.3, p("jetzt entstehen"));
  sfx("typing", t2 + 0.3, -24, 0);
  var tJ = p("jetzt entstehen");
  swap(2, tJ); leave("#late", tJ - 0.3, { y: -40 }, 0.35);
  pop("#req", tJ + 0.08, { y: 60 }, 0.6); sfx("whoosh", tJ + 0.1, -19, 1);
  K.pulse("#req", t("direkt") + 0.1, 1.03, 0.14);
  var tK = t("klicks");
  K.pulse("#reqBtn", tK - 0.3, 0.93, 0.09); sfx("click", tK - 0.28, -13, 0); sfx("click", tK - 0.05, -14, 1);
  pop("#ofr", tK - 0.02, { y: 70, scale: 0.95 }, 0.6); sfx("paper", tK, -17, 0);
  $$("#ofr .ofr__r").forEach(function (r, k) { pop(r, tK + 0.2 + k * 0.14, { x: -20, y: 0 }, 0.4); });
  leave("#req", t3 - 0.45, { y: -40 }, 0.38); leave("#ofr", t3 - 0.42, { y: 40 }, 0.38); leave("#s2", t3 - 0.45, { y: -20 }, 0.3);

  /* 3 · Termine */
  pop("#p3", t3 - 0.1, { x: -30, y: 0 }, 0.45);
  var tZe = t("zetteln");
  ["#st1", "#st2", "#st3"].forEach(function (s, k) { pop(s, tZe - 0.55 + k * 0.2, { y: -80, scale: 1.12, rotation: (k % 2 ? 12 : -12) }, 0.5, "back.out(1.5)"); sfx("paper", tZe - 0.5 + k * 0.2, -18 - k, k); });
  var tKa = p("jetzt im");
  swap(3, tKa);
  ["#st1", "#st2", "#st3"].forEach(function (s, k) { tl.to(s, { y: -140, scale: 0.4, rotation: 0, autoAlpha: 0, duration: 0.4, ease: "power3.in" }, tKa - 0.3 + k * 0.06); });
  pop("#cal2", tKa + 0.05, { y: 60, scale: 0.96 }, 0.6);
  ["#ev1", "#ev2", "#ev3"].forEach(function (s, k) { pop(s, t("kalender") - 0.05 + k * 0.24, { scale: 0.7, y: 0 }, 0.45, "back.out(1.8)"); sfx("pop", t("kalender") - 0.03 + k * 0.24, -19, k); });
  var tBs = t("bestätigung");
  pop("#conf", tBs - 0.3, { y: 50 }, 0.55); sfx("ping", tBs - 0.1, -15, 1);
  K.pulse("#ev1", tBs - 0.3, 1.08, 0.16);
  leave("#cal2", t4 - 0.45, { y: -40 }, 0.38); leave("#conf", t4 - 0.42, { y: 40 }, 0.35); leave("#s3", t4 - 0.45, { y: -20 }, 0.3);

  /* 4 · Nachfassen */
  pop("#p4", t4 - 0.1, { x: -30, y: 0 }, 0.45);
  pop("#stale", t4 + 0.0, { y: 60 }, 0.6); sfx("whoosh", t4 + 0.02, -19, 0);
  var tU = t("unter");
  tl.to("#stale", { y: 170, rotation: -2, autoAlpha: 0.32, filter: "grayscale(1)", duration: 0.9, ease: "power2.in" }, tU - 0.2);
  sfx("swoosh", tU - 0.1, -20, 2);
  var tVs = p("jetzt verschickt");
  swap(4, tVs); leave("#stale", tVs - 0.3, { y: 220 }, 0.3);
  var tEr = t("erinnerungen"), tBr = t("briefe");
  pop("#au1", tEr - 0.3, { x: -40, y: 0 }, 0.5); pop("#au1 > i", tEr + 0.25, { scale: 0.5, y: 0 }, 0.4, "back.out(2)");
  pop("#au2", tBr - 0.3, { x: -40, y: 0 }, 0.5); pop("#au2 > i", tBr + 0.25, { scale: 0.5, y: 0 }, 0.4, "back.out(2)");
  sfx("pop", tEr - 0.28, -18, 0); sfx("pop", tBr - 0.28, -18, 1); sfx("ping", tEr + 0.27, -21, 2); sfx("ping", tBr + 0.27, -21, 0);
  pop("#letter", tBr + 0.2, { y: 100, rotation: -8 }, 0.7); sfx("paper", tBr + 0.22, -16, 1);
  var tSe = t("selbst");
  pop("#autob", tSe - 0.35, { scale: 0.6, y: 0 }, 0.5, "back.out(2)"); sfx("success", tSe - 0.3, -16, 1);
  ["#au1", "#au2", "#letter", "#autob"].forEach(function (s, k) { leave(s, t5 - 0.45 + k * 0.03, { y: -30 }, 0.35); }); leave("#s4", t5 - 0.45, { y: -20 }, 0.3);

  /* 5 · Zahlen */
  pop("#p5", t5 - 0.1, { x: -30, y: 0 }, 0.45);
  $$("#bt5 .k").forEach(function (k, i) { pop(k, t5 + 0.1 + i * 0.12, { y: 40 }, 0.5); });
  pop("#bars", t5 + 0.5, { y: 30 }, 0.5);
  sfx("whoosh", t5 + 0.12, -20, 0);
  var tZ = p("alle zahlen");
  swap(5, tZ);
  var fmtE = function (v) { return Math.round(v / 100) * 100 >= 1000 ? (Math.round(v / 100) * 100).toLocaleString("de-DE") + " €" : Math.round(v) + " €"; };
  K.count("#k1", 0, 48, tZ, 1.4); K.count("#k2", 0, 31, tZ + 0.1, 1.4); K.count("#k3", 0, 19, tZ + 0.2, 1.4); K.count("#k4", 0, 86400, tZ + 0.3, 1.6, fmtE);
  K.D.push(function (ft) { if (ft < tZ) ["#k1", "#k2", "#k3", "#k4"].forEach(function (s) { var e = $(s); if (e.textContent !== "?") e.textContent = "?"; }); });
  $$("#bars i").forEach(function (b, k) { tl.fromTo(b, { scaleY: 0.04 }, { scaleY: 1, duration: 0.7, ease: "power3.out" }, tZ + 0.25 + k * 0.12); });
  sfx("blips", tZ + 0.1, -21, 1);
  K.pulse("#bars .now", t("blick") - 0.05, 1.06, 0.16);
  ["#bt5 .kp", "#bars"].forEach(function (s, k) { leave(s, tD - 0.45 + k * 0.04, { y: -30 }, 0.36); }); leave("#s5", tD - 0.45, { y: -20 }, 0.3);
  leave("#steps", tD - 0.45, { y: -10 }, 0.3);

  /* ---------- D · Für jeden Betrieb ---------- */
  K.reveal("#dkt2", tD - 0.1, 0.75, 0.08); sfx("whoosh", tD - 0.08, -19, 1);
  pop("#m1", t("genau") - 0.15, { y: 80, rotation: -5 }, 0.65); sfx("pop", t("genau") - 0.12, -18, 0);
  pop("#m2", p("ihren betrieb") + 0.2, { y: 80, rotation: 5 }, 0.65); sfx("pop", p("ihren betrieb") + 0.22, -18, 1);
  K.pulse("#m1", t("handwerk") - 0.05, 1.05, 0.16); K.pulse("#m2", t("kanzlei") - 0.05, 1.05, 0.16);
  sfx("ping", t("handwerk"), -21, 0); sfx("ping", t("kanzlei"), -21, 1);
  K.conceal("#dkt2", cJ - 0.55, 0.02); leave("#m1", cJ - 0.5, { y: 40 }, 0.38); leave("#m2", cJ - 0.47, { y: 40 }, 0.38);

  /* ---------- L · Abschluss ---------- */
  var n = W.length, ws = W.slice(n - 5).map(function (w) { return w.s; });
  SVC.end(K, ws);
});
