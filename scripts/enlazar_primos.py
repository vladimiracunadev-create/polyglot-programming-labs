"""Enlaza cada muestra de código con las versiones de su familia en `primos.md`.

Bajo cada bloque de código del núcleo, inserta un enlace a la sección de
`primos.md` que resuelve **el mismo problema** en los lenguajes primos de esa
familia según el Atlas. Así, quien lee la versión de Python puede ver de
inmediato cómo lo escribirían Ruby, Perl, Lua, Tcl o R.

    ### Python · [`python/main.py`](implementaciones/python/main.py) · `python main.py`

    ```python
    ...
    ```

    > 🧬 El mismo programa en la familia **Scripting dinámico**:
    > [Ruby · Perl · Lua · Tcl · R](primos.md#scripting-dinamico)

Solo actúa en las clases que ya tienen `primos.md`. Es **idempotente**.

    python scripts/enlazar_primos.py [--dry-run]
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
CLASES = RAIZ / "classes"

# Nombre en el encabezado -> (familia, ancla en primos.md, primos del Atlas)
FAMILIA = {
    "Python": ("Scripting dinámico", "scripting-dinamico", ["Ruby", "Perl", "Lua", "Tcl", "R"]),
    "PHP": ("Scripting dinámico", "scripting-dinamico", ["Ruby", "Perl", "Lua", "Tcl", "R"]),
    "JavaScript": ("JavaScript / web", "javascript-web", ["Dart", "ActionScript"]),
    "TypeScript": ("JavaScript / web", "javascript-web", ["Dart", "ActionScript"]),
    "Java": ("JVM", "jvm", ["Kotlin", "Scala", "Groovy", "Clojure"]),
    "C#": (".NET", "dotnet", ["F#", "VB.NET"]),
    "C": ("C / llaves", "c-llaves", ["C++", "Objective-C"]),
    "Go": ("Sistemas", "sistemas", ["Zig", "Nim", "D"]),
    "Rust": ("Sistemas", "sistemas", ["Zig", "Nim", "D"]),
    "SQL": ("Lógica y declarativa", "logica-declarativa", ["Prolog", "Datalog"]),
}

ENCABEZADO = re.compile(r"^### (?P<lang>[A-Za-z#+]+(?: [A-Za-z#+]+)*) · ")
FENCE = re.compile(r"^```")


def cita(lang: str) -> list[str]:
    """Párrafo, no cita: una cita chocaría con las notas `>` que ya traen algunas clases (MD028)."""
    familia, ancla, primos = FAMILIA[lang]
    return [
        "",
        f"🧬 **El mismo programa en la familia {familia}:** "
        f"[{' · '.join(primos)}](primos.md#{ancla})",
    ]


def procesar(readme: Path) -> int:
    lineas = readme.read_text(encoding="utf-8").split("\n")
    salida: list[str] = []
    insertados = 0
    i = 0

    while i < len(lineas):
        linea = lineas[i]
        salida.append(linea)
        m = ENCABEZADO.match(linea)
        if not m or m.group("lang") not in FAMILIA:
            i += 1
            continue

        lang = m.group("lang")
        i += 1
        # Copia hasta cerrar el bloque de código que sigue al encabezado.
        abierto = False
        while i < len(lineas):
            actual = lineas[i]
            salida.append(actual)
            i += 1
            if FENCE.match(actual):
                if not abierto:
                    abierto = True
                else:
                    break

        # Inserta la cita si aún no está.
        resto = "\n".join(lineas[i : i + 4])
        if "primos.md#" not in resto:
            salida.extend(cita(lang))
            insertados += 1

    if insertados:
        readme.write_text("\n".join(salida), encoding="utf-8")
    return insertados


def main() -> None:
    dry = "--dry-run" in sys.argv
    con_primos = total = 0

    for readme in sorted(CLASES.glob("parte-*/[0-9][0-9][0-9]-*/README.md")):
        if not (readme.parent / "primos.md").exists():
            continue
        con_primos += 1
        if not dry:
            total += procesar(readme)

    if dry:
        print(f"[dry-run] {con_primos} clases con primos.md")
        return
    print(f"{con_primos} clases con primos.md · {total} enlaces de familia insertados")


if __name__ == "__main__":
    main()
