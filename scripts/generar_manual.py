#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera el **manual del curso en PDF**: consolida las 176 clases en un único
documento, en orden, listo para leer de corrido, imprimir o estudiar offline.

  manual/MANUAL.pdf   render imprimible en B/N (vía Chrome/Edge headless)

El PDF **se versiona** (se sube al repo): así hay un enlace de descarga directo
desde el README y desde GitHub Pages, sin que nadie tenga que generarlo. Se
regenera con este script cuando el contenido cambia, y refleja el repo actual.

El manual respeta el orden global 001→176 agrupado en las 12 partes, con portada
e índice clicable. De cada clase se quita la navegación «⏮️ anterior / siguiente
⏭️» (en un libro se pasa página), se bajan los títulos para que encajen bajo el
título de su parte, y los enlaces relativos pasan a texto (en papel no llevan a
ningún sitio).

El código de los 10 lenguajes del núcleo va incluido: es el contenido del curso,
no un adorno. Los anexos `primos.md` quedan fuera por tamaño — se añaden con
`--con-primos` si quieres el volumen completo.

Uso:  python scripts/generar_manual.py                 # genera manual/MANUAL.pdf
      python scripts/generar_manual.py --con-primos    # incluye los 2722 primos
      python scripts/generar_manual.py --volcar-md R   # además escribe el MD en R (debug)
Requiere: pip install "markdown>=3.6" y Chrome o Edge (headless).
"""
from __future__ import annotations

import argparse
import glob
import os
import re
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLASSES = os.path.join(ROOT, "classes")
MANUAL_DIR = os.path.join(ROOT, "manual")
MANUAL_PDF = os.path.join(MANUAL_DIR, "MANUAL.pdf")

RE_H1 = re.compile(r"^#\s+(.+?)\s*$", re.M)

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


def partes() -> list[tuple[int, str, list[str]]]:
    """[(idx, dir_parte, [rutas de clase en orden])], ordenado por número de parte."""
    out = []
    for pdir in sorted(glob.glob(os.path.join(CLASSES, "parte-*")),
                       key=lambda p: int(re.search(r"parte-(\d+)", p).group(1))):
        idx = int(re.search(r"parte-(\d+)", pdir).group(1))
        clases = sorted(glob.glob(os.path.join(pdir, "[0-9][0-9][0-9]-*", "README.md")),
                        key=lambda r: int(os.path.basename(os.path.dirname(r))[:3]))
        if clases:
            out.append((idx, pdir, clases))
    return out


def construir_markdown(gm, con_primos: bool) -> str:
    lista = partes()
    total = sum(len(c) for _, _, c in lista)
    doc = [
        "# Manual completo — Polyglot Programming Labs",
        "",
        f"*{total} clases · {len(lista)} partes · un concepto, 10 lenguajes, ~40 familias*  ",
        "*github.com/vladimiracunadev-create/polyglot-programming-labs · Licencia MIT*",
        "",
        "[TOC]",
        "",
    ]
    for idx, pdir, clases in lista:
        with open(os.path.join(pdir, "README.md"), encoding="utf-8") as f:
            intro = f.read()
        m = RE_H1.search(intro)
        titulo = re.sub(r"^Parte\s+\d+\s*[—-]\s*", "", m.group(1)).strip() if m else pdir
        intro = RE_H1.sub("", intro, count=1)

        doc.append(f"## Parte {idx} — {titulo}")
        doc.append("")
        doc.append(gm.demotar(gm.quitar_nav(intro), 1).strip())  # H2 -> H3
        doc.append("")
        for ruta in clases:
            with open(ruta, encoding="utf-8") as f:
                cuerpo = gm.demotar(gm.quitar_nav(f.read()), 2).strip()  # H1 clase -> H3
            doc.append(cuerpo)
            doc.append("")
            primos = os.path.join(os.path.dirname(ruta), "primos.md")
            if con_primos and os.path.isfile(primos):
                with open(primos, encoding="utf-8") as f:
                    doc.append(gm.demotar(gm.quitar_nav(f.read()), 3).strip())
                doc.append("")
    return "\n".join(doc)


def main() -> int:
    ap = argparse.ArgumentParser(description="Genera el manual del curso en PDF.")
    ap.add_argument("--con-primos", action="store_true",
                    help="incluir los anexos primos.md (manual mucho más largo)")
    ap.add_argument("--volcar-md", metavar="RUTA",
                    help="además, escribe el Markdown intermedio ahí (para depurar)")
    args = ap.parse_args()

    try:
        import markdown
    except ImportError:
        print("Falta 'markdown'. Instálalo: pip install \"markdown>=3.6\"")
        return 1
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import generar_material as gm  # reutiliza el CSS B/N, la plantilla y buscar_navegador

    lista = partes()
    total = sum(len(c) for _, _, c in lista)
    print(f"== Manual: {len(lista)} partes, {total} clases"
          f"{' (con primos)' if args.con_primos else ''} ==")

    md = construir_markdown(gm, args.con_primos)
    if args.volcar_md:
        with open(args.volcar_md, "w", encoding="utf-8", newline="\n") as f:
            f.write(md)
        print(f"  MD volcado en {args.volcar_md} ({len(md) // 1024} KB)")

    # En papel los enlaces relativos no llevan a ningún sitio: a texto plano.
    # El índice ([TOC]) sí queda clicable, lo genera la extensión 'toc'.
    md = gm.LINK_REL.sub(r"\1", md)
    cuerpo = markdown.markdown(
        md, extensions=["tables", "fenced_code", "sane_lists", "toc"],
        extension_configs={"toc": {"toc_depth": "2-3"}})
    html = gm.PLANTILLA.format(title="Manual completo", css=gm.CSS_PRINT, body=cuerpo)

    navegador = gm.buscar_navegador()
    if navegador is None:
        print("No encontré Chrome ni Edge (hacen falta para el PDF).")
        return 1

    os.makedirs(MANUAL_DIR, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as tmp:
        tmp.write(html)
        ruta_tmp = tmp.name
    try:
        print("Generando el PDF (son cientos de páginas: puede tardar unos minutos)...")
        subprocess.run(
            [navegador, "--headless=new", "--disable-gpu", "--no-sandbox",
             "--no-pdf-header-footer", f"--print-to-pdf={MANUAL_PDF}",
             "file:///" + ruta_tmp.replace("\\", "/")],
            check=True, timeout=900,
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
        print(f"Chrome falló generando el PDF: {e}")
        return 1
    finally:
        os.unlink(ruta_tmp)

    print(f"  {os.path.relpath(MANUAL_PDF, ROOT)} ({os.path.getsize(MANUAL_PDF) // 1024} KB)")
    print("\nOK: manual generado. Recuerda commitearlo (se versiona).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
