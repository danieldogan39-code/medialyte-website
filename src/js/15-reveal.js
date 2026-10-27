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
