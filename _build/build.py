#!/usr/bin/env python3
"""Nirog.com static site generator.
Run from the repo root:  python3 _build/build.py
Edit guides in _build/guides/*.md, videos in _build/videos.json, page copy in _build/pages.py."""
import json, os, re, html, datetime, sys
import markdown

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B = os.path.join(ROOT, "_build")
sys.path.insert(0, B)
BASE_URL = "https://nirog.com/"
TODAY = datetime.date(2026, 10, 28)
ADSENSE = '<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-6620975821265271" crossorigin="anonymous"></script>'
OWNER_URL = "https://web.works/contact"
esc = html.escape

ICONS = {
 "check": '<path d="M5 12l5 5L20 7"/>',
 "scale": '<path d="M12 3v18M5 7h14M7 7l-3 7a3 3 0 006 0L7 7zm10 0l-3 7a3 3 0 006 0l-3-7z"/>',
 "flame": '<path d="M12 3s5 4.5 5 9.5A5 5 0 017 12.5C7 9 9.5 8 9.5 8s.5 3 2.5 3c0-4 0-8 0-8z"/>',
 "drop": '<path d="M12 3s6 6.5 6 11a6 6 0 01-12 0c0-4.5 6-11 6-11z"/>',
 "heart": '<path d="M12 20s-7-4.4-9-9a5 5 0 019-3 5 5 0 019 3c-2 4.6-9 9-9 9z"/><path d="M3 12h4l2-3 3 6 2-3h7"/>',
 "gauge": '<path d="M4 15a8 8 0 1116 0"/><path d="M12 15l4-5"/>',
 "shield": '<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6l8-3z"/><path d="M9 12l2 2 4-4"/>',
 "ruler": '<path d="M3 17L17 3l4 4L7 21l-4-4z"/><path d="M7 13l2 2M10 10l2 2M13 7l2 2"/>',
 "moon": '<path d="M20 14.5A8 8 0 019.5 4 8 8 0 1020 14.5z"/>',
 "baby": '<circle cx="12" cy="8" r="4"/><path d="M5 21c1-4 4-6 7-6s6 2 7 6"/>',
 "bowl": '<path d="M3 11h18a9 9 0 01-18 0z"/><path d="M8 7c0-1.5 1-2 1-3M12 7c0-1.5 1-2 1-3M16 7c0-1.5 1-2 1-3"/>',
 "target": '<circle cx="12" cy="12" r="8"/><circle cx="12" cy="12" r="4"/><circle cx="12" cy="12" r="1"/>',
 "book": '<path d="M4 5a2 2 0 012-2h13v16H6a2 2 0 00-2 2V5z"/><path d="M4 19a2 2 0 012-2h13"/>',
 "play": '<rect x="3" y="5" width="18" height="14" rx="3"/><path d="M10 9l5 3-5 3V9z"/>',
 "gift": '<rect x="3" y="8" width="18" height="13" rx="2"/><path d="M12 8v13M3 12h18M12 8S9 3 7 5s5 3 5 3 3-5 5-3-5 3-5 3"/>',
 "hand": '<path d="M12 21s-8-4.5-8-11a4 4 0 018-1 4 4 0 018 1c0 6.5-8 11-8 11z"/>',
 "users": '<circle cx="9" cy="8" r="3.5"/><path d="M2 20c.8-3.5 3.6-5.5 7-5.5s6.2 2 7 5.5"/><circle cx="17.5" cy="9" r="2.5"/><path d="M17 14.5c2.5 0 4.3 1.6 5 4.5"/>',
 "megaphone": '<path d="M3 10v4h4l7 5V5L7 10H3z"/><path d="M18 8a5 5 0 010 8"/>',
 "search": '<circle cx="11" cy="11" r="7"/><path d="M20 20l-4-4"/>',
 "sun": '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M2 12h2M20 12h2M5 5l1.5 1.5M17.5 17.5L19 19M5 19l1.5-1.5M17.5 6.5L19 5"/>',
 "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
 "lock": '<rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V8a4 4 0 018 0v3"/>',
 "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
 "leaf": '<path d="M5 19C5 10 11 4 20 4c0 9-6 15-15 15z"/><path d="M5 19l8-8"/>',
 "phone": '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 005 5L15 13l5 2v4a2 2 0 01-2 2A16 16 0 013 6a2 2 0 012-2z"/>',
}
def icon(name, size=None):
    return ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" '
            'stroke-linejoin="round" aria-hidden="true">' + ICONS[name] + "</svg>")

