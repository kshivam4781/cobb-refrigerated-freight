"""Builds the static site: wraps src/pages/*.html in src/layout.html and writes them to the repo root.

Run:  python build.py
Then commit the generated .html files — GitHub Pages serves the repo root as-is.

Template tokens available in pages and layout:
  {{form:<prefix>:<compact|full>}}  quote form that emails FORM_ENDPOINT
  {{lanes_svg}}                     distance map centered on the Modesto yard
"""
import datetime
import json
import math
import re
from pathlib import Path

ROOT = Path(__file__).parent
SRC = ROOT / "src"

# Public URL of the site. If a custom domain is added later, change both values
# (e.g. SITE = "https://www.cobbrefrigerated.com/", BASE_PATH = "/").
SITE = "https://kshivam4781.github.io/cobb-refrigerated-freight/"
BASE_PATH = "/cobb-refrigerated-freight/"

# Where quote requests are emailed (FormSubmit AJAX endpoint).
FORM_ENDPOINT = "https://formsubmit.co/ajax/shivam@skytransportsolutions.com"

PAGES = {
    "index.html": {
        "nav": "home",
        "title": "Cobb Refrigerated Freight | Refrigerated Trucking & Cold Storage in Modesto, CA",
        "description": "Refrigerated transportation, cold storage, cross-dock, truck & trailer repair, and roadside service from our Modesto, California yard. Call (209) 576-0327.",
    },
    "services.html": {
        "nav": "services",
        "title": "Services | Storage, Reefer Transportation, Cross Dock, Truck Repair | Cobb Refrigerated Freight",
        "description": "Temperature-controlled storage, refrigerated truckload transportation, cross-docking, truck and trailer repair, and roadside service in Modesto, CA.",
    },
    "about.html": {
        "nav": "about",
        "title": "About Us & Safety Record | Cobb Refrigerated Freight, Modesto CA",
        "description": "Cobb Refrigerated Freight Inc — USDOT 145920, MC-147824, Satisfactory FMCSA safety rating. An asset-based refrigerated carrier in Modesto, California.",
    },
    "contact.html": {
        "nav": "contact",
        "title": "Contact & Request a Quote | Cobb Refrigerated Freight",
        "description": "Request a refrigerated freight, storage, or cross-dock quote, or call for truck repair and roadside service: (209) 576-0327. 420 California Ave, Modesto, CA 95351.",
    },
    "404.html": {
        "nav": "",
        "header": "solid",
        "title": "Page Not Found | Cobb Refrigerated Freight",
        "description": "The page you were looking for could not be found.",
        # GitHub Pages serves 404.html from any missing path, so relative links need an absolute base.
        "head_extra": f'  <base href="{BASE_PATH}">\n  <meta name="robots" content="noindex">',
        "sitemap": False,
    },
}

SERVICES = ["Transportation", "Storage", "Cross Dock", "Truck & Trailer Repair", "Roadside Service"]


def field(p, name, label, kind="text", required=False, auto="", placeholder="", full=False):
    req = " required" if required else ""
    opt = "" if required else ' <span class="opt">(optional)</span>'
    ac = f' autocomplete="{auto}"' if auto else ""
    ph = f' placeholder="{placeholder}"' if placeholder else ""
    if kind == "textarea":
        ctrl = f'<textarea id="{p}-{name}" name="{name}" rows="4"{ph}{req}></textarea>'
    else:
        ctrl = f'<input id="{p}-{name}" name="{name}" type="{kind}"{ac}{ph}{req}>'
    return f'<div class="field"><label for="{p}-{name}">{label}{opt}</label>{ctrl}</div>'


