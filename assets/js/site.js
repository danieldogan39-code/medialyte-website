/* 00-core.js */
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

  /* Ist ein Element gerade wirklich zu sehen? Wie ML.watch, berücksichtigt aber die angeheftete
     Kundenreise: Dort zählt eine Station nur, solange sie die aktive ist (Ereignis „ml:station“). */
  ML.presence = function (el, cb, opts) {
    if (!el) return;
    var st = el.closest ? el.closest("[data-station]") : null;
    var jr = st ? st.closest("[data-journey]") : null;
    var seen = false, last = null;
    function emit() {
      var active = !jr || !jr.classList.contains("journey--pin") || st.classList.contains("is-active");
      var v = seen && active;
      if (v !== last) { last = v; cb(v); }
    }
    ML.watch(el, function (v) { seen = v; emit(); }, opts);
    if (jr) jr.addEventListener("ml:station", emit);
  };
  /* Einmal ausführen, sobald ein Element wirklich zu sehen ist */
  ML.presentOnce = function (el, cb, opts) {
    var done = false;
    ML.presence(el, function (v) { if (v && !done) { done = true; cb(); } }, opts);
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

/* 10-header.js */
/* Seitenwechsel beginnen oben: Wer im Menü (oder sonst) auf eine andere Seite geht, landet am
   Seitenanfang – nicht auf der Höhe der vorigen Seite. Ausnahmen: Sprungziele (#…), Zurück/Vor
   und Neuladen, dort bleibt die Position, die der Browser wiederherstellt. */
ML.module("page-top", function (ML) {
  var KEY = "ml-top";
  document.addEventListener("click", function (e) {
    if (e.defaultPrevented || e.button > 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
    var a = e.target && e.target.closest ? e.target.closest("a[href]") : null;
    if (!a || (a.target && a.target !== "_self") || a.hasAttribute("download")) return;
    var u; try { u = new URL(a.getAttribute("href"), location.href); } catch (err) { return; }
    if (u.origin !== location.origin || u.hash) return;
    if (u.pathname === location.pathname && u.search === location.search) return;
    ML.store.set(KEY, 1);
  }, true);
  var flag = ML.store.get(KEY);
  ML.store.del(KEY);
  if (location.hash) return;
  var nav = null;
  try { nav = performance.getEntriesByType("navigation")[0] || null; } catch (err) { nav = null; }
  var type = nav ? nav.type : "navigate";
  if (!flag && type !== "navigate") return;
  function top() { if ((window.scrollY || 0) > 0) window.scrollTo({ top: 0, left: 0, behavior: "instant" }); }
  /* erst im nächsten Bild: scrollY würde hier sonst das erste Layout der ganzen Seite erzwingen */
  requestAnimationFrame(top);
  window.addEventListener("load", function () { requestAnimationFrame(top); });
});

/* Kopfzeile, Leistungen-Menü, mobiles Menü, WhatsApp-Knopf */
ML.module("header", function (ML) {
  var $ = ML.$, $$ = ML.$$;
  var header = $("[data-header]");

  /* Kopfzeile wird beim Scrollen zur Glasfläche */
  ML.onScroll(function (y) { if (header) header.classList.toggle("is-scrolled", y > 8); });

  /* Leistungen-Menü: Klick, Tastatur, Klick daneben */
  $$("[data-drop]").forEach(function (item) {
    var btn = $(".nav__link", item);
    if (!btn) return;
    var openY = 0;
    function set(open) {
      item.classList.toggle("is-open", open);
      btn.setAttribute("aria-expanded", open ? "true" : "false");
      if (open) openY = window.scrollY || 0;
    }
    /* Wer weiterscrollt, will das Menü nicht mehr: nach einem Stück Weg schließt es */
    ML.onScroll(function (y) { if (item.classList.contains("is-open") && Math.abs(y - openY) > 160) set(false); });
    btn.addEventListener("click", function () { set(!item.classList.contains("is-open")); });
    item.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && item.classList.contains("is-open")) { set(false); btn.focus(); }
    });
    item.addEventListener("focusout", function (e) { if (!item.contains(e.relatedTarget)) set(false); });
    document.addEventListener("click", function (e) { if (!item.contains(e.target)) set(false); });
    /* Maus verlässt das Menü: zu – außer es wurde per Tastatur geöffnet */
    function kb() { try { return btn.matches(":focus-visible"); } catch (e) { return document.activeElement === btn; } }
    item.addEventListener("mouseleave", function () { if (!kb()) set(false); });
  });

  /* Mobiles Menü */
  var burger = $(".burger"), mnav = $("#mnav");
  if (burger && mnav) {
    var lastFocus = null;
    function setMenu(open) {
      var isOpen = mnav.classList.contains("is-open");
      if (open === isOpen) return;
      mnav.classList.toggle("is-open", open);
      if (open) mnav.removeAttribute("inert"); else mnav.setAttribute("inert", "");
      burger.setAttribute("aria-expanded", open ? "true" : "false");
      burger.setAttribute("aria-label", open ? "Menü schließen" : "Menü öffnen");
      document.body.classList.toggle("menu-open", open);
      if (header) header.classList.toggle("is-menu", open);
      if (open) {
        lastFocus = document.activeElement;
        var first = $(".mnav__link", mnav);
        setTimeout(function () { if (first) first.focus({ preventScroll: true }); }, 60);
      } else if (lastFocus && lastFocus.focus) {
        lastFocus.focus({ preventScroll: true });
      }
    }
    burger.addEventListener("click", function () { setMenu(!mnav.classList.contains("is-open")); });
    $$("a", mnav).forEach(function (a) { a.addEventListener("click", function () { setMenu(false); }); });
    document.addEventListener("keydown", function (e) {
      if (!mnav.classList.contains("is-open")) return;
      if (e.key === "Escape") { setMenu(false); burger.focus(); return; }
      if (e.key === "Tab") {
        /* Fokus bleibt im Menü (inklusive Schließen-Knopf) */
        var f = [burger].concat($$("a[href], button:not([disabled])", mnav)).filter(function (el) { return el.offsetParent !== null || el === burger; });
        var i = f.indexOf(document.activeElement);
        if (e.shiftKey && (i <= 0)) { e.preventDefault(); f[f.length - 1].focus(); }
        else if (!e.shiftKey && i === f.length - 1) { e.preventDefault(); f[0].focus(); }
      }
    });
    var sub = $("[data-msub]", mnav), subBox = $("#mnav-sub");
    if (sub && subBox) {
      sub.addEventListener("click", function () {
        var open = sub.getAttribute("aria-expanded") !== "true";
        sub.setAttribute("aria-expanded", open ? "true" : "false");
        subBox.classList.toggle("is-open", open);
      });
    }
    var mq = window.matchMedia("(min-width: 1081px)");
    var onMq = function (m) { if (m.matches) setMenu(false); };
    if (mq.addEventListener) mq.addEventListener("change", onMq); else if (mq.addListener) mq.addListener(onMq);
  }

  /* WhatsApp-Knopf: erscheint nach dem Startbereich, verschwindet bei Buchung und Fußzeile.
     Beim Weiterlesen nach unten tritt er zur Seite und kommt beim Zurückscrollen wieder – so verdeckt er keinen Text. */
  var fab = $(".fab");
  if (fab) {
    var hero = $(".hero"), away = new Set(), pastHero = false, reading = false, lastY = window.scrollY || 0, acc = 0;
    var update = function () { fab.classList.toggle("is-on", pastHero && away.size === 0 && !reading); };
    ML.onScroll(function (y, vh) {
      var limit = hero ? hero.offsetTop + hero.offsetHeight * 0.55 : vh * 0.6;
      var p = y > limit - vh * 0.3;
      var dy = y - lastY; lastY = y;
      /* erst nach einem kleinen Stück in dieselbe Richtung umschalten, damit nichts flackert */
      acc = (dy > 0) === (acc > 0) ? acc + dy : dy;
      var r = reading;
      if (acc > 60) r = true;
      else if (acc < -40) r = false;
      if (p !== pastHero || r !== reading) { pastHero = p; reading = r; update(); }
    });
    if (ML.hasIO) {
      var io = new IntersectionObserver(function (es) {
        es.forEach(function (en) { if (en.isIntersecting) away.add(en.target); else away.delete(en.target); });
        update();
      }, { threshold: 0.08 });
      /* Über Buchung, Fußzeile, Abschluss und den Häufigen Fragen (Plus-Zeichen rechts) bleibt er weg */
      $$("#booking, .footer, .closing, .faq__list").forEach(function (el) { io.observe(el); });
    }
  }
});

/* 15-reveal.js */
/* Einblenden beim Scrollen und Zähler.
   Erst wenn der Beobachter läuft, wird die Klasse .rv gesetzt – ohne Skript bleibt alles sichtbar. */
ML.module("reveal", function (ML) {
  var els = ML.$$("[data-reveal]");
  if (ML.reduce || !ML.hasIO || !els.length) return;
  var vh = window.innerHeight;
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (en) {
      if (en.isIntersecting) { en.target.classList.add("is-in"); io.unobserve(en.target); }
    });
  }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
  els.forEach(function (el) {
    var r = el.getBoundingClientRect();
    if (r.top < vh * 0.92 && r.bottom > 0) el.classList.add("is-in"); /* schon sichtbar: sofort zeigen */
    else io.observe(el);
  });
  document.documentElement.classList.add("rv");
  /* Sicherheitsnetz: Was nach 6 s noch versteckt ist und im Bild liegt, wird gezeigt */
  setTimeout(function () {
    els.forEach(function (el) {
      if (el.classList.contains("is-in")) return;
      var r = el.getBoundingClientRect();
      if (r.top < window.innerHeight && r.bottom > 0) el.classList.add("is-in");
    });
  }, 6000);
});

ML.module("counters", function (ML) {
  if (ML.reduce) return;
  ML.$$("[data-count]").forEach(function (el) {
    var to = parseFloat(el.getAttribute("data-count"));
    if (!isFinite(to) || to === 0) return;
    /* Eine unsichtbare Kopie des Endwerts hält die Breite fest: nichts rückt, kein Abstand am Ende */
    var final = el.textContent;
    el.classList.add("cnt");
    el.innerHTML = '<span class="cnt__g">' + ML.esc(final) + '</span><span class="cnt__v" aria-hidden="true">' + ML.esc(final) + "</span>";
    var v = el.lastChild;
    ML.onVisible(el, function () {
      var t0 = null, dur = 1500;
      function step(t) {
        if (!t0) t0 = t;
        var p = Math.min(1, (t - t0) / dur), k = 1 - Math.pow(1 - p, 3);
        v.textContent = String(Math.round(to * k));
        if (p < 1) requestAnimationFrame(step);
        else { el.classList.remove("cnt"); el.textContent = final; }
      }
      v.textContent = "0";
      requestAnimationFrame(step);
    }, { threshold: 0.6 });
  });
});

/* 20-cockpit.js */
/* Startbereich: Cockpit mit vier Beispiel-Betrieben.
   Ablauf je Betrieb: Anfragen erscheinen, Nachricht an den KI-Agenten, Antwort, Website ändert sich, neue Anfrage kommt rein. */
