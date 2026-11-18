/* Ratgeber: Themenfilter, Lesefortschritt, aktiver Abschnitt im Inhaltsverzeichnis.
   Ohne Skript bleiben alle Beiträge sichtbar, der Filter erscheint gar nicht. */
ML.module("rfilter", function (ML) {
  var box = ML.$("[data-rfilter]"), grid = ML.$("[data-rgrid]");
  if (!box || !grid) return;
  var btns = ML.$$("[data-th]", box), cards = ML.$$(".rcard", grid), n = ML.$("[data-rcount]");
  box.hidden = false;
  function set(th) {
    grid.setAttribute("data-filter", th);
    var c = 0;
    cards.forEach(function (el) {
      var dup = el.classList.contains("rcard--dup");
      var on = th === "alle" ? !dup : el.getAttribute("data-thema") === th;
      el.classList.toggle("is-out", !on);
      if (on) { c++; el.classList.add("is-in"); }
    });
    btns.forEach(function (b) { b.setAttribute("aria-pressed", b.getAttribute("data-th") === th ? "true" : "false"); });
    if (n) n.textContent = c + (c === 1 ? " Beitrag" : " Beiträge");
  }
  btns.forEach(function (b) { b.addEventListener("click", function () { set(b.getAttribute("data-th")); }); });
});

ML.module("rprogress", function (ML) {
  var art = ML.$("[data-rarticle]"), bar = ML.$(".rprog i");
  if (!art || !bar) return;
  document.documentElement.classList.add("has-rprog");
  var ticking = false;
  function upd() {
    ticking = false;
    var r = art.getBoundingClientRect(), h = r.height - window.innerHeight * 0.6;
    var p = h > 0 ? ML.clamp(-r.top / h, 0, 1) : 1;
    bar.style.transform = "scaleX(" + p.toFixed(4) + ")";
  }
  window.addEventListener("scroll", function () { if (!ticking) { ticking = true; requestAnimationFrame(upd); } }, { passive: true });
  window.addEventListener("resize", upd, { passive: true });
  upd();
});

ML.module("rtoc", function (ML) {
  var toc = ML.$(".legal .prose__toc"), art = ML.$("[data-rarticle]");
  if (!toc || !art || !ML.hasIO) return;
  var links = {}, cur = null;
  ML.$$("a[href^='#']", toc).forEach(function (a) { links[a.getAttribute("href").slice(1)] = a; });
  var heads = ML.$$("h2[id]", art).filter(function (h) { return links[h.id]; });
  if (!heads.length) return;
  function mark(id) {
    if (id === cur) return;
    if (cur && links[cur]) links[cur].classList.remove("is-on");
    cur = id;
    if (links[id]) links[id].classList.add("is-on");
  }
  var io = new IntersectionObserver(function () {
    /* Aktiv ist die letzte Überschrift, die das obere Drittel schon passiert hat */
    var line = window.innerHeight * 0.33, best = heads[0].id;
    heads.forEach(function (h) { if (h.getBoundingClientRect().top < line) best = h.id; });
    mark(best);
  }, { rootMargin: "-20% 0px -60% 0px", threshold: [0, 1] });
  heads.forEach(function (h) { io.observe(h); });
  mark(heads[0].id);
});