def quote_form(p, variant):
    """Quote request form. 'compact' fits the hero card; 'full' is used in the dialog and contact page."""
    if variant == "compact":
        svc = "".join(
            f'<label><input type="radio" name="service" value="{v}"{" checked" if i == 0 else ""}><span>{t}</span></label>'
            for i, (v, t) in enumerate((("Transportation", "Freight"), ("Storage", "Storage"), ("Truck & Trailer Repair", "Repair")))
        )
        rows = [
            f'<fieldset style="border:0;margin:0;padding:0"><legend class="sr-only">Service</legend><div class="seg">{svc}</div></fieldset>',
            '<div class="form-row">'
            + field(p, "pickup", "Pickup city / ZIP", required=True, placeholder="City or ZIP")
            + field(p, "delivery", "Delivery city / ZIP", required=True, placeholder="City or ZIP")
            + "</div>",
            '<div class="form-row">'
            + field(p, "name", "Your name", required=True, auto="name")
            + field(p, "phone", "Phone", "tel", required=True, auto="tel", placeholder="(209) 555-0100")
            + "</div>",
            field(p, "email", "Email", "email", required=True, auto="email", placeholder="you@company.com"),
        ]
        cta = "Get my quote"
    else:
        opts = "".join(f"<option>{s.replace('&', '&amp;')}</option>" for s in SERVICES)
        rows = [
            f'<div class="field"><label for="{p}-service">Service needed</label><select id="{p}-service" name="service" required>{opts}</select></div>',
            '<div class="form-row">'
            + field(p, "name", "Full name", required=True, auto="name")
            + field(p, "company", "Company", auto="organization")
            + "</div>",
            '<div class="form-row">'
            + field(p, "phone", "Phone", "tel", required=True, auto="tel", placeholder="(209) 555-0100")
            + field(p, "email", "Email", "email", required=True, auto="email", placeholder="you@company.com")
            + "</div>",
            '<div class="form-row">'
            + field(p, "pickup", "Pickup location", placeholder="City, state or ZIP")
            + field(p, "delivery", "Delivery location", placeholder="City, state or ZIP")
            + "</div>",
            '<div class="form-row">'
            + field(p, "commodity", "Commodity &amp; weight", placeholder="e.g. Produce, 40,000 lb")
            + f'<div class="field"><label for="{p}-temp">Temperature <span class="opt">(optional)</span></label>'
            f'<select id="{p}-temp" name="temperature"><option value="">Select…</option><option>Frozen</option>'
            f"<option>Chilled / fresh</option><option>Dry / ambient</option><option>Not applicable</option></select></div>"
            + "</div>",
            field(p, "details", "Details", "textarea", placeholder="Dates, number of loads, equipment, truck/trailer issue…"),
        ]
        cta = "Send request"
    return f"""    <form class="form" data-quote data-endpoint="{FORM_ENDPOINT}" novalidate>
      {''.join(rows)}
      <div class="hp" aria-hidden="true"><label>Leave this empty <input name="_honey" tabindex="-1" autocomplete="off"></label></div>
      <div class="form-error" role="alert">Sorry &mdash; that didn&rsquo;t go through. Please call <a href="tel:+12095760327">(209) 576-0327</a>.</div>
      <button class="btn btn-primary btn-block" type="submit">{cta} <svg class="ico i-arrow" aria-hidden="true"><use href="#i-arrow"/></svg></button>
      <p class="form-foot"><svg class="ico" aria-hidden="true"><use href="#i-lock"/></svg>Your request goes directly to our team.</p>
    </form>
    <div class="form-success" role="status">
      <div class="check"><svg class="ico" aria-hidden="true"><use href="#i-check"/></svg></div>
      <h3>Request received</h3>
      <p>Thanks &mdash; our team will reach out shortly. Need it sooner? Call <a href="tel:+12095760327">(209) 576-0327</a>.</p>
      <button class="btn btn-line" type="button" data-reset-form style="margin-top:14px">Send another request</button>
    </div>"""


# Approximate road miles from the Modesto yard and compass bearings, for the lanes map.
LANES = [
    ("Stockton", 30, 335, "end"),
    ("Sacramento", 75, 348, "start"),
    ("Bay Area", 85, 283, "end"),
    ("San Jose", 85, 250, "end"),
    ("Fresno", 95, 132, "start"),
    ("Bakersfield", 205, 146, "start"),
    ("Los Angeles", 310, 150, "start"),
    ("Reno", 205, 42, "start"),
]


