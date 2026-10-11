"""
Renders the 6 CONCEPT portfolio mockups (fictional businesses) into images/portfolio/.
Each scene is plain HTML/CSS rendered by headless Chromium, so all text is exact.
Requires: pip install playwright pillow  (and a Chromium/Chrome; set CHROME_PATH to use an installed one)
Run from repo root:  python scripts/generate-concepts.py
Fonts for the mockups are downloaded from Fontsource (OFL) into a temp folder; they are NOT shipped with the site.
"""
import asyncio, io, os, pathlib, tempfile, urllib.request
from playwright.async_api import async_playwright
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "images/portfolio"
FD = pathlib.Path(os.environ.get("CONCEPT_FONTS", pathlib.Path(tempfile.gettempdir()) / "jcp-concept-fonts"))
FONTS = {"PF7": "playfair-display:700", "PF4": "playfair-display:400", "Bebas": "bebas-neue:400", "Osw5": "oswald:500",
         "Osw7": "oswald:700", "Pac": "pacifico:400", "DMS": "dm-serif-display:400", "Arch": "archivo-black:400"}

def font_css():
    FD.mkdir(parents=True, exist_ok=True)
    css = ""
    for fam, spec in FONTS.items():
        n, w = spec.split(":")
        p = FD / f"{n}-{w}.woff2"
        if not p.exists():
            urllib.request.urlretrieve(f"https://cdn.jsdelivr.net/fontsource/fonts/{n}@latest/latin-{w}-normal.woff2", p)
        css += f"@font-face{{font-family:{fam};src:url({p.as_uri()})}}\n"
    for fam, f in [("Inter", "inter-latin-wght-normal.woff2"), ("SG", "space-grotesk-latin-wght-normal.woff2")]:
        css += f"@font-face{{font-family:{fam};src:url({(ROOT/'fonts'/f).as_uri()});font-weight:100 900}}\n"
    return css

NOISE = "url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='300' height='300'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='3' stitchTiles='stitch'/%3E%3CfeColorMatrix values='0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 .09 0'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E\")"

BASE = """
*{margin:0;padding:0;box-sizing:border-box}
body{width:1600px;height:1200px;overflow:hidden;font-family:Inter,sans-serif}
.scene{position:relative;width:1600px;height:1200px;overflow:hidden}
.scene::after{content:"";position:absolute;inset:0;background-image:NOISE;pointer-events:none;mix-blend-mode:multiply;opacity:.9}
.abs{position:absolute}
.sh{box-shadow:0 2px 4px rgba(0,0,0,.12),0 18px 40px rgba(0,0,0,.22),0 50px 90px -20px rgba(0,0,0,.3)}
""".replace("NOISE", NOISE)

