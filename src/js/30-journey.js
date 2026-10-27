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
    if (jr) jr.addEventListener("ml:station", function (ev) { if (!manual && ev.detail && !ev.detail.pinned && parseFloat(rl.style.getPropertyValue("--p")) < 100) setP(100, false); });
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
    function say(t) { if (msgEl) msgEl.textContent = t; }
    function restore() { board.innerHTML = initial; say(initialMsg); counts(); }
    /* Platz für die längste Agent-Nachricht freihalten, damit beim Wechsel nichts springt
       (gemessen an einer unsichtbaren Kopie in derselben Breite) */
    var agentBox = msgEl ? msgEl.closest(".pl__agent") : null;
    function reserve() {
      if (!agentBox || !agentBox.offsetWidth) return;
      var names = $$(".pl__card b", pl).map(function (b) { return b.textContent; }).concat(["Familie Ahrens"]);
      var longest = names.reduce(function (a, b) { return b.length > a.length ? b : a; }, "");
      var texts = [initialMsg].concat(STEPS.map(function (s) { return s[2]; }));
      Object.keys(SAY).forEach(function (k) { texts.push(SAY[k](longest)); });
      var probe = agentBox.cloneNode(true);
      probe.removeAttribute("aria-live");
      probe.setAttribute("aria-hidden", "true");
      probe.style.cssText = "position:absolute;visibility:hidden;pointer-events:none;left:0;top:0;min-height:0;width:" + agentBox.offsetWidth + "px";
      agentBox.parentNode.appendChild(probe);
      var pm = probe.querySelector("[data-plmsg]"), max = 0;
      texts.forEach(function (t) { pm.textContent = t; max = Math.max(max, probe.offsetHeight); });
      probe.remove();
      agentBox.style.minHeight = max ? max + "px" : "";
    }
    reserve();
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(reserve);
    var rsT = null;
    window.addEventListener("resize", function () { clearTimeout(rsT); rsT = setTimeout(reserve, 150); }, { passive: true });
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
  var info = $(".ms__info", root), k = $(".ms__k", root), vOld = $(".v-old", root), vNew = $(".v-new", root);
  var busy = false, touched = false;
  var tick = '<svg viewBox="0 0 16 11" width="16" height="11" fill="none" stroke="#53BDEB" stroke-width="1.6" aria-hidden="true" style="display:inline-block;vertical-align:-1px;margin-left:3px"><path d="M1 6l3 3 6-7M6 9l1 .8L14 2"/></svg>';
  /* Feste, glaubwürdige Uhrzeiten statt der echten Uhr: jede Nachricht eine Minute später */
  var minute = 9 * 60 + 38;
  function stamp() { var h = Math.floor(minute / 60), m = minute % 60; minute++; return (h < 10 ? "0" : "") + h + ":" + (m < 10 ? "0" : "") + m; }
  function bubble(cls, txt, isMe) {
    var d = document.createElement("div");
    d.className = "cp-msg " + cls + " is-pop";
    d.innerHTML = ML.esc(txt) + "<time>" + stamp() + (isMe ? tick : "") + "</time>";
    body.appendChild(d);
    /* Höchstens drei Blasen, damit die neueste Antwort immer ganz zu sehen ist */
    var all = $$(".cp-msg, .cp-typing", body);
    while (all.length > 3) { all.shift().remove(); }
    return d;
  }
  function updateSite(a) {
    if (!info) return;
    $$(".ms__v > span", info).forEach(function (s) { s.style.transition = "none"; });
    if (info.classList.contains("is-upd")) vOld.textContent = vNew.textContent;
    info.classList.remove("is-upd", "is-flash");
    void info.offsetWidth;
    $$(".ms__v > span", info).forEach(function (s) { s.style.transition = ""; });
    k.textContent = a.k;
    vNew.textContent = a.v;
    void info.offsetWidth;
    info.classList.add("is-upd", "is-flash");
    setTimeout(function () { info.classList.remove("is-flash"); }, 1500);
  }
  function run(a, btn) {
    if (busy) return;
    busy = true;
    btns.forEach(function (b) { b.disabled = true; b.setAttribute("aria-pressed", b === btn ? "true" : "false"); });
    bubble("cp-msg--me", a.me, true);
    var fast = ML.reduce;
    setTimeout(function () {
      var t = document.createElement("div"); t.className = "cp-typing is-pop"; t.innerHTML = "<i></i><i></i><i></i>"; body.appendChild(t);
      var all = $$(".cp-msg, .cp-typing", body); while (all.length > 3) { all.shift().remove(); }
    }, fast ? 0 : 700);
    setTimeout(function () {
      var t = $(".cp-typing", body); if (t) t.remove();
      bubble("cp-msg--agent", a.agent, false);
      updateSite(a);
      if (live) live.textContent = "KI-Agent: " + a.agent + " Website: " + a.k + ", " + a.v + ".";
      busy = false;
      btns.forEach(function (b) { b.disabled = false; });
    }, fast ? 50 : 2100);
  }
  /* Jede Anfrage hat mehrere Varianten – wer erneut klickt, schickt die nächste Änderung */
  var seen = {};
  function next(ask) {
    var vs = ask.variants || [ask], i = seen[ask.id] || 0;
    seen[ask.id] = i + 1;
    return vs[i % vs.length];
  }
  btns.forEach(function (b) {
    b.addEventListener("click", function () {
      if (busy) return;
      touched = true;
      var a = asks.filter(function (x) { return x.id === b.getAttribute("data-ask-id"); })[0];
      if (a) run(next(a), b);
    });
  });
  ML.presentOnce(root, function () {
    setTimeout(function () { if (!touched) run(next(asks[0]), btns[0]); }, 900);
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
