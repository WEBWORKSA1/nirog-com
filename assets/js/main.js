/* Nirog.com core interactions */
(function () {
  "use strict";
  var S = window.SITE || {};
  var store = {
    get: function (k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
    set: function (k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
  };
  var root = document.documentElement;

  /* Theme */
  var saved = store.get("nirog-theme");
  if (saved) root.setAttribute("data-theme", saved);
  document.querySelectorAll("[data-theme-toggle]").forEach(function (b) {
    b.addEventListener("click", function () {
      var dark = root.getAttribute("data-theme") === "dark" ||
        (!root.getAttribute("data-theme") && window.matchMedia("(prefers-color-scheme: dark)").matches);
      var next = dark ? "light" : "dark";
      root.setAttribute("data-theme", next); store.set("nirog-theme", next);
    });
  });

  /* Mobile menu */
  var mb = document.querySelector(".menu-btn"), nav = document.getElementById("nav");
  if (mb && nav) mb.addEventListener("click", function () {
    var open = nav.classList.toggle("open"); mb.setAttribute("aria-expanded", open);
  });

  document.querySelectorAll("[data-year]").forEach(function (n) { n.textContent = new Date().getFullYear(); });

  /* Consent */
  function npa() { (window.adsbygoogle = window.adsbygoogle || []).requestNonPersonalizedAds = 1; }
  var c = document.getElementById("consent");
  if (c && !store.get("nirog-consent")) {
    c.hidden = false;
    c.querySelectorAll("[data-consent]").forEach(function (b) {
      b.addEventListener("click", function () {
        store.set("nirog-consent", b.getAttribute("data-consent"));
        if (b.getAttribute("data-consent") === "essential") npa();
        c.hidden = true;
      });
    });
  }
  if (store.get("nirog-consent") === "essential") npa();

  /* Sticky mobile CTA after scrolling */
  var sc = document.querySelector(".sticky-cta");
  if (sc) {
    document.body.classList.add("has-sticky");
    var onS = function () { sc.classList.toggle("show", window.scrollY > 600); };
    window.addEventListener("scroll", onS, { passive: true }); onS();
  }

  /* Form relay: address assembled at runtime, never present in markup */
  function relay() {
    var k = S._k || [];
    var rev = function (b) { return atob(b).split("").reverse().join(""); };
    return "https://formsubmit.co/ajax/" + rev(k[0]) + String.fromCharCode(64) + rev(k[1]);
  }
  window.NIROG_RELAY = relay;

  /* Prefill from query string (e.g. ?need=parents) */
  var qs = new URLSearchParams(location.search);
  qs.forEach(function (v, k) {
    document.querySelectorAll('[name="' + k + '"]').forEach(function (el) {
      if (el.type === "radio" || el.type === "checkbox") { if (el.value === v) el.checked = true; }
      else if (!el.value) el.value = v;
    });
  });

  /* Multi-step forms */
  document.querySelectorAll("form[data-steps]").forEach(function (f) {
    var steps = f.querySelectorAll(".step"), bars = f.querySelectorAll(".steps-bar i"), i = 0;
    function show(n) {
      steps.forEach(function (s, j) { s.hidden = j !== n; });
      bars.forEach(function (b, j) { b.classList.toggle("on", j <= n); });
      i = n;
      var first = steps[n].querySelector("input,select,textarea"); if (first && n > 0) first.focus();
    }
    f.querySelectorAll("[data-next]").forEach(function (b) {
      b.addEventListener("click", function () {
        var ok = true, st = f.querySelector(".form-status");
        steps[i].querySelectorAll("[required]").forEach(function (el) { if (!el.checkValidity()) { if (ok) el.reportValidity(); ok = false; } });
        var group = steps[i].querySelector("[data-need-one]");
        if (ok && group && !group.querySelector("input:checked")) { ok = false; if (st) { st.className = "form-status err"; st.textContent = "Pick at least one option to continue."; } }
        if (ok) { if (st) st.textContent = ""; show(i + 1); }
      });
    });
    f.querySelectorAll("[data-prev]").forEach(function (b) { b.addEventListener("click", function () { show(i - 1); }); });
    show(0);
  });

  /* All forms post to the relay */
  document.querySelectorAll("form[data-form]").forEach(function (f) {
    f.addEventListener("submit", function (e) {
      e.preventDefault();
      var status = f.querySelector(".form-status"), btn = f.querySelector("[type=submit]");
      var hp = f.querySelector(".hp input"); if (hp && hp.value) return;
      var data = {};
      new FormData(f).forEach(function (v, k) {
        if (k === "_hp") return;
        data[k] = data[k] ? data[k] + ", " + v : v;
      });
      data._subject = "Nirog.com — " + f.getAttribute("data-form") + (data.name ? " from " + data.name : "");
      data._template = "table"; data._captcha = "false";
      data.page = location.href;
      if (typeof f._extra === "function") Object.assign(data, f._extra());
      if (btn) { btn.disabled = true; btn.dataset.label = btn.textContent; btn.textContent = "Sending…"; }
      if (status) { status.className = "form-status"; status.textContent = ""; }
      fetch(relay(), { method: "POST", headers: { "Content-Type": "application/json", "Accept": "application/json" }, body: JSON.stringify(data) })
        .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
        .then(function () {
          var go = f.getAttribute("data-redirect");
          if (go) { location.href = go; return; }
          if (status) { status.className = "form-status ok"; status.textContent = f.getAttribute("data-ok") || "Thank you. We'll get back to you within two business days."; }
          f.reset();
        })
        .catch(function () {
          if (status) { status.className = "form-status err"; status.textContent = "That didn't go through. Check your connection and try again, or use the contact page."; }
        })
        .finally(function () { if (btn) { btn.disabled = false; btn.textContent = btn.dataset.label; } });
    });
  });

  /* Lite YouTube embeds: nothing loads from YouTube until the visitor clicks */
  document.querySelectorAll("[data-yt]").forEach(function (b) {
    var id = b.getAttribute("data-yt");
    b.style.backgroundImage = "url(https://i.ytimg.com/vi/" + id + "/hqdefault.jpg)";
    b.addEventListener("click", function () {
      var fr = document.createElement("iframe");
      fr.src = "https://www.youtube-nocookie.com/embed/" + id + "?autoplay=1&rel=0";
      fr.title = b.getAttribute("aria-label") || "Video";
      fr.className = "yt-frame";
      fr.allow = "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture";
      fr.allowFullscreen = true;
      b.replaceWith(fr);
    });
  });

  /* Support page: tiers + payment links */
  var tiers = document.querySelectorAll(".tier");
  if (tiers.length) {
    var amt = document.getElementById("amount");
    tiers.forEach(function (t) {
      t.addEventListener("click", function () {
        tiers.forEach(function (x) { x.setAttribute("aria-pressed", "false"); });
        t.setAttribute("aria-pressed", "true");
        if (amt) amt.value = t.getAttribute("data-amount");
      });
    });
  }
  var p = S.payments || {}, box = document.getElementById("pay-links");
  if (box) {
    var links = [["razorpay", "Give by UPI / card (Razorpay)"], ["paypal", "Give with PayPal"], ["stripe", "Give by card (Stripe)"], ["buymeacoffee", "Buy us a chai"]];
    var any = false;
    if (p.upi) {
      any = true; var u = document.createElement("a");
      u.href = "upi://pay?pa=" + encodeURIComponent(p.upi) + "&pn=Nirog&cu=INR&tn=Support%20Nirog";
      u.className = "btn primary"; u.textContent = "Pay by UPI app"; box.appendChild(u);
    }
    links.forEach(function (l) {
      if (p[l[0]]) { any = true; var a = document.createElement("a"); a.href = p[l[0]]; a.className = "btn brand"; a.target = "_blank"; a.rel = "noopener"; a.textContent = l[1]; box.appendChild(a); }
    });
    var n = document.getElementById(any ? "pay-note" : "pledge-note"); if (n) n.hidden = false;
  }

  /* Filter buttons (guides, tools, videos) */
  document.querySelectorAll("[data-filter-group]").forEach(function (g) {
    var target = document.querySelector(g.getAttribute("data-filter-group"));
    g.querySelectorAll("button").forEach(function (b) {
      b.addEventListener("click", function () {
        g.querySelectorAll("button").forEach(function (x) { x.setAttribute("aria-pressed", "false"); });
        b.setAttribute("aria-pressed", "true");
        var v = b.getAttribute("data-filter");
        target.querySelectorAll("[data-cat]").forEach(function (el) {
          el.hidden = !(v === "all" || el.getAttribute("data-cat") === v);
        });
      });
    });
  });

  /* Site search */
  var sf = document.getElementById("site-search");
  if (sf) {
    var out = document.getElementById("search-results"), input = sf.querySelector("input"), idx = null;
    var base = sf.getAttribute("data-base") || "";
    function run() {
      var q = (input.value || "").trim().toLowerCase();
      if (!q) { out.innerHTML = ""; return; }
      var terms = q.split(/\s+/);
      var hits = idx.map(function (d) {
        var hay = (d.t + " " + d.d + " " + d.k).toLowerCase(), s = 0;
        terms.forEach(function (t) { if (hay.indexOf(t) > -1) s += (d.t.toLowerCase().indexOf(t) > -1 ? 3 : 1); });
        return { d: d, s: s };
      }).filter(function (h) { return h.s > 0; }).sort(function (a, b) { return b.s - a.s; }).slice(0, 20);
      out.innerHTML = hits.length ? hits.map(function (h) {
        return '<a href="' + base + h.d.u + '"><b>' + h.d.t + '</b><span>' + h.d.d + '</span></a>';
      }).join("") : '<p class="muted">No matches. Try a simpler word like "sugar", "BP" or "insurance".</p>';
    }
    fetch(base + "search-index.json").then(function (r) { return r.json(); }).then(function (j) {
      idx = j; if (qs.get("q")) { input.value = qs.get("q"); run(); }
    });
    sf.addEventListener("submit", function (e) { e.preventDefault(); if (idx) run(); });
    input.addEventListener("input", function () { if (idx) run(); });
  }
})();