LOGO = ('<svg viewBox="0 0 40 40" aria-hidden="true"><circle cx="20" cy="20" r="19" fill="#0E5E4F"/>'
        '<path d="M11 27c0-9 6-15 18-16 0 11-7 17-16 17" fill="#E3F0EB"/>'
        '<path d="M8 21h6l2.5-4 3.5 8 2.5-4H32" fill="none" stroke="#D9701A" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></svg>')
FAVICON = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 40 40"><circle cx="20" cy="20" r="19" fill="#0E5E4F"/>'
           '<path d="M11 27c0-9 6-15 18-16 0 11-7 17-16 17" fill="#E3F0EB"/>'
           '<path d="M8 21h6l2.5-4 3.5 8 2.5-4H32" fill="none" stroke="#D9701A" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></svg>')

NAV = [("guides/index.html", "Health guides", "guides"), ("tools/index.html", "Tools", "tools"),
       ("nirog-score.html", "Nirog Score", "score"), ("videos.html", "Videos", "videos"),
       ("get-advice.html", "Insurance help", "advice"), ("contests.html", "Contests", "contests"),
       ("support.html", "Support us", "support")]

def hp():
    return '<div class="hp" aria-hidden="true"><label>Leave this empty<input name="_hp" tabindex="-1" autocomplete="off"></label></div>'

