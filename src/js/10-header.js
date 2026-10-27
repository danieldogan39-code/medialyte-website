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
    function set(open) {
      item.classList.toggle("is-open", open);
      btn.setAttribute("aria-expanded", open ? "true" : "false");
    }
    btn.addEventListener("click", function () { set(!item.classList.contains("is-open")); });
    item.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && item.classList.contains("is-open")) { set(false); btn.focus(); }
    });
    item.addEventListener("focusout", function (e) { if (!item.contains(e.relatedTarget)) set(false); });
    document.addEventListener("click", function (e) { if (!item.contains(e.target)) set(false); });
    item.addEventListener("mouseleave", function () { if (document.activeElement !== btn) set(false); });
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
      $$("#booking, .footer, .closing").forEach(function (el) { io.observe(el); });
    }
  }
});
