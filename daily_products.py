#!/usr/bin/env python3
import os,re,json,random,datetime
TAG="brightlane201-20"
BASE="https://brightlane.github.io/shopppingonline/"
TODAY=datetime.date.today().isoformat()
TODAY_NICE=datetime.date.today().strftime("%B %d, %Y")
SEED=int(datetime.date.today().strftime("%Y%m%d"))
RATES={"$":1.0,"£":0.79,"CA$":1.35,"€":0.92,"zł":4.0,"kr":10.5}
DOMAINS={"US":"amazon.com","GB":"amazon.co.uk","CA":"amazon.ca","DE":"amazon.de","FR":"amazon.fr","ES":"amazon.es","IT":"amazon.it","NL":"amazon.nl","PL":"amazon.pl","SE":"amazon.se"}
LANGS=[
{"code":"en-us","cc":"US","flag":"🇺🇸","cur":"$","buy":"View on Amazon","prime":"Free Prime shipping"},
{"code":"en-gb","cc":"GB","flag":"🇬🇧","cur":"£","buy":"View on Amazon UK","prime":"Free Prime delivery"},
{"code":"en-ca","cc":"CA","flag":"🇨🇦","cur":"CA$","buy":"View on Amazon Canada","prime":"Free Prime shipping"},
{"code":"de","cc":"DE","flag":"🇩🇪","cur":"€","buy":"Bei Amazon ansehen","prime":"Kostenloser Prime-Versand"},
{"code":"fr","cc":"FR","flag":"🇫🇷","cur":"€","buy":"Voir sur Amazon","prime":"Livraison Prime gratuite"},
{"code":"es","cc":"ES","flag":"🇪🇸","cur":"€","buy":"Ver en Amazon","prime":"Envío Prime gratis"},
{"code":"it","cc":"IT","flag":"🇮🇹","cur":"€","buy":"Vedi su Amazon","prime":"Spedizione Prime gratuita"},
{"code":"nl","cc":"NL","flag":"🇳🇱","cur":"€","buy":"Bekijk op Amazon","prime":"Gratis Prime levering"},
{"code":"pl","cc":"PL","flag":"🇵🇱","cur":"zł","buy":"Zobacz na Amazon","prime":"Darmowa dostawa Prime"},
{"code":"se","cc":"SE","flag":"🇸🇪","cur":"kr","buy":"Se på Amazon","prime":"Gratis Prime-leverans"},
]
PRODUCTS=[
{"kw":"echo dot 5th gen alexa","name":"Echo Dot 5th Gen","emoji":"🔊","cat":"Smart Home","usd":24.99,"was":49.99,"stars":5,"rev":"89,000","sold":"50,000+",
"feats":["Alexa voice assistant built-in","Improved bass and clearer audio","Built-in motion and temperature sensors","Multi-room audio with other Echo devices","Works with 100,000+ smart home devices","Compact sphere design for any room"],
"pros":["Exceptional value under $25","Works with every smart home platform","Best sound of any Echo Dot yet","Motion sensor enables powerful automations","5-minute setup via the Alexa app"],
"cons":["Not a replacement for a proper speaker","Requires Wi-Fi","Always-on microphone concerns for some"],
"tips":["Watch for Prime Day deals — drops to $15-18","Bundle with smart plug for instant automation","Clock display version suits bedrooms","Buy multipacks for whole-home coverage","Explore Alexa routines after setup — they unlock real value"],
"faqs":[("What can Echo Dot do?","Controls smart home, plays music, answers questions, sets timers, makes calls and runs thousands of Alexa skills. The motion sensor triggers automations automatically."),("Need Prime?","No. You need an Amazon account but not Prime. You can still use Spotify, Apple Music and other services."),("How many can you have?","Unlimited. Most households put one per room for multi-room audio and whole-home voice control."),("Worth upgrading from 4th Gen?","Yes — adds motion sensor, temperature sensor and improved bass. For new buyers, always choose 5th Gen.")]},
{"kw":"air fryer 5.8qt digital 1700w","name":"Digital Air Fryer 5.8QT","emoji":"🍳","cat":"Kitchen","usd":39.99,"was":89.99,"stars":5,"rev":"41,000","sold":"20,000+",
"feats":["5.8QT capacity for family portions","1700W for fast even cooking","8 preset cooking modes","Temperature 180-400°F","Dishwasher-safe basket","60-minute auto shutoff timer"],
"pros":["Cooks with 80% less oil than deep frying","Preheats in under 3 minutes","Dishwasher-safe basket — easy cleanup","Significantly cheaper to run than a full oven","Large enough for a whole chicken"],
"cons":["Takes up counter space","Flat items like thin pizzas cook unevenly","Settings take 2-3 uses to dial in"],
"tips":["5.8QT is the ideal size for 2-4 people","1700W heats faster than 1200W budget models","Dishwasher-safe basket is non-negotiable","Preheat 3 minutes for more consistent results","A viewing window lets you check food without opening"],
"faqs":[("What can you cook?","Fries, wings, salmon, vegetables, bacon, frozen foods, steak and small cakes. Handles a whole chicken under 4lbs."),("Does it taste as good as deep frying?","For most foods, very close — crispy outside, moist inside. 90% of recipes produce excellent results."),("How much electricity?","Running 20 minutes costs approximately 7 cents at US average rates — far cheaper than a full oven."),("What size do I need?","1-2 people: 2-3QT. 3-4 people: 5.8QT. 5+ people: 6QT+.")]},
{"kw":"kindle paperwhite 16gb waterproof ereader","name":"Kindle Paperwhite 16GB","emoji":"📖","cat":"Electronics","usd":99.99,"was":149.99,"stars":5,"rev":"71,000","sold":"40,000+",
"feats":["6.8-inch 300ppi glare-free display","Adjustable warm light","IPX8 waterproof","Weeks of battery per charge","16GB holds thousands of books","205g — lighter than a paperback"],
"pros":["Zero eye strain after hours of reading","Weeks of battery beats any tablet","Waterproof for bath pool and beach reading","Access to millions of books plus free library loans","Warm light better for evening reading than any backlit screen"],
"cons":["Only reads Amazon formats natively","No colour display","Library tied to Amazon ecosystem"],
"tips":["16GB worth it if you download audiobooks","Leather cover doubles as a stand","Library loans via Libby app are free — huge added value","Kindle Unlimited worth it at 2+ books per month","Signature Edition adds wireless charging"],
"faqs":[("Worth it over reading on a phone?","Yes — e-ink causes far less eye strain, battery lasts weeks, it is lighter for extended reading and removes phone distractions."),("Can I read library books?","Yes — most public libraries offer free ebook lending through Libby which sends books directly to your Kindle."),("What is Kindle Unlimited?","4 million+ ebooks and audiobooks for $9.99/month. Worth it if you read frequently."),("Works in bright sunlight?","Better than any tablet. E-ink improves in direct sunlight — ideal for beach reading.")]},
{"kw":"robot vacuum wifi smart home schedule","name":"Wi-Fi Robot Vacuum","emoji":"🤖","cat":"Home","usd":79.99,"was":199.99,"stars":4,"rev":"9,200","sold":"5,000+",
"feats":["Wi-Fi app control from anywhere","Auto-scheduling for daily runs","Works on hard floors and carpets","Anti-drop and anti-collision sensors","2.8-inch slim profile under furniture","100-minute run time per charge"],
"pros":["Maintenance vacuuming becomes completely passive","App scheduling keeps floors clean for guests","Effective on pet hair","Reaches under sofas and beds uprights cannot","Quiet enough for work calls"],
"cons":["Needs floor prep — cables cause problems","Mapping takes 2-3 runs to calibrate","Complements rather than replaces deep cleaning"],
"tips":["Floor-prep 20 minutes before first run","Self-emptying base cuts maintenance to monthly","HEPA filter worth it for allergy sufferers","Magnetic strips block off areas you want avoided","Wi-Fi control is worth the small premium"],
"faqs":[("Do they actually work?","Yes — for maintenance cleaning, genuinely effective. Daily runs keep floors consistently clean with zero effort."),("How often should it run?","Daily or every other day for consistent cleanliness. Weekly fine for low-traffic no-pet homes."),("Handles pet hair?","Yes — rubber brush rolls handle pet hair better than bristle rolls."),("Need to be home?","No — schedule runs while at work and come home to clean floors.")],},
{"kw":"wireless earbuds noise cancelling bluetooth 5","name":"Wireless Earbuds ANC","emoji":"🎧","cat":"Electronics","usd":19.99,"was":59.99,"stars":4,"rev":"24,000","sold":"12,000+",
"feats":["Active noise cancellation","Bluetooth 5.3 stable connection","6 hours per charge plus 18 from case","IPX4 sweat resistant","Touch controls","Transparency mode"],
"pros":["Real ANC under $20 is remarkable value","Comfortable for 2-3 hours continuous wear","Solid bass without muddying mids","15-minute charge gives 2 hours playback","Call quality handles wind well"],
"cons":["ANC not as powerful as Sony or AirPods Pro","Default tips may not suit all ears","Occasional dropout in crowded Wi-Fi areas"],
"tips":["Try all ear tip sizes — fit determines ANC effectiveness","Bluetooth 5.0+ minimum — better range and stability","IPX4 sufficient for workouts","Check companion app quality — some budget earbuds have great EQ","Buy from a retailer with easy returns — fit is personal"],
"faqs":[("Are cheap earbuds any good?","Yes — at $20 you now get genuine ANC, good sound and reliable Bluetooth. The gap between budget and premium has closed significantly."),("How long do they last?","5-6 hours per charge. With case: 20-24 hours total. Battery degrades after 2-3 years."),("Good for calls?","Yes — look for dual microphones and ENC for best quality in noisy environments."),("Are they safe?","At normal volumes yes. Keep below 80% and take hourly breaks during long sessions.")]},
{"kw":"standing desk electric height adjustable dual motor","name":"Electric Standing Desk","emoji":"🖥️","cat":"Furniture","usd":299.99,"was":499.99,"stars":5,"rev":"14,200","sold":"8,000+",
"feats":["Dual motor raises and lowers in 15 seconds","Height range 28-48 inches","4 memory presets","Anti-collision detection","48x24 inch desktop","220lb weight capacity"],
"pros":["Switching heights takes seconds — you actually do it","Memory presets eliminate manual readjusting","Dual motor quieter and more reliable than single","Back pain reduces measurably within 2 weeks","Lasts 10-15 years — a real health investment"],
"cons":["Assembly takes 45-90 minutes","Heavy once assembled and loaded","Significant upfront cost"],
"tips":["Dual motor worth the premium — quieter and more reliable","Check height range covers your sitting and standing heights","Memory presets are almost essential for daily use","Add anti-fatigue mat immediately — essential for standing comfort","Cable management box keeps the desk professional"],
"faqs":[("Does standing actually help?","Yes — alternate 20-30 minutes per hour. Improves circulation, reduces back pain and burns 50-100 extra calories per hour vs sitting."),("What height should it be?","Standing: elbows at 90 degrees — typically waist height. Sitting: forearms parallel to floor. Most people: standing 40-44 inches, sitting 28-30 inches."),("How long do they last?","10-15 years for quality models. Look for 5+ year motor warranties."),("What accessories?","Anti-fatigue mat (essential), monitor arm, keyboard tray and cable management box.")]},
{"kw":"smart plug wifi alexa google home timer","name":"Wi-Fi Smart Plug","emoji":"🔌","cat":"Smart Home","usd":12.99,"was":24.99,"stars":5,"rev":"45,000","sold":"35,000+",
"feats":["Works with Alexa Google Home and Apple HomeKit","24-hour scheduling","Remote control from anywhere","Energy monitoring","No hub required","Compact — doesn't block adjacent outlet"],
"pros":["Makes any device voice and app controlled","Scheduling eliminates forgotten devices","Energy monitoring reveals expensive appliances","Under $13 for whole-home upgrades","Works with existing smart home setups instantly"],
"cons":["Requires 2.4GHz Wi-Fi — not 5GHz only","Setup takes 10-15 minutes","Won't work during internet outages"],
"tips":["Buy multipacks — per-unit price drops significantly","2.4GHz router support is standard — just confirm","Energy monitoring reveals which appliances cost most","Compact designs not blocking adjacent outlets worth slightly more","Check ecosystem compatibility before buying"],
"faqs":[("What can you control?","Any standard plug-in device — lamps, fans, coffee makers, TVs, chargers, heaters. Device must be switched on."),("Work with old appliances?","Yes — that is the point. Any plug-in device becomes voice and app controlled."),("Use electricity when idle?","Yes — 0.5-2W standby. Costs pennies per year. Scheduling savings far outweigh it."),("Reduce electricity bills?","Yes — by scheduling devices off during unused hours and identifying power-hungry appliances.")]},
{"kw":"portable power bank 20000mah usb-c fast charge","name":"Power Bank 20000mAh","emoji":"🔋","cat":"Electronics","usd":29.99,"was":59.99,"stars":5,"rev":"32,000","sold":"18,000+",
"feats":["20,000mAh charges iPhone 15 five times","22.5W fast charging output","USB-C plus dual USB-A — 3 devices at once","LED display shows exact percentage","Full recharge in 4-5 hours via USB-C","Slim enough for jacket pocket"],
"pros":["Handles multi-day trips without hunting outlets","22.5W charges phone at full speed","Three simultaneous ports for groups","Digital display eliminates guessing charge level","Priced well below competitors with same specs"],
"cons":["350g — heavier than 10,000mAh alternatives","Check airline carry-on compliance before flying","No wireless charging output"],
"tips":["20,000mAh is the sweet spot for multi-day travel","USB-C input for fast recharging of the bank itself","Multiple ports let you charge phone earbuds and tablet simultaneously","Most 20,000mAh banks are within the 100Wh airline limit","Fast charging output means phone charges at normal speed"],
"faqs":[("How many charges for my phone?","iPhone 15: approximately 4-5 times. Galaxy S24: approximately 4 times."),("Can I take it on a plane?","Most are within the 100Wh carry-on limit. Must be in carry-on — never checked bags."),("How long to recharge the bank?","Via 22.5W USB-C: 4-5 hours. Via standard 5W: 12-15 hours."),("What size for travel?","10,000mAh for day trips. 20,000mAh for multi-day. 26,800mAh+ for laptop charging.")]},
{"kw":"weighted blanket 15lb glass beads sleep anxiety","name":"Weighted Blanket 15lb","emoji":"🛏️","cat":"Health","usd":49.99,"was":89.99,"stars":5,"rev":"42,000","sold":"25,000+",
"feats":["15lb optimal for 130-170lb adults","Glass bead filling in small even pockets","Breathable cotton cover","Machine washable","60x80 inches full bed width","Dual-sided for year-round use"],
"pros":["Reduces sleep onset time within 1-2 nights","Deep pressure reliably calms anxiety","Dual-sided for year-round use","Machine washable — practical for real life","Backed by peer-reviewed sleep research"],
"cons":["Takes a few nights to adjust to the weight","Heats up more than a regular blanket","Needs large-capacity washing machine"],
"tips":["10% of body weight is the standard rule — 150lb person uses 15lb","Glass bead filling quieter and more even than plastic pellets","Breathable cotton cover important — avoid polyester which traps heat","A removable duvet cover extends blanket life significantly","Machine washable is non-negotiable"],
"faqs":[("What weight should I get?","Approximately 10% of your body weight. A 150lb person uses a 15lb blanket. Go slightly lighter if unsure."),("Do they actually work?","Yes — studies confirm they reduce cortisol, increase serotonin and melatonin and improve sleep quality. Most users notice effects within 1-2 nights."),("Help with anxiety?","Yes — deep pressure stimulation activates the parasympathetic nervous system reducing anxiety heart rate and breathing rate."),("How to wash?","Use a machine with 5kg+ capacity. Cold gentle cycle. Tumble dry low or air dry flat.")]},
{"kw":"massage gun mini deep tissue percussion recovery","name":"Mini Massage Gun","emoji":"💆","cat":"Health","usd":35.99,"was":89.99,"stars":5,"rev":"12,400","sold":"7,500+",
"feats":["5 speed settings 1800-3200 PPM","6 interchangeable attachments","6-hour battery on lower speeds","Quiet brushless motor under 45dB","Fits in any gym bag","USB-C charging in 2.5 hours"],
"pros":["Measurably reduces post-workout soreness","Quiet enough for office or TV use","6 attachments cover every muscle group","Compact — actually gets used away from home","Sub-$40 makes percussion therapy accessible"],
"cons":["Less powerful than full-size Theragun","Battery drops to 2-3 hours at highest speed","Smaller handle less comfortable for long sessions"],
"tips":["Use 1-2 minutes per muscle group — more is not better","Round ball for large muscles bullet for deep knots","Apply 30-60 seconds before workouts to activate muscles","USB-C charging more convenient than proprietary cables","Under 50dB means you can use it in shared spaces"],
"faqs":[("Do they actually help recovery?","Yes — studies show percussion massage increases blood flow reduces lactic acid and decreases delayed onset muscle soreness."),("How long per area?","1-2 minutes per muscle group. Before workout: 30-60 seconds. After workout: 1-2 minutes per sore area."),("Can you use it on your neck?","Lowest speed only on the sides — trapezius muscles. Never directly on the spine or vertebrae."),("Which attachment where?","Round ball: large muscles. Flat head: general use. Fork: alongside spine. Bullet: deep targeted knots.")]},
]

