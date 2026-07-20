#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera guías **PDF imprimibles en blanco y negro** a partir de los README de clase.

Los PDF NO se versionan (pesan mucho y el sitio web ya cubre la lectura online):
se generan bajo demanda en `material/`, que está en .gitignore.

Cada guía incluye la clase con **el código a la vista de los 10 lenguajes del
núcleo**, que es lo que hace útil imprimirla: se compara en papel sin saltar
entre archivos.

Uso:
  python scripts/generar_material.py --parte 3      # solo la parte 3
  python scripts/generar_material.py --parte 3 4 5  # varias partes
  python scripts/generar_material.py --all          # las 176 clases (~8 min)
  python scripts/generar_material.py --parte 3 --con-primos   # añade primos.md
  python scripts/generar_material.py --parte 3 --solo-html    # sin PDF (rápido)

Requiere: pip install "markdown>=3.6" y Chrome o Edge instalado (headless).
"""
from __future__ import annotations

import argparse
import glob
import os
import re
import shutil
import subprocess
import sys
import tempfile

import markdown

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLASSES = os.path.join(ROOT, "classes")
OUT = os.path.join(ROOT, "material")

REPO = "github.com/vladimiracunadev-create/polyglot-programming-labs"
PROGRAMA = "Polyglot Programming Labs"

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

NAVEGADORES = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    "/usr/bin/google-chrome",
    "/usr/bin/chromium",
    "/usr/bin/chromium-browser",
]

# CSS de impresión: cero color, denso pero legible, sin cortar bloques de código.
# En este curso el código es el contenido, así que se protege más que en otros:
# un bloque partido entre páginas arruina la comparación entre lenguajes.
CSS_PRINT = """
@page { size: A4; margin: 16mm 14mm 16mm 14mm; }
* { box-sizing: border-box; }
body { font-family: Georgia, 'Times New Roman', serif; font-size: 10.5pt; line-height: 1.45;
       color: #000; background: #fff; margin: 0; }
h1 { font-size: 17pt; margin: 0 0 .2em; border-bottom: 2px solid #000; padding-bottom: .2em; }
h2 { font-size: 13pt; margin: 1.1em 0 .35em; border-bottom: 1px solid #999; padding-bottom: .12em;
     page-break-after: avoid; }
h3 { font-size: 11.5pt; margin: .8em 0 .3em; page-break-after: avoid; }
h4 { font-size: 10.5pt; margin: .7em 0 .25em; page-break-after: avoid; }
p, li { orphans: 3; widows: 3; }
ul, ol { margin: .35em 0 .35em 1.1em; padding-left: .8em; }
li { margin: .12em 0; }
blockquote { border-left: 3px solid #666; margin: .6em 0; padding: .1em .8em; font-style: italic; }
code { font-family: 'Consolas', 'DejaVu Sans Mono', monospace; font-size: 9pt;
       background: #f0f0f0; padding: .05em .25em; border-radius: 2px; }
pre { font-family: 'Consolas', 'DejaVu Sans Mono', monospace; font-size: 8.6pt; line-height: 1.35;
      background: #f4f4f4; border: 1px solid #bbb; border-radius: 3px; padding: .5em .6em;
      overflow: visible; white-space: pre-wrap; word-wrap: break-word;
      page-break-inside: avoid; }  /* no partir el código entre páginas */
pre code { background: none; padding: 0; font-size: inherit; }
table { border-collapse: collapse; width: 100%; margin: .5em 0; font-size: 9.4pt;
        page-break-inside: avoid; }
th, td { border: 1px solid #666; padding: .28em .45em; text-align: left; vertical-align: top; }
th { background: #e8e8e8; font-weight: bold; }
a { color: #000; text-decoration: none; }
a[href^="http"]::after { content: " (" attr(href) ")"; font-size: 7.5pt; color: #555;
                         word-break: break-all; }
img { max-width: 100%; filter: grayscale(100%); }
hr { border: 0; border-top: 1px solid #999; margin: 1em 0; }
.pie { margin-top: 1.4em; padding-top: .5em; border-top: 1px solid #999;
       font-size: 8pt; color: #444; text-align: center; }
"""

PLANTILLA = """<!doctype html>
<html lang="es"><head><meta charset="utf-8"><title>{title}</title>
<style>{css}</style></head><body>
{body}
<div class="pie">""" + PROGRAMA + """ · {title}<br>
""" + REPO + """ · Licencia MIT</div>
</body></html>
"""

# Los enlaces relativos no sirven en papel: se quedan como texto.
LINK_REL = re.compile(r"\[([^\]]+)\]\((?!https?://)[^)]+\)")

# Pie de navegación entre clases: «> [⏮️ Clase 040] · … · [Clase 042 ⏭️]».
RE_NAV = re.compile(r"^\s*>\s*\[⏮️[^\n]*\n?", re.M)
RE_NAV_CAB = re.compile(r"^\s*>\s*\[⬅️[^\n]*\n?", re.M)
RE_H1 = re.compile(r"^#\s+(.+?)\s*$", re.M)
RE_FENCE = re.compile(r"^(\s*)(```|~~~)")


def buscar_navegador() -> str | None:
    for c in NAVEGADORES:
        if os.path.isfile(c):
            return c
    return shutil.which("chrome") or shutil.which("chromium") or shutil.which("msedge")


def quitar_nav(texto: str) -> str:
    """En papel no hay «siguiente»: se pasa la página."""
    texto = RE_NAV.sub("", texto)
    texto = RE_NAV_CAB.sub("", texto)
    # El separador que quedaba justo antes del pie ya no separa nada.
    return re.sub(r"\n---\s*\n\s*$", "\n", texto)


def demotar(texto: str, niveles: int) -> str:
    """Baja `niveles` cada título, sin tocar los '#' de dentro del código."""
    salida, en_fence, marca = [], False, ""
    for linea in texto.splitlines():
        f = RE_FENCE.match(linea)
        if f:
            if not en_fence:
                en_fence, marca = True, f.group(2)
            elif f.group(2) == marca:
                en_fence = False
            salida.append(linea)
        elif not en_fence and linea.startswith("#"):
            salida.append("#" * niveles + linea)
        else:
            salida.append(linea)
    return "\n".join(salida)


def clases(partes: list[int] | None) -> list[tuple[int, str, str]]:
    """[(num, ruta_readme, slug_parte)] filtradas por parte."""
    out = []
    for pdir in sorted(glob.glob(os.path.join(CLASSES, "parte-*"))):
        pslug = os.path.basename(pdir)
        pidx = int(re.search(r"parte-(\d+)", pslug).group(1))
        if partes is not None and pidx not in partes:
            continue
        for cdir in sorted(glob.glob(os.path.join(pdir, "*"))):
            base = os.path.basename(cdir)
            rm = os.path.join(cdir, "README.md")
            if os.path.isdir(cdir) and re.match(r"^\d{3}-", base) and os.path.isfile(rm):
                out.append((int(base[:3]), rm, pslug))
    return sorted(out)


def a_html(ruta_readme: str, con_primos: bool) -> tuple[str, str]:
    with open(ruta_readme, encoding="utf-8") as f:
        md_texto = f.read()

    m = RE_H1.search(md_texto)
    title = re.sub(r"[#*`]", "", m.group(1)).strip() if m else "Clase"
    md_texto = quitar_nav(md_texto)

    # El anexo de primos es opcional: multiplica por tres el tamaño de la guía.
    primos = os.path.join(os.path.dirname(ruta_readme), "primos.md")
    if con_primos and os.path.isfile(primos):
        with open(primos, encoding="utf-8") as f:
            anexo = quitar_nav(f.read())
        # El H1 del anexo pasa a H2 para colgar de la clase.
        md_texto += "\n\n---\n\n" + demotar(anexo, 1)

    md_texto = LINK_REL.sub(r"\1", md_texto)
    cuerpo = markdown.markdown(md_texto, extensions=["tables", "fenced_code", "sane_lists"])
    return title, PLANTILLA.format(title=title, css=CSS_PRINT, body=cuerpo)


def main() -> int:
    ap = argparse.ArgumentParser(description="Genera guías PDF imprimibles (B/N) por clase.")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--parte", nargs="+", type=int, help="números de parte (0-11)")
    g.add_argument("--all", action="store_true", help="todas las clases")
    ap.add_argument("--con-primos", action="store_true",
                    help="incluir primos.md como anexo (guías mucho más largas)")
    ap.add_argument("--solo-html", action="store_true",
                    help="no generar PDF (rápido, para revisar)")
    args = ap.parse_args()

    lista = clases(None if args.all else args.parte)
    if not lista:
        print("No hay clases para esos filtros.")
        return 1

    navegador = None
    if not args.solo_html:
        navegador = buscar_navegador()
        if navegador is None:
            print("ERROR: no se encontró Chrome ni Edge. Usa --solo-html o instala un navegador.")
            return 1

    os.makedirs(OUT, exist_ok=True)
    hechos = 0
    for num, rm, pslug in lista:
        title, html = a_html(rm, args.con_primos)
        destino = os.path.join(OUT, pslug)
        os.makedirs(destino, exist_ok=True)
        base = f"clase-{num:03d}"

        if args.solo_html:
            with open(os.path.join(destino, base + ".html"), "w", encoding="utf-8") as f:
                f.write(html)
            hechos += 1
            continue

        with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as tmp:
            tmp.write(html)
            ruta_tmp = tmp.name
        pdf = os.path.join(destino, base + ".pdf")
        try:
            subprocess.run(
                [navegador, "--headless=new", "--disable-gpu", "--no-sandbox",
                 "--no-pdf-header-footer", f"--print-to-pdf={pdf}",
                 "file:///" + ruta_tmp.replace("\\", "/")],
                check=True, timeout=120,
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            hechos += 1
            print(f"  [{hechos}/{len(lista)}] {os.path.relpath(pdf, ROOT)}")
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
            print(f"  ERROR en la clase {num:03d}: {e}")
        finally:
            os.unlink(ruta_tmp)

    tipo = "HTML" if args.solo_html else "PDF"
    print(f"\n{hechos}/{len(lista)} guías {tipo} generadas en material/")
    print("Nota: material/ está en .gitignore (los PDF no se versionan).")
    return 0 if hechos == len(lista) else 1


if __name__ == "__main__":
    raise SystemExit(main())
