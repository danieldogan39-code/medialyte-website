/* Film 3 · KI-Agent – Zeitleiste */
FILM(function (K) {
  var tl = K.tl, t = K.t, p = K.p, $ = K.$, $$ = K.$$, pop = K.pop, leave = K.leave, sfx = K.sfx, vis = K.vis;
  var M = window.TM.music, T1 = M.T1, cJ = M.cJ, W = window.TM.words;

  var tB = t("früher"), tC = t("selbst"), tD = t("oder", 1), tF = p("keine fachbegriffe"), tG = p("und wenn");
  vis("#scA", 0, tB); vis("#scB", tB - 0.5, tC + 0.1); vis("#scC", tC - 0.5, tD + 0.1); vis("#scD", tD - 0.5, T1 + 0.1);
  vis("#scE", T1 - 0.5, tF + 0.1); vis("#scF", tF - 0.5, tG + 0.1); vis("#scG", tG - 0.5, cJ);
  SVC.chap(K, "3", "KI-Agent", 0, cJ - 0.7);

  /* ---------- A · Einstieg ---------- */
  tl.fromTo("#hkA", { y: 14, scale: 1.03, transformOrigin: "0% 50%" }, { y: 0, scale: 1, duration: 0.9 }, 0);
  pop("#hrs", 0.02, { y: 40 }, 0.7);
  sfx("impact", 0.0, -16, 0);
  var tA = t("änderung", 1);
  tl.fromTo("#h16", { "--k": 0 }, { "--k": 1, duration: 0.3, ease: "power2.out" }, tA - 0.1);
  tl.to("#h16", { autoAlpha: 0, y: -26, duration: 0.3, ease: "power2.in" }, tA + 0.35);
  pop("#h18", tA + 0.45, { y: 30 }, 0.45);
  sfx("swoosh", tA - 0.08, -21, 0); sfx("pop", tA + 0.45, -19, 1);
  pop("#price", t("website", 1) - 0.25, { scale: 0.5, rotation: -24, y: 0 }, 0.8, "back.out(1.8)");
  sfx("pop", t("website", 1) - 0.22, -17, 2);
  K.conceal("#hkA", tB - 0.45, 0.03); leave("#hrs", tB - 0.45, { y: 40 }, 0.38); leave("#price", tB - 0.42, { scale: 0.7 }, 0.36);

  /* ---------- B · Zwei Möglichkeiten ---------- */
  pop("#perB", tB - 0.2, { y: 70, scale: 0.94 }, 0.75); sfx("whoosh", tB - 0.15, -18, 0);
  var tZ = t("zwei");
  pop("#o1", tZ - 0.05, { y: 40 }, 0.55); pop("#o2", tZ + 0.25, { y: 40 }, 0.55);
  sfx("pop", tZ - 0.03, -19, 0); sfx("pop", tZ + 0.27, -19, 1);
  leave("#perB", tC - 0.5, { y: -40, scale: 0.96 }, 0.4); leave("#o2", tC - 0.45, { x: 60 }, 0.35); leave("#o1", tC - 0.45, { y: -30 }, 0.35);

  /* ---------- C · Selbst machen ---------- */
  pop("#ol1", tC - 0.2, { x: -30, y: 0 }, 0.5);
  pop("#cms", tC - 0.1, { y: 70 }, 0.7); sfx("whoosh", tC - 0.05, -17, 1);
  var tS = t("system", 1);
  pop("#cmsW", tS - 0.2, { y: -10 }, 0.4); sfx("blips", tS - 0.18, -22, 0);
  tl.fromTo("#blkHi", { backgroundColor: "#ffffff" }, { backgroundColor: "#EAF2FB", duration: 0.3 }, tS + 0.1);
  pop("#cmsE", t("einarbeiten") + 0.25, { y: 10 }, 0.4); sfx("pop", t("einarbeiten") + 0.25, -18, 3);
  var tAb = t("abend");
  pop("#clk", tAb - 0.6, { y: 40 }, 0.5);
  K.count("#clkT", 0, 220, tAb - 0.45, 1.6, function (v) { var m = 19 * 60 + Math.round(v / 5) * 5; return Math.floor(m / 60) + ":" + ("0" + (m % 60)).slice(-2); }, "power1.inOut");
  pop("#loss", t("verlieren") - 0.05, { x: -20, y: 0 }, 0.5); sfx("swoosh", t("verlieren"), -20, 2);
  leave("#cms", tD - 0.42, { y: -40 }, 0.38); leave("#clk", tD - 0.42, { y: 30 }, 0.35); leave("#loss", tD - 0.42, { y: 30 }, 0.35); leave("#ol1", tD - 0.42, { y: -20 }, 0.3);

  /* ---------- D · Agentur fragen ---------- */
  pop("#ol2", tD - 0.1, { x: -30, y: 0 }, 0.5);
  var tAg = t("agentur", 1);
  pop("#mail", tAg - 0.3, { y: 60 }, 0.6); sfx("whoosh", tAg - 0.25, -18, 0);
  K.typeText("#mailTx", "Hallo, bitte ändern Sie unsere Öffnungszeiten auf 7–18 Uhr. Danke!", tAg + 0.15, 1.2);
  sfx("typing", tAg + 0.15, -24, 0);
  var tW = t("warten", 1);
  K.pulse("#mailSend", tW - 0.35, 0.94, 0.1); sfx("click", tW - 0.33, -14, 0);
  pop("#wait", tW - 0.05, { y: 30 }, 0.5);
  K.text("#waitD", [[0, "Tag 1"], [tW + 0.45, "Tag 2"], [tW + 0.9, "Tag 3"]]);
  sfx("blips", tW + 0.45, -23, 1);
  var tJ = t("jede");
  pop("#inv", tJ - 0.15, { y: 80, rotation: -8 }, 0.7); sfx("paper", tJ - 0.12, -16, 0);
  pop("#invSt", t("bezahlen") - 0.05, { scale: 1.7, y: 0 }, 0.35, "power4.in"); sfx("impact", t("bezahlen") + 0.27, -18, 1);
  leave("#mail", T1 - 0.45, { y: -40 }, 0.38); leave("#wait", T1 - 0.45, { y: 30 }, 0.35); leave("#inv", T1 - 0.42, { y: 40 }, 0.38); leave("#ol2", T1 - 0.45, { y: -20 }, 0.3);

  /* ---------- E · Heute: per WhatsApp (Aufbruch der Musik) ---------- */
  tl.fromTo("#lt3", { opacity: 0 }, { opacity: 1, duration: 0.35 }, T1 - 0.04); tl.to("#lt3", { opacity: 0, duration: 2.2, ease: "power1.inOut" }, T1 + 0.5);
  sfx("riser", T1 - 0.02, -16, 0); sfx("impact", T1 - 0.01, -11, 0);
  pop("#phE", T1 - 0.12, { y: 140 }, 0.85);
  pop("#ws", T1 + 0.3, { x: 90, y: 0 }, 0.75);
  var msg = "Ab Montag haben wir bis 18 Uhr geöffnet. Und bitte das neue Küchenfoto in die Galerie.";
  var tSend = t("worten") - 0.05, tType = t("schreibt") + 0.1;
  K.typeText("#waTx", msg, tType, tSend - tType - 0.25, tSend);
  sfx("typing", tType, -23, 1); sfx("typing", tType + 1.5, -24, 2);
  K.grow("#bMe", tSend, 0.42, { marginTop: [0, 10] }); sfx("whoosh", tSend, -20, 1);
  K.grow("#bImg", tSend + 0.32, 0.42, { marginTop: [0, 10] }); sfx("pop", tSend + 0.32, -20, 0);
  var tR = t("kurz") + 0.05;
  K.vis("#waOn", 0, tSend + 0.6); K.vis("#waTy", tSend + 0.6, tR);
  K.grow("#bIn", tSend + 0.7, 0.42, { marginTop: [0, 10] });
  K.vis("#dots", tSend + 0.7, tR); K.vis("#bInTx", tR, null);
  $$("#dots i").forEach(function (d, k) { tl.fromTo(d, { y: 0 }, { y: -6, duration: 0.25, yoyo: true, repeat: 5, ease: "sine.inOut", immediateRender: false }, tSend + 0.75 + k * 0.12); });
  sfx("ping", tR, -15, 2);
  var tO = t("online") - 0.25;
  tl.to("#wOld", { yPercent: -100, autoAlpha: 0, duration: 0.45, ease: "power3.in" }, tO);
  tl.fromTo("#wNew", { yPercent: 100, autoAlpha: 0 }, { yPercent: 0, autoAlpha: 1, duration: 0.5, ease: "power3.out" }, tO + 0.2);
  tl.fromTo("#flash", { opacity: 0 }, { opacity: 1, duration: 0.2, yoyo: true, repeat: 1 }, tO + 0.2);
  pop("#upd", tO + 0.35, { scale: 0.6, y: 0 }, 0.45, "back.out(2)");
  pop("#gNew", tO + 0.55, { scale: 0.6, y: 0 }, 0.55, "back.out(1.6)");
  sfx("success", tO + 0.3, -16, 0);
  leave("#phE", tF - 0.45, { x: -120 }, 0.4); leave("#ws", tF - 0.45, { x: 120 }, 0.4);

  /* ---------- F · Vorteile ---------- */
  [["#b1", t("fachbegriffe")], ["#b2", t("warten", 2)], ["#b3", t("extrakosten")]].forEach(function (b, k) {
    pop(b[0], b[1] - 0.3, { x: -40, y: 0 }, 0.55); sfx("pop", b[1] - 0.28, -18, k);
  });
  var tKa = t("ki-agent", 1);
  pop("#abo", tKa - 0.35, { y: 60 }, 0.65); sfx("whoosh", tKa - 0.3, -19, 0);
  K.pulse("#aboKi em", t("enthalten") - 0.05, 1.12, 0.16); sfx("success", t("enthalten"), -17, 1);
  ["#b1", "#b2", "#b3"].forEach(function (s, k) { leave(s, tG - 0.45 + k * 0.03, { x: -50 }, 0.35); }); leave("#abo", tG - 0.42, { y: 40 }, 0.38);

  /* ---------- G · Team ---------- */
  pop("#team", tG - 0.12, { y: 60, scale: 0.97 }, 0.7); sfx("whoosh", tG - 0.1, -18, 1);
  $$("#team li").forEach(function (li, k) { pop(li, t("team") - 0.1 + k * 0.16, { x: 30, y: 0 }, 0.45); });
  sfx("swoosh", t("team"), -19, 3);
  leave("#team", cJ - 0.5, { y: -30, scale: 0.97 }, 0.42);

  /* ---------- L · Abschluss ---------- */
  var n = W.length, ws = W.slice(n - 8).map(function (w) { return w.s; });
  SVC.end(K, [ws[0], ws[1], ws[2], ws[3] - 0.08, ws[3], ws[4], ws[5], ws[6], ws[7]]);
});
