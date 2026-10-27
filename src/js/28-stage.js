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
      sts.forEach(function (s) { if (on) s.setAttribute("role", "tabpanel"); else s.removeAttribute("role"); });
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
    function check() {
      var want = mq.matches && !ML.reduce;
      if (want !== pinned) setMode(want);
      if (fit() < MIN_FIT && pinned) { setMode(false); fit(); }
    }
    if (mq.addEventListener) mq.addEventListener("change", check); else if (mq.addListener) mq.addListener(check);
    var rt = null;
    window.addEventListener("resize", function () { clearTimeout(rt); rt = setTimeout(check, 180); });
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(check);
    check();
  });
});
