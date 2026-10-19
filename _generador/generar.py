"""Genera les pàgines de servei i de zona (CA i ES), la portada en castellà,
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

UI = {
    "ca": {
        "inici": "Inici", "serveis": "Serveis", "zones": "Zones", "contactar": "Contactar",
        "home": "/", "altre": "es", "altre_nom": "Castellano", "locale": "ca_ES",
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
    },
    "es": {
        "inici": "Inicio", "serveis": "Servicios", "zones": "Zonas", "contactar": "Contactar",
        "home": "/es/", "altre": "ca", "altre_nom": "Català", "locale": "es_ES",
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
    serveis = "".join(f'<a href="/{s[lang]["slug"]}">{e(s[lang]["nom"])}</a>' for s in SERVEIS)
    pobles = "".join(f'<a href="/{p[lang]["slug"]}">{e(p["nom"])}</a>' for p in POBLES)
    priv = '<a href="/privacitat.html">' + u["privacitat"] + "</a>"
    return (f'<footer><div class="wrap fcols"><div><b>{u["serveis_peu"]}</b>{serveis}</div>'
            f'<div><b>{u["zones_peu"]}</b>{pobles}</div>'
            f'<div><b>Proinstal Empordà</b><a href="{u["home"]}">{u["inici"]}</a>'
            f'<a href="tel:+34671510146">671 510 146</a><a href="mailto:info@proinstalemporda.com">info@proinstalemporda.com</a>'
            f'<a href="https://www.instagram.com/proinstalemporda/">Instagram</a>{priv}</div></div>'
            f'<div class="wrap fnote">© {date.today().year} {e(u["empresa"])}</div></footer>')


def pagina(lang, d, comu, cos_extra, schema_principal, molla):
    """d: textos de la pàgina en aquest idioma; comu: dades comunes (hero, img, ca/es)."""
    u = UI[lang]
    altre = comu[u["altre"]]["slug"]
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
    hreflang = (f'<link rel="alternate" hreflang="ca" href="{url(comu["ca"]["slug"])}">'
                f'<link rel="alternate" hreflang="es" href="{url(comu["es"]["slug"])}">'
                f'<link rel="alternate" hreflang="x-default" href="{url(comu["ca"]["slug"])}">')
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
</head><body><header class="topbar"><div class="wrap"><a class="brand" href="{u["home"]}"><img src="/logo.jpg" alt="Proinstal Empordà">PROINSTAL <em>EMPORDÀ</em></a><nav class="nav"><a href="{u["home"]}#serveis">{u["serveis"]}</a><a href="{u["home"]}#zones">{u["zones"]}</a><a class="lang" href="/{altre}" hreflang="{u["altre"]}" lang="{u["altre"]}">{u["altre"].upper()}</a><a class="cta" href="{wa(d.get("wa", ""))}">{u["contactar"]}</a></nav></div></header>
<section class="hero" style="--hero:url('{comu["hero"]}')"><div class="wrap"><nav class="crumbs" aria-label="breadcrumb">{crumbs}</nav><div class="eyebrow">{e(d["eyebrow"])}</div><h1>{e(d["h1"])}</h1><p>{e(d["intro"])}</p><div class="actions"><a class="button" href="{wa(d.get("wa", ""))}">{u["wa_btn"]}</a><a class="button secondary" href="tel:+34671510146">{u["trucar"]}</a></div></div></section>
<main><section><div class="wrap split"><div><div class="eyebrow">{e(d["e2"])}</div><h2>{e(d["h2"])}</h2><p class="lead">{e(d["lead"])}</p><ul class="checklist">{llista}</ul></div><img src="{comu["img"]}" alt="{e(d["alt"])}" loading="lazy"></div></section>
<section class="areas"><div class="wrap"><h2>{e(d["h2b"])}</h2><div class="grid">{fitxes}</div></div></section>
<section class="faq"><div class="wrap"><div class="eyebrow">{u["faq_e"]}</div><h2>{u["faq"]}</h2>{faq_html}</div></section>
{cos_extra}</main>
<section class="contact"><div class="wrap"><h2>{e(d["cta_h"])}</h2><p>{e(d["cta_p"])}</p><a class="button" href="{wa(d.get("wa", ""))}">{u["wa_btn"]}</a></div></section>{peu(lang)}</body></html>
"""


def pagines_servei():
    for s in SERVEIS:
        for lang in ("ca", "es"):
            u, d = UI[lang], s[lang]
            pobles = [(p["nom"], p[lang]["slug"]) for p in POBLES]
            altres = [(o[lang]["nom"], o[lang]["slug"]) for o in SERVEIS if o is not s]
            extra = (f'<section class="areas"><div class="wrap"><h2>{u["on"]}</h2><p class="lead">{u["on_lead"]}</p>'
                     f'<div class="chips">{chips(pobles)}</div><h3 class="sub">{u["altres_serveis"]}</h3><div class="chips">{chips(altres)}</div></div></section>')
            principal = {"@type": "Service", "name": d["h1"], "serviceType": d["nom"], "provider": {"@id": NEGOCI["@id"]},
                         "areaServed": [{"@type": "City", "name": p["nom"]} for p in POBLES] + [{"@type": "AdministrativeArea", "name": "Alt Empordà"}, {"@type": "AdministrativeArea", "name": "Baix Empordà"}],
                         "url": url(d["slug"]), "inLanguage": lang}
            molla = [(u["inici"], None), (d["nom"], d["slug"])]
            yield d["slug"], pagina(lang, d, s, extra, principal, molla)


