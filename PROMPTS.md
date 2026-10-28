# Nirog.com: business case and phase-wise build prompt

## 1. The idea (and why this one)

**Nirog (निरोग) = "free of disease".** The name is a promise of prevention, so the site is built as **India's preventive-health decision hub**: free calculators and risk checks, plain-English guides, and a free advice service that turns readers into high-value leads for health insurance, preventive check-ups and doctor consultations.

Options considered:

| Concept | Traffic potential | Revenue per visitor | AdSense approval risk | Verdict |
|---|---|---|---|---|
| Ayurveda remedies blog | High | Low (supplement CPCs) | High (cure claims, YMYL) | Rejected |
| Symptom checker | High | Low-medium | High (diagnostic YMYL) | Rejected |
| Doctor directory | Medium | Medium | Low | Too capital- and data-heavy for v1 |
| **Preventive tools + guides + insurance/check-up advice** | **High (evergreen calculators)** | **High (insurance CPC + leads)** | **Low-medium (educational, sourced)** | **Chosen** |

### Revenue logic (estimates, verify with your own data)
- **AdSense floor:** health-insurance keywords are among the most expensive in India (published CPC estimates of roughly ₹50–120 for terms like "best health insurance for family"). Health content broadly earns a lower RPM; insurance and check-up pages lift the average.
- **Leads are the business:** published affiliate ranges for Indian health-insurance referrals run about ₹500–2,000 per qualified lead. Illustration: 100,000 visits/month × 1.5% form conversion = 1,500 leads × ₹300–800 blended = **₹4.5–12 lakh/month**, several times what display ads would pay on the same traffic.
- **Secondary:** check-up package referrals (labs), sponsored tools/series, contest sponsors, CSR camps, reader support.
- **Compliance note:** insurance leads must flow to IRDAI-licensed partners (broker, web aggregator or corporate agent programmes). Do not quote premiums or "sell" insurance on the site itself.

### Traffic engine
1. 12 calculators targeting evergreen, high-volume queries (BMI for Indians, diabetes risk, BP chart, calorie, protein, insurance cover).
2. 16 long-form, sourced guides (prevention, conditions, lifestyle, insurance) with FAQ schema.
3. Nirog Score (shareable 2-minute quiz) for WhatsApp virality.
4. Hindi versions of the top 20 pages (phase 4) for the largest underserved audience.

## 2. Phase-wise build prompt

Use these prompts in order. Each phase is self-contained.

### Phase 1: Foundation and compliance
> Build a static, GitHub-Pages-compatible website for Nirog.com (no server, no build step required at runtime). Use a Python generator (`_build/build.py`) that writes plain HTML into the repo root. Create a shared layout with: a top bar on every page reading "Contact, if you are interested in this website / domain name / Sponsorship / Advertisement / Partnership" linked to https://web.works/contact; a sticky header with logo, navigation (Health guides, Tools, Nirog Score, Videos, Insurance help, Contests, Support us), search, light/dark toggle and a "Free advice" CTA; a footer with newsletter form, link columns, medical disclaimer and trademark notice. Add the Google AdSense script `ca-pub-6620975821265271` in every `<head>`, an `ads.txt` (`google.com, pub-6620975821265271, DIRECT, f08c47fec0942fa0`), a cookie notice that can request non-personalised ads, `robots.txt`, `sitemap.xml`, canonical URLs on https://nirog.com/, Open Graph tags and Organization/WebSite JSON-LD. Create About, Editorial policy, Contact, Privacy (AdSense cookie disclosures, DPDP Act 2023), Terms, Medical disclaimer, Trademark & copyright disclosure (independent; "nirog" is a common Hindi word; no affiliation with any Nirog-named business), Sitemap, 404 and Thank-you pages. All forms post via JavaScript to a form relay whose address is assembled at runtime from an encoded key; the inbox address must never appear in markup, code comments or visible text.

### Phase 2: Tools and the Nirog Score
> Add 12 private, client-side calculators, each on its own SEO page with an explainer, FAQ (FAQPage schema), WebApplication schema and a lead CTA: BMI (Asian cut-offs 18.5/23/25), calorie (Mifflin-St Jeor), Indian Diabetes Risk Score (IDRS), blood pressure checker (ACC/AHA categories with emergency guidance), health insurance cover calculator (city tier × family × age × pre-existing, plus super top-up), waist-to-height ratio, ideal weight, water intake, heart-rate zones (Tanaka/Karvonen), protein (ICMR 0.83 g/kg), pregnancy due date (Naegele) and sleep cycles. Build the Nirog Score: 12 one-tap questions, a score out of 100, a personal action list and a lead form that carries the score.

### Phase 3: Content, video and trust
> Write 16 original, sourced guides (1,100–1,600 words) with key takeaways, tables, "when to see a doctor", FAQs and verified source links: preventive check-ups by age, type 2 diabetes, blood pressure, thyroid, vitamin D, anaemia, fatty liver, PCOS, heart attack signs, healthy Indian plate, sleep, yoga and movement, stress, health insurance buying guide, insurance for parents, cashless vs reimbursement. Render them with breadcrumbs, table of contents, an inline lead CTA, related guides and MedicalWebPage + FAQPage + BreadcrumbList schema. Add a video library of verified embeds from authoritative publishers using click-to-load privacy-enhanced YouTube embeds, and client-side site search.

### Phase 4: Conversion and community
> Build a dedicated multi-step lead page (need → people/age/city/conditions → contact + DPDP-style consent), a quick lead form on the home page, a sticky mobile CTA, and "free advice" CTAs on every tool and guide. Add Support (donation tiers, purpose selector, pledge form, UPI/Razorpay/PayPal/Stripe/Buy-Me-a-Coffee links switchable in `assets/js/config.js`), Contests (four seasonal challenges, rules FAQ, entry form), Careers (eight roles, application form) and Advertise & Partner (lead partnerships, sponsorships, CSR camps, domain/website enquiries).

### Phase 5: Launch and growth (after this build)
> 1) Point nirog.com DNS to GitHub Pages and add a `CNAME` file. 2) Submit to Google Search Console and apply for AdSense once the domain serves the site. 3) Activate the form relay with the first test submission. 4) Sign an affiliate/lead agreement with an IRDAI-licensed broker and an accredited lab chain. 5) Recruit two medical reviewers and add reviewer credits to guides. 6) Publish Hindi versions of the top 20 pages, then 2 new guides a week. 7) Add manual ad units (in-article, after tools) once AdSense issues slot IDs.

## 3. Feature checklist delivered in this repo
See `RESEARCH.md` for the 36+ site competitive review and the full adopted-feature checklist.
