/* Vorher/Nachher, Vergleich, Paket-Finder, Ablauf, Laufband, FAQ, Film */
ML.module("before-after", function (ML) {
  ML.$$("[data-ba]").forEach(function (ba) {
    var r = ba.querySelector("input[type=range]");
    if (!r) return;
    var set = function (v) { ba.style.setProperty("--pos", v + "%"); };
    r.addEventListener("input", function () { set(r.value); touched = true; });
    set(r.value);
    var touched = false;
    if (ML.reduce) return;
    /* Kleiner Hinweis, dass man ziehen kann – einmal, wenn der Regler ins Bild kommt */
    ML.onVisible(ba, function () {
      setTimeout(function () {
        if (touched) return;
        var t0 = null, from = 50;
        function step(t) {
          if (touched) return;
          if (!t0) t0 = t;
          var p = Math.min(1, (t - t0) / 1600);
          var v = from + Math.sin(p * Math.PI * 2) * 14 * (1 - p * 0.3);
          if (p >= 1) v = 50;
          r.value = v; set(v.toFixed(2));
          if (p < 1) requestAnimationFrame(step);
        }
        requestAnimationFrame(step);
      }, 500);
    }, { threshold: 0.6 });
  });
});

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

/* Film-Platzhalter: Kapitel laufen als Titelkarten durch; ein Klick in der Liste springt dorthin */
ML.module("film", function (ML) {
  ML.$$("[data-film]").forEach(function (root) {
    var scenes = ML.$$(".film__scene", root), chs = ML.$$(".film__ch", root), bars = ML.$$(".film__bars i", root);
    var cur = 0, timer = null, auto = !ML.reduce, DUR = 4800, inView = false;
    root.style.setProperty("--dur", DUR + "ms");
    function show(i) {
      cur = i;
      scenes.forEach(function (s, j) { s.classList.toggle("is-on", j === i); });
      chs.forEach(function (c, j) { c.classList.toggle("is-on", j === i); c.setAttribute("aria-pressed", j === i ? "true" : "false"); });
      bars.forEach(function (b, j) { b.classList.remove("is-on"); b.classList.toggle("is-done", j < i); if (j === i) { void b.offsetWidth; b.classList.add("is-on"); } });
      schedule();
    }
    function schedule() {
      clearTimeout(timer);
      root.classList.toggle("is-playing", auto && inView);
      if (!auto || !inView) return;
      timer = setTimeout(function () { show((cur + 1) % scenes.length); }, DUR);
    }
    chs.forEach(function (c, i) { c.addEventListener("click", function () { auto = false; show(i); }); });
    ML.watch(root, function (v) { inView = v; if (v) show(cur); else { clearTimeout(timer); root.classList.remove("is-playing"); } }, { threshold: 0.4 });
  });
});
