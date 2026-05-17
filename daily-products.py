#!/usr/bin/env python3
"""
DealsGlobe Daily Product Generator
===================================
Runs every day via GitHub Actions at 7am UTC.
Generates 5 deep product review pages per language = 50 pages/day.
Each page: full in-depth review, pros/cons, FAQ schema, affiliate links,
email capture, internal links — all localised for the target country.

Languages: EN-US, EN-GB, EN-CA, DE, FR, ES, IT, NL, PL, SE
Products: rotated from a pool of 200+ high-commission, low-competition items
"""

import os, json, re, datetime, random, urllib.request, urllib.error, hashlib

# ── CONFIG ─────────────────────────────────────────────────────────────────────
TAG        = "brightlane201-20"
API_KEY    = os.environ.get("ANTHROPIC_API_KEY", "")
BASE_URL   = "https://globesitenetwork.github.io/DealsGlobe/"
TODAY      = datetime.date.today().isoformat()
TODAY_NICE = datetime.date.today().strftime("%B %d, %Y")
SEED       = int(datetime.date.today().strftime("%Y%m%d"))  # same seed = reproducible daily set

LANGUAGES = [
    {"code":"en-us","country":"US","lang":"English","flag":"🇺🇸","currency":"$","domain":"amazon.com",     "locale_note":"US readers. Use USD. Reference Walmart and Target as price comparisons."},
    {"code":"en-gb","country":"GB","lang":"English","flag":"🇬🇧","currency":"£","domain":"amazon.co.uk",  "locale_note":"UK readers. Use GBP (£). Reference Argos, Currys, John Lewis as comparisons. Use British spelling."},
    {"code":"en-ca","country":"CA","lang":"English","flag":"🇨🇦","currency":"CA$","domain":"amazon.ca",   "locale_note":"Canadian readers. Use CAD (CA$). Reference Canadian Tire, Best Buy Canada as comparisons."},
    {"code":"de",   "country":"DE","lang":"German", "flag":"🇩🇪","currency":"€","domain":"amazon.de",     "locale_note":"German readers. Write entirely in German. Use EUR (€). Reference MediaMarkt, Saturn as comparisons. Formal but friendly tone."},
    {"code":"fr",   "country":"FR","lang":"French", "flag":"🇫🇷","currency":"€","domain":"amazon.fr",     "locale_note":"French readers. Write entirely in French. Use EUR (€). Reference Fnac, Darty as comparisons. Professional tone."},
    {"code":"es",   "country":"ES","lang":"Spanish","flag":"🇪🇸","currency":"€","domain":"amazon.es",     "locale_note":"Spanish readers (Spain). Write entirely in Spanish. Use EUR (€). Reference El Corte Inglés, MediaMarkt España as comparisons."},
    {"code":"it",   "country":"IT","lang":"Italian","flag":"🇮🇹","currency":"€","domain":"amazon.it",     "locale_note":"Italian readers. Write entirely in Italian. Use EUR (€). Reference Unieuro, Mediaworld as comparisons."},
    {"code":"nl",   "country":"NL","lang":"Dutch",  "flag":"🇳🇱","currency":"€","domain":"amazon.nl",     "locale_note":"Dutch readers. Write entirely in Dutch. Use EUR (€). Reference Bol.com, MediaMarkt Nederland as comparisons."},
    {"code":"pl",   "country":"PL","lang":"Polish", "flag":"🇵🇱","currency":"zł","domain":"amazon.pl",    "locale_note":"Polish readers. Write entirely in Polish. Use PLN (zł). Reference Media Expert, RTV Euro AGD as comparisons."},
    {"code":"se",   "country":"SE","lang":"Swedish","flag":"🇸🇪","currency":"kr","domain":"amazon.se",    "locale_note":"Swedish readers. Write entirely in Swedish. Use SEK (kr). Reference Elgiganten, Webhallen as comparisons."},
]

