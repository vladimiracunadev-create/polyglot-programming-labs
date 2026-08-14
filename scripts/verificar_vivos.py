#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ejecuta de verdad los **lenguajes vivos** de cada `vivos.md` contra su `casos.json`.

Cada clase de código tiene una página `vivos.md` que resuelve **el problema de esa
clase** en los lenguajes antiguos que siguen en producción (ver
`atlas/vivos.md`). Este script extrae ese código del Markdown, lo compila o lo
interpreta, le da la entrada por stdin y compara la salida con la que espera el
mismo `casos.json` que verifica a las diez implementaciones del núcleo.

Qué SÍ se verifica aquí (toolchain barato de instalar en un runner de Ubuntu):

    COBOL (GnuCOBOL) · Fortran (gfortran) · Ada (GNAT) · Pascal (Free Pascal)
    Common Lisp (SBCL) · Tcl (tclsh) · Perl · C++ (g++)

Qué NO, y por qué — se declara en cada página en lugar de fingir lo contrario:

  - **Contrato adaptado**: RPG recibe parámetros, no stdin; JCL no calcula, orquesta;
    VBA vive dentro de Excel; AutoLISP dentro de AutoCAD. Su código es correcto para
    su anfitrión, pero no puede pasar por este verificador sin falsear el lenguaje.
  - **Sin toolchain en CI**: PL/I necesita z/OS, MUMPS y Smalltalk requieren
    instalaciones pesadas, y el ensamblador depende de la arquitectura concreta.

Verificar ocho de dieciocho no es verificarlos todos, y conviene no venderlo así.

Uso:
  python scripts/verificar_vivos.py 041                 # una clase
  python scripts/verificar_vivos.py --all               # todas
  python scripts/verificar_vivos.py --all --lang cobol  # un solo lenguaje
  python scripts/verificar_vivos.py --all --estricto    # falla si algo falla
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
CLASES = RAIZ / "classes"

# clave -> (encabezado en vivos.md, extensión, candidatos de ejecutable)
VIVOS = {
    "cobol":   ("COBOL",        ".cob",  ["cobc"]),
    "fortran": ("Fortran",      ".f90",  ["gfortran"]),
    "ada":     ("Ada",          ".adb",  ["gnatmake"]),
    "pascal":  ("Pascal",       ".pas",  ["fpc"]),
    "lisp":    ("Common Lisp",  ".lisp", ["sbcl"]),
    "tcl":     ("Tcl",          ".tcl",  ["tclsh", "tclsh8.6", "tclsh9.0"]),
    "perl":    ("Perl",         ".pl",   ["perl"]),
    "cpp":     ("C++",          ".cpp",  ["g++", "clang++"]),
}

# Lenguajes que aparecen en las páginas pero NO se ejecutan, con el motivo.
# Se listan aquí para que el informe los nombre en vez de callarlos.
NO_VERIFICADOS = {
    "RPG":         "contrato adaptado (parámetros de IBM i, no stdin)",
    "JCL":         "no calcula: orquesta el COBOL que sí calcula",
    "VBA":         "contrato adaptado (celdas de Excel, no stdin)",
    "AutoLISP":    "contrato adaptado (línea de comandos de AutoCAD)",
    "PL/I":        "sin compilador en CI (requiere z/OS)",
    "M / MUMPS":   "sin intérprete en CI",
    "Smalltalk":   "sin imagen Pharo en CI",
    "Assembler":   "específico de arquitectura (x86-64 System V)",
}

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


def ejecutable(lang: str) -> str | None:
    for c in VIVOS[lang][2]:
        if shutil.which(c):
            return c
    return None


def extraer(vivos_md: Path, lang: str) -> str | None:
    """Código del lenguaje, del primer bloque cercado tras su `### <Nombre>`."""
    nombre = VIVOS[lang][0]
    texto = vivos_md.read_text(encoding="utf-8")
    # Ojo con `\b`: tras el `+` de "C++" nunca casa, porque `+` no es carácter de
    # palabra. La alternativa correcta es un lookahead negativo explícito.
    patron = re.compile(
        r"^###\s+" + re.escape(nombre) + r"(?![\w+#])[^\n]*\n"  # el encabezado
        r"(?:(?!^###\s)[^\n]*\n)*?"                             # prosa intermedia
        r"```[a-z0-9+#-]*\n(.*?)^```",                          # el primer bloque
        re.M | re.S)
    m = patron.search(texto)
    return m.group(1) if m else None


def _texto(b: bytes) -> str:
    return b.decode("utf-8", errors="replace").replace("\r\n", "\n").replace("\r", "\n")


def correr(cmd: list[str], entrada: str, cwd: Path, timeout: int = 30) -> tuple[bool, str]:
    # stdin en BYTES: en modo texto Python traduciría `\n` a os.linesep y en
    # Windows el caso llegaría como "Ada\r\n". El contrato es que el programa
    # recibe exactamente lo que dice casos.json.
    try:
        p = subprocess.run(cmd, input=entrada.encode("utf-8"), cwd=str(cwd),
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                           timeout=timeout)
    except subprocess.TimeoutExpired:
        return False, "TIMEOUT"
    except OSError as e:
        return False, f"ERROR AL EJECUTAR: {e}"
    if p.returncode != 0:
        return False, _texto(p.stderr).strip() or f"código de salida {p.returncode}"
    return True, _texto(p.stdout).strip()


