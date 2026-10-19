"""Genera les pàgines de servei i de zona (CA, ES i FR), les portades en castellà i francès,
el sitemap i llms.txt a partir de serveis.py i pobles.py.

    python3 _generador/generar.py

La carpeta comença per guió baix perquè GitHub Pages no la publiqui.
"""
import html
import importlib.util
import json
import re
import sys
from datetime import date
from pathlib import Path
from urllib.parse import quote

AQUI = Path(__file__).resolve().parent
ARREL = AQUI.parent
DOMINI = "https://proinstalemporda.com"
WA = "34671510146"
AVUI = date.today().isoformat()


def carrega(nom):
    spec = importlib.util.spec_from_file_location(nom, AQUI / f"{nom}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


SERVEIS = carrega("serveis").SERVEIS
_p = carrega("pobles")
POBLES, ZONES = _p.POBLES, _p.ZONES
PER_ID = {p["id"]: p for p in POBLES}
_i = carrega("imatges")
PARELLES, FOTOS, ALTS = _i.PARELLES, _i.FOTOS, _i.ALTS
_f = carrega("frances")
PEUS_FR = _f.PEUS_FR
LANGS = ("ca", "es", "fr")
for _it in SERVEIS + POBLES + ZONES:
    _it["hero"], _it["img"], _it["parelles"] = FOTOS[_it["id"]]
    for _n, _l in enumerate(("ca", "es")):
        if _it["id"] in ALTS:
            _it[_l]["alt"] = ALTS[_it["id"]][_n]
    if _it["id"] in _f.FR:
        _it["fr"] = _f.FR[_it["id"]]
TOTS = SERVEIS + POBLES + ZONES


def te(it, lang):
    return lang in it


def en(llista, lang):
    return [it for it in llista if lang in it]

UI = {
    "ca": {
        "inici": "Inici", "serveis": "Serveis", "zones": "Zones", "contactar": "Contactar",
        "home": "/", "locale": "ca_ES",
        "wa_btn": "💬 Demanar pressupost per WhatsApp", "trucar": "📞 Trucar",
        "faq": "Preguntes freqüents", "faq_e": "Dubtes habituals",
        "on": "On treballem", "on_lead": "Sortim de Vilajuïga i treballem a tot l’Alt Empordà i a bona part del Baix Empordà.",
        "altres_serveis": "Altres serveis", "serveis_a": "Serveis a {nom}", "altres_pobles": "Altres municipis",
        "pobles_zona": "Municipis d’aquesta zona", "feines": "Treballs habituals a {nom}",
        "cta_poble_h": "Tens una obra a {nom}?", "cta_poble_p": "Explica’ns què necessites i on és l’habitatge. Et respondrem per valorar una visita.",
        "wa_poble": "Hola Proinstal Empordà, tinc una consulta per a una obra a {nom}",
        "serveis_peu": "Serveis", "zones_peu": "Zones", "privacitat": "Privacitat",
        "empresa": "Proinstal Empordà · Carrer Roca de la Balena 4, 17493 Vilajuïga (Girona) · 671 510 146 · info@proinstalemporda.com",
        "tipus_poble": "Reformes i instal·lacions",
        "ad_e": "Feina feta", "ad_h": "Abans i després", "abans": "Abans", "despres": "Després",
    },
    "es": {
        "inici": "Inicio", "serveis": "Servicios", "zones": "Zonas", "contactar": "Contactar",
        "home": "/es/", "locale": "es_ES",
        "wa_btn": "💬 Pedir presupuesto por WhatsApp", "trucar": "📞 Llamar",
        "faq": "Preguntas frecuentes", "faq_e": "Dudas habituales",
        "on": "Dónde trabajamos", "on_lead": "Salimos de Vilajuïga y trabajamos en todo el Alt Empordà y en buena parte del Baix Empordà.",
        "altres_serveis": "Otros servicios", "serveis_a": "Servicios en {nom}", "altres_pobles": "Otros municipios",
        "pobles_zona": "Municipios de esta zona", "feines": "Trabajos habituales en {nom}",
        "cta_poble_h": "¿Tienes una obra en {nom}?", "cta_poble_p": "Cuéntanos qué necesitas y dónde está la vivienda. Te responderemos para valorar una visita.",
        "wa_poble": "Hola Proinstal Empordà, tengo una consulta para una obra en {nom}",
        "serveis_peu": "Servicios", "zones_peu": "Zonas", "privacitat": "Privacidad",
        "empresa": "Proinstal Empordà · Carrer Roca de la Balena 4, 17493 Vilajuïga (Girona) · 671 510 146 · info@proinstalemporda.com",
        "tipus_poble": "Reformas e instalaciones",
        "ad_e": "Trabajo hecho", "ad_h": "Antes y después", "abans": "Antes", "despres": "Después",
    },
    "fr": {
        "inici": "Accueil", "serveis": "Services", "zones": "Zones", "contactar": "Contact",
        "home": "/fr/", "locale": "fr_FR",
        "wa_btn": "💬 Demander un devis par WhatsApp", "trucar": "📞 Appeler",
        "faq": "Questions fréquentes", "faq_e": "Vos questions",
        "on": "Où nous intervenons", "on_lead": "Nous partons de Vilajuïga et intervenons dans tout l’Alt Empordà et une bonne partie du Baix Empordà : Roses, Empuriabrava, L’Escala, Cadaqués, Llançà, Figueres et Castelló d’Empúries.",
        "altres_serveis": "Autres services", "serveis_a": "Nos services à {nom}", "altres_pobles": "Autres communes",
        "pobles_zona": "Communes de cette zone", "feines": "Travaux fréquents à {nom}",
        "cta_poble_h": "Un projet à {nom} ?", "cta_poble_p": "Dites-nous ce dont vous avez besoin et où se trouve le logement. Nous vous répondons pour organiser une visite.",
        "wa_poble": "Bonjour Proinstal Empordà, j’ai un projet à {nom}",
        "serveis_peu": "Services", "zones_peu": "Communes", "privacitat": "Confidentialité",
        "empresa": "Proinstal Empordà · Carrer Roca de la Balena 4, 17493 Vilajuïga (Girona, Espagne) · +34 671 510 146 · info@proinstalemporda.com",
        "tipus_poble": "Rénovation et installations",
        "ad_e": "Travaux réalisés", "ad_h": "Avant et après", "abans": "Avant", "despres": "Après",
    },
}

NEGOCI = {
    "@type": ["GeneralContractor", "Electrician", "Plumber", "HVACBusiness"],
    "@id": f"{DOMINI}/#business",
    "name": "Proinstal Empordà",
    "url": f"{DOMINI}/",
    "telephone": "+34671510146",
    "email": "info@proinstalemporda.com",
    "address": {"@type": "PostalAddress", "streetAddress": "Carrer Roca de la Balena 4", "postalCode": "17493",
                "addressLocality": "Vilajuïga", "addressRegion": "Girona", "addressCountry": "ES"},
}

e = html.escape


def url(slug):
    return f"{DOMINI}/{slug}"


def wa(text):
    return f"https://wa.me/{WA}?text={quote(text)}"


def chips(enllacos):
    return "".join(f'<a href="/{s}">{e(n)}</a>' for n, s in enllacos)


def peu(lang):
    u = UI[lang]
    serveis = "".join(f'<a href="/{s[lang]["slug"]}">{e(s[lang]["nom"])}</a>' for s in en(SERVEIS, lang))
    pobles = "".join(f'<a href="/{p[lang]["slug"]}">{e(p["nom"])}</a>' for p in en(POBLES, lang))
    priv = '<a href="/privacitat.html">' + u["privacitat"] + "</a>"
    priv += "".join(f'<a href="{UI[l]["home"]}" hreflang="{l}">{l.upper()}</a>' for l in LANGS if l != lang)
    return (f'<footer><div class="wrap fcols"><div><b>{u["serveis_peu"]}</b>{serveis}</div>'
            f'<div><b>{u["zones_peu"]}</b>{pobles}</div>'
            f'<div><b>Proinstal Empordà</b><a href="{u["home"]}">{u["inici"]}</a>'
            f'<a href="tel:+34671510146">671 510 146</a><a href="mailto:info@proinstalemporda.com">info@proinstalemporda.com</a>'
            f'<a href="https://www.instagram.com/proinstalemporda/">Instagram</a>{priv}</div></div>'
            f'<div class="wrap fnote">© {date.today().year} {e(u["empresa"])}</div></footer>')


def abans_despres(lang, claus):
    if not claus:
        return ""
    u = UI[lang]
    fitxes = []
    for c in claus:
        a, b, ca, es = PARELLES[c]
        peu = {"ca": ca, "es": es, "fr": PEUS_FR[c]}[lang]
        fitxes.append(f'<figure class="ad"><div class="ad2"><div><img src="{a}" alt="{e(u["abans"] + ": " + peu)}" loading="lazy"><span>{u["abans"]}</span></div>'
                      f'<div><img src="{b}" alt="{e(u["despres"] + ": " + peu)}" loading="lazy"><span class="d">{u["despres"]}</span></div></div>'
                      f'<figcaption>{e(peu)}</figcaption></figure>')
    return (f'<section class="abdes"><div class="wrap"><div class="eyebrow">{u["ad_e"]}</div><h2>{u["ad_h"]}</h2>'
            f'<div class="adg">{"".join(fitxes)}</div></div></section>')


def pagina(lang, d, comu, cos_extra, schema_principal, molla):
    """d: textos de la pàgina en aquest idioma; comu: dades comunes (hero, img, ca/es)."""
    u = UI[lang]
    altres_idiomes = "".join(f'<a class="lang" href="/{comu[l]["slug"]}" hreflang="{l}" lang="{l}">{l.upper()}</a>'
                             for l in LANGS if l != lang and l in comu)
    canon = url(d["slug"])
    faq = d.get("faq", [])
    grafs = [NEGOCI, schema_principal,
             {"@type": "BreadcrumbList", "itemListElement": [
                 {"@type": "ListItem", "position": i + 1, "name": n, "item": url(s) if s else f"{DOMINI}{u['home']}"}
                 for i, (n, s) in enumerate(molla)]}]
    if faq:
        grafs.append({"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]})
    ld = json.dumps({"@context": "https://schema.org", "@graph": grafs}, ensure_ascii=False, separators=(",", ":"))
    hreflang = "".join(f'<link rel="alternate" hreflang="{l}" href="{url(comu[l]["slug"])}">' for l in LANGS if l in comu)
    hreflang += f'<link rel="alternate" hreflang="x-default" href="{url(comu["ca"]["slug"])}">'
    llista = "".join(f"<li>{e(x)}</li>" for x in d["llista"])
    fitxes = "".join(f'<article class="card"><h3>{e(h)}</h3><p>{e(p)}</p></article>' for h, p in d["fitxes"])
    faq_html = "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in faq)
    crumbs = " › ".join(
        (f'<a href="/{s}">{e(n)}</a>' if s else f'<a href="{u["home"]}">{e(n)}</a>') if i < len(molla) - 1 else f"<span>{e(n)}</span>"
        for i, (n, s) in enumerate(molla))
    return f"""<!doctype html><html lang="{lang}"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(d["title"])}</title>
<meta name="description" content="{e(d["desc"])}"><meta name="robots" content="index,follow,max-image-preview:large"><link rel="canonical" href="{canon}">
{hreflang}
<meta property="og:type" content="website"><meta property="og:locale" content="{u["locale"]}"><meta property="og:site_name" content="Proinstal Empordà"><meta property="og:title" content="{e(d["h1"])}"><meta property="og:description" content="{e(d["desc"])}"><meta property="og:url" content="{canon}"><meta property="og:image" content="{DOMINI}{comu["hero"]}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@700;800;900&family=Barlow:wght@400;500;600;700&display=swap" rel="stylesheet"><link rel="stylesheet" href="/assets/seo-pages.css"><script src="/assets/analytics-config.js"></script><script defer src="/assets/analytics.js"></script>
<script type="application/ld+json">{ld}</script>
</head><body><header class="topbar"><div class="wrap"><a class="brand" href="{u["home"]}"><img src="/logo.jpg" alt="Proinstal Empordà">PROINSTAL <em>EMPORDÀ</em></a><nav class="nav"><a href="{u["home"]}#serveis">{u["serveis"]}</a><a href="{u["home"]}#zones">{u["zones"]}</a>{altres_idiomes}<a class="cta" href="{wa(d.get("wa", ""))}">{u["contactar"]}</a></nav></div></header>
<section class="hero" style="--hero:url('{comu["hero"]}')"><div class="wrap"><nav class="crumbs" aria-label="breadcrumb">{crumbs}</nav><div class="eyebrow">{e(d["eyebrow"])}</div><h1>{e(d["h1"])}</h1><p>{e(d["intro"])}</p><div class="actions"><a class="button" href="{wa(d.get("wa", ""))}">{u["wa_btn"]}</a><a class="button secondary" href="tel:+34671510146">{u["trucar"]}</a></div></div></section>
<main><section><div class="wrap{" split" if comu["img"] else ""}"><div><div class="eyebrow">{e(d["e2"])}</div><h2>{e(d["h2"])}</h2><p class="lead">{e(d["lead"])}</p><ul class="checklist">{llista}</ul></div>{f'<img src="{comu["img"]}" alt="{e(d["alt"])}" loading="lazy">' if comu["img"] else ""}</div></section>
{abans_despres(lang, comu["parelles"])}
<section class="areas"><div class="wrap"><h2>{e(d["h2b"])}</h2><div class="grid">{fitxes}</div></div></section>
<section class="faq"><div class="wrap"><div class="eyebrow">{u["faq_e"]}</div><h2>{u["faq"]}</h2>{faq_html}</div></section>
{cos_extra}</main>
<section class="contact"><div class="wrap"><h2>{e(d["cta_h"])}</h2><p>{e(d["cta_p"])}</p><a class="button" href="{wa(d.get("wa", ""))}">{u["wa_btn"]}</a></div></section>{peu(lang)}</body></html>
"""


def pagines_servei():
    for s in SERVEIS:
        for lang in [l for l in LANGS if l in s]:
            u, d = UI[lang], s[lang]
            pobles = [(p["nom"], p[lang]["slug"]) for p in en(POBLES, lang)]
            altres = [(o[lang]["nom"], o[lang]["slug"]) for o in en(SERVEIS, lang) if o is not s]
            extra = (f'<section class="areas"><div class="wrap"><h2>{u["on"]}</h2><p class="lead">{u["on_lead"]}</p>'
                     f'<div class="chips">{chips(pobles)}</div><h3 class="sub">{u["altres_serveis"]}</h3><div class="chips">{chips(altres)}</div></div></section>')
            principal = {"@type": "Service", "name": d["h1"], "serviceType": d["nom"], "provider": {"@id": NEGOCI["@id"]},
                         "areaServed": [{"@type": "City", "name": p["nom"]} for p in POBLES] + [{"@type": "AdministrativeArea", "name": "Alt Empordà"}, {"@type": "AdministrativeArea", "name": "Baix Empordà"}],
                         "url": url(d["slug"]), "inLanguage": lang}
            molla = [(u["inici"], None), (d["nom"], d["slug"])]
            yield d["slug"], pagina(lang, d, s, extra, principal, molla)


def pagines_poble():
    for p in POBLES + ZONES:
        for lang in [l for l in LANGS if l in p]:
            u = UI[lang]
            d = dict(p[lang])
            nom = d.get("nom", p["nom"])
            d.setdefault("h2b", u["feines"].format(nom=nom))
            d.setdefault("cta_h", u["cta_poble_h"].format(nom=nom))
            d.setdefault("cta_p", u["cta_poble_p"])
            d.setdefault("wa", u["wa_poble"].format(nom=nom))
            d.setdefault("nom", nom)
            serveis = [(s[lang]["nom"], s[lang]["slug"]) for s in en(SERVEIS, lang)]
            if "pobles" in p:
                fills = [(PER_ID[i]["nom"], PER_ID[i][lang]["slug"]) for i in p["pobles"]]
                bloc_pobles = f'<h3 class="sub">{u["pobles_zona"]}</h3><div class="chips">{chips(fills)}</div>'
                area = [{"@type": "City", "name": PER_ID[i]["nom"]} for i in p["pobles"]]
            else:
                altres = [(o["nom"], o[lang]["slug"]) for o in en(POBLES, lang) if o is not p]
                bloc_pobles = f'<h3 class="sub">{u["altres_pobles"]}</h3><div class="chips">{chips(altres)}</div>'
                area = {"@type": "City", "name": p["nom"]}
            extra = (f'<section class="areas"><div class="wrap"><h2>{u["serveis_a"].format(nom=nom)}</h2>'
                     f'<div class="chips">{chips(serveis)}</div>{bloc_pobles}</div></section>')
            principal = {"@type": "Service", "name": d["h1"], "serviceType": u["tipus_poble"], "provider": {"@id": NEGOCI["@id"]},
                         "areaServed": area, "url": url(d["slug"]), "inLanguage": lang}
            molla = [(u["inici"], None), (nom, d["slug"])]
            yield d["slug"], pagina(lang, d, p, extra, principal, molla)


# ---------- portades en castellà i francès ----------

PORTADA = {
    "es": {
        "cos": [
            ('placeholder="Nom"', 'placeholder="Nombre"'), ('placeholder="Telèfon"', 'placeholder="Teléfono"'),
            ('placeholder="Població / zona"', 'placeholder="Población / zona"'),
            ('placeholder="Explica breument què necessites..."', 'placeholder="Cuéntanos brevemente qué necesitas..."'),
            ('alt="Reforma de bany a l\'Empordà"', 'alt="Reforma de baño en el Empordà"'),
            ('alt="Abans"', 'alt="Antes"'), ('alt="Després"', 'alt="Después"'),
            ('>📞 Trucar</a>', '>📞 Llamar</a>'), ('>Privacitat</a>', '>Privacidad</a>'), ('>Zones</a>', '>Zonas</a>'),
        ],
        "title": "Proinstal Empordà | Reformas e instalaciones en el Empordà",
        "desc": "Proinstal Empordà: reformas, instalaciones, electricidad, fontanería, placas solares, aire acondicionado, carpintería y pérgolas en el Alt y Baix Empordà. Presupuesto gratis.",
        "og_desc": "Reformas, electricidad, fontanería, climatización, placas solares, carpintería y pérgolas en el Alt y Baix Empordà.",
        "tw": "Un solo equipo para reformas e instalaciones en el Empordà.",
    },
    "fr": {
        "cos": [
            ('placeholder="Telèfon"', 'placeholder="Téléphone"'),
            ('placeholder="Població / zona"', 'placeholder="Commune / zone"'),
            ('placeholder="Explica breument què necessites..."', 'placeholder="Décrivez brièvement votre besoin..."'),
            ('alt="Reforma de bany a l\'Empordà"', 'alt="Rénovation de salle de bain dans l’Empordà"'),
            ('alt="Abans"', 'alt="Avant"'), ('alt="Després"', 'alt="Après"'),
            ('>📞 Trucar</a>', '>📞 Appeler</a>'), ('>Privacitat</a>', '>Confidentialité</a>'),
        ],
        "title": "Proinstal Empordà | Rénovation et installations sur la Costa Brava (Espagne)",
        "desc": "Entreprise de rénovation et d’installations dans l’Empordà, Costa Brava (Espagne) : plomberie, électricité, climatisation, panneaux solaires, menuiserie et pergolas à Roses, Empuriabrava et L’Escala. On parle français.",
        "og_desc": "Rénovation, plomberie, électricité, climatisation, panneaux solaires et pergolas sur la Costa Brava. On parle français.",
        "tw": "Une seule équipe pour vos travaux sur la Costa Brava.",
    },
}


def llegeix_diccionari(index, lang):
    ini = index.index(f"\n{lang}:{{")
    fi = index.index("},\n", ini)
    cos = index[ini + len(lang) + 3:fi]
    parells = re.findall(r'(\w+):("(?:[^"\\]|\\.)*"|\'(?:[^\'\\]|\\.)*\')', cos)
    return {k: v[1:-1].replace("\\'", "'").replace('\\"', '"') for k, v in parells}


def substitueix(text, vell, nou):
    if vell not in text:
        sys.exit(f"No trobo a la portada: {vell!r}")
    return text.replace(vell, nou)


def bloc_enllacos(lang, text):
    """Omple els enllaços del peu de la portada entre <!--enllacos--> i <!--/enllacos-->."""
    u = UI[lang]
    serveis = "".join(f'<a href="/{s[lang]["slug"]}">{e(s[lang]["nom"])}</a>' for s in en(SERVEIS, lang))
    zones = "".join(f'<a href="/{p[lang]["slug"]}">{e(p["nom"])}</a>' for p in en(POBLES, lang))
    bloc = (f'<!--enllacos--><div class="wrap fx"><b>{u["serveis_peu"]}</b>{serveis}</div>'
            f'<div class="wrap fx"><b>{u["zones_peu"]}</b>{zones}</div><!--/enllacos-->')
    return re.sub(r"<!--enllacos-->.*?<!--/enllacos-->", lambda m: bloc, text, count=1, flags=re.S)


def portada_catala():
    index = bloc_enllacos("ca", (ARREL / "index.html").read_text(encoding="utf8"))
    (ARREL / "index.html").write_text(index, encoding="utf8")
    return index


def portada(lang, index):
    t = llegeix_diccionari(index, lang)
    txt = PORTADA[lang]

    def tradueix(m):
        clau = m.group(3)
        return m.group(1) + t[clau] + m.group(5) if clau in t else m.group(0)

    cap, cos = index.split("<body>", 1)
    cos, script = cos.split("<script>\nvar I=", 1)
    cos = re.sub(r'(<(\w+)[^>]*\sdata-t="(\w+)"[^>]*>)(.*?)(</\2>)', tradueix, cos, flags=re.S)
    for it in en(TOTS, lang):
        cos = cos.replace(f'href="/{it["ca"]["slug"]}', f'href="/{it[lang]["slug"]}')
    for vell, nou in txt["cos"] + [
        ('<button class="lb" id="lBtn">🌐 CA ▾</button>', f'<button class="lb" id="lBtn">🌐 {lang.upper()} ▾</button>'),
        ('<div class="lo ac" onclick="sL(\'ca\')">', '<div class="lo" onclick="location.href=\'/\'">'),
        (f'<div class="lo" onclick="location.href=\'/{lang}/\'">', f'<div class="lo ac" onclick="sL(\'{lang}\')">'),
        ('<a href="/" class="lw">', f'<a href="/{lang}/" class="lw">'),
        (f'?text={llegeix_diccionari(index, "ca")["wa"]}', f'?text={t["wa"]}'),
    ]:
        cos = substitueix(cos, vell, nou)
    script = substitueix(script, "var CL='ca';", f"var CL='{lang}';")
    cos = bloc_enllacos(lang, cos)
    for vell, nou in [
        ('<html lang="ca">', f'<html lang="{lang}">'),
        ('content="Proinstal Empordà: reformes, instal·lacions, electricitat, fontaneria, plaques solars, climatització, fusteria i pèrgoles a l\'Empordà."', f'content="{e(txt["desc"])}"'),
        ("<title>Proinstal Empordà | Reformes i Instal·lacions</title>", f"<title>{e(txt['title'])}</title>"),
        ('<link rel="canonical" href="https://proinstalemporda.com/"/>', f'<link rel="canonical" href="https://proinstalemporda.com/{lang}/"/>'),
        ('content="ca_ES"', f'content="{UI[lang]["locale"]}"'),
        ('content="Proinstal Empordà | Reformes i Instal·lacions"', f'content="{e(txt["title"])}"'),
        ('content="Reformes, electricitat, fontaneria, climatització, plaques solars, fusteria i pèrgoles a l\'Alt i Baix Empordà."', f'content="{e(txt["og_desc"])}"'),
        ('<meta property="og:url" content="https://proinstalemporda.com/"/>', f'<meta property="og:url" content="https://proinstalemporda.com/{lang}/"/>'),
        ('content="Un sol equip per a reformes i instal·lacions a l\'Empordà."', f'content="{e(txt["tw"])}"'),
    ]:
        cap = substitueix(cap, vell, nou)
    return cap + "<body>" + cos + "<script>\nvar I=" + script


# ---------- sitemap i llms.txt ----------

def grups():
    g = [{"ca": "", "es": "es/", "fr": "fr/"}]
    g += [{l: it[l]["slug"] for l in LANGS if l in it} for it in TOTS]
    return g


def sitemap():
    files = []
    for grup in grups():
        alt = "".join(f'<xhtml:link rel="alternate" hreflang="{l}" href="{url(s)}"/>' for l, s in grup.items())
        for s in grup.values():
            files.append(f"  <url><loc>{url(s)}</loc><lastmod>{AVUI}</lastmod>{alt}</url>")
    files.append(f"  <url><loc>{url('privacitat.html')}</loc><lastmod>{AVUI}</lastmod></url>")
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
            + "\n".join(files) + "\n</urlset>\n")


def llms():
    l = ["# Proinstal Empordà", "",
         "> Empresa de reformes i instal·lacions de Vilajuïga (Alt Empordà, Girona). Un sol equip fa reformes integrals, "
         "lampisteria i fontaneria, electricitat, aire condicionat, aerotèrmia, plaques solars, fusteria, pèrgoles, "
         "reparació d’humitats i manteniment de segones residències a l’Alt i Baix Empordà. "
         "Atén en català, castellà, francès, anglès i alemany.", "",
         "- Adreça: Carrer Roca de la Balena 4, 17493 Vilajuïga (Girona)",
         "- Telèfons: +34 671 510 146 · +34 635 014 684 (també WhatsApp al 671 510 146)",
         "- Correu: info@proinstalemporda.com",
         "- Instagram: https://www.instagram.com/proinstalemporda/",
         "- Pressupost i visita sense cost.", "",
         "## Serveis (català)", ""]
    l += [f"- [{s['ca']['h1']}]({url(s['ca']['slug'])}): {s['ca']['intro']}" for s in SERVEIS]
    l += ["", "## Servicios (castellano)", ""]
    l += [f"- [{s['es']['h1']}]({url(s['es']['slug'])}): {s['es']['intro']}" for s in SERVEIS]
    l += ["", "## Services (français)", ""]
    l += [f"- [{it['fr']['h1']}]({url(it['fr']['slug'])}): {it['fr']['intro']}" for it in en(TOTS, "fr")]
    l += ["", "## Municipis / Municipios", ""]
    l += [f"- [{p['nom']}]({url(p['ca']['slug'])}) · [ES]({url(p['es']['slug'])}): {p['ca']['intro']}" for p in POBLES]
    l += ["", "## Zones / Zonas", ""]
    l += [f"- [{z['ca']['nom']}]({url(z['ca']['slug'])}) · [ES]({url(z['es']['slug'])})" for z in ZONES]
    l += ["", "## Optional", "", f"- [Portada en català]({DOMINI}/)", f"- [Portada en castellano]({DOMINI}/es/)",
          f"- [Accueil en français]({DOMINI}/fr/)", ""]
    return "\n".join(l)


def main():
    n = 0
    for slug, contingut in list(pagines_servei()) + list(pagines_poble()):
        desti = ARREL / slug
        desti.parent.mkdir(parents=True, exist_ok=True)
        desti.write_text(contingut, encoding="utf8")
        n += 1
    index = portada_catala()
    for lang in ("es", "fr"):
        (ARREL / lang).mkdir(exist_ok=True)
        (ARREL / lang / "index.html").write_text(portada(lang, index), encoding="utf8")
    (ARREL / "sitemap.xml").write_text(sitemap(), encoding="utf8")
    (ARREL / "llms.txt").write_text(llms(), encoding="utf8")
    print(f"{n} pàgines de servei i zona, 3 portades, {sum(len(g) for g in grups()) + 1} URL al sitemap")


if __name__ == "__main__":
    main()
