# Cobb Refrigerated Freight — Website

Static website for **Cobb Refrigerated Freight Inc**, Modesto, CA (USDOT 145920 · MC-147824).

**Live site:** https://kshivam4781.github.io/cobb-refrigerated-freight/

## Pages

| Page | File |
| --- | --- |
| Home | `index.html` |
| Services (Storage, Transportation, Cross Dock, Truck & Trailer Repair, Roadside Service) | `services.html` |
| About & Safety record | `about.html` |
| Contact & Quote | `contact.html` |
| Not found | `404.html` |

## Editing

Page content lives in `src/pages/`, and the shared header, footer, and SEO tags live in `src/layout.html`.
After editing, rebuild and commit:

```bash
python build.py
```

The generated `*.html`, `sitemap.xml`, `robots.txt`, and `site.webmanifest` in the repo root are what GitHub Pages serves.

### Turning on the online quote form

The contact page shows a "call us" card until a form delivery address is configured. To receive form submissions by email
(free, via [FormSubmit](https://formsubmit.co)), set `data-endpoint` on the form in `src/pages/contact.html`:

```html
<form ... data-quote-form data-endpoint="https://formsubmit.co/ajax/dispatch@yourdomain.com" hidden novalidate>
```

Run `python build.py`, push, then confirm the activation email FormSubmit sends on the first submission.

### Custom domain

To use a domain like `cobbrefrigerated.com`: add it under **Settings → Pages → Custom domain**, then update `SITE` and
`BASE_PATH` at the top of `build.py` and rebuild.

## Brand

- Logo files: `assets/brand/` (`logo.svg`, `logo-white.svg`, `mark.svg`, `favicon.svg`, PNG exports)
- Colors: Navy `#0B2A5B` · Blue `#1565D8` · Ice `#38B6FF`
- Fonts: Barlow Condensed (headlines), Inter (body), Montserrat ExtraBold (logo wordmark)
- Logo concepts and template explorations: `design/` (`design/build_logos.py` regenerates the logo)

## Credits

- Photography: AI-generated with Google Gemini, except the produce photo by [@louisllp on Unsplash](https://unsplash.com/photos/crates-of-peppers-and-cabbage-e5YH11u1lSw) (Unsplash License).
- Carrier data: [FMCSA SAFER Company Snapshot](https://safer.fmcsa.dot.gov/query.asp?searchtype=ANY&query_type=queryCarrierSnapshot&query_param=USDOT&query_string=145920).