def pagines_poble():
    for p in POBLES + ZONES:
        for lang in ("ca", "es"):
            u = UI[lang]
            d = dict(p[lang])
            nom = d.get("nom", p["nom"])
            d.setdefault("h2b", u["feines"].format(nom=nom))
            d.setdefault("cta_h", u["cta_poble_h"].format(nom=nom))
            d.setdefault("cta_p", u["cta_poble_p"])
            d.setdefault("wa", u["wa_poble"].format(nom=nom))
            d.setdefault("nom", nom)
            serveis = [(s[lang]["nom"], s[lang]["slug"]) for s in SERVEIS]
            if "pobles" in p:
                fills = [(PER_ID[i]["nom"], PER_ID[i][lang]["slug"]) for i in p["pobles"]]
                bloc_pobles = f'<h3 class="sub">{u["pobles_zona"]}</h3><div class="chips">{chips(fills)}</div>'
                area = [{"@type": "City", "name": PER_ID[i]["nom"]} for i in p["pobles"]]
            else:
                altres = [(o["nom"], o[lang]["slug"]) for o in POBLES if o is not p]
                bloc_pobles = f'<h3 class="sub">{u["altres_pobles"]}</h3><div class="chips">{chips(altres)}</div>'
                area = {"@type": "City", "name": p["nom"]}
            extra = (f'<section class="areas"><div class="wrap"><h2>{u["serveis_a"].format(nom=nom)}</h2>'
                     f'<div class="chips">{chips(serveis)}</div>{bloc_pobles}</div></section>')
            principal = {"@type": "Service", "name": d["h1"], "serviceType": u["tipus_poble"], "provider": {"@id": NEGOCI["@id"]},
                         "areaServed": area, "url": url(d["slug"]), "inLanguage": lang}
            molla = [(u["inici"], None), (nom, d["slug"])]
            yield d["slug"], pagina(lang, d, p, extra, principal, molla)


# ---------- portada en castellà ----------

def mapa_ca_es():
    m = {}
    for it in SERVEIS + POBLES + ZONES:
        m["/" + it["ca"]["slug"]] = "/" + it["es"]["slug"]
    return m


def llegeix_diccionari(index, lang):
    ini = index.index(f"\n{lang}:{{")
    fi = index.index("},\n", ini)
    cos = index[ini + len(lang) + 3:fi]
    parells = re.findall(r'(\w+):("(?:[^"\\]|\\.)*"|\'(?:[^\'\\]|\\.)*\')', cos)
    return {k: v[1:-1].replace("\\'", "'").replace('\\"', '"') for k, v in parells}


def substitueix(text, vell, nou, cops=1):
    n = text.count(vell)
    if n < cops:
        sys.exit(f"No trobo a la portada: {vell!r}")
    return text.replace(vell, nou)


def bloc_enllacos(lang, text):
    """Omple els enllaços del peu de la portada entre <!--enllacos--> i <!--/enllacos-->."""
    u = UI[lang]
    serveis = "".join(f'<a href="/{s[lang]["slug"]}">{e(s[lang]["nom"])}</a>' for s in SERVEIS)
    zones = "".join(f'<a href="/{p[lang]["slug"]}">{e(p["nom"])}</a>' for p in POBLES)
    bloc = (f'<!--enllacos--><div class="wrap fx"><b>{u["serveis_peu"]}</b>{serveis}</div>'
            f'<div class="wrap fx"><b>{u["zones_peu"]}</b>{zones}</div><!--/enllacos-->')
    return re.sub(r"<!--enllacos-->.*?<!--/enllacos-->", lambda m: bloc, text, count=1, flags=re.S)