def page(path, title, desc, body, active="", schema=None, extra_js="", robots="index,follow", og_type="website", sticky=True):
    depth = path.count("/")
    R = "../" * depth
    canon = BASE_URL + ("" if path == "index.html" else path)
    navhtml = "".join('<a href="%s%s"%s>%s</a>' % (R, h, ' aria-current="page"' if k == active else "", t) for h, t, k in NAV)
    ld = [{"@context": "https://schema.org", "@type": "Organization", "name": "Nirog.com", "url": BASE_URL,
           "logo": BASE_URL + "assets/img/logo.svg"}]
    if schema: ld += schema if isinstance(schema, list) else [schema]
    ld_html = "".join('<script type="application/ld+json">%s</script>' % json.dumps(s, ensure_ascii=False) for s in ld)
    full_title = title if title.endswith("Nirog.com") else title + " | Nirog.com"
    sticky_html = ('<div class="sticky-cta"><a class="btn primary" href="%sget-advice.html">Free health &amp; insurance advice</a></div>' % R) if sticky else ""
    return f'''<!doctype html>
<html lang="en-IN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(full_title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{canon}">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="Nirog.com">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{BASE_URL}assets/img/og.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0E5E4F">
<meta name="google-adsense-account" content="ca-pub-6620975821265271">
<link rel="icon" href="{R}assets/img/favicon.svg" type="image/svg+xml">
<link rel="manifest" href="{R}site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Figtree:wght@400;600;700&family=Fraunces:opsz,wght@9..144,500;9..144,600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{R}assets/css/site.css">
<script>try{{var t=localStorage.getItem("nirog-theme");if(t)document.documentElement.setAttribute("data-theme",t)}}catch(e){{}}</script>
{ADSENSE}
{ld_html}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div class="ownerbar"><a href="{OWNER_URL}" target="_blank" rel="noopener">Contact, if you are interested in this website / domain name / Sponsorship / Advertisement / Partnership</a></div>
<header class="site-head"><div class="wrap head-row">
<a class="logo" href="{R}index.html" aria-label="Nirog.com home">{LOGO}<span><b>nirog</b>.com</span></a>
<nav class="nav" id="nav" aria-label="Main">{navhtml}</nav>
<div class="head-tools">
<a class="icon-btn" href="{R}search.html" aria-label="Search">{icon("search")}</a>
<button class="icon-btn" type="button" data-theme-toggle aria-label="Switch light or dark theme">{icon("sun")}</button>
<a class="btn primary sm head-cta" href="{R}get-advice.html">Free advice</a>
<button class="icon-btn menu-btn" type="button" aria-expanded="false" aria-controls="nav" aria-label="Menu">{icon("menu")}</button>
</div></div></header>
<main id="main">
{body}
</main>
<footer class="site-foot"><div class="wrap">
<div class="foot-grid">
<div><a class="logo" href="{R}index.html">{LOGO}<span>nirog.com</span></a>
<p style="margin-top:14px">Independent, evidence-based preventive health for India: free tools, plain-English guides and unbiased help with check-ups and health insurance.</p>
<form class="news-form" data-form="Newsletter signup" data-ok="You're in. Watch your inbox for the weekly Nirog note.">
<label class="sr" for="nl-email">Email address</label><input id="nl-email" type="email" name="email" required placeholder="Your email" autocomplete="email">{hp()}<button class="btn primary sm" type="submit">Join</button>
<p class="form-status" role="status" style="flex-basis:100%"></p></form></div>
<div><h4>Explore</h4><ul><li><a href="{R}guides/index.html">Health guides</a></li><li><a href="{R}tools/index.html">Free health tools</a></li><li><a href="{R}nirog-score.html">Nirog Score</a></li><li><a href="{R}videos.html">Health videos</a></li><li><a href="{R}search.html">Search</a></li></ul></div>
<div><h4>Get involved</h4><ul><li><a href="{R}get-advice.html">Free insurance &amp; check-up advice</a></li><li><a href="{R}support.html">Donate / support</a></li><li><a href="{R}contests.html">Contests &amp; prizes</a></li><li><a href="{R}careers.html">Careers</a></li><li><a href="{R}advertise.html">Advertise &amp; partner</a></li></ul></div>
<div><h4>About</h4><ul><li><a href="{R}about.html">About us</a></li><li><a href="{R}editorial-policy.html">Editorial policy</a></li><li><a href="{R}contact.html">Contact</a></li><li><a href="{R}privacy.html">Privacy policy</a></li><li><a href="{R}terms.html">Terms of use</a></li><li><a href="{R}disclaimer.html">Medical disclaimer</a></li><li><a href="{R}trademark.html">Trademark &amp; copyright</a></li><li><a href="{R}sitemap.html">Sitemap</a></li></ul></div>
</div>
<div class="foot-legal">
<p><b>Medical disclaimer:</b> Nirog.com provides general health information for education only. It is not a substitute for professional medical advice, diagnosis or treatment. In an emergency in India, call <b>108</b> or <b>112</b>.</p>
<p><b>Trademark notice:</b> Nirog.com is an independent website. "Nirog" is a common Hindi/Sanskrit word meaning "free of disease"; this site is not affiliated with, endorsed by or connected to any company, product, brand or service that uses "Nirog" or a similar name. All third-party trademarks belong to their owners. <a href="{R}trademark.html">Read the full disclosure</a>.</p>
<p>© <span data-year>2026</span> Nirog.com. All rights reserved. Content may not be copied without permission.</p>
</div></div></footer>
<div class="consent" id="consent" role="dialog" aria-live="polite" aria-label="Cookie notice" hidden>
<p>We use cookies for essential features and, with Google AdSense, to show and measure ads (which keep Nirog.com free). See our <a href="{R}privacy.html">privacy policy</a>.</p>
<div class="btn-row"><button class="btn brand sm" data-consent="all">Accept all</button><button class="btn ghost sm" data-consent="essential">Essential + non-personalised ads</button></div></div>
{sticky_html}
<script src="{R}assets/js/config.js"></script>
<script>window.NIROG_BASE="{R}";</script>
<script src="{R}assets/js/main.js" defer></script>
{extra_js}
</body>
</html>
'''

OUT = {}
def emit(path, title, desc, body, **kw):
    OUT[path] = page(path, title, desc, body, **kw)
    return path