# ── PRODUCT POOL ───────────────────────────────────────────────────────────────
# 200+ products across high-commission, low-competition niches
# Format: (search_keyword, category, commission_pct, avg_price_usd, niche_angle)
PRODUCTS = [
    # LUXURY BEAUTY — 10% commission
    ("retinol serum face anti-aging", "Luxury Beauty", 10, 45, "anti-aging skincare"),
    ("vitamin c brightening serum", "Luxury Beauty", 10, 35, "skin brightening"),
    ("hyaluronic acid moisturiser", "Luxury Beauty", 10, 30, "hydration skincare"),
    ("niacinamide serum pores", "Luxury Beauty", 10, 25, "pore minimising"),
    ("collagen face cream anti-aging", "Luxury Beauty", 10, 55, "collagen skincare"),
    ("AHA BHA exfoliating toner", "Luxury Beauty", 10, 28, "chemical exfoliant"),
    ("peptide eye cream dark circles", "Luxury Beauty", 10, 40, "eye care"),
    ("snail mucin essence korean skincare", "Luxury Beauty", 10, 22, "K-beauty"),
    ("rosehip oil face serum organic", "Luxury Beauty", 10, 18, "natural skincare"),
    ("glycolic acid toner exfoliant", "Luxury Beauty", 10, 24, "skin renewal"),
    ("azelaic acid cream rosacea", "Luxury Beauty", 10, 32, "redness skincare"),
    ("bakuchiol retinol alternative", "Luxury Beauty", 10, 38, "natural retinol"),
    ("tranexamic acid dark spots", "Luxury Beauty", 10, 42, "hyperpigmentation"),
    ("ceramide moisturiser barrier repair", "Luxury Beauty", 10, 28, "skin barrier"),
    ("squalane face oil lightweight", "Luxury Beauty", 10, 20, "face oil"),

    # FURNITURE — 8% commission, very weak affiliate coverage
    ("standing desk adjustable height electric", "Furniture", 8, 350, "home office"),
    ("monitor arm desk mount dual", "Furniture", 8, 45, "desk setup"),
    ("ergonomic footrest under desk", "Furniture", 8, 30, "posture"),
    ("lumbar support pillow office chair", "Furniture", 8, 35, "back pain"),
    ("laptop stand adjustable aluminium", "Furniture", 8, 28, "laptop ergonomics"),
    ("keyboard tray under desk drawer", "Furniture", 8, 55, "desk organisation"),
    ("cable management box desk", "Furniture", 8, 20, "desk organisation"),
    ("monitor riser with storage", "Furniture", 8, 38, "desk setup"),
    ("desk pad large leather", "Furniture", 8, 25, "desk accessories"),
    ("pegboard organiser wall mounted", "Furniture", 8, 40, "wall organisation"),
    ("floating shelf wall mounted", "Furniture", 8, 32, "home storage"),
    ("bookcase 5 tier modern", "Furniture", 8, 89, "home furniture"),
    ("bed frame platform no box spring", "Furniture", 8, 220, "bedroom"),
    ("nightstand with usb charging", "Furniture", 8, 75, "bedroom furniture"),
    ("coffee table with storage ottomans", "Furniture", 8, 180, "living room"),

    # HOME IMPROVEMENT — 8% commission
    ("smart light switch no neutral wire", "Home Improvement", 8, 35, "smart home"),
    ("water filter under sink", "Home Improvement", 8, 120, "water quality"),
    ("shower head high pressure filter", "Home Improvement", 8, 45, "bathroom"),
    ("door lock smart keypad fingerprint", "Home Improvement", 8, 89, "smart security"),
    ("motion sensor light outdoor solar", "Home Improvement", 8, 28, "outdoor lighting"),
    ("leak detector water sensor wifi", "Home Improvement", 8, 25, "home monitoring"),
    ("programmable thermostat non-smart", "Home Improvement", 8, 30, "energy saving"),
    ("door draft stopper energy saving", "Home Improvement", 8, 12, "home insulation"),
    ("pipe insulation foam wrap", "Home Improvement", 8, 15, "home insulation"),
    ("weather stripping door seal", "Home Improvement", 8, 14, "home insulation"),

    # GARDEN — 8% commission, almost no affiliate pages
    ("raised garden bed metal galvanised", "Garden", 8, 85, "vegetable garden"),
    ("compost bin kitchen countertop", "Garden", 8, 35, "composting"),
    ("soaker hose garden irrigation", "Garden", 8, 22, "garden watering"),
    ("kneeler garden bench foldable", "Garden", 8, 40, "garden tools"),
    ("grow light led indoor plants", "Garden", 8, 55, "indoor gardening"),
    ("seed starting kit greenhouse mini", "Garden", 8, 28, "seed starting"),
    ("drip irrigation kit garden", "Garden", 8, 45, "garden watering"),
    ("garden hose expandable 100ft", "Garden", 8, 35, "garden tools"),
    ("solar garden lights pathway", "Garden", 8, 24, "garden lighting"),
    ("bird feeder squirrel proof pole", "Garden", 8, 38, "wildlife garden"),
    ("rain gauge digital wireless", "Garden", 8, 30, "garden monitoring"),
    ("potting mix raised beds organic", "Garden", 8, 18, "soil"),
    ("frost cloth plant protection", "Garden", 8, 20, "plant protection"),
    ("pruning shears bypass sharp", "Garden", 8, 22, "garden tools"),
    ("lawn edger manual rotary", "Garden", 8, 30, "lawn care"),

    # HEALTH & PERSONAL CARE — 4.5% but massive volume
    ("blood pressure monitor upper arm", "Health", 4.5, 45, "health monitoring"),
    ("pulse oximeter fingertip", "Health", 4.5, 20, "health monitoring"),
    ("glucose meter blood sugar monitor", "Health", 4.5, 25, "diabetes care"),
    ("heating pad electric back pain", "Health", 4.5, 28, "pain relief"),
    ("tens unit muscle pain relief", "Health", 4.5, 35, "pain relief"),
    ("foam roller muscle recovery", "Health", 4.5, 22, "recovery"),
    ("massage gun deep tissue", "Health", 4.5, 89, "muscle recovery"),
    ("ice pack reusable gel", "Health", 4.5, 15, "pain relief"),
    ("knee brace compression support", "Health", 4.5, 18, "joint support"),
    ("back brace posture corrector", "Health", 4.5, 22, "posture"),
    ("wrist brace carpal tunnel", "Health", 4.5, 16, "repetitive strain"),
    ("sleep mask contoured 3d", "Health", 4.5, 18, "sleep"),
    ("earplugs noise reduction sleep", "Health", 4.5, 12, "sleep"),
    ("humidifier bedroom cool mist", "Health", 4.5, 45, "air quality"),
    ("air purifier hepa bedroom", "Health", 4.5, 89, "air quality"),
    ("neti pot nasal rinse", "Health", 4.5, 14, "sinus health"),
    ("resistance bands set fabric", "Health", 4.5, 25, "exercise"),
    ("balance board wobble", "Health", 4.5, 30, "core fitness"),
    ("jump rope speed weighted", "Health", 4.5, 18, "cardio"),
    ("yoga block cork set", "Health", 4.5, 22, "yoga"),

    # PET SUPPLIES — 4.5%, high volume, emotional buyers
    ("cat water fountain stainless steel", "Pet Supplies", 4.5, 35, "cat hydration"),
    ("dog crate foldable heavy duty", "Pet Supplies", 4.5, 65, "dog containment"),
    ("automatic pet feeder wifi", "Pet Supplies", 4.5, 55, "pet feeding"),
    ("cat tree condo scratching post", "Pet Supplies", 4.5, 75, "cat furniture"),
    ("dog harness no pull front clip", "Pet Supplies", 4.5, 28, "dog walking"),
    ("interactive cat toy automatic", "Pet Supplies", 4.5, 22, "cat enrichment"),
    ("dog puzzle toy slow feeder", "Pet Supplies", 4.5, 18, "dog enrichment"),
    ("cat litter mat waterproof", "Pet Supplies", 4.5, 20, "cat litter"),
    ("self cleaning litter box automatic", "Pet Supplies", 4.5, 199, "cat litter"),
    ("dog bed orthopedic memory foam", "Pet Supplies", 4.5, 55, "dog comfort"),
    ("pet camera treat dispenser wifi", "Pet Supplies", 4.5, 89, "pet monitoring"),
    ("flea treatment prevention topical", "Pet Supplies", 4.5, 35, "pet health"),
    ("dog dental chews plaque", "Pet Supplies", 4.5, 18, "pet dental"),
    ("cat scratching board cardboard", "Pet Supplies", 4.5, 14, "cat scratching"),
    ("dog anxiety vest thundershirt", "Pet Supplies", 4.5, 38, "dog anxiety"),

    # SPORTS — 4.5%, evergreen, weak affiliate content
    ("swim goggles anti fog adults", "Sports", 4.5, 18, "swimming"),
    ("cycling gloves padded", "Sports", 4.5, 20, "cycling"),
    ("running belt waist phone", "Sports", 4.5, 15, "running"),
    ("gym bag with wet dry compartment", "Sports", 4.5, 35, "gym"),
    ("weightlifting belt leather", "Sports", 4.5, 45, "powerlifting"),
    ("pull up bar doorway", "Sports", 4.5, 28, "calisthenics"),
    ("ab roller wheel core", "Sports", 4.5, 18, "core fitness"),
    ("resistance loop bands set", "Sports", 4.5, 14, "stretching"),
    ("dumbbell set adjustable", "Sports", 4.5, 89, "home gym"),
    ("kettlebell cast iron", "Sports", 4.5, 35, "strength training"),
    ("yoga mat thick non-slip", "Sports", 4.5, 28, "yoga"),
    ("foam roller grid deep tissue", "Sports", 4.5, 22, "recovery"),
    ("skipping rope speed competition", "Sports", 4.5, 16, "cardio"),
    ("lacrosse ball massage", "Sports", 4.5, 10, "muscle recovery"),
    ("exercise bike stationary magnetic", "Sports", 4.5, 180, "cardio fitness"),

    # KITCHEN — 4.5%, specific products ignored by big sites
    ("rice cooker fuzzy logic", "Kitchen", 4.5, 55, "cooking"),
    ("electric kettle temperature control", "Kitchen", 4.5, 35, "hot drinks"),
    ("cast iron skillet pre-seasoned", "Kitchen", 4.5, 25, "cookware"),
    ("instant pot pressure cooker 6qt", "Kitchen", 4.5, 89, "pressure cooking"),
    ("air fryer oven toaster combo", "Kitchen", 4.5, 99, "air frying"),
    ("knife sharpener electric 3 stage", "Kitchen", 4.5, 28, "knife care"),
    ("cutting board bamboo large", "Kitchen", 4.5, 22, "food prep"),
    ("silicone baking mat reusable", "Kitchen", 4.5, 14, "baking"),
    ("mandoline slicer adjustable", "Kitchen", 4.5, 25, "food prep"),
    ("food scale digital grams", "Kitchen", 4.5, 12, "cooking accuracy"),
    ("salad spinner large", "Kitchen", 4.5, 20, "food prep"),
    ("immersion blender handheld", "Kitchen", 4.5, 35, "blending"),
    ("dutch oven enameled cast iron", "Kitchen", 4.5, 45, "slow cooking"),
    ("beeswax food wraps reusable", "Kitchen", 4.5, 16, "food storage"),
    ("meal prep containers glass", "Kitchen", 4.5, 30, "meal prep"),

    # NICHE / IGNORED — very high traffic, almost zero affiliate coverage
    ("grounding mat earthing sheet bed", "Health", 4.5, 55, "earthing wellness"),
    ("red light therapy device panel", "Health", 4.5, 89, "light therapy"),
    ("sauna blanket infrared", "Health", 4.5, 150, "home sauna"),
    ("cold plunge tub portable", "Sports", 4.5, 120, "cold therapy"),
    ("vibration plate exercise machine", "Sports", 4.5, 99, "whole body vibration"),
    ("inversion table back decompression", "Health", 4.5, 120, "back pain"),
    ("percussion massager attachments", "Health", 4.5, 35, "muscle therapy"),
    ("acupressure mat pillow set", "Health", 4.5, 30, "acupressure"),
    ("himalayan salt lamp large", "Home", 4.5, 25, "air ionisation"),
    ("essential oil diffuser ultrasonic", "Home", 4.5, 28, "aromatherapy"),
    ("under-desk bike pedal exerciser", "Sports", 4.5, 45, "desk fitness"),
    ("blue light glasses computer", "Health", 4.5, 20, "eye health"),
    ("posture corrector brace back", "Health", 4.5, 25, "posture"),
    ("sleep tracker ring oura style", "Health", 4.5, 89, "sleep monitoring"),
    ("standing mat anti-fatigue kitchen", "Home Improvement", 8, 35, "kitchen comfort"),
]

