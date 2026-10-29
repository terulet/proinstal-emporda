# Proinstal Empordà web

- Repository: `https://github.com/terulet/proinstal-emporda`
- Canonical checkout: `/Volumes/Crucial X9/BOAB TECH/WEBS/PROINSTAL_EMPORDA` on Mac Server
- Hosting: GitHub Pages at `https://proinstalemporda.com/`
- Build: none; the site is static HTML, CSS and JavaScript
- Local preview on Mac Server: `ruby -run -e httpd . -p 8008`
- Preview from MacBoab while the local server is running: `http://100.98.237.124:8008`
- Git content: source HTML, CSS, JavaScript, sitemap, robots file and the existing image library
- Server-only content: none

## Measurement setup

Done on 2026-10-19 with the Google account borraseloi@gmail.com:

1. GA4: account and property «Proinstal Empordà» (Spain time zone, EUR, optional data sharing off), web stream `https://proinstalemporda.com`, measurement ID `G-LRQ46SCY62` in `assets/analytics-config.js`.
   `generate_lead` is a key event (no monetary value, counted once per session) and event data retention is 14 months.
2. Checked on the live site: before a choice and after «Rebutjar» no Google script loads; after «Acceptar» gtag loads with `G-LRQ46SCY62`.
3. Search Console: URL-prefix property `https://proinstalemporda.com/`, verified with the HTML file `google7174c917ed822f9c.html` at the root. Do not delete that file, or the property loses its verification.
4. `sitemap.xml` submitted to Search Console: accepted, 57 pages found.
5. Bing Webmaster Tools: signed in with Google, site imported from Search Console (only this site), with `sitemap.xml` imported.

6. GA4 is linked to the Search Console property, so search queries show up in Analytics.

IndexNow (Bing, Yandex and others): key file `68598d9a27efd07aea416b8d0d08ea5a.txt` at the root. All 57 sitemap URLs were submitted to `https://api.indexnow.org/indexnow` on 2026-10-19; it answered `202 Accepted`. After regenerating, committing and pushing, and once GitHub Pages serves the new pages, notify the changed pages:

    python3 _generador/indexnow.py            # pages changed in the last commit
    python3 _generador/indexnow.py <commit>   # pages changed since that commit
    python3 _generador/indexnow.py --totes    # every sitemap URL

It only sends URLs that are in `sitemap.xml`.

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

## Candidato de contacto francés · 29-10-2026

Base comprobada: cde2c543e377451f7c1c495fdefbc93ceea240bb, igual a origin y a los tres HTML públicos al iniciar.
Candidato aislado en PROINSTAL_CANDIDATAS/seo-datos-20261029, sin publicar.

Prioridad basada en los datos guardados de Search Console del 28/10: fontanería FR (2 clics/33 impresiones), climatización FR (2/30) y electricidad FR (0/28). Son agregados por página y una muestra pequeña; no prueban origen nacional, demanda total, contactos ni causas. La lectura API de 76 filas tiene otro desglose y periodo: no se mezclan cifras.

Cambios: instrucciones para pedir presupuesto, horario confirmado L-V de 8 a 17 y fin de semana cerrado, teléfono y enlace al formulario francés junto a WhatsApp. Se conserva el contenido de trabajos reales anterior. El formulario existente abre WhatsApp; no se ha conectado un nuevo receptor ni se acredita recepción automática en RADAR. No se cambian títulos, canonical, hreflang ni datos estructurados, que ya eran coherentes.

Regeneración acotada: python3 _generador/generar.py --fr-contact-only.
Dos regeneraciones idénticas; otras 58 páginas de servicio/zona y sitemap intactos.
QA independiente: tres páginas en 390 y 1280 px, enlaces y fragmento de formulario, sin errores JS ni desbordamiento. Consentimiento y contact_click probados con gtag simulado y peticiones externas bloqueadas; no confirma recepción real en GA4 ni contacto recibido. Evidencia externa al sitio publicado: ../qa-seo-datos-20261029/qa-results.json y capturas.
Preview privada: http://100.98.237.124:18771/; Analytics desactivado mediante respuesta del servidor de preview.
Publicación pendiente de autorización y comprobación posterior. Sin nuevas llamadas pagadas a OpenAI o búsquedas.
