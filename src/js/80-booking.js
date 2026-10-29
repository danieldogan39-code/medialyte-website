/* Terminbuchung: mehrstufig, mit Kalender (Feiertage, deutsche Zeit), Rückruf-Option und WhatsApp */
ML.module("booking", function (ML) {
  var $ = ML.$, $$ = ML.$$, store = ML.store, esc = ML.esc, CFG = ML.cfg, reduce = ML.reduce;
  var bk = $("#booking");
  if (bk) booking(bk);

  function booking(root) {
    var form = $("form", root);
    var steps = $$(".bk__step", root);
    var prog = $$(".bk__progress li", root);
    var err = $(".bk__err", root);
    var btnBack = $("[data-back]", root), btnNext = $("[data-next]", root);
    var navBar = $(".bk__nav", root);
    var demo = root.getAttribute("data-demo") === "1";
    var endpoint = root.getAttribute("data-endpoint");
    var slotsUrl = root.getAttribute("data-slots");
    var C = CFG.booking || {};
    var DUR = C.duration || 30, SLOT = C.step || 30, AHEAD = C.daysAhead || 42, LEAD = C.leadHours || 18;
    var HOURS = C.hours || { 1: ["09:00", "18:00"], 2: ["09:00", "18:00"], 3: ["09:00", "18:00"], 4: ["09:00", "18:00"], 5: ["09:00", "16:00"] };
    var booked = {};
    var step = 1, sel = { date: null, time: null }, month = null;
    var KEY = "ml-booking";

    /* Prefill aus URL, Paket-Buttons und Sitzung */
    var saved = store.get(KEY);
    var qs = new URLSearchParams(location.search);
    $$("[data-ask]").forEach(function (b) {
      b.addEventListener("click", function () {
        var ask = b.getAttribute("data-ask");
        if (ask) { $$('input[name="anliegen"]', form).forEach(function (i) { i.checked = false; }); preselect(ask.split(",")); }
        var br = b.getAttribute("data-branche");
        if (br && form.elements.branche) { form.elements.branche.value = br; persist(); }
        if (step !== 1) go(1, true);
      });
    });
    function preselect(list) {
      list.forEach(function (v) { var i = form.querySelector('input[name="anliegen"][value="' + v.trim() + '"]'); if (i) i.checked = true; });
      persist();
    }

    /* Gebuchte Zeiten laden (nur live) */
    if (!demo && slotsUrl) {
      fetch(slotsUrl, { headers: { "Accept": "application/json" } }).then(function (r) { return r.ok ? r.json() : null; })
        .then(function (j) { if (j && j.booked) { j.booked.forEach(function (s) { booked[s] = true; }); renderCal(); } })
        .catch(function () { /* ohne Liste weiter */ });
    }

    /* ---------- Feiertage (bundesweit + Hamburg) ---------- */
    function easter(y) {
      var a = y % 19, b = Math.floor(y / 100), c = y % 100, d = Math.floor(b / 4), e = b % 4, f = Math.floor((b + 8) / 25),
        g = Math.floor((b - f + 1) / 3), h = (19 * a + b - d - g + 15) % 30, i = Math.floor(c / 4), k = c % 4,
        l = (32 + 2 * e + 2 * i - h - k) % 7, m = Math.floor((a + 11 * h + 22 * l) / 451),
        mo = Math.floor((h + l - 7 * m + 114) / 31), da = ((h + l - 7 * m + 114) % 31) + 1;
      return new Date(Date.UTC(y, mo - 1, da));
    }
    var holCache = {};
    function holidays(y) {
      if (holCache[y]) return holCache[y];
      var e = easter(y), add = function (n) { var d = new Date(e); d.setUTCDate(d.getUTCDate() + n); return ymd(d.getUTCFullYear(), d.getUTCMonth() + 1, d.getUTCDate()); };
      var list = [ymd(y, 1, 1), add(-2), add(1), ymd(y, 5, 1), add(39), add(50), ymd(y, 10, 3), ymd(y, 10, 31), ymd(y, 12, 24), ymd(y, 12, 25), ymd(y, 12, 26), ymd(y, 12, 31)];
      var set = {}; list.forEach(function (s) { set[s] = true; }); holCache[y] = set; return set;
    }
    (C.closed || []).forEach(function (s) { var y = +s.slice(0, 4); holidays(y)[s] = true; });

    /* ---------- Zeit-Helfer (Europe/Berlin) ---------- */
    function pad(n) { return (n < 10 ? "0" : "") + n; }
    function ymd(y, m, d) { return y + "-" + pad(m) + "-" + pad(d); }
    /* Ein Formatierer für alle Abfragen und ein Merkzettel je Tag und Stunde: Intl neu anzulegen kostet auf dem Handy spürbar Zeit */
    var offFmt = null, offCache = {};
    function berlinOffsetMin(y, m, d, hh, mm) {
      var key = y + "-" + m + "-" + d + "-" + hh;
      if (offCache[key] != null) return offCache[key];
      return (offCache[key] = offsetNow(y, m, d, hh, mm));
    }
    function offsetNow(y, m, d, hh, mm) {
      try {
        var dt = new Date(Date.UTC(y, m - 1, d, hh, mm));
        offFmt = offFmt || new Intl.DateTimeFormat("en-US", { timeZone: "Europe/Berlin", timeZoneName: "shortOffset" });
        var parts = offFmt.formatToParts(dt);
        var tz = (parts.find(function (p) { return p.type === "timeZoneName"; }) || {}).value || "GMT+1";
        var mt = tz.match(/GMT([+-]\d+)(?::(\d+))?/);
        return mt ? (parseInt(mt[1], 10) * 60 + (mt[2] ? parseInt(mt[2], 10) : 0)) : 60;
      } catch (e) { return (m > 3 && m < 11) ? 120 : 60; }
    }
    function slotEpoch(dateStr, time) {
      var p = dateStr.split("-").map(Number), t = time.split(":").map(Number);
      var off = berlinOffsetMin(p[0], p[1], p[2], t[0], t[1]);
      return Date.UTC(p[0], p[1] - 1, p[2], t[0], t[1]) - off * 60000;
    }
    function isoWithOffset(dateStr, time) {
      var p = dateStr.split("-").map(Number), t = time.split(":").map(Number);
      var off = berlinOffsetMin(p[0], p[1], p[2], t[0], t[1]);
      var s = off >= 0 ? "+" : "-", a = Math.abs(off);
      return dateStr + "T" + time + ":00" + s + pad(Math.floor(a / 60)) + ":" + pad(a % 60);
    }
    function berlinToday() {
      try {
        var f = new Intl.DateTimeFormat("en-CA", { timeZone: "Europe/Berlin", year: "numeric", month: "2-digit", day: "2-digit" }).format(new Date());
        return f;
      } catch (e) { var d = new Date(); return ymd(d.getFullYear(), d.getMonth() + 1, d.getDate()); }
    }
    function weekday(dateStr) { var p = dateStr.split("-").map(Number); return new Date(Date.UTC(p[0], p[1] - 1, p[2])).getUTCDay(); }
    function addDays(dateStr, n) { var p = dateStr.split("-").map(Number); var d = new Date(Date.UTC(p[0], p[1] - 1, p[2] + n)); return ymd(d.getUTCFullYear(), d.getUTCMonth() + 1, d.getUTCDate()); }
    var DOW = ["So", "Mo", "Di", "Mi", "Do", "Fr", "Sa"];
    var DOWL = ["Sonntag", "Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag"];
    var MON = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"];
    function fmtDate(dateStr, long) {
      var p = dateStr.split("-").map(Number), w = weekday(dateStr);
      return (long ? DOWL[w] : DOW[w]) + ", " + p[2] + ". " + MON[p[1] - 1] + (long ? " " + p[0] : "");
    }

    function slotsFor(dateStr) {
      var w = weekday(dateStr), h = HOURS[w];
      if (!h || holidays(+dateStr.slice(0, 4))[dateStr]) return [];
      var out = [], from = h[0].split(":").map(Number), to = h[1].split(":").map(Number);
      var m = from[0] * 60 + from[1], end = to[0] * 60 + to[1] - DUR, now = Date.now() + LEAD * 3600000;
      for (; m <= end; m += SLOT) {
        var t = pad(Math.floor(m / 60)) + ":" + pad(m % 60);
        if (slotEpoch(dateStr, t) < now) continue;
        if (booked[dateStr + "T" + t]) continue;
        out.push(t);
      }
      return out;
    }
    var today = berlinToday(), lastDay = addDays(today, AHEAD);
    function availDays() {
      var list = [];
      for (var i = 0; i <= AHEAD; i++) { var d = addDays(today, i); if (slotsFor(d).length) list.push(d); }
      return list;
    }

    /* ---------- Kalender ---------- */
    var calGrid = $(".cal__grid", root), calTitle = $(".cal__head b", root);
    var calPrev = $("[data-cal-prev]", root), calNext = $("[data-cal-next]", root);
    var slotBox = $(".slots", root);
    var cbOnly = $("#bk-callback", root), calWrap = $(".cal", root), cbWrap = $(".bk__cb", root);
    function renderCal() {
      if (!calGrid) return;
      var avail = {}; availDays().forEach(function (d) { avail[d] = true; });
      if (!month) { var first = Object.keys(avail)[0] || today; month = first.slice(0, 7); }
      var y = +month.slice(0, 4), m = +month.slice(5, 7);
      calTitle.textContent = MON[m - 1] + " " + y;
      var firstDow = (new Date(Date.UTC(y, m - 1, 1)).getUTCDay() + 6) % 7;
      var days = new Date(Date.UTC(y, m, 0)).getUTCDate();
      var html = ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"].map(function (d) { return '<span class="cal__dow">' + d + "</span>"; }).join("");
      for (var i = 0; i < firstDow; i++) html += "<span></span>";
      for (var d = 1; d <= days; d++) {
        var ds = ymd(y, m, d), cls = "cal__day", attrs = "";
        if (avail[ds]) { cls += " is-avail"; attrs = ' data-date="' + ds + '" aria-label="' + fmtDate(ds, true) + ', Termine verfügbar"'; }
        else attrs = ' disabled aria-label="' + fmtDate(ds, true) + ', keine Termine"';
        if (ds === sel.date) cls += " is-sel";
        if (ds === today) cls += " is-today";
        html += '<button type="button" class="' + cls + '"' + attrs + (ds === sel.date ? ' aria-pressed="true"' : "") + ">" + d + "</button>";
      }
      calGrid.innerHTML = html;
      calPrev.disabled = month <= today.slice(0, 7);
      calNext.disabled = month >= lastDay.slice(0, 7);
      renderSlots();
    }
    function renderSlots() {
      if (!slotBox) return;
      if (!sel.date) { slotBox.innerHTML = '<p class="slots__h">Uhrzeit<small>Bitte zuerst einen Tag wählen.</small></p>'; return; }
      var list = slotsFor(sel.date);
      var html = '<p class="slots__h">' + fmtDate(sel.date) + '<small>Deutsche Zeit, ' + DUR + " Minuten</small></p>";
      if (!list.length) html += '<p class="slots__empty">An diesem Tag ist leider nichts mehr frei.</p>';
      list.forEach(function (t) { html += '<button type="button" class="slot" data-time="' + t + '" aria-pressed="' + (sel.time === t ? "true" : "false") + '">' + t + " Uhr</button>"; });
      slotBox.innerHTML = html;
    }
    if (calGrid) {
      calGrid.addEventListener("click", function (e) {
        var b = e.target.closest("[data-date]"); if (!b) return;
        sel.date = b.getAttribute("data-date"); sel.time = null; renderCal(); persist();
        var first = $(".slot", slotBox); if (first && window.innerWidth < 700) first.scrollIntoView({ block: "nearest", behavior: reduce ? "auto" : "smooth" });
      });
      slotBox.addEventListener("click", function (e) {
        var b = e.target.closest("[data-time]"); if (!b) return;
        sel.time = b.getAttribute("data-time"); renderSlots(); persist(); clearErr();
      });
      calPrev.addEventListener("click", function () { var y = +month.slice(0, 4), m = +month.slice(5, 7) - 1; if (m < 1) { m = 12; y--; } month = y + "-" + pad(m); renderCal(); });
      calNext.addEventListener("click", function () { var y = +month.slice(0, 4), m = +month.slice(5, 7) + 1; if (m > 12) { m = 1; y++; } month = y + "-" + pad(m); renderCal(); });
      if (cbOnly) cbOnly.addEventListener("change", function () { calWrap.hidden = cbOnly.checked; cbWrap.hidden = !cbOnly.checked; persist(); });
      renderCal();
    }

    /* ---------- Schritte ---------- */
    function val(name) { var el = form.elements[name]; if (!el) return ""; if (el.length && !el.tagName) { var c = Array.prototype.find.call(el, function (x) { return x.checked; }); return c ? c.value : ""; } return (el.value || "").trim(); }
    function checkedList(name) { return $$('input[name="' + name + '"]:checked', form).map(function (i) { return i.value; }); }
    function labelOf(input) { var l = form.querySelector('label[for="' + input.id + '"] b'); return l ? l.textContent : input.value; }
    function clearErr() { err.textContent = ""; $$(".is-invalid", form).forEach(function (f) { f.classList.remove("is-invalid"); }); $$("[aria-invalid]", form).forEach(function (f) { f.removeAttribute("aria-invalid"); }); }
    function bad(msg, names) {
      err.textContent = msg;
      (names || []).forEach(function (n) {
        var el = form.elements[n]; if (!el) return;
        var f = (el.closest ? el : el[0]).closest(".field"); if (f) f.classList.add("is-invalid");
        if (el.setAttribute) el.setAttribute("aria-invalid", "true");
      });
      var first = names && names.length && form.elements[names[0]];
      if (first && first.focus) first.focus();
      return false;
    }
    function validate(s) {
      clearErr();
      if (s === 1 && !checkedList("anliegen").length) return bad("Bitte wählen Sie mindestens ein Anliegen.");
      if (s === 2) {
        var miss = [];
        if (!val("firma")) miss.push("firma");
        if (!val("branche")) miss.push("branche");
        if (miss.length) return bad("Bitte nennen Sie Ihr Unternehmen und Ihre Branche.", miss);
        var w = val("website");
        if (w && !/^(https?:\/\/)?[^\s.]+\.[^\s]{2,}$/i.test(w)) return bad("Bitte prüfen Sie die Adresse Ihrer Website.", ["website"]);
      }
      if (s === 3) {
        if (!val("format")) return bad("Bitte wählen Sie, wie das Gespräch stattfinden soll.");
        if (!(cbOnly && cbOnly.checked) && !(sel.date && sel.time)) return bad("Bitte wählen Sie einen Tag und eine Uhrzeit oder fordern Sie einen Rückruf an.");
      }
      if (s === 4) {
        var m = [];
        if (val("name").length < 2) m.push("name");
        if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(val("email"))) m.push("email");
        var needPhone = val("format") === "telefon" || (cbOnly && cbOnly.checked) || $("#bk-wa", form).checked;
        if (needPhone && val("telefon").replace(/\D/g, "").length < 6) m.push("telefon");
        if (m.length) return bad(m.indexOf("telefon") >= 0 && m.length === 1 ? "Für Telefonat, Rückruf oder WhatsApp brauchen wir Ihre Nummer." : "Bitte prüfen Sie die markierten Felder.", m);
        if (!$("#bk-consent", form).checked) return bad("Bitte bestätigen Sie die Einwilligung zur Bearbeitung Ihrer Anfrage.", ["einwilligung"]);
      }
      return true;
    }
    function go(n, quiet) {
      step = n;
      steps.forEach(function (s) {
        var on = +s.getAttribute("data-step") === n;
        s.hidden = !on;
        if (on) { s.classList.remove("is-enter"); void s.offsetWidth; s.classList.add("is-enter"); }
      });
      prog.forEach(function (li) { var p = +li.getAttribute("data-p"); li.classList.toggle("is-on", p === n); li.classList.toggle("is-done", p < n); });
      btnBack.hidden = n === 1 || n === 5;
      navBar.hidden = n === 5;
      var isCb = cbOnly && cbOnly.checked;
      btnNext.textContent = n === 4 ? (isCb ? "Rückruf anfordern" : "Termin anfragen") : "Weiter";
      var lead4 = $('[data-step="4"] > p', root);
      if (lead4) lead4.textContent = isCb ? "Fast geschafft. Wir rufen Sie im gewünschten Zeitraum zurück." : "Fast geschafft. Wir bestätigen Ihren Termin per E-Mail.";
      if (n === 4) renderPick();
      if (!quiet) {
        var h = $(".bk__step:not([hidden]) h3", root);
        if (h) { h.setAttribute("tabindex", "-1"); h.focus({ preventScroll: true }); }
        /* Zum Formular scrollen (nicht zur Seitenleiste darüber), unter der festen Kopfzeile */
        var hd = document.querySelector(".header"), off = (hd ? hd.offsetHeight : 72) + 12;
        var top = form.getBoundingClientRect().top;
        if (top < off - 4 || top > window.innerHeight * 0.5) window.scrollTo({ top: Math.max(0, Math.round(top + (window.scrollY || 0) - off)), behavior: reduce ? "auto" : "smooth" });
      }
      persist();
    }
    function renderPick() {
      var box = $(".bk__pick", root); if (!box) return;
      var fmt = $('input[name="format"]:checked', form);
      var when = (cbOnly && cbOnly.checked) ? "Rückruf, " + (val("zeitfenster") || "flexibel") : (sel.date ? fmtDate(sel.date, true) + ", " + sel.time + " Uhr" : "");
      box.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><rect x="3" y="4.5" width="18" height="16" rx="3"/><path d="M3 9.5h18M8 2.5v4M16 2.5v4"/></svg><span><b>' + esc(when) + "</b>" + (fmt ? " · " + esc(labelOf(fmt)) : "") + '</span><button type="button" data-goto="3">Ändern</button>';
      $("[data-goto]", box).addEventListener("click", function () { go(3); });
    }
    btnBack.addEventListener("click", function () { if (step > 1) go(step - 1); });
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!validate(step)) return;
      if (step < 4) { go(step + 1); return; }
      send();
    });
    form.addEventListener("change", function () { persist(); });
    form.addEventListener("input", function (e) { if (e.target.closest(".is-invalid")) e.target.closest(".is-invalid").classList.remove("is-invalid"); persist(); });

    function payload() {
      var anl = $$('input[name="anliegen"]:checked', form);
      var fmt = $('input[name="format"]:checked', form);
      var utm = {}; ["utm_source", "utm_medium", "utm_campaign", "gclid"].forEach(function (k) { if (qs.get(k)) utm[k] = qs.get(k); });
      var cb = cbOnly && cbOnly.checked;
      return {
        anliegen: anl.map(function (i) { return i.value; }),
        anliegen_text: anl.map(labelOf),
        firma: val("firma"), branche: val("branche"), website: val("website"), ort: val("ort"), groesse: val("groesse"),
        format: fmt ? fmt.value : "", format_text: fmt ? labelOf(fmt) : "",
        termin: cb ? null : { start: isoWithOffset(sel.date, sel.time), datum: sel.date, uhrzeit: sel.time, dauer_min: DUR },
        rueckruf: cb ? { zeitfenster: val("zeitfenster") || "flexibel" } : null,
        name: val("name"), email: val("email"), telefon: val("telefon"),
        whatsapp_ok: $("#bk-wa", form).checked, nachricht: val("nachricht"),
        einwilligung: $("#bk-consent", form).checked,
        quelle: { seite: location.pathname, referrer: document.referrer || "", utm: utm },
        hp: val("firma_url")
      };
    }
    function send() {
      var data = payload();
      btnNext.disabled = true;
      btnNext.textContent = "Wird gesendet …";
      var done = function (ok, msg) {
        btnNext.disabled = false;
        if (ok) { finish(data); store.del(KEY); }
        else { go(4); err.textContent = msg || "Das hat leider nicht geklappt. Bitte versuchen Sie es erneut oder schreiben Sie uns per WhatsApp."; }
      };
      if (demo || !endpoint) { setTimeout(function () { done(true); }, 700); return; }
      fetch(endpoint, { method: "POST", headers: { "Content-Type": "application/json", "Accept": "application/json" }, body: JSON.stringify(data) })
        .then(function (r) { return r.json().catch(function () { return { ok: false }; }).then(function (j) { return { status: r.status, j: j }; }); })
        .then(function (res) {
          if (res.j && res.j.ok) done(true);
          else if (res.status === 409) { booked[data.termin && (data.termin.datum + "T" + data.termin.uhrzeit)] = true; sel.time = null; renderCal(); go(3); err.textContent = "Dieser Termin wurde gerade vergeben. Bitte wählen Sie eine andere Uhrzeit."; btnNext.disabled = false; }
          else done(false, res.j && res.j.error);
        })
        .catch(function () { done(false); });
    }
    function finish(d) {
      go(5);
      var first = d.name.split(" ")[0];
      $(".done__name", root).textContent = first ? ", " + first : "";
      var ZF = { vormittags: "vormittags", nachmittags: "nachmittags", flexibel: "wann es Ihnen passt" };
      var when = d.termin ? fmtDate(d.termin.datum, true) + ", " + d.termin.uhrzeit + " Uhr (" + d.format_text + ")" : "Rückruf, " + (ZF[d.rueckruf.zeitfenster] || d.rueckruf.zeitfenster);
      var line = $(".done__line", root);
      if (line) {
        if (d.termin) { line.innerHTML = 'Ihre Anfrage für <b class="done__when"></b> ist bei uns eingegangen. Sie erhalten in Kürze eine Bestätigung per E-Mail.'; line.querySelector("b").textContent = when; }
        else { line.innerHTML = 'Ihre Rückrufbitte ist bei uns eingegangen. Wir melden uns <b class="done__when"></b> bei Ihnen.'; line.querySelector("b").textContent = ZF[d.rueckruf.zeitfenster] || "zeitnah"; }
      }
      var sum = $(".done .summary", root);
      sum.innerHTML = [
        [d.termin ? "Termin" : "Rückruf", d.termin ? when : (ZF[d.rueckruf.zeitfenster] || d.rueckruf.zeitfenster)], ["Anliegen", d.anliegen_text.join(", ")], ["Unternehmen", d.firma + (d.branche ? " · " + d.branche : "")], ["Kontakt", d.email + (d.telefon ? " · " + d.telefon : "")]
      ].map(function (r) { return "<div><dt>" + esc(r[0]) + "</dt><dd>" + esc(r[1]) + "</dd></div>"; }).join("");
      var ics = $("[data-ics]", root);
      if (ics) {
        ics.hidden = demo || !d.termin;
        ics.onclick = function () { downloadIcs(d); };
      }
      var wa = $("[data-wa-done]", root);
      if (wa) {
        var txt = "Hallo Medialyte, ich habe gerade " + (d.termin ? "einen Termin am " + fmtDate(d.termin.datum, true) + " um " + d.termin.uhrzeit + " Uhr angefragt." : "einen Rückruf angefragt.");
        wa.href = (CFG.whatsapp || "https://wa.me/491709647532") + "?text=" + encodeURIComponent(txt);
      }
      var note = $(".demo-note", root); if (note) note.hidden = !demo;
    }
    function downloadIcs(d) {
      var start = new Date(slotEpoch(d.termin.datum, d.termin.uhrzeit)), end = new Date(start.getTime() + DUR * 60000);
      var f = function (dt) { return dt.toISOString().replace(/[-:]/g, "").replace(/\.\d{3}/, ""); };
      var ics = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Medialyte//Termin//DE", "BEGIN:VEVENT",
        "UID:" + Date.now() + "@medialyte.de", "DTSTAMP:" + f(new Date()), "DTSTART:" + f(start), "DTEND:" + f(end),
        "SUMMARY:Erstgespräch mit Medialyte", "DESCRIPTION:" + d.format_text + " – Medialyte meldet sich zur Bestätigung.",
        "LOCATION:" + (d.format === "vor-ort" ? "Bei Ihnen vor Ort (Adresse stimmen wir vorher ab)" : d.format_text), "END:VEVENT", "END:VCALENDAR"].join("\r\n");
      var a = document.createElement("a");
      a.href = URL.createObjectURL(new Blob([ics], { type: "text/calendar;charset=utf-8" }));
      a.download = "medialyte-termin.ics"; document.body.appendChild(a); a.click(); a.remove();
    }

    /* Sitzung merken */
    function persist() {
      if (step === 5) return;
      var o = { step: step, sel: sel, f: {} };
      $$("input, select, textarea", form).forEach(function (el) {
        if (!el.name || el.name === "firma_url" || el.name === "einwilligung") return;
        if (el.type === "checkbox" || el.type === "radio") { if (el.checked) (o.f[el.name] = o.f[el.name] || []).push(el.value); }
        else o.f[el.name] = el.value;
      });
      store.set(KEY, o);
    }
    function restore(o) {
      if (!o || !o.f) return;
      Object.keys(o.f).forEach(function (k) {
        var v = o.f[k];
        $$('[name="' + k + '"]', form).forEach(function (el) {
          if (el.type === "checkbox" || el.type === "radio") el.checked = Array.isArray(v) && v.indexOf(el.value) >= 0;
          else el.value = v;
        });
      });
      if (o.sel) sel = { date: o.sel.date || null, time: o.sel.time || null };
      if (sel.date && sel.date < today) sel = { date: null, time: null };
      /* Termin aus der letzten Sitzung: nur behalten, wenn er noch weit genug in der Zukunft liegt */
      if (sel.date && sel.time) { try { if (slotEpoch(sel.date, sel.time) < Date.now() + LEAD * 3600000) sel.time = null; } catch (e) { sel.time = null; } }
      if (cbOnly && cbOnly.checked) { calWrap.hidden = true; cbWrap.hidden = false; }
    }
    if (saved) restore(saved);
    if (qs.get("anliegen")) preselect(qs.get("anliegen").split(","));
    if (qs.get("branche") && form.elements.branche) { form.elements.branche.value = qs.get("branche"); }
    if (qs.get("quelle") === "brief") preselect(["brief"]);
    if (sel.date) month = sel.date.slice(0, 7);
    renderCal();
    go(saved && saved.step > 1 && saved.step < 5 ? saved.step : 1, true);
  }
});