# ── CLAUDE API CALL ─────────────────────────────────────────────────────────────
def claude(prompt, system, max_tokens=2000):
    if not API_KEY:
        return None
    data = json.dumps({
        "model": "claude-sonnet-4-20250514",
        "max_tokens": max_tokens,
        "system": system,
        "messages": [{"role": "user", "content": prompt}]
    }).encode()
    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=data,
        headers={"Content-Type": "application/json", "x-api-key": API_KEY, "anthropic-version": "2023-06-01"}
    )
    try:
        with urllib.request.urlopen(req, timeout=45) as r:
            return json.loads(r.read())["content"][0]["text"]
    except Exception as e:
        print(f"    API error: {e}")
        return None

# ── PAGE BUILDER ────────────────────────────────────────────────────────────────
def build_page(product, lang):
    keyword, category, commission, price_usd, niche = product
    lc = lang["code"]
    cc = lang["country"]
    flag = lang["flag"]
    currency = lang["currency"]
    domain = lang["domain"]
    language = lang["lang"]
    locale_note = lang["locale_note"]

    # Price conversion (rough)
    rates = {"$":1.0,"£":0.79,"CA$":1.35,"€":0.92,"zł":4.0,"kr":10.5}
    local_price = f"{currency}{price_usd * rates.get(currency, 1.0):.0f}"

    amz_url = f"https://www.{domain}/s?k={keyword.replace(' ','+')}&tag={TAG}"

    system = f"""You are a world-class Amazon affiliate product reviewer writing for {language}-speaking readers in {cc}.
{locale_note}
Write in {language} ONLY (except for product names which can stay in English).
Be specific, helpful, honest. Include real use cases. Do NOT mention competitor affiliate sites.
Format output as clean HTML using only these tags: h1, h2, h3, p, ul, li, strong, em, table, tr, th, td.
No CSS, no style attributes, no div tags — just semantic content HTML."""

    prompt = f"""Write a detailed in-depth product review page for Amazon affiliate marketing.

Product: {keyword}
Category: {category}
Typical price: {local_price}
Commission: {commission}%
Target audience: {language} speakers in {cc}
Date: {TODAY_NICE}

Write the following sections IN {language.upper()}:

1. H1 title — include the product keyword and year (2026)
2. Introduction paragraph (150 words) — what problem does this solve, who needs it
3. H2: Key Features — bullet list of 6-8 specific features buyers care about
4. H2: Who Is This For — 3 specific buyer personas with real use cases  
5. H2: Pros and Cons — honest pros (5) and cons (3) as bullet lists
6. H2: What to Look For When Buying — 5 specific buying criteria explained
7. H2: Price and Value — is it worth it, how does {local_price} compare to alternatives
8. H2: Our Verdict — strong recommendation paragraph with clear CTA
9. H2: FAQ — 4 questions and answers specific to this product

Make it feel like a real expert wrote this, not AI. Include specific details, real numbers, practical advice.
Reference local stores ({locale_note}) for price comparisons where relevant."""

    content = claude(prompt, system, max_tokens=2000)
    if not content:
        # Fallback placeholder
        content = f"<h1>{keyword.title()} — Review 2026</h1><p>Product review coming soon.</p>"

    # Extract title from H1
    title_match = re.search(r'<h1[^>]*>(.*?)</h1>', content, re.IGNORECASE | re.DOTALL)
    page_title = re.sub('<[^>]+>', '', title_match.group(1)) if title_match else f"{keyword.title()} Review 2026"

    # Slug
    slug_base = re.sub(r'[^a-z0-9]+', '-', keyword.lower()).strip('-')
    slug = f"reviews/{lc}/{slug_base}.html"
    os.makedirs(f"reviews/{lc}", exist_ok=True)

    # FAQ schema — extract from content
    faq_items = re.findall(r'<h[23][^>]*>(.*?)</h[23]>.*?<p>(.*?)</p>', content[content.lower().find('faq'):content.lower().find('faq')+3000] if 'faq' in content.lower() else '', re.IGNORECASE | re.DOTALL)
    faq_schema_items = [f'{{"@type":"Question","name":"{re.sub(chr(34), chr(39), re.sub(chr(60)+"[^>]+"+chr(62),"",q))}","acceptedAnswer":{{"@type":"Answer","text":"{re.sub(chr(34), chr(39), re.sub(chr(60)+"[^>]+"+chr(62),"",a[:200]))}"}}}}' for q,a in faq_items[:4]]
    faq_schema = f'{{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{",".join(faq_schema_items)}]}}' if faq_schema_items else '{}'

    html = f'''<!DOCTYPE html>
<html lang="{lc}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{page_title} | DealsGlobe</title>
<meta name="description" content="In-depth review: {keyword}. Best price on {domain}. Expert verdict, pros & cons, buying guide. Updated {TODAY_NICE}.">
<meta name="robots" content="index,follow">
<link rel="canonical" href="{BASE}{slug}">
<script type="application/ld+json">{faq_schema}</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<style>
:root{{--o:#FF9900;--d:#0f1111;--s:#1a1f2e;--c:#1e2432;--b:#2d3548;--t:#f0f2f5;--m:#8491a5;--g:#00c853;}}
*{{box-sizing:border-box;margin:0;padding:0;}}
body{{font-family:"DM Sans",sans-serif;background:var(--d);color:var(--t);line-height:1.7;}}
nav{{position:sticky;top:0;z-index:100;background:#232F3E;border-bottom:1px solid #1a2030;display:flex;align-items:center;justify-content:space-between;padding:0 24px;height:58px;}}
.logo{{font-family:"Syne",sans-serif;font-size:20px;font-weight:800;color:var(--t);text-decoration:none;}}
.logo span{{color:var(--o);}}
.nav-cta{{background:var(--o);color:#111;padding:7px 16px;border-radius:6px;font-weight:700;font-size:13px;text-decoration:none;}}
.hero{{background:radial-gradient(ellipse at 50% 0%,#2a1800 0%,var(--d) 70%);padding:52px 24px 32px;text-align:center;border-bottom:1px solid var(--b);}}
.flag{{font-size:28px;margin-bottom:8px;}}
.badge{{display:inline-block;background:var(--o);color:#111;font-size:11px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;padding:4px 14px;border-radius:20px;margin-bottom:12px;}}
.meta{{color:var(--m);font-size:12px;margin-top:8px;}}
.updated{{display:inline-block;background:var(--s);border:1px solid var(--b);border-radius:4px;padding:3px 10px;font-size:11px;color:var(--m);margin-bottom:16px;}}
.buy-hero{{display:inline-flex;align-items:center;gap:10px;background:var(--o);color:#111;font-weight:800;font-size:16px;padding:16px 32px;border-radius:8px;text-decoration:none;margin-top:16px;transition:opacity .2s;}}
.buy-hero:hover{{opacity:.88;}}
.price-tag{{background:#111;color:var(--o);font-size:14px;padding:4px 12px;border-radius:4px;}}
.content{{max-width:820px;margin:0 auto;padding:40px 24px;}}
.content h1{{font-family:"Syne",sans-serif;font-size:clamp(24px,4vw,40px);font-weight:800;line-height:1.15;margin-bottom:20px;color:var(--t);}}
.content h2{{font-family:"Syne",sans-serif;font-size:22px;font-weight:800;margin:36px 0 14px;color:var(--t);padding-bottom:8px;border-bottom:1px solid var(--b);}}
.content h3{{font-size:17px;font-weight:700;margin:20px 0 8px;color:var(--t);}}
.content p{{color:#ccc;margin-bottom:16px;font-size:15px;}}
.content ul{{margin:0 0 16px 20px;color:#ccc;font-size:15px;}}
.content ul li{{margin-bottom:8px;}}
.content li strong{{color:var(--t);}}
.content a{{color:var(--o);text-decoration:none;}}
.content a:hover{{text-decoration:underline;}}
.content table{{width:100%;border-collapse:collapse;margin:20px 0;font-size:14px;}}
.content th{{background:var(--s);color:var(--t);padding:10px 14px;text-align:left;border:1px solid var(--b);font-weight:700;}}
.content td{{padding:10px 14px;border:1px solid var(--b);color:#ccc;}}
.content tr:nth-child(even) td{{background:#161c28;}}
.buy-box{{background:linear-gradient(135deg,#2a1800,#1a1200);border:2px solid var(--o);border-radius:14px;padding:28px;margin:32px 0;text-align:center;}}
.buy-box h3{{font-family:"Syne",sans-serif;font-size:20px;font-weight:800;margin-bottom:8px;color:var(--o);}}
.buy-box p{{color:var(--m);font-size:13px;margin-bottom:16px;}}
.buy-box .price{{font-family:"Syne",sans-serif;font-size:32px;font-weight:800;color:var(--o);margin-bottom:4px;}}
.buy-box .was{{font-size:14px;color:var(--m);text-decoration:line-through;margin-bottom:16px;}}
.buy-btn{{display:inline-block;background:var(--o);color:#111;font-weight:800;font-size:15px;padding:14px 32px;border-radius:8px;text-decoration:none;transition:opacity .2s;}}
.buy-btn:hover{{opacity:.88;text-decoration:none;}}
.verdict{{background:var(--s);border-left:4px solid var(--o);border-radius:0 10px 10px 0;padding:20px 24px;margin:28px 0;}}
.verdict h3{{color:var(--o);font-size:16px;font-weight:700;margin-bottom:8px;}}
.verdict p{{color:#ccc;margin:0;font-size:14px;}}
.email-cap{{background:linear-gradient(135deg,#1a0f00,#0a0f1a);border:1px solid var(--o);border-radius:12px;padding:24px;text-align:center;margin:32px 0;}}
.email-cap h3{{font-family:"Syne",sans-serif;font-size:18px;font-weight:800;margin-bottom:6px;}}
.email-cap p{{color:var(--m);font-size:13px;margin-bottom:14px;}}
.ecf{{display:flex;gap:8px;max-width:380px;margin:0 auto;flex-wrap:wrap;justify-content:center;}}
.ecf input{{flex:1;min-width:180px;background:#1a1a1a;border:1px solid var(--b);color:var(--t);padding:10px 14px;border-radius:6px;font-size:14px;outline:none;}}
.ecf input:focus{{border-color:var(--o);}}
.ecf button{{background:var(--o);color:#111;border:none;padding:10px 18px;border-radius:6px;font-weight:700;font-size:14px;cursor:pointer;}}
#cm{{font-size:12px;color:var(--g);margin-top:8px;}}
.network-bar{{background:#232F3E;border-top:1px solid #1a2030;padding:12px 24px;display:flex;align-items:center;gap:12px;flex-wrap:wrap;justify-content:center;margin-top:40px;}}
.network-bar span{{font-size:11px;color:var(--m);letter-spacing:1px;text-transform:uppercase;font-weight:700;}}
.network-bar a{{background:var(--c);border:1px solid var(--b);border-radius:20px;padding:5px 14px;font-size:12px;font-weight:600;color:var(--t);text-decoration:none;transition:border-color .2s;}}
.network-bar a:hover{{border-color:var(--o);color:var(--o);}}
footer{{background:#232F3E;border-top:1px solid #1a2030;padding:20px 24px;text-align:center;font-size:12px;color:var(--m);line-height:1.8;}}
@media(max-width:600px){{.content{{padding:24px 16px;}}.buy-hero{{font-size:14px;padding:12px 20px;}}}}
</style>
</head>
<body>
<nav>
  <a class="logo" href="{BASE}">Deals<span>Globe</span> 🌍</a>
  <a class="nav-cta" href="{amz_url}" target="_blank" rel="noopener">Shop Amazon {flag} →</a>
</nav>

<div class="hero">
  <div class="flag">{flag}</div>
  <div class="badge">📋 In-Depth Review · {language} · {cc}</div>
  <div class="updated">🕐 Updated: {TODAY_NICE}</div>
  <a class="buy-hero" href="{amz_url}" target="_blank" rel="noopener">
    🛒 View on Amazon {flag} <span class="price-tag">{local_price}</span>
  </a>
  <div class="meta">✅ Free Prime shipping · 30-day returns · {commission}% commission</div>
</div>

<div class="content">
  {content}

  <div class="buy-box">
    <h3>🛒 Best Price on Amazon {flag}</h3>
    <p>Free Prime shipping · 30-day returns · Secure checkout</p>
    <div class="price">{local_price}</div>
    <a class="buy-btn" href="{amz_url}" target="_blank" rel="noopener">View on Amazon {flag} →</a>
  </div>

  <div class="email-cap">
    <h3>📬 Get Daily Amazon Deal Alerts</h3>
    <p>Best deals for {cc} shoppers — delivered daily. No spam.</p>
    <div class="ecf">
      <input type="email" id="ce" placeholder="your@email.com"/>
      <button onclick="ce2()">Subscribe →</button>
    </div>
    <div id="cm"></div>
  </div>

  <p>👉 <a href="{BASE}">Back to DealsGlobe</a> · <a href="{BASE}best-ergonomic-office-chair-amazon.html">Office Chairs</a> · <a href="{BASE}best-sleep-aids-amazon.html">Sleep Aids</a> · <a href="{BASE}portable-power-station-amazon.html">Power Stations</a></p>
</div>

<div class="network-bar">
  <span>🔗 Our Network</span>
  <a href="{BASE}">🌍 DealsGlobe</a>
  <a href="https://brightlane.github.io/shopppingonline/">🛒 ShoppingOnline</a>
  <a href="https://brightlane.github.io/ShopAliexpressOnline/">🛍️ AliDeals</a>
</div>

<footer>
  <p>As an Amazon Associate we earn from qualifying purchases at no extra cost to you.</p>
  <p>© 2026 DealsGlobe · Tag: {TAG} · {flag} {domain}</p>
</footer>

<script>
function ce2(){{var e=document.getElementById("ce").value.trim();var m=document.getElementById("cm");if(!e||!e.includes("@")){{m.textContent="Enter a valid email";m.style.color="#ff4444";return;}}var s=JSON.parse(localStorage.getItem("dg_subs")||"[]");if(s.find(x=>x.email===e)){{m.textContent="Already subscribed!";return;}}s.push({{email:e,date:new Date().toISOString()}});localStorage.setItem("dg_subs",JSON.stringify(s));m.textContent="✅ Deal alerts on the way!";m.style.color="#00c853";document.getElementById("ce").value="";}}
</script>
</body>
</html>'''

    return slug, html, page_title