# ---------------------------------------------------------------- 1 COFFEE
COFFEE_MARK = """<svg viewBox="0 0 120 120" width="{s}" height="{s}"><circle cx="60" cy="60" r="56" fill="none" stroke="{c}" stroke-width="3"/>
<path d="M30 52h52v14a26 26 0 0 1-52 0z" fill="{c}"/><path d="M82 56h6a9 9 0 0 1 0 18h-8" fill="none" stroke="{c}" stroke-width="5"/>
<path d="M44 22c-5 7 5 12 0 20M56 18c-5 8 5 14 0 24M68 22c-5 7 5 12 0 20" fill="none" stroke="{a}" stroke-width="4" stroke-linecap="round"/></svg>"""
def coffee():
    m = lambda s, c="#123140", a="#c8794a": COFFEE_MARK.format(s=s, c=c, a=a)
    return f"""<div class="scene" style="background:radial-gradient(circle at 30% 20%,#efe6d6,#ddd0ba 70%)">
<div class="abs sh" style="left:90px;top:110px;width:760px;height:980px;background:#123140;border-radius:6px;display:flex;flex-direction:column;align-items:center;justify-content:center;color:#f3ead8">
  {m(250,"#f3ead8","#c8794a")}
  <div style="font:700 92px/1 PF7;margin-top:46px;letter-spacing:-1px">Brew &amp; Falls</div>
  <div style="font:600 24px/1 Inter;letter-spacing:.42em;margin-top:22px;color:#c8794a">COFFEE</div>
  <div style="width:80px;height:2px;background:#c8794a;margin:44px 0 26px"></div>
  <div style="font:500 20px/1 Inter;letter-spacing:.3em;opacity:.8">NIAGARA FALLS, NY</div>
</div>
<div class="abs sh" style="left:920px;top:110px;width:580px;height:330px;background:#f3ead8;border-radius:6px;padding:44px;display:flex;gap:30px;align-items:center;transform:rotate(-3deg)">
  {m(130)}<div><div style="font:700 46px/1 PF7;color:#123140">Brew &amp; Falls</div><div style="font:600 15px/1 Inter;letter-spacing:.35em;color:#c8794a;margin-top:12px">COFFEE</div>
  <div style="font:400 17px/1.6 Inter;color:#123140;margin-top:26px">Maya Lindqvist &middot; Owner<br>hello@brewandfalls.co</div></div>
</div>
<div class="abs sh" style="left:980px;top:490px;width:240px;height:300px;background:linear-gradient(90deg,#e9e1d1,#fbf6ec 40%,#e3d9c7);border-radius:8px 8px 40px 40px;display:flex;align-items:center;justify-content:center">
  <div style="position:absolute;top:-22px;left:-12px;right:-12px;height:30px;background:#123140;border-radius:8px"></div>
  <div style="width:100%;height:150px;background:#123140;display:flex;align-items:center;justify-content:center">{m(110,"#f3ead8","#c8794a")}</div>
</div>
<div class="abs" style="left:1260px;top:500px;display:grid;gap:14px">
  {''.join(f'<div class="sh" style="width:240px;height:72px;border-radius:6px;background:{c};display:flex;align-items:flex-end;padding:10px 14px;font:600 14px Inter;color:{t}">{h}</div>' for c,t,h in [("#123140","#f3ead8","Falls Navy #123140"),("#c8794a","#fff","Copper #C8794A"),("#f3ead8","#123140","Foam #F3EAD8"),("#2b2b2b","#f3ead8","Roast #2B2B2B")])}
</div>
<div class="abs sh" style="left:920px;top:880px;width:580px;height:220px;background:#fbf7ef;border-radius:6px;padding:36px 44px;color:#123140">
  <div style="font:600 13px Inter;letter-spacing:.3em;color:#c8794a">TYPOGRAPHY</div>
  <div style="display:flex;justify-content:space-between;align-items:flex-end;margin-top:14px"><div style="font:700 84px/1 PF7">Aa</div><div style="font:600 72px/1 Inter">Aa</div></div>
  <div style="display:flex;justify-content:space-between;font:500 16px Inter;margin-top:14px;opacity:.75"><span>Playfair Display</span><span>Inter</span></div>
</div></div>"""

