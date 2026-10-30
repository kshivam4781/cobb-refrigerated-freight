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

### Quote forms

Every quote form (hero card, quote dialog, contact page) emails requests to `QUOTE_EMAIL` in `build.py`. It sends through
[Web3Forms](https://web3forms.com) when `WEB3FORMS_ACCESS_KEY` is set, and falls back to [FormSubmit](https://formsubmit.co), which emails the
request to the address in `FORM_ENDPOINT` at the top of `build.py`. To change the recipient, edit that line, run
`python build.py`, push, and confirm the one-time activation email FormSubmit sends to the new address.

### Custom domain

To use a domain like `cobbrefrigerated.com`: add it under **Settings → Pages → Custom domain**, then update `SITE` and
`BASE_PATH` at the top of `build.py` and rebuild.

## Brand

- Logo files: `assets/brand/` (`logo.svg`, `logo-white.svg`, `mark.svg`, `favicon.svg`, PNG exports)
- Colors: Navy `#0B2A5B` · Blue `#1565D8` · Ice `#38B6FF`
- Fonts: Archivo Expanded (headlines), Inter (body), JetBrains Mono (data labels), Montserrat ExtraBold (logo wordmark)
- Logo concepts and template explorations: `design/` (`design/build_logos.py` regenerates the logo)

## Credits

- Photography: AI-generated with Google Gemini, except the produce photo by [@louisllp on Unsplash](https://unsplash.com/photos/crates-of-peppers-and-cabbage-e5YH11u1lSw) (Unsplash License).
- Carrier data: [FMCSA SAFER Company Snapshot](https://safer.fmcsa.dot.gov/query.asp?searchtype=ANY&query_type=queryCarrierSnapshot&query_param=USDOT&query_string=145920).
