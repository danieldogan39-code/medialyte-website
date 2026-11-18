/* Website-Check: misst eine Adresse mit Google PageSpeed Insights und zeigt das Ergebnis verständlich.
   Die Anfrage geht erst nach einem Klick auf „Website prüfen“ an Google. Nichts wird gespeichert.
   Handy-Ansicht zuerst; die Computer-Ansicht wird erst gemessen, wenn sie jemand anklickt. */
ML.module("wcheck", function (ML) {
  var $ = ML.$, $$ = ML.$$, esc = ML.esc;

  function norm(v) {
    v = String(v || "").trim().replace(/\s+/g, "");
    if (!v) return "";
    if (!/^https?:\/\//i.test(v)) v = "https://" + v;
    try { var u = new URL(v); if (!/\.[a-z]{2,}$/i.test(u.hostname)) return ""; return u.href; } catch (e) { return ""; }
  }
  function short(u) { return String(u).replace(/^https?:\/\//, "").replace(/\/$/, ""); }
  function host(u) { try { return new URL(u).hostname.replace(/^www\./, ""); } catch (e) { return short(u); } }
  function bad(input) {
    input.setAttribute("aria-invalid", "true");
    input.focus();
    var f = input.closest("form");
    if (f && !f.querySelector(".wcf__err")) {
      var p = document.createElement("p"); p.className = "wcf__err"; p.setAttribute("role", "alert");
      p.textContent = "Bitte geben Sie eine gültige Adresse ein, z. B. ihre-website.de";
      f.appendChild(p);
    }
  }
  $$("[data-wcheck-form]").forEach(function (f) {
    var input = f.querySelector("input");
    input.addEventListener("input", function () { input.removeAttribute("aria-invalid"); var er = f.querySelector(".wcf__err"); if (er) er.remove(); });
    f.addEventListener("submit", function (ev) {
      var u = norm(input.value);
      if (!u) { ev.preventDefault(); bad(input); return; }
      input.value = short(u);
      if (f.hasAttribute("data-wcheck-page")) { ev.preventDefault(); start(u); }
    });
  });

  /* Erstgespräch nach dem Check: Website ins Buchungsformular übernehmen */
  try {
    var w = new URLSearchParams(location.search).get("website"), bw = $("#bk-website");
    if (w && bw && !bw.value) { bw.value = w; bw.dispatchEvent(new Event("input", { bubbles: true })); }
  } catch (e) { /* egal */ }

  var box = $("[data-wcheck]");
  if (!box) return;
  var form = $("[data-wcheck-page]"), input = form.querySelector("input"), btn = form.querySelector("button");
  var stage = $("[data-wst]"), cache = {}, cur = { url: "", view: "mobile" }, busy = false, tick = null;

  function show(s) {
    $("[data-wc-load]", box).hidden = s !== "load";
    $("[data-wc-err]", box).hidden = s !== "err";
    $("[data-wc-done]", box).hidden = s !== "done";
  }
  function fail(t, p) {
    $("[data-wc-errt]", box).textContent = t;
    $("[data-wc-errp]", box).textContent = p;
    show("err");
  }
  /* Fortschritt ist echt: jeder Prüfbereich läuft als eigene Messung, sein Schritt wird abgehakt, sobald Google ihn liefert */
  var PARTS = [["PERFORMANCE", "performance"], ["ACCESSIBILITY", "accessibility"], ["BEST_PRACTICES", "best-practices"], ["SEO", "seo"]];
  var t0 = 0, doneN = 0;
  function loading(on, url) {
    if (stage) stage.classList.toggle("is-scan", on);
    var prog = $("[data-wc-prog]", box), tm = $("[data-wc-timer]", box);
    clearInterval(tick);
    if (!on) return;
    $("[data-wc-runhost]", box).textContent = host(url) + (cur.view === "desktop" ? " (Computer)" : "");
    t0 = Date.now(); doneN = 0;
    $$("[data-wc-steps] li", box).forEach(function (li) { li.className = li.hasAttribute("data-part") ? "is-on" : ""; li.removeAttribute("data-t"); });
    function upd() {
      var s = (Date.now() - t0) / 1000;
      tm.textContent = Math.floor(s) + " s";
      /* Balken: fertige Bereiche zählen voll, der laufende Anteil wächst langsam, erreicht aber nie den nächsten Abschnitt */
      var base = doneN / PARTS.length, slice = 1 / PARTS.length, creep = doneN < PARTS.length ? slice * 0.85 * (1 - Math.exp(-s / 12)) : 0;
      prog.style.transform = "scaleX(" + Math.min(0.97, 0.03 + (base + creep) * 0.94).toFixed(3) + ")";
    }
    upd(); tick = setInterval(upd, 200);
  }
  function stepDone(cat, ok) {
    var li = $('[data-wc-steps] li[data-part="' + cat + '"]', box);
    if (!li) return;
    doneN++;
    li.className = ok ? "is-done" : "is-fail";
    li.setAttribute("data-t", Math.round((Date.now() - t0) / 1000) + " s");
    if (doneN === PARTS.length) { var last = $("[data-wc-steps] li[data-final]", box); if (last) last.className = "is-on"; }
  }

  function start(url) {
    cur.url = url; cur.view = "mobile"; cache = {};
    try { history.replaceState(null, "", location.pathname + "?url=" + encodeURIComponent(short(url))); } catch (e) { /* egal */ }
    var g = $("[data-wc-google]", box);
    if (g) g.setAttribute("href", "https://pagespeed.web.dev/analysis?url=" + encodeURIComponent(url) + "&form_factor=mobile");
    var sh = stage && stage.querySelector("[data-wst-host]"); if (sh) sh.textContent = host(url);
    measure(url, "mobile");
  }

  function one(url, view, part) {
    var q = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=" + encodeURIComponent(url) +
      "&strategy=" + view + "&locale=de&category=" + part[0] + (ML.cfg.psiKey ? "&key=" + encodeURIComponent(ML.cfg.psiKey) : "");
    var ctrl = window.AbortController ? new AbortController() : null;
    var to = setTimeout(function () { if (ctrl) ctrl.abort(); }, 110000);
    return fetch(q, ctrl ? { signal: ctrl.signal } : {}).then(function (r) {
      return r.json().then(function (j) { return { ok: r.ok, status: r.status, j: j }; });
    }, function () { return { ok: false, status: 0, j: {} }; }).then(function (res) {
      clearTimeout(to);
      var lr = res.ok && res.j.lighthouseResult;
      var good = !!(lr && !(lr.runtimeError && lr.runtimeError.code && lr.runtimeError.code !== "NO_ERROR") && lr.categories && lr.categories[part[1]]);
      stepDone(part[1], good);
      return { part: part[1], ok: good, status: res.status, j: res.j, lr: lr };
    });
  }

  function measure(url, view) {
    if (busy) return;
    if (cache[view]) { render(cache[view], view); return; }
    busy = true; cur.view = view;
    btn.disabled = true; btn.querySelector("span").textContent = "Prüft …";
    box.hidden = false; show("load"); loading(true, url);
    box.scrollIntoView({ behavior: ML.reduce ? "auto" : "smooth", block: "start" });
    Promise.all(PARTS.map(function (p) { return one(url, view, p); })).then(function (rs) {
      var perf = rs[0];
      if (!perf.ok) {
        if (rs.some(function (r) { return r.status === 429; })) return fail("Gerade sind sehr viele Prüfungen unterwegs.", "Bitte versuchen Sie es in ein paar Minuten noch einmal – oder wir prüfen Ihre Website gern persönlich.");
        if (rs.every(function (r) { return r.status === 0; })) return fail("Die Prüfung hat zu lange gedauert.", "Bitte versuchen Sie es gleich noch einmal – oder wir prüfen Ihre Website persönlich.");
        return fail("Die Seite ließ sich nicht prüfen.", "Stimmt die Adresse? Ist die Website erreichbar? Manche Websites blockieren automatische Prüfungen. Gern schauen wir uns Ihre Seite persönlich an.");
      }
      /* Ergebnisse der vier Messungen zusammenführen */
      var lr = { finalDisplayedUrl: perf.lr.finalDisplayedUrl, finalUrl: perf.lr.finalUrl, categories: {}, audits: {} };
      rs.forEach(function (r) { if (!r.ok) return; Object.assign(lr.audits, r.lr.audits); lr.categories[r.part] = r.lr.categories[r.part]; });
      Object.assign(lr.audits, perf.lr.audits); /* Messwerte und Bilder immer aus der Ladezeit-Messung */
      cache[view] = { lr: lr, field: perf.j.loadingExperience, url: url };
      var last = $("[data-wc-steps] li[data-final]", box);
      if (last) last.className = "is-done";
      $("[data-wc-prog]", box).style.transform = "scaleX(1)";
      /* kurz zeigen, dass alles fertig ist, dann das Ergebnis */
      return new Promise(function (ok) { setTimeout(ok, ML.reduce ? 0 : 450); }).then(function () { render(cache[view], view); });
    }).catch(function () {
      fail("Die Prüfung hat nicht geklappt.", "Bitte versuchen Sie es gleich noch einmal – oder wir prüfen Ihre Website persönlich.");
    }).then(function () {
      loading(false);
      busy = false; btn.disabled = false; btn.querySelector("span").textContent = "Website prüfen";
    });
  }

  /* Ansicht wechseln, Link kopieren, neu prüfen */
  $$("[data-wc-view]", box).forEach(function (b) {
    b.addEventListener("click", function () {
      var v = b.getAttribute("data-wc-view");
      if (v === cur.view && cache[v]) return;
      measure(cur.url, v);
    });
  });
  var cp = $("[data-wc-copy]", box);
  if (cp) cp.addEventListener("click", function () {
    var link = location.origin + location.pathname + "?url=" + encodeURIComponent(short(cur.url)), sp = cp.querySelector("span");
    function done(t) { sp.textContent = t; setTimeout(function () { sp.textContent = "Link kopieren"; }, 2200); }
    if (navigator.clipboard) navigator.clipboard.writeText(link).then(function () { done("Kopiert"); }, function () { done("Nicht möglich"); });
    else done("Nicht möglich");
  });
  var ag = $("[data-wc-again]", box);
  if (ag) ag.addEventListener("click", function () {
    window.scrollTo({ top: 0, behavior: ML.reduce ? "auto" : "smooth" });
    input.value = ""; setTimeout(function () { input.focus({ preventScroll: true }); }, ML.reduce ? 0 : 450);
  });

  /* ---------------- Auswertung ---------------- */
  var CAT = [
    ["performance", "Ladezeit", "Wie schnell Ihre Seite lädt und auf Eingaben reagiert.", "zap"],
    ["accessibility", "Barrierefreiheit", "Ob alle Menschen Ihre Seite gut nutzen können.", "eye"],
    ["best-practices", "Technik", "Sicherheit und moderne Technik nach aktuellem Standard.", "shield"],
    ["seo", "Google-Grundlagen", "Ob Google Ihre Seite gut lesen und anzeigen kann.", "search"]];
  /* Grenzwerte nach Google: gut bis …, schlecht ab … */
  var MET = {
    lcp: ["Ladezeit (LCP)", "Größter Inhalt sichtbar", 2500, 4000, "ms"],
    fcp: ["Erster Inhalt (FCP)", "Erstes Element sichtbar", 1800, 3000, "ms"],
    inp: ["Reaktion (INP)", "Reaktion auf Tippen und Klicken", 200, 500, "ms"],
    tbt: ["Blockierzeit (TBT)", "Zeit, in der die Seite nicht reagiert", 200, 600, "ms"],
    cls: ["Stabilität (CLS)", "Wie stark Inhalte verrutschen", 0.1, 0.25, ""],
    si: ["Aufbau (Speed Index)", "Wie schnell die Seite sichtbar wird", 3400, 5800, "ms"]};
  var BASICS = [
    ["is-on-https", "Verschlüsselt (HTTPS)", "Nicht verschlüsselt (kein HTTPS)"],
    ["viewport", "Für das Handy eingerichtet", "Nicht für das Handy eingerichtet"],
    ["document-title", "Seitentitel vorhanden", "Seitentitel fehlt"],
    ["meta-description", "Beschreibung für Google vorhanden", "Beschreibung für Google fehlt"],
    ["is-crawlable", "Google darf die Seite aufnehmen", "Seite ist für Google gesperrt"],
    ["http-status-code", "Seite antwortet fehlerfrei", "Seite antwortet mit Fehler"],
    ["html-has-lang", "Sprache der Seite angegeben", "Sprache der Seite fehlt"],
    ["link-text", "Aussagekräftige Linktexte", "Linktexte wie „hier klicken“"],
    ["image-alt", "Bilder mit Alternativtext", "Bildern fehlt der Alternativtext"],
    ["color-contrast", "Ausreichende Kontraste", "Kontraste zu schwach"]];

  function tone(s) { return s >= 90 ? "ok" : s >= 50 ? "mid" : "bad"; }
  function clean(t) {
    return String(t || "").replace(/\[([^\]]+)\]\([^)]+\)/g, "$1").replace(/`/g, "")
      .replace(/\s*((Weitere )?Informationen (zu|zum|zur|über|dazu)|Weitere Informationen|Mehr erfahren|Learn more)[^.]*\.?\s*$/i, "").trim();
  }
  function fmt(v, unit) {
    if (unit === "ms") return v >= 1000 ? (v / 1000).toFixed(1).replace(".", ",") + " s" : Math.round(v) + " ms";
    return v.toFixed(2).replace(".", ",");
  }
  function ring(s, r) {
    var c = 2 * Math.PI * r;
    return 'stroke-dasharray="' + c.toFixed(1) + '" stroke-dashoffset="' + (c * (1 - s / 100)).toFixed(1) + '"';
  }
  function svgRing(s) {
    return '<svg viewBox="0 0 72 72" aria-hidden="true"><circle class="wring__bg" cx="36" cy="36" r="30"/><circle class="wring__fg" cx="36" cy="36" r="30" ' + ring(s, 30) + "/></svg>";
  }

  function render(d, view) {
    var lr = d.lr, A = lr.audits || {}, cats = lr.categories || {};
    cur.view = view;
    $$("[data-wc-view]", box).forEach(function (b) { b.setAttribute("aria-pressed", b.getAttribute("data-wc-view") === view ? "true" : "false"); });
    $("[data-wc-host]", box).textContent = host(lr.finalDisplayedUrl || lr.finalUrl || d.url);

    /* Gesamtwert: Ladezeit zählt doppelt, weil sie am stärksten über Anfragen entscheidet */
    var sc = {}, sum = 0, wsum = 0;
    CAT.forEach(function (c) { var x = cats[c[0]]; if (x && x.score != null) { sc[c[0]] = Math.round(x.score * 100); var w = c[0] === "performance" ? 2 : 1; sum += sc[c[0]] * w; wsum += w; } });
    var total = wsum ? Math.round(sum / wsum) : 0, t = tone(total);
    var g = $("[data-wc-grade]", box);
    g.className = "wgrade wgrade--" + t;
    g.querySelector(".wgrade__fg").setAttribute("stroke-dasharray", (2 * Math.PI * 52).toFixed(1));
    g.querySelector(".wgrade__fg").setAttribute("stroke-dashoffset", (2 * Math.PI * 52 * (1 - total / 100)).toFixed(1));
    $("[data-wc-total]", box).textContent = total;
    $("[data-wc-label]", box).innerHTML = '<span class="wsum__grade">' + (total >= 90 ? "Sehr gut" : total >= 75 ? "Gut" : total >= 50 ? "Ausbaufähig" : "Kritisch") + "</span><span>" + (view === "desktop" ? "Computer-Ansicht" : "Handy-Ansicht") + "</span>";
    $("[data-wc-verdict]", box).textContent = total >= 90 ? "Stark – technisch ist Ihre Website gut aufgestellt." : total >= 75 ? "Solide, mit Luft nach oben." : total >= 50 ? "Hier verschenkt Ihre Website Potenzial." : "Hier besteht dringender Handlungsbedarf.";
    var weakest = CAT.filter(function (c) { return sc[c[0]] != null; }).sort(function (a, b) { return sc[a[0]] - sc[b[0]]; })[0];
    $("[data-wc-explain]", box).textContent = total >= 90
      ? "Ihre Seite erfüllt die wichtigsten technischen Anforderungen. Ob sie auch überzeugt und Anfragen bringt, entscheiden Inhalt, Aufbau und der nächste Schritt für Ihre Besucher."
      : "Am meisten Potenzial liegt im Bereich „" + weakest[1] + "“. Unten sehen Sie, was konkret bremst – sortiert nach Wirkung.";

    /* Bildschirmfoto aus der Messung */
    var shot = A["final-screenshot"] && A["final-screenshot"].details && A["final-screenshot"].details.data;
    $("[data-wc-shotbox]", box).hidden = !shot;
    $("[data-wc-frame]", box).className = "wshot__frame wshot__frame--" + view;
    if (shot) $("[data-wc-shot]", box).src = shot;
    $("[data-wc-shotcap]", box).textContent = view === "desktop" ? "So sah Ihre Seite am Computer aus" : "So sah Ihre Seite auf dem Handy aus";

    /* Kategorien */
    $("[data-wc-cats]", box).innerHTML = CAT.map(function (c) {
      var s = sc[c[0]]; if (s == null) return "";
      return '<li class="wcat wcat--' + tone(s) + '"><div class="wcat__ring">' + svgRing(s) + '<b class="tnum">' + s + "</b></div>" +
        '<div class="wcat__txt"><h3>' + esc(c[1]) + "</h3><p>" + esc(c[2]) + "</p></div></li>";
    }).join("");

    /* Filmstreifen */
    var th = A["screenshot-thumbnails"] && A["screenshot-thumbnails"].details && A["screenshot-thumbnails"].details.items;
    var fb = $("[data-wc-filmbox]", box);
    fb.hidden = !(th && th.length);
    if (th && th.length) {
      var pick = th.length > 8 ? th.filter(function (x, i) { return i % Math.ceil(th.length / 8) === 0 || i === th.length - 1; }) : th;
      $("[data-wc-film]", box).innerHTML = pick.map(function (x) {
        return '<li><div class="wfilm__img wfilm__img--' + view + '"><img src="' + x.data + '" alt="" loading="lazy" decoding="async"></div><span class="tnum">' + fmt(x.timing, "ms") + "</span></li>";
      }).join("");
    }

    /* Messwerte: echte Besuche, wenn vorhanden, sonst Testmessung */
    var fm = d.field && d.field.metrics, rows = [], useField = !!(fm && fm.LARGEST_CONTENTFUL_PAINT_MS && view === "mobile");
    function add(key, v) { if (v != null && isFinite(v)) rows.push([key, v]); }
    if (useField) {
      add("lcp", fm.LARGEST_CONTENTFUL_PAINT_MS.percentile);
      if (fm.INTERACTION_TO_NEXT_PAINT) add("inp", fm.INTERACTION_TO_NEXT_PAINT.percentile);
      if (fm.CUMULATIVE_LAYOUT_SHIFT_SCORE) add("cls", fm.CUMULATIVE_LAYOUT_SHIFT_SCORE.percentile / 100);
      if (fm.FIRST_CONTENTFUL_PAINT_MS) add("fcp", fm.FIRST_CONTENTFUL_PAINT_MS.percentile);
    } else {
      var nv = function (id) { return A[id] && A[id].numericValue; };
      add("lcp", nv("largest-contentful-paint")); add("fcp", nv("first-contentful-paint"));
      add("tbt", nv("total-blocking-time")); add("cls", nv("cumulative-layout-shift")); add("si", nv("speed-index"));
    }
    $("[data-wc-vsrc]", box).textContent = useField ? "Echte Besuche der letzten 28 Tage (Daten von Google)" : "Testmessung – für diese Seite liegen keine Daten echter Besuche vor";
    $("[data-wc-metrics]", box).innerHTML = rows.map(function (r) {
      var m = MET[r[0]], v = r[1], st = v <= m[2] ? "ok" : v <= m[3] ? "mid" : "bad";
      var max = m[3] * 1.6, pos = Math.min(100, (v / max) * 100), g1 = (m[2] / max) * 100, g2 = (m[3] / max) * 100;
      return '<li class="wm wm--' + st + '"><div class="wm__top"><span><b>' + esc(m[0]) + "</b><small>" + esc(m[1]) + '</small></span><span class="wm__v tnum">' + fmt(v, m[4]) + "</span></div>" +
        '<div class="wm__bar" style="--g1:' + g1.toFixed(1) + "%;--g2:" + g2.toFixed(1) + '%"><i style="left:' + pos.toFixed(1) + '%"></i></div>' +
        '<div class="wm__leg"><span>gut bis ' + fmt(m[2], m[4]) + "</span><em>" + (st === "ok" ? "gut" : st === "mid" ? "verbesserungswürdig" : "zu langsam") + "</em></div></li>";
    }).join("");

    /* Grundlagen */
    $("[data-wc-basics]", box).innerHTML = BASICS.filter(function (b) { return A[b[0]] && A[b[0]].score != null; }).map(function (b) {
      var ok = A[b[0]].score >= 0.9;
      return '<li class="is-' + (ok ? "ok" : "bad") + '"><span class="wbasic__ic" aria-hidden="true">' + (ok ? "✓" : "!") + "</span><span>" + esc(ok ? b[1] : b[2]) + "</span></li>";
    }).join("");

    /* Empfehlungen: nicht bestandene Prüfungen nach Wirkung */
    var found = [], seen = {};
    CAT.forEach(function (c) {
      var x = cats[c[0]]; if (!x) return;
      (x.auditRefs || []).forEach(function (ref) {
        var a = A[ref.id], mode = a && a.scoreDisplayMode;
        if (!a || seen[ref.id] || a.score == null || a.score >= 0.9 || mode === "informative" || mode === "manual" || mode === "notApplicable" || mode === "numeric") return;
        seen[ref.id] = 1;
        var ms = a.details && a.details.overallSavingsMs ? a.details.overallSavingsMs : (a.metricSavings && a.metricSavings.LCP) || 0;
        found.push({ t: clean(a.title), d: clean(a.description), ms: ms, cat: c[1], w: ((ref.weight || 0) + Math.min(10, ms / 300)) * (1 - a.score) + (c[0] === "performance" ? 0.5 : 0) });
      });
    });
    found.sort(function (x, y) { return y.w - x.w; });
    var top = found.slice(0, 6);
    $("[data-wc-findbox]", box).hidden = !top.length;
    $("[data-wc-findt]", box).textContent = total >= 90 ? "Was sich noch verbessern lässt" : "Das bremst Ihre Website am meisten";
    $("[data-wc-find]", box).innerHTML = top.map(function (f, i) {
      var sv = f.ms >= 100 ? '<span class="wfind__save">spart ca. ' + fmt(f.ms, "ms") + "</span>" : "";
      return '<li><details' + (i === 0 ? " open" : "") + '><summary><span class="wfind__n">' + (i + 1) + '</span><span class="wfind__t">' + esc(f.t) + "</span>" + sv +
        '<span class="wfind__cat">' + esc(f.cat) + '</span><span class="qa__ic" aria-hidden="true"></span></summary><p>' + esc(f.d) + "</p></details></li>";
    }).join("");

    var bk = $("[data-wc-book]", box);
    if (bk) { var h = bk.getAttribute("href").split("&website=")[0]; bk.setAttribute("href", h + "&website=" + encodeURIComponent(short(d.url))); }
    show("done");
  }

  /* Mit ?url= gekommen (z. B. von der Startseite): direkt prüfen */
  var q0 = null;
  try { q0 = new URLSearchParams(location.search).get("url"); } catch (e) { q0 = null; }
  if (q0) { var u0 = norm(q0); if (u0) { input.value = short(u0); start(u0); } }
});
