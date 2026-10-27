/* Weitere Oberflächen auf den Leistungsseiten: Monatsbericht (Online-Marketing) und
   KI-Agent im Dashboard (KI-Agent). Beide starten einmal, sobald sie zu sehen sind. */
ML.module("report", function (ML) {
  ML.$$("[data-report]").forEach(function (rp) {
    var nums = ML.$$("[data-count-to]", rp);
    ML.presentOnce(rp, function () {
      rp.classList.add("is-on");
      if (ML.reduce) return;
      nums.forEach(function (el) {
        var to = +el.getAttribute("data-count-to"), t0 = null;
        function step(t) {
          if (!t0) t0 = t;
          var p = Math.min(1, (t - t0) / 1300), k = 1 - Math.pow(1 - p, 3);
          el.textContent = String(Math.round(to * k));
          if (p < 1) requestAnimationFrame(step);
        }
        el.textContent = "0";
        requestAnimationFrame(step);
      });
    }, { threshold: 0.4 });
  });
});

ML.module("agentdash", function (ML) {
  var $ = ML.$, $$ = ML.$$;
  $$("[data-agentdash]").forEach(function (root) {
    var btn = $("[data-adb-go]", root), list = $("[data-adb-list]", root);
    if (!btn || !list) return;
    var check = btn.querySelector("svg") ? btn.querySelector("svg").outerHTML : "";
    function done(animate) {
      btn.classList.remove("is-press");
      btn.classList.add("is-done");
      btn.innerHTML = check + "<span>Veröffentlicht</span>";
      var rows = $$(".adb__row", list);
      rows.forEach(function (r) {
        var s = +r.style.getPropertyValue("--slot") + 1;
        r.style.setProperty("--slot", s);
        if (s > 2) r.classList.add("is-leave");
      });
      var n = document.createElement("div");
      n.className = "adb__row is-new" + (animate ? " is-enter" : "");
      n.style.setProperty("--slot", 0);
      n.innerHTML = '<span class="adb__ok">' + check + "</span><b>Profil Dr. Sara Yilmaz veröffentlicht</b><time>gerade eben</time>";
      list.insertBefore(n, list.firstChild);
      if (animate) requestAnimationFrame(function () { requestAnimationFrame(function () { n.classList.remove("is-enter"); }); });
      setTimeout(function () { $$(".is-leave", list).forEach(function (r) { r.remove(); }); }, animate ? 800 : 0);
    }
    var finished = false, timers = [];
    function finish(animate) {
      if (finished) return;
      finished = true;
      timers.forEach(clearTimeout);
      btn.disabled = true;
      done(animate);
      var hint = root.querySelector(".adb__hint"); if (hint) hint.textContent = "Ist online – ohne dass jemand etwas programmieren musste.";
    }
    /* Selbst freigeben geht auch */
    btn.addEventListener("click", function () { finish(!ML.reduce); });
    /* Erst zum Klicken einladen; wer nur schaut, sieht nach ein paar Sekunden trotzdem das Ergebnis */
    ML.presentOnce(root, function () {
      if (ML.reduce) { finish(false); return; }
      timers.push(setTimeout(function () { if (!finished) btn.classList.add("is-hint"); }, 900));
      timers.push(setTimeout(function () { if (!finished) { btn.classList.remove("is-hint"); btn.classList.add("is-press"); } }, 6200));
      timers.push(setTimeout(function () { finish(true); }, 6450));
    }, { threshold: 0.45 });
  });
});