ML.module("cockpit", function (ML) {
  var $ = ML.$, $$ = ML.$$;
  var root = $("[data-cockpit]");
  var D = ML.json("cockpit-data");
  if (!root || !D) return;
  var chips = $$(".cp-tab", root);
  var tabsEl = $(".cp-tabs", root), ind = $(".cp-tabs__ind", root), panel = $("[data-cp=panel]", root);
  var pauseBtn = $(".cp-pause", root);
  var feed = $("[data-cp=feed]", root), msgs = $("[data-cp=msgs]", root), kpi = $("[data-cp=kpi]", root);
  var tl = ML.timeline();
  var cur = root.getAttribute("data-branch") || D.order[0];
  var auto = !ML.reduce, paused = false, inView = false, played = false;
  var SCENE = 9200, rounds = 0;

  function text(key, v) { var el = $("[data-cp=" + key + "]", root); if (el) el.textContent = v; }
  function feedItem(it, slot, isNew) {
    var d = document.createElement("div");
    d.className = "cp-feed__item" + (isNew ? " is-new" : "");
    d.style.setProperty("--slot", slot);
    d.innerHTML = '<span class="ic">' + (D.icons[it[0]] || "") + "</span><b>" + ML.esc(it[1]) + "</b><small>" + ML.esc(it[2]) + "</small><time>" + ML.esc(it[3]) + "</time>";
    return d;
  }
  function msg(cls, html, time) {
    var d = document.createElement("div");
    d.className = "cp-msg " + cls + " is-pop";
    d.innerHTML = html + (time ? "<time>" + time + "</time>" : "");
    msgs.appendChild(d);
    /* Höchstens zwei Nachrichten, damit die neueste immer ganz zu sehen ist */
    var all = $$(".cp-msg", msgs);
    while (all.length > 2) { all.shift().remove(); }
    return d;
  }
  function site(key) { return $(".ms--" + key, root); }
  function syncSite(s) { var c = s && $("[data-msform]", s); if (c && c._sync) c._sync(); }
  /* Neuer Eintrag oben im Verlauf, die anderen rücken nach */
  function pushFeed(it) {
    $$(".cp-feed__item", feed).forEach(function (el) { var n = +el.style.getPropertyValue("--slot") + 1; el.style.setProperty("--slot", n); if (n > 2) el.classList.add("is-leave"); });
    var n = feedItem(it, 0, true); n.classList.add("is-enter"); feed.insertBefore(n, feed.firstChild);
    requestAnimationFrame(function () { requestAnimationFrame(function () { n.classList.remove("is-enter"); }); });
    setTimeout(function () { $$(".is-leave", feed).forEach(function (el) { el.remove(); }); }, 800);
  }
  /* Markierung des gewählten Betriebs gleitet unter den nächsten Reiter */
  function placeInd(animate) {
    var t = tabsEl && $(".cp-tab[aria-selected=true]", tabsEl);
    if (!t || !ind || !t.offsetWidth) return;
    if (!animate) ind.style.transition = "none";
    ind.style.setProperty("--x", t.offsetLeft + "px");
    ind.style.setProperty("--w", t.offsetWidth + "px");
    if (!animate) { void ind.offsetWidth; ind.style.transition = ""; }
    tabsEl.classList.add("has-ind");
  }
  var kpiNow = 0, count = 0, minute = 9 * 60 + 42, tried = false, kpiT = null, liveEl = $("[data-cp-live]", root.parentNode);
  function setKpi(v, tick) {
    kpiNow = v;
    clearTimeout(kpiT);   /* ein Wechsel des Betriebs bricht das Nachzählen ab – keine alte Zahl */
    var a = kpi.children[0], b = kpi.children[1];
    if (!tick) { kpi.classList.remove("is-tick"); a.textContent = v; b.textContent = ""; return; }
    b.textContent = v;
    kpi.classList.add("is-tick");
    kpiT = setTimeout(function () { kpi.classList.remove("is-tick"); a.style.transition = b.style.transition = "none"; a.textContent = v; b.textContent = "";
      void kpi.offsetWidth; a.style.transition = b.style.transition = ""; }, 700);
  }

  /* Zustand eines Betriebs vorbereiten (vor der Animation) */
  function reset(key) {
    var b = D.b[key];
    var changed = root.getAttribute("data-branch") !== key;
    root.setAttribute("data-branch", key);
    text("host", b.host);
    text("kpil", b.kpi[0]);
    text("kpid", b.kpi[2]);
    text("ch", b.channel === "wa" ? "KI-Agent · per WhatsApp" : "KI-Agent · im Dashboard");
    count = b.feed.length;
    tried = false;
    text("count", "Heute " + count);
    text("time", "09:41"); minute = 9 * 60 + 42;
    setKpi(b.kpi[1], false);
    feed.innerHTML = "";
    /* Beim Wechsel zwischen Betrieben stehen die Einträge sofort da (kein Leeren und Einblenden, das wirkt wie Flackern);
       nur beim ersten Abspielen gleiten sie herein */
    b.feed.forEach(function (it, i) { var el = feedItem(it, i, false); if (!played) el.classList.add("is-enter"); feed.appendChild(el); });
    msgs.innerHTML = "";
    var s = site(key);
    if (s) {
      var info = $(".ms__info", s), note = $(".ms__notice", s), card = $("[data-msform]", s);
      s.classList.remove("is-upd");
      if (info) info.classList.remove("is-upd", "is-flash");
      if (note) note.classList.remove("is-on");
      if (card) { card.classList.remove("is-done"); if (card._sync) card._sync(); }
    }
    chips.forEach(function (c) {
      var on = c.getAttribute("data-branch") === key;
      c.setAttribute("aria-selected", on ? "true" : "false");
      c.tabIndex = on ? 0 : -1;
    });
    $$(".cp-site__view > .ms", root).forEach(function (m) { m.inert = !m.classList.contains("ms--" + key); });
    if (panel) panel.setAttribute("aria-labelledby", "cpt-" + key);
    placeInd(changed && !ML.reduce);
  }

  /* Endzustand ohne Animation (für reduzierte Bewegung) */
  function finalState(key) {
    reset(key);
    var b = D.b[key];
    feed.innerHTML = "";
    feed.appendChild(feedItem(b["new"], 0, true));
    b.feed.forEach(function (it, i) { feed.appendChild(feedItem(it, i + 1, false)); });
    count = b.feed.length + 1; text("count", "Heute " + count);
    if (b.channel === "wa") { msg("cp-msg--me", ML.esc(b.me), "09:38"); msg("cp-msg--agent", ML.esc(b.agent), "09:39"); }
    else { msg("cp-msg--task", "<b>" + ML.esc(b.task[0]) + "</b>" + ML.esc(b.agent)); }
    $$(".cp-msg", msgs).forEach(function (m) { m.classList.remove("is-pop"); });
    var s = site(key);
    if (s) { var info = $(".ms__info", s), note = $(".ms__notice", s); s.classList.add("is-upd"); if (info) info.classList.add("is-upd"); if (note) note.classList.add("is-on"); syncSite(s); }
    setKpi(b.kpi[1] + 1, false);
  }

  /* Website des Betriebs zeigt die Änderung */
  function updateSite(key) {
    var s = site(key); if (!s || s.classList.contains("is-upd")) return;
    var info = $(".ms__info", s), note = $(".ms__notice", s);
    s.classList.add("is-upd");
    syncSite(s);
    if (info) { info.classList.add("is-upd", "is-flash"); setTimeout(function () { info.classList.remove("is-flash"); }, 1500); }
    if (note) note.classList.add("is-on");
  }
  function publish(btn, key) {
    btn.disabled = true;
    btn.classList.remove("is-press"); btn.classList.add("is-done");
    btn.innerHTML = D.check + "Veröffentlicht";
    updateSite(key);
  }

  function play(key) {
    tl.clear();
    var b = D.b[key];
    cur = key;
    reset(key);
    played = true;
    tl.at(120, function () { $$(".cp-feed__item", feed).forEach(function (el, i) { setTimeout(function () { el.classList.remove("is-enter"); }, i * 90); }); });
    if (b.channel === "wa") {
      tl.at(1300, function () { msg("cp-msg--me", ML.esc(b.me), "09:38"); });
      tl.at(2300, function () { var t = document.createElement("div"); t.className = "cp-typing is-pop"; t.innerHTML = "<i></i><i></i><i></i>"; msgs.appendChild(t); });
      tl.at(3600, function () { var t = $(".cp-typing", msgs); if (t) t.remove(); msg("cp-msg--agent", ML.esc(b.agent), "09:39"); });
    } else {
      var card;
      tl.at(1300, function () {
        card = msg("cp-msg--task", "<b>" + ML.esc(b.task[0]) + "</b>" + ML.esc(b.task[1]) + '<br><button type="button" class="cp-msg__btn">' + D.check + "Veröffentlichen</button>");
        var btn = $(".cp-msg__btn", card);
        if (btn) btn.addEventListener("click", function () { interact(); publish(btn, key); });
      });
      tl.at(2900, function () { var btn = card && $(".cp-msg__btn", card); if (btn && !btn.disabled) btn.classList.add("is-press"); });
      tl.at(3150, function () { var btn = card && $(".cp-msg__btn", card); if (btn && !btn.disabled) publish(btn, key); });
    }
    tl.at(3900, function () { updateSite(key); });
    tl.at(5100, function () {
      if (tried) return;   /* Wer selbst etwas abgeschickt hat, sieht seinen eigenen Eintrag oben */
      pushFeed(b["new"]);
      setKpi(kpiNow + 1, true);
      count++; text("count", "Heute " + count);
    });
    tl.at(SCENE, function () {
      if (!auto || paused || !inView || document.hidden) return;
      /* Nach zwei Runden durch alle Betriebe hält die Vorführung an – eine offene Seite soll den Rechner nicht dauerhaft beschäftigen */
      if (++rounds >= D.order.length * 2) return;
      var i = D.order.indexOf(cur);
      play(D.order[(i + 1) % D.order.length]);
    });
  }

  function select(key, user) {
    if (user) { auto = false; rounds = 0; }
    if (ML.reduce || paused) { tl.clear(); finalState(key); cur = key; return; }
    play(key);
  }

  chips.forEach(function (c, i) {
    c.addEventListener("click", function () {
      if (c.getAttribute("aria-selected") === "true" && played) return;   /* schon gewählt: nichts neu starten */
      select(c.getAttribute("data-branch"), true);
    });
    c.addEventListener("keydown", function (e) {
      var n = null;
      if (e.key === "ArrowRight") n = (i + 1) % chips.length;
      if (e.key === "ArrowLeft") n = (i - 1 + chips.length) % chips.length;
      if (e.key === "Home") n = 0;
      if (e.key === "End") n = chips.length - 1;
      if (n === null) return;
      e.preventDefault(); chips[n].focus(); select(chips[n].getAttribute("data-branch"), true);
    });
  });

  if (pauseBtn) {
    if (ML.reduce) pauseBtn.hidden = true;
    pauseBtn.addEventListener("click", function () {
      paused = !paused;
      pauseBtn.setAttribute("aria-pressed", paused ? "true" : "false");
      pauseBtn.setAttribute("aria-label", paused ? "Animation fortsetzen" : "Animation anhalten");
      if (paused) { tl.clear(); finalState(cur); }
      else { auto = true; play(cur); }
    });
  }

  /* ---------- Beispiel-Websites zum Ausprobieren ----------
     Auswahl treffen, abschicken – und die Anfrage steht sofort im Cockpit. */
  function stamp() { var h = Math.floor(minute / 60), m = minute % 60; minute++; return (h < 10 ? "0" : "") + h + ":" + (m < 10 ? "0" : "") + m; }
  function fill(t, v) { return String(t || "").replace(/\{(\w+)\}/g, function (_, k) { return v[k] != null ? v[k] : ""; }); }
  function interact() { auto = false; }
  $$("[data-msform]", root).forEach(function (card) {
    var key = card.getAttribute("data-msform"), s = card.closest(".ms"), F = (D.b[key] || {}).form || {};
    var toast = $("[data-mstoast]", s), ctas = $$("[data-mscta]", s), sb = $("[data-mssubmit]", card), again = $("[data-msagain]", card);
    function val(name) { var o = $('[data-msgroup="' + name + '"] .mc__o.is-on', card); return o ? o.getAttribute("data-v") : ""; }
    /* Felder zum Antippen (Tag, Behandlung) und Personen mit − und + */
    var cyc = {}, persons = F.persons || 0, pEl = $("[data-mspersons]", card);
    $$("[data-mscycle]", card).forEach(function (b) {
      var name = b.getAttribute("data-mscycle"), list = (F.cycles || {})[name] || [], out = $("[data-mscyclev]", b);
      cyc[name] = 0;
      b.addEventListener("click", function () {
        interact();
        if (!list.length) return;
        cyc[name] = (cyc[name] + 1) % list.length;
        out.textContent = list[cyc[name]].label;
        b.setAttribute("aria-label", (b.querySelector("small") || {}).textContent + ": " + list[cyc[name]].label + " – antippen zum Ändern");
        b.classList.remove("is-tap"); void b.offsetWidth; b.classList.add("is-tap");
      });
    });
    $$("[data-msstep]", card).forEach(function (b) {
      b.addEventListener("click", function () {
        interact();
        persons = ML.clamp(persons + (+b.getAttribute("data-msstep")), 1, 8);
        if (pEl) pEl.textContent = persons;
      });
    });
    function vals() {
      var v = { time: val("time"), topic: val("topic"), day: val("day") };
      if (v.day && F.days && F.days[v.day]) { v.dayShort = F.days[v.day][0]; v.dayLong = F.days[v.day][1]; }
      Object.keys(cyc).forEach(function (name) { var it = ((F.cycles || {})[name] || [])[cyc[name]]; if (it) Object.keys(it).forEach(function (k) { v[k] = it[k]; }); });
      if (persons) { v.persons = persons; v.personsText = persons === 1 ? "1 Person" : persons + " Personen"; }
      return v;
    }
    function hidden() { return getComputedStyle(card).display === "none"; }
    function changed(name, v) {
      if (name === "topic" && F.area) { var a = $("[data-msarea]", card); if (a) a.textContent = F.area[v] || ""; }
      if (key === "praxis") sync();
    }
    /* Praxis: Nach der Änderung durch den Agenten ist Mittwochnachmittag nicht mehr buchbar */
    function sync() {
      var pm = $(".mc__pm", card); if (!pm) return;
      var closed = s.classList.contains("is-upd") && val("day") === "Mi 18";
      pm.disabled = closed;
      pm.setAttribute("aria-disabled", closed ? "true" : "false");
      if (closed && pm.classList.contains("is-on")) { var first = $('[data-msgroup="time"] .mc__o', card); if (first) pick(first); }
    }
    function pick(o, focus) {
      if (o.disabled) return;
      var g = o.closest("[data-msgroup]");
      $$(".mc__o", g).forEach(function (x) { var on = x === o; x.classList.toggle("is-on", on); x.setAttribute("aria-checked", on ? "true" : "false"); x.tabIndex = on ? 0 : -1; });
      if (focus) o.focus();
      changed(g.getAttribute("data-msgroup"), o.getAttribute("data-v"));
    }
    $$("[data-msgroup]", card).forEach(function (g) {
      var opts = $$(".mc__o", g);
      opts.forEach(function (o, i) {
        o.addEventListener("click", function () { interact(); pick(o); });
        o.addEventListener("keydown", function (e) {
          var d = (e.key === "ArrowRight" || e.key === "ArrowDown") ? 1 : (e.key === "ArrowLeft" || e.key === "ArrowUp") ? -1 : 0;
          if (!d) return;
          e.preventDefault(); interact();
          var j = i, guard = 0;
          do { j = (j + d + opts.length) % opts.length; guard++; } while (opts[j].disabled && guard < opts.length);
          pick(opts[j], true);
        });
      });
    });
    function submit() {
      interact();
      tried = true;
      var v = vals(), t = stamp();
      var title = fill(F.feed && F.feed[1], v), sub = fill(F.feed && F.feed[2], v);
      $("[data-msdone]", card).textContent = fill(F.done, v);
      var stacked = root.getBoundingClientRect().width < 860;
      $("[data-mswhere]", card).textContent = stacked ? "Steht jetzt unten im Dashboard bei den neuen Anfragen." : "Steht jetzt rechts im Dashboard bei den neuen Anfragen.";
      card.classList.add("is-done");
      if (again && !hidden()) again.focus({ preventScroll: true });
      pushFeed([F.feed ? F.feed[0] : "inbox", title, sub, t]);
      setKpi(kpiNow + 1, !ML.reduce);
      count++; text("count", "Heute " + count);
      text("time", t);
      if (liveEl) liveEl.textContent = "Neu im Dashboard: " + title + ", " + sub + ".";
      /* Der KI-Agent meldet sich kurz darauf zu der neuen Anfrage */
      var say = fill(F.agent, v), forKey = key;
      if (say) setTimeout(function () {
        if (cur !== forKey) return;
        $$(".cp-typing", msgs).forEach(function (x) { x.remove(); });
        var all = $$(".cp-msg", msgs);
        var keep = (all.length && !all[all.length - 1].classList.contains("cp-msg--task")) ? 1 : 0;
        while (all.length > keep) { all.shift().remove(); }
        msg("cp-msg--agent", ML.esc(say), t);
      }, ML.reduce ? 0 : 1100);
      if (toast && hidden()) {
        toast.textContent = fill(F.done, v) + (stacked ? " – steht jetzt unten im Dashboard." : " – steht jetzt im Dashboard.");
        toast.classList.add("is-on"); clearTimeout(toast._t);
        toast._t = setTimeout(function () { toast.classList.remove("is-on"); }, 4200);
      }
    }
    if (sb) sb.addEventListener("click", submit);
    if (again) again.addEventListener("click", function () { interact(); card.classList.remove("is-done"); var f = $(".mc__o.is-on", card) || sb; if (f) f.focus({ preventScroll: true }); });
    ctas.forEach(function (cta) { cta.addEventListener("click", function () {
      if (hidden()) { submit(); return; }
      interact();
      card.classList.remove("is-done");
      card.classList.remove("is-hint"); void card.offsetWidth; card.classList.add("is-hint");
      var f = $(".mc__o.is-on", card) || sb; if (f) f.focus({ preventScroll: true });
    }); });
    card._sync = sync;
  });

  /* Markierung nachführen, wenn sich die Breite ändert */
  if ("ResizeObserver" in window && tabsEl) new ResizeObserver(function () { placeInd(false); }).observe(tabsEl);
  else window.addEventListener("resize", function () { placeInd(false); });
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { placeInd(false); });

  /* Nach dem Laden in einer ruhigen Sekunde alle Beispiel-Websites vorzeichnen, damit der erste Wechsel nicht stockt */
  function warm() { root.classList.add("is-warm"); }
  window.addEventListener("load", function () { setTimeout(warm, 1500); });
  ["pointerenter", "touchstart", "focusin"].forEach(function (ev) { root.addEventListener(ev, warm, { once: true, passive: true }); });

  if (ML.reduce) { finalState(cur); return; }
  reset(cur);
  var left = false;
  ML.watch(root, function (vis) {
    inView = vis;
    if (!vis) { if (played) left = true; return; }
    if (paused) return;
    if (!played) { play(cur); return; }
    /* Zurück im Bild: Die Vorführung läuft wieder von selbst weiter – auch nach einem Klick */
    if (left) { left = false; auto = true; rounds = 0; }
    if (auto) { tl.clear(); tl.at(1800, function () { if (inView && !paused) { var i = D.order.indexOf(cur); play(D.order[(i + 1) % D.order.length]); } }); }
  }, { threshold: 0.25 });
  document.addEventListener("visibilitychange", function () {
    if (!document.hidden && inView && auto && !paused) { tl.clear(); tl.at(1200, function () { play(cur); }); }
  });

  /* Räumliche Neigung: das Cockpit richtet sich beim Scrollen auf (nur große Bildschirme).
     Der Text darüber bleibt ruhig stehen. */
  var wide = window.matchMedia("(min-width: 900px)");
  ML.onScroll(function (y, vh) {
    if (!wide.matches) { if (root.style.transform) root.style.transform = ""; return; }
    if (y > vh * 1.4) return;
    var p = ML.clamp(y / (vh * 0.62), 0, 1);
    var e = 1 - Math.pow(1 - p, 2);
    root.style.transform = "rotateX(" + (12 * (1 - e)).toFixed(2) + "deg) scale(" + (0.94 + 0.06 * e).toFixed(4) + ")";
  });
});

