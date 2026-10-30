# Cobb Refrigerated Freight Website

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

Every quote form (hero card, quote dialog, contact page) emails requests to `QUOTE_EMAIL` in `build.py`.

1. **Web3Forms (primary):** sign in at [web3forms.com](https://web3forms.com), create an access key for `QUOTE_EMAIL`,
   paste it into `WEB3FORMS_ACCESS_KEY` in `build.py`, run `python build.py`, and push.
2. **FormSubmit (fallback):** used automatically if Web3Forms is not set up or fails. The first submission makes
   FormSubmit send an "Activate Form" email to `QUOTE_EMAIL`; click it once to start receiving requests.

If both fail, the visitor sees an error asking them to call (209) 576-0327, so nothing is silently lost.

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
