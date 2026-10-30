"""Builds the static site: wraps src/pages/*.html in src/layout.html and writes them to the repo root.

Run:  python build.py
Then commit the generated .html files — GitHub Pages serves the repo root as-is.
"""
import datetime
import json
from pathlib import Path

ROOT = Path(__file__).parent
SRC = ROOT / "src"

# Public URL of the site. If a custom domain is added later, change both values
# (e.g. SITE = "https://www.cobbrefrigerated.com/", BASE_PATH = "/").
SITE = "https://kshivam4781.github.io/cobb-refrigerated-freight/"
BASE_PATH = "/cobb-refrigerated-freight/"

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
        "title": "Page Not Found | Cobb Refrigerated Freight",
        "description": "The page you were looking for could not be found.",
        # GitHub Pages serves 404.html from any missing path, so relative links need an absolute base.
        "head_extra": f'  <base href="{BASE_PATH}">\n  <meta name="robots" content="noindex">',
        "sitemap": False,
    },
}


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
            "head_extra": meta.get("head_extra", ""),
            "body": (SRC / "pages" / name).read_text(encoding="utf-8").rstrip(),
        }
        for key, val in values.items():
            html = html.replace("{{%s}}" % key, val)
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
        "theme_color": "#0B2A5B",
        "icons": [
            {"src": "assets/brand/apple-touch-icon.png", "sizes": "180x180", "type": "image/png"},
            {"src": "assets/brand/icon-512.png", "sizes": "512x512", "type": "image/png"},
        ],
    }, indent=2), encoding="utf-8")
    print("built sitemap.xml, robots.txt, site.webmanifest")


if __name__ == "__main__":
    build()