/* 25-idea.js */
/* Die Idee: drei Säulen mit je einer Frage zum Selbstcheck. Die Antworten zeigen den größten Hebel
   und wählen im Erstgespräch die passenden Anliegen vor (Startseite) bzw. geben sie an /termin/ weiter. */
ML.module("idea", function (ML) {
  var $ = ML.$, $$ = ML.$$;
  $$("[data-pillars]").forEach(function (root) {
    var cards = $$(".pillar", root), out = root.nextElementSibling;
    if (!cards.length || !out || !out.hasAttribute("data-pillars-out")) return;
    var txt = $("[data-po-text]", out), cta = $("[data-po-cta]", out), dots = $$(".po__dot", out);
    var base = cta ? (cta.getAttribute("href") || "").split("?")[0] : "";
    var onHome = !!document.getElementById("booking");
    var WHY = {
      vermehrung: "Mehr Anfragen – mit einer Website, die bei Google gefunden wird, und Werbung, die genau Ihre Zielgruppe erreicht.",
      verbesserung: "Ein Auftritt, der auf jedem Gerät überzeugt und immer aktuell ist – gepflegt per WhatsApp.",
      verwaltung: "Ein eigenes System, in dem jede Anfrage, jeder Termin und jeder Auftrag landet."
    };
    var ans = {};

    function list(words) {
      if (words.length < 2) return words.join("");
      return words.slice(0, -1).join(", ") + " und " + words[words.length - 1];
    }
    function say(head, rest) {
      txt.innerHTML = "<b>" + ML.esc(head) + "</b> <span>" + ML.esc(rest) + "</span>";
    }
    function render() {
      var gaps = cards.filter(function (c) { return ans[c.getAttribute("data-pillar")] === "gap"; });
      var done = cards.filter(function (c) { return !!ans[c.getAttribute("data-pillar")]; }).length;
      var open = cards.length - done;
      if (!done) say("Wo liegt Ihr größter Hebel?", "Beantworten Sie die drei Fragen oben – das Ergebnis nehmen wir direkt ins Erstgespräch mit.");
      else if (gaps.length === 1) say("Ihr größter Hebel: " + gaps[0].getAttribute("data-name") + ".", WHY[gaps[0].getAttribute("data-pillar")]);
      else if (gaps.length === cards.length) say("Bei allen drei ist Luft nach oben.", "Genau dafür sind wir da. Im Erstgespräch klären wir, womit Sie am besten anfangen.");
      else if (gaps.length > 1) say("Ihre Hebel: " + list(gaps.map(function (c) { return c.getAttribute("data-name"); })) + ".", "Im Erstgespräch zeigen wir, womit Sie am besten anfangen – und was es bringt.");
      else if (open) say(open === 1 ? "Noch eine Frage." : "Noch " + (open === 2 ? "zwei" : open) + " Fragen.", "Dann sehen Sie, wo Ihr größter Hebel liegt.");
      else say("Stark aufgestellt.", "Im Erstgespräch zeigen wir Ihnen gern, wo trotzdem noch Luft ist – ehrlich und ohne Verkaufsdruck.");

      /* Anliegen für die Buchung: alles, was zu den Hebeln gehört – ohne Doppelte */
      var asks = [];
      gaps.forEach(function (c) {
        (c.getAttribute("data-asks") || "").split(",").forEach(function (a) { if (a && asks.indexOf(a) < 0) asks.push(a); });
      });
      if (cta) {
        cta.setAttribute("data-ask", asks.join(","));
        cta.textContent = gaps.length ? "Erstgespräch dazu buchen" : "Erstgespräch buchen";
        if (!onHome && base) cta.setAttribute("href", asks.length ? base + "?anliegen=" + encodeURIComponent(asks.join(",")) : base);
      }
      out.classList.toggle("has-gap", gaps.length > 0);
      out.classList.toggle("is-done", !open);
      dots.forEach(function (d) {
        var a = ans[d.getAttribute("data-k")];
        d.classList.toggle("is-gap", a === "gap");
        d.classList.toggle("is-ok", a === "ok");
      });
    }

    cards.forEach(function (c) {
      var key = c.getAttribute("data-pillar"), btns = $$(".pillar__ans .chip", c);
      btns.forEach(function (b) {
        b.addEventListener("click", function () {
          var a = b.getAttribute("data-a");
          if (ans[key] === a) delete ans[key]; else ans[key] = a; /* zweiter Klick nimmt die Antwort zurück */
          btns.forEach(function (x) { x.setAttribute("aria-pressed", ans[key] === x.getAttribute("data-a") ? "true" : "false"); });
          c.classList.toggle("is-gap", ans[key] === "gap");
          c.classList.toggle("is-ok", ans[key] === "ok");
          render();
        });
      });
    });
  });
});

/* 28-stage.js */
/* Kundenreise als Bühne: Auf großen Bildschirmen bleibt eine Bühne stehen, Scrollen schaltet die
   vier Stationen um, die Leiste oben zeigt den Fortschritt und springt per Klick zu einer Station.
   Mobil, ohne Skript und bei reduzierter Bewegung stehen die Stationen untereinander. */
ML.module("journey", function (ML) {
  var $ = ML.$, $$ = ML.$$;
  $$("[data-journey]").forEach(function (jr) {
    var sts = $$(".st", jr), rail = $(".jr__rail", jr), steps = $$(".jr__step", jr), fill = $(".jr__bar i", jr);
    var n = sts.length, cur = 0, pinned = false, lock = null;
    if (!n) return;
    var mq = window.matchMedia("(min-width: 1000px) and (min-height: 640px)");

    function fire() {
      var ev;
      try { ev = new CustomEvent("ml:station", { detail: { index: cur, pinned: pinned } }); }
      catch (e) { ev = document.createEvent("CustomEvent"); ev.initCustomEvent("ml:station", false, false, { index: cur, pinned: pinned }); }
      jr.dispatchEvent(ev);
    }
    function activate(i, force) {
      if (i === cur && !force) return;
      cur = i;
      sts.forEach(function (s, j) {
        s.classList.toggle("is-active", j === i);
        s.classList.toggle("is-before", j < i);
      });
      steps.forEach(function (b, j) {
        b.setAttribute("aria-selected", j === i ? "true" : "false");
        b.tabIndex = j === i ? 0 : -1;
        b.classList.toggle("is-done", j < i);
      });
      fire();
    }
    function setMode(on) {
      pinned = on;
      jr.classList.toggle("journey--pin", on);
      if (rail) { rail.hidden = !on; if (on) rail.setAttribute("role", "tablist"); else rail.removeAttribute("role"); }
      steps.forEach(function (b) { if (on) b.setAttribute("role", "tab"); else b.removeAttribute("role"); });
      sts.forEach(function (s) { s.setAttribute("role", on ? "tabpanel" : "group"); });
      activate(cur, true);
      ML.tick();
    }
    function span() { return Math.max(1, jr.offsetHeight - window.innerHeight); }
    function top() { return jr.getBoundingClientRect().top + (window.scrollY || document.documentElement.scrollTop || 0); }

    /* Zu einer Station scrollen (Station 1 so weit, dass der Relaunch fertig ist) */
    function go(i) {
      if (!pinned) { sts[i].scrollIntoView({ behavior: ML.reduce ? "auto" : "smooth", block: "start" }); return; }
      var t = Math.round(top() + span() * ((i + (i === 0 ? 0.8 : 0.3)) / n));
      lock = { i: i, t: t, until: Date.now() + 1600 };
      activate(i);
      window.scrollTo({ top: t, behavior: ML.reduce ? "auto" : "smooth" });
    }
    steps.forEach(function (b, i) {
      b.addEventListener("click", function () { go(i); });
      b.addEventListener("keydown", function (e) {
        var k = null;
        if (e.key === "ArrowRight" || e.key === "ArrowDown") k = Math.min(n - 1, i + 1);
        if (e.key === "ArrowLeft" || e.key === "ArrowUp") k = Math.max(0, i - 1);
        if (e.key === "Home") k = 0;
        if (e.key === "End") k = n - 1;
        if (k === null) return;
        e.preventDefault(); steps[k].focus(); go(k);
      });
    });

    ML.onScroll(function (y, vh) {
      if (!pinned) return;
      var r = jr.getBoundingClientRect();
      if (r.bottom < -vh || r.top > vh * 2) return;
      var p = ML.clamp(-r.top / span(), 0, 1);
      if (fill) fill.style.transform = "scaleX(" + p.toFixed(4) + ")";
      if (lock) {
        if (Date.now() < lock.until && Math.abs(y - lock.t) > 4) return;
        lock = null;
      }
      activate(Math.min(n - 1, Math.floor(p * n)));
    });

    /* Darstellungen in die verfügbare Fläche einpassen; liefert die stärkste Verkleinerung */
    function fit() {
      var least = 1;
      sts.forEach(function (s) {
        var vis = $(".st__vis", s), f = vis && $(".st__fit", vis);
        if (!f) return;
        if (!pinned) { f.style.removeProperty("--fit"); return; }
        var k = Math.min(1, vis.clientWidth / Math.max(1, f.offsetWidth), vis.clientHeight / Math.max(1, f.offsetHeight));
        least = Math.min(least, k);
        f.style.setProperty("--fit", (Math.floor(k * 1000) / 1000).toString());
      });
      return least;
    }
    var stage = $(".jr__stage", jr);
    if ("ResizeObserver" in window && stage) new ResizeObserver(fit).observe(stage);

    /* Bühne nur, wenn alles gut lesbar bleibt: Müsste eine Darstellung stärker als auf
       84 % verkleinert werden (z. B. 1366 × 657), stehen die Stationen untereinander. */
    var MIN_FIT = 0.84;
    /* Nach einer Größenänderung (Fenster, Drehen) wieder bei derselben Station stehen */
    function place(i) {
      if (pinned) {
        var t = Math.round(top() + span() * ((i + (i === 0 ? 0.8 : 0.3)) / n));
        lock = { i: i, t: t, until: Date.now() + 800 };
        activate(i);
        window.scrollTo({ top: t, behavior: "instant" });
      } else {
        sts[i].scrollIntoView({ block: "start", behavior: "instant" });
      }
    }
    function check(user) {
      var r = jr.getBoundingClientRect(), vis = r.top < window.innerHeight && r.bottom > 0, keep = cur, was = pinned;
      var want = mq.matches && !ML.reduce;
      if (want !== pinned) setMode(want);
      if (fit() < MIN_FIT && pinned) { setMode(false); fit(); }
      if (user && vis && (was !== pinned || pinned)) place(keep);
    }
    if (mq.addEventListener) mq.addEventListener("change", function () { check(true); }); else if (mq.addListener) mq.addListener(function () { check(true); });
    var rt = null, lastW = window.innerWidth, lastH = window.innerHeight;
    window.addEventListener("resize", function () {
      clearTimeout(rt);
      rt = setTimeout(function () {
        /* Nur echte Größenänderungen – nicht die ein- und ausfahrende Adressleiste am Handy */
        var w = window.innerWidth, h = window.innerHeight, real = w !== lastW || Math.abs(h - lastH) > 120;
        lastW = w; lastH = h;
        check(real);
      }, 180);
    });
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { check(false); });
    check(false);
  });
});