def lanes_svg():
    c, scale = 300, lambda mi: 34 + mi * 0.78
    vb = (120, 60, 440, 540)  # crop to where the destinations are; rings run off the edges like a radar
    out = [f'<svg viewBox="{vb[0]} {vb[1]} {vb[2]} {vb[3]}" role="img" aria-labelledby="lanes-t">',
           '<title id="lanes-t">Approximate road miles from our Modesto yard to major California markets and Reno</title>',
           '<defs><linearGradient id="routeGrad" x1="0" y1="0" x2="1" y2="1">'
           '<stop offset="0" stop-color="#38B6FF"/><stop offset="1" stop-color="#1565D8"/></linearGradient></defs>']
    for mi in (100, 200, 300):
        r = scale(mi)
        out.append(f'<circle class="ring" cx="{c}" cy="{c}" r="{r:.1f}"/>')
        a = math.radians(200)
        out.append(f'<text class="ring-label" x="{c + r * math.sin(a):.1f}" y="{c - r * math.cos(a) + 14:.1f}" text-anchor="middle">{mi} MI</text>')
    for name, mi, bearing, anchor in LANES:
        r = scale(mi)
        a = math.radians(bearing)
        x, y = c + r * math.sin(a), c - r * math.cos(a)
        mx, my = c + r * 0.55 * math.sin(a) + 14 * math.cos(a), c - r * 0.55 * math.cos(a) + 14 * math.sin(a)
        out.append(f'<path class="route" d="M{c} {c} Q{mx:.1f} {my:.1f} {x:.1f} {y:.1f}"/>')
        dx = 11 if anchor == "start" else -11
        out.append(f'<circle class="node" cx="{x:.1f}" cy="{y:.1f}" r="5"/>')
        out.append(f'<text class="city" x="{x + dx:.1f}" y="{y - 1:.1f}" text-anchor="{anchor}">{name}</text>')
        out.append(f'<text class="mi" x="{x + dx:.1f}" y="{y + 13:.1f}" text-anchor="{anchor}">~{mi} MI</text>')
    out.append(f'<circle class="pulse" cx="{c}" cy="{c}" r="10"/><circle class="hub" cx="{c}" cy="{c}" r="9"/>')
    out.append(f'<circle cx="{c}" cy="{c}" r="3.5" fill="#04122A"/>')
    out.append("</svg>")
    out.append('<div class="lanes-legend"><span><i></i>Modesto yard &middot; 420 California Ave</span><span><i class="n"></i>Destination &middot; approx. road miles</span></div>')
    return "".join(out)


def render_tokens(html):
    html = re.sub(r"\{\{form:(\w+):(compact|full)\}\}", lambda m: quote_form(m.group(1), m.group(2)), html)
    return html.replace("{{lanes_svg}}", lanes_svg())


def build():
    layout = (SRC / "layout.html").read_text(encoding="utf-8")
    version = datetime.datetime.now().strftime("%Y%m%d%H%M")
    for name, meta in PAGES.items():
        canonical = SITE if name == "index.html" else SITE + name
        html = layout
        for key in ("home", "services", "about", "contact"):
            html = html.replace("{{nav_%s}}" % key, ' aria-current="page"' if meta["nav"] == key else "")
        values = {
            "title": meta["title"],
            "description": meta["description"],
            "canonical": canonical,
            "site": SITE,
            "version": version,
            "header_mode": meta.get("header", "overlay"),
            "head_extra": meta.get("head_extra", ""),
            "body": (SRC / "pages" / name).read_text(encoding="utf-8").rstrip(),
        }
        for key, val in values.items():
            html = html.replace("{{%s}}" % key, val)
        html = render_tokens(html)
        leftover = re.findall(r"\{\{[^}]+\}\}", html)
        if leftover:
            raise SystemExit(f"{name}: unreplaced tokens {leftover}")
        (ROOT / name).write_text(html, encoding="utf-8")
        print("built", name)

    today = datetime.date.today().isoformat()
    urls = "".join(
        f"  <url><loc>{SITE if n == 'index.html' else SITE + n}</loc><lastmod>{today}</lastmod></url>\n"
        for n, m in PAGES.items() if m.get("sitemap", True)
    )
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + "</urlset>\n",
        encoding="utf-8",
    )
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}sitemap.xml\n", encoding="utf-8")
    (ROOT / "site.webmanifest").write_text(json.dumps({
        "name": "Cobb Refrigerated Freight",
        "short_name": "Cobb Freight",
        "start_url": BASE_PATH,
        "display": "standalone",
        "background_color": "#ffffff",
        "theme_color": "#04122A",
        "icons": [
            {"src": "assets/brand/apple-touch-icon.png", "sizes": "180x180", "type": "image/png"},
            {"src": "assets/brand/icon-512.png", "sizes": "512x512", "type": "image/png"},
        ],
    }, indent=2), encoding="utf-8")
    print("built sitemap.xml, robots.txt, site.webmanifest")


if __name__ == "__main__":
    build()
