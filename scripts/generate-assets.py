"""
Regenerates the site's generated images (you normally never need to run this):
  images/og-image.png             1200x630 social share image
  images/icons/*.png              favicon / app icons from the JCP monogram
  images/portfolio/placeholder-*.webp   labeled placeholder portfolio images

Requires: pip install playwright pillow  &&  playwright install chromium
Run from the repo root:  python scripts/generate-assets.py
"""
import asyncio, io, os, pathlib
from playwright.async_api import async_playwright
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
FONTS = (ROOT / "fonts").as_uri()

BASE_CSS = f"""
@font-face{{font-family:Inter;src:url({FONTS}/inter-latin-wght-normal.woff2) format('woff2');font-weight:100 900}}
@font-face{{font-family:SG;src:url({FONTS}/space-grotesk-latin-wght-normal.woff2) format('woff2');font-weight:300 700}}
*{{margin:0;box-sizing:border-box}}
body{{background:#0a0a0a;color:#f5f5f7;font-family:Inter,sans-serif;overflow:hidden}}
"""

OG = BASE_CSS + """
.wrap{width:1200px;height:630px;position:relative;padding:72px 80px;display:flex;flex-direction:column;justify-content:space-between;overflow:hidden}
.glow{position:absolute;width:1100px;height:1100px;right:-420px;top:-560px;background:radial-gradient(closest-side,rgba(37,99,255,.55),rgba(37,99,255,.1) 55%,transparent 72%)}
.top{display:flex;align-items:center;gap:16px;font-weight:600;font-size:26px;position:relative}
.mark{background:#2563ff;color:#fff;font:700 22px/1 SG;padding:12px 14px;border-radius:12px}
h1{font:700 92px/0.95 SG;letter-spacing:-0.045em;max-width:15ch;position:relative}
h1 span{color:#5b8cff}
.bottom{display:flex;justify-content:space-between;color:#a1a1a6;font-size:24px;position:relative;border-top:1px solid rgba(255,255,255,.14);padding-top:24px}
"""
OG_HTML = """<div class="wrap"><div class="glow"></div>
<div class="top"><span class="mark">JCP</span>JCP Graphic Design</div>
<h1>Design that makes small businesses <span>look&nbsp;big.</span></h1>
<div class="bottom"><span>Graphic designer &middot; Niagara Falls, NY</span><span>Logos &middot; Menus &middot; Social &middot; Web</span></div></div>"""

ICON_HTML = """<div style="width:512px;height:512px;display:grid;place-items:center;background:{bg};border-radius:{r}px">
<div style="font:700 {fs}px/1 SG;letter-spacing:-0.04em;color:#fff">JCP</div></div>"""

