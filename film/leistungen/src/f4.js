/* Film 4 · Online-Marketing – Zeitleiste */
FILM(function (K) {
  var tl = K.tl, t = K.t, p = K.p, $ = K.$, $$ = K.$$, pop = K.pop, leave = K.leave, sfx = K.sfx, vis = K.vis;
  var M = window.TM.music, T1 = M.T1, cJ = M.cJ, W = window.TM.words;
  var de = function (v) { return Math.round(v).toLocaleString("de-DE"); };

  var tB = t("sophia"), tC = p("die anzeigen"), tZ = p("ihre zielgruppe"), tE = t("deshalb"), tF = t("jede"), tG = p("aus über");
  vis("#scA", 0, tB); vis("#scB", tB - 0.5, tC + 0.1); vis("#scC", tC - 0.5, T1 + 0.1); vis("#scD", T1 - 0.5, tE + 0.1);
  vis("#scE", tE - 0.5, tF + 0.1); vis("#scF", tF - 0.5, tG + 0.1); vis("#scG", tG - 0.5, cJ);
  SVC.chap(K, "4", "Online-Marketing", 0, cJ - 0.7);

  function people(sel, n) { var c = $(sel); for (var i = 0; i < n; i++) { var d = document.createElement("i"); d.className = "pp"; c.appendChild(d); } return $$(sel + " .pp"); }

  /* ---------- A · Einstieg ---------- */
  SVC.hook(K, "#hkA", [0, t("kosten") - 0.05, t("und") - 0.05, t("nur") - 0.05]);
  ["#mt1", "#mt2", "#mt3"].forEach(function (s, k) { pop(s, 0.05 + k * 0.22, { y: 40 }, 0.55); sfx("pop", 0.07 + k * 0.22, -20, k); });
  sfx("impact", 0.0, -16, 0);
  K.count("#mBud", 1500, 0, 1.1, 2.4, function (v) { return de(v) + " €"; }, "power1.inOut");
  K.count("#mClk", 0, 412, 1.3, 2.2, de, "power2.out");
  sfx("blips", 1.3, -22, 0);
  var tKl = t("klicks");
  K.pulse("#mt3", tKl - 0.05, 1.08, 0.16); sfx("impact", tKl, -17, 1);
  K.conceal("#hkA", tB - 0.45, 0.02);
  ["#mt1", "#mt2", "#mt3"].forEach(function (s, k) { leave(s, tB - 0.45 + k * 0.03, { y: 40 }, 0.35); });

  /* ---------- B · Sophia und die Agentur ---------- */
  pop("#perB", tB - 0.2, { y: 70, scale: 0.94 }, 0.75); sfx("whoosh", tB - 0.15, -18, 0);
  var tAg = t("agentur");
  pop("#ag", tAg - 0.3, { y: 80, rotation: 8 }, 0.65); sfx("paper", tAg - 0.28, -17, 0);
  var tNi = t("nicht", 1);
  ["#ag1", "#ag2", "#ag3"].forEach(function (s, k) { pop(s + " .mk", tNi - 0.35 + k * 0.16, { scale: 0.4, y: 0 }, 0.4, "back.out(2)"); sfx("pop", tNi - 0.33 + k * 0.16, -19, k); });
  leave("#perB", tC - 0.45, { y: -40, scale: 0.96 }, 0.4); leave("#ag", tC - 0.45, { x: 80 }, 0.38);

  /* ---------- C · Streuverlust ---------- */
  var pps = people("#crowd", 21);
  pop("#gad", tC - 0.1, { y: 50 }, 0.55); sfx("whoosh", tC - 0.08, -19, 0);
  pop("#crowd", tC + 0.15, { y: 40 }, 0.6);
  var tAl = t("alle");
  pps.forEach(function (e, i) { var d = ((i * 7) % 11) * 0.03; tl.to(e, { color: "rgba(110,155,255,.62)", duration: 0.3, ease: "power1.out" }, tAl - 0.1 + d); });
  sfx("blips", tAl - 0.05, -21, 1);
  var tFu = t("führten");
  leave("#gad", tFu - 0.45, { y: -40 }, 0.35); leave("#crowd", tFu - 0.42, { y: 60 }, 0.35);
  pop("#osite", tFu - 0.15, { y: 60 }, 0.6); sfx("whoosh", tFu - 0.12, -19, 1);
  $$("#ost > div").forEach(function (d, k) { pop(d, tFu + 0.5 + k * 0.3, { y: 40 }, 0.5); sfx("pop", tFu + 0.52 + k * 0.3, -19, k); });
  K.count("#ost > div:first-child b", 0, 412, tFu + 0.5, 1.0, de);
  K.count("#ost > div:nth-child(2) b", 0, 87, tFu + 0.8, 1.0, function (v) { return Math.round(v) + " %"; });
  var tVk = t("verkaufte");
  K.pulse("#ost0", tVk - 0.05, 1.1, 0.16); sfx("impact", tVk, -17, 2);
  tl.to("#osite", { filter: "grayscale(1) brightness(.8)", duration: 0.6, ease: "power1.inOut" }, tVk - 0.1);
  leave("#osite", T1 - 0.45, { y: -40 }, 0.38); leave("#ost", T1 - 0.42, { y: 40 }, 0.36);

  /* ---------- D · Wende (Aufbruch der Musik) ---------- */
  tl.fromTo("#lt3", { opacity: 0 }, { opacity: 1, duration: 0.35 }, T1 - 0.04); tl.to("#lt3", { opacity: 0, duration: 2.2, ease: "power1.inOut" }, T1 + 0.5);
  sfx("riser", T1 - 0.02, -16, 0); sfx("impact", T1 - 0.01, -11, 0);
  var lns = $$("#dk4 .ln"), lt = [T1 - 0.1, t("werbung", 2) - 0.08, t("bei", 2) - 0.08];
  lns.forEach(function (ln, i) { K.words(ln).forEach(function (w, k) { tl.fromTo(w, { yPercent: 140 }, { yPercent: 0, duration: 0.75, ease: "power4.out" }, lt[i] + k * 0.07); }); });
  sfx("swoosh", t("null") - 0.1, -19, 1);
  K.conceal("#dk4", tZ - 0.5, 0.02);
  pop("#zg", tZ - 0.12, { y: 70, scale: 0.97 }, 0.65); sfx("whoosh", tZ - 0.1, -18, 0);
  $$("#zg .zg__r").forEach(function (r, k) { pop(r, tZ + 0.25 + k * 0.18, { x: -30, y: 0 }, 0.45); });
  var tAn = t("analyse");
  pop("#zgSrc", tAn - 0.15, { y: 20, scale: 0.96 }, 0.5); sfx("success", tAn - 0.1, -17, 0);
  [["#r1", t("wer")], ["#r2", t("wonach")], ["#r3", p("was sie überzeugt")]].forEach(function (r, k) {
    tl.fromTo(r[0], { backgroundColor: "rgba(110,155,255,0)" }, { backgroundColor: "rgba(110,155,255,.13)", duration: 0.25, ease: "power1.out", immediateRender: false }, r[1] - 0.1);
    if (k < 2) tl.to(r[0], { backgroundColor: "rgba(110,155,255,0)", duration: 0.3, ease: "power1.in" }, (k === 0 ? t("wonach") : p("was sie überzeugt")) - 0.15);
    sfx("pop", r[1] - 0.08, -21, k);
  });
  leave("#zg", tE - 0.45, { y: -40 }, 0.4);

  /* ---------- E · Gezielte Anzeigen und passende Seiten ---------- */
  pop("#gg", tE - 0.05, { y: 60 }, 0.6); sfx("whoosh", tE - 0.03, -19, 0);
  var q = "küche nach maß lüneburg", tGo = t("google");
  K.typeText("#ggQ", q, tE + 0.35, 1.3); K.blink("#ggC", tE + 0.2, tGo - 0.3); sfx("typing", tE + 0.35, -23, 1);
  pop("#gg .gg__r", tGo - 0.35, { y: 20 }, 0.5); sfx("pop", tGo - 0.33, -18, 0);
  var tSo = t("sozialen");
  pop("#ig", tSo - 0.4, { y: 80, rotation: -4 }, 0.6); sfx("whoosh", tSo - 0.38, -19, 1);
  var tp = people("#tgt", 12), tGe = t("genau");
  pop("#tgt", tGe - 0.45, { y: 30 }, 0.5);
  [1, 6, 8].forEach(function (i, k) {
    K.cls(tp[i], "hit", tGe + 0.05 + k * 0.2);
    tl.fromTo(tp[i], { scale: 1 }, { scale: 1.18, duration: 0.18, yoyo: true, repeat: 1, ease: "sine.inOut", immediateRender: false }, tGe + 0.05 + k * 0.2);
    sfx("ping", tGe + 0.05 + k * 0.2, -20 - k, k);
  });
  tp.forEach(function (e, i) { if ([1, 6, 8].indexOf(i) < 0) tl.to(e, { opacity: 0.45, duration: 0.4 }, tGe + 0.1); });
  var tL = t("führen");
  leave("#gg", tL - 0.45, { y: -40 }, 0.36); leave("#ig", tL - 0.42, { x: -60 }, 0.36); leave("#tgt", tL - 0.42, { x: 60 }, 0.36);
  pop("#lp", tL - 0.12, { y: 70, scale: 0.96 }, 0.65); sfx("whoosh", tL - 0.1, -18, 1);
  ["#lp1", "#lp2", "#lp3"].forEach(function (s, k) { pop(s, tL + 0.55 + k * 0.28, { x: -24, y: 0 }, 0.45); sfx("pop", tL + 0.57 + k * 0.28, -21, k); });
  var tGb = t("gebaut");
  pop("#lpCta", tGb - 0.3, { scale: 0.85, y: 0 }, 0.5, "back.out(1.8)"); sfx("success", tGb - 0.25, -18, 2);
  leave("#lp", tF - 0.45, { y: -40 }, 0.38);

  /* ---------- F · Jede Anfrage im System ---------- */
  pop("#fn", tF - 0.12, { y: -40 }, 0.5); sfx("ping", tF - 0.1, -15, 0);
  var tSy = t("system");
  pop("#src", tSy - 0.45, { y: 70 }, 0.6); sfx("whoosh", tSy - 0.42, -19, 1);
  K.pulse("#fn", tSy - 0.1, 1.04, 0.14);
  $$("#src .sr").forEach(function (r, k) { pop(r, tSy - 0.1 + k * 0.16, { x: -30, y: 0 }, 0.45); });
  var tWe = t("welche");
  [["#q1", 14], ["#a1", 6], ["#q2", 9], ["#a2", 4], ["#q3", 2], ["#a3", 0]].forEach(function (c, k) { K.count(c[0], 0, c[1], tWe - 0.3 + (k >> 1) * 0.12, 1.1); });
  sfx("blips", tWe - 0.25, -21, 0);
  var tWi = t("wirklich");
  K.morph("#sr1", "sr--best", null, tWi - 0.1, 0.3);
  pop("#best", tWi + 0.05, { scale: 0.7, y: 0 }, 0.45, "back.out(2)"); sfx("success", tWi + 0.05, -16, 1);
  leave("#fn", tG - 0.45, { y: -30 }, 0.35); leave("#src", tG - 0.45, { y: 40 }, 0.38);

  /* ---------- G · Erfahrung ---------- */
  pop("#big", tG - 0.15, { scale: 0.9, y: 30 }, 0.6); sfx("whoosh", tG - 0.12, -19, 0);
  var t200 = t("200");
  K.count("#bigN", 0, 200, tG - 0.05, t200 - tG + 0.45, null, "power2.out");
  sfx("blips", tG, -22, 1); sfx("impact", t200 + 0.4, -15, 1);
  $$("#chn span").forEach(function (s, k) { pop(s, t("kampagnen") + k * 0.15, { y: 24 }, 0.45); sfx("pop", t("kampagnen") + 0.02 + k * 0.15, -21, k); });
  K.pulse("#big b", t("wirkt") - 0.05, 1.04, 0.16);
  leave("#big", cJ - 0.5, { y: -30 }, 0.38); leave("#chn", cJ - 0.48, { y: 30 }, 0.36);

  /* ---------- L · Abschluss ---------- */
  var n = W.length, ws = W.slice(n - 5).map(function (w) { return w.s; });
  SVC.end(K, ws);
});