def compilar(lang: str, exe: str, fuente: Path, tmp: Path) -> tuple[list[str] | None, str]:
    """Devuelve (comando de ejecución, error). Los interpretados no compilan."""
    binario = tmp / ("prog.exe" if os.name == "nt" else "prog")

    if lang == "tcl":
        return [exe, str(fuente)], ""
    if lang == "perl":
        return [exe, str(fuente)], ""
    if lang == "lisp":
        return [exe, "--script", str(fuente)], ""

    if lang == "cobol":
        cmd = [exe, "-x", "-free", "-o", str(binario), str(fuente)]
    elif lang == "fortran":
        cmd = [exe, "-O1", "-o", str(binario), str(fuente)]
    elif lang == "ada":
        # GNAT exige que el fichero se llame como la unidad, en minúsculas.
        cmd = [exe, "-q", "-o", str(binario), str(fuente)]
    elif lang == "pascal":
        cmd = [exe, "-Mobjfpc", f"-o{binario}", str(fuente)]
    elif lang == "cpp":
        cmd = [exe, "-O1", "-std=c++17", "-o", str(binario), str(fuente)]
    else:
        return None, f"lenguaje sin regla de compilación: {lang}"

    p = subprocess.run(cmd, cwd=str(tmp), stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE, timeout=180)
    if p.returncode != 0 or not binario.exists():
        return None, (_texto(p.stderr) or _texto(p.stdout)).strip()[:1200]
    return [str(binario)], ""


def nombre_fuente(lang: str, codigo: str) -> str:
    """El nombre del fichero importa en Ada: GNAT lo usa para localizar la unidad."""
    if lang == "ada":
        m = re.search(r"^\s*procedure\s+([A-Za-z]\w*)\s+is", codigo, re.M)
        if m:
            return m.group(1).lower() + ".adb"
        return "prog.adb"
    return "prog" + VIVOS[lang][1]


def verificar_clase(cdir: Path, langs: list[str], verboso: bool) -> tuple[int, int, int]:
    vivos_md = cdir / "vivos.md"
    casos_json = cdir / "casos.json"
    if not vivos_md.is_file() or not casos_json.is_file():
        return 0, 0, 0

    casos = json.loads(casos_json.read_text(encoding="utf-8")).get("casos", [])
    num = cdir.name[:3]
    ok = fallos = omitidos = 0

    for lang in langs:
        nombre = VIVOS[lang][0]
        codigo = extraer(vivos_md, lang)
        if codigo is None:
            continue                          # ese lenguaje no está en esta clase
        exe = ejecutable(lang)
        if exe is None:
            omitidos += 1
            if verboso:
                print(f"  {num} {nombre:<13} ⚪ omitido (sin {VIVOS[lang][2][0]})")
            continue

        with tempfile.TemporaryDirectory() as td:
            tmp = Path(td)
            fuente = tmp / nombre_fuente(lang, codigo)
            fuente.write_text(codigo, encoding="utf-8", newline="\n")

            cmd, err = compilar(lang, exe, fuente, tmp)
            if cmd is None:
                fallos += 1
                print(f"  {num} {nombre:<13} ❌ no compila")
                print(f"      {err.splitlines()[0] if err else ''}")
                continue

            malos = []
            for caso in casos:
                entrada = caso["stdin"]
                if not entrada.endswith("\n"):
                    entrada += "\n"
                bien, salida = correr(cmd, entrada, tmp)
                esperado = caso["esperado"].strip()
                if not bien or salida != esperado:
                    malos.append((caso["stdin"], esperado, salida))

            if malos:
                fallos += 1
                print(f"  {num} {nombre:<13} ❌ {len(malos)}/{len(casos)} casos")
                for e, esp, got in malos[:2]:
                    print(f"      stdin={e!r}  esperado={esp!r}  obtenido={got!r}")
            else:
                ok += 1
                if verboso:
                    print(f"  {num} {nombre:<13} ✅ {len(casos)}/{len(casos)} casos")

    return ok, fallos, omitidos


def clases(filtro: str | None) -> list[Path]:
    todas = sorted(p.parent for p in CLASES.glob("parte-*/[0-9][0-9][0-9]-*/vivos.md"))
    if filtro:
        todas = [c for c in todas if c.name.startswith(filtro)]
    return todas


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("clase", nargs="?", help="número de clase, p. ej. 041")
    ap.add_argument("--all", action="store_true", help="todas las clases con vivos.md")
    ap.add_argument("--lang", help="solo estos lenguajes (coma): " + ",".join(VIVOS))
    ap.add_argument("--estricto", action="store_true", help="salir con error si algo falla")
    ap.add_argument("-v", "--verboso", action="store_true")
    args = ap.parse_args()

    if not args.all and not args.clase:
        ap.print_help()
        return 2

    langs = list(VIVOS)
    if args.lang:
        langs = [l.strip() for l in args.lang.split(",") if l.strip() in VIVOS]
        if not langs:
            print(f"❌ --lang desconocido. Válidos: {', '.join(VIVOS)}")
            return 2

    objetivo = clases(None if args.all else args.clase)
    if not objetivo:
        print("No hay clases con vivos.md que coincidan.")
        return 0

    print(f"🧟 Verificando lenguajes vivos · {len(objetivo)} clase(s) · "
          f"{len(langs)} lenguaje(s): {', '.join(VIVOS[l][0] for l in langs)}")
    print()

    ok = fallos = omitidos = 0
    for cdir in objetivo:
        a, b, c = verificar_clase(cdir, langs, args.verboso or len(objetivo) == 1)
        ok += a
        fallos += b
        omitidos += c

    print()
    print(f"✅ {ok} implementaciones correctas · ❌ {fallos} fallidas · ⚪ {omitidos} omitidas")
    print()
    print("No pasan por aquí, y se declara en cada página:")
    for nombre, motivo in NO_VERIFICADOS.items():
        print(f"  ⚪ {nombre:<12} {motivo}")

    if fallos and args.estricto:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