PH_CSS = BASE_CSS + """
.ph{width:1600px;height:1200px;position:relative;overflow:hidden;display:flex;flex-direction:column;justify-content:space-between;padding:96px;background:#111113}
.ph .g{position:absolute;inset:0}
.cat{position:relative;font:600 30px/1 Inter;letter-spacing:.16em;text-transform:uppercase;color:#c7d6ff}
.big{position:relative;font:700 150px/0.92 SG;letter-spacing:-0.05em}
.big span{color:#5b8cff}
.tag{position:relative;display:inline-flex;gap:16px;align-items:center;font:500 34px/1 Inter;color:#d1d1d6;border:2px dashed rgba(255,255,255,.35);border-radius:999px;padding:22px 34px;align-self:flex-start}
.shape{position:absolute;right:96px;top:50%;transform:translateY(-50%)}
"""
PLACEHOLDERS = [
  ("Logo design",     "radial-gradient(circle at 80% 30%, rgba(37,99,255,.55), transparent 55%)",
   '<svg class="shape" width="420" height="420" viewBox="0 0 100 100"><circle cx="50" cy="50" r="46" fill="none" stroke="#5b8cff" stroke-width="3"/><circle cx="50" cy="50" r="22" fill="#2563ff"/></svg>'),
  ("Brand kit",       "linear-gradient(135deg, rgba(37,99,255,.35), transparent 60%)",
   '<div class="shape" style="display:grid;grid-template-columns:repeat(2,180px);gap:24px"><div style="height:180px;border-radius:28px;background:#2563ff"></div><div style="height:180px;border-radius:28px;background:#f5f5f7"></div><div style="height:180px;border-radius:28px;background:#2a2a2e"></div><div style="height:180px;border-radius:28px;border:3px solid #5b8cff"></div></div>'),
  ("Restaurant menu", "radial-gradient(circle at 20% 90%, rgba(37,99,255,.45), transparent 55%)",
   '<div class="shape" style="width:360px;height:520px;border-radius:20px;background:#f5f5f7;padding:40px;display:grid;gap:22px;align-content:start"><div style="height:34px;width:60%;background:#0a0a0a;border-radius:6px"></div><div style="height:14px;background:#c7c7cc;border-radius:4px"></div><div style="height:14px;width:80%;background:#c7c7cc;border-radius:4px"></div><div style="height:14px;width:90%;background:#c7c7cc;border-radius:4px"></div><div style="height:30px;width:45%;background:#2563ff;border-radius:6px;margin-top:20px"></div><div style="height:14px;background:#c7c7cc;border-radius:4px"></div><div style="height:14px;width:70%;background:#c7c7cc;border-radius:4px"></div></div>'),
  ("Flyer & print",   "linear-gradient(200deg, rgba(37,99,255,.5), transparent 55%)",
   '<div class="shape" style="width:380px;height:520px;border-radius:12px;background:#2563ff;transform:translateY(-50%) rotate(6deg);box-shadow:0 40px 80px rgba(0,0,0,.5);padding:40px;font:700 80px/0.9 SG;color:#fff;letter-spacing:-0.04em">BIG<br>SALE</div>'),
  ("Social media",    "radial-gradient(circle at 75% 75%, rgba(37,99,255,.5), transparent 55%)",
   '<div class="shape" style="display:grid;grid-template-columns:repeat(3,140px);gap:14px"><div style="height:140px;border-radius:18px;background:#2563ff"></div><div style="height:140px;border-radius:18px;background:#2a2a2e"></div><div style="height:140px;border-radius:18px;background:#f5f5f7"></div><div style="height:140px;border-radius:18px;background:#2a2a2e"></div><div style="height:140px;border-radius:18px;background:#5b8cff"></div><div style="height:140px;border-radius:18px;background:#2a2a2e"></div><div style="height:140px;border-radius:18px;background:#f5f5f7"></div><div style="height:140px;border-radius:18px;background:#2a2a2e"></div><div style="height:140px;border-radius:18px;background:#2563ff"></div></div>'),
  ("Website",         "linear-gradient(160deg, transparent 40%, rgba(37,99,255,.45))",
   '<div class="shape" style="width:560px;height:400px;border-radius:20px;background:#1c1c1f;border:2px solid #3a3a3e;overflow:hidden"><div style="height:44px;background:#2a2a2e;display:flex;gap:10px;align-items:center;padding-left:18px"><i style="width:14px;height:14px;border-radius:50%;background:#5b8cff"></i><i style="width:14px;height:14px;border-radius:50%;background:#555"></i><i style="width:14px;height:14px;border-radius:50%;background:#555"></i></div><div style="padding:40px;display:grid;gap:18px"><div style="height:40px;width:75%;background:#f5f5f7;border-radius:6px"></div><div style="height:14px;width:55%;background:#636366;border-radius:4px"></div><div style="height:52px;width:200px;background:#2563ff;border-radius:999px;margin-top:20px"></div></div></div>'),
]

def ph_html(i, cat, bg, shape):
    return f"""<div class="ph"><div class="g" style="background:{bg}"></div>{shape}
<div class="cat">{cat}</div>
<div class="big">Your<br>work<br><span>here.</span></div>
<div class="tag">Placeholder &mdash; your work here &middot; #{i}</div></div>"""

async def shot(page, css, html, w, h, transparent=False):
    await page.set_viewport_size({"width": w, "height": h})
    await page.set_content(f"<style>{css}</style>{html}")
    await page.evaluate("document.fonts.ready")
    await page.wait_for_timeout(150)
    return Image.open(io.BytesIO(await page.screenshot(clip={"x": 0, "y": 0, "width": w, "height": h}, omit_background=transparent)))

async def main():
    async with async_playwright() as p:
        exe = os.environ.get("CHROME_PATH")  # optional: path to an installed Chrome
        b = await (p.chromium.launch(executable_path=exe) if exe else p.chromium.launch())
        page = await b.new_page()
        page.set_default_timeout(20000)
        await page.goto((ROOT / "index.html").as_uri())  # file:// origin so local fonts load

        og = await shot(page, OG, OG_HTML, 1200, 630)
        og.convert("RGB").save(ROOT / "images/og-image.png", optimize=True)

        icons = ROOT / "images/icons"
        rounded = await shot(page, BASE_CSS + "body{background:transparent}", ICON_HTML.format(bg="#2563ff", r=96, fs=190), 512, 512, transparent=True)
        square = await shot(page, BASE_CSS, ICON_HTML.format(bg="#2563ff", r=0, fs=150), 512, 512)
        for size, name, src in [(32, "favicon-32.png", rounded), (192, "icon-192.png", rounded), (512, "icon-512.png", rounded),
                                (180, "apple-touch-icon.png", square), (512, "icon-512-maskable.png", square)]:
            src.resize((size, size), Image.LANCZOS).save(icons / name, optimize=True)

        for i, (cat, bg, shape) in enumerate(PLACEHOLDERS, 1):
            im = await shot(page, PH_CSS, ph_html(i, cat, bg, shape), 1600, 1200)
            im.convert("RGB").resize((1200, 900), Image.LANCZOS).save(ROOT / f"images/portfolio/placeholder-{i}.webp", quality=80, method=6)
        await b.close()

asyncio.run(main())
