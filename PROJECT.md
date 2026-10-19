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

Done on 2026-10-19 with the Google account borraseloi@gmail.com:

1. GA4: account and property «Proinstal Empordà» (Spain time zone, EUR, optional data sharing off), web stream `https://proinstalemporda.com`, measurement ID `G-LRQ46SCY62` in `assets/analytics-config.js`.
2. Checked on the live site: before a choice and after «Rebutjar» no Google script loads; after «Acceptar» gtag loads with `G-LRQ46SCY62`.
3. Search Console: URL-prefix property `https://proinstalemporda.com/`, verified with the HTML file `google7174c917ed822f9c.html` at the root. Do not delete that file, or the property loses its verification.
4. `sitemap.xml` submitted to Search Console: accepted, 57 pages found.
5. Bing Webmaster Tools: signed in with Google, site imported from Search Console (only this site), with `sitemap.xml` imported.

IndexNow (Bing, Yandex and others): key file `68598d9a27efd07aea416b8d0d08ea5a.txt` at the root. All 57 sitemap URLs were submitted to `https://api.indexnow.org/indexnow` on 2026-10-19; it answered `202 Accepted`. Resubmit changed URLs with the same key after each regeneration.

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