# ---------------------------------------------------------------- 2 PIZZA MENU
def pizza():
    items = [("Margherita", "San Marzano, fresh mozzarella, basil", "14"), ("Classic Pepperoni", "Cup-and-char pepperoni, oregano", "16"),
             ("Buffalo Chicken", "Hot sauce, blue cheese, celery", "17"), ("White Garlic", "Ricotta, roasted garlic, lemon", "15"),
             ("The Ironwood", "Sausage, peppers, onion, provolone", "18")]
    rows = "".join(f'<div style="display:flex;justify-content:space-between;align-items:center;margin-top:26px"><div><div style="font:700 30px/1 Osw7;letter-spacing:.02em;text-transform:uppercase">{n}</div><div style="font:400 17px/1.4 Inter;color:#6b5a4a;margin-top:6px">{d}</div></div><div style="font:700 30px Osw7;color:#b3261e">{p}</div></div>' for n, d, p in items)
    wings = "".join(f'<div style="display:flex;justify-content:space-between;align-items:center;font:500 20px Inter;margin-top:14px"><span>{a}</span><span style="font:700 22px Osw7;color:#b3261e">{b}</span></div>' for a, b in [("10 wings, any sauce", "14"), ("20 wings, any sauce", "26"), ("Garlic knots", "6"), ("House salad", "8")])
    wood = "repeating-linear-gradient(92deg,#3a2416 0 14px,#432a1a 14px 22px,#36210f 22px 40px,#4a2f1d 40px 46px),linear-gradient(#3a2416,#2a190e)"
    return f"""<div class="scene" style="background:{wood};background-blend-mode:overlay">
<div class="abs" style="inset:0;background:radial-gradient(circle at 40% 40%,transparent 30%,rgba(0,0,0,.55))"></div>
<div class="abs sh" style="left:170px;top:70px;width:720px;height:1060px;background:#f7f0e3;border-radius:4px;transform:rotate(-2deg);padding:64px 70px;color:#1f1712">
  <div style="text-align:center;border-bottom:3px solid #1f1712;padding-bottom:28px">
    <div style="font:400 26px Inter;letter-spacing:.5em;color:#b3261e">EST. BUFFALO</div>
    <div style="font:700 96px/1 Osw7;letter-spacing:.01em;margin-top:12px">IRONWOOD</div>
    <div style="font:500 32px/1 Osw5;letter-spacing:.42em;margin-top:6px">SLICE CO.</div>
  </div>
  <div style="font:700 22px Inter;letter-spacing:.35em;color:#b3261e;margin-top:38px">WOOD-FIRED PIES</div>
  {rows}
  <div style="position:absolute;left:70px;right:70px;bottom:60px;border-top:2px solid #1f1712;padding-top:26px;display:flex;justify-content:space-between;align-items:center"><span style="font:700 34px Osw7">SLICES ALL DAY</span><span style="font:700 34px Osw7;color:#b3261e">$4</span></div>
</div>
<div class="abs sh" style="left:930px;top:180px;width:540px;height:760px;background:#1f1712;border-radius:4px;transform:rotate(2.5deg);padding:56px 56px;color:#f7f0e3">
  <div style="font:700 22px Inter;letter-spacing:.35em;color:#e5a33a">WINGS &amp; SIDES</div>
  {wings}
  <div style="margin-top:56px;border:2px solid #e5a33a;border-radius:4px;padding:28px;text-align:center">
    <div style="font:700 44px/1 Osw7;letter-spacing:.02em">FRIDAY SLICE NIGHT</div>
    <div style="font:500 20px Inter;margin-top:14px;color:#e5a33a">Any slice + drink $6</div>
  </div>
  <div style="position:absolute;bottom:56px;left:56px;right:56px;display:flex;justify-content:space-between;font:500 16px Inter;opacity:.75"><span>ironwoodslice.co</span><span>Dine in &middot; Takeout</span></div>
</div>
</div>"""