def crumbs(R, items):
    parts = ['<a href="%sindex.html">Home</a>' % R]
    for href, t in items:
        parts.append('<a href="%s%s">%s</a>' % (R, href, t) if href else esc(t))
    return '<nav class="crumbs" aria-label="Breadcrumb">' + " › ".join(parts) + "</nav>"

def breadcrumb_ld(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": BASE_URL + u} for i, (u, n) in enumerate(items)]}

def faq_ld(pairs):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in pairs]}

def faq_html(pairs):
    return '<div class="faq">' + "".join("<details><summary>%s</summary><p>%s</p></details>" % (esc(q), a) for q, a in pairs) + "</div>"

# ---------------- Guides ----------------
CAT_SLUG = {"Prevention": "prevention", "Conditions": "conditions", "Nutrition & Lifestyle": "lifestyle", "Health Insurance": "insurance"}

def load_guides():
    gs = []
    for fn in sorted(os.listdir(os.path.join(B, "guides"))):
        if not fn.endswith(".md"): continue
        raw = open(os.path.join(B, "guides", fn), encoding="utf-8").read()
        m = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", raw, re.S)
        if not m: print("skip (no front matter):", fn); continue
        meta = {}
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1); meta[k.strip()] = v.strip().strip('"')
        body = m.group(2).strip()
        body = re.sub(r"^#\s+.*\n", "", body)  # drop stray H1
        meta["slug"] = meta.get("slug") or fn[:-3]
        meta["body"] = body
        meta["cat"] = CAT_SLUG.get(meta.get("category", "Prevention"), "prevention")
        # FAQ extraction
        faqs = []
        fm = re.search(r"^##\s+Frequently asked questions\s*$(.*?)(?=^##\s|\Z)", body, re.S | re.M)
        if fm:
            for q, a in re.findall(r"^###\s+(.+?)\s*$\n(.*?)(?=^###\s|\Z)", fm.group(1), re.S | re.M):
                a = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", " ".join(a.split()))
                faqs.append((q.strip(), esc(a)))
        meta["faqs"] = faqs
        gs.append(meta)
    order = ["preventive-health-checkup-by-age", "type-2-diabetes-prevention", "high-blood-pressure", "health-insurance-buying-guide"]
    gs.sort(key=lambda g: (order.index(g["slug"]) if g["slug"] in order else 99, g["title"]))
    return gs

def guide_card(g, R):
    return ('<a class="guide-card" data-cat="%s" href="%sguides/%s.html"><span class="tag%s">%s</span><h3>%s</h3><p>%s</p><span class="meta">%s read · Updated %s</span></a>'
            % (g["cat"], R, g["slug"], " accent" if g["cat"] == "insurance" else "", esc(g.get("category", "")), esc(g["title"]), esc(g.get("description", "")),
               esc(g.get("read_time", "6 min")), datetime.date.fromisoformat(g.get("updated", "2026-10-28")).strftime("%d %b %Y")))

