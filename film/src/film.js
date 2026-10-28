/* Zeitleiste des Erklärfilms. Jede Bewegung hängt an einem Wort des Sprechers (timing.json),
   damit Bild und Stimme zusammenpassen. Gerendert wird Bild für Bild über window.__seek(t). */
(function () {
  "use strict";
  var TM = window.TM, DUR = TM.duration;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var norm = function (s) { return String(s).toLowerCase().replace(/[.,!?:;„“"()–]/g, "").replace(/^-+/, "").trim(); };
  /* Zeitpunkt des n-ten Vorkommens eines Wortes */
  function t(word, n, edge) {
    n = n || 1; edge = edge || "s";
    var c = 0, k = norm(word);
    for (var i = 0; i < TM.words.length; i++) {
      if (norm(TM.words[i].w) === k && ++c === n) return TM.words[i][edge];
    }
    throw new Error("Wort fehlt: " + word + " #" + n);
  }
  function S(i) { return TM.sentences[i]; }

  gsap.defaults({ ease: "power3.out", duration: 0.7 });
  var tl = gsap.timeline({ paused: true });

  /* ---------- Bausteine ---------- */
  function scene(id, tIn, tOut, o) {
    o = o || {};
    var el = document.getElementById(id), cam = $(".cam", el);
    tl.set(el, { autoAlpha: 0 }, 0);
    tl.to(el, { autoAlpha: 1, duration: o.fadeIn || 0.55, ease: "power1.out" }, tIn);
    if (tOut != null) tl.to(el, { autoAlpha: 0, duration: o.fadeOut || 0.5, ease: "power1.in" }, tOut);
    var end = tOut != null ? tOut + 0.5 : DUR;
    tl.fromTo(cam, { scale: 1 }, { scale: 1 + (o.push == null ? 0.025 : o.push), duration: end - tIn, ease: "none" }, tIn);
    tl.fromTo(cam, { y: o.rise == null ? 26 : o.rise }, { y: 0, duration: 1.1, ease: "power3.out" }, tIn);
    return el;
  }
  function pop(sel, at, from, dur) {
    var el = typeof sel === "string" ? $(sel) : sel;
    var f = Object.assign({ autoAlpha: 0, y: 24 }, from || {}), to = { autoAlpha: 1, duration: dur || 0.7 };
    if ("x" in f) to.x = 0;
    if ("y" in f) to.y = 0;
    if ("scale" in f) to.scale = 1;
    if ("rotation" in f) to.rotation = f.rotationTo != null ? f.rotationTo : 0;
    delete f.rotationTo;
    tl.fromTo(el, f, to, at);
    return el;
  }
  function fadeOut(sel, at, to, dur) {
    tl.to(typeof sel === "string" ? $(sel) : sel, Object.assign({ autoAlpha: 0, duration: dur || 0.4, ease: "power1.in" }, to || {}), at);
  }
  function typeText(el, text, at, dur) {
    var o = { n: 0 };
    tl.to(o, { n: text.length, duration: dur, ease: "none", onUpdate: function () { el.textContent = text.slice(0, Math.round(o.n)); } }, at);
  }
  function count(el, from, to, at, dur, fmt) {
    var o = { v: from };
    fmt = fmt || function (v) { return String(Math.round(v)); };
    tl.to(o, { v: to, duration: dur, ease: "power2.out", onUpdate: function () { el.textContent = fmt(o.v); } }, at);
  }
  function setText(el, text, at) { var before = null; tl.call(function () { before = el.textContent; el.textContent = text; }, null, at); }
  function addClass(el, cls, at) { tl.call(function () { el.classList.add(cls); }, null, at); }
  function caret(el, from, to) {
    for (var x = from; x < to; x += 1.0) tl.set(el, { opacity: 0 }, x + 0.5).set(el, { opacity: 1 }, x + 1.0);
  }
  /* Kapitel-Hinweis */
  function chapter(text, at) {
    var c = $("#chap").cloneNode(true);
    c.removeAttribute("id"); $("span", c).textContent = text;
    $("#stage").appendChild(c);
    tl.set(c, { autoAlpha: 0 }, 0);
    tl.fromTo(c, { autoAlpha: 0, x: -14 }, { autoAlpha: 1, x: 0, duration: 0.6 }, at);
    tl.fromTo($("b", c), { scaleX: 0 }, { scaleX: 1, duration: 0.8, ease: "power2.out" }, at + 0.05);
    tl.to(c, { autoAlpha: 0, duration: 0.6, ease: "power1.in" }, at + 4.2);
  }
  /* Lage eines Elements relativ zur Bühne */
  var stageR = $("#stage").getBoundingClientRect();
  function rect(el) { var r = el.getBoundingClientRect(); return { x: r.left - stageR.left, y: r.top - stageR.top, w: r.width, h: r.height }; }

  /* ---------- Hintergrund: Licht wandert langsam ---------- */
  tl.fromTo(".bg .f1", { x: 0, y: 0 }, { x: 260, y: 170, duration: DUR, ease: "sine.inOut" }, 0);
  tl.fromTo(".bg .f2", { x: 0, y: 0, scale: 1 }, { x: -240, y: -150, scale: 1.12, duration: DUR, ease: "sine.inOut" }, 0);

  chapter("Die Ausgangslage", 0.6);
  chapter("Unser Ablauf", S(5).s + 0.2);
  chapter("Der Unterschied", S(10).s + 0.1);
  chapter("Ihr KI-Agent", S(14).s + 0.1);

  /* ======================================================= 1 · Suche, alte Website, Absprung */
  (function () {
    var tOut = S(3).s - 0.45;
    scene("s1", 0, tOut, { fadeIn: 0.2, rise: 0 });
    var ph = $("#ph1"), q = $("#q"), hit = $("#hit");
    /* Ringe an den echten Stellen der alten Seite */
    var scr = rect($(".ph__screen", ph));
    /* [Ring, Element, Abstand oben, seitlich, unten] – Kopf und Navigation berühren sich nicht */
    [["#ring1", ".old__top", 5, 6, -1], ["#ring2", ".old__nav", -1, 6, 4], ["#ring3", "#oldHours", 8, 8, 8]].forEach(function (a) {
      var r = rect($(a[1])), ring = $(a[0]), top = a[2], side = a[3], bot = a[4];
      var left = r.x - scr.x - side;
      ring.style.left = left + "px"; ring.style.top = (r.y - scr.y - top) + "px";
      ring.style.width = Math.min(r.w + side * 2, scr.w - left - 4) + "px"; ring.style.height = (r.h + top + bot) + "px";
    });
    tl.set(ph, { x: 235 }, 0);
    pop(ph, 0.15, { y: 60, scale: 0.97 }, 1.1);
    typeText(q, "Tischlerei in der Nähe", 1.0, 1.55);
    caret($("#caret"), 0.4, 3.0);
    tl.set("#caret", { opacity: 0 }, 3.1);
    $$(".res li").forEach(function (li, i) { pop(li, 2.75 + i * 0.16, { y: 18 }, 0.6); });
    /* Antippen und Laden */
    var tap = t("findet");
    tl.to(ph, { x: 0, duration: 0.9, ease: "power2.inOut" }, tap - 0.45);
    tl.fromTo("#tap", { autoAlpha: 0, scale: 0.5 }, { autoAlpha: 1, scale: 1.25, duration: 0.25, ease: "power2.out" }, tap);
    tl.to("#tap", { autoAlpha: 0, duration: 0.3 }, tap + 0.25);
    tl.to(hit, { backgroundColor: "#E9EEF8", duration: 0.2 }, tap);
    tl.set("#scrLoad", { autoAlpha: 1 }, tap + 0.4);
    tl.fromTo("#loadbar", { scaleX: 0 }, { scaleX: 0.86, duration: 1.1, ease: "power1.out" }, tap + 0.4);
    tl.fromTo("#spin", { rotation: 0 }, { rotation: 900, duration: 1.3, ease: "none" }, tap + 0.4);
    var shown = tap + 1.45;
    tl.set("#scrOld", { autoAlpha: 1 }, shown);
    tl.set("#scrLoad", { autoAlpha: 0 }, shown + 0.05);
    tl.fromTo("#old", { y: 0 }, { y: -120, duration: 1.4, ease: "power1.inOut" }, shown + 0.3);
    /* Besuchszeit läuft – dann Absprung */
    var vis = $("#visit");
    pop(vis, tap + 0.35, { x: 40, y: 0 }, 0.7);
    count($("#tm"), 0, 4, tap + 0.4, t("weg") - tap - 0.3, function (v) { return "0:0" + Math.floor(v); });
    setText($("#vstx"), "Sieht sich um", shown);
    var gone = t("weg");
    setText($("#vstx"), "Absprung", gone);
    addClass($("#vst"), "is-gone", gone);
    tl.fromTo("#vst", { scale: 1 }, { scale: 1.08, duration: 0.18, yoyo: true, repeat: 1, ease: "power1.inOut" }, gone);
    tl.to("#scrOld", { x: 400, duration: 0.45, ease: "power2.in" }, gone - 0.05);
    tl.set("#scrOld", { autoAlpha: 0 }, gone + 0.42);
    tl.to(hit, { opacity: 0.55, duration: 0.3 }, gone + 0.3);
    /* Blick auf die Mängel */
    var look = S(2).s - 0.3;
    fadeOut(vis, look - 0.2, { x: 40 }, 0.4);
    tl.to(ph, { x: -150, scale: 1.04, duration: 0.9, ease: "power2.inOut" }, look);
    tl.set("#old", { y: 0 }, look);
    tl.fromTo("#scrOld", { x: 380, autoAlpha: 0 }, { x: 0, autoAlpha: 1, duration: 0.6, ease: "power2.out", immediateRender: false }, look + 0.1);
    var flags = $$("#flags li"), hits = [t("veraltet"), t("handy"), t("öffnungszeiten", 1)];
    flags.forEach(function (li, i) {
      pop(li, hits[i] - 0.05, { x: 40, y: 0 }, 0.6);
      tl.fromTo("#ring" + (i + 1), { autoAlpha: 0, scale: 1.08 }, { autoAlpha: 1, scale: 1, duration: 0.45, ease: "back.out(2)" }, hits[i]);
    });
  })();

  /* ======================================================= 3 · Anfragen verstreut */
  (function () {
    var tIn = S(3).s - 0.45, tOut = S(5).s - 0.75;
    scene("s3", tIn, tOut, { rise: 0 });
    pop("#note", t("anfragen", 1), { y: 40, rotation: -10, rotationTo: -4 }, 0.8);
    pop("#cTel", t("telefon"), { y: 30, scale: 0.94 }, 0.7);
    pop("#cMail", t("e"), { y: 30, scale: 0.94 }, 0.7);
    pop("#cWa", t("whatsapp", 1), { y: 30, scale: 0.94 }, 0.7);
    /* leichtes Schweben */
    ["#note", "#cTel", "#cMail", "#cWa"].forEach(function (s, i) {
      tl.to(s, { y: (i % 2 ? -10 : 10), duration: 2.6, ease: "sine.inOut", yoyo: true, repeat: 1 }, tIn + 1.4 + i * 0.2);
    });
    /* … und gehen im Alltag unter */
    var sink = t("gehen");
    ["#note", "#cTel", "#cMail", "#cWa"].forEach(function (s, i) {
      tl.to(s, { y: "+=190", rotation: (i % 2 ? 7 : -9), opacity: 0.12, filter: "blur(6px)", duration: 1.7, ease: "power2.in" }, sink - 0.1 + i * 0.07);
    });
  })();

  /* ======================================================= 4 · Wende */
  (function () {
    var tIn = S(5).s - 0.5, tOut = S(6).s - 0.45;
    scene("s4", tIn, tOut, { push: 0.03, rise: 0 });
    tl.fromTo(".bg .f3", { autoAlpha: 0 }, { autoAlpha: 1, duration: 1.2, ease: "power1.out" }, tIn);
    tl.to(".bg .f3", { autoAlpha: 0, duration: 1.4, ease: "power1.inOut" }, tOut);
    pop("#turnMk", tIn + 0.1, { y: 0, scale: 0.86 }, 0.9);
    var words = $$("#turnHl .word"), at = [t("genau"), t("hier"), t("setzen"), t("wir", 1), t("an")];
    words.forEach(function (w, i) { pop(w, at[i] - 0.06, { y: 36 }, 0.55); });
  })();

  /* ======================================================= 5 · Erstgespräch und Angebot */
  (function () {
    var tIn = S(6).s - 0.45, tOut = S(8).s - 0.4;
    scene("s5", tIn, tOut, { rise: 18 });
    tl.set("#bk", { x: 370 }, 0);
    pop("#bk", tIn + 0.1, { y: 30 }, 0.9);
    tl.to("#bk", { x: 0, duration: 0.9, ease: "power3.inOut" }, t("innerhalb") - 0.35);
    var dayAt = t("kostenfreies", 1), slotAt = t("erstgespräch", 1);
    addClass($("#day"), "sel", dayAt);
    tl.fromTo("#day", { scale: 1 }, { scale: 1.12, duration: 0.16, yoyo: true, repeat: 1, ease: "power1.inOut" }, dayAt);
    addClass($("#slot"), "sel", slotAt);
    tl.fromTo("#slot", { scale: 1 }, { scale: 1.06, duration: 0.16, yoyo: true, repeat: 1, ease: "power1.inOut" }, slotAt);
    pop("#bkok", slotAt + 0.45, { y: 14 }, 0.5);
    pop("#offer", t("innerhalb"), { x: 70, y: 10, rotation: 2.5, rotationTo: 0 }, 0.9);
    pop("#h48", t("48"), { y: 0, scale: 0.7 }, 0.6);
    tl.to("#h48", { scale: 1.06, duration: 0.25, yoyo: true, repeat: 1, ease: "power1.inOut" }, t("48") + 0.6);
  })();

  /* ======================================================= 6 + 7 · Ablauf, neue Website, Kundensystem */
  (function () {
    var tIn = S(8).s - 0.4, tOut = S(10).s - 0.55;
    scene("s6", tIn, tOut, { push: 0.015, rise: 16 });
    var br = $("#br"), lis = $$("#rail li");
    pop("#rail", tIn + 0.15, { y: -16 }, 0.7);
    pop(br, tIn + 0.2, { y: 40 }, 0.9);
    /* Schritt 1: Ihre Kunden kennenlernen */
    var s1 = t("lernen"), s2 = t("gestalten"), s3 = t("bauen"), s4 = t("testen"), s5 = t("live");
    function step(i, at) {
      addClass(lis[i], "on", at);
      tl.fromTo($("i", lis[i]), { scale: 1 }, { scale: 1.18, duration: 0.18, yoyo: true, repeat: 1, ease: "power1.inOut" }, at);
      tl.to("#railFill", { scaleX: i / 4, duration: 0.6, ease: "power2.inOut" }, at - 0.15);
    }
    step(0, s1);
    $$(".pch").forEach(function (c, i) { pop(c, s1 + 0.15 + i * 0.28, { y: 18, scale: 0.95 }, 0.55); });
    /* Schritt 2: Gestaltung – Skizze, dann Design von links */
    step(1, s2);
    fadeOut("#persona", s2 - 0.05, { scale: 1.02 }, 0.4);
    tl.fromTo("#wf", { clipPath: "inset(0% 0% 0% 0%)" }, { clipPath: "inset(0% 0% 0% 100%)", duration: 1.25, ease: "power2.inOut" }, s2 + 0.45);
    tl.fromTo(".ns__title", { y: 18, opacity: 0.0 }, { y: 0, opacity: 1, duration: 0.8 }, s2 + 0.75);
    /* Schritt 3 und 4: Entwicklung und Test */
    step(2, s3);
    tl.fromTo("#nsForm", { y: 0 }, { y: -6, duration: 0.3, yoyo: true, repeat: 1, ease: "power1.inOut" }, s3 + 0.1);
    step(3, s4);
    $$("#checks span").forEach(function (c, i) { pop(c, s4 + 0.1 + i * 0.24, { x: 30, y: 0 }, 0.5); });
    /* Schritt 5: Live */
    step(4, s5);
    pop("#live", s5, { y: 0, scale: 0.7 }, 0.5);
    fadeOut("#checks", s5 + 0.5, { x: 20 }, 0.4);
    /* Dahinter: das eigene System */
    var sys = S(9).s;
    fadeOut("#rail", sys - 0.3, { y: -16 }, 0.4);
    var SC = 0.52, DX = -190, DY = 70;
    tl.to(br, { x: DX, y: DY, scale: SC, duration: 1.0, ease: "power3.inOut" }, sys - 0.1);
    pop("#db", sys + 0.5, { x: 70, y: 0 }, 0.9);
    /* jede Anfrage … fliegt aus dem Formular ins Dashboard */
    var brR = rect(br), sendR = rect($(".ns__send", br)), newR = rect($("#pcNew"));
    var sx = brR.x + DX + (sendR.x - brR.x) * SC, sy = brR.y + DY + (sendR.y - brR.y) * SC;
    var fly = $("#flyA"), aT = t("anfrage");
    tl.set(fly, { left: sx, top: sy, autoAlpha: 0, scale: 0.6 }, 0);
    tl.to(fly, { autoAlpha: 1, scale: 0.9, duration: 0.25, ease: "power1.out" }, aT - 0.1);
    tl.to(fly, { left: newR.x, top: newR.y, scale: 1, duration: 0.95, ease: "power2.inOut" }, aT + 0.1);
    tl.to(fly, { width: newR.w, duration: 0.95, ease: "power2.inOut" }, aT + 0.1);
    tl.set("#pcNew", { opacity: 1 }, aT + 1.05);
    tl.set(fly, { autoAlpha: 0 }, aT + 1.06);
    setText($("#kA"), "3", aT + 1.05); setText($("#nNeu"), "2", aT + 1.05);
    /* jeder Termin */
    var tT = t("termin");
    pop("#tagT", tT, { y: 8, scale: 0.8 }, 0.5);
    setText($("#kT"), "4", tT + 0.2);
    /* jeder Auftrag: Karte wandert in „Auftrag“ */
    var oT = t("auftrag"), a = rect($("#pcAng")), b = rect($("#slotAuf"));
    tl.to("#pcAng", { x: b.x - a.x, y: b.y - a.y, duration: 0.9, ease: "power3.inOut" }, oT - 0.1);
    pop("#tagO", oT + 0.65, { y: 8, scale: 0.8 }, 0.5);
    setText($("#nAng"), "0", oT + 0.5); setText($("#nAuf"), "1", oT + 0.5); setText($("#kO"), "6", oT + 0.6);
  })();

  /* ======================================================= 8 · Aus einer Hand */
  (function () {
    var tIn = S(10).s - 0.55, tOut = S(12).s - 0.5;
    scene("s8", tIn, tOut, { rise: 18 });
    pop("#handHl", S(10).s, { y: 30 }, 0.8);
    var hits = [t("website", 3), t("system", 2), t("pflege"), t("werbung")];
    ["#t1", "#t2", "#t3", "#t4"].forEach(function (s, i) { pop(s, hits[i] - 0.08, { y: 50, scale: 0.96 }, 0.7); });
    tl.to("#link", { scaleX: 1, duration: 1.0, ease: "power2.inOut" }, t("aufeinander") - 0.1);
    ["#t1", "#t2", "#t3", "#t4"].forEach(function (s, i) {
      tl.to(s, { borderColor: "rgba(170,190,220,.42)", duration: 0.4, ease: "power1.out" }, t("aufeinander") + i * 0.18);
    });
    pop("#contact", t("festen") - 0.1, { y: 40 }, 0.8);
  })();

  /* ======================================================= 9 · Erfahrung und Ergebnis */
  (function () {
    var tIn = S(12).s - 0.5, tOut = S(14).s - 0.5;
    scene("s9", tIn, tOut, { rise: 18 });
    pop("#big", tIn + 0.1, { y: 30 }, 0.8);
    count($("#n200"), 0, 200, t("200") - 0.2, 1.2);
    pop("#imp", S(13).s, { x: 70, y: 0 }, 0.9);
    pop("#ir1", S(13).s + 0.35, { y: 14 }, 0.6);
    var bars = $$("#ir1 .bar u i");
    tl.fromTo(bars[0], { scaleX: 0 }, { scaleX: 1, duration: 0.8, ease: "power2.out" }, S(13).s + 0.6);
    tl.fromTo(bars[1], { scaleX: 0 }, { scaleX: 1, duration: 1.3, ease: "power2.out" }, t("230") - 0.1);
    tl.fromTo("#ir1 > b", { autoAlpha: 0 }, { autoAlpha: 1, duration: 0.3 }, t("230") - 0.12);
    count($("#n230"), 0, 230, t("230") - 0.1, 1.3);
    ["#ir2", "#ir3", "#ir4"].forEach(function (s, i) { pop(s, S(13).s + 0.8 + i * 0.22, { y: 14 }, 0.55); });
    tl.to("#big", { opacity: 0.5, duration: 0.8, ease: "power1.inOut" }, S(13).s + 0.2);
  })();

  /* ======================================================= 10 · KI-Agent per WhatsApp */
  (function () {
    var tIn = S(14).s - 0.5, tOut = S(18).s - 0.5;
    scene("s10", tIn, tOut, { rise: 18 });
    pop("#ph2", tIn + 0.1, { y: 60 }, 1.0);
    pop("#site", t("ändert") - 0.2, { x: 70, y: 0 }, 0.9);
    pop("#ch1", t("öffnungszeiten", 2), { y: 10, scale: 0.9 }, 0.45);
    pop("#ch2", t("angebot", 2), { y: 10, scale: 0.9 }, 0.45);
    pop("#ch3", t("fotos"), { y: 10, scale: 0.9 }, 0.45);
    var msg = "Ab Montag haben wir 8–18 Uhr geöffnet. Bitte auf der Website ändern.";
    var tw = t("schreiben");
    tl.to("#ch1", { backgroundColor: "rgba(0,168,132,.25)", borderColor: "rgba(0,168,132,.7)", duration: 0.3 }, tw - 0.15);
    typeText($("#waTx"), msg, tw, 1.7);
    var sent = tw + 1.9;
    setText($("#waTx"), "", sent);
    pop("#bMe", sent, { y: 24 }, 0.45);
    fadeOut(".wa__chips", sent, {}, 0.3);
    setText($("#waSt"), "schreibt …", sent + 0.35);
    pop("#dots", sent + 0.35, { y: 12 }, 0.35);
    $$("#dots i").forEach(function (d, i) {
      tl.to(d, { y: -6, duration: 0.25, yoyo: true, repeat: 3, ease: "sine.inOut" }, sent + 0.5 + i * 0.12);
    });
    var done = t("pflegt") - 0.15;
    tl.to("#dots", { autoAlpha: 0, height: 0, paddingTop: 0, paddingBottom: 0, duration: 0.2 }, done - 0.05);
    setText($("#waSt"), "online", done);
    pop("#bIn", done, { y: 24 }, 0.5);
    /* Website zeigt die Änderung */
    var up = done + 0.35;
    tl.fromTo("#flash", { autoAlpha: 0 }, { autoAlpha: 1, duration: 0.25, yoyo: true, repeat: 1, ease: "power1.inOut" }, up);
    fadeOut("#rowOld", up + 0.15, { y: -10 }, 0.3);
    pop("#rowNew", up + 0.3, { y: 12 }, 0.45);
    pop("#upd", up + 0.45, { y: 0, scale: 0.7 }, 0.45);
    tl.to("#site", { y: -8, duration: 0.35, yoyo: true, repeat: 1, ease: "power1.inOut" }, up);
  })();

  /* ======================================================= 11 · Dashboard und Team */
  (function () {
    var tIn = S(18).s - 0.5, tOut = S(20).s - 0.65;
    scene("s11", tIn, tOut, { rise: 18 });
    tl.set("#db2", { x: 280 }, 0);
    pop("#db2", tIn + 0.1, { y: 40 }, 0.9);
    tl.to("#db2", { x: 0, duration: 0.9, ease: "power3.inOut" }, t("team") - 0.9);
    var cmd = "Neue Leistung „Treppen nach Maß“ auf die Website";
    typeText($("#cmd"), cmd, S(18).s + 0.3, 1.8);
    caret($("#caret2"), tIn, S(18).s + 2.4);
    tl.set("#caret2", { opacity: 0 }, S(18).s + 2.5);
    pop("#ans", S(18).s + 2.45, { y: 16 }, 0.6);
    pop("#add", S(18).s + 2.85, { y: -10 }, 0.5);
    pop("#team", t("team") - 0.6, { x: 70, y: 0 }, 0.9);
    $$("#team li").forEach(function (li, i) { pop(li, t("team") - 0.2 + i * 0.25, { x: 20, y: 0 }, 0.5); });
  })();

  /* ======================================================= 12 · Abschluss */
  (function () {
    var tIn = S(20).s - 0.6;
    scene("s12", tIn, null, { push: 0.02, rise: 0 });
    tl.fromTo(".bg .f3", { autoAlpha: 0 }, { autoAlpha: 0.9, duration: 2.0, ease: "power1.out", immediateRender: false }, tIn);
    pop("#endMk", t("medialeit") - 0.1, { y: 0, scale: 0.86 }, 1.0);
    pop("#endWm", t("medialeit") + 0.2, { y: 18 }, 0.9);
    pop("#endTag", t("damit") - 0.05, { y: 22 }, 0.8);
    pop("#endCta", t("buchen") - 0.1, { y: 16, scale: 0.94 }, 0.7);
    pop("#endUrl", t("buchen") + 0.5, { y: 10 }, 0.6);
  })();

  tl.set({}, {}, DUR);
  window.__dur = DUR;
  window.__seek = function (s) { tl.seek(s, false); return true; };
  window.__tl = tl;
  window.__ready = true;
})();