# ---------------------------------------------------------------- 3 BARBER LOGO REFRESH
def barber():
    badge = """<svg viewBox="0 0 300 300" width="300" height="300"><circle cx="150" cy="150" r="146" fill="#14171a"/><circle cx="150" cy="150" r="128" fill="none" stroke="#c9a45c" stroke-width="3"/>
<defs><path id="t" d="M150 150 m-104 0 a104 104 0 1 1 208 0"/><path id="b" d="M150 150 m-110 0 a110 110 0 0 0 220 0"/></defs>
<text font-family="Osw5" font-size="24" letter-spacing="6" fill="#f2ede4"><textPath href="#t" startOffset="50%" text-anchor="middle">GORGE &amp; GRAIN</textPath></text>
<text font-family="Osw5" font-size="18" letter-spacing="7" fill="#c9a45c"><textPath href="#b" startOffset="50%" text-anchor="middle">BARBER CO.</textPath></text>
<text x="150" y="172" text-anchor="middle" font-family="DMS" font-size="78" fill="#f2ede4">G&amp;G</text>
<circle cx="42" cy="150" r="5" fill="#c9a45c"/><circle cx="258" cy="150" r="5" fill="#c9a45c"/></svg>"""
    return f"""<div class="scene" style="background:linear-gradient(160deg,#cfccc6,#a9a59e)">
<div class="abs" style="left:80px;top:80px;font:600 18px Inter;letter-spacing:.35em;color:#3b3b3b">LOGO REFRESH</div>
<div class="abs sh" style="left:80px;top:140px;width:620px;height:560px;background:#fff;border-radius:6px;display:flex;flex-direction:column;align-items:center;justify-content:center">
  <div style="position:absolute;top:24px;left:28px;font:600 14px Inter;letter-spacing:.3em;color:#999">BEFORE</div>
  <div style="font:italic 700 52px/1.1 Georgia,serif;color:#7a1f1f;text-align:center">Gorge and Grain<br><span style="font-size:36px">Barber Shop</span></div>
  <div style="margin-top:22px;font:400 22px Arial,sans-serif;color:#444">&#9986; Cuts &bull; Shaves &bull; Beards &#9986;</div>
</div>
<div class="abs sh" style="left:760px;top:140px;width:760px;height:560px;background:#f2ede4;border-radius:6px;display:flex;align-items:center;justify-content:center;gap:56px">
  <div style="position:absolute;top:24px;left:28px;font:600 14px Inter;letter-spacing:.3em;color:#9b7f45">AFTER</div>
  {badge}
  <div><div style="font:400 64px/0.95 DMS;color:#14171a">Gorge<br>&amp; Grain</div><div style="font:500 20px Osw5;letter-spacing:.5em;color:#9b7f45;margin-top:18px">BARBER CO.</div></div>
</div>
<div class="abs sh" style="left:80px;top:760px;width:820px;height:360px;background:#14171a;border-radius:6px;display:flex;align-items:center;justify-content:center;gap:40px;overflow:hidden">
  <div style="position:absolute;inset:0;background:repeating-linear-gradient(90deg,rgba(255,255,255,.03) 0 2px,transparent 2px 60px)"></div>
  <div style="transform:scale(.8)">{badge.replace('#14171a','#1d2125')}</div>
  <div style="color:#f2ede4"><div style="font:400 30px Osw5;letter-spacing:.3em">WALK-INS</div><div style="font:400 30px Osw5;letter-spacing:.3em;color:#c9a45c">WELCOME</div><div style="font:400 18px Inter;margin-top:16px;opacity:.7">Niagara Falls, NY</div></div>
</div>
<div class="abs sh" style="left:960px;top:760px;width:250px;height:360px;background:#f2ede4;border-radius:6px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:20px">
  <div style="width:150px;height:150px;border-radius:36px;background:#14171a;display:grid;place-items:center;font:400 52px DMS;color:#c9a45c">G&amp;G</div>
  <div style="font:500 14px Inter;color:#555;letter-spacing:.2em">APP ICON</div>
</div>
<div class="abs sh" style="left:1270px;top:760px;width:250px;height:360px;border-radius:6px;overflow:hidden;display:grid;grid-template-rows:repeat(4,1fr)">
  <div style="background:#14171a"></div><div style="background:#c9a45c"></div><div style="background:#f2ede4"></div><div style="background:#7a1f1f"></div>
</div></div>"""