def portada_es():
    index = bloc_enllacos("ca", (ARREL / "index.html").read_text(encoding="utf8"))
    (ARREL / "index.html").write_text(index, encoding="utf8")
    t = llegeix_diccionari(index, "es")

    def tradueix(m):
        clau = m.group(3)
        return m.group(1) + t[clau] + m.group(5) if clau in t else m.group(0)

    cap, cos = index.split("<body>", 1)
    cos, script = cos.split("<script>\nvar I=", 1)
    cos = re.sub(r'(<(\w+)[^>]*\sdata-t="(\w+)"[^>]*>)(.*?)(</\2>)', tradueix, cos, flags=re.S)
    for ca, es in mapa_ca_es().items():
        cos = cos.replace(f'href="{ca}', f'href="{es}')
    for vell, nou in [
        ('placeholder="Nom"', 'placeholder="Nombre"'), ('placeholder="Telèfon"', 'placeholder="Teléfono"'),
        ('placeholder="Població / zona"', 'placeholder="Población / zona"'),
        ('placeholder="Explica breument què necessites..."', 'placeholder="Cuéntanos brevemente qué necesitas..."'),
        ('alt="Reforma de bany a l\'Empordà"', 'alt="Reforma de baño en el Empordà"'),
        ('alt="Abans"', 'alt="Antes"'), ('alt="Després"', 'alt="Después"'),
        ('<button class="lb" id="lBtn">🌐 CA ▾</button>', '<button class="lb" id="lBtn">🌐 ES ▾</button>'),
        ('<div class="lo ac" onclick="sL(\'ca\')">', '<div class="lo" onclick="location.href=\'/\'">'),
        ('<div class="lo" onclick="location.href=\'/es/\'">', '<div class="lo ac" onclick="sL(\'es\')">'),
        ('>📞 Trucar</a>', '>📞 Llamar</a>'), ('>Privacitat</a>', '>Privacidad</a>'), ('>Zones</a>', '>Zonas</a>'),
        ('<a href="/" class="lw">', '<a href="/es/" class="lw">'),
        (f'?text={t_wa_ca(index)}', f'?text={t["wa"]}'),
    ]:
        cos = substitueix(cos, vell, nou)
    script = substitueix(script, "var CL='ca';", "var CL='es';")
    cos = bloc_enllacos("es", cos)
    for vell, nou in [
        ('<html lang="ca">', '<html lang="es">'),
        ('content="Proinstal Empordà: reformes, instal·lacions, electricitat, fontaneria, plaques solars, climatització, fusteria i pèrgoles a l\'Empordà."',
         'content="Proinstal Empordà: reformas, instalaciones, electricidad, fontanería, placas solares, aire acondicionado, carpintería y pérgolas en el Alt y Baix Empordà. Presupuesto gratis."'),
        ("<title>Proinstal Empordà | Reformes i Instal·lacions</title>", "<title>Proinstal Empordà | Reformas e instalaciones en el Empordà</title>"),
        ('<link rel="canonical" href="https://proinstalemporda.com/"/>', '<link rel="canonical" href="https://proinstalemporda.com/es/"/>'),
        ('content="ca_ES"', 'content="es_ES"'),
        ('content="Proinstal Empordà | Reformes i Instal·lacions"', 'content="Proinstal Empordà | Reformas e instalaciones en el Empordà"'),
        ('content="Reformes, electricitat, fontaneria, climatització, plaques solars, fusteria i pèrgoles a l\'Alt i Baix Empordà."',
         'content="Reformas, electricidad, fontanería, climatización, placas solares, carpintería y pérgolas en el Alt y Baix Empordà."'),
        ('<meta property="og:url" content="https://proinstalemporda.com/"/>', '<meta property="og:url" content="https://proinstalemporda.com/es/"/>'),
        ('content="Un sol equip per a reformes i instal·lacions a l\'Empordà."', 'content="Un solo equipo para reformas e instalaciones en el Empordà."'),
    ]:
        cap = substitueix(cap, vell, nou)
    return cap + "<body>" + cos + "<script>\nvar I=" + script


def t_wa_ca(index):
    return llegeix_diccionari(index, "ca")["wa"]


# ---------- sitemap i llms.txt ----------

def sitemap(parells):
    files = []
    for ca, es in parells:
        alt = (f'<xhtml:link rel="alternate" hreflang="ca" href="{url(ca)}"/>'
               f'<xhtml:link rel="alternate" hreflang="es" href="{url(es)}"/>')
        for s in (ca, es):
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
    l += ["", "## Municipis / Municipios", ""]
    l += [f"- [{p['nom']}]({url(p['ca']['slug'])}) · [ES]({url(p['es']['slug'])}): {p['ca']['intro']}" for p in POBLES]
    l += ["", "## Zones / Zonas", ""]
    l += [f"- [{z['ca']['nom']}]({url(z['ca']['slug'])}) · [ES]({url(z['es']['slug'])})" for z in ZONES]
    l += ["", "## Optional", "", f"- [Portada en català]({DOMINI}/)", f"- [Portada en castellano]({DOMINI}/es/)", ""]
    return "\n".join(l)


def main():
    parells = [("", "es/")]
    for slug, contingut in list(pagines_servei()) + list(pagines_poble()):
        desti = ARREL / slug
        desti.parent.mkdir(parents=True, exist_ok=True)
        desti.write_text(contingut, encoding="utf8")
    for it in SERVEIS + POBLES + ZONES:
        parells.append((it["ca"]["slug"], it["es"]["slug"]))
    (ARREL / "es").mkdir(exist_ok=True)
    (ARREL / "es" / "index.html").write_text(portada_es(), encoding="utf8")
    (ARREL / "sitemap.xml").write_text(sitemap(parells), encoding="utf8")
    (ARREL / "llms.txt").write_text(llms(), encoding="utf8")
    print(f"{len(parells) * 2} pàgines al sitemap, {len(parells) - 1} parelles CA/ES generades")


if __name__ == "__main__":
    main()
