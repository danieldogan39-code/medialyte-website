/* Gemeinsame Abläufe der Leistungsfilme: Kapitelzeile, Einstieg ab Bild 0, Abschluss mit Logo auf dem letzten Musikschlag. */
window.SVC = {
  /* Kapitelzeile oben links: „1  Website-Erstellung“, Fortschrittsbalken läuft bis zum Abschluss */
  chap: function (K, n, title, t0, t1) {
    K.$("#chapN").textContent = n; K.$("#chapT").textContent = title;
    K.vis("#chap", 0, t1 + 0.6);
    K.tl.fromTo("#chap", { autoAlpha: 1, x: 0 }, { autoAlpha: 1, x: 0, duration: 0.01 }, 0);
    K.tl.fromTo("#chapB", { scaleX: 0 }, { scaleX: 1, duration: t1 - t0, ease: "none" }, t0);
    K.tl.to("#chap", { autoAlpha: 0, y: -16, duration: 0.45, ease: "power2.in" }, t1);
  },
  /* Einstieg: die erste Zeile steht ab Bild 0 (setzt sich nur), weitere Zeilen steigen mit dem Sprecher auf */
  hook: function (K, sel, times) {
    var lines = K.$$(sel + " .ln");
    lines.forEach(function (ln, i) {
      var ws = K.words(ln);
      if (i === 0) {
        K.tl.fromTo(ln, { y: 14, scale: 1.03, transformOrigin: "0% 50%" }, { y: 0, scale: 1, duration: 0.9, ease: "power3.out" }, 0);
      } else {
        ws.forEach(function (w, k) { K.tl.fromTo(w, { yPercent: 140 }, { yPercent: 0, duration: 0.7, ease: "power4.out" }, (times[i] || 0) + k * 0.06); });
      }
    });
  },
  /* Abschluss: Logo-Zeichen zuerst (Schlag), dann Wortmarke, Satz, Knopf */
  end: function (K, tagTimes, glowAt) {
    var TM = window.TM, cJ = TM.music.cJ, SW = K.SW;
    var a = cJ - 0.08;
    K.vis("#scL", a - 0.6, null);
    K.tl.fromTo("#endGlow", { autoAlpha: 0, scale: 0.8 }, { autoAlpha: 1, scale: 1, duration: 2.2, ease: "power2.out" }, a - 0.3);
    var mk = K.rect("#endMk"), mx = (SW / 2 - (mk.x + mk.w / 2));
    K.pop("#endMk", a, { y: 0, scale: 0.8, x: mx, to: { x: mx } }, 0.8, "power3.out");
    K.tl.to("#endMk", { x: 0, duration: 0.72, ease: "power3.inOut" }, a + 0.45);
    K.tl.fromTo("#endWm", { clipPath: "inset(-10% -2% 100% -2%)", y: 70 }, { clipPath: "inset(-10% -2% -12% -2%)", y: 0, duration: 0.8, ease: "power4.out" }, a + 0.85);
    K.sfx("impact", cJ, -15, 2);
    K.reveal("#endTag", tagTimes.map(function (x) { return x - 0.05; }), 0.7);
    var last = tagTimes[tagTimes.length - 1];
    K.pop("#endCta", last + 0.35, { y: 20, scale: 0.94 }, 0.6);
    K.pop("#endUrl", last + 0.7, { y: 10 }, 0.5);
    K.sfx("pop", last + 0.37, -18, 2);
  }
};
