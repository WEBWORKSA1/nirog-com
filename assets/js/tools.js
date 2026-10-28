/* Nirog.com calculators and the Nirog Score. All maths runs in the browser; nothing is stored or sent. */
(function () {
  "use strict";
  function $(s, r) { return (r || document).querySelector(s); }
  function num(f, n) { var el = f.elements[n]; if (!el) return NaN; var v = parseFloat(el.value); return isNaN(v) ? NaN : v; }
  function val(f, n) { var el = f.elements[n]; if (!el) return ""; if (el.length && !el.tagName) { for (var i = 0; i < el.length; i++) if (el[i].checked) return el[i].value; return ""; } return el.value; }
  function fmt(n, d) { return Number(n).toLocaleString("en-IN", { maximumFractionDigits: d == null ? 0 : d, minimumFractionDigits: d == null ? 0 : d }); }
  function pill(cls, t) { return '<span class="pill ' + cls + '">' + t + "</span>"; }
  function meter(pct) { pct = Math.max(0, Math.min(100, pct)); return '<div class="meter" aria-hidden="true"><i style="left:' + pct + '%"></i></div>'; }
  function cta(text, href) { return '<p class="small" style="margin-top:14px"><a class="btn primary sm" href="' + (window.NIROG_BASE || "") + (href || "get-advice.html") + '">' + (text || "Get free check-up advice") + "</a></p>"; }
  var empty = '<p class="muted">Fill in the fields and your result appears here instantly.</p>';

  var calcs = {
    bmi: function (f) {
      var h = num(f, "height") / 100, w = num(f, "weight");
      if (!(h > 0.9 && w > 20)) return empty;
      var b = w / (h * h), cls, lab;
      if (b < 18.5) { cls = "info"; lab = "Underweight"; }
      else if (b < 23) { cls = "ok"; lab = "Healthy range"; }
      else if (b < 25) { cls = "warn"; lab = "Overweight (Asian cut-off)"; }
      else { cls = "err"; lab = "Obesity (Asian cut-off)"; }
      var lo = 18.5 * h * h, hi = 22.9 * h * h;
      return '<div class="big">' + fmt(b, 1) + '</div><div class="label">' + pill(cls, lab) + "</div>" + meter((b - 15) / 25 * 100) +
        "<p>Healthy weight for your height (BMI 18.5–22.9): <b>" + fmt(lo, 1) + "–" + fmt(hi, 1) + " kg</b>.</p>" +
        '<p class="small muted">Indian and Asian guidelines use lower cut-offs than the global ones (overweight from 23, obesity from 25) because South Asians develop diabetes and heart disease at lower body weights. BMI does not measure body fat directly; check your waist too.</p>' + cta("Get a free preventive check-up plan");
    },
    calories: function (f) {
      var a = num(f, "age"), h = num(f, "height"), w = num(f, "weight"), s = val(f, "sex"), act = num(f, "activity");
      if (!(a > 14 && h > 90 && w > 25 && act)) return empty;
      var bmr = 10 * w + 6.25 * h - 5 * a + (s === "female" ? -161 : 5), tdee = bmr * act;
      return '<div class="big">' + fmt(tdee) + ' kcal</div><div class="label">Estimated daily needs to maintain weight</div>' +
        "<table class='prose'><tr><td>Resting (BMR)</td><td><b>" + fmt(bmr) + " kcal</b></td></tr><tr><td>Gentle weight loss (about −500 kcal)</td><td><b>" + fmt(Math.max(tdee - 500, s === "female" ? 1200 : 1500)) + " kcal</b></td></tr><tr><td>Weight gain (about +300 kcal)</td><td><b>" + fmt(tdee + 300) + " kcal</b></td></tr></table>" +
        '<p class="small muted">Mifflin-St Jeor equation. Real needs vary by about ±10%. Pregnant or breastfeeding women and people with medical conditions should follow their doctor or dietitian.</p>';
    },
    idrs: function (f) {
      var a = val(f, "age"), w = val(f, "waist"), p = val(f, "activity"), fh = val(f, "family");
      if (!a || !w || !p || !fh) return '<p class="muted">Answer all four questions to see your score.</p>';
      var s = (+a) + (+w) + (+p) + (+fh), cls, lab, msg;
      if (s >= 60) { cls = "err"; lab = "High risk"; msg = "A score of 60 or more points to a high likelihood of diabetes or prediabetes. Get a fasting glucose and HbA1c test soon and discuss the result with a doctor."; }
      else if (s >= 30) { cls = "warn"; lab = "Moderate risk"; msg = "Plan a blood sugar test (fasting glucose or HbA1c) in the next few months and start the lifestyle changes below."; }
      else { cls = "ok"; lab = "Low risk"; msg = "Keep it that way: stay active, watch your waist and repeat a sugar test as part of routine check-ups."; }
      return '<div class="big">' + s + ' / 100</div><div class="label">' + pill(cls, lab) + "</div>" + meter(s) + "<p>" + msg + "</p>" +
        '<p class="small muted">Based on the Indian Diabetes Risk Score (IDRS) developed by the Madras Diabetes Research Foundation (Mohan V et al., JAPI 2005). It is a screening tool, not a diagnosis.</p>' + cta("Book a free sugar-test consultation", "get-advice.html?need=checkup");
    },
    bp: function (f) {
      var sy = num(f, "sys"), di = num(f, "dia");
      if (!(sy > 60 && di > 30)) return empty;
      var cls, lab, msg;
      if (sy > 180 || di > 120) { cls = "err"; lab = "Very high: seek care now"; msg = "Readings this high can be dangerous. Re-check after 5 minutes of rest. If still this high, or with chest pain, breathlessness, weakness, vision or speech problems, call 108 or 112 immediately."; }
      else if (sy >= 140 || di >= 90) { cls = "err"; lab = "Stage 2 high blood pressure"; msg = "See a doctor soon to confirm with repeated readings and agree a treatment plan."; }
      else if (sy >= 130 || di >= 80) { cls = "warn"; lab = "Stage 1 high blood pressure"; msg = "Confirm with home readings over a week and talk to your doctor. Lifestyle changes help a lot at this stage."; }
      else if (sy >= 120) { cls = "warn"; lab = "Elevated"; msg = "Above ideal. Cut salt, move more and re-check regularly."; }
      else if (sy < 90 || di < 60) { cls = "info"; lab = "Low blood pressure"; msg = "Low readings are often harmless, but tell a doctor if you feel dizzy, faint or unusually tired."; }
      else { cls = "ok"; lab = "Normal"; msg = "Great. Keep checking at least once a year, more often if you have diabetes or a family history."; }
      return '<div class="big">' + sy + "/" + di + '</div><div class="label">' + pill(cls, lab) + "</div>" + meter((sy - 90) / 100 * 100) + "<p>" + msg + "</p>" +
        '<p class="small muted">Categories follow the 2017 ACC/AHA guideline. One reading is never enough to diagnose hypertension.</p>';
    },
    water: function (f) {
      var w = num(f, "weight"), ex = num(f, "exercise") || 0, hot = val(f, "climate") === "hot";
      if (!(w > 20)) return empty;
      var ml = w * 33 + ex * 12 + (hot ? 500 : 0), glasses = ml / 250;
      return '<div class="big">' + fmt(ml / 1000, 1) + ' litres</div><div class="label">About ' + fmt(glasses) + " glasses (250 ml) a day</div>" +
        '<p class="small muted">A practical starting point (about 33 ml per kg, plus extra for exercise and heat). Food, tea, milk and dal count too. People with kidney, heart or liver disease may need a fluid limit: ask your doctor.</p>';
    },
    idealweight: function (f) {
      var h = num(f, "height") / 100; if (!(h > 0.9)) return empty;
      var lo = 18.5 * h * h, hi = 22.9 * h * h, mid = 21.7 * h * h;
      return '<div class="big">' + fmt(lo, 0) + "–" + fmt(hi, 0) + ' kg</div><div class="label">Healthy weight range for ' + fmt(h * 100) + " cm</div><p>A practical target in the middle of the range: <b>" + fmt(mid, 0) + " kg</b>.</p>" +
        '<p class="small muted">Uses the Asian healthy BMI range of 18.5–22.9. Muscular people may sit above it and still be healthy; waist size matters as much as weight.</p>';
    },
    whtr: function (f) {
      var w = num(f, "waist"), h = num(f, "height"); if (!(w > 30 && h > 90)) return empty;
      var r = w / h, cls, lab;
      if (r < 0.4) { cls = "info"; lab = "Possibly underweight"; } else if (r < 0.5) { cls = "ok"; lab = "Healthy"; } else if (r < 0.6) { cls = "warn"; lab = "Increased health risk"; } else { cls = "err"; lab = "High health risk"; }
      return '<div class="big">' + fmt(r, 2) + '</div><div class="label">' + pill(cls, lab) + "</div>" + meter((r - 0.35) / 0.35 * 100) +
        "<p>Rule of thumb: keep your waist to less than half your height, i.e. under <b>" + fmt(h / 2) + " cm</b>.</p>" +
        '<p class="small muted">Waist-to-height ratio predicts heart and diabetes risk better than BMI alone. Measure midway between the lowest rib and the top of the hip bone, after breathing out.</p>' + cta();
    },
    heartrate: function (f) {
      var a = num(f, "age"), rest = num(f, "rest"); if (!(a > 10 && a < 100)) return empty;
      var max = 208 - 0.7 * a, useK = rest > 30 && rest < 120;
      var z = [[50, 60, "Very light", "Warm-up, recovery"], [60, 70, "Light", "Fat-burning base, brisk walking"], [70, 80, "Moderate", "Aerobic fitness"], [80, 90, "Hard", "Tempo, speed"], [90, 100, "Maximum", "Short intervals only"]];
      var rows = z.map(function (r) {
        var lo = useK ? rest + (max - rest) * r[0] / 100 : max * r[0] / 100, hi = useK ? rest + (max - rest) * r[1] / 100 : max * r[1] / 100;
        return "<tr><td><b>" + r[2] + "</b><br><span class='small muted'>" + r[3] + "</span></td><td>" + fmt(lo) + "–" + fmt(hi) + " bpm</td></tr>";
      }).join("");
      return '<div class="big">' + fmt(max) + ' bpm</div><div class="label">Estimated maximum heart rate</div><table class="prose">' + rows + "</table>" +
        '<p class="small muted">Tanaka formula (208 − 0.7 × age)' + (useK ? " with the Karvonen method using your resting pulse" : "") + ". If you take BP or heart medicines (e.g. beta-blockers) or have heart disease, ask your doctor for safe targets.</p>";
    },
    cover: function (f) {
      var city = val(f, "city"), adults = num(f, "adults") || 1, kids = num(f, "kids") || 0, age = num(f, "eldest"), ped = val(f, "ped"), parents = val(f, "parents");
      if (!city || !(age > 17)) return '<p class="muted">Choose your city type and the age of the eldest member.</p>';
      var base = { metro: 10, tier2: 7.5, tier3: 5 }[city];
      var factor = 1 + Math.max(0, adults - 1) * 0.4 + kids * 0.15;
      if (age >= 60) factor *= 1.6; else if (age >= 45) factor *= 1.3;
      if (ped === "yes") factor *= 1.2;
      var raw = base * factor, steps = [5, 7.5, 10, 15, 20, 25, 30, 50, 75, 100], rec = steps[steps.length - 1];
      for (var i = 0; i < steps.length; i++) if (steps[i] >= raw) { rec = steps[i]; break; }
      var top = rec >= 15 ? rec * 2 : 25;
      var par = parents === "yes" ? "<li>Buy a <b>separate policy for parents</b> (often ₹5–10 lakh plus a super top-up) so their claims don't eat into your family cover.</li>" : "";
      return '<div class="big">₹' + fmt(rec, rec % 1 ? 1 : 0) + ' lakh</div><div class="label">Suggested base cover</div><ul class="list-check"><li>Add a <b>super top-up of ₹' + fmt(top) + " lakh</b> to protect against one very large bill at low cost.</li>" + par +
        "<li>Prefer <b>no room-rent cap</b> and no or low co-pay.</li><li>Check the waiting period for pre-existing diseases (now capped at 3 years).</li></ul>" +
        '<p class="small muted">A rule-of-thumb estimate based on city hospital costs, family size and age. It is not insurance advice or a quote; read each policy wording.</p>' +
        cta("Get free, unbiased plan recommendations", "get-advice.html?need=insurance");
    },
    duedate: function (f) {
      var lmp = f.elements.lmp && f.elements.lmp.value, cyc = num(f, "cycle") || 28;
      if (!lmp) return empty;
      var d = new Date(lmp + "T00:00:00"); if (isNaN(d)) return empty;
      var due = new Date(d.getTime() + (280 + (cyc - 28)) * 864e5), now = new Date();
      var days = Math.floor((now - d) / 864e5), wk = Math.floor(days / 7), dd = days % 7;
      var o = { day: "numeric", month: "long", year: "numeric" };
      var tri = wk < 13 ? "First trimester" : wk < 27 ? "Second trimester" : "Third trimester";
      var prog = days >= 0 && days < 300 ? "<p>You are about <b>" + wk + " weeks " + dd + " days</b> along (" + tri + ").</p>" : "";
      return '<div class="big" style="font-size:2rem">' + due.toLocaleDateString("en-IN", o) + '</div><div class="label">Estimated due date</div>' + prog +
        '<p class="small muted">Naegele\'s rule (280 days from the first day of your last period, adjusted for cycle length). Only about 1 in 20 babies arrives on the due date; your doctor will confirm with an ultrasound.</p>';
    },
    sleep: function (f) {
      var t = f.elements.wake && f.elements.wake.value; if (!t) return empty;
      var p = t.split(":"), wake = (+p[0]) * 60 + (+p[1]), out = [];
      [6, 5, 4].forEach(function (cyc) {
        var m = wake - cyc * 90 - 15; m = ((m % 1440) + 1440) % 1440;
        var h = Math.floor(m / 60), mm = m % 60, ap = h >= 12 ? "PM" : "AM", h12 = h % 12 || 12;
        out.push("<tr><td><b>" + h12 + ":" + (mm < 10 ? "0" : "") + mm + " " + ap + "</b></td><td>" + cyc + " cycles · " + fmt(cyc * 1.5, 1) + " h sleep" + (cyc === 5 ? " (good)" : cyc === 6 ? " (ideal)" : " (minimum)") + "</td></tr>");
      });
      return '<div class="label">Go to bed at one of these times</div><table class="prose">' + out.join("") + "</table>" +
        '<p class="small muted">Assumes about 15 minutes to fall asleep and 90-minute sleep cycles. Adults need 7 or more hours a night.</p>';
    },
    protein: function (f) {
      var w = num(f, "weight"), g = num(f, "goal") || 0.83; if (!(w > 20)) return empty;
      var need = w * g;
      return '<div class="big">' + fmt(need) + ' g</div><div class="label">Protein a day</div>' +
        "<p>Roughly: 1 katori cooked dal ≈ 7–9 g · 100 g paneer ≈ 18 g · 1 egg ≈ 6 g · 1 cup curd ≈ 8 g · 100 g chicken ≈ 25 g · 30 g roasted chana ≈ 6 g.</p>" +
        '<p class="small muted">0.83 g/kg is the ICMR-NIN requirement for healthy adults; active people, older adults and people losing weight often benefit from more. People with kidney disease should ask their doctor first.</p>';
    }
  };

  document.querySelectorAll("form[data-calc]").forEach(function (f) {
    var fn = calcs[f.getAttribute("data-calc")], out = document.getElementById(f.getAttribute("data-out") || "result");
    if (!fn || !out) return;
    var go = function () { out.innerHTML = fn(f); };
    f.addEventListener("input", go); f.addEventListener("change", go);
    f.addEventListener("submit", function (e) { e.preventDefault(); go(); });
    go();
  });

  /* Unit toggle for height (cm / ft-in) */
  document.querySelectorAll("[data-ftin]").forEach(function (box) {
    var f = box.closest("form"), cm = f.elements.height;
    box.querySelectorAll("input").forEach(function (i) {
      i.addEventListener("input", function () {
        var ft = parseFloat(box.querySelector("[name=ft]").value) || 0, inch = parseFloat(box.querySelector("[name=in]").value) || 0;
        if (ft) { cm.value = Math.round((ft * 12 + inch) * 2.54); cm.dispatchEvent(new Event("input", { bubbles: true })); }
      });
    });
  });

  /* Nirog Score: 12-question lifestyle and risk check */
  var sf = document.getElementById("score-form");
  if (sf) {
    var qs = sf.querySelectorAll(".q"), idx = 0, bar = document.getElementById("score-progress"), counter = document.getElementById("score-count");
    function show(n) {
      qs.forEach(function (q, j) { q.hidden = j !== n; }); idx = n;
      if (bar) bar.style.width = (n / qs.length * 100) + "%";
      if (counter) counter.textContent = "Question " + (n + 1) + " of " + qs.length;
      var b = document.getElementById("score-back"); if (b) b.hidden = n === 0;
    }
    sf.addEventListener("change", function (e) {
      if (e.target.type !== "radio") return;
      setTimeout(function () { if (idx < qs.length - 1) show(idx + 1); else finish(); }, 180);
    });
    var back = document.getElementById("score-back"); if (back) back.addEventListener("click", function () { if (idx > 0) show(idx - 1); });
    function finish() {
      var total = 0, max = 0, flags = [];
      qs.forEach(function (q) {
        var c = q.querySelector("input:checked"), opts = q.querySelectorAll("input");
        var hi = 0; opts.forEach(function (o) { hi = Math.max(hi, +o.value); }); max += hi;
        if (c) { total += +c.value; if (+c.value <= hi * 0.34 && q.getAttribute("data-tip")) flags.push(q.getAttribute("data-tip")); }
      });
      var score = Math.round(total / max * 100), cls, lab;
      if (score >= 80) { cls = "ok"; lab = "Strong foundations"; } else if (score >= 60) { cls = "info"; lab = "Good, with room to improve"; } else if (score >= 40) { cls = "warn"; lab = "Several risks to work on"; } else { cls = "err"; lab = "Time for a proper check-up"; }
      sf.hidden = true; if (bar) bar.style.width = "100%"; if (counter) counter.textContent = "Done";
      var r = document.getElementById("score-result"); r.hidden = false;
      document.getElementById("score-num").textContent = score;
      document.querySelector("#score-result .score-ring").style.setProperty("--p", score);
      document.getElementById("score-label").innerHTML = pill(cls, lab);
      document.getElementById("score-tips").innerHTML = (flags.length ? flags.slice(0, 5) : ["Keep doing what you're doing, and book a yearly preventive check-up."]).map(function (t) { return "<li>" + t + "</li>"; }).join("");
      var hid = document.getElementById("score-hidden"); if (hid) hid.value = score + "/100 (" + lab + "); focus: " + flags.slice(0, 5).map(function (t) { return t.replace(/<[^>]+>/g, ""); }).join(" | ");
      r.scrollIntoView({ behavior: "smooth", block: "start" });
    }
    show(0);
  }
})();