def build_guides(guides):
    md = markdown.Markdown(extensions=["tables", "toc", "sane_lists"], extension_configs={"toc": {"permalink": False}})
    for g in guides:
        md.reset()
        htmlbody = md.convert(g["body"])
        htmlbody = re.sub(r'<a href="(https?://[^"]+)"', r'<a href="\1" target="_blank" rel="noopener nofollow"', htmlbody)
        heads = [(t["id"], t["name"]) for t in md.toc_tokens if t["level"] == 2]
        ins = g["cat"] == "insurance"
        cta = ('<aside class="inline-cta"><div><b>%s</b><p class="small muted">%s</p></div><a class="btn primary" href="../get-advice.html?need=%s">%s</a></aside>'
               % (("Confused by policy fine print?", "Get free, unbiased help choosing or claiming health insurance. No spam, no pressure.", "insurance", "Get free advice") if ins else
                  ("Not sure which tests you need?", "Get a free, personalised preventive check-up plan from our advisors.", "checkup", "Get my free plan")))
        parts = re.split(r"(?=<h2)", htmlbody)
        if len(parts) > 4: parts.insert(4, cta)
        else: parts.append(cta)
        htmlbody = "".join(parts)
        toc = "".join('<li><a href="#%s">%s</a></li>' % (i, esc(n)) for i, n in heads)
        related = [x for x in guides if x["cat"] == g["cat"] and x["slug"] != g["slug"]]
        related += [x for x in guides if x["cat"] != g["cat"]]
        rel = "".join(guide_card(x, "../") for x in related[:3])
        upd = datetime.date.fromisoformat(g.get("updated", "2026-10-28"))
        body = f'''<div class="wrap">
{crumbs("../", [("guides/index.html", "Health guides"), ("", g["title"])])}
<header class="article-head narrow"><span class="tag{' accent' if ins else ''}">{esc(g.get("category", ""))}</span>
<h1 style="margin-top:12px">{esc(g["title"])}</h1>
<p class="muted" style="font-size:1.12rem">{esc(g.get("description", ""))}</p>
<div class="byline"><span>By the Nirog editorial team</span><span>Fact-checked against the sources listed below</span><span>Updated {upd.strftime("%d %B %Y")}</span><span>{esc(g.get("read_time", ""))} read</span></div></header>
<div class="article-grid">
<article class="prose">{htmlbody}
<div class="callout small" style="margin-top:2em"><b>Medical disclaimer:</b> This guide is general information, not medical advice. Talk to a qualified doctor about your own health. In an emergency call 108 or 112. See our <a href="../editorial-policy.html">editorial policy</a>.</div>
</article>
<aside class="aside"><div class="toc"><p class="eyebrow">On this page</p><ol>{toc}</ol>
<div class="card" style="margin-top:24px"><b>Check your risk in 2 minutes</b><p class="small muted">Take the free Nirog Score and get your personal action list.</p><a class="btn brand sm" href="../nirog-score.html">Start Nirog Score</a></div></div></aside>
</div>
<section style="padding-top:48px"><h2>Keep reading</h2><div class="grid g3">{rel}</div></section>
</div>'''
        schema = [{"@context": "https://schema.org", "@type": "MedicalWebPage", "headline": g["title"], "description": g.get("description", ""),
                   "url": BASE_URL + "guides/%s.html" % g["slug"], "datePublished": "2026-10-28", "dateModified": upd.isoformat(),
                   "inLanguage": "en-IN", "author": {"@type": "Organization", "name": "Nirog editorial team", "url": BASE_URL + "editorial-policy.html"},
                   "publisher": {"@type": "Organization", "name": "Nirog.com", "logo": {"@type": "ImageObject", "url": BASE_URL + "assets/img/logo.svg"}},
                   "lastReviewed": upd.isoformat(), "keywords": g.get("keywords", "")},
                  breadcrumb_ld([("", "Home"), ("guides/index.html", "Health guides"), ("guides/%s.html" % g["slug"], g["title"])])]
        if g["faqs"]: schema.append(faq_ld(g["faqs"]))
        emit("guides/%s.html" % g["slug"], g["title"], g.get("description", ""), body, active="guides", schema=schema, og_type="article")

    cats = [("all", "All")] + [(v, k) for k, v in CAT_SLUG.items()]
    filt = "".join('<button type="button" data-filter="%s" aria-pressed="%s">%s</button>' % (v, "true" if v == "all" else "false", esc(k)) for v, k in cats)
    cards = "".join(guide_card(g, "../") for g in guides)
    body = f'''<div class="wrap">{crumbs("../", [("", "Health guides")])}
<div class="section-head"><span class="eyebrow">Health library</span><h1>Health guides you can actually use</h1>
<p class="muted">Plain-English, India-specific guides on prevention, common conditions, food, sleep, movement and health insurance. Every guide lists its sources and is updated as guidance changes.</p></div>
<div class="filters" data-filter-group="#guide-list">{filt}</div>
<div class="grid g3" id="guide-list">{cards}</div>
<section><div class="lead-box split" style="align-items:center"><div><h2>Want a plan made for you?</h2><p class="muted">Tell us your age, city and concerns. An advisor will suggest the right check-ups and, if you want, unbiased health insurance options. Free and no obligation.</p></div>
<div class="btn-row"><a class="btn primary" href="../get-advice.html">Get free advice</a><a class="btn ghost" href="../nirog-score.html">Take the Nirog Score</a></div></div></section></div>'''
    emit("guides/index.html", "Health Guides: Prevention, Conditions, Lifestyle & Insurance", "Free, evidence-based health guides for India: preventive check-ups, diabetes, BP, thyroid, vitamin D, fatty liver, PCOS, sleep, diet and health insurance.", body, active="guides",
         schema=breadcrumb_ld([("", "Home"), ("guides/index.html", "Health guides")]))

