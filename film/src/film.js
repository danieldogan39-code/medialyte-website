/* Zeitleiste des Erklärfilms. Jede Bewegung hängt an einem Wort des Sprechers (timing.json),
   damit Bild und Stimme zusammenpassen. Gerendert wird Bild für Bild über window.__seek(t).
   Regeln für saubere Bilder: Szenen überblenden nie ineinander (die alte ist weg, bevor die neue kommt),
   kein Dauer-Zoom (Schrift würde flimmern), Elemente bewegen sich nur über transform und opacity –
   ausgenommen Chatblasen und Hinweise, die beim Erscheinen ihren Platz sanft aufziehen. */
(function () {
  "use strict";
  var TM = window.TM, DUR = TM.duration;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var norm = function (s) { return String(s).toLowerCase().replace(/[.,!?:;„“"()–…%]/g, "").replace(/^-+/, "").trim(); };
  var WN = TM.words.map(function (w) { return norm(w.w); });
  /* Zeitpunkt des n-ten Vorkommens eines Wortes */
  function t(word, n, edge) {
    n = n || 1; edge = edge || "s";
    var c = 0, k = norm(word);
    for (var i = 0; i < WN.length; i++) if (WN[i] === k && ++c === n) return TM.words[i][edge];
    throw new Error("Wort fehlt: " + word + " #" + n);
  }
  /* Beginn einer Wortfolge („und die anfragen“) */
  function p(phrase) {
    var ks = phrase.split(" ").map(norm);
    for (var i = 0; i + ks.length <= WN.length; i++) {
      var ok = true;
      for (var j = 0; j < ks.length; j++) if (WN[i + j] !== ks[j]) { ok = false; break; }
      if (ok) return TM.words[i].s;
    }
    throw new Error("Wortfolge fehlt: " + phrase);
  }

  gsap.defaults({ ease: "power3.out", duration: 0.7 });
  var tl = gsap.timeline({ paused: true });
  var OUT = 0.4;    /* Ausblenden einer Szene: weich, ohne Ruck am Ende */

  /* ---------- Bausteine ---------- */
  function scene(id, tIn, tOut) {
    var el = document.getElementById(id);
    tl.set(el, { autoAlpha: 0 }, 0);
    tl.set(el, { autoAlpha: 1, y: 0 }, tIn);
    if (tOut != null) tl.to(el, { autoAlpha: 0, y: -12, duration: OUT, ease: "sine.inOut" }, tOut);
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
    tl.to(typeof sel === "string" ? $(sel) : sel, Object.assign({ autoAlpha: 0, duration: dur || 0.35, ease: "power2.in" }, to || {}), at);
  }
  /* Element zieht seinen Platz auf (Chatblasen, Hinweise in Karten) */
  function grow(sel, at, box, dur) {
    var el = typeof sel === "string" ? $(sel) : sel;
    var full = el.offsetHeight;   /* fertige Höhe samt Innenabstand vorab messen – „auto“ würde am Ende springen */
    var from = { autoAlpha: 0, height: 0 }, to = { autoAlpha: 1, height: full, duration: dur || 0.5, ease: "power2.out" };
    Object.keys(box || {}).forEach(function (k) { from[k] = box[k][0]; to[k] = box[k][1]; });
    tl.fromTo(el, from, to, at);
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
  function setText(el, text, at) { tl.call(function () { el.textContent = text; }, null, at); }
  function addClass(el, cls, at) { tl.call(function () { el.classList.add(cls); }, null, at); }
  /* Zustandswechsel (ausgewählt, aktiv, abgesprungen): Klasse setzen und die Farben kurz hinüberblenden statt umzuschalten */
  var MORPH = ["color", "backgroundColor", "borderColor"];
  function morph(owner, cls, targets, at, dur) {
    targets = targets || [owner];
    var pick = function (el) { var cs = getComputedStyle(el), o = {}; MORPH.forEach(function (k) { o[k] = cs[k]; }); return o; };
    var from = targets.map(pick);
    owner.classList.add(cls); var to = targets.map(pick); owner.classList.remove(cls);
    addClass(owner, cls, at);
    targets.forEach(function (el, k) {
      tl.fromTo(el, from[k], Object.assign({ duration: dur || 0.22, ease: "power1.out", immediateRender: false }, to[k]), at);
    });
  }
  function caret(el, from, to) {
    for (var x = from; x < to; x += 1.0) tl.set(el, { opacity: 0 }, x + 0.5).set(el, { opacity: 1 }, x + 1.0);
  }
  function pulse(sel, at, k) { tl.fromTo(sel, { scale: 1 }, { scale: k || 1.08, duration: 0.18, yoyo: true, repeat: 1, ease: "sine.inOut" }, at); }
  /* Kapitel-Hinweis unten links */
  function chapter(text, at) {
    var c = $("#chap").cloneNode(true);
    c.removeAttribute("id"); $("span", c).textContent = text;
    $("#stage").appendChild(c);
    tl.set(c, { autoAlpha: 0 }, 0);
    tl.fromTo(c, { autoAlpha: 0, x: -14 }, { autoAlpha: 1, x: 0, duration: 0.6 }, at);
    tl.fromTo($("b", c), { scaleX: 0 }, { scaleX: 1, duration: 0.8, ease: "power2.out" }, at + 0.05);
    tl.to(c, { autoAlpha: 0, duration: 0.5, ease: "power1.in" }, at + 3.8);
  }
  var stageR = $("#stage").getBoundingClientRect();
  function rect(el) { var r = el.getBoundingClientRect(); return { x: r.left - stageR.left, y: r.top - stageR.top, w: r.width, h: r.height }; }

  /* ---------- Szenengrenzen: Bild kommt kurz vor dem ersten Wort, die alte Szene ist dann schon weg ---------- */
  var LEAD = 0.3;
  var B = {
    s1: 0,
    s3: p("und die anfragen") - LEAD,
    s4: p("genau hier") - LEAD,
    s5: p("am anfang") + 0.12,          /* die Wende-Zeile darf erst ganz stehen */
    s6: p("dann lernen") - LEAD,
    s8: p("das alles") - 0.15,
    s9: p("aus über") - LEAD,
    s10: p("und wenn sich") - LEAD,
    s11: p("bei umfangreichen"),        /* das Dashboard kommt mit „Bei umfangreichen …“ */
    s12: t("medialyte") - LEAD
  };
  var ORDER = ["s1", "s3", "s4", "s5", "s6", "s8", "s9", "s10", "s11", "s12"];
  function endOf(id) { var i = ORDER.indexOf(id); return i < ORDER.length - 1 ? B[ORDER[i + 1]] - OUT - 0.06 : null; }
  ORDER.forEach(function (id) { scene(id, B[id], endOf(id)); });

  /* ---------- Hintergrund: Licht wandert langsam ---------- */
  tl.fromTo(".bg .f1", { x: 0, y: 0 }, { x: 260, y: 170, duration: DUR, ease: "sine.inOut" }, 0);
  tl.fromTo(".bg .f2", { x: 0, y: 0, scale: 1 }, { x: -240, y: -150, scale: 1.12, duration: DUR, ease: "sine.inOut" }, 0);

  chapter("Die Ausgangslage", 0.6);
  chapter("Unser Ablauf", B.s4 + 0.4);
  chapter("Der Unterschied", B.s8 + 0.3);
  chapter("Ihr KI-Agent", B.s10 + 0.3);

  /* ======================================================= 1 · Suche, alte Website, Absprung */
  (function () {
    var ph = $("#ph1"), q = $("#q"), hit = $("#hit");
    /* Ringe an den echten Stellen der alten Seite: [Ring, Element, oben, seitlich, unten] */
    var scr = rect($(".ph__screen", ph));
    [["#ring1", ".old__top", 5, 6, -1], ["#ring2", ".old__nav", -1, 6, 4], ["#ring3", "#oldHours", 8, 8, 8]].forEach(function (a) {
      var r = rect($(a[1])), ring = $(a[0]), top = a[2], side = a[3], bot = a[4];
      var left = r.x - scr.x - side;
      ring.style.left = left + "px"; ring.style.top = (r.y - scr.y - top) + "px";
      ring.style.width = Math.min(r.w + side * 2, scr.w - left - 4) + "px"; ring.style.height = (r.h + top + bot) + "px";
    });
    tl.set(ph, { x: 235 }, 0);
    pop(ph, 0.15, { y: 60, scale: 0.97 }, 1.1);
    var q0 = Math.max(0.9, t("jemand") + 0.05), q1 = Math.max(q0 + 1.2, t("anbieten") - 0.1);
    typeText(q, "Tischlerei in der Nähe", q0, q1 - q0);
    caret($("#caret"), 0.4, q1 + 0.3);
    tl.set("#caret", { opacity: 0 }, q1 + 0.35);
    $$(".res li").forEach(function (li, i) { pop(li, q1 + 0.15 + i * 0.14, { y: 18 }, 0.6); });
    /* Antippen, Laden, alte Seite */
    var tap = Math.max(q1 + 0.75, t("findet"));
    tl.to(ph, { x: 0, duration: 0.9, ease: "power3.inOut" }, tap + 0.2);     /* erst tippen, dann macht das Telefon Platz */
    tl.fromTo("#tap", { autoAlpha: 0, scale: 0.5 }, { autoAlpha: 1, scale: 1.2, duration: 0.25, ease: "power2.out" }, tap);
    tl.to("#tap", { autoAlpha: 0, duration: 0.3 }, tap + 0.25);
    tl.to(hit, { backgroundColor: "#E9EEF8", duration: 0.2 }, tap);
    var gone = t("weg"), load = tap + 0.35, shown = Math.min(load + 1.0, gone - 1.0);
    tl.set("#scrLoad", { autoAlpha: 1, x: 400 }, load);                          /* neue Seite schiebt sich herein */
    tl.to("#scrLoad", { x: 0, duration: 0.45, ease: "power3.out" }, load);
    tl.fromTo("#loadbar", { scaleX: 0 }, { scaleX: 0.86, duration: shown - load, ease: "power1.out" }, load);
    tl.fromTo("#spin", { rotation: 0 }, { rotation: 720, duration: shown - load + 0.1, ease: "none" }, load);
    tl.set("#scrOld", { x: 0 }, shown);
    tl.fromTo("#scrOld", { autoAlpha: 0 }, { autoAlpha: 1, duration: 0.22, ease: "power1.out", immediateRender: false }, shown);   /* Seite baut sich auf */
    tl.set("#scrLoad", { autoAlpha: 0 }, shown + 0.25);
    tl.fromTo("#old", { y: 0 }, { y: -110, duration: Math.max(0.6, gone - shown - 0.1), ease: "power1.inOut" }, shown + 0.1);
    /* Besuchszeit läuft – dann Absprung */
    var vis = $("#visit");
    pop(vis, tap + 0.5, { x: 40, y: 0 }, 0.7);
    count($("#tm"), 0, 4, tap + 0.35, gone - tap - 0.35, function (v) { return "0:0" + Math.floor(v); });
    setText($("#vstx"), "Sieht sich um", shown);
    setText($("#vstx"), "Absprung", gone);
    morph($("#vst"), "is-gone", [$("#vst"), $("#vst i")], gone);
    pulse("#vst", gone, 1.08);
    tl.to("#scrOld", { x: 400, duration: 0.45, ease: "power2.in" }, gone - 0.05);
    tl.set("#scrOld", { autoAlpha: 0 }, gone + 0.42);
    tl.to(hit, { opacity: 0.55, duration: 0.3 }, gone + 0.3);
    /* Blick auf die Mängel */
    var look = Math.max(gone + 0.5, t("veraltet") - 0.45);
    fadeOut(vis, look - 0.15, { x: 40 }, 0.35);
    tl.to(ph, { x: -150, duration: 0.9, ease: "power2.inOut" }, look);
    /* die alte Seite kommt zur Analyse zurück: deckend hineingeschoben wie eine neue Seite, ohne Überblendung */
    tl.set("#old", { y: 0 }, look);
    tl.set("#scrOld", { autoAlpha: 1, x: 400 }, look);
    tl.to("#scrOld", { x: 0, duration: 0.6, ease: "power3.out" }, look + 0.05);
    var hits = [Math.max(look + 0.5, t("veraltet")), t("handy"), t("öffnungszeiten", 1)];
    $$("#flags li").forEach(function (li, i) {
      pop(li, hits[i] - 0.05, { x: 40, y: 0 }, 0.6);
      tl.fromTo("#ring" + (i + 1), { autoAlpha: 0, scale: 1.05 }, { autoAlpha: 1, scale: 1, duration: 0.45, ease: "power3.out" }, hits[i]);
    });
  })();

  /* ======================================================= 3 · Anfragen verstreut */
  (function () {
    var tIn = B.s3;
    pop("#note", tIn + 0.1, { y: 40, rotation: -10, rotationTo: -4 }, 0.8);
    pop("#cTel", Math.max(tIn + 0.5, t("telefon")), { y: 30, scale: 0.94 }, 0.7);
    pop("#cMail", Math.max(tIn + 0.8, t("e-mail")), { y: 30, scale: 0.94 }, 0.7);
    pop("#cWa", Math.max(tIn + 1.1, t("whatsapp", 1)), { y: 30, scale: 0.94 }, 0.7);
    /* leichtes Schweben, dann gehen sie im Alltag unter */
    var sink = t("gehen"), cards = ["#note", "#cTel", "#cMail", "#cWa"];
    cards.forEach(function (s, i) {
      tl.to(s, { y: (i % 2 ? -10 : 10), duration: Math.max(1, sink - tIn - 1.4), ease: "sine.inOut" }, tIn + 1.0 + i * 0.1);
      tl.to(s, { y: "+=180", rotation: (i % 2 ? 6 : -8), opacity: 0.1, filter: "blur(5px)", duration: 1.4, ease: "power2.in" }, sink - 0.05 + i * 0.06);
    });
  })();

  /* ======================================================= 4 · Wende */
  (function () {
    var tIn = B.s4;
    tl.fromTo(".bg .f3", { autoAlpha: 0 }, { autoAlpha: 1, duration: 1.0, ease: "power1.out" }, tIn);
    tl.to(".bg .f3", { autoAlpha: 0, duration: 1.2, ease: "power1.inOut" }, endOf("s4"));
    pop("#turnMk", tIn + 0.05, { y: 0, scale: 0.88 }, 0.8);
    var words = $$("#turnHl .word"), at = [t("genau", 2), t("hier"), t("setzen"), t("wir", 1), t("an")];
    words.forEach(function (w, i) { pop(w, Math.max(tIn + 0.1, at[i] - 0.08), { y: 32 }, 0.5); });
  })();

  /* ======================================================= 5 · Erstgespräch und Angebot */
  (function () {
    var tIn = B.s5;
    tl.set("#bk", { x: 370 }, 0);
    pop("#bk", tIn + 0.05, { y: 30 }, 0.8);
    var dayAt = t("kostenfreies", 1), slotAt = t("erstgespräch", 1), offAt = t("innerhalb");
    morph($("#day"), "sel", null, dayAt); pulse("#day", dayAt, 1.1);
    morph($("#slot"), "sel", null, slotAt); pulse("#slot", slotAt, 1.05);
    pop("#bkok", slotAt + 0.4, { y: 14 }, 0.5);
    tl.to("#bk", { x: 0, duration: 0.9, ease: "power3.inOut" }, offAt - 0.35);
    pop("#offer", offAt + 0.05, { x: 70, y: 0 }, 0.85);
    pop("#h48", Math.max(offAt + 0.4, t("48")), { y: 10, scale: 0.92 }, 0.5);
  })();

  /* ======================================================= 6 + 7 · Ablauf, neue Website, Kundensystem */
  (function () {
    var tIn = B.s6, br = $("#br"), lis = $$("#rail li");
    /* Geometrie messen, bevor Startzustände gesetzt werden – sonst stecken deren Versätze in den Maßen */
    var brR = rect(br), sendR = rect($(".ns__send", br)), newR = rect($("#pcNew")), angR = rect($("#pcAng")), aufR = rect($("#slotAuf"));
    pop("#rail", tIn + 0.05, { y: -16 }, 0.7);
    pop(br, tIn + 0.1, { y: 40 }, 0.9);
    var s1 = t("lernen"), s2 = t("gestalten"), s3 = t("bauen"), s4 = t("testen"), s5 = t("live");
    function step(i, at) {
      morph(lis[i], "on", [lis[i], $("i", lis[i])], at);
      pulse($("i", lis[i]), at, 1.15);
      tl.to("#railFill", { scaleX: i / 4, duration: 0.6, ease: "power2.inOut" }, at - 0.15);
    }
    /* Schritt 1: Ihre Kunden kennenlernen */
    step(0, s1);
    $$(".pch").forEach(function (c, i) { pop(c, s1 + 0.1 + i * 0.22, { y: 18, scale: 0.96 }, 0.5); });
    /* Schritt 2: Gestaltung – Skizze, dann Design von links */
    step(1, s2);
    /* Wischen statt Überblenden: erst die Zielgruppe weg, dann wird aus der Skizze das Design */
    tl.fromTo("#persona", { clipPath: "inset(0% 0% 0% 0%)" }, { clipPath: "inset(0% 0% 0% 100%)", duration: 0.55, ease: "power2.inOut" }, s2 - 0.15);
    tl.fromTo("#wf", { clipPath: "inset(0% 0% 0% 0%)" }, { clipPath: "inset(0% 0% 0% 100%)", duration: 0.9, ease: "power2.inOut" }, s2 + 0.6);
    /* Schritt 3 und 4: Entwicklung und Test (Prüfliste rechts neben dem Browser) */
    step(2, s3);
    step(3, s4);
    pop("#checks b", s4 - 0.05, { y: 10 }, 0.4);
    $$("#checks span").forEach(function (c, i) { pop(c, s4 + 0.05 + i * 0.16, { x: 24, y: 0 }, 0.45); });
    /* Schritt 5: Live */
    step(4, s5);
    pop("#live", s5, { y: 0, scale: 0.8 }, 0.45);
    /* Dahinter: das eigene System */
    var sys = t("dahinter");
    fadeOut("#checks", sys - 0.55, { x: 24 }, 0.35);
    fadeOut("#rail", sys - 0.45, { y: -16 }, 0.35);
    var SC = 0.58, X0 = 110, CY = 527;
    var DX = X0 - brR.x, DY = (CY - brR.h * SC / 2) - brR.y;
    tl.to(br, { x: DX, y: DY, scale: SC, duration: 1.0, ease: "power3.inOut" }, sys - 0.1);
    pop("#db", sys + 0.4, { x: 70, y: 0 }, 0.9);
    /* jede Anfrage … fliegt aus dem Formular ins Dashboard (nur transform, Breite bleibt fest) */
    var sx = brR.x + DX + (sendR.x - brR.x) * SC, sy = brR.y + DY + (sendR.y - brR.y) * SC;
    var fly = $("#flyA"), aT = t("anfrage");
    fly.style.left = newR.x + "px"; fly.style.top = newR.y + "px"; fly.style.width = newR.w + "px";
    tl.set(fly, { autoAlpha: 0, x: sx - newR.x, y: sy - newR.y, scale: 0.5, transformOrigin: "0 0" }, 0);
    tl.to(fly, { autoAlpha: 1, duration: 0.2, ease: "power1.out" }, aT - 0.1);
    tl.to(fly, { x: 0, y: 0, scale: 1, duration: 0.95, ease: "power2.inOut" }, aT - 0.05);
    tl.set("#pcNew", { opacity: 1 }, aT + 0.92);
    tl.set(fly, { autoAlpha: 0 }, aT + 0.93);
    setText($("#kA"), "3", aT + 0.9); setText($("#nNeu"), "2", aT + 0.9);
    /* jeder Termin: Hinweis zieht in der Karte auf */
    var tT = t("termin"), tagBox = { marginTop: [-4, 6], paddingTop: [0, 4], paddingBottom: [0, 4] };
    grow("#tagT", tT - 0.05, tagBox, 0.45);
    setText($("#kT"), "4", tT + 0.2);
    /* jeder Auftrag: Karte wandert in „Auftrag“ */
    var oT = t("auftrag");
    tl.to("#pcAng", { x: aufR.x - angR.x, y: aufR.y - angR.y, duration: 0.8, ease: "power3.inOut" }, oT - 0.25);
    grow("#tagO", oT + 0.5, tagBox, 0.45);
    setText($("#nAng"), "0", oT + 0.35); setText($("#nAuf"), "1", oT + 0.35); setText($("#kO"), "6", oT + 0.5);
  })();

  /* ======================================================= 8 · Aus einer Hand */
  (function () {
    var tIn = B.s8;
    pop("#handHl", tIn + 0.05, { y: 30 }, 0.8);
    var hits = [t("website", 3), t("system", 2), t("pflege"), t("werbung")];
    ["#t1", "#t2", "#t3", "#t4"].forEach(function (s, i) { pop(s, Math.max(tIn + 0.4, hits[i] - 0.08), { y: 46, scale: 0.97 }, 0.65); });
    var ab = t("aufeinander");
    tl.to("#link", { scaleX: 1, duration: 0.9, ease: "power2.inOut" }, ab - 0.1);
    ["#t1", "#t2", "#t3", "#t4"].forEach(function (s, i) {
      tl.to(s, { borderColor: "rgba(170,190,220,.42)", duration: 0.35, ease: "power1.out" }, ab + i * 0.15);
    });
    pop("#contact", t("festen") - 0.15, { y: 36 }, 0.75);
  })();

  /* ======================================================= 9 · Erfahrung und Ergebnis */
  (function () {
    var tIn = B.s9, rr = p("bei rechnungsradar");
    /* die Zahl steht erst allein in der Mitte und macht dann der Ergebniskarte Platz */
    var bigR = rect($("#big"));
    tl.set("#big", { x: 960 - (bigR.x + bigR.w / 2) }, 0);
    pop("#big", tIn + 0.05, { y: 30 }, 0.8);
    tl.to("#big", { x: 0, duration: 0.9, ease: "power3.inOut" }, rr - 0.55);
    count($("#n200"), 0, 200, Math.max(tIn + 0.2, t("200") - 0.25), 1.1);
    pop("#imp", rr - 0.1, { x: 70, y: 0 }, 0.85);
    pop("#ir1", rr + 0.2, { y: 14 }, 0.55);
    ["#ir2", "#ir3", "#ir4"].forEach(function (s, i) { pop(s, rr + 0.5 + i * 0.18, { y: 14 }, 0.5); });
    var bars = $$("#ir1 .bar u i"), n = t("230");
    tl.fromTo(bars[0], { scaleX: 0 }, { scaleX: 1, duration: 0.8, ease: "power2.out" }, rr + 0.45);
    tl.fromTo(bars[1], { scaleX: 0 }, { scaleX: 1, duration: 1.2, ease: "power2.out" }, n - 0.15);
    tl.fromTo("#ir1 > b", { autoAlpha: 0 }, { autoAlpha: 1, duration: 0.25 }, n - 0.2);
    count($("#n230"), 0, 230, n - 0.15, 1.2);
  })();

  /* ======================================================= 10 · KI-Agent per WhatsApp */
  (function () {
    var tIn = B.s10;
    pop("#ph2", tIn + 0.05, { y: 60 }, 0.95);
    pop("#site", tIn + 0.45, { x: 70, y: 0 }, 0.85);
    pop("#ch1", t("öffnungszeiten", 2), { y: 10, scale: 0.92 }, 0.4);
    pop("#ch2", t("angebot", 2), { y: 10, scale: 0.92 }, 0.4);
    pop("#ch3", t("fotos"), { y: 10, scale: 0.92 }, 0.4);
    var msg = "Ab Montag haben wir 8–18 Uhr geöffnet. Bitte auf der Website ändern.";
    var tw = t("schreiben"), done = t("pflegt") - 0.2;
    var typeDur = Math.min(1.7, done - tw - 1.2);
    tl.to("#ch1", { backgroundColor: "rgba(0,168,132,.25)", borderColor: "rgba(0,168,132,.7)", duration: 0.25 }, tw - 0.15);
    typeText($("#waTx"), msg, tw, typeDur);
    var sent = tw + typeDur + 0.15;
    setText($("#waTx"), "", sent);
    fadeOut(".wa__chips", sent, {}, 0.25);
    var bub = { marginTop: [0, 12], paddingTop: [0, 14], paddingBottom: [0, 10] };
    grow("#bMe", sent, bub, 0.45);
    /* Agent tippt … */
    setText($("#waSt"), "schreibt …", sent + 0.3);
    tl.fromTo("#dots", { autoAlpha: 0, height: 0, marginTop: 0 }, { autoAlpha: 1, height: 44, marginTop: 12, duration: 0.3, ease: "power2.out" }, sent + 0.3);
    $$("#dots i").forEach(function (d, i) {
      tl.to(d, { y: -5, duration: 0.22, yoyo: true, repeat: 5, ease: "sine.inOut" }, sent + 0.4 + i * 0.1);
    });
    /* … und antwortet: Punkte weichen, Antwort zieht auf */
    tl.to("#dots", { autoAlpha: 0, height: 0, marginTop: 0, duration: 0.25, ease: "power2.in" }, done - 0.1);
    setText($("#waSt"), "online", done);
    grow("#bIn", done + 0.05, bub, 0.5);
    /* Website zeigt die Änderung: alt raus, neu rein – nacheinander, nicht übereinander */
    var up = done + 0.25;
    tl.fromTo("#flash", { autoAlpha: 0 }, { autoAlpha: 1, duration: 0.25, yoyo: true, repeat: 1, ease: "power1.inOut" }, up);
    fadeOut("#rowOld", up, { y: -14 }, 0.22);
    pop("#rowNew", up + 0.28, { y: 14 }, 0.4);
    pop("#upd", up + 0.45, { y: 0, scale: 0.8 }, 0.4);
  })();

  /* ======================================================= 11 · Dashboard und Team */
  (function () {
    var tIn = B.s11, team = t("team");
    tl.set("#db2", { x: 280 }, 0);
    pop("#db2", tIn + 0.05, { y: 40 }, 0.85);
    var cmd = "Neue Leistung „Treppen nach Maß“ auf die Website", c0 = tIn + 0.55, cDur = Math.min(1.7, team - c0 - 2.2);
    typeText($("#cmd"), cmd, c0, cDur);
    caret($("#caret2"), tIn, c0 + cDur + 0.2);
    tl.set("#caret2", { opacity: 0 }, c0 + cDur + 0.25);
    pop("#ans", c0 + cDur + 0.3, { y: 14 }, 0.5);
    pop("#add", c0 + cDur + 0.65, { y: -10 }, 0.45);
    tl.to("#db2", { x: 0, duration: 0.9, ease: "power3.inOut" }, team - 0.95);
    pop("#team", team - 0.6, { x: 70, y: 0 }, 0.85);
    $$("#team li").forEach(function (li, i) { pop(li, team - 0.2 + i * 0.2, { x: 20, y: 0 }, 0.45); });
  })();

  /* ======================================================= 12 · Abschluss */
  (function () {
    var tIn = B.s12;
    tl.fromTo(".bg .f3", { autoAlpha: 0 }, { autoAlpha: 0.9, duration: 1.8, ease: "power1.out", immediateRender: false }, tIn);
    pop("#endMk", tIn + 0.1, { y: 0, scale: 0.88 }, 0.9);
    pop("#endWm", tIn + 0.35, { y: 16 }, 0.8);
    pop("#endTag", t("damit") - 0.05, { y: 20 }, 0.7);
    pop("#endCta", t("buchen") - 0.1, { y: 14, scale: 0.95 }, 0.65);
    pop("#endUrl", t("buchen") + 0.45, { y: 10 }, 0.5);
  })();

  tl.set({}, {}, DUR);
  window.__dur = DUR;
  window.__B = B;          /* Szenengrenzen – für Kapitelmarken der Website und die Prüfung */
  window.__seek = function (s) { tl.seek(s, false); return true; };
  window.__tl = tl;
  window.__ready = true;
})();
