/* Film 1 · Website-Erstellung – Zeitleiste. Jede Bewegung hängt an einem Wort des Sprechers. */
FILM(function (K) {
  var tl = K.tl, t = K.t, p = K.p, $ = K.$, $$ = K.$$, pop = K.pop, leave = K.leave, sfx = K.sfx, vis = K.vis;
  var M = window.TM.music, T1 = M.T1, cJ = M.cJ;
  var W = window.TM.words;

  /* Szenen sichtbar */
  vis("#scA", 0, 4.9); vis("#scB", 4.3, 8.9); vis("#scC", 7.9, T1 + 0.4); vis("#scD", T1 - 0.5, p("wir arbeiten") + 0.2);
  vis("#scE", p("wir arbeiten") - 0.6, p("dann analysieren") + 0.3); vis("#scF", p("dann analysieren") - 0.5, p("daraus") + 0.2);
  vis("#scG", p("daraus") - 0.6, p("heute melden") + 0.3); vis("#scH", p("heute melden") - 0.5, cJ - 0.05);
  SVC.chap(K, "1", "Website-Erstellung", 0, cJ - 0.7);

  /* ---------- A · Einstieg ---------- */
  var crowd = $("#crowd");
  for (var i = 0; i < 28; i++) { var d = document.createElement("i"); d.className = "pp"; crowd.appendChild(d); }
  var pps = $$(".pp");
  tl.fromTo("#hkA", { y: 14, scale: 1.03, transformOrigin: "0% 50%" }, { y: 0, scale: 1, duration: 0.9 }, 0);
  pps.forEach(function (e, k) { tl.fromTo(e, { autoAlpha: 0, y: 26 }, { autoAlpha: 1, y: 0, duration: 0.5 }, 0.02 + k * 0.014); });
  sfx("impact", 0.0, -16, 0);
  var tAll = t("allen");
  tl.to(pps, { color: "rgba(110,155,255,.95)", duration: 0.35, ease: "power1.out", stagger: { each: 0.012, from: "random" } }, tAll - 0.1);
  sfx("blips", tAll - 0.05, -22, 1);
  K.conceal("#hkA", t("dann") - 0.42, 0.03);
  K.reveal("#hkB .ln:nth-child(1)", t("dann") - 0.05, 0.7, 0.07);
  K.reveal("#hkB .ln:nth-child(2)", t("niemanden") - 0.06, 0.75);
  tl.to(pps, { color: "rgba(150,178,224,.10)", y: 10, duration: 0.5, ease: "power2.out", stagger: { each: 0.02, from: "random" } }, t("niemanden") - 0.1);
  sfx("swoosh", t("niemanden"), -20, 1);
  K.conceal("#hkB", t("das", 1) - 0.45, 0.03);
  leave("#crowd", t("das", 1) - 0.45, { y: 50 }, 0.4);

  /* ---------- B · Sophia ---------- */
  var tS = t("sophia", 1);
  pop("#per", tS - 0.32, { y: 90, scale: 0.92 }, 0.85);
  sfx("whoosh", tS - 0.3, -17, 0);
  pop("#trade", t("küchen") - 0.1, { y: 26, scale: 0.9 }, 0.6);
  sfx("pop", t("küchen") - 0.08, -18, 0);
  var tC = t("auf", 1);
  tl.to("#per", { scale: 0.18, x: -380, y: -420, autoAlpha: 0, duration: 0.55, ease: "power3.in" }, tC - 0.55);
  leave("#trade", tC - 0.55, { y: 30 }, 0.3);

  /* ---------- C · Die alte Website ---------- */
  pop("#whoC", tC - 0.12, { x: -40, y: 0 }, 0.6);
  pop("#phC", tC - 0.25, { x: 160, y: 0 }, 0.8);
  sfx("swoosh", tC - 0.2, -18, 2);
  tl.to("#oldC", { y: -150, duration: 3.4, ease: "sine.inOut" }, t("viel") - 0.2);
  pop("#has h6", t("viel") - 0.15, { y: 14 }, 0.5);
  ["#h1", "#h2", "#h3"].forEach(function (s, k) { pop(s, t("werkstatt") - 0.75 + k * 0.28, { x: -30, y: 0 }, 0.5); sfx("pop", t("werkstatt") - 0.73 + k * 0.28, -22, k); });
  pop("#asks h6", t("wenig") - 0.1, { y: 14 }, 0.5);
  var tq = t("kunden", 1) - 0.35;
  ["#q1", "#q2", "#q3"].forEach(function (s, k) {
    pop(s, tq + k * 0.42, { y: 24, scale: 0.94 }, 0.55);
    tl.fromTo(s + " .mk", { scale: 0.4, autoAlpha: 0 }, { scale: 1, autoAlpha: 1, duration: 0.4, ease: "back.out(2.2)" }, tq + k * 0.42 + 0.55);
    sfx("pop", tq + k * 0.42, -19, k + 1);
  });
  var tCo = T1 - 0.48;
  leave("#phC", tCo, { x: 200 }, 0.42); leave("#has", tCo, { x: -60 }, 0.4); leave("#asks", tCo + 0.04, { x: -60 }, 0.4); leave("#whoC", tCo, { y: -20 }, 0.35);

  /* ---------- D · Die Wende (Aufbruch der Musik) ---------- */
  tl.fromTo("#lt3", { opacity: 0 }, { opacity: 1, duration: 0.35, ease: "power2.out" }, T1 - 0.04);
  tl.to("#lt3", { opacity: 0, duration: 2.2, ease: "power1.inOut" }, T1 + 0.5);
  sfx("riser", T1 - 0.02, -16, 0); sfx("impact", T1 - 0.01, -11, 0);
  var dl = $$("#dkt .ln");
  K.reveal(dl[0], t("nicht", 1) - 0.06, 0.7, 0.07);
  pop("#wfc", t("design") - 0.45, { y: 40 }, 0.6);
  tl.fromTo("#wfcX", { scaleX: 0 }, { scaleX: 1, duration: 0.35, ease: "power2.out" }, t("design") + 0.15);
  tl.to("#wfc", { opacity: 0.38, duration: 0.5 }, t("design") + 0.4);
  sfx("swoosh", t("design") + 0.12, -21, 3);
  K.reveal(dl[1], t("sondern") - 0.05, 0.7, 0.07);
  K.reveal(dl[2], t("unternehmen") - 0.06, 0.75);
  pop("#coD", t("unternehmen") - 0.2, { y: 60, scale: 0.95 }, 0.75);
  sfx("success", t("unternehmen") + 0.1, -19, 0);
  var tE = p("wir arbeiten");
  K.conceal("#dkt", tE - 0.48, 0.02); leave("#wfc", tE - 0.48, { y: 40 }, 0.38); leave("#coD", tE - 0.45, { y: 40 }, 0.4);

  /* ---------- E · Einarbeiten ---------- */
  K.reveal("#ehl", tE - 0.05, 0.75);
  var q1 = p("was wollen"), q2 = p("an wen"), q3 = p("und warum");
  pop("#qa1", q1 - 0.15, { y: 50 }, 0.6); pop("#qa2", q2 - 0.15, { y: 50 }, 0.6); pop("#qa3", q3 - 0.15, { y: 50 }, 0.6);
  K.typeText("#a1", "Küchen nach Maß und Einbauschränke", q1 + 0.85, 0.9);
  K.typeText("#a2", "Familien, die bauen oder renovieren", q2 + 0.35, 0.95);
  K.typeText("#a3", "Meisterbetrieb mit eigener Werkstatt", q3 + 1.2, 0.95);
  sfx("typing", q1 + 0.85, -24, 0); sfx("typing", q2 + 0.35, -24, 1); sfx("typing", q3 + 1.2, -24, 2);
  [q1, q2, q3].forEach(function (x, k) { sfx("pop", x - 0.13, -20, k); });
  var tF = p("dann analysieren");
  K.conceal("#ehl", tF - 0.45, 0.02);
  ["#qa1", "#qa2", "#qa3"].forEach(function (s, k) { leave(s, tF - 0.45 + k * 0.05, { y: -40 }, 0.36); });

  /* ---------- F · Zielgruppe ---------- */
  pop("#tgp", tF - 0.02, { y: 70, scale: 0.97 }, 0.75);
  sfx("whoosh", tF, -17, 1);
  var rs = [["#r1", t("fragen")], ["#r2", t("zweifel")], ["#r3", p("wie sie sucht")], ["#r4", p("was sie überzeugt")]];
  rs.forEach(function (r, k) {
    pop(r[0], tF + 0.5 + k * 0.12, { y: 20 }, 0.5);
    pop(r[0] + " .fill", r[1] - 0.12, { x: 30, y: 0 }, 0.5);
    leave(r[0] + " .skl", r[1] - 0.12, {}, 0.25);
    tl.to(r[0] + " .ic", { opacity: 1, duration: 0.3 }, r[1] - 0.1);
    sfx("pop", r[1] - 0.1, -19, k);
  });
  K.typeText("#sq", "küche nach maß lüneburg", p("wie sie sucht") + 0.25, 1.05);
  K.blink("#sqc", p("wie sie sucht") + 0.1, p("daraus"));
  sfx("typing", p("wie sie sucht") + 0.25, -23, 1);
  $$("#r4 .zg__c span").forEach(function (e, k) { pop(e, p("was sie überzeugt") + 0.35 + k * 0.16, { y: 14, scale: 0.9 }, 0.45); });
  var tG = p("daraus");
  leave("#tgp", tG - 0.45, { y: -50, scale: 0.97 }, 0.42);

  /* ---------- G · Die neue Website ---------- */
  pop("#phG", tG - 0.15, { y: 140 }, 0.85);
  sfx("whoosh", tG - 0.1, -16, 0);
  var nsm = $("#nsm"), cta = $("#nsCta"), faq = $("#nsFaq");
  var viewH = 930 - 26 - 64;
  var yFaq = -(faq.offsetTop - 20), yCta = -(cta.offsetTop + cta.offsetHeight + 30 - viewH);
  var tSp = t("sprache"), tAn = t("antworten"), tAf = t("anfrage");
  pop("#l1", tSp - 0.12, { x: -40, y: 0 }, 0.55); K.cls("#nsHero", "hl", tSp - 0.05, tAn - 0.4); sfx("pop", tSp - 0.1, -18, 0);
  tl.to(nsm, { y: yFaq, duration: 0.8, ease: "power2.inOut" }, tAn - 0.75);
  pop("#l2", tAn - 0.12, { x: -40, y: 0 }, 0.55); K.cls("#fq1", "hl", tAn - 0.05, p("einem klaren") - 0.3); sfx("pop", tAn - 0.1, -18, 1);
  tl.to(nsm, { y: yCta, duration: 0.8, ease: "power2.inOut" }, p("einem klaren") - 0.55);
  pop("#l3", tAf - 0.3, { x: -40, y: 0 }, 0.55); K.cls("#nsCta", "hl", tAf - 0.2, null); sfx("pop", tAf - 0.28, -18, 2);
  var cr = cta.getBoundingClientRect(), sr = $("#phG .ph__screen").getBoundingClientRect();
  var tap = $("#tapG"); tap.style.left = (cta.offsetLeft + cta.offsetWidth * 0.62) + "px"; tap.style.top = (64 + cta.offsetTop + yCta + cta.offsetHeight / 2) + "px";
  tl.fromTo(tap, { autoAlpha: 0.9, scale: 0.4 }, { autoAlpha: 0, scale: 1.6, duration: 0.6, ease: "power2.out" }, tAf + 0.35);
  K.pulse("#nsCta", tAf + 0.32, 0.95, 0.12); sfx("tap", tAf + 0.33, -12, 0);
  var tH = p("heute melden");
  leave("#phG", tH - 0.45, { x: 180 }, 0.42); ["#l1", "#l2", "#l3"].forEach(function (s, k) { leave(s, tH - 0.45 + k * 0.04, { x: -50 }, 0.38); });

  /* ---------- H · Ergebnis ---------- */
  pop("#perH", tH - 0.15, { y: 60, scale: 0.94 }, 0.75);
  sfx("whoosh", tH - 0.1, -18, 1);
  var tk = t("kunden", 3);
  ["#n1", "#n2", "#n3"].forEach(function (s, k) { pop(s, tk - 0.25 + k * 0.38, { y: 40, scale: 0.96 }, 0.55); sfx("ping", tk - 0.23 + k * 0.38, -20, k); });
  sfx("success", tk + 0.9, -18, 2);
  leave("#perH", cJ - 0.55, { y: -30, scale: 0.97 }, 0.4); leave("#notes", cJ - 0.5, { y: 30 }, 0.38);

  /* ---------- L · Abschluss ---------- */
  var n = W.length, tags = W.slice(n - 5).map(function (w) { return w.s; });
  SVC.end(K, tags);
});
