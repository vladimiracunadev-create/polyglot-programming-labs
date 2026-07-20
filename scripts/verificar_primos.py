#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verifica los **lenguajes primos** de `primos.md` contra el mismo `casos.json`.

Las páginas `primos.md` resuelven el problema de cada clase en los lenguajes
primos de su familia del Atlas. Ese material nació como **ilustrativo**: nadie
lo ejecutaba. Este script lo ejecuta de verdad para los primos cuyo toolchain es
barato de instalar (Ruby, Perl y Lua están en los runners de GitHub casi de
fábrica), extrayendo el código del Markdown y alimentándolo por stdin.

Lo que no verifica: los otros 17 primos (Zig, Prolog, Objective-C, ActionScript…)
siguen siendo ilustrativos, y así se declara en cada página. Verificar tres de
veinte no es verificarlos todos, y conviene no vender lo contrario.

Uso:
  python scripts/verificar_primos.py 041           # una clase
  python scripts/verificar_primos.py --all         # todas
  python scripts/verificar_primos.py --all --lang perl
  python scripts/verificar_primos.py --all --estricto   # falla si un primo falla
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
CLASES = RAIZ / "classes"

# Primo -> (encabezado en primos.md, extensión, orden de ejecutables a probar)
PRIMOS = {
    "ruby": ("Ruby", ".rb", ["ruby"]),
    "perl": ("Perl", ".pl", ["perl"]),
    "lua": ("Lua", ".lua", ["lua", "lua5.4", "lua5.3", "luajit"]),
}

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


def ejecutable(lang: str) -> str | None:
    for c in PRIMOS[lang][2]:
        if shutil.which(c):
            return c
    return None


def extraer(primos_md: Path, lang: str) -> str | None:
    """Código del primo, tomado del bloque que sigue a su encabezado `### <Nombre>`."""
    nombre = PRIMOS[lang][0]
    texto = primos_md.read_text(encoding="utf-8")
    # `### Ruby` (posiblemente con sufijos como «Ruby 3») y el primer bloque cercado.
    patron = re.compile(
        r"^###\s+" + re.escape(nombre) + r"\b[^\n]*\n+```[a-z0-9+#]*\n(.*?)^```",
        re.M | re.S)
    m = patron.search(texto)
    return m.group(1) if m else None


def _texto(b: bytes) -> str:
    """Bytes del proceso a texto, normalizando finales de línea a `\\n`."""
    return b.decode("utf-8", errors="replace").replace("\r\n", "\n").replace("\r", "\n")


def correr(cmd: str, ruta: Path, entrada: str, timeout: int = 20) -> tuple[bool, str]:
    # stdin va en BYTES a propósito: en modo texto Python traduce `\n` a
    # `os.linesep`, así que en Windows el caso de prueba llegaría como
    # "Ada\r\n". Intérpretes sin capa :crlf (por ejemplo el Perl de Cygwin que
    # trae Git para Windows) dejan ese `\r` dentro del dato y `chomp` sólo se
    # come el `\n`: "Ada" mediría 4 y las búsquedas en hash fallarían. El
    # contrato es que el primo recibe exactamente lo que dice casos.json.
    try:
        p = subprocess.run([cmd, str(ruta)], input=(entrada + "\n").encode("utf-8"),
                           capture_output=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return False, "TIMEOUT"
    except OSError as e:
        return False, f"no se pudo ejecutar: {e}"
    if p.returncode != 0:
        err = _texto(p.stderr or b"").strip().splitlines()
        return False, (err[-1] if err else f"salida {p.returncode}")
    return True, _texto(p.stdout or b"").strip()


def verificar_clase(cdir: Path, langs: list[str]) -> list[tuple[str, str, str]]:
    """[(lang, estado, detalle)] con estado en {ok, FALLA, omitido}."""
    primos_md, casos_json = cdir / "primos.md", cdir / "casos.json"
    if not (primos_md.exists() and casos_json.exists()):
        return []
    casos = json.loads(casos_json.read_text(encoding="utf-8")).get("casos", [])
    if not casos:
        return []

    resultados = []
    for lang in langs:
        cmd = ejecutable(lang)
        if cmd is None:
            resultados.append((lang, "omitido", "toolchain no instalado"))
            continue
        codigo = extraer(primos_md, lang)
        if codigo is None:
            resultados.append((lang, "omitido", "sin bloque en primos.md"))
            continue

        with tempfile.TemporaryDirectory() as tmp:
            ruta = Path(tmp) / ("main" + PRIMOS[lang][1])
            # newline="\n": el fichero debe ser byte a byte el del Markdown.
            ruta.write_text(codigo, encoding="utf-8", newline="\n")
            fallo = None
            for caso in casos:
                ok, salida = correr(cmd, ruta, caso["stdin"])
                esperado = caso["esperado"].strip()
                if not ok:
                    fallo = f"stdin={caso['stdin']!r} → {salida}"
                    break
                if salida != esperado:
                    fallo = f"stdin={caso['stdin']!r} esperaba {esperado!r}, dio {salida!r}"
                    break
            resultados.append((lang, "FALLA", fallo) if fallo else (lang, "ok", ""))
    return resultados


def main() -> int:
    ap = argparse.ArgumentParser(description="Verifica los lenguajes primos contra casos.json.")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("clase", nargs="?", help="número de clase, p. ej. 041")
    g.add_argument("--all", action="store_true", help="todas las clases con primos.md")
    ap.add_argument("--lang", choices=sorted(PRIMOS), help="verificar solo este primo")
    ap.add_argument("--estricto", action="store_true",
                    help="devolver error si algún primo falla (por defecto solo informa)")
    args = ap.parse_args()

    langs = [args.lang] if args.lang else sorted(PRIMOS)
    if args.all:
        dirs = sorted(d for d in CLASES.glob("parte-*/[0-9][0-9][0-9]-*") if (d / "primos.md").exists())
    else:
        dirs = [d for d in CLASES.glob(f"parte-*/{args.clase}-*") if (d / "primos.md").exists()]
        if not dirs:
            print(f"No encontré la clase {args.clase} con primos.md")
            return 1

    total = {"ok": 0, "FALLA": 0, "omitido": 0}
    fallos: list[str] = []
    for cdir in dirs:
        for lang, estado, detalle in verificar_clase(cdir, langs):
            total[estado] += 1
            if estado == "FALLA":
                fallos.append(f"  {cdir.name[:3]} · {lang}: {detalle}")

    print(f"\n== Primos verificados: {total['ok']} ok · {total['FALLA']} fallan · "
          f"{total['omitido']} omitidos ==")
    if fallos:
        print(f"\nFallos ({len(fallos)}):")
        for f in fallos[:60]:
            print(f)
        if len(fallos) > 60:
            print(f"  … y {len(fallos) - 60} más")

    if args.estricto and total["FALLA"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
