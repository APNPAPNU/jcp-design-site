# JCP Graphic Design: portfolio website

One-page portfolio site for **Jonathan Pettit / JCP Graphic Design**, an affordable freelance graphic designer for small businesses, based in Niagara Falls, NY and working with clients anywhere in the US and beyond (everything is done online).

- **Live site:** https://apnpapnu.github.io/jcp-design-site/
- **Built with:** plain HTML, CSS and a little vanilla JavaScript. No build step, no frameworks, no paid services.
- **Hosting:** GitHub Pages, deployed straight from the `main` branch (repo root). Every push to `main` updates the live site within a minute or two.

---

## File structure

```
jcp-design-site/
├── index.html              ← the whole website (all sections + text + prices)
├── 404.html                ← "page not found" page
├── thanks.html             ← thank-you page (used only if a visitor has JavaScript off)
├── css/styles.css          ← all styling (colors are at the top in :root)
├── js/portfolio.js         ← ★ THE PORTFOLIO LIST: edit this to change your work
├── js/main.js              ← menu, animations, lightbox, contact form, footer year
├── images/
│   ├── portfolio/          ← ★ put your portfolio images here
│   ├── about/              ← your portrait (jonathan-pettit.webp + .jpg)
│   ├── icons/              ← favicon + app icons (JCP monogram)
│   └── og-image.png        ← 1200×630 preview image for Facebook/LinkedIn/texts
├── fonts/                  ← self-hosted Inter + Space Grotesk (fast, private)
├── sitemap.xml, robots.txt, site.webmanifest
├── .nojekyll               ← tells GitHub Pages to serve files as-is
└── scripts/
    ├── set-site-url.sh     ← swaps the site address everywhere (for a custom domain)
    ├── generate-assets.py  ← regenerates og-image + icons (optional)
    └── generate-concepts.py← regenerates the 6 concept portfolio mockups (optional)
```

---

## Editing on GitHub (no software needed)

You can do every change below right in your browser:
1. Open https://github.com/APNPAPNU/jcp-design-site
2. Click the file you want → the **pencil icon** (Edit) → make your change → **Commit changes**.
3. To upload images: open the folder (e.g. `images/portfolio`) → **Add file → Upload files**.
4. Wait 1–2 minutes, then refresh the live site (hard refresh: Ctrl+Shift+R / Cmd+Shift+R).

---

## Swap in your portfolio images (step by step)

**Right now** the gallery shows 6 **concept projects** for *fictional* businesses (Brew & Falls Coffee, Ironwood Slice Co., Gorge & Grain Barber Co., Sugar Mist Bakery, Cobalt Canal Brewing, Northbank Landscape Co.). Each one is clearly tagged "Concept project" on the card and in the lightbox, and the section intro says client work is coming soon. Swap them out for real client work as you get it.

1. **Prepare each image**
   - Shape: **4:3 landscape** looks best in the grid (other shapes are cropped to fit on the grid but shown whole in the lightbox).
   - Size: **1600 × 1200 px** (1200 × 900 is fine too).
   - Format: **.webp** (smallest) or **.jpg**. Aim for **under ~300 KB** each. Free tool: https://squoosh.app (choose WebP, quality ~80).
   - Name: lowercase with dashes, no spaces, e.g. `bills-pizza-menu.webp`.
2. **Upload** them into `images/portfolio/`.
3. **Edit `js/portfolio.js`**. Each `{ ... }` block is one project:
   ```js
   {
     file: "bills-pizza-menu.webp",
     title: "Bill's Pizza \u2014 Menu design",
     category: "Menu design",
     alt: "Two-page takeout menu design for Bill's Pizza in Niagara Falls",
     width: 1600, height: 1200
   },
   ```
   - `file` must match the file name exactly (capitals matter).
   - `alt` = a short description of the image (helps blind visitors and Google).
   - `width`/`height` = the image's real pixel size.
   - **Real client work: leave out `concept: true`.** That line is what adds the "Concept project" tag.
   - The order of blocks = order on the page. Keep the commas between blocks.
4. **Remove a concept**: delete its block in `js/portfolio.js` and its image file. When all six are gone, change the portfolio intro text in `index.html` (search for "Concept projects showing").
5. To tweak or re-render the concepts: `python scripts/generate-concepts.py` (needs Playwright + Pillow; set `CHROME_PATH` to use an installed Chrome).