# ---------------------------------------------------------------- 4 BAKERY SOCIAL
def bakery():
    def tile(bg, html): return f'<div style="background:{bg};display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;overflow:hidden;position:relative">{html}</div>'
    donut = '<div style="width:62%;aspect-ratio:1;border-radius:50%;background:radial-gradient(circle,{c0} 0 18%,#c98a4e 19% 24%,{c1} 25% 66%,#d9a066 67%)"></div>'
    tiles = [
        tile("#f7c6cf", '<div style="font:400 40px/1 Pac;color:#6b2d3a">Fresh<br>daily</div>'),
        tile("#fff4ec", donut.format(c0="#fff4ec", c1="#f28bb0")),
        tile("#6b2d3a", '<div style="font:700 26px/1.1 PF7;color:#fff4ec">Maple<br>donuts<br>are back!</div>'),
        tile("#fde3c8", donut.format(c0="#fde3c8", c1="#7a4a2a")),
        tile("#fff4ec", '<div style="font:700 22px/1.2 Inter;color:#6b2d3a;letter-spacing:.08em">ORDER<br>AHEAD<br>FOR PICKUP</div>'),
        tile("#f28bb0", '<div style="font:400 34px/1 Pac;color:#fff">Sweet<br>Saturday</div>'),
        tile("#6b2d3a", donut.format(c0="#6b2d3a", c1="#f7c6cf")),
        tile("#f7c6cf", '<div style="font:700 22px/1.25 Inter;color:#6b2d3a">6 cupcakes<br><span style="font:700 40px PF7">$18</span></div>'),
        tile("#fff4ec", '<div style="font:400 30px/1 Pac;color:#f28bb0">Thank you,<br>Niagara!</div>'),
        tile("#fde3c8", '<div style="font:700 22px/1.2 Inter;color:#6b2d3a;letter-spacing:.08em">OPEN<br>7 AM</div>'),
        tile("#f28bb0", donut.format(c0="#f28bb0", c1="#fff4ec")),
        tile("#6b2d3a", '<div style="font:400 30px/1 Pac;color:#f7c6cf">Sugar<br>Mist</div>'),
    ]
    phone = f"""<div class="abs sh" style="left:560px;top:90px;width:480px;height:1000px;border-radius:64px;background:#111;padding:18px">
<div style="width:100%;height:100%;border-radius:48px;background:#fff;overflow:hidden">
  <div style="height:56px"></div>
  <div style="display:flex;align-items:center;gap:20px;padding:10px 26px">
    <div style="width:96px;height:96px;border-radius:50%;background:#f7c6cf;display:grid;place-items:center;font:400 34px Pac;color:#6b2d3a;border:3px solid #f28bb0">S</div>
    <div><div style="font:700 22px Inter;color:#222">sugarmistbakery</div><div style="font:400 16px/1.4 Inter;color:#666;margin-top:4px">Small-batch bakery<br>Niagara Falls, NY</div></div>
  </div>
  <div style="display:flex;gap:10px;padding:16px 26px 20px"><div style="flex:1;height:40px;border-radius:10px;background:#f28bb0;color:#fff;font:600 16px/40px Inter;text-align:center">Follow</div><div style="flex:1;height:40px;border-radius:10px;background:#eee;font:600 16px/40px Inter;text-align:center;color:#222">Message</div></div>
  <div style="display:grid;grid-template-columns:repeat(3,1fr);grid-auto-rows:146px;gap:3px">{''.join(tiles)}</div>
  <div style="position:absolute;left:18px;right:18px;bottom:18px;height:70px;border-radius:0 0 48px 48px;background:#fff;border-top:1px solid #eee;display:flex;justify-content:space-around;align-items:center">{''.join('<span style="width:26px;height:26px;border-radius:7px;border:2.5px solid #333;display:inline-block"></span>' for _ in range(4))}</div>
</div></div>"""
    post = lambda l, t, r, bg, inner: f'<div class="abs sh" style="left:{l}px;top:{t}px;width:380px;height:380px;border-radius:18px;background:{bg};transform:rotate({r}deg);display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;overflow:hidden">{inner}</div>'
    return f"""<div class="scene" style="background:radial-gradient(circle at 70% 30%,#fbe3e7,#f3c9d1 75%)">
{post(110,170,-7,"#6b2d3a",'<div style="font:400 30px Pac;color:#f7c6cf">Sugar Mist</div><div style="font:700 64px/1 PF7;color:#fff4ec;margin-top:20px">Maple<br>donuts</div><div style="font:600 18px Inter;letter-spacing:.3em;color:#f7c6cf;margin-top:24px">ARE BACK</div>')}
{post(150,640,5,"#fff4ec",'<div style="width:190px;height:190px;border-radius:50%;background:radial-gradient(circle,#fff4ec 0 18%,#c98a4e 19% 24%,#f28bb0 25% 66%,#d9a066 67%)"></div><div style="font:700 26px Inter;color:#6b2d3a;margin-top:26px;letter-spacing:.06em">FRESH DAILY &middot; 7 AM</div>')}
{phone}
{post(1110,150,6,"#f28bb0",'<div style="font:400 58px/1 Pac;color:#fff">Sweet<br>Saturday</div><div style="font:700 22px Inter;color:#6b2d3a;margin-top:30px;background:#fff4ec;padding:12px 22px;border-radius:999px">6 CUPCAKES $18</div>')}
{post(1090,640,-5,"#fde3c8",'<div style="font:700 30px/1.15 Inter;color:#6b2d3a;letter-spacing:.06em">ORDER AHEAD<br>FOR PICKUP</div><div style="font:400 36px Pac;color:#f28bb0;margin-top:22px">Sugar Mist Bakery</div>')}
</div>"""