def make_og(path):
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        print("Pillow not installed: skipping og.png"); return
    import glob
    def font(sz, bold=False):
        want = "dejavuserif-bold.ttf" if bold else "dejavusans.ttf"
        for f in glob.glob("/usr/share/fonts/**/*.ttf", recursive=True):
            if f.lower().endswith(want): return ImageFont.truetype(f, sz)
        return ImageFont.load_default()
    im = Image.new("RGB", (1200, 630), "#0E5E4F"); d = ImageDraw.Draw(im)
    d.ellipse((780, -160, 1420, 480), fill="#13705E")
    d.text((80, 170), "nirog.com", font=font(110, True), fill="#FFFFFF")
    d.text((84, 320), "Free health tools, guides & unbiased", font=font(44), fill="#E3F0EB")
    d.text((84, 380), "insurance & check-up advice for India", font=font(44), fill="#E3F0EB")
    d.rounded_rectangle((84, 470, 520, 540), radius=35, fill="#D9701A")
    d.text((118, 486), "Check your Nirog Score", font=font(32), fill="#FFFFFF")
    im.save(path, optimize=True)

if __name__ == "__main__":
    import pages
    guides = load_guides()
    build_guides(guides)
    pages.build(globals(), guides)
    for p, content in OUT.items():
        fp = os.path.join(ROOT, p); os.makedirs(os.path.dirname(fp), exist_ok=True)
        open(fp, "w", encoding="utf-8").write(content)
    # sitemap.xml
    urls = sorted(p for p in OUT if p not in ("404.html", "thank-you.html"))
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for p in urls:
        pr = "1.0" if p == "index.html" else ("0.9" if p in ("get-advice.html", "nirog-score.html") else "0.8" if p.startswith(("guides/", "tools/")) else "0.6")
        sm.append("<url><loc>%s</loc><lastmod>%s</lastmod><priority>%s</priority></url>" % (BASE_URL + ("" if p == "index.html" else p), TODAY.isoformat(), pr))
    sm.append("</urlset>")
    open(os.path.join(ROOT, "sitemap.xml"), "w").write("\n".join(sm) + "\n")
    open(os.path.join(ROOT, "robots.txt"), "w").write("User-agent: *\nAllow: /\nDisallow: /_build/\n\nSitemap: %ssitemap.xml\n" % BASE_URL)
    open(os.path.join(ROOT, "ads.txt"), "w").write("google.com, pub-6620975821265271, DIRECT, f08c47fec0942fa0\n")
    open(os.path.join(ROOT, ".nojekyll"), "w").write("")
    os.makedirs(os.path.join(ROOT, "assets/img"), exist_ok=True)
    open(os.path.join(ROOT, "assets/img/favicon.svg"), "w").write(FAVICON)
    open(os.path.join(ROOT, "assets/img/logo.svg"), "w").write(FAVICON)
    make_og(os.path.join(ROOT, "assets/img/og.png"))
    json.dump({"name": "Nirog.com", "short_name": "Nirog", "start_url": "./index.html", "display": "standalone",
               "background_color": "#FAF7F0", "theme_color": "#0E5E4F",
               "icons": [{"src": "assets/img/favicon.svg", "sizes": "any", "type": "image/svg+xml"}]},
              open(os.path.join(ROOT, "site.webmanifest"), "w"), indent=1)
    print("Built %d pages (%d guides)." % (len(OUT), len(guides)))