### Your portrait
`images/about/jonathan-pettit.webp` and `.jpg` (880 × 1100, 4:5, metadata stripped). To replace, upload new files with the same names and size ratio.

---

## Current prices & what's included

| Service | Price | Includes |
|---|---|---|
| Business listing setup | $50 | Google Business Profile, Yelp & Tripadvisor: hours, services/menu, description and photos added or updated. Client keeps ownership; Google may require the owner to verify. |
| Flyer, menu & print design | $60 | 1 flyer, poster or one-page menu (front & back), unlimited small revisions, print-ready PDF + web/social image |
| Social media graphics pack | $75 | 6 custom post designs, feed + story sizes for Instagram & Facebook, editable Canva templates, unlimited small revisions |
| Logo refresh | $90 | 2 refreshed directions, unlimited small revisions, color / black & white / white versions, PNG, JPG, SVG & PDF |
| New logo + brand kit | $175 | 3 initial concepts; main logo, alternate layout & icon; color palette, font pairing & 1-page brand guide; business card design; all file formats |
| Monthly social media graphics | $200/mo | 12 custom posts a month (about 3/week) around promos, specials & holidays; feed + story sizes; one monthly batch; unlimited small revisions |
| Small business website | $250 | Up to 4 pages, mobile-friendly, working contact form, basic Google SEO, free hosting set up (domain ~$10–12/yr not included) |

These were set against 2025–26 market rates for newer freelancers competing on price (Fiverr flyers ~$35–80, beginner logos ~$20–100, marketplace logo + brand kits ~$165–270, monthly social retainers ~$200–400). Adjust them anytime.

## Edit prices and text

