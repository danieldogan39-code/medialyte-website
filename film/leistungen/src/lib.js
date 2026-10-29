/* Medialyte Leistungsfilme – gemeinsame Werkzeuge (aus dem Erklärfilm übernommen).
   Jeder Film ruft window.FILM(function (K) {...}) auf; K enthält Zeitleiste und Werkzeuge. */
(function () {
  "use strict";
  window.FILM = function (scenes) {
  var TM = window.TM, DUR = TM.duration;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  $$("[data-kt]").forEach(function (el) {
    el.innerHTML = el.textContent.trim().split(/\s+/).map(function (w) { return '<span class="w"><i>' + w + "</i></span>"; }).join(" ");
  });
  var lay = (location.search + location.hash).match(/layout=(\w+)/);
  if (lay) { document.getElementById(lay[1]).style.visibility = "visible"; window.__ready = true; return; }
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
  /* Format: Breitbild 1920 × 1080 oder Hochkant 1080 × 1920 (<body class="v">, Layout in film_v.css) */
  var V = document.body.classList.contains("v"), SW = V ? 1080 : 1920, SH = V ? 1920 : 1080;
  var FY = V ? 60 : -86;     /* Versatz des Dashboards nach dem Umdrehen (Breitbild nach oben, Hochkant zur Mitte) */
  /* Hochkant: Browser, Dashboards und Geräte behalten ihr Breitbild-Layout und werden als Ganzes verkleinert */
  var BS = {};
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
    vis(path, at, null);                /* vorher unsichtbar: sonst zeigt die runde Linienkappe schon einen Punkt */
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

  var K = { tl: tl, t: t, p: p, $: $, $$: $$, vis: vis, text: text, cls: cls, typeText: typeText, count: count, blink: blink, pop: pop, leave: leave,
            words: words, reveal: reveal, conceal: conceal, grow: grow, morph: morph, pulse: pulse, draw: draw, cursorTo: cursorTo, click: click,
            pan: pan, sfx: sfx, rect: rect, D: D, SW: SW, SH: SH, DUR: DUR, B: {} };
  scenes(K);
  var B = K.B;
  tl.set({}, {}, DUR);

  /* ---------- Schnittstelle für Rendern und Prüfen ---------- */
  window.__dur = DUR;
  window.__fmt = V ? "v" : "h";
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
  };
})();
