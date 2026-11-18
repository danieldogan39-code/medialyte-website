/* Website-Check: misst eine Adresse mit Google PageSpeed Insights (Handy-Ansicht) und zeigt das Ergebnis verständlich.
   Die Anfrage geht erst nach einem Klick auf „Prüfen“ an Google. Nichts wird gespeichert. */
ML.module("wcheck", function (ML) {
  var $ = ML.$, $$ = ML.$$, esc = ML.esc;

  function norm(v) {
    v = String(v || "").trim().replace(/\s+/g, "");
    if (!v) return "";
    if (!/^https?:\/\//i.test(v)) v = "https://" + v;
    try { var u = new URL(v); if (!/\.[a-z]{2,}$/i.test(u.hostname)) return ""; return u.href; } catch (e) { return ""; }
  }
  function bad(input) {
    input.setAttribute("aria-invalid", "true");
    input.focus();
    var f = input.closest("form");
    if (f && !f.querySelector(".wcf__err")) {
      var p = document.createElement("p"); p.className = "wcf__err"; p.textContent = "Bitte geben Sie eine gültige Adresse ein, z. B. ihre-website.de";
      f.appendChild(p);
    }
  }
  /* Startseite und Ratgeber: Formular führt zur Check-Seite (ohne Skript klappt das genauso über GET) */
  $$("[data-wcheck-form]").forEach(function (f) {
    var input = f.querySelector("input");
    input.addEventListener("input", function () { input.removeAttribute("aria-invalid"); var er = f.querySelector(".wcf__err"); if (er) er.remove(); });
    f.addEventListener("submit", function (ev) {
      var u = norm(input.value);
      if (!u) { ev.preventDefault(); bad(input); return; }
      input.value = u.replace(/^https?:\/\//, "").replace(/\/$/, "");
      if (f.hasAttribute("data-wcheck-page")) { ev.preventDefault(); run(u, input); }
    });
  });

  /* Erstgespräch nach dem Check: Website ins Buchungsformular übernehmen */
  try {
    var w = new URLSearchParams(location.search).get("website"), bw = $("#bk-website");
    if (w && bw && !bw.value) { bw.value = w; bw.dispatchEvent(new Event("input", { bubbles: true })); }
  } catch (e) { /* egal */ }

  var box = $("[data-wcheck]");
  if (!box) return;
  var pageForm = $("[data-wcheck-page]"), pageInput = pageForm && pageForm.querySelector("input");

  var busy = false, stepT = null;
  var STEPS = ["Ihre Website wird geladen …", "Ladezeit wird gemessen …", "Darstellung auf dem Handy wird geprüft …", "Google-Grundlagen werden geprüft …", "Barrierefreiheit wird geprüft …", "Ergebnis wird zusammengestellt …"];
  function show(state) {
    $("[data-wc-load]", box).hidden = state !== "load";
    $("[data-wc-err]", box).hidden = state !== "err";
    $("[data-wc-done]", box).hidden = state !== "done";
  }
  function fail(t, p) {
    $("[data-wc-errt]", box).textContent = t;
    $("[data-wc-errp]", box).textContent = p;
    show("err");
  }
  function run(url, input) {
    if (busy) return;
    busy = true;
    var btn = pageForm.querySelector("button");
    btn.disabled = true; btn.textContent = "Prüft …";
    box.hidden = false; show("load");
    var si = 0, step = $("[data-wc-step]", box);
    step.textContent = STEPS[0];
    clearInterval(stepT);
    stepT = setInterval(function () { si = Math.min(si + 1, STEPS.length - 1); step.textContent = STEPS[si]; }, 6000);
    box.scrollIntoView({ behavior: ML.reduce ? "auto" : "smooth", block: "start" });
    var q = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=" + encodeURIComponent(url) +
      "&strategy=mobile&locale=de&category=PERFORMANCE&category=ACCESSIBILITY&category=BEST_PRACTICES&category=SEO" +
      (ML.cfg.psiKey ? "&key=" + encodeURIComponent(ML.cfg.psiKey) : "");
    var ctrl = window.AbortController ? new AbortController() : null;
    var to = setTimeout(function () { if (ctrl) ctrl.abort(); }, 100000);
    fetch(q, ctrl ? { signal: ctrl.signal } : {}).then(function (r) {
      return r.json().then(function (j) { return { ok: r.ok, status: r.status, j: j }; });
    }).then(function (res) {
      if (!res.ok) {
        if (res.status === 429) return fail("Gerade sind sehr viele Prüfungen unterwegs.", "Bitte versuchen Sie es in ein paar Minuten noch einmal – oder wir prüfen Ihre Website gern persönlich.");
        return fail("Die Seite ließ sich nicht prüfen.", "Stimmt die Adresse? Manche Websites blockieren automatische Prüfungen. Gern schauen wir uns Ihre Seite persönlich an.");
      }
      var lr = res.j.lighthouseResult;
      if (!lr || (lr.runtimeError && lr.runtimeError.code && lr.runtimeError.code !== "NO_ERROR"))
        return fail("Die Seite ließ sich nicht laden.", "Stimmt die Adresse? Ist die Website gerade erreichbar? Gern prüfen wir sie auch persönlich.");
      render(lr, res.j.loadingExperience, url);
    }).catch(function () {
      fail("Die Prüfung hat zu lange gedauert.", "Bitte versuchen Sie es gleich noch einmal – oder wir prüfen Ihre Website persönlich.");
    }).then(function () {
      clearTimeout(to); clearInterval(stepT);
      busy = false; btn.disabled = false; btn.textContent = "Prüfen";
    });
  }

  /* Mit ?url= von der Startseite gekommen: direkt prüfen */
  var start = null;
  try { start = new URLSearchParams(location.search).get("url"); } catch (e) { start = null; }
  if (start && pageInput) {
    var su = norm(start);
    if (su) { pageInput.value = su.replace(/^https?:\/\//, "").replace(/\/$/, ""); run(su, pageInput); }
  }

  function tone(s) { return s >= 90 ? "ok" : s >= 50 ? "mid" : "bad"; }
  function clean(t) { return String(t || "").replace(/\[([^\]]+)\]\([^)]+\)/g, "$1").replace(/`/g, ""); }
  function ring(label, s) {
    var c = 2 * Math.PI * 30, off = c * (1 - s / 100);
    return '<li class="wcs wcs--' + tone(s) + '"><svg viewBox="0 0 72 72" aria-hidden="true"><circle class="wcs__bg" cx="36" cy="36" r="30"/>' +
      '<circle class="wcs__fg" cx="36" cy="36" r="30" stroke-dasharray="' + c.toFixed(1) + '" stroke-dashoffset="' + off.toFixed(1) + '"/></svg>' +
      '<b>' + s + '</b><span>' + esc(label) + "</span></li>";
  }
  function render(lr, field, url) {
    var cats = lr.categories || {}, A = lr.audits || {};
    var names = [["performance", "Ladezeit"], ["accessibility", "Barrierefreiheit"], ["best-practices", "Technik"], ["seo", "Google-Grundlagen"]];
    var scores = names.map(function (n) { var c = cats[n[0]]; return c && c.score != null ? Math.round(c.score * 100) : null; });
    var valid = scores.filter(function (s) { return s != null; });
    var avg = valid.length ? valid.reduce(function (a, b) { return a + b; }, 0) / valid.length : 0;
    $("[data-wc-host]", box).textContent = (function () { try { return new URL(lr.finalDisplayedUrl || lr.finalUrl || url).hostname.replace(/^www\./, ""); } catch (e) { return url; } })();
    $("[data-wc-verdict]", box).textContent = avg >= 90 ? "Stark – technisch ist Ihre Website gut aufgestellt." : avg >= 75 ? "Solide, mit Luft nach oben." : avg >= 50 ? "Hier verschenkt Ihre Website Potenzial." : "Hier besteht dringender Handlungsbedarf.";
    $("[data-wc-scores]", box).innerHTML = names.map(function (n, i) { return scores[i] == null ? "" : ring(n[1], scores[i]); }).join("");

    /* Messwerte: echte Besuche (Google-Daten), sonst Testmessung */
    var fm = field && field.metrics, vit = [];
    function row(name, val, okv, unit, good, note) {
      var st = good ? "ok" : "bad";
      vit.push('<li class="is-' + st + '"><span>' + esc(name) + '<small>' + esc(note) + '</small></span><b>' + esc(val + unit) + '</b><i>' + (good ? "gut" : "zu langsam") + "</i></li>");
    }
    if (fm && fm.LARGEST_CONTENTFUL_PAINT_MS) {
      $("[data-wc-src]", box).textContent = "Gemessen an echten Besuchen der letzten 28 Tage (Daten von Google).";
      var l = fm.LARGEST_CONTENTFUL_PAINT_MS.percentile / 1000;
      row("Ladezeit (LCP)", l.toFixed(1).replace(".", ","), 2.5, " s", l <= 2.5, "gut: bis 2,5 s");
      if (fm.INTERACTION_TO_NEXT_PAINT) { var n = fm.INTERACTION_TO_NEXT_PAINT.percentile; row("Reaktion (INP)", n, 200, " ms", n <= 200, "gut: bis 200 ms"); }
      if (fm.CUMULATIVE_LAYOUT_SHIFT_SCORE) { var s = fm.CUMULATIVE_LAYOUT_SHIFT_SCORE.percentile / 100; row("Stabilität (CLS)", s.toFixed(2).replace(".", ","), 0.1, "", s <= 0.1, "gut: bis 0,1"); }
    } else {
      $("[data-wc-src]", box).textContent = "Testmessung in der Handy-Ansicht – für Ihre Seite liegen noch keine Daten echter Besuche vor.";
      var lcp = A["largest-contentful-paint"], cls = A["cumulative-layout-shift"], tbt = A["total-blocking-time"];
      if (lcp) { var lv = lcp.numericValue / 1000; row("Ladezeit (LCP)", lv.toFixed(1).replace(".", ","), 2.5, " s", lv <= 2.5, "gut: bis 2,5 s"); }
      if (tbt) { var tv = Math.round(tbt.numericValue); row("Blockierzeit (TBT)", tv, 200, " ms", tv <= 200, "gut: bis 200 ms"); }
      if (cls) { var cv = cls.numericValue; row("Stabilität (CLS)", cv.toFixed(2).replace(".", ","), 0.1, "", cv <= 0.1, "gut: bis 0,1"); }
    }
    $("[data-wc-vitals]", box).innerHTML = vit.join("");

    /* Grundlagen: einfache Ja/Nein-Punkte */
    var basics = [["is-on-https", "Verschlüsselt (HTTPS)", "Nicht verschlüsselt (kein HTTPS)"], ["viewport", "Für das Handy eingerichtet", "Nicht für das Handy eingerichtet"],
                  ["document-title", "Seitentitel vorhanden", "Seitentitel fehlt"], ["meta-description", "Beschreibung für Google vorhanden", "Beschreibung für Google fehlt"],
                  ["image-alt", "Bilder mit Alternativtext", "Bildern fehlt der Alternativtext"], ["color-contrast", "Ausreichende Kontraste", "Kontraste zu schwach"]];
    $("[data-wc-basics]", box).innerHTML = basics.filter(function (b) { return A[b[0]] && A[b[0]].score != null; }).map(function (b) {
      var ok = A[b[0]].score >= 0.9;
      return '<li class="is-' + (ok ? "ok" : "bad") + '"><span class="wcb__ic" aria-hidden="true">' + (ok ? "✓" : "!") + "</span>" + esc(ok ? b[1] : b[2]) + "</li>";
    }).join("");

    /* Die größten Bremsen: nicht bestandene Prüfungen, nach Gewicht sortiert */
    var found = [], seen = {};
    names.forEach(function (n) {
      var c = cats[n[0]]; if (!c) return;
      (c.auditRefs || []).forEach(function (ref) {
        var a = A[ref.id];
        if (!a || seen[ref.id] || a.score == null || a.score >= 0.9 || a.scoreDisplayMode === "informative" || a.scoreDisplayMode === "numeric" || a.scoreDisplayMode === "manual" || a.scoreDisplayMode === "notApplicable") return;
        seen[ref.id] = 1;
        var w = (ref.weight || 0) + (a.details && a.details.overallSavingsMs ? Math.min(10, a.details.overallSavingsMs / 300) : 0);
        found.push({ t: clean(a.title), w: w * (1 - a.score), cat: n[1] });
      });
    });
    found.sort(function (x, y) { return y.w - x.w; });
    var top = found.slice(0, 5);
    $("[data-wc-findbox]", box).hidden = !top.length;
    $("[data-wc-find]", box).innerHTML = top.map(function (f) { return "<li><span>" + esc(f.t) + "</span><small>" + esc(f.cat) + "</small></li>"; }).join("");

    var bk = $("[data-wc-book]", box);
    if (bk) { var h = bk.getAttribute("href").split("&website=")[0]; bk.setAttribute("href", h + "&website=" + encodeURIComponent(url.replace(/^https?:\/\//, "").replace(/\/$/, ""))); }
    show("done");
  }
});