/* 30-journey.js */
/* Kundenreise: Relaunch (alt → neu), Pipeline, KI-Agent zum Ausprobieren, Kampagne.
   Jede Darstellung startet, sobald sie sichtbar ist. In der angehefteten Kundenreise
   folgt der Relaunch direkt dem Scrollen. */
ML.module("relaunch", function (ML) {
  ML.$$("[data-relaunch]").forEach(function (rl) {
    var frame = rl.closest(".st__frame") || rl.parentNode;
    var btns = ML.$$("[data-rl]", frame);
    var jr = rl.closest("[data-journey]");
    var manual = false;
    function setP(v, animate) {
      rl.classList.toggle("rl--scrub", !animate);
      rl.style.setProperty("--p", v + "%");
      btns.forEach(function (b) { b.setAttribute("aria-pressed", (+b.getAttribute("data-rl") === (v >= 50 ? 100 : 0)) ? "true" : "false"); });
    }
    function sweep() {
      rl.classList.add("is-scanning");
      setP(100, true);
      setTimeout(function () { rl.classList.remove("is-scanning"); }, 1500);
    }
    btns.forEach(function (b) {
      b.addEventListener("click", function () {
        manual = true;
        rl.classList.add("is-scanning");
        setP(+b.getAttribute("data-rl"), true);
        setTimeout(function () { rl.classList.remove("is-scanning"); }, 1500);
      });
    });
    if (ML.reduce) { setP(100, false); return; }
    setP(0, false);
    var pinned = function () { return jr && jr.classList.contains("journey--pin"); };
    /* Auf der Bühne folgt der Relaunch dem Scrollen durch die erste Station */
    ML.onScroll(function (y, vh) {
      if (manual || !pinned()) return;
      var r = jr.getBoundingClientRect();
      if (r.bottom < 0 || r.top > vh) return;
      var n = parseFloat(getComputedStyle(jr).getPropertyValue("--n")) || 4;
      var seg = ML.clamp(-r.top / Math.max(1, r.height - vh), 0, 1) * n;
      var p = ML.clamp((seg - 0.1) / 0.6, 0, 1) * 100;
      rl.classList.toggle("is-scanning", p > 0.5 && p < 99.5);
      setP(Math.round(p * 10) / 10, false);
    });
    /* Wechselt die Darstellung (z. B. Fenster schmaler), steht die neue Seite fertig da */
    if (jr) jr.addEventListener("ml:station", function (ev) {
      var d = ev.detail || {};
      /* Wer die Station verlässt, findet bei der Rückkehr wieder den Scroll-Ablauf vor */
      if (d.pinned && d.index !== 0) manual = false;
      if (!manual && !d.pinned && parseFloat(rl.style.getPropertyValue("--p")) < 100) setP(100, false);
    });
    /* Sonst: einmal automatisch, sobald sichtbar */
    ML.presentOnce(rl, function () {
      if (manual || pinned()) return;
      setTimeout(function () { if (!manual && !pinned()) sweep(); }, 600);
    }, { threshold: 0.5 });
  });
});

ML.module("pipeline", function (ML) {
  var $ = ML.$, $$ = ML.$$;
  $$("[data-pipeline]").forEach(function (pl) {
    var board = $(".pl__board", pl), initial = board.innerHTML;
    var msgEl = $("[data-plmsg]", pl), kOpen = $("[data-plk=open]", pl), kOff = $("[data-plk=offers]", pl);
    var initialMsg = msgEl ? msgEl.textContent : "";
    var tl = ML.timeline(), running = false, manual = false;
    var COLS = ["neu", "gespraech", "angebot", "auftrag"];
    var STEPS = [
      ["c1", "gespraech", "Termin mit Familie Petersen ist eingetragen. Die Erinnerung geht morgen raus."],
      ["c3", "angebot", "Das Angebot für die Weber GmbH ist verschickt."],
      ["c4", "auftrag", "Frau Lindner hat angenommen – aus dem Angebot wird ein Auftrag."],
      ["new", "neu", "Neue Anfrage über die Website: Familie Ahrens, Garderobe nach Maß."]
    ];
    /* Was der Agent sagt, wenn jemand eine Karte von Hand weiterschiebt */
    var SAY = {
      gespraech: function (n) { return "Termin mit " + n + " ist eingetragen. Die Erinnerung geht automatisch raus."; },
      angebot: function (n) { return "Ich bereite das Angebot für " + n + " vor – Sie geben es nur noch frei."; },
      auftrag: function (n) { return n + " hat angenommen. Der Auftrag ist angelegt, die Rechnung folgt nach Abschluss."; },
      fertig: function (n) { return "Für " + n + " ist alles erledigt. Ziehen Sie gern eine andere Karte weiter."; }
    };
    function colName(col) { var h = col.querySelector("h5"); return h && h.firstChild ? String(h.firstChild.textContent).trim() : ""; }
    /* Spaltenzähler und Kennzahlen aus dem, was auf dem Board liegt (plus Karten außerhalb des Ausschnitts) */
    function counts() {
      $$(".pl__col", pl).forEach(function (c) { var n = c.querySelector("[data-colcount]"); if (n) n.textContent = c.querySelectorAll(".pl__card").length; });
      var n = function (k) { return $$('[data-col="' + k + '"] .pl__card', pl).length; };
      if (kOpen) kOpen.textContent = 2 + n("neu") + n("gespraech") + n("angebot");
      if (kOff) kOff.textContent = 2 + n("angebot");
    }
    /* FLIP für alle Karten: Auch Karten, die nur nachrücken, gleiten an ihren neuen Platz */
    function flip(change) {
      var cards = $$(".pl__card", pl), before = cards.map(function (c) { return c.getBoundingClientRect(); });
      var fresh = change();
      cards.forEach(function (c, i) {
        var a = before[i], b = c.getBoundingClientRect();
        var dx = a.left - b.left, dy = a.top - b.top;
        if (!b.width || (Math.abs(dx) < 1 && Math.abs(dy) < 1)) return;
        c.style.transition = "none";
        c.style.transform = "translate(" + dx + "px," + dy + "px)";
        void c.offsetWidth;
        c.style.transition = "transform .75s cubic-bezier(.77,0,.175,1)";
        c.style.transform = "none";
      });
      if (fresh) {
        fresh.style.opacity = "0"; fresh.style.transform = "translateY(-12px)";
        requestAnimationFrame(function () { requestAnimationFrame(function () {
          fresh.style.transition = "opacity .5s ease, transform .6s cubic-bezier(.23,1,.32,1)"; fresh.style.opacity = "1"; fresh.style.transform = "none"; }); });
      }
      counts();
    }
    function moveCard(c, col) {
      var target = $('[data-col="' + col + '"]', pl);
      if (!c || !target) return;
      flip(function () {
        target.appendChild(c);
        /* In der Listenansicht (schmale Bildschirme) wechselt außerdem der Status der Karte */
        c.setAttribute("data-st", col);
        c.classList.add("is-moved");
        var st = c.querySelector(".pl__st"); if (st) st.textContent = colName(target);
        return null;
      });
    }
    function addNew(col) {
      var target = $('[data-col="' + col + '"]', pl);
      if (!target) return;
      flip(function () {
        var card = document.createElement("button");
        card.type = "button";
        card.className = "pl__card is-moved";
        card.setAttribute("data-card", "c6");
        card.setAttribute("data-st", col);
        card.setAttribute("aria-label", "Familie Ahrens: in den nächsten Schritt schieben");
        card.innerHTML = "<b>Familie Ahrens</b><small>Garderobe · Website</small><span class=\"pl__tag\">gerade eben</span><span class=\"pl__st\">" + colName(target) + "</span>";
        target.insertBefore(card, target.children[1] || null);
        return card;
      });
    }
    /* Die Rückfrage des Agenten lässt sich beantworten („Ja, nachfassen“) */
    var reply = $("[data-plreply]", pl);
    function say(t, ask) { if (msgEl) msgEl.textContent = t; if (reply) reply.hidden = !ask; }
    function restore() { board.innerHTML = initial; say(initialMsg, true); counts(); }
    if (reply) reply.addEventListener("click", function () {
      if (!manual) { manual = true; tl.clear(); }
      var c = $('[data-card="c4"]', pl), tag = c && c.querySelector(".pl__tag");
      if (tag) { tag.textContent = "erinnert"; c.classList.add("is-moved"); }
      say("Mache ich: Frau Lindner bekommt heute eine kurze Erinnerung zum Angebot.");
      var k = $(".pl__agent", pl); if (k) { k.classList.remove("is-ok"); void k.offsetWidth; k.classList.add("is-ok"); }
    });
    function cycle() {
      tl.clear();
      STEPS.forEach(function (st, i) {
        tl.at(900 + i * 2300, function () {
          if (st[0] === "new") addNew(st[1]); else moveCard($('[data-card="' + st[0] + '"]', pl), st[1]);
          say(st[2]);
        });
      });
      tl.at(900 + STEPS.length * 2300 + 2600, function () { restore(); if (running && !manual) cycle(); });
    }
    /* Von Hand: Karte antippen schiebt sie einen Schritt weiter (die Vorführung hält dann an) */
    board.addEventListener("click", function (ev) {
      var c = ev.target.closest(".pl__card");
      if (!c || !board.contains(c)) return;
      if (!manual) { manual = true; tl.clear(); }
      var name = (c.querySelector("b") || {}).textContent || "";
      var col = c.closest("[data-col]").getAttribute("data-col"), i = COLS.indexOf(col);
      if (i >= COLS.length - 1) { say(SAY.fertig(name)); c.classList.remove("is-nudge"); void c.offsetWidth; c.classList.add("is-nudge"); return; }
      var next = COLS[i + 1];
      moveCard(c, next);
      say(SAY[next](name));
      c.focus({ preventScroll: true });
    });
    counts();
    if (ML.reduce) return;
    ML.presence(pl, function (v) {
      if (manual) return;
      if (v && !running) { running = true; cycle(); }
      else if (!v && running) { running = false; tl.clear(); restore(); }
    }, { threshold: 0.45 });
  });
});