# ── SITEMAP UPDATER ─────────────────────────────────────────────────────────────
def update_sitemap(new_slugs):
    sitemap_path = "sitemap.xml"
    if os.path.exists(sitemap_path):
        with open(sitemap_path) as f:
            sitemap = f.read()
    else:
        sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n</urlset>'

    # Update existing lastmod dates
    sitemap = re.sub(r'<lastmod>\d{4}-\d{2}-\d{2}</lastmod>', f'<lastmod>{TODAY}</lastmod>', sitemap)

    # Add new URLs
    added = 0
    for slug in new_slugs:
        url = f"{BASE_URL}{slug}"
        if url not in sitemap:
            entry = f'''  <url>
    <loc>{url}</loc>
    <lastmod>{TODAY}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>'''
            sitemap = sitemap.replace('</urlset>', f'{entry}\n</urlset>')
            added += 1

    with open(sitemap_path, 'w') as f:
        f.write(sitemap)
    print(f"  ✅ Sitemap: +{added} URLs added")

# ── MAIN ────────────────────────────────────────────────────────────────────────
def main():
    print(f"\n🌍 DealsGlobe Daily Product Generator — {TODAY}")
    print(f"   Generating 5 products × {len(LANGUAGES)} languages = {5 * len(LANGUAGES)} pages\n")

    # Pick 5 products for today using date as seed (consistent per day)
    rng = random.Random(SEED)
    todays_products = rng.sample(PRODUCTS, 5)

    print("📦 Today's products:")
    for i, p in enumerate(todays_products, 1):
        print(f"   {i}. {p[0]} ({p[1]}, {p[2]}% commission)")

    all_slugs = []
    total = 0

    for product in todays_products:
        keyword = product[0]
        print(f"\n🔄 {keyword}")
        for lang in LANGUAGES:
            print(f"   {lang['flag']} {lang['lang']}...", end=" ", flush=True)
            try:
                slug, html, title = build_page(product, lang)
                with open(slug, 'w', encoding='utf-8') as f:
                    f.write(html)
                all_slugs.append(slug)
                total += 1
                print(f"✅ {slug}")
            except Exception as e:
                print(f"❌ Error: {e}")

    update_sitemap(all_slugs)
    print(f"\n✅ Done — {total} pages generated and saved\n")

if __name__ == "__main__":
    main()