- **Prices:** open `index.html`, search for `card__price`. Each service card has a line like `<p class="card__price">$90</p>`. Change the number. The "what's included" bullets are the `<li>` lines inside `<ul class="card__list">` on the same card.
  Also update the matching option in the contact form (search for `f-service`) and the `"price"` values in the JSON-LD block near the top (that's what Google reads).
- **Any other text** (headline, FAQ answers, about blurb): open `index.html` and edit the words between the tags. Each section is marked with a big comment like `<!-- ===== 2. SERVICES & PRICING ===== -->`.
- **Accent color:** `css/styles.css`, top of the file: `--accent` (buttons) and `--accent-text` (blue text). Keep enough contrast with black.

### Please confirm (written generically, not invented policy)
- **FAQ → Payment:** says "typically a deposit to start and the balance on delivery, payable through common methods." Change it to your real terms (e.g. 50% deposit, Venmo/PayPal/Zelle/card).
- **FAQ → Turnaround:** "within a few days of approving the mockup."
- **FAQ → Revisions:** "small revisions are unlimited."
- **Free mockup** wording ("no obligation to continue").

### Testimonials
The three cards are clearly marked placeholders. Replace them with **real** client quotes (with permission). Never invent reviews.
To hide the section until you have real ones, change `<section class="section" id="testimonials"` to `<section hidden class="section" id="testimonials"`.

---

## How the contact form works

The form sends messages to **jcpgraphicdesign@gmail.com** using **FormSubmit** (https://formsubmit.co, free, no account).

- With JavaScript on (normal), it submits in the background and shows "Thanks!" or an error inline. Without JavaScript, it falls back to a regular form post and lands on `thanks.html`.
- Fields: name, email, business name, service, message, plus a hidden **honeypot** field (`_honey`) that catches spam bots.
- **One-time activation:** the very first submission makes FormSubmit email jcpgraphicdesign@gmail.com a message titled something like *"Action Required: Activate FormSubmit on …"*. Click **Activate Form** in that email. Until you do, messages are held, not lost (FormSubmit keeps them 30 days). Check spam if you don't see it.
- Replies: just hit "Reply" in Gmail; it goes to the visitor's email.

**Change the destination email:** in `index.html`, find `action="https://formsubmit.co/jcpgraphicdesign@gmail.com"` and change the address (it will need activating again).
*Optional:* after activation, FormSubmit shows a random alias (like `formsubmit.co/abc123…`). You can use that in `action` instead of your email to hide your address from spam bots.

**Switch to Web3Forms instead** (also free, 250 submissions/month):
1. Go to https://web3forms.com, create an access key for jcpgraphicdesign@gmail.com (it's emailed to you).
2. In `index.html`, change the form's `action` to `https://api.web3forms.com/submit`.
3. Paste the key into `<input type="hidden" name="access_key" value="">`.
The JavaScript detects Web3Forms automatically; nothing else to change.

---

## Site address (canonical / social / sitemap URLs)

A few places need the site's full address: the canonical link, Open Graph + Twitter tags, JSON-LD, `sitemap.xml`, `robots.txt`, and the `_next` thank-you redirect in the form. They're currently set to:

`https://apnpapnu.github.io/jcp-design-site`

Files containing it: `index.html`, `sitemap.xml`, `robots.txt`.
To change it (e.g. when you get a custom domain), run from the repo folder:
```bash
./scripts/set-site-url.sh https://www.yourdomain.com
```
...or do a find-and-replace of `https://apnpapnu.github.io/jcp-design-site` in those 3 files on GitHub. No trailing slash.

---

## Connect a custom domain (about $10–12/yr)

### 1. Buy the domain
- **Cloudflare Registrar** (at-cost pricing, ~$10/yr for .com): https://dash.cloudflare.com → sign up → **Domain Registration → Register Domains** → search → buy.
- **Porkbun** (~$11/yr, free WHOIS privacy): https://porkbun.com → search → add to cart → checkout.
Idea: `jcpgraphicdesign.com`, `jcpdesign.co`, `jonathanpettitdesign.com`.

### 2. Tell GitHub about the domain
1. Repo → **Settings → Pages → Custom domain** → type `www.yourdomain.com` → **Save**.
   (This creates a `CNAME` file in the repo containing just `www.yourdomain.com`. You can also add that file yourself.)
2. Optional but recommended: verify the domain at **GitHub → your profile Settings → Pages → Add a domain** (prevents takeovers).

### 3. Add DNS records at your registrar

| Type  | Name / Host | Value |
|-------|-------------|-------|
| A     | `@`   | `185.199.108.153` |
| A     | `@`   | `185.199.109.153` |
| A     | `@`   | `185.199.110.153` |
| A     | `@`   | `185.199.111.153` |
| AAAA  | `@`   | `2606:50c0:8000::153` |
| AAAA  | `@`   | `2606:50c0:8001::153` |
| AAAA  | `@`   | `2606:50c0:8002::153` |
| AAAA  | `@`   | `2606:50c0:8003::153` |
| CNAME | `www` | `apnpapnu.github.io` |

Delete any existing "parking" A/CNAME/ALIAS records for `@` or `www` first.

**On Cloudflare:** Dashboard → your domain → **DNS → Records → Add record**. For every record above, set **Proxy status to "DNS only" (grey cloud)**, at least until GitHub has issued the HTTPS certificate (step 4). Proxied/orange records block GitHub's certificate. Afterwards you may leave them grey (simplest) or switch to orange with SSL/TLS mode **Full**.

**On Porkbun:** Domain Management → your domain → **DNS** → delete the default parking records (ALIAS/CNAME to `pixie.porkbun.com`) → add the records above (leave Host blank for `@`, `www` for the CNAME). TTL 600 is fine.

### 4. Turn on HTTPS
DNS can take from minutes up to 24 hours. Back in **Settings → Pages**, wait until the DNS check is green, then tick **Enforce HTTPS** (if greyed out, the certificate is still being issued: wait up to an hour and refresh).

### 5. Update the site address
```bash
./scripts/set-site-url.sh https://www.yourdomain.com
git commit -am "Use custom domain" && git push
```
Then submit `https://www.yourdomain.com/sitemap.xml` in Google Search Console (free) and add the site to your **Google Business Profile**, which helps people find you when they search for "freelance graphic designer" or "graphic designer near me".

---

## Run it locally (optional)
```bash
python3 -m http.server 8000   # then open http://localhost:8000
```

## Regenerate images (optional)
`scripts/generate-assets.py` rebuilds the OG image, icons and placeholders with headless Chromium:
`pip install playwright pillow && playwright install chromium && python scripts/generate-assets.py`
