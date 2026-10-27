/* Medialyte – Grundfunktionen für alle Module.
   Jedes Modul läuft gekapselt: Fällt eines aus, laufen die anderen weiter. */
(function () {
  "use strict";
  var ML = window.ML = window.ML || {};
  ML.cfg = window.ML_CONFIG || {};
  var mq = window.matchMedia ? window.matchMedia("(prefers-reduced-motion: reduce)") : null;
  ML.reduce = !!(mq && mq.matches);
  ML.$ = function (s, r) { return (r || document).querySelector(s); };
  ML.$$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  ML.clamp = function (v, a, b) { return Math.max(a, Math.min(b, v)); };
  ML.esc = function (s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  };
  ML.store = {
    get: function (k) { try { return JSON.parse(sessionStorage.getItem(k)); } catch (e) { return null; } },
    set: function (k, v) { try { sessionStorage.setItem(k, JSON.stringify(v)); } catch (e) { /* ohne Speicher weiter */ } },
    del: function (k) { try { sessionStorage.removeItem(k); } catch (e) { /* egal */ } }
  };
  ML.json = function (id) {
    var el = document.getElementById(id);
    if (!el) return null;
    try { return JSON.parse(el.textContent); } catch (e) { return null; }
  };
  ML.hasIO = "IntersectionObserver" in window;

  /* Einmal ausführen, sobald ein Element sichtbar wird */
  ML.onVisible = function (el, cb, opts) {
    if (!el) return;
    if (!ML.hasIO) { cb(); return; }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { io.disconnect(); cb(); } });
    }, opts || { threshold: 0.3 });
    io.observe(el);
  };
  /* Laufend melden, ob ein Element im Bild ist */
  ML.watch = function (el, cb, opts) {
    if (!el) return;
    if (!ML.hasIO) { cb(true); return; }
    new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { cb(en.isIntersecting, en); });
    }, opts || { threshold: 0 }).observe(el);
  };

  /* Ein gemeinsamer Scroll-Takt für alle Module (ein requestAnimationFrame pro Bild) */
  var subs = [], ticking = false;
  function run() {
    ticking = false;
    var y = window.scrollY || document.documentElement.scrollTop || 0, vh = window.innerHeight;
    for (var i = 0; i < subs.length; i++) {
      try { subs[i](y, vh); } catch (e) { if (window.console) console.error("[Medialyte] Scroll", e); }
    }
  }
  function req() { if (!ticking) { ticking = true; requestAnimationFrame(run); } }
  window.addEventListener("scroll", req, { passive: true });
  window.addEventListener("resize", req, { passive: true });
  ML.onScroll = function (fn) { subs.push(fn); req(); };
  ML.tick = req;

  /* Zeitsteuerung, die sich sauber abbrechen lässt */
  ML.timeline = function () {
    var ids = [];
    return {
      at: function (ms, fn) { ids.push(setTimeout(fn, ms)); },
      clear: function () { ids.forEach(clearTimeout); ids = []; }
    };
  };

  ML.module = function (name, fn) {
    try { fn(ML); } catch (e) { if (window.console) console.error("[Medialyte] Modul " + name, e); }
  };
})();