# ---------------------------------------------------------------- 5 BREWERY FLYER
def brewery():
    brick = "repeating-linear-gradient(0deg,#5b2c22 0 52px,#3a1b15 52px 58px)"
    poster = lambda w, h, s: f"""<div style="width:{w}px;height:{h}px;background:#0e2a5c;position:relative;overflow:hidden;color:#f4ecd8;padding:{56*s}px {54*s}px">
<div style="position:absolute;right:-{170*s}px;top:{150*s}px;width:{460*s}px;height:{460*s}px;border-radius:50%;background:#f0a830"></div>
<div style="position:absolute;left:0;right:0;bottom:{230*s}px;height:{120*s}px;background:repeating-linear-gradient(180deg,#1e4fa8 0 {10*s}px,transparent {10*s}px {22*s}px)"></div>
<div style="position:relative;font:600 {20*s}px Inter;letter-spacing:.35em;color:#f0a830">COBALT CANAL BREWING</div>
<div style="position:relative;font:400 {170*s}px/.86 Bebas;margin-top:{40*s}px">FALL<br>TAP<br>TAKE&shy;OVER</div>
<div style="position:absolute;left:{54*s}px;right:{54*s}px;bottom:{56*s}px">
  <div style="font:400 {54*s}px/1 Bebas;color:#f0a830">SAT OCT 24 &middot; 2&ndash;10 PM</div>
  <div style="font:500 {22*s}px/1.5 Inter;margin-top:{10*s}px">12 taps &middot; Live music &middot; Food trucks</div>
  <div style="font:500 {18*s}px Inter;margin-top:{14*s}px;opacity:.75">Lockport, NY &middot; 21+ &middot; Free entry</div>
</div></div>"""
    tape = lambda l, t, r: f'<div class="abs" style="left:{l}px;top:{t}px;width:130px;height:40px;background:rgba(240,232,210,.82);transform:rotate({r}deg);z-index:3"></div>'
    return f"""<div class="scene" style="background:{brick}">
<div class="abs" style="inset:0;background:repeating-linear-gradient(90deg,transparent 0 120px,#3a1b15 120px 126px);background-size:252px 116px;opacity:.9;-webkit-mask:repeating-linear-gradient(0deg,#000 0 58px,transparent 58px 116px)"></div>
<div class="abs" style="inset:0;background:repeating-linear-gradient(90deg,transparent 0 60px,#3a1b15 60px 66px,transparent 66px 126px);background-size:252px 116px;-webkit-mask:repeating-linear-gradient(0deg,transparent 0 58px,#000 58px 116px)"></div>
<div class="abs" style="inset:0;background:radial-gradient(circle at 45% 40%,rgba(255,200,140,.18),rgba(0,0,0,.6) 80%)"></div>
<div class="abs sh" style="left:250px;top:80px;transform:rotate(-2.5deg)">{poster(640,1000,1)}</div>
{tape(260,70,-12)}{tape(780,60,10)}
<div class="abs sh" style="left:1000px;top:340px;transform:rotate(4deg)">{poster(420,650,0.65)}</div>
{tape(1150,330,3)}
</div>"""

