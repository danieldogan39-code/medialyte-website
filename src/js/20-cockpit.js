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
    b.feed.forEach(function (it, i) { var el = feedItem(it, i, false); el.classList.add("is-enter"); feed.appendChild(el); });
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
    tl.at(350, function () { $$(".cp-feed__item", feed).forEach(function (el, i) { setTimeout(function () { el.classList.remove("is-enter"); }, i * 120); }); });
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

  if (ML.reduce) { finalState(cur); return; }
  reset(cur);
  var left = false;
  ML.watch(root, function (vis) {
    inView = vis;
    if (!vis) { if (played) left = true; return; }
    if (paused) return;
    if (!played) { play(cur); return; }
    /* Zurück im Bild: Die Vorführung läuft wieder von selbst weiter – auch nach einem Klick */
    if (left) { left = false; auto = true; }
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
