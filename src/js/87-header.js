/* WhatsApp im Kopfbereich: grüner Punkt, solange wir erreichbar sind (Mo–Do 9–18, Fr 9–16 Uhr, Berliner Zeit) */
ML.module("hwa", function (ML) {
  var el = ML.$(".hwa"); if (!el) return;
  var H = { 1: [9, 18], 2: [9, 18], 3: [9, 18], 4: [9, 18], 5: [9, 16] };
  function upd() {
    var p = {};
    try {
      new Intl.DateTimeFormat("en-US", { timeZone: "Europe/Berlin", weekday: "short", hour: "numeric", minute: "numeric", hourCycle: "h23" })
        .formatToParts(new Date()).forEach(function (x) { p[x.type] = x.value; });
    } catch (e) { return; }
    var d = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"].indexOf(p.weekday), h = +p.hour + (+p.minute) / 60, t = H[d];
    var open = !!t && h >= t[0] && h < t[1];
    el.classList.toggle("is-open", open);
    el.setAttribute("aria-label", "Per WhatsApp schreiben" + (open ? " – jetzt erreichbar" : ""));
    el.title = open ? "Jetzt erreichbar – wir antworten schnell" : "Schreiben Sie uns – wir antworten am nächsten Werktag";
  }
  upd(); setInterval(upd, 60000);
});
