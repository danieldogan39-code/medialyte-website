/* Startbereich: Cockpit mit vier Beispiel-Betrieben.
   Ablauf je Betrieb: Anfragen erscheinen, Nachricht an den KI-Agenten, Antwort, Website ändert sich, neue Anfrage kommt rein. */
ML.module("cockpit", function (ML) {
  var $ = ML.$, $$ = ML.$$;
  var root = $("[data-cockpit]");
  var D = ML.json("cockpit-data");
  if (!root || !D) return;
  var chips = $$(".cp-ctl .chip");
  var pauseBtn = $(".cp-pause");
  var feed = $("[data-cp=feed]", root), msgs = $("[data-cp=msgs]", root), kpi = $("[data-cp=kpi]", root);
  var tl = ML.timeline();
  var cur = root.getAttribute("data-branch") || D.order[0];
  var auto = !ML.reduce, paused = false, inView = false, played = false;
  var SCENE = 9200;

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
    return d;
  }
  function site(key) { return $(".ms--" + key, root); }
  function setKpi(v, tick) {
    var a = kpi.children[0], b = kpi.children[1];
    if (!tick) { kpi.classList.remove("is-tick"); a.textContent = v; b.textContent = ""; return; }
    b.textContent = v;
    kpi.classList.add("is-tick");
    setTimeout(function () { kpi.classList.remove("is-tick"); a.style.transition = b.style.transition = "none"; a.textContent = v; b.textContent = "";
      void kpi.offsetWidth; a.style.transition = b.style.transition = ""; }, 700);
  }

  /* Zustand eines Betriebs vorbereiten (vor der Animation) */
  function reset(key) {
    var b = D.b[key];
    root.setAttribute("data-branch", key);
    text("name", "/ " + b.name);
    text("host", b.host);
    text("kpil", b.kpi[0]);
    text("kpid", b.kpi[2]);
    text("ch", b.channel === "wa" ? "KI-Agent · per WhatsApp" : "KI-Agent · im Cockpit");
    text("count", "Heute " + (b.feed.length + 1));
    setKpi(b.kpi[1], false);
    feed.innerHTML = "";
    b.feed.forEach(function (it, i) { var el = feedItem(it, i, false); el.classList.add("is-enter"); feed.appendChild(el); });
    msgs.innerHTML = "";
    var s = site(key);
    if (s) {
      var info = $(".ms__info", s), note = $(".ms__notice", s);
      if (info) info.classList.remove("is-upd", "is-flash");
      if (note) note.classList.remove("is-on");
    }
    chips.forEach(function (c) {
      var on = c.getAttribute("data-branch") === key;
      c.setAttribute("aria-selected", on ? "true" : "false");
      c.tabIndex = on ? 0 : -1;
    });
  }

  /* Endzustand ohne Animation (für reduzierte Bewegung) */
  function finalState(key) {
    reset(key);
    var b = D.b[key];
    feed.innerHTML = "";
    feed.appendChild(feedItem(b["new"], 0, true));
    b.feed.forEach(function (it, i) { feed.appendChild(feedItem(it, i + 1, false)); });
    if (b.channel === "wa") { msg("cp-msg--me", ML.esc(b.me), "09:38"); msg("cp-msg--agent", ML.esc(b.agent), "09:39"); }
    else { msg("cp-msg--task", "<b>" + ML.esc(b.task[0]) + "</b>" + ML.esc(b.agent)); }
    $$(".cp-msg", msgs).forEach(function (m) { m.classList.remove("is-pop"); });
    var s = site(key);
    if (s) { var info = $(".ms__info", s), note = $(".ms__notice", s); if (info) info.classList.add("is-upd"); if (note) note.classList.add("is-on"); }
    setKpi(b.kpi[1] + 1, false);
  }

  function play(key) {
    tl.clear();
    var b = D.b[key];
    cur = key;
    reset(key);
    played = true;
    tl.at(350, function () { $$(".cp-feed__item", feed).forEach(function (el, i) { setTimeout(function () { el.classList.remove("is-enter"); }, i * 120); }); });
    if (b.channel === "wa") {
      tl.at(1300, function () { msg("cp-msg--me", ML.esc(b.me), "09:38"); });
      tl.at(2300, function () { var t = document.createElement("div"); t.className = "cp-typing is-pop"; t.innerHTML = "<i></i><i></i><i></i>"; msgs.appendChild(t); });
      tl.at(3600, function () { var t = $(".cp-typing", msgs); if (t) t.remove(); msg("cp-msg--agent", ML.esc(b.agent), "09:39"); });
    } else {
      var card;
      tl.at(1300, function () { card = msg("cp-msg--task", "<b>" + ML.esc(b.task[0]) + "</b>" + ML.esc(b.task[1]) + '<br><span class="cp-msg__btn">' + D.check + "Veröffentlichen</span>"); });
      tl.at(2900, function () { var btn = $(".cp-msg__btn", card); if (btn) btn.classList.add("is-press"); });
      tl.at(3150, function () { var btn = $(".cp-msg__btn", card); if (btn) { btn.classList.remove("is-press"); btn.classList.add("is-done"); btn.innerHTML = D.check + "Veröffentlicht"; } });
    }
    tl.at(3900, function () {
      var s = site(key); if (!s) return;
      var info = $(".ms__info", s), note = $(".ms__notice", s);
      if (info) { info.classList.add("is-upd", "is-flash"); setTimeout(function () { info.classList.remove("is-flash"); }, 1500); }
      if (note) note.classList.add("is-on");
    });
    tl.at(5100, function () {
      var items = $$(".cp-feed__item", feed);
      items.forEach(function (el) { var s = +el.style.getPropertyValue("--slot") + 1; el.style.setProperty("--slot", s); if (s > 2) el.classList.add("is-leave"); });
      var n = feedItem(b["new"], 0, true); n.classList.add("is-enter"); feed.insertBefore(n, feed.firstChild);
      requestAnimationFrame(function () { requestAnimationFrame(function () { n.classList.remove("is-enter"); }); });
      setTimeout(function () { $$(".is-leave", feed).forEach(function (el) { el.remove(); }); }, 800);
      setKpi(b.kpi[1] + 1, true);
    });
    tl.at(SCENE, function () {
      if (!auto || paused || !inView || document.hidden) return;
      var i = D.order.indexOf(cur);
      play(D.order[(i + 1) % D.order.length]);
    });
  }

  function select(key, user) {
    if (user) { auto = false; }
    if (ML.reduce || paused) { tl.clear(); finalState(key); cur = key; return; }
    play(key);
  }

  chips.forEach(function (c, i) {
    c.addEventListener("click", function () { select(c.getAttribute("data-branch"), true); });
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

  if (ML.reduce) { finalState(cur); return; }
  reset(cur);
  ML.watch(root, function (vis) {
    inView = vis;
    if (vis && !paused) {
      if (!played) play(cur);
      else if (auto) { tl.clear(); tl.at(1800, function () { if (inView && !paused) { var i = D.order.indexOf(cur); play(D.order[(i + 1) % D.order.length]); } }); }
    }
  }, { threshold: 0.25 });
  document.addEventListener("visibilitychange", function () {
    if (!document.hidden && inView && auto && !paused) { tl.clear(); tl.at(1200, function () { play(cur); }); }
  });

  /* Räumliche Neigung: das Cockpit richtet sich beim Scrollen auf (nur große Bildschirme) */
  var wide = window.matchMedia("(min-width: 900px)");
  var copy = document.querySelector(".hero__in");
  ML.onScroll(function (y, vh) {
    if (!wide.matches) {
      if (root.style.transform) root.style.transform = "";
      if (copy && copy.style.transform) { copy.style.transform = ""; copy.style.opacity = ""; }
      return;
    }
    if (y > vh * 1.4) return;
    var p = ML.clamp(y / (vh * 0.62), 0, 1);
    var e = 1 - Math.pow(1 - p, 2);
    root.style.transform = "rotateX(" + (12 * (1 - e)).toFixed(2) + "deg) scale(" + (0.94 + 0.06 * e).toFixed(4) + ")";
    /* Text bleibt etwas zurück und tritt in den Hintergrund – Tiefe beim Scrollen */
    if (copy) {
      var q = ML.clamp(y / (vh * 0.9), 0, 1);
      copy.style.transform = "translate3d(0," + (y * 0.22).toFixed(1) + "px,0)";
      copy.style.opacity = (1 - q * 0.75).toFixed(3);
    }
  });
});