# ---------------------------------------------------------------- 6 LANDSCAPE WEBSITE
def landscape():
    hero_img = """<div style="position:absolute;inset:0;background:linear-gradient(180deg,#bfe0f0 0%,#e8f3e6 55%,#7fae63 56%,#4f8a3f 100%)"></div>
<div style="position:absolute;left:-10%;right:-10%;bottom:-30%;height:75%;border-radius:50% 50% 0 0;background:#5e9a48"></div>
<div style="position:absolute;left:55%;right:-20%;bottom:-20%;height:60%;border-radius:50% 50% 0 0;background:#3f7a35"></div>
<div style="position:absolute;left:12%;bottom:30%;width:9%;aspect-ratio:1;border-radius:50%;background:#2f6a2c;box-shadow:40px 10px 0 -6px #376f2e"></div>
<div style="position:absolute;left:70%;bottom:38%;width:12%;aspect-ratio:1;border-radius:50%;background:#2d5f28"></div>
<div style="position:absolute;left:40%;bottom:0;width:20%;height:34%;background:linear-gradient(90deg,#cbb89a,#ddd0b5);clip-path:polygon(40% 0,60% 0,100% 100%,0 100%)"></div>"""
    site = f"""<div style="width:100%;height:100%;background:#fbfaf6;font-family:Inter;color:#1d2b1f;overflow:hidden">
  <div style="display:flex;align-items:center;justify-content:space-between;padding:20px 36px">
    <div style="display:flex;align-items:center;gap:10px;font:700 20px SG"><span style="width:28px;height:28px;border-radius:8px;background:#2f6a3a;display:inline-block"></span>Northbank Landscape Co.</div>
    <div style="display:flex;gap:26px;font:500 14px Inter;color:#4a5a4c;align-items:center">Services<span>Projects</span><span>About</span><span style="background:#2f6a3a;color:#fff;padding:9px 16px;border-radius:999px">Free estimate</span></div>
  </div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:30px;padding:30px 36px">
    <div style="padding-top:20px"><div style="font:600 12px Inter;letter-spacing:.25em;color:#2f6a3a">BUFFALO &amp; WESTERN NEW YORK</div>
      <div style="font:700 50px/1 SG;letter-spacing:-.03em;margin-top:16px">Yards worth coming home to.</div>
      <div style="font:400 16px/1.5 Inter;color:#55655a;margin-top:16px">Lawn care, landscaping and patios, done right the first time.</div>
      <div style="display:flex;gap:12px;margin-top:26px"><span style="background:#2f6a3a;color:#fff;padding:13px 22px;border-radius:999px;font:600 14px Inter">Get a free estimate</span><span style="border:1.5px solid #2f6a3a;color:#2f6a3a;padding:12px 20px;border-radius:999px;font:600 14px Inter">See our work</span></div></div>
    <div style="position:relative;height:300px;border-radius:16px;overflow:hidden">{hero_img}</div>
  </div>
  <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:16px;padding:6px 36px">
    {''.join(f'<div style="background:#eef2ea;border-radius:14px;padding:18px"><div style="font:700 17px SG">{a}</div><div style="font:400 13px/1.4 Inter;color:#5d6b60;margin-top:6px">{b}</div></div>' for a,b in [("Lawn care","Weekly mowing, edging and cleanup."),("Landscaping","Beds, plantings and fresh mulch."),("Hardscapes","Patios, walkways and retaining walls.")])}
  </div>
  <div style="margin:22px 36px 0;padding:18px 24px;border-radius:14px;background:#2f6a3a;color:#fff;display:flex;justify-content:space-between;align-items:center"><span style="font:700 18px SG">Proudly serving Buffalo, Amherst, Tonawanda &amp; Niagara Falls</span><span style="font:600 14px Inter;background:#fff;color:#2f6a3a;padding:10px 16px;border-radius:999px">Call for a quote</span></div></div>"""
    mobile = f"""<div style="width:100%;height:100%;background:#fbfaf6;font-family:Inter;color:#1d2b1f;overflow:hidden">
  <div style="height:40px"></div>
  <div style="display:flex;justify-content:space-between;align-items:center;padding:10px 20px;font:700 15px SG"><span style="display:flex;gap:8px;align-items:center"><span style="width:22px;height:22px;border-radius:6px;background:#2f6a3a;display:inline-block"></span>Northbank</span><span style="font:400 22px Inter">&#9776;</span></div>
  <div style="position:relative;height:200px;margin:10px 16px;border-radius:14px;overflow:hidden">{hero_img}</div>
  <div style="padding:12px 20px"><div style="font:700 30px/1.02 SG;letter-spacing:-.03em">Yards worth coming home to.</div>
  <div style="font:400 13px/1.5 Inter;color:#55655a;margin-top:10px">Lawn care, landscaping and patios in Buffalo &amp; WNY.</div>
  <div style="background:#2f6a3a;color:#fff;padding:13px;border-radius:999px;font:600 14px Inter;text-align:center;margin-top:18px">Get a free estimate</div></div></div>"""
    return f"""<div class="scene" style="background:linear-gradient(150deg,#e6ebe1,#cdd6c6)">
<div class="abs" style="left:90px;top:150px;width:1180px;height:760px;background:#1b1d1f;border-radius:30px 30px 0 0;padding:28px 28px 34px" >
  <div style="width:100%;height:100%;border-radius:6px;overflow:hidden">{site}</div></div>
<div class="abs" style="left:30px;top:910px;width:1300px;height:40px;background:linear-gradient(#d3d5d8,#9c9fa3);border-radius:0 0 30px 30px;box-shadow:0 40px 60px -10px rgba(0,0,0,.35)"></div>
<div class="abs" style="left:590px;top:910px;width:180px;height:14px;background:#b8babd;border-radius:0 0 14px 14px"></div>
<div class="abs sh" style="left:1190px;top:330px;width:330px;height:680px;border-radius:50px;background:#1b1d1f;padding:14px">
  <div style="width:100%;height:100%;border-radius:38px;overflow:hidden">{mobile}</div></div>
</div>"""

SCENES = [("brew-and-falls-coffee-brand-identity", coffee), ("ironwood-slice-menu-design", pizza),
          ("gorge-and-grain-barber-logo-refresh", barber), ("sugar-mist-bakery-social-media-pack", bakery),
          ("cobalt-canal-brewing-event-flyer", brewery), ("northbank-landscape-website", landscape)]

async def main():
    css = font_css() + BASE
    async with async_playwright() as p:
        exe = os.environ.get("CHROME_PATH")
        b = await (p.chromium.launch(executable_path=exe) if exe else p.chromium.launch())
        pg = await b.new_page(viewport={"width": 1600, "height": 1200})
        await pg.goto((ROOT / "index.html").as_uri())
        for name, fn in SCENES:
            await pg.set_content(f"<style>{css}</style>{fn()}")
            await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(300)
            im = Image.open(io.BytesIO(await pg.screenshot())).convert("RGB")
            if os.environ.get("PREVIEW"): im.save(f"/tmp/{name}.png")
            im.save(OUT / f"{name}.webp", quality=82, method=6)
            print(name, (OUT / f"{name}.webp").stat().st_size // 1024, "KB")
        await b.close()

asyncio.run(main())
