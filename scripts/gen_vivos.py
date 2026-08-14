#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera la página `vivos.md` de cada clase a partir de una especificación.

Qué es `vivos.md` y en qué se diferencia de `primos.md`:

  - `primos.md` compara **familias** del Atlas: el mismo programa en Ruby, Kotlin,
    Zig o Prolog, para reconocer el parecido dentro de una familia.
  - `vivos.md` pregunta otra cosa: **qué enseña ESTA clase en un lenguaje que
    lleva cuarenta años en producción**. COBOL sigue facturando, Fortran sigue
    prediciendo el clima y Ada sigue volando; cada uno resuelve el problema de la
    clase de una forma que los diez del núcleo ya no muestran.

El esqueleto de la página (encabezado, contrato, tabla de casos, secciones por
nivel de verificación, pie) se genera aquí para que las 136 clases sean
consistentes. **El contenido —el código y su explicación— se escribe a mano**,
clase por clase y lenguaje por lenguaje, en los módulos `vivos_parteN.py`: una
plantilla de prosa repetida sería exactamente el defecto que este material
quiere evitar.

    python scripts/gen_vivos.py 3            # una parte
    python scripts/gen_vivos.py 3 --dry-run
"""
from __future__ import annotations

import argparse
import importlib
import json
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

RAIZ = Path(__file__).resolve().parent.parent
CLASES = RAIZ / "classes"

# --------------------------------------------------------------------------
# Los lenguajes vivos, con su nivel de verificación.
#   ci        -> se ejecuta en CI contra el mismo casos.json que el núcleo
#   adaptado  -> no puede cumplir el contrato sin falsearse; se declara
#   lectura   -> podría, pero no hay toolchain en el runner; se declara
# --------------------------------------------------------------------------
LANGS = {
    "cobol": dict(
        nombre="COBOL", ficha="cobol", fence="cobol", nivel="ci",
        sector="Banca, seguros, gobierno, medios de pago",
        run="cobc -x -free prog.cob"),
    "fortran": dict(
        nombre="Fortran", ficha="fortran", fence="fortran", nivel="ci",
        sector="HPC, clima, física, BLAS/LAPACK",
        run="gfortran -O2 prog.f90"),
    "ada": dict(
        nombre="Ada", ficha="ada", fence="ada", nivel="ci",
        sector="Aviónica, espacio, ferrocarril, defensa",
        run="gnatmake prog.adb"),
    "pascal": dict(
        nombre="Pascal", ficha="pascal", fence="pascal", nivel="ci",
        sector="Escritorio empresarial, TPV, industria (vía Delphi y Free Pascal)",
        run="fpc -Mobjfpc prog.pas"),
    "lisp": dict(
        nombre="Common Lisp", ficha="common-lisp", fence="lisp", nivel="ci",
        sector="IA simbólica, CAD, investigación",
        run="sbcl --script prog.lisp"),
    "tcl": dict(
        nombre="Tcl", ficha="tcl", fence="tcl", nivel="ci",
        sector="Diseño de chips (EDA), redes, testing",
        run="tclsh prog.tcl"),
    "perl": dict(
        nombre="Perl", ficha="perl", fence="perl", nivel="ci",
        sector="Sysadmin, texto, bioinformática",
        run="perl prog.pl"),
    "cpp": dict(
        nombre="C++", ficha="cpp", fence="cpp", nivel="ci",
        sector="Videojuegos, navegadores, finanzas, HPC",
        run="g++ -std=c++17 prog.cpp"),
    "rpg": dict(
        nombre="RPG", ficha="rpg", fence="rpgle", nivel="adaptado",
        sector="IBM i: ERP, retail, logística, manufactura",
        run="CRTBNDRPG sobre IBM i",
        motivo="En IBM i un programa recibe sus datos por **parámetros**, por un "
               "**fichero** o por una **pantalla**, nunca por la entrada estándar."),
    "pli": dict(
        nombre="PL/I", ficha="pl-i", fence="pli", nivel="lectura",
        sector="Mainframe z/OS: banca, seguros",
        run="IBM Enterprise PL/I for z/OS"),
    "mumps": dict(
        nombre="M / MUMPS", ficha="mumps", fence="mumps", nivel="lectura",
        sector="Sanidad: historia clínica, VistA, Epic",
        run="YottaDB"),
    "smalltalk": dict(
        nombre="Smalltalk", ficha="smalltalk", fence="smalltalk", nivel="lectura",
        sector="Banca, seguros, trading",
        run="Pharo"),
}

ORDEN = ["cobol", "fortran", "ada", "pascal", "lisp", "tcl", "perl", "cpp",
         "rpg", "pli", "mumps", "smalltalk"]

SECCIONES = [
    ("ci", "## 🟢 Se ejecutan en CI", None),
    ("adaptado", "## 🟡 Contrato adaptado, y declarado",
     "Estos lenguajes **no pueden** leer de `stdin` y escribir en `stdout` sin dejar de ser ellos\n"
     "mismos. No es una limitación del material: es su naturaleza. El cálculo es el mismo y la forma\n"
     "de entrar y salir es la de su anfitrión. **No pasan por el verificador**, y se dice."),
    ("lectura", "## ⚪ Correctos, sin sello de máquina",
     "Sí podrían cumplir el contrato, pero su cadena de herramientas no está en los *runners* de CI."),
]


def tabla_casos(casos: list[dict]) -> str:
    filas = "\n".join(f"| `{c['stdin']}` | `{c['esperado']}` |" for c in casos)
    return "| stdin | esperado |\n|---|---|\n" + filas


def render(num: str, spec: dict, datos: dict, prof: int = 3) -> str:
    arriba = "../" * prof
    casos = datos.get("casos", [])
    out: list[str] = []
    a = out.append

    a(f"# 🧟 El mismo problema en los lenguajes que siguen vivos — Clase {num}")
    a("")
    a(f"> [⬅️ Volver a la clase {num}](README.md) · [🧬 Primos del Atlas](primos.md) ·")
    a(f"> [🧟 Índice de lenguajes vivos]({arriba}atlas/vivos.md) · [📚 Índice](../../README.md)")
    a("")
    a(spec["gancho"].strip())
    a("")
    a("> **🎯 Estos lenguajes no están aquí por ser antiguos**")
    a(">")
    a(f"> El criterio es doble y se declara en la [ficha de cada uno]({arriba}atlas/vivos.md):")
    a("> que **se ejecute hoy** —banca, sanidad, aviónica, ERP, diseño de chips, CAD— y que **deje a")
    a("> la vista un concepto que los diez del núcleo esconden**.")
    a(">")
    for parrafo in spec["porque"].strip().split("\n\n"):
        for linea in parrafo.strip().split("\n"):
            a("> " + linea)
        a(">")
    a("> Y ninguno es una foto fija: casi todos han incorporado en los últimos años JSON, REST, GPU,")
    a("> Unicode o Git. Cada ficha lo detalla en su sección `🔄 Lo que se ha modernizado`.")
    a("")
    a("## El contrato, igual para todos")
    a("")
    a(f"- **Entrada / salida:** {datos.get('contrato', '').strip()}")
    if datos.get("formula"):
        a(f"- **Regla:** `{datos['formula'].strip()}`")
    a("")
    a(tabla_casos(casos))
    a("")
    a("> **Qué está verificado en esta página.** Los lenguajes de la sección 🟢 se **ejecutan en CI**")
    a("> contra este mismo `casos.json`, igual que las diez implementaciones del núcleo")
    a(f"> ([workflow Labs]({arriba}labs/README.md)). Los de la sección 🟡 **no pueden** cumplir este")
    a("> contrato sin falsear el lenguaje, y se explica por qué. Los de la sección ⚪ sí podrían, pero")
    a("> su cadena de herramientas no está en los *runners*: son correctos, sin sello de máquina.")
    a("")
    a("---")
    a("")

    for nivel, titulo, nota in SECCIONES:
        claves = [k for k in ORDEN if k in spec["langs"] and LANGS[k]["nivel"] == nivel]
        if not claves:
            continue
        a(titulo)
        a("")
        if nota:
            a(nota)
            a("")
        for k in claves:
            L = LANGS[k]
            codigo, explicacion = spec["langs"][k]
            a(f"### {L['nombre']}")
            a("")
            a(f"[Ficha completa]({arriba}atlas/{L['ficha']}.md) · {L['sector']} · `{L['run']}`")
            a("")
            if L.get("motivo"):
                a("> " + L["motivo"])
                a("")
            a(f"```{L['fence']}")
            a(codigo.strip("\n"))
            a("```")
            a("")
            a(explicacion.strip())
            a("")
        a("---")
        a("")

    a("## Y de vuelta a la clase")
    a("")
    a(spec["cierre"].strip())
    a("")
    a(f"⏮️ [Volver a la clase {num}](README.md) · 🧬 [Los primos del Atlas](primos.md) ·")
    a(f"🧟 [Índice de lenguajes vivos]({arriba}atlas/vivos.md)")
    return "\n".join(out) + "\n"


def enlazar_readme(cdir: Path, spec: dict) -> bool:
    """Añade el enlace a `vivos.md` bajo el encabezado de la clase. Idempotente."""
    readme = cdir / "README.md"
    if not readme.is_file():
        return False
    texto = readme.read_text(encoding="utf-8")
    if "vivos.md" in texto:
        return False
    nombres = " · ".join(LANGS[k]["nombre"] for k in ORDEN if k in spec["langs"])
    bloque = (
        "\n📄 **Páginas de esta clase:** [🧬 Primos del Atlas](primos.md) — el mismo programa en las\n"
        "familias · [🧟 Lenguajes que siguen vivos](vivos.md) — el mismo problema en "
        f"{nombres},\ncon lo que cada uno enseña **sobre esta clase**.\n"
    )
    marca = "\n\n---\n"
    i = texto.find(marca)
    if i < 0:
        return False
    readme.write_text(texto[:i] + "\n" + bloque + texto[i:], encoding="utf-8")
    return True


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("parte", help="número de parte, p. ej. 3")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    try:
        mod = importlib.import_module(f"vivos_parte{args.parte}")
    except ModuleNotFoundError:
        print(f"❌ falta scripts/vivos_parte{args.parte}.py")
        return 2

    escritas = enlazadas = 0
    for num, spec in sorted(mod.SPECS.items()):
        cdirs = list(CLASES.glob(f"parte-*/{num}-*"))
        if not cdirs:
            print(f"  ❌ no encuentro la clase {num}")
            continue
        cdir = cdirs[0]
        datos = json.loads((cdir / "casos.json").read_text(encoding="utf-8"))
        pagina = render(num, spec, datos)
        faltan = [k for k in spec["langs"] if k not in LANGS]
        if faltan:
            print(f"  ❌ {num}: lenguajes desconocidos {faltan}")
            return 2
        if args.dry_run:
            print(f"  {num} · {len(spec['langs'])} lenguajes · {len(pagina)} bytes")
        else:
            (cdir / "vivos.md").write_text(pagina, encoding="utf-8", newline="\n")
            escritas += 1
            if enlazar_readme(cdir, spec):
                enlazadas += 1

    print(f"✅ {escritas} páginas vivos.md · {enlazadas} README enlazados")
    return 0


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    raise SystemExit(main())
