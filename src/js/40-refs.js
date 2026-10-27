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