def lp(usd,cur):
    r=RATES.get(cur,1.0);p=usd*r
    return f"{cur}{p:.0f}" if cur in ["zł","kr"] else f"{cur}{p:.2f}"

def au(cc,kw):
    return f"https://www.{DOMAINS.get(cc,'amazon.com')}/s?k={kw.replace(' ','+')}&tag={TAG}"

CSS='''<style>
:root{--o:#FF9900;--d:#0f1111;--s:#1a1f2e;--c:#1e2432;--b:#2d3548;--t:#f0f2f5;--m:#8491a5;--g:#00c853;}
*{box-sizing:border-box;margin:0;padding:0;}body{font-family:"DM Sans",sans-serif;background:var(--d);color:var(--t);line-height:1.7;}
nav{position:sticky;top:0;z-index:100;background:#232F3E;border-bottom:1px solid #1a2030;display:flex;align-items:center;justify-content:space-between;padding:0 24px;height:58px;}
.logo{font-family:"Syne",sans-serif;font-size:20px;font-weight:800;color:var(--t);text-decoration:none;}.logo span{color:var(--o);}
.nc{background:var(--o);color:#111;padding:7px 16px;border-radius:6px;font-weight:700;font-size:13px;text-decoration:none;}
.hero{background:radial-gradient(ellipse at 50% 0%,#2a1800 0%,var(--d) 70%);padding:48px 24px 28px;text-align:center;border-bottom:1px solid var(--b);}
.bdg{display:inline-block;background:var(--o);color:#111;font-size:11px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;padding:4px 14px;border-radius:20px;margin-bottom:10px;}
.upd{display:inline-block;background:var(--s);border:1px solid var(--b);border-radius:4px;padding:3px 10px;font-size:11px;color:var(--m);margin-bottom:12px;}
.bb{display:inline-flex;align-items:center;gap:10px;background:var(--o);color:#111;font-weight:800;font-size:16px;padding:14px 28px;border-radius:8px;text-decoration:none;margin-top:8px;}
.pt{background:#111;color:var(--o);font-size:14px;padding:4px 12px;border-radius:4px;}
.mt{color:var(--m);font-size:12px;margin-top:8px;}
.content{max-width:820px;margin:0 auto;padding:32px 24px;}
h1{font-family:"Syne",sans-serif;font-size:clamp(22px,4vw,36px);font-weight:800;line-height:1.15;margin-bottom:16px;}
h1 em{color:var(--o);font-style:normal;}
h2{font-family:"Syne",sans-serif;font-size:20px;font-weight:800;margin:28px 0 12px;padding-bottom:8px;border-bottom:1px solid var(--b);}
p{color:#ccc;margin-bottom:14px;font-size:15px;}ul{margin:0 0 14px 20px;color:#ccc;font-size:15px;}li{margin-bottom:8px;}
.fl{list-style:none;margin-left:0;}.fl li{padding:8px 0;border-bottom:1px solid var(--b);font-size:14px;color:#ccc;}.fl li:last-child{border-bottom:none;}
.pc{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin:14px 0;}
.pros{background:#0a1a0a;border:1px solid #1a3a1a;border-radius:10px;padding:16px;}
.cons{background:#1a0a0a;border:1px solid #3a1a1a;border-radius:10px;padding:16px;}
.pros h3{color:var(--g);margin-bottom:8px;font-size:15px;}.cons h3{color:#ff6666;margin-bottom:8px;font-size:15px;}
.pros ul,.cons ul{margin-left:16px;}.pros li,.cons li{font-size:13px;margin-bottom:6px;}
.bx{background:linear-gradient(135deg,#2a1800,#1a1200);border:2px solid var(--o);border-radius:14px;padding:22px;margin:24px 0;text-align:center;}
.bx h3{font-family:"Syne",sans-serif;font-size:18px;font-weight:800;color:var(--o);margin-bottom:8px;}
.pr{font-family:"Syne",sans-serif;font-size:28px;font-weight:800;color:var(--o);}.ws{font-size:14px;color:var(--m);text-decoration:line-through;margin-left:8px;}
.bbt{display:inline-block;background:var(--o);color:#111;font-weight:800;font-size:15px;padding:12px 28px;border-radius:8px;text-decoration:none;margin-top:12px;}
.vd{background:var(--s);border-left:4px solid var(--o);border-radius:0 10px 10px 0;padding:16px 20px;margin:22px 0;}
.vd h3{color:var(--o);font-size:15px;font-weight:700;margin-bottom:6px;}.vd p{color:#ccc;margin:0;font-size:14px;}
.fb{background:var(--c);border:1px solid var(--b);border-radius:12px;padding:20px;margin:24px 0;}
.fi{border-bottom:1px solid var(--b);padding:12px 0;}.fi:last-child{border-bottom:none;}
.fq{font-weight:700;font-size:15px;margin-bottom:8px;color:var(--t);}.fa{color:var(--m);font-size:14px;line-height:1.6;}
.ec{background:linear-gradient(135deg,#1a0f00,#0a0f1a);border:1px solid var(--o);border-radius:12px;padding:20px;text-align:center;margin:24px 0;}
.ec h3{font-family:"Syne",sans-serif;font-size:17px;font-weight:800;margin-bottom:6px;}.ec p{color:var(--m);font-size:13px;margin-bottom:12px;}
.ecf{display:flex;gap:8px;max-width:360px;margin:0 auto;flex-wrap:wrap;justify-content:center;}
.ecf input{flex:1;min-width:180px;background:#1a1a1a;border:1px solid var(--b);color:var(--t);padding:10px 14px;border-radius:6px;font-size:14px;outline:none;}
.ecf button{background:var(--o);color:#111;border:none;padding:10px 16px;border-radius:6px;font-weight:700;font-size:14px;cursor:pointer;}
#cm{font-size:12px;color:var(--g);margin-top:8px;}
.nb{background:#232F3E;border-top:1px solid #1a2030;padding:12px 24px;display:flex;align-items:center;gap:12px;flex-wrap:wrap;justify-content:center;margin-top:32px;}
.nb span{font-size:11px;color:var(--m);letter-spacing:1px;text-transform:uppercase;font-weight:700;}
.nb a{background:var(--c);border:1px solid var(--b);border-radius:20px;padding:5px 14px;font-size:12px;font-weight:600;color:var(--t);text-decoration:none;}
footer{background:#232F3E;border-top:1px solid #1a2030;padding:16px 24px;text-align:center;font-size:12px;color:var(--m);line-height:1.8;}
@media(max-width:600px){.hero{padding:36px 16px 24px;}.content{padding:20px 16px;}.pc{grid-template-columns:1fr;}}
</style>'''

