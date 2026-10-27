/* Die Idee: Vermehrung, Verbesserung, Verwaltung – Kreis mit drei Bereichen */
ML.module("idea", function (ML) {
  var $ = ML.$, $$ = ML.$$;
  ML.$$("[data-idea]").forEach(function (root) {
    var tabs = $$(".orb__node", root), panels = $$(".idea__panel", root), arcs = $$(".orb__arc", root), dots = $$(".idea__dots i", root);
    var orb = $(".orb", root);
    var cur = 0, timer = null, auto = !ML.reduce, inView = false, DUR = 7000;
    root.style.setProperty("--dur", DUR + "ms");
    function select(i, focus) {
      cur = i;
      tabs.forEach(function (t, j) { t.setAttribute("aria-selected", i === j ? "true" : "false"); t.tabIndex = i === j ? 0 : -1; });
      panels.forEach(function (p, j) { p.classList.toggle("is-on", i === j); if (i === j) p.removeAttribute("aria-hidden"); else p.setAttribute("aria-hidden", "true"); });
      arcs.forEach(function (a, j) { a.classList.toggle("is-on", i === j); });
      dots.forEach(function (d, j) { d.classList.remove("is-on"); if (i === j) { void d.offsetWidth; d.classList.add("is-on"); } });
      if (focus) tabs[i].focus();
      schedule();
    }
    function schedule() {
      clearTimeout(timer);
      if (!auto || !inView || hold) return;
      timer = setTimeout(function () { if (!document.hidden) select((cur + 1) % tabs.length); else schedule(); }, DUR);
    }
    function manual() { auto = false; clearTimeout(timer); root.classList.add("is-manual"); }
    tabs.forEach(function (t, i) {
      t.addEventListener("click", function () { manual(); select(i); });
      t.addEventListener("keydown", function (e) {
        var n = null;
        if (e.key === "ArrowRight" || e.key === "ArrowDown") n = (i + 1) % tabs.length;
        if (e.key === "ArrowLeft" || e.key === "ArrowUp") n = (i - 1 + tabs.length) % tabs.length;
        if (n === null) return;
        e.preventDefault(); manual(); select(n, true);
      });
    });
    if (ML.reduce) root.classList.add("is-manual");
    /* Beim Lesen nicht weiterschalten: Zeiger oder Fokus im Bereich hält an */
    var hold = false;
    root.addEventListener("mouseenter", function () { hold = true; clearTimeout(timer); root.classList.add("is-hold"); });
    root.addEventListener("mouseleave", function () { hold = false; root.classList.remove("is-hold"); if (auto) select(cur); });
    root.addEventListener("focusin", function () { manual(); });
    ML.watch(root, function (v) {
      inView = v;
      if (orb) orb.classList.toggle("is-paused", !v);
      if (v) { if (auto) select(cur); } else clearTimeout(timer);
    }, { threshold: 0.35 });
  });
});
