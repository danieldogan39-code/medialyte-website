/* Die Idee: drei Säulen mit je einer Frage zum Selbstcheck. Die Antworten zeigen den größten Hebel
   und wählen im Erstgespräch die passenden Anliegen vor (Startseite) bzw. geben sie an /termin/ weiter. */
ML.module("idea", function (ML) {
  var $ = ML.$, $$ = ML.$$;
  $$("[data-pillars]").forEach(function (root) {
    var cards = $$(".pillar", root), out = root.nextElementSibling;
    if (!cards.length || !out || !out.hasAttribute("data-pillars-out")) return;
    var txt = $("[data-po-text]", out), cta = $("[data-po-cta]", out), dots = $$(".po__dot", out);
    var base = cta ? (cta.getAttribute("href") || "").split("?")[0] : "";
    var onHome = !!document.getElementById("booking");
    var WHY = {
      vermehrung: "Mehr Anfragen – mit einer Website, die bei Google gefunden wird, und Werbung, die genau Ihre Zielgruppe erreicht.",
      verbesserung: "Ein Auftritt, der auf jedem Gerät überzeugt und immer aktuell ist – gepflegt per WhatsApp.",
      verwaltung: "Ein eigenes System, in dem jede Anfrage, jeder Termin und jeder Auftrag landet."
    };
    var ans = {};

    function list(words) {
      if (words.length < 2) return words.join("");
      return words.slice(0, -1).join(", ") + " und " + words[words.length - 1];
    }
    function say(head, rest) {
      txt.innerHTML = "<b>" + ML.esc(head) + "</b> <span>" + ML.esc(rest) + "</span>";
    }
    function render() {
      var gaps = cards.filter(function (c) { return ans[c.getAttribute("data-pillar")] === "gap"; });
      var done = cards.filter(function (c) { return !!ans[c.getAttribute("data-pillar")]; }).length;
      var open = cards.length - done;
      if (!done) say("Wo liegt Ihr größter Hebel?", "Beantworten Sie die drei Fragen oben – das Ergebnis nehmen wir direkt ins Erstgespräch mit.");
      else if (gaps.length === 1) say("Ihr größter Hebel: " + gaps[0].getAttribute("data-name") + ".", WHY[gaps[0].getAttribute("data-pillar")]);
      else if (gaps.length === cards.length) say("Bei allen drei ist Luft nach oben.", "Genau dafür sind wir da. Im Erstgespräch klären wir, womit Sie am besten anfangen.");
      else if (gaps.length > 1) say("Ihre Hebel: " + list(gaps.map(function (c) { return c.getAttribute("data-name"); })) + ".", "Im Erstgespräch zeigen wir, womit Sie am besten anfangen – und was es bringt.");
      else if (open) say(open === 1 ? "Noch eine Frage." : "Noch " + (open === 2 ? "zwei" : open) + " Fragen.", "Dann sehen Sie, wo Ihr größter Hebel liegt.");
      else say("Stark aufgestellt.", "Im Erstgespräch zeigen wir Ihnen gern, wo trotzdem noch Luft ist – ehrlich und ohne Verkaufsdruck.");

      /* Anliegen für die Buchung: alles, was zu den Hebeln gehört – ohne Doppelte */
      var asks = [];
      gaps.forEach(function (c) {
        (c.getAttribute("data-asks") || "").split(",").forEach(function (a) { if (a && asks.indexOf(a) < 0) asks.push(a); });
      });
      if (cta) {
        cta.setAttribute("data-ask", asks.join(","));
        cta.textContent = gaps.length ? "Erstgespräch dazu buchen" : "Erstgespräch buchen";
        if (!onHome && base) cta.setAttribute("href", asks.length ? base + "?anliegen=" + encodeURIComponent(asks.join(",")) : base);
      }
      out.classList.toggle("has-gap", gaps.length > 0);
      out.classList.toggle("is-done", !open);
      dots.forEach(function (d) {
        var a = ans[d.getAttribute("data-k")];
        d.classList.toggle("is-gap", a === "gap");
        d.classList.toggle("is-ok", a === "ok");
      });
    }

    cards.forEach(function (c) {
      var key = c.getAttribute("data-pillar"), btns = $$(".pillar__ans .chip", c);
      btns.forEach(function (b) {
        b.addEventListener("click", function () {
          var a = b.getAttribute("data-a");
          if (ans[key] === a) delete ans[key]; else ans[key] = a; /* zweiter Klick nimmt die Antwort zurück */
          btns.forEach(function (x) { x.setAttribute("aria-pressed", ans[key] === x.getAttribute("data-a") ? "true" : "false"); });
          c.classList.toggle("is-gap", ans[key] === "gap");
          c.classList.toggle("is-ok", ans[key] === "ok");
          render();
        });
      });
    });
  });
});
