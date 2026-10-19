"""Avisa IndexNow (Bing, Yandex, Seznam…) de les pàgines que han canviat.

    python3 _generador/indexnow.py            # pàgines canviades a l'últim commit
    python3 _generador/indexnow.py 20d3b44    # pàgines canviades des d'aquest commit
    python3 _generador/indexnow.py --totes    # totes les URL del sitemap

Executa-ho després del git push, quan GitHub Pages ja serveixi les pàgines noves.
Només s'envien URL que són al sitemap.xml.
"""
import json
import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

ARREL = Path(__file__).resolve().parent.parent
DOMINI = "https://proinstalemporda.com"
CLAU = "68598d9a27efd07aea416b8d0d08ea5a"
API = "https://api.indexnow.org/indexnow"


def urls_sitemap():
    return re.findall(r"<loc>(.*?)</loc>", (ARREL / "sitemap.xml").read_text(encoding="utf8"))


def url_de(fitxer):
    if fitxer == "index.html":
        return DOMINI + "/"
    if fitxer.endswith("/index.html"):
        return f"{DOMINI}/{fitxer[:-len('index.html')]}"
    return f"{DOMINI}/{fitxer}"


def urls_canviades(des_de):
    sortida = subprocess.run(["git", "diff", "--name-only", des_de, "HEAD", "--", "*.html"],
                             cwd=ARREL, capture_output=True, text=True, check=True).stdout
    return [url_de(f) for f in sortida.split()]


def envia(urls):
    cos = {"host": DOMINI.removeprefix("https://"), "key": CLAU,
           "keyLocation": f"{DOMINI}/{CLAU}.txt", "urlList": urls}
    peticio = urllib.request.Request(API, data=json.dumps(cos).encode(), method="POST",
                                     headers={"Content-Type": "application/json; charset=utf-8"})
    try:
        with urllib.request.urlopen(peticio, timeout=30) as resposta:
            return resposta.status
    except urllib.error.HTTPError as error:
        return error.code


def main():
    arg = sys.argv[1] if len(sys.argv) > 1 else "HEAD~1"
    al_sitemap = urls_sitemap()
    if arg == "--totes":
        urls = al_sitemap
    else:
        urls = [u for u in urls_canviades(arg) if u in set(al_sitemap)]
    if not urls:
        print("Cap pàgina del sitemap ha canviat: no s'envia res.")
        return
    estat = envia(urls)
    print(f"{len(urls)} URL enviades a IndexNow: HTTP {estat}")
    for u in urls:
        print("  " + u)
    if estat not in (200, 202):
        sys.exit(1)


if __name__ == "__main__":
    main()
