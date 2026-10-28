"""Page copy and layouts for Nirog.com (everything except guides)."""
import json, os, re
from tools_data import TOOLS

def build(G, guides):
    emit, icon, hp, esc = G["emit"], G["icon"], G["hp"], G["esc"]
    crumbs, faq_html, faq_ld, bld, guide_card = G["crumbs"], G["faq_html"], G["faq_ld"], G["breadcrumb_ld"], G["guide_card"]
    BASE_URL, B, ROOT, OWNER = G["BASE_URL"], G["B"], G["ROOT"], G["OWNER_URL"]
    videos = json.load(open(os.path.join(B, "videos.json"), encoding="utf-8"))
    TJS = '<script src="%sassets/js/tools.js" defer></script>'
    CONSENT_TXT = ('I agree that Nirog.com and its partner advisors (licensed insurance intermediaries, diagnostic labs or clinics) may contact me by call, SMS, WhatsApp or email about my request, '
                   'and I accept the <a href="%sprivacy.html" target="_blank">privacy policy</a>. This overrides any DND registration for this request only. I can withdraw consent at any time.')

    def yt(v, R=""):
        return ('<div class="card" data-cat="%s" style="padding:14px"><button class="yt" type="button" data-yt="%s" aria-label="Play: %s"></button>'
                '<p style="margin:12px 4px 2px"><b>%s</b></p><p class="small muted" style="margin:0 4px 4px">%s · %s</p></div>'
                % (re.sub(r"[^a-z]+", "-", v["topic"].lower()).strip("-"), v["id"], esc(v["title"]), esc(v["title"]), esc(v["channel"]), esc(v["summary"])))

    def tile(href, ic, title, text):
        return '<a class="tile" href="%s"><span class="ic">%s</span><strong>%s</strong><span>%s</span></a>' % (href, icon(ic), title, text)

    def need_choices(name="need"):
        opts = [("insurance", "New health insurance", "shield"), ("parents", "Insurance for parents / seniors", "users"), ("renew", "Port, renew or compare my policy", "clock"),
                ("claim", "Help with a claim or rejection", "hand"), ("checkup", "Preventive health check-up", "heart"), ("doctor", "Talk to a doctor / second opinion", "phone"),
                ("corporate", "Employee / corporate wellness", "megaphone")]
        return ('<div class="choices" data-need-one>' + "".join(
            '<label class="choice"><input type="radio" name="%s" value="%s" required><span>%s %s</span></label>' % (name, v, icon(i).replace("<svg", '<svg width="20" height="20" style="flex:none"'), t) for v, t, i in opts) + "</div>")

    # ---------- Tools ----------
    tool_cats = {"body": "Body & weight", "risk": "Risk checks", "food": "Food & water", "fitness": "Fitness & sleep", "money": "Health insurance", "family": "Family"}
    for t in TOOLS:
        others = "".join(tile(o["slug"] + ".html", o["icon"], o["name"], o["short"]) for o in [x for x in TOOLS if x["slug"] != t["slug"]][:3])
        body = f'''<div class="wrap">{crumbs("../", [("tools/index.html", "Tools"), ("", t["name"])])}
<div class="section-head" style="margin-bottom:24px"><span class="eyebrow">Free health tool</span><h1>{esc(t["title"])}</h1><p class="muted">{esc(t["desc"])}</p></div>
<div class="tool"><form class="card form" data-calc="x" id="calc" novalidate>{t["form"]}<p class="small muted" style="margin:0">{icon("lock").replace("<svg", '<svg width="14" height="14" style="display:inline;vertical-align:-2px"')} Private: calculated in your browser. Nothing is stored or sent.</p></form>
<div class="result" id="result" aria-live="polite"></div></div>
<div class="article-grid" style="margin-top:48px"><article class="prose"><h2>How it works</h2>{t["about"]}
<h2>Frequently asked questions</h2>{faq_html(t["faqs"])}
<div class="callout small" style="margin-top:2em"><b>Note:</b> This tool gives general estimates for healthy adults. It is not medical advice or a diagnosis. Talk to a doctor about your own results.</div></article>
<aside class="aside"><div class="lead-box"><b>Get a free preventive health plan</b><p class="small muted">Tell us your age and concerns; an advisor suggests the right tests and, if you want, unbiased insurance options.</p><a class="btn primary sm" href="../get-advice.html">Get free advice</a></div></aside></div>
<section><h2>More free tools</h2><div class="grid g3">{others}</div></section></div>'''
        emit("tools/%s.html" % t["slug"], t["title"], t["desc"], body, active="tools", extra_js=TJS % "../",
             schema=[{"@context": "https://schema.org", "@type": "WebApplication", "name": t["name"], "url": BASE_URL + "tools/%s.html" % t["slug"],
                      "applicationCategory": "HealthApplication", "operatingSystem": "Any", "offers": {"@type": "Offer", "price": "0", "priceCurrency": "INR"}},
                     faq_ld(t["faqs"]), bld([("", "Home"), ("tools/index.html", "Tools"), ("tools/%s.html" % t["slug"], t["name"])])])
    # map calc ids: data-calc uses keys in tools.js
    CALC_KEYS = {"bmi-calculator": "bmi", "calorie-calculator": "calories", "diabetes-risk-score": "idrs", "blood-pressure-checker": "bp",
                 "health-insurance-cover-calculator": "cover", "waist-to-height-ratio": "whtr", "ideal-weight-calculator": "idealweight",
                 "water-intake-calculator": "water", "heart-rate-zones": "heartrate", "protein-calculator": "protein", "due-date-calculator": "duedate", "sleep-calculator": "sleep"}
    for slug, key in CALC_KEYS.items():
        p = "tools/%s.html" % slug
        G["OUT"][p] = re.sub(r'data-calc="[^"]*"', 'data-calc="%s"' % key, G["OUT"][p], count=1)

    tfilt = '<button type="button" data-filter="all" aria-pressed="true">All</button>' + "".join('<button type="button" data-filter="%s" aria-pressed="false">%s</button>' % (k, v) for k, v in tool_cats.items())
    tcards = "".join('<a class="tile" data-cat="%s" href="%s.html"><span class="ic">%s</span><strong>%s</strong><span>%s</span></a>' % (t["cat"], t["slug"], icon(t["icon"]), t["name"], t["short"]) for t in TOOLS)
    emit("tools/index.html", "Free Health Calculators & Tools for India", "12 free, private health calculators: BMI with Asian cut-offs, diabetes risk score, BP checker, calories, protein, health insurance cover and more.",
         f'''<div class="wrap">{crumbs("../", [("", "Tools")])}<div class="section-head"><span class="eyebrow">Free · private · instant</span><h1>Health tools built for Indian bodies and budgets</h1>
<p class="muted">Every calculator runs in your browser: nothing you type is stored or sent. Where Indian guidelines differ from global ones (like BMI cut-offs), we use the Indian ones.</p></div>
<div class="filters" data-filter-group="#tool-list">{tfilt}</div><div class="grid g3" id="tool-list">{tcards}
<a class="tile" data-cat="risk" href="../nirog-score.html"><span class="ic">{icon("leaf")}</span><strong>Nirog Score</strong><span>Our 12-question lifestyle and risk check with a personal action list.</span></a></div></div>''',
         active="tools", schema=bld([("", "Home"), ("tools/index.html", "Tools")]))

    # ---------- Nirog Score ----------
    Q = [("How old are you?", None, [("Under 30", 3), ("30–44", 2), ("45–59", 1), ("60 or older", 0)]),
         ("How is your waist? (women under 80 cm / men under 90 cm is healthy)", "Bring your waist down: aim for less than half your height. Try the <a href='tools/waist-to-height-ratio.html'>waist-to-height tool</a>.", [("In the healthy range", 3), ("A little over", 1), ("Well over / not sure", 0)]),
         ("How many days a week do you get 30+ minutes of brisk activity?", "Build up to 150 minutes of brisk activity a week; a daily 30-minute walk counts.", [("5 or more", 3), ("3–4", 2), ("1–2", 1), ("Rarely", 0)]),
         ("How many hours do you usually sleep?", "Protect 7–8 hours of sleep with a fixed wake-up time. See our <a href='guides/better-sleep.html'>sleep guide</a>.", [("7–9 hours", 3), ("6–7 hours", 2), ("Less than 6", 0), ("More than 9", 1)]),
         ("How many servings of fruit and vegetables do you eat a day?", "Fill half your plate with vegetables and add 1–2 fruits daily.", [("5 or more", 3), ("3–4", 2), ("1–2", 1), ("Hardly any", 0)]),
         ("Do you use tobacco (cigarettes, bidi, gutka, khaini)?", "Quitting tobacco is the single biggest health win. Free help: National Tobacco Quitline 1800-112-356.", [("Never", 3), ("Quit over a year ago", 2), ("Occasionally", 1), ("Daily", 0)]),
         ("How often do you drink alcohol?", "Cut down on alcohol: no amount is risk-free, and less is always better for your liver and heart.", [("Never or rarely", 3), ("1–2 times a week", 2), ("3–5 times a week", 1), ("Most days", 0)]),
         ("How stressed do you feel most weeks?", "Make time for stress relief: breathing exercises, yoga, time outdoors and talking to someone you trust. Tele-MANAS: 14416.", [("Rarely stressed", 3), ("Sometimes", 2), ("Often", 1), ("Almost always", 0)]),
         ("When did you last check your blood pressure?", "Check your blood pressure: it is free at most pharmacies and health centres. Use our <a href='tools/blood-pressure-checker.html'>BP checker</a>.", [("Within 1 year and it was normal", 3), ("Within 1 year, it was high", 1), ("More than a year ago", 1), ("Never / don't know", 0)]),
         ("When did you last test your blood sugar (fasting or HbA1c)?", "Get a fasting glucose or HbA1c test. Start with our <a href='tools/diabetes-risk-score.html'>diabetes risk score</a>.", [("Within 1 year and normal", 3), ("Within 1 year, it was high", 1), ("More than a year ago", 1), ("Never / don't know", 0)]),
         ("Does a parent or sibling have diabetes, heart disease or stroke?", "With a family history, start screening earlier and repeat it every year. See <a href='guides/preventive-health-checkup-by-age.html'>check-ups by age</a>.", [("No", 3), ("One of these", 1), ("More than one", 0), ("Not sure", 1)]),
         ("Do you have health insurance that would cover a ₹5 lakh+ hospital bill?", "Protect your family's savings with adequate health insurance. Try the <a href='tools/health-insurance-cover-calculator.html'>cover calculator</a>.", [("Yes, personal + employer cover", 3), ("Only employer cover", 1), ("A small policy", 1), ("No cover", 0)])]
    qhtml = ""
    for i, (q, tip, opts) in enumerate(Q):
        ch = "".join('<label class="choice"><input type="radio" name="q%d" value="%d"><span>%s</span></label>' % (i, v, t) for t, v in opts)
        qhtml += '<fieldset class="q" style="border:0;padding:0;margin:0"%s><legend class="step-title">%s</legend><div class="choices" style="margin-top:14px">%s</div></fieldset>' % (' data-tip="%s"' % tip.replace('"', "&quot;") if tip else "", q, ch)
    score_body = f'''<div class="wrap narrow">{crumbs("", [("", "Nirog Score")])}
<div class="section-head"><span class="eyebrow">2-minute health check</span><h1>Your Nirog Score</h1><p class="muted">Twelve quick questions about your habits, history and protection. You'll get a score out of 100 and a short, personal action list. Private: answers stay in your browser unless you choose to send them.</p></div>
<div class="card"><p class="small muted" id="score-count" style="margin:0 0 6px">Question 1 of 12</p><div class="progress" style="margin-bottom:22px"><i id="score-progress" style="width:0"></i></div>
<form id="score-form">{qhtml}</form><button class="btn ghost sm" type="button" id="score-back" hidden style="margin-top:18px">← Back</button>
<div id="score-result" hidden><div class="split" style="align-items:center"><div class="center"><div class="score-ring"><div><span><b id="score-num">0</b><small>out of 100</small></span></div></div><div id="score-label"></div></div>
<div><h2 style="font-size:1.5rem">Your top actions</h2><ol id="score-tips" class="prose"></ol></div></div>
<hr><div class="lead-box"><h3>Get your free personalised check-up plan</h3><p class="small muted">An advisor reviews your score and suggests which tests to do first, where to get them at a fair price, and whether your insurance is enough. Free, no obligation.</p>
<form class="form" data-form="Nirog Score lead" data-redirect="thank-you.html"><input type="hidden" name="nirog_score" id="score-hidden"><input type="hidden" name="need" value="checkup">
<div class="row2"><div class="field"><label for="s-name">Name</label><input id="s-name" name="name" required autocomplete="name"></div><div class="field"><label for="s-phone">Mobile</label><input id="s-phone" type="tel" name="phone" required pattern="[0-9+ ]{{10,15}}" autocomplete="tel" placeholder="10-digit mobile"></div></div>
<div class="row2"><div class="field"><label for="s-city">City</label><input id="s-city" name="city" required autocomplete="address-level2"></div><div class="field"><label for="s-email">Email (optional)</label><input id="s-email" type="email" name="email" autocomplete="email"></div></div>
<label class="check"><input type="checkbox" name="consent" value="yes" required><span>{CONSENT_TXT % ""}</span></label>{hp()}
<button class="btn primary" type="submit">Send me my free plan</button><p class="form-status" role="status"></p></form></div>
<p class="small muted" style="margin-top:16px">The Nirog Score is an educational self-check, not a medical test or diagnosis. <a href="nirog-score.html">Retake</a></p></div></div></div>'''
    emit("nirog-score.html", "Nirog Score: Free 2-Minute Health Risk Check", "Take the free Nirog Score: 12 quick questions on habits, screening and protection. Get a score out of 100 and a personal action list.", score_body, active="score", extra_js=TJS % "")

    # ---------- Get advice (lead generation) ----------
    adv_faq = [("Is the advice really free?", "Yes. You pay nothing for advice. If you choose to buy a policy or book a test through a partner, the partner may pay us a referral fee; it never changes the price you pay."),
               ("Who will contact me?", "A Nirog advisor or a vetted partner: an IRDAI-licensed insurance intermediary for insurance requests, or a NABL-accredited lab or registered clinic for check-ups. We share your details only for the request you make."),
               ("Will I get spam calls?", "No. We contact you only about your request, at the time you choose, and you can opt out at any time. We never sell your data to random call centres."),
               ("Do you recommend one insurer over another?", "We compare features such as room-rent limits, co-pay, waiting periods and network hospitals against your needs. We don't push a single company.")]
    adv_body = f'''<section class="hero" style="padding-bottom:24px"><div class="wrap"><div class="hero-grid" style="align-items:start">
<div><span class="eyebrow">Free · independent · 60 seconds</span><h1>Get unbiased help with <em>health insurance</em> and check-ups</h1>
<p class="lede">Tell us what you need. A real advisor will call you back with clear options: the right cover for your family, the right tests for your age, at a fair price. No pressure, no jargon.</p>
<ul class="list-check" style="margin-top:22px"><li>Compare policies on what matters: room rent, co-pay, waiting periods, network hospitals</li><li>Cover for parents and seniors, including pre-existing conditions</li><li>Help porting a policy or fighting a rejected claim</li><li>Preventive check-up packages from accredited labs, with home sample collection</li></ul>
<div class="trust-row"><span>{icon("lock")} Your data stays private</span><span>{icon("check")} No spam, ever</span><span>{icon("shield")} Licensed partners only</span></div></div>
<div class="lead-box" id="form"><form class="form" data-form="Lead: free advice" data-steps data-redirect="thank-you.html">
<div class="steps-bar" aria-hidden="true"><i></i><i></i><i></i></div>
<div class="step"><p class="step-title">What can we help with?</p>{need_choices()}<button class="btn primary" type="button" data-next>Continue</button></div>
<div class="step" hidden><p class="step-title">Who needs cover or care?</p>
<div class="choices"><label class="choice"><input type="checkbox" name="members" value="Self"><span>Me</span></label><label class="choice"><input type="checkbox" name="members" value="Spouse"><span>Spouse</span></label><label class="choice"><input type="checkbox" name="members" value="Children"><span>Children</span></label><label class="choice"><input type="checkbox" name="members" value="Parents"><span>Parents</span></label></div>
<div class="row2"><div class="field"><label for="a-age">Age of eldest person</label><input id="a-age" type="number" name="eldest_age" min="0" max="110" required></div><div class="field"><label for="a-city">City / pincode</label><input id="a-city" name="city" required autocomplete="postal-code"></div></div>
<div class="field"><label for="a-ped">Any existing conditions?</label><select id="a-ped" name="conditions"><option>None</option><option>Diabetes</option><option>High BP</option><option>Thyroid</option><option>Heart condition</option><option>More than one</option><option>Prefer to discuss on call</option></select></div>
<div class="field"><label for="a-budget">Yearly budget (optional)</label><select id="a-budget" name="budget"><option value="">Not sure</option><option>Under ₹10,000</option><option>₹10,000–25,000</option><option>₹25,000–50,000</option><option>Over ₹50,000</option></select></div>
<div class="btn-row"><button class="btn ghost" type="button" data-prev>Back</button><button class="btn primary" type="button" data-next>Continue</button></div></div>
<div class="step" hidden><p class="step-title">Where should we reach you?</p>
<div class="field"><label for="a-name">Full name</label><input id="a-name" name="name" required autocomplete="name"></div>
<div class="row2"><div class="field"><label for="a-phone">Mobile number</label><input id="a-phone" type="tel" name="phone" required pattern="[0-9+ ]{{10,15}}" placeholder="10-digit mobile" autocomplete="tel"></div>
<div class="field"><label for="a-time">Best time to call</label><select id="a-time" name="call_time"><option>Anytime</option><option>Morning (9–12)</option><option>Afternoon (12–4)</option><option>Evening (4–8)</option></select></div></div>
<div class="field"><label for="a-email">Email (optional)</label><input id="a-email" type="email" name="email" autocomplete="email"></div>
<label class="check"><input type="checkbox" name="whatsapp" value="yes" checked><span>Send updates on WhatsApp</span></label>
<label class="check"><input type="checkbox" name="consent" value="yes" required><span>{CONSENT_TXT % ""}</span></label>{hp()}
<div class="btn-row"><button class="btn ghost" type="button" data-prev>Back</button><button class="btn primary" type="submit">Get my free advice</button></div></div>
<p class="form-status" role="status"></p></form>
<div class="badges"><span>100% free</span><span>Reply within 1 business day</span><span>Opt out anytime</span></div></div></div></div></section>
<section class="band"><div class="wrap"><div class="section-head center"><h2>How it works</h2></div><ol class="howto grid g3">
<li><h3>Tell us your need</h3><p class="muted">Three short steps. No documents, no payment.</p></li>
<li><h3>Talk to an advisor</h3><p class="muted">We call at your chosen time and explain options in plain language, in English or Hindi.</p></li>
<li><h3>Decide in your own time</h3><p class="muted">Compare, ask questions, take a written summary. Buy only if it is right for you.</p></li></ol></div></section>
<section><div class="wrap split"><div><h2>Before you decide, read these</h2><div class="grid" style="gap:12px">{"".join(guide_card(g, "") for g in guides if g["cat"] == "insurance")}</div></div>
<div><h2>Questions people ask</h2>{faq_html(adv_faq)}<p class="small muted" style="margin-top:18px">Nirog.com is an information and referral platform. We are not an insurer or a medical provider. Insurance is solicited only by IRDAI-licensed partners; read the policy wording before you buy.</p></div></div></section>'''
    emit("get-advice.html", "Free Health Insurance & Check-up Advice", "Get free, unbiased help choosing health insurance, covering parents, fixing claims or booking a preventive check-up in India. Takes 60 seconds.", adv_body, active="advice", schema=faq_ld(adv_faq), sticky=False)

    # ---------- Home ----------
    feat_tools = ["bmi-calculator", "diabetes-risk-score", "blood-pressure-checker", "health-insurance-cover-calculator", "calorie-calculator", "waist-to-height-ratio", "protein-calculator", "sleep-calculator"]
    tm = {t["slug"]: t for t in TOOLS}
    ttiles = "".join(tile("tools/%s.html" % s, tm[s]["icon"], tm[s]["name"], tm[s]["short"]) for s in feat_tools)
    gcards = "".join(guide_card(g, "") for g in guides[:6])
    vcards = "".join(yt(v) for v in videos[:3])
    home_faq = [("What does “nirog” mean?", "Nirog is a Hindi and Sanskrit word meaning free of disease, or healthy. That is our goal for every reader: prevention first, so fewer people need hospital care."),
                ("Is Nirog.com free?", "Yes. All guides, tools and the Nirog Score are free. We are funded by advertising, reader support and partner referral fees, which never change what you pay."),
                ("Can Nirog.com diagnose my condition?", "No. We provide general, evidence-based information and tools. Only a qualified doctor who examines you can diagnose and treat a condition."),
                ("How do you choose what to publish?", "We write from authoritative sources such as WHO, ICMR, MoHFW, NHS and peer-reviewed research, list every source, and update guides when guidance changes. Read our editorial policy.")]
    home = f'''<section class="hero"><div class="wrap hero-grid">
<div><span class="eyebrow">Preventive health for India</span><h1>Stay <em>nirog</em>. Catch problems before they become disease.</h1>
<p class="lede">Free health tools, plain-English guides and unbiased help with check-ups and health insurance, built around Indian bodies, food and budgets.</p>
<div class="btn-row" style="margin-top:24px"><a class="btn primary" href="nirog-score.html">Check my Nirog Score</a><a class="btn ghost" href="get-advice.html">Free insurance &amp; check-up advice</a></div>
<div class="trust-row"><span>{icon("check")} Evidence-based, sources listed</span><span>{icon("check")} Indian guidelines</span><span>{icon("check")} No paywall, no app needed</span></div></div>
<div class="score-card"><p class="eyebrow" style="margin:0">2-minute health check</p><h2 style="font-size:1.6rem;margin:.3em 0">How healthy are your habits?</h2>
<p class="muted small">Answer 12 quick questions and get a score out of 100 with your top 5 actions.</p>
<p style="font-weight:700;margin:18px 0 10px">Question 1: How many days a week do you get 30+ minutes of brisk activity?</p>
<div class="choices"><a class="choice" href="nirog-score.html"><span>5 or more</span></a><a class="choice" href="nirog-score.html"><span>3–4 days</span></a><a class="choice" href="nirog-score.html"><span>1–2 days</span></a><a class="choice" href="nirog-score.html"><span>Rarely</span></a></div>
<a class="btn brand" style="width:100%;margin-top:16px" href="nirog-score.html">Start the full check</a></div></div></section>
<section class="band-brand" style="padding:36px 0"><div class="wrap stats"><div class="stat"><b>12</b><span>free, private health calculators</span></div><div class="stat"><b>{len(guides)}</b><span>in-depth, sourced health guides</span></div><div class="stat"><b>₹0</b><span>cost for advice, tools and guides</span></div><div class="stat"><b>108 / 112</b><span>call these in any emergency</span></div></div></section>
<section><div class="wrap"><div class="section-head"><span class="eyebrow">Free tools</span><h2>Know your numbers in under a minute</h2><p class="muted">Calculators tuned to Indian guidelines, from Asian BMI cut-offs to the Indian Diabetes Risk Score.</p></div>
<div class="grid g4">{ttiles}</div><p style="margin-top:20px"><a href="tools/index.html">See all 12 tools →</a></p></div></section>
<section class="band"><div class="wrap split" style="align-items:center"><div><span class="eyebrow">Free advice, real people</span><h2>Health insurance is confusing. We make it simple.</h2>
<p class="muted">Room-rent caps, co-pays, waiting periods, sub-limits: the fine print decides whether your claim gets paid. Tell us about your family and an independent advisor will explain your options clearly. Check-up packages from accredited labs too.</p>
<ul class="list-check"><li>Family, parents and senior citizen cover</li><li>Porting, renewals and claim rejections</li><li>Preventive check-ups with home sample collection</li></ul></div>
<div class="lead-box"><form class="form" data-form="Lead: home quick form" data-redirect="thank-you.html"><p class="step-title" style="margin-top:0">Get a free callback</p>
<div class="field"><label for="h-need">I need help with</label><select id="h-need" name="need" required><option value="insurance">New health insurance</option><option value="parents">Insurance for parents / seniors</option><option value="renew">Port or renew my policy</option><option value="claim">A claim or rejection</option><option value="checkup">Preventive health check-up</option><option value="doctor">Doctor consultation</option></select></div>
<div class="row2"><div class="field"><label for="h-name">Name</label><input id="h-name" name="name" required autocomplete="name"></div><div class="field"><label for="h-phone">Mobile</label><input id="h-phone" type="tel" name="phone" required pattern="[0-9+ ]{{10,15}}" placeholder="10-digit mobile" autocomplete="tel"></div></div>
<div class="field"><label for="h-city">City</label><input id="h-city" name="city" required autocomplete="address-level2"></div>
<label class="check"><input type="checkbox" name="consent" value="yes" required><span>{CONSENT_TXT % ""}</span></label>{hp()}
<button class="btn primary" type="submit">Call me back, free</button><p class="form-status" role="status"></p></form>
<div class="badges"><span>Free</span><span>No spam</span><span>Licensed partners</span></div></div></div></section>
<section><div class="wrap"><div class="section-head"><span class="eyebrow">Health library</span><h2>Guides that answer the questions doctors don't have time for</h2></div>
<div class="grid g3">{gcards}</div><p style="margin-top:20px"><a href="guides/index.html">Browse all guides →</a></p></div></section>
<section class="band"><div class="wrap"><div class="section-head"><span class="eyebrow">Watch &amp; learn</span><h2>Short videos from trusted health experts</h2><p class="muted">Hand-picked from WHO, Mayo Clinic, Cleveland Clinic, the American Heart Association and India's national yoga institute.</p></div>
<div class="grid g3">{vcards}</div><p style="margin-top:20px"><a href="videos.html">See all videos →</a></p></div></section>
<section><div class="wrap"><div class="section-head center"><h2>Join the movement for a healthier India</h2></div><div class="grid g4">
{tile("contests.html", "gift", "Contests &amp; prizes", "Monthly health challenges with prizes for healthy habits.")}
{tile("support.html", "hand", "Support our mission", "Fund free tools, check-up camps and expert reviewers.")}
{tile("careers.html", "users", "Work with us", "Doctors, writers, video creators and advisors.")}
{tile("advertise.html", "megaphone", "Partner &amp; advertise", "Reach health-conscious Indian families.")}</div></div></section>
<section class="band"><div class="wrap split"><div><span class="eyebrow">Why trust Nirog.com</span><h2>Evidence first. No miracle cures.</h2>
<ul class="list-check"><li>Every guide lists its sources: WHO, ICMR, MoHFW, NHS and peer-reviewed research.</li><li>We follow Indian clinical guidelines where they differ from global ones.</li><li>We never sell "cures", and we flag when to see a doctor.</li><li>We tell you how we make money. Read our <a href="editorial-policy.html">editorial policy</a>.</li></ul></div>
<div><h2>Common questions</h2>{faq_html(home_faq)}</div></div></section>'''
    emit("index.html", "Nirog.com: Free Health Tools, Guides & Insurance Advice for India", "Stay nirog: free health calculators, evidence-based guides on diabetes, BP, thyroid and more, plus unbiased health insurance and check-up advice.", home,
         schema=[{"@context": "https://schema.org", "@type": "WebSite", "name": "Nirog.com", "url": BASE_URL,
                  "potentialAction": {"@type": "SearchAction", "target": BASE_URL + "search.html?q={search_term_string}", "query-input": "required name=search_term_string"}}, faq_ld(home_faq)])

    # ---------- Videos ----------
    topics = []
    for v in videos:
        if v["topic"] not in topics: topics.append(v["topic"])
    vf = '<button type="button" data-filter="all" aria-pressed="true">All</button>' + "".join('<button type="button" data-filter="%s" aria-pressed="false">%s</button>' % (re.sub(r"[^a-z]+", "-", t.lower()).strip("-"), esc(t)) for t in topics)
    emit("videos.html", "Health Videos from Trusted Experts", "Watch short, trusted health videos on diabetes, blood pressure, heart attack signs, CPR, yoga, sleep, stress and more from WHO, Mayo Clinic and others.",
         f'''<div class="wrap">{crumbs("", [("", "Videos")])}<div class="section-head"><span class="eyebrow">Video library</span><h1>Health videos worth your time</h1>
<p class="muted">Every video comes from an established medical or public-health publisher. Videos load from YouTube only when you press play (privacy-enhanced mode).</p></div>
<div class="filters" data-filter-group="#video-list">{vf}</div><div class="grid g3" id="video-list">{"".join(yt(v) for v in videos)}</div>
<section><div class="card split" style="align-items:center"><div><h2>Make health videos with us</h2><p class="muted">Doctors, dietitians, yoga teachers and creators: we're building a Hindi and English video series on prevention.</p></div><div class="btn-row"><a class="btn brand" href="careers.html">Apply as a creator</a><a class="btn ghost" href="advertise.html">Sponsor a series</a></div></div></section>
<p class="small muted">Videos are embedded from YouTube and remain the property of their publishers. Nirog.com is not affiliated with these publishers.</p></div>''', active="videos",
         schema={"@context": "https://schema.org", "@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": "https://www.youtube.com/watch?v=" + v["id"], "name": v["title"]} for i, v in enumerate(videos)]})

    # ---------- Support / donations ----------
    sup = f'''<section class="hero"><div class="wrap hero-grid"><div><span class="eyebrow">Support Nirog.com</span><h1>Help keep preventive health <em>free</em> for every Indian family</h1>
<p class="lede">Your support pays for running the site, awareness campaigns, expert medical reviewers, contest prizes and free community check-up camps. Every rupee is reported back to supporters.</p>
<ul class="list-check"><li><b>Operations</b>: hosting, tools, security and translation into Hindi and more languages</li><li><b>Promotion &amp; awareness</b>: campaigns in schools, workplaces and villages</li><li><b>Hiring talent</b>: doctors and dietitians who review every guide</li><li><b>Contests &amp; prizes</b>: rewards for healthy habits</li><li><b>Free check-up camps</b>: BP, sugar and anaemia screening where it's needed most</li></ul></div>
<div class="lead-box"><p class="step-title" style="margin-top:0">Choose an amount</p>
<div class="tiers"><button class="tier" type="button" data-amount="₹199" aria-pressed="false"><b>₹199</b><span>A chai for the team</span></button><button class="tier" type="button" data-amount="₹999" aria-pressed="true"><b>₹999</b><span>Funds one sugar test at a camp</span></button><button class="tier" type="button" data-amount="₹4,999" aria-pressed="false"><b>₹4,999</b><span>Funds one guide's medical review</span></button><button class="tier" type="button" data-amount="₹24,999" aria-pressed="false"><b>₹24,999</b><span>Sponsors a monthly contest</span></button></div>
<div id="pay-links" class="btn-row" style="margin-top:18px"></div><p id="pay-note" class="small muted" hidden>Payments open in a secure payment page. Then fill the form below so we can thank you and send a receipt.</p>
<p id="pledge-note" class="small muted" hidden style="margin-top:14px">Online checkout is being set up. Pledge below and we'll send you a secure UPI / card / bank payment link with a receipt.</p>
<form class="form" data-form="Donation pledge" data-redirect="thank-you.html?type=support" style="margin-top:12px">
<div class="row2"><div class="field"><label for="d-amt">Amount</label><input id="d-amt" name="amount" id="amount" value="₹999" required></div><div class="field"><label for="d-freq">Frequency</label><select id="d-freq" name="frequency"><option>One-time</option><option>Monthly</option><option>Yearly</option></select></div></div>
<div class="field"><label for="d-use">Direct my support to</label><select id="d-use" name="purpose"><option>Where it's needed most</option><option>Operations</option><option>Promotion &amp; awareness</option><option>Hiring medical reviewers</option><option>Contests &amp; prizes</option><option>Free check-up camps</option></select></div>
<div class="row2"><div class="field"><label for="d-name">Name</label><input id="d-name" name="name" required autocomplete="name"></div><div class="field"><label for="d-email">Email</label><input id="d-email" type="email" name="email" required autocomplete="email"></div></div>
<div class="field"><label for="d-msg">Message (optional)</label><input id="d-msg" name="message"></div>
<label class="check"><input type="checkbox" name="public_thanks" value="yes"><span>Thank me publicly on the supporters' wall</span></label>{hp()}
<button class="btn primary" type="submit">Pledge my support</button><p class="form-status" role="status"></p></form></div></div></section>
<section class="band"><div class="wrap"><div class="section-head"><h2>Other ways to help</h2></div><div class="grid g3">
<div class="card"><h3>Sponsor a check-up camp</h3><p class="muted">Companies, clinics and CSR teams can fund a full screening day in a community of their choice, with co-branding and an impact report.</p><a href="advertise.html#form">Talk to us →</a></div>
<div class="card"><h3>Volunteer your skills</h3><p class="muted">Doctors, nurses, translators, designers and developers: give a few hours a month and help us reach more people.</p><a href="careers.html">See open roles →</a></div>
<div class="card"><h3>Share Nirog.com</h3><p class="muted">Forward a guide or the Nirog Score to your family WhatsApp group. It costs nothing and may prompt a check-up that matters.</p><a href="nirog-score.html">Share the Nirog Score →</a></div></div>
<p class="small muted" style="margin-top:24px">Nirog.com is an independent website, not a registered charity; contributions are voluntary support for the project and are not tax-deductible unless stated on your receipt. Contributions are non-refundable except where the law requires.</p></div></section>'''
    emit("support.html", "Support Nirog.com: Donate to Keep Preventive Health Free", "Support Nirog.com with a one-time or monthly contribution. Fund free health tools, medical reviewers, awareness campaigns, contests and check-up camps.", sup, active="support")
    G["OUT"]["support.html"] = G["OUT"]["support.html"].replace('id="d-amt" name="amount" id="amount"', 'id="amount" name="amount"').replace('for="d-amt"', 'for="amount"')

    # ---------- Contests ----------
    contests = [("30-Day Walk India Challenge", "Fitness", "Walk at least 30 minutes a day for 30 days. Log your daily steps or minutes and share a weekly screenshot from any fitness app.", "Fitness bands, check-up vouchers and cash prizes up to ₹10,000"),
                ("Healthy Thali Photo Contest", "Food", "Cook a balanced Indian thali (half vegetables, a quarter protein, a quarter whole grains) and share a photo with the recipe.", "Kitchen vouchers, cookbooks and featured spots on Nirog.com"),
                ("Monthly Health Myth-Buster Quiz", "Knowledge", "Ten questions on everyday health myths. Highest score in the fastest time wins; ties go to a random draw.", "Gift vouchers and Nirog supporter merchandise"),
                ("Know Your Numbers Pledge", "Prevention", "Get your BP, sugar and waist checked this month and pledge to share the Nirog Score with three family members.", "Free preventive check-up packages for winners and a family member")]
    ccards = "".join('<div class="card"><span class="tag accent">%s</span><h3 style="margin-top:12px">%s</h3><p class="muted">%s</p><p class="small"><b>Prizes:</b> %s</p><a class="btn brand sm" href="#enter">Enter now</a></div>' % (c, t, d, p) for t, c, d, p in contests)
    rules = [("Who can enter?", "Residents of India aged 18 or over. Employees of Nirog.com and contest sponsors cannot win. Under-18s may join challenges for fun with a parent's consent but are not eligible for prizes."),
             ("Is there an entry fee?", "No. Entry is always free and no purchase is necessary. Contests are judged on skill and effort, not luck, except for tie-break draws."),
             ("How are winners chosen?", "Each contest lists its criteria. A panel judges creativity, healthfulness and consistency. Winners are announced on this page and contacted within 14 days of the contest closing."),
             ("Where do prizes come from?", "Prizes are funded by sponsors and reader support. The exact prizes for each season are published here before entries open, and they are never exchanged for cash unless stated."),
             ("What happens to my entry and data?", "We use your details only to run the contest. By entering, you allow us to feature your first name, city and entry on Nirog.com. Medical data is never requested or published.")]
    cbody = f'''<section class="hero"><div class="wrap"><div class="section-head"><span class="eyebrow">Contests &amp; prizes</span><h1>Build healthy habits. <em>Win</em> for it.</h1>
<p class="lede">Free monthly challenges that reward walking, cooking well, knowing your numbers and busting health myths. Season prizes are funded by sponsors and supporters.</p>
<div class="btn-row"><a class="btn primary" href="#enter">Enter a contest</a><a class="btn ghost" href="advertise.html">Sponsor prizes</a></div></div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="grid g2">{ccards}</div></div></section>
<section class="band" id="enter"><div class="wrap split"><div class="lead-box"><h2 style="margin-top:0">Enter this season</h2>
<form class="form" data-form="Contest entry" data-redirect="thank-you.html?type=contest">
<div class="field"><label for="c-contest">Contest</label><select id="c-contest" name="contest" required>{"".join("<option>%s</option>" % t for t, *_ in contests)}</select></div>
<div class="row2"><div class="field"><label for="c-name">Name</label><input id="c-name" name="name" required autocomplete="name"></div><div class="field"><label for="c-city">City</label><input id="c-city" name="city" required></div></div>
<div class="row2"><div class="field"><label for="c-email">Email</label><input id="c-email" type="email" name="email" required autocomplete="email"></div><div class="field"><label for="c-phone">Mobile</label><input id="c-phone" type="tel" name="phone" required pattern="[0-9+ ]{{10,15}}"></div></div>
<div class="field"><label for="c-link">Link to your entry (photo, video or screenshot)</label><input id="c-link" type="url" name="entry_link" placeholder="Google Drive, Instagram or YouTube link"><span class="hint">Leave blank for the quiz; we'll email you the link when it opens.</span></div>
<div class="field"><label for="c-note">Tell us about your entry</label><textarea id="c-note" name="description"></textarea></div>
<label class="check"><input type="checkbox" name="rules" value="accepted" required><span>I am 18+, live in India and accept the contest rules on this page.</span></label>{hp()}
<button class="btn primary" type="submit">Submit my entry</button><p class="form-status" role="status"></p></form></div>
<div><h2>Contest rules in brief</h2>{faq_html(rules)}</div></div></section>'''
    emit("contests.html", "Health Contests & Prizes: Monthly Challenges", "Join free monthly health contests on Nirog.com: 30-day walking challenge, healthy thali photo contest, myth-buster quiz and more. Win prizes.", cbody, active="contests", schema=faq_ld(rules))

    # ---------- Careers ----------
    roles = [("Medical reviewer (MBBS/MD)", "Freelance · Remote", "Review guides for accuracy against current Indian and international guidelines. 4–8 hours a month."),
             ("Dietitian / nutritionist reviewer", "Freelance · Remote", "Review food, weight and nutrition content; help design Indian meal plans."),
             ("Health writer (English / Hindi)", "Freelance · Remote", "Research and write clear, sourced guides. Science or health background preferred."),
             ("Video creator & editor", "Freelance · Remote", "Script, shoot or edit short health explainers for YouTube, Instagram and the site."),
             ("Insurance advisor (IRDAI-licensed POSP or broker)", "Partner · India", "Handle insurance leads with honest, needs-based advice. Commission-based partnership."),
             ("Community & partnerships manager", "Part-time · Remote", "Run contests, check-up camps and partnerships with clinics, labs and employers."),
             ("Front-end developer (volunteer or paid)", "Project · Remote", "Build new tools and improve speed and accessibility on a static stack."),
             ("Interns: public health, marketing, design", "Internship · Remote", "Real projects, a mentor and a certificate. Stipend for selected roles.")]
    rcards = "".join('<div class="card"><h3>%s</h3><p class="small"><span class="tag">%s</span></p><p class="muted">%s</p><a href="#apply" class="small">Apply →</a></div>' % r for r in roles)
    car = f'''<section class="hero"><div class="wrap"><div class="section-head"><span class="eyebrow">Careers</span><h1>Help millions of Indians stay <em>nirog</em></h1>
<p class="lede">We're a small, remote-first team building India's most useful preventive health resource. We value accuracy, clear writing and kindness to readers.</p></div>
<div class="grid g4">{rcards}</div></div></section>
<section class="band" id="apply"><div class="wrap narrow"><div class="lead-box"><h2 style="margin-top:0">Apply or express interest</h2>
<form class="form" data-form="Job application" data-redirect="thank-you.html?type=careers">
<div class="field"><label for="j-role">Role</label><select id="j-role" name="role" required>{"".join("<option>%s</option>" % r[0] for r in roles)}<option>Other / volunteer</option></select></div>
<div class="row2"><div class="field"><label for="j-name">Name</label><input id="j-name" name="name" required autocomplete="name"></div><div class="field"><label for="j-email">Email</label><input id="j-email" type="email" name="email" required autocomplete="email"></div></div>
<div class="row2"><div class="field"><label for="j-phone">Mobile</label><input id="j-phone" type="tel" name="phone"></div><div class="field"><label for="j-city">City</label><input id="j-city" name="city"></div></div>
<div class="field"><label for="j-quals">Qualifications / registration (e.g. MBBS, NMC/State Council reg., IRDAI licence)</label><input id="j-quals" name="qualifications"></div>
<div class="field"><label for="j-link">CV, LinkedIn or portfolio link</label><input id="j-link" type="url" name="cv_link" required placeholder="https://"></div>
<div class="field"><label for="j-why">Why Nirog.com? What would you do first?</label><textarea id="j-why" name="message" required></textarea></div>{hp()}
<button class="btn primary" type="submit">Send application</button><p class="form-status" role="status"></p></form></div>
<p class="small muted center" style="margin-top:16px">We never charge candidates any fee. Equal opportunity: we welcome applicants of every background.</p></div></section>'''
    emit("careers.html", "Careers at Nirog.com: Doctors, Writers, Creators", "Join Nirog.com: medical reviewers, dietitians, health writers, video creators, insurance advisors, developers and interns. Remote-first.", car)

    # ---------- Advertise / partner ----------
    pk = [("Lead partnerships", "Insurers, brokers, labs, hospitals and clinics: receive consented, verified leads for health insurance, check-ups and consultations on a cost-per-lead or revenue-share basis."),
          ("Sponsored tools &amp; series", "Sponsor a calculator, a guide series or a video series with clear 'sponsored' labelling. Editorial content stays independent."),
          ("Display &amp; newsletter", "Reach health-conscious readers through direct display placements and the weekly Nirog newsletter."),
          ("Contests &amp; prizes", "Fund a monthly challenge and put your brand in front of an engaged, action-taking audience."),
          ("CSR &amp; check-up camps", "Fund community screening camps with co-branding and a transparent impact report."),
          ("Acquire or invest", "Interested in the Nirog.com domain or the whole website? Reach the owner directly via the link at the top of every page.")]
    adv = f'''<section class="hero"><div class="wrap"><div class="section-head"><span class="eyebrow">Advertise · sponsor · partner</span><h1>Reach Indian families when they're making <em>health decisions</em></h1>
<p class="lede">Nirog.com readers come to check their risk, compare cover and book check-ups. Partner with us on transparent, policy-compliant terms.</p></div>
<div class="grid g3">{"".join('<div class="card"><h3>%s</h3><p class="muted">%s</p></div>' % x for x in pk)}</div>
<p class="small muted" style="margin-top:20px">Interested in this website, the domain name, sponsorship, advertisement or partnership? You can also <a href="{OWNER}" target="_blank" rel="noopener">contact the owner directly</a>.</p></div></section>
<section class="band" id="form"><div class="wrap split"><div><h2>Our partner standards</h2><ul class="list-check"><li>Health claims must be lawful and evidence-based; no "cure" claims.</li><li>Insurance partners must be IRDAI-licensed; labs NABL-accredited or equivalent; doctors registered with NMC or a State Medical Council.</li><li>Sponsored content is always labelled.</li><li>Leads are shared only with the consent of the person, for the purpose they asked for.</li></ul></div>
<div class="lead-box"><form class="form" data-form="Partnership / advertising enquiry" data-redirect="thank-you.html?type=partner">
<div class="field"><label for="p-type">I'm interested in</label><select id="p-type" name="interest" required><option>Lead partnership</option><option>Sponsorship</option><option>Advertising</option><option>Contest / prize sponsorship</option><option>CSR / check-up camp</option><option>Buying the domain or website</option><option>Investment / partnership</option></select></div>
<div class="row2"><div class="field"><label for="p-name">Name</label><input id="p-name" name="name" required autocomplete="name"></div><div class="field"><label for="p-co">Company</label><input id="p-co" name="company" required autocomplete="organization"></div></div>
<div class="row2"><div class="field"><label for="p-email">Work email</label><input id="p-email" type="email" name="email" required autocomplete="email"></div><div class="field"><label for="p-phone">Phone</label><input id="p-phone" type="tel" name="phone"></div></div>
<div class="field"><label for="p-budget">Budget range</label><select id="p-budget" name="budget"><option>To discuss</option><option>Under ₹50,000</option><option>₹50,000–₹2 lakh</option><option>₹2–10 lakh</option><option>Over ₹10 lakh</option></select></div>
<div class="field"><label for="p-msg">Message</label><textarea id="p-msg" name="message" required></textarea></div>{hp()}
<button class="btn primary" type="submit">Send enquiry</button><p class="form-status" role="status"></p></form></div></div></section>'''
    emit("advertise.html", "Advertise, Sponsor & Partner with Nirog.com", "Partner with Nirog.com: lead partnerships for insurers, labs and clinics, sponsorships, display ads, contests and CSR check-up camps.", adv)

    # ---------- About / editorial ----------
    emit("about.html", "About Nirog.com", "Nirog.com is an independent preventive-health website for India: free tools, evidence-based guides and unbiased help with check-ups and insurance.",
         f'''<div class="wrap narrow prose">{crumbs("", [("", "About")])}<h1>About Nirog.com</h1>
<p><b>Nirog</b> (निरोग) means "free of disease". We believe most Indian families could avoid years of illness and lakhs in hospital bills by catching problems early: a blood-sugar test at 35, a blood pressure check at the pharmacy, a waist that stays under half your height, and health insurance that actually covers what it should.</p>
<h2>What we do</h2><ul><li><b>Free tools</b> such as BMI with Asian cut-offs, the Indian Diabetes Risk Score and a health insurance cover calculator.</li><li><b>Plain-English guides</b> on prevention, common conditions, nutrition, sleep, movement and health insurance, each with listed sources.</li><li><b>Free advice</b>: we connect readers who ask for help with licensed insurance advisors, accredited labs and registered doctors.</li><li><b>Community</b>: contests, awareness campaigns and check-up camps funded by supporters and sponsors.</li></ul>
<h2>How we make money</h2><p>We are funded by advertising (Google AdSense), referral fees from vetted partners when a reader asks to be connected, sponsorships that are always labelled, and voluntary reader support. Money never buys a recommendation or changes the facts in a guide. Read more in our <a href="editorial-policy.html">editorial policy</a>.</p>
<h2>What we are not</h2><p>We are not a hospital, clinic, pharmacy or insurance company, and we do not diagnose or treat anyone. Always consult a qualified professional about your own health. In an emergency call 108 or 112.</p>
<h2>Contact</h2><p>Use our <a href="contact.html">contact form</a>. For interest in this website, the domain name, sponsorship, advertising or partnership, use the link at the top of every page.</p></div>''')
    emit("editorial-policy.html", "Editorial Policy & Medical Review Standards", "How Nirog.com researches, writes, fact-checks, updates and corrects health content, and how we keep advertising separate from editorial.",
         f'''<div class="wrap narrow prose">{crumbs("", [("", "Editorial policy")])}<h1>Editorial policy</h1><p>Health information can change lives, so we hold it to a high standard. This page explains how we work.</p>
<h2>Sources</h2><p>We base our content on authoritative sources: the World Health Organization, the Indian Council of Medical Research (including ICMR-NIN), the Ministry of Health &amp; Family Welfare, national programmes, IRDAI for insurance, the NHS, CDC and peer-reviewed research. Every guide lists its main sources at the end, with links.</p>
<h2>Writing and fact-checking</h2><p>Guides are written by our editorial team in plain language and checked against the cited sources before publishing. Specific numbers, thresholds and rules are verified at the source. When Indian guidance differs from international guidance (for example BMI cut-offs), we say so.</p>
<h2>Medical review</h2><p>We are building a panel of registered doctors and dietitians to review guides; reviewed guides will show the reviewer's name and registration details. Qualified professionals can <a href="careers.html">apply here</a>.</p>
<h2>Updates and corrections</h2><p>Each guide shows the date it was last updated. We review guides at least once a year and whenever major guidance changes. Spotted an error? Tell us through the <a href="contact.html">contact form</a>; we correct mistakes promptly and note significant changes.</p>
<h2>What we won't publish</h2><ul><li>Claims that any product, herb or therapy cures a disease without strong evidence.</li><li>Medicine doses or advice to stop prescribed treatment.</li><li>Content that discourages people from seeing a doctor.</li></ul>
<h2>Advertising and partnerships</h2><p>Ads are served by Google AdSense and are clearly separate from our content. Sponsored content is labelled "sponsored". Partner referral fees never influence what we write; insurance guides do not name or rank insurers.</p>
<h2>AI and tools</h2><p>We may use software, including AI tools, to help research and draft. Every published page is checked by a person against the sources, and our calculators use published, cited formulas.</p></div>''')

    # ---------- Contact ----------
    emit("contact.html", "Contact Nirog.com", "Contact Nirog.com with questions, corrections, partnership ideas or feedback. We reply within two business days.",
         f'''<div class="wrap">{crumbs("", [("", "Contact")])}<div class="split"><div><h1>Contact us</h1><p class="muted">Questions, corrections, partnership ideas or feedback: send a message and we'll reply within two business days.</p>
<ul class="list-check"><li>Need health insurance or check-up help? <a href="get-advice.html">Use the free advice form</a> for the fastest response.</li><li>Want to advertise or partner? <a href="advertise.html">See partnership options</a>.</li><li>Interested in this website or domain name? <a href="{OWNER}" target="_blank" rel="noopener">Contact the owner</a>.</li></ul>
<div class="callout warn small"><b>Medical emergency?</b> Do not use this form. Call 108 or 112 right away.</div></div>
<div class="lead-box"><form class="form" data-form="Contact form" data-redirect="thank-you.html?type=contact">
<div class="field"><label for="ct-topic">Topic</label><select id="ct-topic" name="topic"><option>General question</option><option>Report an error / correction</option><option>Partnership or advertising</option><option>Website or domain enquiry</option><option>Privacy or data request</option><option>Copyright or trademark</option><option>Other</option></select></div>
<div class="row2"><div class="field"><label for="ct-name">Name</label><input id="ct-name" name="name" required autocomplete="name"></div><div class="field"><label for="ct-email">Email</label><input id="ct-email" type="email" name="email" required autocomplete="email"></div></div>
<div class="field"><label for="ct-msg">Message</label><textarea id="ct-msg" name="message" required></textarea></div>{hp()}
<button class="btn primary" type="submit">Send message</button><p class="form-status" role="status"></p></form></div></div></div>''')

    # ---------- Legal ----------
    upd = "Last updated: 28 October 2026"
    emit("privacy.html", "Privacy Policy", "How Nirog.com collects, uses and protects your information, including cookies, Google AdSense advertising and form submissions, under India's DPDP Act.",
         f'''<div class="wrap narrow prose">{crumbs("", [("", "Privacy policy")])}<h1>Privacy policy</h1><p class="muted">{upd}</p>
<p>This policy explains what information Nirog.com ("we") collects, why, and your choices. We follow the Digital Personal Data Protection Act, 2023 (India) and apply similar standards to visitors from other countries.</p>
<h2>Information you give us</h2><p>When you submit a form (advice request, Nirog Score plan, newsletter, contest, job application, donation pledge or contact) we receive the details you enter, such as name, phone, email, city and your message. We use it only for the purpose you asked for. Form submissions are delivered through a third-party form-processing service (FormSubmit) to our private inbox.</p>
<h2>Sharing with partners</h2><p>If you request insurance, check-up or doctor help and give consent, we share the minimum necessary details with one or more vetted partners (licensed insurance intermediaries, accredited labs or registered clinics) so they can respond. We do not sell your personal data.</p>
<h2>Calculators and the Nirog Score</h2><p>Calculations run in your browser. Your answers are not stored or sent unless you choose to submit a form.</p>
<h2>Cookies and advertising</h2><p>We use essential browser storage (for example to remember your theme and cookie choice). Third-party vendors, including Google, use cookies to serve ads based on your prior visits to this and other websites. Google's use of advertising cookies enables it and its partners to serve ads to you based on your visits to this site and/or other sites on the Internet. You can opt out of personalised advertising by visiting <a href="https://adssettings.google.com" target="_blank" rel="noopener">Google Ads Settings</a>, or opt out of some third-party vendors' use of cookies at <a href="https://www.aboutads.info/choices/" target="_blank" rel="noopener">aboutads.info</a>. Learn more about <a href="https://policies.google.com/technologies/partner-sites" target="_blank" rel="noopener">how Google uses data from partner sites</a>. Choosing "Essential + non-personalised ads" in our cookie notice requests non-personalised ads.</p>
<h2>Videos</h2><p>YouTube videos load in privacy-enhanced mode only after you press play; YouTube's own privacy policy then applies.</p>
<h2>Retention and security</h2><p>We keep form data only as long as needed for your request, contests or legal obligations (typically up to 24 months), then delete it. We use HTTPS and limit access to those who need it.</p>
<h2>Your rights</h2><p>You can ask to access, correct or erase your data, withdraw consent or nominate someone to act for you, using the <a href="contact.html">contact form</a> (topic: privacy). You may also raise a grievance with the Data Protection Board of India.</p>
<h2>Children</h2><p>Nirog.com is meant for adults. We do not knowingly collect personal data from children under 18.</p>
<h2>Changes</h2><p>We may update this policy and will change the date above when we do.</p></div>''')
    emit("terms.html", "Terms of Use", "The terms that apply when you use Nirog.com, its health tools, guides, forms, contests and partner referral services.",
         f'''<div class="wrap narrow prose">{crumbs("", [("", "Terms of use")])}<h1>Terms of use</h1><p class="muted">{upd}</p>
<p>By using Nirog.com you agree to these terms. If you do not agree, please do not use the site.</p>
<h2>Information only</h2><p>Content and tools are for general education and are not medical, insurance, financial or legal advice. See the <a href="disclaimer.html">medical disclaimer</a>.</p>
<h2>Referral services</h2><p>When you request help, we may connect you with independent partners. Any policy, test or consultation you choose is a contract between you and that provider, on their terms. We are not responsible for partners' products or services, though we take complaints about partners seriously.</p>
<h2>Acceptable use</h2><p>Do not misuse forms, submit false information, scrape the site at scale, or attempt to disrupt it.</p>
<h2>Contests</h2><p>Contests are governed by the rules on the <a href="contests.html">contests page</a> and any additional rules published for a specific contest.</p>
<h2>Intellectual property</h2><p>The text, design, tools and code of Nirog.com are protected by copyright. You may share links and short quotes with attribution. See our <a href="trademark.html">trademark and copyright disclosure</a>.</p>
<h2>Liability</h2><p>To the extent permitted by law, Nirog.com is not liable for any loss arising from use of the site or reliance on its content. The site is provided "as is".</p>
<h2>Governing law</h2><p>These terms are governed by the laws of India.</p></div>''')
    emit("disclaimer.html", "Medical Disclaimer", "Nirog.com provides general health information for education only, not medical advice, diagnosis or treatment. Read our full medical disclaimer.",
         f'''<div class="wrap narrow prose">{crumbs("", [("", "Medical disclaimer")])}<h1>Medical disclaimer</h1><p class="muted">{upd}</p>
<p>The content on Nirog.com, including text, calculators, the Nirog Score, videos and links, is for general information and education only. It is <b>not</b> a substitute for professional medical advice, diagnosis or treatment.</p>
<ul><li>Always seek the advice of a qualified doctor or other health professional about any medical condition, test result or treatment.</li><li>Never disregard professional advice, or delay seeking it, because of something you read here.</li><li>Do not start, stop or change any medicine without your doctor's advice.</li><li>Calculator results are estimates based on published formulas and may not apply to you, especially if you are pregnant, under 18, elderly or have a medical condition.</li></ul>
<p><b>In a medical emergency, call 108 (ambulance) or 112 (emergency) immediately.</b> For mental health support, call Tele-MANAS at 14416.</p>
<p>Insurance information is general and may change; always read the policy wording and consult a licensed advisor. Links to third-party sites are provided for convenience; we do not control their content.</p></div>''')
    emit("trademark.html", "Trademark & Copyright Disclosure", "Nirog.com trademark and copyright disclosure: independent website, not affiliated with any Nirog-named business; how to report infringement.",
         f'''<div class="wrap narrow prose">{crumbs("", [("", "Trademark & copyright")])}<h1>Trademark &amp; copyright disclosure</h1><p class="muted">{upd}</p>
<h2>Independence</h2><p>Nirog.com is an independent website. The word "nirog" (निरोग) is a common Hindi and Sanskrit word meaning "free of disease" or "healthy", used here in its ordinary descriptive sense.</p>
<p>Nirog.com is <b>not affiliated with, endorsed by, sponsored by or connected to</b> any company, product, brand, medicine, clinic, app or service that uses "Nirog", "Nirogi" or any similar name or mark, in India or elsewhere. Any such names belong to their respective owners. We do not sell or promote any product under the name "Nirog".</p>
<h2>Third-party marks</h2><p>Names of organisations, programmes and publishers mentioned on this site (for example WHO, ICMR, IRDAI, YouTube and the publishers of embedded videos) are trademarks or names of their respective owners and are used only for identification and reference. Their mention does not imply endorsement.</p>
<h2>Copyright</h2><p>© 2026 Nirog.com. All original text, graphics, logos, page design, calculators and code on this site are protected by copyright. You may link to our pages and quote brief excerpts with clear attribution and a link. Republishing full guides, or copying tools or design, requires written permission.</p>
<p>Embedded videos remain the property of their publishers and are shown through YouTube's standard embed. Formulas used in our calculators come from published research, which we cite.</p>
<h2>Report a concern</h2><p>If you believe content on Nirog.com infringes your trademark or copyright, send details through our <a href="contact.html">contact form</a> (topic: copyright or trademark), including the page address, the work or mark concerned and your contact details. We review every notice and act promptly, including removing material where appropriate.</p></div>''')

    # ---------- Search, thanks, 404, sitemap ----------
    emit("search.html", "Search Nirog.com", "Search Nirog.com health guides, calculators and pages.",
         f'''<div class="wrap narrow">{crumbs("", [("", "Search")])}<h1>Search</h1><form id="site-search" class="search-box" role="search" data-base=""><label class="sr" for="q">Search</label><input id="q" type="search" name="q" placeholder="Try: sugar, BP, thyroid, insurance for parents" autofocus><button class="btn brand" type="submit">Search</button></form>
<div id="search-results" class="search-results" style="margin-top:20px" aria-live="polite"></div></div>''', robots="noindex,follow")
    emit("thank-you.html", "Thank You", "Thank you for contacting Nirog.com.",
         '''<section class="hero"><div class="wrap narrow center"><span class="eyebrow">Received</span><h1>Thank you. We've got your message.</h1><p class="lede" style="margin:0 auto">We'll get back to you within one to two business days, at the time and channel you chose. Meanwhile, here are useful next steps.</p>
<div class="btn-row" style="justify-content:center;margin-top:24px"><a class="btn primary" href="nirog-score.html">Take the Nirog Score</a><a class="btn ghost" href="tools/index.html">Explore free tools</a><a class="btn ghost" href="guides/index.html">Read health guides</a></div></div></section>''', robots="noindex,follow", sticky=False)
    emit("404.html", "Page Not Found", "The page you are looking for could not be found.",
         '''<section class="hero"><div class="wrap narrow center"><span class="eyebrow">404</span><h1>We couldn't find that page</h1><p class="lede" style="margin:0 auto">It may have moved. Try the links below or search the site.</p>
<div class="btn-row" style="justify-content:center;margin-top:24px"><a class="btn primary" href="/nirog-com/index.html">Home</a><a class="btn ghost" href="/nirog-com/search.html">Search</a></div></div></section>''', robots="noindex")
    # 404 must work from any path on GitHub Pages: use absolute-ish links that work on both hosts
    G["OUT"]["404.html"] = G["OUT"]["404.html"].replace('href="/nirog-com/index.html"', 'href="./"').replace('href="/nirog-com/search.html"', 'href="search.html"')

    # sitemap.html + search index
    titles = {}
    for p, h in G["OUT"].items():
        m = re.search(r"<title>(.*?)</title>", h); d = re.search(r'<meta name="description" content="(.*?)"', h)
        titles[p] = (m.group(1).replace(" | Nirog.com", "") if m else p, d.group(1) if d else "")
    def lst(prefix_filter):
        return "".join('<li><a href="%s">%s</a></li>' % (p, titles[p][0]) for p in sorted(titles) if prefix_filter(p))
    emit("sitemap.html", "Sitemap", "All pages on Nirog.com: guides, tools, advice, community and policy pages.",
         f'''<div class="wrap prose">{crumbs("", [("", "Sitemap")])}<h1>Sitemap</h1><div class="grid g3"><div><h2>Health guides</h2><ul>{lst(lambda p: p.startswith("guides/"))}</ul></div>
<div><h2>Tools</h2><ul>{lst(lambda p: p.startswith("tools/"))}<li><a href="nirog-score.html">Nirog Score</a></li></ul></div>
<div><h2>Pages</h2><ul>{lst(lambda p: "/" not in p and p not in ("404.html", "thank-you.html", "search.html"))}</ul></div></div></div>''')
    idx = []
    for p, (t, d) in titles.items():
        if p in ("404.html", "thank-you.html", "search.html"): continue
        kw = ""
        for g in guides:
            if p == "guides/%s.html" % g["slug"]: kw = g.get("keywords", "") + " " + g.get("category", "")
        idx.append({"u": p, "t": esc(t, quote=False) if False else t, "d": d, "k": kw})
    open(os.path.join(ROOT, "search-index.json"), "w", encoding="utf-8").write(json.dumps(idx, ensure_ascii=False))
