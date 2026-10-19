# Proinstal Empordà web

- Repository: `https://github.com/terulet/proinstal-emporda`
- Canonical checkout: `/Volumes/Crucial X9/Projects/proinstal-emporda` on Mac Server
- Hosting: GitHub Pages at `https://proinstalemporda.com/`
- Build: none; the site is static HTML, CSS and JavaScript
- Local preview on Mac Server: `ruby -run -e httpd . -p 8008`
- Preview from MacBoab while the local server is running: `http://100.98.237.124:8008`
- Git content: source HTML, CSS, JavaScript, sitemap, robots file and the existing image library
- Server-only content: none

## Measurement setup

1. Create the GA4 web stream for `https://proinstalemporda.com/`.
2. Put its `G-...` measurement ID in `assets/analytics-config.js`.
3. Verify that analytics does not load until consent is accepted.
4. Create a Search Console Domain property for `proinstalemporda.com` and verify it by DNS.
5. Submit `https://proinstalemporda.com/sitemap.xml`.

Events prepared: `generate_lead` for WhatsApp, phone and email; `outbound_click` for Instagram; `language_change` for the homepage selector. Personal form fields are not sent to GA4.

## Generated pages

Service, town and zone pages (CA, ES and FR), `es/index.html`, `fr/index.html`, `sitemap.xml` and `llms.txt` are generated:

    python3 _generador/generar.py

- Texts live in `_generador/serveis.py` and `_generador/pobles.py`. Edit them there, not in the HTML.
- French pages live in `_generador/frances.py`; only the services and towns with real French searches have one.
- Photos and before/after pairs live in `_generador/imatges.py`.
- `es/index.html` and `fr/index.html` are built from `index.html` with the `es` and `fr` strings of its translation dictionary. Edit the Catalan homepage, then regenerate.
- The footer links of the homepage are filled between `<!--enllacos-->` markers.
- `_generador/` is not published: GitHub Pages skips folders starting with `_`.
