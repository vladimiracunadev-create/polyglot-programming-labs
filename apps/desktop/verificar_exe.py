#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifica que el ejecutable lleva el curso DENTRO — no que compiló.

Un binario de PyInstaller que se generó sin `--add-data "site;site"` pesa poco,
arranca igual y muestra una ventana perfectamente funcional... sin una sola
clase. Todas las señales de build quedan en verde. La única prueba real es abrir
el binario y contar lo que hay dentro, que es lo que hace este script.

Lee el índice (TOC) del archivo CArchive que PyInstaller pega al final del
ejecutable y enumera los recursos empaquetados. No descomprime nada: los nombres
viven en el TOC en claro, así que basta con recorrerlo.

Uso:
    python apps/desktop/verificar_exe.py dist/PolyglotProgrammingLabs.exe
    python apps/desktop/verificar_exe.py <exe> --clases 176 --primos 136 \
        --vivos 136 --fichas 60

Salida 0 si el recuento cuadra; 1 si falta contenido (para usarlo como gate).
"""
from __future__ import annotations

import argparse
import os
import re
import struct
import sys

try:  # la consola de Windows llega en cp1252 y no traga los emoji del informe
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

# Cookie que PyInstaller escribe al final del ejecutable (bootloader v5+).
MAGIC = b"MEI\014\013\012\013\016"
COOKIE = struct.Struct("!8sIIII64s")   # magic, len, pos_toc, len_toc, pyvers, pylib
ENTRADA = struct.Struct("!IIIIBB")     # structlen, pos, len, ulen, cflag, typcd


def leer_toc(ruta: str) -> list[str]:
    """Devuelve los nombres de los recursos empaquetados en el ejecutable."""
    with open(ruta, "rb") as fh:
        fh.seek(0, os.SEEK_END)
        tam = fh.tell()
        # La cookie está al final; se busca en la cola por si hay firma o relleno.
        cola = max(0, tam - 4096)
        fh.seek(cola)
        buf = fh.read()
        pos = buf.rfind(MAGIC)
        if pos < 0:
            raise SystemExit("No es un ejecutable de PyInstaller (no encuentro la cookie MEI).")
        magic, largo, pos_toc, len_toc, _pyvers, _pylib = COOKIE.unpack_from(buf, pos)
        inicio = cola + pos + COOKIE.size - largo   # comienzo del CArchive

        fh.seek(inicio + pos_toc)
        toc = fh.read(len_toc)

    nombres, i = [], 0
    while i + ENTRADA.size <= len(toc):
        structlen, _p, _l, _ul, _cf, _tc = ENTRADA.unpack_from(toc, i)
        if structlen <= ENTRADA.size:
            break
        crudo = toc[i + ENTRADA.size:i + structlen]
        nombres.append(crudo.split(b"\0", 1)[0].decode("utf-8", "replace"))
        i += structlen
    return nombres


def main() -> int:
    ap = argparse.ArgumentParser(description="Comprueba el contenido dentro del ejecutable")
    ap.add_argument("ejecutable")
    ap.add_argument("--clases", type=int, default=176, help="páginas de clase esperadas")
    ap.add_argument("--primos", type=int, default=136, help="anexos de primos esperados")
    ap.add_argument("--vivos", type=int, default=136, help="anexos de lenguajes vivos esperados")
    ap.add_argument("--fichas", type=int, default=60, help="fichas de lenguaje del Atlas")
    args = ap.parse_args()

    if not os.path.isfile(args.ejecutable):
        print(f"ERROR: no existe {args.ejecutable}", file=sys.stderr)
        return 1

    # PyInstaller usa el separador nativo: en Windows llegan con «\».
    nombres = [n.replace("\\", "/") for n in leer_toc(args.ejecutable)]
    clases = [n for n in nombres if re.search(r"/[0-9]{3}-[^/]+/README\.html$", n)]
    primos = [n for n in nombres if re.search(r"/[0-9]{3}-[^/]+/primos\.html$", n)]
    vivos = [n for n in nombres if re.search(r"/[0-9]{3}-[^/]+/vivos\.html$", n)]
    partes = [n for n in nombres if re.search(r"/parte-[0-9]+-[^/]+/README\.html$", n)]
    # Las fichas del Atlas: `atlas/*.html` menos sus tres índices, que no son fichas.
    fichas = [n for n in nombres
              if re.search(r"/atlas/[^/]+\.html$", n)
              and os.path.basename(n) not in ("README.html", "lenguajes.html", "vivos.html")]
    paginas = [n for n in nombres if n.endswith(".html")]
    mb = os.path.getsize(args.ejecutable) / (1024 * 1024)

    print(f"Ejecutable : {args.ejecutable} ({mb:.1f} MB)")
    print(f"Recursos   : {len(nombres)}")
    print(f"Páginas    : {len(paginas)} HTML · {len(clases)} clases · {len(partes)} partes · "
          f"{len(primos)} primos · {len(vivos)} vivos · {len(fichas)} fichas")

    fallos = []
    if len(clases) != args.clases:
        fallos.append(f"clases: esperadas {args.clases}, encontradas {len(clases)}")
    if len(primos) != args.primos:
        fallos.append(f"primos: esperados {args.primos}, encontrados {len(primos)}")
    if len(vivos) != args.vivos:
        fallos.append(f"vivos: esperados {args.vivos}, encontrados {len(vivos)}")
    if len(fichas) != args.fichas:
        fallos.append(f"fichas: esperadas {args.fichas}, encontradas {len(fichas)}")
    if not any(n.endswith("site/index.html") for n in nombres):
        fallos.append("falta site/index.html (la portada del curso)")

    if fallos:
        print("\nBLOQUEANTE — el ejecutable NO lleva el curso completo:")
        for f in fallos:
            print(f"  ✗ {f}")
        return 1

    print("\n✅ El ejecutable lleva el curso completo dentro.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