ML.module("agent", function (ML) {
  var $ = ML.$, $$ = ML.$$;
  var root = $("[data-agent]");
  var asks = ML.json("agent-data");
  if (!root || !asks) return;
  var body = $("[data-wa]", root), btns = $$(".ad__ask", root), live = $("[data-agent-live]", root);
  var ms = $(".ms", root), info = $(".ms__info", root), k = $(".ms__k", root), vOld = $(".v-old", root), vNew = $(".v-new", root);
  var ev = $(".ms__event", root);
  var busy = false, pending = null, touched = false, autoDone = false, uses = {};
  var fast = ML.reduce;
  var tick = '<svg viewBox="0 0 16 11" width="16" height="11" fill="none" stroke="#53BDEB" stroke-width="1.6" aria-hidden="true" style="display:inline-block;vertical-align:-1px;margin-left:3px"><path d="M1 6l3 3 6-7M6 9l1 .8L14 2"/></svg>';
  /* Feste, glaubwürdige Uhrzeiten statt der echten Uhr: jede Nachricht eine Minute später */
  var minute = 9 * 60 + 38;
  function stamp() { var h = Math.floor(minute / 60), m = minute % 60; minute++; return (h < 10 ? "0" : "") + h + ":" + (m < 10 ? "0" : "") + m; }
  function trim() { var all = $$(".cp-msg, .cp-typing", body); while (all.length > 3) { all.shift().remove(); } }
  function bubble(cls, txt, isMe) {
    var d = document.createElement("div");
    d.className = "cp-msg " + cls + " is-pop";
    d.innerHTML = ML.esc(txt) + "<time>" + stamp() + (isMe ? tick : "") + "</time>";
    body.appendChild(d);
    /* Höchstens drei Blasen, damit die neueste Antwort immer ganz zu sehen ist */
    trim();
    return d;
  }
  /* Kleine Infozeile der Website (Mittagstisch, Öffnungszeiten) */
  function updateInfo(v) {
    if (!info) return;
    $$(".ms__v > span", info).forEach(function (s) { s.style.transition = "none"; });
    if (info.classList.contains("is-upd")) vOld.textContent = vNew.textContent;
    info.classList.remove("is-upd", "is-flash");
    void info.offsetWidth;
    $$(".ms__v > span", info).forEach(function (s) { s.style.transition = ""; });
    k.textContent = v.k;
    vNew.textContent = v.v;
    void info.offsetWidth;
    info.classList.add("is-upd", "is-flash");
    setTimeout(function () { info.classList.remove("is-flash"); }, 1500);
  }
  /* Veranstaltung: erscheint groß im Startbereich, mit Button */
  function showEvent(v) {
    if (!ms || !ev) return;
    var map = { k: v.ek, t: v.et, p: v.ep, b: v.eb };
    Object.keys(map).forEach(function (key) { var el = $('[data-ev="' + key + '"]', ev); if (el) el.textContent = map[key]; });
    if (ms.classList.contains("is-event")) { ev.classList.remove("is-flash"); void ev.offsetWidth; ev.classList.add("is-flash"); }
    else ms.classList.add("is-event");
  }
  /* Jede Nachricht hat Varianten: Ein erneuter Klick zeigt eine neue Änderung */
  function next(a) { var i = uses[a.id] || 0; uses[a.id] = i + 1; return a.variants[i % a.variants.length]; }
  function mark(btn) { btns.forEach(function (b) { b.setAttribute("aria-pressed", b === btn ? "true" : "false"); }); }
  function run(a, btn) {
    /* Läuft gerade eine Antwort, kommt die neue Nachricht direkt danach – kein Klick geht verloren */
    if (busy) { pending = { a: a, btn: btn }; mark(btn); return; }
    busy = true;
    mark(btn);
    btns.forEach(function (b) { b.classList.remove("is-hint"); });
    var v = next(a);
    bubble("cp-msg--me", v.me, true);
    setTimeout(function () {
      var t = document.createElement("div"); t.className = "cp-typing is-pop"; t.innerHTML = "<i></i><i></i><i></i>"; body.appendChild(t);
      trim();
    }, fast ? 0 : 650);
    setTimeout(function () {
      var t = $(".cp-typing", body); if (t) t.remove();
      bubble("cp-msg--agent", v.agent, false);
      if (v.type === "event") showEvent(v); else updateInfo(v);
      if (live) live.textContent = "KI-Agent: " + v.agent + " Website: " + (v.type === "event" ? v.ek + ", " + v.et + ", " + v.ep : v.k + ", " + v.v) + ".";
      busy = false;
      if (pending) { var p = pending; pending = null; setTimeout(function () { run(p.a, p.btn); }, fast ? 0 : 450); }
      else if (!touched && btns[1]) btns[1].classList.add("is-hint");
    }, fast ? 50 : 1900);
  }
  btns.forEach(function (b) {
    b.addEventListener("click", function () {
      touched = true;
      var a = asks.filter(function (x) { return x.id === b.getAttribute("data-ask-id"); })[0];
      if (a) run(a, b);
    });
  });
  /* Vorführung einmal von selbst – aber erst, wenn die Demo kurz in Ruhe zu sehen war
     (schnelles Durchscrollen verbraucht sie nicht) */
  var dwell = null;
  ML.presence(root, function (v) {
    clearTimeout(dwell);
    if (!v || touched || autoDone) return;
    dwell = setTimeout(function () { if (!touched && !autoDone) { autoDone = true; run(asks[0], btns[0]); } }, fast ? 0 : 1300);
  }, { threshold: 0.5 });
});

ML.module("campaign", function (ML) {
  ML.$$("[data-campaign]").forEach(function (cg) {
    var nums = ML.$$("[data-count-to]", cg);
    var fmt = function (n) { return String(n).replace(/\B(?=(\d{3})+(?!\d))/g, "."); };
    ML.presentOnce(cg, function () {
      cg.classList.add("is-on");
      if (ML.reduce) return;
      nums.forEach(function (el) {
        var to = +el.getAttribute("data-count-to"), t0 = null;
        function step(t) {
          if (!t0) t0 = t;
          var p = Math.min(1, (t - t0) / 1600), k = 1 - Math.pow(1 - p, 3);
          el.textContent = fmt(Math.round(to * k));
          if (p < 1) requestAnimationFrame(step);
        }
        el.textContent = "0";
        requestAnimationFrame(step);
      });
    }, { threshold: 0.45 });
  });
});

/* 35-mocks.js */
/* Weitere Oberflächen auf den Leistungsseiten: Monatsbericht (Online-Marketing) und
   KI-Agent im Dashboard (KI-Agent). Beide starten einmal, sobald sie zu sehen sind. */
ML.module("report", function (ML) {
  ML.$$("[data-report]").forEach(function (rp) {
    var nums = ML.$$("[data-count-to]", rp);
    ML.presentOnce(rp, function () {
      rp.classList.add("is-on");
      if (ML.reduce) return;
      nums.forEach(function (el) {
        var to = +el.getAttribute("data-count-to"), t0 = null;
        function step(t) {
          if (!t0) t0 = t;
          var p = Math.min(1, (t - t0) / 1300), k = 1 - Math.pow(1 - p, 3);
          el.textContent = String(Math.round(to * k));
          if (p < 1) requestAnimationFrame(step);
        }
        el.textContent = "0";
        requestAnimationFrame(step);
      });
    }, { threshold: 0.4 });
  });
});

ML.module("agentdash", function (ML) {
  var $ = ML.$, $$ = ML.$$;
  $$("[data-agentdash]").forEach(function (root) {
    var btn = $("[data-adb-go]", root), list = $("[data-adb-list]", root);
    if (!btn || !list) return;
    var check = btn.querySelector("svg") ? btn.querySelector("svg").outerHTML : "";
    function done(animate) {
      btn.classList.remove("is-press");
      btn.classList.add("is-done");
      btn.innerHTML = check + "<span>Veröffentlicht</span>";
      var rows = $$(".adb__row", list);
      rows.forEach(function (r) {
        var s = +r.style.getPropertyValue("--slot") + 1;
        r.style.setProperty("--slot", s);
        if (s > 2) r.classList.add("is-leave");
      });
      var n = document.createElement("div");
      n.className = "adb__row is-new" + (animate ? " is-enter" : "");
      n.style.setProperty("--slot", 0);
      n.innerHTML = '<span class="adb__ok">' + check + "</span><b>Profil Dr. Sara Yilmaz veröffentlicht</b><time>gerade eben</time>";
      list.insertBefore(n, list.firstChild);
      if (animate) requestAnimationFrame(function () { requestAnimationFrame(function () { n.classList.remove("is-enter"); }); });
      setTimeout(function () { $$(".is-leave", list).forEach(function (r) { r.remove(); }); }, animate ? 800 : 0);
    }
    var finished = false, timers = [];
    function finish(animate) {
      if (finished) return;
      finished = true;
      timers.forEach(clearTimeout);
      btn.disabled = true;
      done(animate);
      var hint = root.querySelector(".adb__hint"); if (hint) hint.textContent = "Ist online – ohne dass jemand etwas programmieren musste.";
    }
    /* Selbst freigeben geht auch */
    btn.addEventListener("click", function () { finish(!ML.reduce); });
    /* Erst zum Klicken einladen; wer nur schaut, sieht nach ein paar Sekunden trotzdem das Ergebnis */
    ML.presentOnce(root, function () {
      if (ML.reduce) { finish(false); return; }
      timers.push(setTimeout(function () { if (!finished) btn.classList.add("is-hint"); }, 900));
      timers.push(setTimeout(function () { if (!finished) { btn.classList.remove("is-hint"); btn.classList.add("is-press"); } }, 6200));
      timers.push(setTimeout(function () { finish(true); }, 6450));
    }, { threshold: 0.45 });
  });
});

/* 40-refs.js */
/* Referenzen: Screenshots laufen beim Scrollen mit, Vorschau-Dialog für die ganze Seite */
ML.module("cases", function (ML) {
  var shots = ML.$$("[data-scrub]");
  if (!shots.length || ML.reduce) return;
  var active = new Set();
  shots.forEach(function (s) {
    ML.watch(s, function (v) { if (v) active.add(s); else active.delete(s); ML.tick(); }, { rootMargin: "100px 0px" });
  });
  ML.onScroll(function (y, vh) {
    active.forEach(function (s) {
      var img = s.querySelector("img");
      if (!img || !img.complete) return;
      var r = s.getBoundingClientRect();
      var max = img.offsetHeight - r.height;
      if (max <= 0) return;
      var p = ML.clamp((vh - r.top) / (vh + r.height), 0, 1);
      var e = p < 0.5 ? 2 * p * p : 1 - Math.pow(-2 * p + 2, 2) / 2;
      img.style.transform = "translate3d(0," + (-e * max).toFixed(1) + "px,0)";
    });
  });
  shots.forEach(function (s) { var img = s.querySelector("img"); if (img) img.addEventListener("load", ML.tick); });
});

ML.module("ref-dialog", function (ML) {
  var $ = ML.$, $$ = ML.$$;
  var dlg = $("#ref-dialog"), data = ML.json("refs-data");
  if (!dlg || !data) return;
  var view = "desktop", current = null, opener = null, leaving = false;
  function set(key, v) { var el = $("[data-rd=" + key + "]", dlg); if (el) el.textContent = v; }
  function render() {
    var r = data[current]; if (!r) return;
    var isM = view === "mobile";
    set("title", r.title); set("cat", r.cat); set("text", r.text); set("host", r.host);
    $("[data-rd=facts]", dlg).innerHTML = r.facts.map(function (f) { return "<div><dt>" + ML.esc(f[0]) + "</dt><dd>" + ML.esc(f[1]) + "</dd></div>"; }).join("");
    $("[data-rd=nums]", dlg).innerHTML = (r.numsLabel ? '<small class="case__facts-l">' + ML.esc(r.numsLabel) + "</small>" : "") + (r.nums || []).map(function (n) { return "<div><b>" + ML.esc(n[0]) + "</b><small>" + ML.esc(n[1]) + "</small></div>"; }).join("");
    var link = $("[data-rd=link]", dlg); link.href = r.url; link.querySelector("span").textContent = r.visit;
    var frame = $(".rd__frame", dlg); frame.classList.toggle("rd__frame--mobile", isM);
    var img = $(".rd__scroll img", dlg);
    /* Das Bild des vorigen Projekts nicht stehen lassen: erst zeigen, wenn das neue geladen ist */
    var src = isM ? r.mobile : r.desktop;
    if (img.getAttribute("src") !== src) {
      img.style.opacity = "0";
      img.onload = function () { img.style.opacity = ""; };
      img.width = isM ? 520 : 1200; img.height = isM ? r.mobileH : r.desktopH;
      img.src = src;
      if (img.complete && img.naturalWidth) img.style.opacity = "";
    }
    img.alt = "Vorschau der Website " + r.title + (isM ? " auf dem Smartphone" : " am Desktop");
    $$("[data-view]", dlg).forEach(function (b) { b.setAttribute("aria-pressed", b.getAttribute("data-view") === view ? "true" : "false"); });
    $(".rd__scroll", dlg).scrollTop = 0;
  }
  function open(key, from) {
    current = key; opener = from || null;
    view = window.innerWidth < 700 ? "mobile" : "desktop";
    render();
    if (typeof dlg.showModal === "function") dlg.showModal(); else dlg.setAttribute("open", "");
    document.documentElement.style.overflow = "hidden";
    var c = $(".rd__close", dlg); if (c) c.focus();
  }
  function close() { if (typeof dlg.close === "function") dlg.close(); else { dlg.removeAttribute("open"); onClose(); } }
  function onClose() {
    document.documentElement.style.overflow = "";
    if (!leaving && opener && opener.focus) opener.focus({ preventScroll: true });
    leaving = false;
  }
  dlg.addEventListener("close", onClose);
  $$("[data-ref]").forEach(function (b) { b.addEventListener("click", function (e) { e.preventDefault(); open(b.getAttribute("data-ref"), b); }); });
  $(".rd__close", dlg).addEventListener("click", close);
  /* „Ähnliches Projekt anfragen“: Dialog zu, der Fokus geht mit zur Terminbuchung statt zurück zum Projekt */
  $$("[data-close-dialog]", dlg).forEach(function (a) {
    a.addEventListener("click", function () {
      leaving = true;
      close();
      var href = a.getAttribute("href") || "";
      if (href.charAt(0) === "#") setTimeout(function () {
        var t = document.querySelector(href);
        if (t) { if (!t.hasAttribute("tabindex")) t.setAttribute("tabindex", "-1"); t.focus({ preventScroll: true }); }
      }, 60);
    });
  });
  dlg.addEventListener("click", function (e) { if (e.target === dlg) close(); });
  $$("[data-view]", dlg).forEach(function (b) { b.addEventListener("click", function () { view = b.getAttribute("data-view"); render(); }); });
});