JS='''<script>
function ce2(){var e=document.getElementById("ce").value.trim();var m=document.getElementById("cm");
if(!e||!e.includes("@")){m.textContent="Enter a valid email";m.style.color="#ff4444";return;}
var s=JSON.parse(localStorage.getItem("so_subs")||"[]");
if(s.find(x=>x.email===e)){m.textContent="Already subscribed!";return;}
s.push({email:e,date:new Date().toISOString()});localStorage.setItem("so_subs",JSON.stringify(s));
m.textContent="✅ Done!";m.style.color="#00c853";document.getElementById("ce").value="";}
</script>'''

def build(prod,lang):
    lc=lang["code"];cc=lang["cc"];flag=lang["flag"];cur=lang["cur"]
    buy=lang["buy"];prime=lang["prime"]
    url=au(cc,prod["kw"]);price=lp(prod["usd"],cur);was=lp(prod["was"],cur)
    dom=DOMAINS[cc]
    feats="".join([f"<li>✓ {f}</li>" for f in prod["feats"]])
    pros="".join([f"<li>{p}</li>" for p in prod["pros"]])
    cons="".join([f"<li>{c}</li>" for c in prod["cons"]])
    tips="".join([f"<li>{t}</li>" for t in prod["tips"]])
    faqs="".join([f'<div class="fi"><div class="fq">{q}</div><div class="fa">{a}</div></div>' for q,a in prod["faqs"]])
    fsch=json.dumps({"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in prod["faqs"]]})
    slug_base=re.sub(r'[^a-z0-9]+',' ',prod["kw"].lower()).strip().replace(' ','-')
    slug=f"reviews/{lc}/{slug_base}.html"
    os.makedirs(f"reviews/{lc}",exist_ok=True)
    html=f'''<!DOCTYPE html>
<html lang="{lc}"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{prod["name"]} Review 2026 {flag} | ShoppingOnline</title>
<meta name="description" content="In-depth review of {prod["name"]} for {cc} shoppers. Best price on {dom}. Updated {TODAY_NICE}.">
<meta name="robots" content="index,follow">
<link rel="canonical" href="{BASE}{slug}">
<script type="application/ld+json">{fsch}</script>
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@400;500;600&display=swap" rel="stylesheet">
{CSS}
</head><body>
<nav><a class="logo" href="{BASE}">Shopping<span>Online</span> {flag}</a><a class="nc" href="{url}" target="_blank" rel="noopener">{buy} →</a></nav>
<div class="hero">
<div class="bdg">📋 Review · {cc} · 2026</div><br>
<div class="upd">🕐 {TODAY_NICE}</div>
<div style="font-size:52px;margin:10px 0">{prod["emoji"]}</div>
<a class="bb" href="{url}" target="_blank" rel="noopener">🛒 {buy} <span class="pt">{price}</span></a>
<div class="mt">✅ {prime} · 30-day returns · {prod["stars"]*"★"} ({prod["rev"]} reviews) · {prod["sold"]} sold last month</div>
</div>
<div class="content">
<h1>{prod["emoji"]} {prod["name"]} — <em>In-Depth Review</em> 2026</h1>
<p>{prod["name"]} is one of the best-selling products on {dom} right now — {prod["sold"]} units sold last month with {prod["rev"]} reviews averaging {prod["stars"]*"★"}. Here is everything you need to know before buying.</p>
<h2>Key Features</h2><ul class="fl">{feats}</ul>
<h2>Pros &amp; Cons</h2>
<div class="pc">
<div class="pros"><h3>✅ Pros</h3><ul>{pros}</ul></div>
<div class="cons"><h3>❌ Cons</h3><ul>{cons}</ul></div>
</div>
<div class="bx">
<h3>🛒 Best Price on Amazon {flag}</h3>
<p style="color:var(--m);font-size:13px;margin-bottom:12px">{prime} · 30-day returns · Secure checkout</p>
<div><span class="pr">{price}</span><span class="ws">{was}</span></div>
<a class="bbt" href="{url}" target="_blank" rel="noopener">{buy} {flag} →</a>
</div>
<h2>Buying Guide</h2><ul>{tips}</ul>
<div class="vd"><h3>⭐ Our Verdict</h3>
<p>The {prod["name"]} delivers exceptional value at {price}. With {prod["rev"]} reviews averaging {prod["stars"]*"★"} and {prod["sold"]} sold last month, it is one of the strongest buys in its category on {dom} right now.</p>
</div>
<div class="fb"><h2>❓ FAQ</h2>{faqs}</div>
<div class="ec">
<h3>📬 Get Daily Amazon Deal Alerts</h3>
<p>No spam. Unsubscribe any time.</p>
<div class="ecf"><input type="email" id="ce" placeholder="email@example.com"/><button onclick="ce2()">Subscribe →</button></div>
<div id="cm"></div>
</div>
<p style="font-size:14px;color:var(--m)">👉 <a href="{BASE}" style="color:var(--o)">Back to ShoppingOnline</a> · <a href="{au(cc,'deals')}" target="_blank" rel="noopener" style="color:var(--o)">See all deals {flag}</a></p>
</div>
<div class="nb"><span>🔗 Network</span>
<a href="{BASE}">🛒 ShoppingOnline</a>
<a href="https://globesitenetwork.github.io/DealsGlobe/">🌍 DealsGlobe</a>
<a href="https://brightlane.github.io/ShopAliexpressOnline/">🛍️ AliDeals</a>
</div>
<footer><p>As an Amazon Associate we earn from qualifying purchases at no extra cost to you.</p>
<p>© 2026 ShoppingOnline · {flag} {dom} · Tag: {TAG}</p></footer>
{JS}
</body></html>'''
    return slug, html

def update_sitemap(slugs):
    path="sitemap.xml"
    if os.path.exists(path):
        with open(path) as f: sm=f.read()
    else:
        sm='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n</urlset>'
    sm=re.sub(r'<lastmod>\d{4}-\d{2}-\d{2}</lastmod>',f'<lastmod>{TODAY}</lastmod>',sm)
    added=0
    for s in slugs:
        url=f"{BASE}{s}"
        if url not in sm:
            sm=sm.replace('</urlset>',f'  <url><loc>{url}</loc><lastmod>{TODAY}</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>\n</urlset>')
            added+=1
    with open(path,'w') as f: f.write(sm)
    print(f"  Sitemap: +{added} URLs")

def main():
    print(f"\n🛒 ShoppingOnline Daily Generator — {TODAY}")
    rng=random.Random(SEED)
    todays=rng.sample(PRODUCTS,5)
    print(f"Products: {[p['name'] for p in todays]}\n")
    slugs=[]
    total=0
    for prod in todays:
        print(f"  {prod['emoji']} {prod['name']}")
        for lang in LANGS:
            try:
                slug,html=build(prod,lang)
                with open(slug,'w',encoding='utf-8') as f: f.write(html)
                slugs.append(slug);total+=1
                print(f"    {lang['flag']} ✅")
            except Exception as e:
                print(f"    {lang['flag']} ❌ {e}")
    update_sitemap(slugs)
    print(f"\n✅ {total} pages generated\n")

if __name__=="__main__":
    main()
