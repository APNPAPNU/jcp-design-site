"""
Regenerates the site's generated images (you normally never need to run this):
  images/og-image.png             1200x630 social share image
  images/icons/*.png              favicon / app icons from the JCP monogram

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

        await b.close()

asyncio.run(main())