/* 50-sections.js */
/* Vergleich, Paket-Finder, Ablauf, Laufband, FAQ, Film */
ML.module("compare", function (ML) {
  var tbl = ML.$(".cmp");
  if (!tbl) return;
  var btns = ML.$$(".cmp-tabs [data-vs]");
  btns.forEach(function (b) {
    b.addEventListener("click", function () {
      tbl.setAttribute("data-vs", b.getAttribute("data-vs"));
      btns.forEach(function (x) { x.setAttribute("aria-pressed", x === b ? "true" : "false"); });
    });
  });
});

ML.module("finder", function (ML) {
  var $ = ML.$, $$ = ML.$$;
  var f = $("[data-finder]");
  if (!f) return;
  var plans = $$("[data-plan]"), wrap = $("[data-plans]");
  var bmap = {}, fit = {};
  try { bmap = JSON.parse(f.getAttribute("data-branchen") || "{}"); } catch (e) { bmap = {}; }
  try { fit = JSON.parse(f.getAttribute("data-fit") || "{}"); } catch (e) { fit = {}; }
  var NAMES = { praesenz: "Präsenz", wachstum: "Wachstum", system: "System" };
  var WHY = {
    praesenz: { ohne: "Eine Website, die bei Google gefunden wird und die Sie per WhatsApp aktuell halten – der beste Start.",
                alt: "Ein Relaunch, der auf dem Smartphone überzeugt und bei Google gefunden wird. Pflege per WhatsApp inklusive.",
                gut: "Wir machen Ihre Website noch sichtbarer und halten sie mit dem KI-Agenten aktuell." },
    wachstum: "Eine Website, die überzeugt, und Kampagnen, die gezielt neue Anfragen bringen – messbar bis zur Buchung.",
    system: "Ein eigenes System, in dem jede Anfrage, jeder Termin und jeder Auftrag landet – direkt mit Ihrer Website verbunden."
  };
  function pick(web, ziel) {
    if (ziel === "verwaltung") return "system";
    if (ziel === "anfragen") return "wachstum";
    return web === "gut" ? "wachstum" : "praesenz";
  }
  function asksFor(plan, web) {
    var site = web === "gut" ? "web-besser" : "web-neu";
    if (plan === "praesenz") return [site, "agent"];
    if (plan === "wachstum") return [site, "werbung"];
    return web === "gut" ? ["system"] : ["system", site];
  }
  function update() {
    var br = f.elements.branche.value, web = f.elements.web.value, ziel = f.elements.ziel.value;
    var plan = pick(web, ziel);
    var why = WHY[plan]; if (typeof why === "object") why = why[web];
    $("[data-fr=name]", f).textContent = NAMES[plan];
    $("[data-fr=why]", f).textContent = why;
    var fitEl = $("[data-fr=fit]", f);
    if (fitEl) fitEl.textContent = (fit[br] && fit[br][plan]) || "";
    var cta = $("[data-fr=cta]", f);
    var asks = asksFor(plan, web).join(",");
    cta.setAttribute("data-ask", asks);
    cta.setAttribute("data-branche", bmap[br] || "");
    if (!document.getElementById("booking")) {
      var base = cta.getAttribute("href").split("?")[0];
      cta.setAttribute("href", base + "?anliegen=" + encodeURIComponent(asks) + "&branche=" + encodeURIComponent(bmap[br] || ""));
    }
    plans.forEach(function (p) { p.classList.toggle("is-match", p.getAttribute("data-plan") === plan); });
    if (wrap) wrap.classList.add("has-match");
  }
  /* Sichtbaren Wert neben dem (unsichtbaren) Auswahlfeld nachführen */
  $$("select", f).forEach(function (s) {
    var val = s.parentNode.querySelector(".finder__val");
    s.addEventListener("change", function () { if (val) val.textContent = s.options[s.selectedIndex].text; update(); });
  });
  update();
});

ML.module("process", function (ML) {
  ML.$$("[data-proc]").forEach(function (list) {
    var line = list.querySelector(".proc__line i"), items = ML.$$(".proc__item", list);
    var vertical = function () { return getComputedStyle(list).gridTemplateColumns.split(" ").length === 1; };
    if (ML.reduce) { if (line) line.style.transform = "none"; items.forEach(function (i) { i.classList.add("is-on"); }); return; }
    ML.onScroll(function (y, vh) {
      var r = list.getBoundingClientRect();
      if (r.bottom < -50 || r.top > vh + 50) return;
      var v = vertical();
      var p = v ? ML.clamp((vh * 0.65 - r.top) / r.height, 0, 1) : ML.clamp((vh * 0.8 - r.top) / (vh * 0.45), 0, 1);
      if (line) line.style.transform = v ? "scaleY(" + p.toFixed(3) + ")" : "scaleX(" + p.toFixed(3) + ")";
      items.forEach(function (it, i) {
        var on = v ? it.getBoundingClientRect().top < vh * 0.65 : p >= (i / Math.max(1, items.length - 1)) - 0.02;
        it.classList.toggle("is-on", on);
      });
    });
  });
});

ML.module("marquee", function (ML) {
  ML.$$("[data-marquee]").forEach(function (m) {
    ML.watch(m, function (v) { m.classList.toggle("is-paused", !v); });
    /* Zum Ansehen anhalten: Zeiger darüber oder Finger darauf */
    m.addEventListener("pointerenter", function (e) { if (e.pointerType === "mouse") m.classList.add("is-hold"); });
    m.addEventListener("pointerleave", function () { m.classList.remove("is-hold"); });
    m.addEventListener("touchstart", function () { m.classList.add("is-hold"); }, { passive: true });
    m.addEventListener("touchend", function () { setTimeout(function () { m.classList.remove("is-hold"); }, 1200); }, { passive: true });
  });
});

ML.module("faq", function (ML) {
  ML.$$("[data-faq]").forEach(function (list) {
    var items = ML.$$("details", list);
    items.forEach(function (d) {
      d.addEventListener("toggle", function () {
        if (!d.open) return;
        items.forEach(function (o) { if (o !== d) o.open = false; });
      });
    });
  });
  /* Links auf eine Antwort (#faq-…) klappen sie auf – die anderen sofort zu, damit sich beim
     Scrollen nichts mehr verschiebt – und führen dann genau dorthin */
  function openTarget(id) {
    var d = id && document.getElementById(id);
    if (!d || d.tagName !== "DETAILS") return null;
    var list = d.closest("[data-faq]");
    if (list) ML.$$("details", list).forEach(function (o) { if (o !== d) o.open = false; });
    d.open = true;
    return d;
  }
  ML.$$("[data-faq-link]").forEach(function (a) {
    a.addEventListener("click", function (e) {
      var id = (a.getAttribute("href") || "").replace(/^#/, ""), d = openTarget(id);
      if (!d) return;
      e.preventDefault();
      /* Ziel aus dem Layout berechnen (ohne die Einblend-Verschiebung), Abstand wie bei Ankern */
      var y = 0, el = d;
      while (el) { y += el.offsetTop; el = el.offsetParent; }
      var pad = parseFloat(getComputedStyle(document.documentElement).scrollPaddingTop) || 0;
      window.scrollTo({ top: Math.max(0, y - pad), behavior: ML.reduce ? "auto" : "smooth" });
      try { history.pushState(null, "", "#" + id); } catch (err) { /* egal */ }
      var s = d.querySelector("summary"); if (s) s.focus({ preventScroll: true });
    });
  });
  if (location.hash && /^#faq-/.test(location.hash)) {
    var t = openTarget(location.hash.slice(1));
    if (t) setTimeout(function () { t.scrollIntoView({ block: "start" }); }, 60);
  }
  window.addEventListener("hashchange", function () { if (/^#faq-/.test(location.hash)) openTarget(location.hash.slice(1)); });
});

/* Erklärfilm: großer Abspiel-Knopf, Kapitel springen an die Stelle, das laufende Kapitel ist markiert.
   Der Film lädt erst beim Abspielen und hält an, wenn er aus dem Bild gescrollt wird. */
ML.module("film", function (ML) {
  ML.$$("[data-film]").forEach(function (root) {
    var v = ML.$(".film__video", root), btn = ML.$(".film__play", root), chs = ML.$$(".film__ch", root);
    if (!v || !btn) return;
    v.removeAttribute("controls");
    var at = chs.map(function (c) { return parseFloat(c.getAttribute("data-at")) || 0; });
    var lbl = ML.$(".film__lbl b", root);
    function mark() {
      var t = v.currentTime || 0, k = 0;
      at.forEach(function (a, i) { if (t >= a - 0.1) k = i; });
      chs.forEach(function (c, i) { c.classList.toggle("is-on", i === k); c.setAttribute("aria-pressed", i === k ? "true" : "false"); });
    }
    function start(t) {
      root.classList.add("is-started");
      v.setAttribute("controls", "");
      /* play() direkt im Klick, damit der Ton erlaubt ist; die Sprungstelle folgt, sobald die Länge bekannt ist */
      var p = v.play(); if (p && p.catch) p.catch(function () { root.classList.remove("is-started"); });
      if (t != null) {
        if (v.readyState >= 1) v.currentTime = t;
        else {
          v.addEventListener("loadedmetadata", function once() { v.removeEventListener("loadedmetadata", once); v.currentTime = t; });
          /* Sicherheitshalber noch einmal, sobald abgespielt werden kann */
          v.addEventListener("canplay", function again() { v.removeEventListener("canplay", again); if (Math.abs(v.currentTime - t) > 1) v.currentTime = t; });
        }
      }
      mark();
    }
    btn.addEventListener("click", function () { start(v.ended ? 0 : null); try { v.focus({ preventScroll: true }); } catch (e) { /* egal */ } });
    chs.forEach(function (c, i) { c.addEventListener("click", function () { start(at[i]); }); });
    v.addEventListener("timeupdate", mark);
    v.addEventListener("seeked", mark);
    v.addEventListener("ended", function () {
      root.classList.remove("is-started"); v.removeAttribute("controls");
      if (lbl) lbl.textContent = "Noch einmal ansehen";
    });
    ML.watch(root, function (vis) { if (!vis && !v.paused) v.pause(); }, { threshold: 0.15 });
    /* Start aus dem Kopfbereich: kommt synchron aus dem Klick, damit der Ton erlaubt bleibt */
    root.addEventListener("ml:play", function () { if (v.paused) start(v.ended ? 0 : null); });
  });

  /* „Film ansehen“ oben: zum Film scrollen (mittig, unter der Kopfleiste) und abspielen */
  ML.$$("[data-film-jump]").forEach(function (a) {
    a.addEventListener("click", function (ev) {
      var sec = document.getElementById("film"), root = sec && ML.$("[data-film]", sec);
      if (!root) return;
      ev.preventDefault();
      /* Einblendungen im Ziel sofort fertig zeigen, damit die Maße stimmen (sie wären sonst noch verkleinert) */
      var rv = ML.$$("[data-reveal]", sec);
      rv.forEach(function (el) { el.style.transition = "none"; el.classList.add("is-in"); });
      var fr = ML.$(".film__frame", root) || root, r = fr.getBoundingClientRect();
      rv.forEach(function (el) { el.style.transition = ""; });
      var head = (ML.$(".header") || {}).offsetHeight || 0;
      /* Passt die Überschrift mit aufs Bild, beginnt die Ansicht bei ihr; sonst steht der Film mittig */
      var h = ML.$("h2", sec), top = Math.min(r.top, h ? h.getBoundingClientRect().top : r.top);
      var y = r.bottom - top + head + 40 <= window.innerHeight ? top - head - 24 : r.top - Math.max(head + 16, (window.innerHeight - r.height) / 2);
      var reduce = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
      window.scrollTo({ top: Math.max(0, y + window.scrollY), behavior: reduce ? "auto" : "smooth" });
      root.dispatchEvent(new CustomEvent("ml:play"));
    });
  });
});

/* Fußzeile: Erreichbarkeit nach Hamburger Zeit („Jetzt erreichbar“ oder wann wir wieder da sind) */
ML.module("reach", function (ML) {
  var el = ML.$("[data-reach]"); if (!el) return;
  var out = ML.$("[data-reach-text]", el);
  var H = { 1: [9, 18], 2: [9, 18], 3: [9, 18], 4: [9, 18], 5: [9, 16] };
  var NAMES = ["Sonntag", "Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag"];
  function now() {
    var p = {}; new Intl.DateTimeFormat("en-US", { timeZone: "Europe/Berlin", weekday: "short", hour: "numeric", minute: "numeric", hourCycle: "h23" })
      .formatToParts(new Date()).forEach(function (x) { p[x.type] = x.value; });
    return { d: ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"].indexOf(p.weekday), h: +p.hour + (+p.minute) / 60 };
  }
  function update() {
    var n = now(), t = H[n.d], open = !!t && n.h >= t[0] && n.h < t[1];
    el.classList.toggle("is-open", open);
    if (open) { out.textContent = "Jetzt erreichbar – heute bis " + t[1] + " Uhr"; return; }
    for (var i = 0; i < 8; i++) {
      var d = (n.d + i) % 7, w = H[d];
      if (!w || (i === 0 && n.h >= w[0])) continue;
      out.textContent = "Wieder erreichbar " + (i === 0 ? "heute" : i === 1 ? "morgen" : "am " + NAMES[d]) + " ab " + w[0] + " Uhr · WhatsApp jederzeit";
      return;
    }
  }
  try { update(); setInterval(update, 60000); } catch (e) { /* Text mit den Zeiten bleibt stehen */ }
});

/* 80-booking.js */
/* Terminbuchung: mehrstufig, mit Kalender (Feiertage, deutsche Zeit), Rückruf-Option und WhatsApp */
ML.module("booking", function (ML) {
  var $ = ML.$, $$ = ML.$$, store = ML.store, esc = ML.esc, CFG = ML.cfg, reduce = ML.reduce;
  var bk = $("#booking");
  if (bk) booking(bk);

  function booking(root) {
    var form = $("form", root);
    var steps = $$(".bk__step", root);
    var prog = $$(".bk__progress li", root);
    var err = $(".bk__err", root);
    var btnBack = $("[data-back]", root), btnNext = $("[data-next]", root);
    var navBar = $(".bk__nav", root);
    var demo = root.getAttribute("data-demo") === "1";
    var endpoint = root.getAttribute("data-endpoint");
    var slotsUrl = root.getAttribute("data-slots");
    var C = CFG.booking || {};
    var DUR = C.duration || 30, SLOT = C.step || 30, AHEAD = C.daysAhead || 42, LEAD = C.leadHours || 18;
    var HOURS = C.hours || { 1: ["09:00", "18:00"], 2: ["09:00", "18:00"], 3: ["09:00", "18:00"], 4: ["09:00", "18:00"], 5: ["09:00", "16:00"] };
    var booked = {};
    var step = 1, sel = { date: null, time: null }, month = null;
    var KEY = "ml-booking";

    /* Prefill aus URL, Paket-Buttons und Sitzung */
    var saved = store.get(KEY);
    var qs = new URLSearchParams(location.search);
    $$("[data-ask]").forEach(function (b) {
      b.addEventListener("click", function () {
        var ask = b.getAttribute("data-ask");
        if (ask) { $$('input[name="anliegen"]', form).forEach(function (i) { i.checked = false; }); preselect(ask.split(",")); }
        var br = b.getAttribute("data-branche");
        if (br && form.elements.branche) { form.elements.branche.value = br; persist(); }
        if (step !== 1) go(1, true);
      });
    });
    function preselect(list) {
      list.forEach(function (v) { var i = form.querySelector('input[name="anliegen"][value="' + v.trim() + '"]'); if (i) i.checked = true; });
      persist();
    }

    /* Gebuchte Zeiten laden (nur live) */
    if (!demo && slotsUrl) {
      fetch(slotsUrl, { headers: { "Accept": "application/json" } }).then(function (r) { return r.ok ? r.json() : null; })
        .then(function (j) { if (j && j.booked) { j.booked.forEach(function (s) { booked[s] = true; }); renderCal(); } })
        .catch(function () { /* ohne Liste weiter */ });
    }

    /* ---------- Feiertage (bundesweit + Hamburg) ---------- */
    function easter(y) {
      var a = y % 19, b = Math.floor(y / 100), c = y % 100, d = Math.floor(b / 4), e = b % 4, f = Math.floor((b + 8) / 25),
        g = Math.floor((b - f + 1) / 3), h = (19 * a + b - d - g + 15) % 30, i = Math.floor(c / 4), k = c % 4,
        l = (32 + 2 * e + 2 * i - h - k) % 7, m = Math.floor((a + 11 * h + 22 * l) / 451),
        mo = Math.floor((h + l - 7 * m + 114) / 31), da = ((h + l - 7 * m + 114) % 31) + 1;
      return new Date(Date.UTC(y, mo - 1, da));
    }
    var holCache = {};
    function holidays(y) {
      if (holCache[y]) return holCache[y];
      var e = easter(y), add = function (n) { var d = new Date(e); d.setUTCDate(d.getUTCDate() + n); return ymd(d.getUTCFullYear(), d.getUTCMonth() + 1, d.getUTCDate()); };
      var list = [ymd(y, 1, 1), add(-2), add(1), ymd(y, 5, 1), add(39), add(50), ymd(y, 10, 3), ymd(y, 10, 31), ymd(y, 12, 24), ymd(y, 12, 25), ymd(y, 12, 26), ymd(y, 12, 31)];
      var set = {}; list.forEach(function (s) { set[s] = true; }); holCache[y] = set; return set;
    }
    (C.closed || []).forEach(function (s) { var y = +s.slice(0, 4); holidays(y)[s] = true; });

    /* ---------- Zeit-Helfer (Europe/Berlin) ---------- */
    function pad(n) { return (n < 10 ? "0" : "") + n; }
    function ymd(y, m, d) { return y + "-" + pad(m) + "-" + pad(d); }
    /* Ein Formatierer für alle Abfragen und ein Merkzettel je Tag und Stunde: Intl neu anzulegen kostet auf dem Handy spürbar Zeit */
    var offFmt = null, offCache = {};
    function berlinOffsetMin(y, m, d, hh, mm) {
      var key = y + "-" + m + "-" + d + "-" + hh;
      if (offCache[key] != null) return offCache[key];
      return (offCache[key] = offsetNow(y, m, d, hh, mm));
    }
    function offsetNow(y, m, d, hh, mm) {
      try {
        var dt = new Date(Date.UTC(y, m - 1, d, hh, mm));
        offFmt = offFmt || new Intl.DateTimeFormat("en-US", { timeZone: "Europe/Berlin", timeZoneName: "shortOffset" });
        var parts = offFmt.formatToParts(dt);
        var tz = (parts.find(function (p) { return p.type === "timeZoneName"; }) || {}).value || "GMT+1";
        var mt = tz.match(/GMT([+-]\d+)(?::(\d+))?/);
        return mt ? (parseInt(mt[1], 10) * 60 + (mt[2] ? parseInt(mt[2], 10) : 0)) : 60;
      } catch (e) { return (m > 3 && m < 11) ? 120 : 60; }
    }
    function slotEpoch(dateStr, time) {
      var p = dateStr.split("-").map(Number), t = time.split(":").map(Number);
      var off = berlinOffsetMin(p[0], p[1], p[2], t[0], t[1]);
      return Date.UTC(p[0], p[1] - 1, p[2], t[0], t[1]) - off * 60000;
    }
    function isoWithOffset(dateStr, time) {
      var p = dateStr.split("-").map(Number), t = time.split(":").map(Number);
      var off = berlinOffsetMin(p[0], p[1], p[2], t[0], t[1]);
      var s = off >= 0 ? "+" : "-", a = Math.abs(off);
      return dateStr + "T" + time + ":00" + s + pad(Math.floor(a / 60)) + ":" + pad(a % 60);
    }
    function berlinToday() {
      try {
        var f = new Intl.DateTimeFormat("en-CA", { timeZone: "Europe/Berlin", year: "numeric", month: "2-digit", day: "2-digit" }).format(new Date());
        return f;
      } catch (e) { var d = new Date(); return ymd(d.getFullYear(), d.getMonth() + 1, d.getDate()); }
    }
    function weekday(dateStr) { var p = dateStr.split("-").map(Number); return new Date(Date.UTC(p[0], p[1] - 1, p[2])).getUTCDay(); }
    function addDays(dateStr, n) { var p = dateStr.split("-").map(Number); var d = new Date(Date.UTC(p[0], p[1] - 1, p[2] + n)); return ymd(d.getUTCFullYear(), d.getUTCMonth() + 1, d.getUTCDate()); }
    var DOW = ["So", "Mo", "Di", "Mi", "Do", "Fr", "Sa"];
    var DOWL = ["Sonntag", "Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag"];
    var MON = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"];
    function fmtDate(dateStr, long) {
      var p = dateStr.split("-").map(Number), w = weekday(dateStr);
      return (long ? DOWL[w] : DOW[w]) + ", " + p[2] + ". " + MON[p[1] - 1] + (long ? " " + p[0] : "");
    }

    function slotsFor(dateStr) {
      var w = weekday(dateStr), h = HOURS[w];
      if (!h || holidays(+dateStr.slice(0, 4))[dateStr]) return [];
      var out = [], from = h[0].split(":").map(Number), to = h[1].split(":").map(Number);
      var m = from[0] * 60 + from[1], end = to[0] * 60 + to[1] - DUR, now = Date.now() + LEAD * 3600000;
      for (; m <= end; m += SLOT) {
        var t = pad(Math.floor(m / 60)) + ":" + pad(m % 60);
        if (slotEpoch(dateStr, t) < now) continue;
        if (booked[dateStr + "T" + t]) continue;
        out.push(t);
      }
      return out;
    }
    var today = berlinToday(), lastDay = addDays(today, AHEAD);
    function availDays() {
      var list = [];
      for (var i = 0; i <= AHEAD; i++) { var d = addDays(today, i); if (slotsFor(d).length) list.push(d); }
      return list;
    }

    /* ---------- Kalender ---------- */
    var calGrid = $(".cal__grid", root), calTitle = $(".cal__head b", root);
    var calPrev = $("[data-cal-prev]", root), calNext = $("[data-cal-next]", root);
    var slotBox = $(".slots", root);
    var cbOnly = $("#bk-callback", root), calWrap = $(".cal", root), cbWrap = $(".bk__cb", root);
    function renderCal() {
      if (!calGrid) return;
      var avail = {}; availDays().forEach(function (d) { avail[d] = true; });
      if (!month) { var first = Object.keys(avail)[0] || today; month = first.slice(0, 7); }
      var y = +month.slice(0, 4), m = +month.slice(5, 7);
      calTitle.textContent = MON[m - 1] + " " + y;
      var firstDow = (new Date(Date.UTC(y, m - 1, 1)).getUTCDay() + 6) % 7;
      var days = new Date(Date.UTC(y, m, 0)).getUTCDate();
      var html = ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"].map(function (d) { return '<span class="cal__dow">' + d + "</span>"; }).join("");
      for (var i = 0; i < firstDow; i++) html += "<span></span>";
      for (var d = 1; d <= days; d++) {
        var ds = ymd(y, m, d), cls = "cal__day", attrs = "";
        if (avail[ds]) { cls += " is-avail"; attrs = ' data-date="' + ds + '" aria-label="' + fmtDate(ds, true) + ', Termine verfügbar"'; }
        else attrs = ' disabled aria-label="' + fmtDate(ds, true) + ', keine Termine"';
        if (ds === sel.date) cls += " is-sel";
        if (ds === today) cls += " is-today";
        html += '<button type="button" class="' + cls + '"' + attrs + (ds === sel.date ? ' aria-pressed="true"' : "") + ">" + d + "</button>";
      }
      calGrid.innerHTML = html;
      calPrev.disabled = month <= today.slice(0, 7);
      calNext.disabled = month >= lastDay.slice(0, 7);
      renderSlots();
    }
    function renderSlots() {
      if (!slotBox) return;
      if (!sel.date) { slotBox.innerHTML = '<p class="slots__h">Uhrzeit<small>Bitte zuerst einen Tag wählen.</small></p>'; return; }
      var list = slotsFor(sel.date);
      var html = '<p class="slots__h">' + fmtDate(sel.date) + '<small>Deutsche Zeit, ' + DUR + " Minuten</small></p>";
      if (!list.length) html += '<p class="slots__empty">An diesem Tag ist leider nichts mehr frei.</p>';
      list.forEach(function (t) { html += '<button type="button" class="slot" data-time="' + t + '" aria-pressed="' + (sel.time === t ? "true" : "false") + '">' + t + " Uhr</button>"; });
      slotBox.innerHTML = html;
    }
    if (calGrid) {
      calGrid.addEventListener("click", function (e) {
        var b = e.target.closest("[data-date]"); if (!b) return;
        sel.date = b.getAttribute("data-date"); sel.time = null; renderCal(); persist();
        var first = $(".slot", slotBox); if (first && window.innerWidth < 700) first.scrollIntoView({ block: "nearest", behavior: reduce ? "auto" : "smooth" });
      });
      slotBox.addEventListener("click", function (e) {
        var b = e.target.closest("[data-time]"); if (!b) return;
        sel.time = b.getAttribute("data-time"); renderSlots(); persist(); clearErr();
      });
      calPrev.addEventListener("click", function () { var y = +month.slice(0, 4), m = +month.slice(5, 7) - 1; if (m < 1) { m = 12; y--; } month = y + "-" + pad(m); renderCal(); });
      calNext.addEventListener("click", function () { var y = +month.slice(0, 4), m = +month.slice(5, 7) + 1; if (m > 12) { m = 1; y++; } month = y + "-" + pad(m); renderCal(); });
      if (cbOnly) cbOnly.addEventListener("change", function () { calWrap.hidden = cbOnly.checked; cbWrap.hidden = !cbOnly.checked; persist(); });
      renderCal();
    }

    /* ---------- Schritte ---------- */
    function val(name) { var el = form.elements[name]; if (!el) return ""; if (el.length && !el.tagName) { var c = Array.prototype.find.call(el, function (x) { return x.checked; }); return c ? c.value : ""; } return (el.value || "").trim(); }
    function checkedList(name) { return $$('input[name="' + name + '"]:checked', form).map(function (i) { return i.value; }); }
    function labelOf(input) { var l = form.querySelector('label[for="' + input.id + '"] b'); return l ? l.textContent : input.value; }
    function clearErr() { err.textContent = ""; $$(".is-invalid", form).forEach(function (f) { f.classList.remove("is-invalid"); }); $$("[aria-invalid]", form).forEach(function (f) { f.removeAttribute("aria-invalid"); }); }
    function bad(msg, names) {
      err.textContent = msg;
      (names || []).forEach(function (n) {
        var el = form.elements[n]; if (!el) return;
        var f = (el.closest ? el : el[0]).closest(".field"); if (f) f.classList.add("is-invalid");
        if (el.setAttribute) el.setAttribute("aria-invalid", "true");
      });
      var first = names && names.length && form.elements[names[0]];
      if (first && first.focus) first.focus();
      return false;
    }
    function validate(s) {
      clearErr();
      if (s === 1 && !checkedList("anliegen").length) return bad("Bitte wählen Sie mindestens ein Anliegen.");
      if (s === 2) {
        var miss = [];
        if (!val("firma")) miss.push("firma");
        if (!val("branche")) miss.push("branche");
        if (miss.length) return bad("Bitte nennen Sie Ihr Unternehmen und Ihre Branche.", miss);
        var w = val("website");
        if (w && !/^(https?:\/\/)?[^\s.]+\.[^\s]{2,}$/i.test(w)) return bad("Bitte prüfen Sie die Adresse Ihrer Website.", ["website"]);
      }
      if (s === 3) {
        if (!val("format")) return bad("Bitte wählen Sie, wie das Gespräch stattfinden soll.");
        if (!(cbOnly && cbOnly.checked) && !(sel.date && sel.time)) return bad("Bitte wählen Sie einen Tag und eine Uhrzeit oder fordern Sie einen Rückruf an.");
      }
      if (s === 4) {
        var m = [];
        if (val("name").length < 2) m.push("name");
        if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(val("email"))) m.push("email");
        var needPhone = val("format") === "telefon" || (cbOnly && cbOnly.checked) || $("#bk-wa", form).checked;
        if (needPhone && val("telefon").replace(/\D/g, "").length < 6) m.push("telefon");
        if (m.length) return bad(m.indexOf("telefon") >= 0 && m.length === 1 ? "Für Telefonat, Rückruf oder WhatsApp brauchen wir Ihre Nummer." : "Bitte prüfen Sie die markierten Felder.", m);
        if (!$("#bk-consent", form).checked) return bad("Bitte bestätigen Sie die Einwilligung zur Bearbeitung Ihrer Anfrage.", ["einwilligung"]);
      }
      return true;
    }
    function go(n, quiet) {
      step = n;
      steps.forEach(function (s) {
        var on = +s.getAttribute("data-step") === n;
        s.hidden = !on;
        if (on) { s.classList.remove("is-enter"); void s.offsetWidth; s.classList.add("is-enter"); }
      });
      prog.forEach(function (li) { var p = +li.getAttribute("data-p"); li.classList.toggle("is-on", p === n); li.classList.toggle("is-done", p < n); });
      btnBack.hidden = n === 1 || n === 5;
      navBar.hidden = n === 5;
      var isCb = cbOnly && cbOnly.checked;
      btnNext.textContent = n === 4 ? (isCb ? "Rückruf anfordern" : "Termin anfragen") : "Weiter";
      var lead4 = $('[data-step="4"] > p', root);
      if (lead4) lead4.textContent = isCb ? "Fast geschafft. Wir rufen Sie im gewünschten Zeitraum zurück." : "Fast geschafft. Wir bestätigen Ihren Termin per E-Mail.";
      if (n === 4) renderPick();
      if (!quiet) {
        var h = $(".bk__step:not([hidden]) h3", root);
        if (h) { h.setAttribute("tabindex", "-1"); h.focus({ preventScroll: true }); }
        /* Zum Formular scrollen (nicht zur Seitenleiste darüber), unter der festen Kopfzeile */
        var hd = document.querySelector(".header"), off = (hd ? hd.offsetHeight : 72) + 12;
        var top = form.getBoundingClientRect().top;
        if (top < off - 4 || top > window.innerHeight * 0.5) window.scrollTo({ top: Math.max(0, Math.round(top + (window.scrollY || 0) - off)), behavior: reduce ? "auto" : "smooth" });
      }
      persist();
    }
    function renderPick() {
      var box = $(".bk__pick", root); if (!box) return;
      var fmt = $('input[name="format"]:checked', form);
      var when = (cbOnly && cbOnly.checked) ? "Rückruf, " + (val("zeitfenster") || "flexibel") : (sel.date ? fmtDate(sel.date, true) + ", " + sel.time + " Uhr" : "");
      box.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><rect x="3" y="4.5" width="18" height="16" rx="3"/><path d="M3 9.5h18M8 2.5v4M16 2.5v4"/></svg><span><b>' + esc(when) + "</b>" + (fmt ? " · " + esc(labelOf(fmt)) : "") + '</span><button type="button" data-goto="3">Ändern</button>';
      $("[data-goto]", box).addEventListener("click", function () { go(3); });
    }
    btnBack.addEventListener("click", function () { if (step > 1) go(step - 1); });
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!validate(step)) return;
      if (step < 4) { go(step + 1); return; }
      send();
    });
    form.addEventListener("change", function () { persist(); });
    form.addEventListener("input", function (e) { if (e.target.closest(".is-invalid")) e.target.closest(".is-invalid").classList.remove("is-invalid"); persist(); });

    function payload() {
      var anl = $$('input[name="anliegen"]:checked', form);
      var fmt = $('input[name="format"]:checked', form);
      var utm = {}; ["utm_source", "utm_medium", "utm_campaign", "gclid"].forEach(function (k) { if (qs.get(k)) utm[k] = qs.get(k); });
      var cb = cbOnly && cbOnly.checked;
      return {
        anliegen: anl.map(function (i) { return i.value; }),
        anliegen_text: anl.map(labelOf),
        firma: val("firma"), branche: val("branche"), website: val("website"), ort: val("ort"), groesse: val("groesse"),
        format: fmt ? fmt.value : "", format_text: fmt ? labelOf(fmt) : "",
        termin: cb ? null : { start: isoWithOffset(sel.date, sel.time), datum: sel.date, uhrzeit: sel.time, dauer_min: DUR },
        rueckruf: cb ? { zeitfenster: val("zeitfenster") || "flexibel" } : null,
        name: val("name"), email: val("email"), telefon: val("telefon"),
        whatsapp_ok: $("#bk-wa", form).checked, nachricht: val("nachricht"),
        einwilligung: $("#bk-consent", form).checked,
        quelle: { seite: location.pathname, referrer: document.referrer || "", utm: utm },
        hp: val("ml_zx")
      };
    }
    function send() {
      var data = payload();
      btnNext.disabled = true;
      btnNext.textContent = "Wird gesendet …";
      var done = function (ok, msg) {
        btnNext.disabled = false;
        if (ok) { finish(data); store.del(KEY); }
        else { go(4); err.textContent = msg || "Das hat leider nicht geklappt. Bitte versuchen Sie es erneut oder schreiben Sie uns per WhatsApp."; }
      };
      if (demo || !endpoint) { setTimeout(function () { done(true); }, 700); return; }
      fetch(endpoint, { method: "POST", headers: { "Content-Type": "application/json", "Accept": "application/json" }, body: JSON.stringify(data) })
        .then(function (r) { return r.json().catch(function () { return { ok: false }; }).then(function (j) { return { status: r.status, j: j }; }); })
        .then(function (res) {
          if (res.j && res.j.ok) done(true);
          else if (res.status === 409) { booked[data.termin && (data.termin.datum + "T" + data.termin.uhrzeit)] = true; sel.time = null; renderCal(); go(3); err.textContent = "Dieser Termin wurde gerade vergeben. Bitte wählen Sie eine andere Uhrzeit."; btnNext.disabled = false; }
          else done(false, res.j && res.j.error);
        })
        .catch(function () { done(false); });
    }
    function finish(d) {
      go(5);
      var first = d.name.split(" ")[0];
      $(".done__name", root).textContent = first ? ", " + first : "";
      var ZF = { vormittags: "vormittags", nachmittags: "nachmittags", flexibel: "wann es Ihnen passt" };
      var when = d.termin ? fmtDate(d.termin.datum, true) + ", " + d.termin.uhrzeit + " Uhr (" + d.format_text + ")" : "Rückruf, " + (ZF[d.rueckruf.zeitfenster] || d.rueckruf.zeitfenster);
      var line = $(".done__line", root);
      if (line) {
        if (d.termin) { line.innerHTML = 'Ihre Anfrage für <b class="done__when"></b> ist bei uns eingegangen. Sie erhalten in Kürze eine Bestätigung per E-Mail.'; line.querySelector("b").textContent = when; }
        else { line.innerHTML = 'Ihre Rückrufbitte ist bei uns eingegangen. Wir melden uns <b class="done__when"></b> bei Ihnen.'; line.querySelector("b").textContent = ZF[d.rueckruf.zeitfenster] || "zeitnah"; }
      }
      var sum = $(".done .summary", root);
      sum.innerHTML = [
        [d.termin ? "Termin" : "Rückruf", d.termin ? when : (ZF[d.rueckruf.zeitfenster] || d.rueckruf.zeitfenster)], ["Anliegen", d.anliegen_text.join(", ")], ["Unternehmen", d.firma + (d.branche ? " · " + d.branche : "")], ["Kontakt", d.email + (d.telefon ? " · " + d.telefon : "")]
      ].map(function (r) { return "<div><dt>" + esc(r[0]) + "</dt><dd>" + esc(r[1]) + "</dd></div>"; }).join("");
      var ics = $("[data-ics]", root);
      if (ics) {
        ics.hidden = demo || !d.termin;
        ics.onclick = function () { downloadIcs(d); };
      }
      var wa = $("[data-wa-done]", root);
      if (wa) {
        var txt = "Hallo Medialyte, ich habe gerade " + (d.termin ? "einen Termin am " + fmtDate(d.termin.datum, true) + " um " + d.termin.uhrzeit + " Uhr angefragt." : "einen Rückruf angefragt.");
        wa.href = (CFG.whatsapp || "https://wa.me/491709647532") + "?text=" + encodeURIComponent(txt);
      }
      var note = $(".demo-note", root); if (note) note.hidden = !demo;
    }
    function downloadIcs(d) {
      var start = new Date(slotEpoch(d.termin.datum, d.termin.uhrzeit)), end = new Date(start.getTime() + DUR * 60000);
      var f = function (dt) { return dt.toISOString().replace(/[-:]/g, "").replace(/\.\d{3}/, ""); };
      var ics = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Medialyte//Termin//DE", "BEGIN:VEVENT",
        "UID:" + Date.now() + "@medialyte.de", "DTSTAMP:" + f(new Date()), "DTSTART:" + f(start), "DTEND:" + f(end),
        "SUMMARY:Erstgespräch mit Medialyte", "DESCRIPTION:" + d.format_text + " – Medialyte meldet sich zur Bestätigung.",
        "LOCATION:" + (d.format === "vor-ort" ? "Bei Ihnen vor Ort (Adresse stimmen wir vorher ab)" : d.format_text), "END:VEVENT", "END:VCALENDAR"].join("\r\n");
      var a = document.createElement("a");
      a.href = URL.createObjectURL(new Blob([ics], { type: "text/calendar;charset=utf-8" }));
      a.download = "medialyte-termin.ics"; document.body.appendChild(a); a.click(); a.remove();
    }

    /* Sitzung merken */
    function persist() {
      if (step === 5) return;
      var o = { step: step, sel: sel, f: {} };
      $$("input, select, textarea", form).forEach(function (el) {
        if (!el.name || el.name === "ml_zx" || el.name === "einwilligung") return;
        if (el.type === "checkbox" || el.type === "radio") { if (el.checked) (o.f[el.name] = o.f[el.name] || []).push(el.value); }
        else o.f[el.name] = el.value;
      });
      store.set(KEY, o);
    }
    function restore(o) {
      if (!o || !o.f) return;
      Object.keys(o.f).forEach(function (k) {
        var v = o.f[k];
        $$('[name="' + k + '"]', form).forEach(function (el) {
          if (el.type === "checkbox" || el.type === "radio") el.checked = Array.isArray(v) && v.indexOf(el.value) >= 0;
          else el.value = v;
        });
      });
      if (o.sel) sel = { date: o.sel.date || null, time: o.sel.time || null };
      if (sel.date && sel.date < today) sel = { date: null, time: null };
      /* Termin aus der letzten Sitzung: nur behalten, wenn er noch weit genug in der Zukunft liegt */
      if (sel.date && sel.time) { try { if (slotEpoch(sel.date, sel.time) < Date.now() + LEAD * 3600000) sel.time = null; } catch (e) { sel.time = null; } }
      if (cbOnly && cbOnly.checked) { calWrap.hidden = true; cbWrap.hidden = false; }
    }
    if (saved) restore(saved);
    if (qs.get("anliegen")) preselect(qs.get("anliegen").split(","));
    if (qs.get("branche") && form.elements.branche) { form.elements.branche.value = qs.get("branche"); }
    if (qs.get("quelle") === "brief") preselect(["brief"]);
    if (sel.date) month = sel.date.slice(0, 7);
    renderCal();
    go(saved && saved.step > 1 && saved.step < 5 ? saved.step : 1, true);
  }
});
