"""Enlaza cada bloque de código a la vista con su archivo real en implementaciones/.

En las clases de código, el README muestra el código de los 10 lenguajes del
núcleo. Este script convierte el encabezado de cada lenguaje

    ### Python · `python main.py`

en uno que enlaza al archivo fuente de verdad:

    ### Python · [`python/main.py`](implementaciones/python/main.py) · `python main.py`

Así el código a la vista es trazable: se lee en la clase y se abre, ejecuta o
copia desde su archivo. Es **idempotente**: si el enlace ya está, no lo repite.

    python scripts/enlazar_codigo.py [--dry-run]
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
CLASES = RAIZ / "classes"

# Nombre que aparece en el encabezado -> carpeta dentro de implementaciones/
CARPETA = {
    "Python": "python",
    "JavaScript": "javascript",
    "TypeScript": "typescript",
    "Java": "java",
    "C#": "csharp",
    "Go": "go",
    "Rust": "rust",
    "C": "c",
    "SQL": "sql",
    "PHP": "php",
}

# Extensiones de fuente por carpeta (excluye manifiestos: .csproj, go.mod, Cargo.toml...)
EXTENSIONES = {
    "python": (".py",),
    "javascript": (".mjs", ".js"),
    "typescript": (".ts",),
    "java": (".java",),
    "csharp": (".cs",),
    "go": (".go",),
    "rust": (".rs",),
    "c": (".c",),
    "sql": (".sql",),
    "php": (".php",),
}

# ### Python · `python main.py`
ENCABEZADO = re.compile(r"^### (?P<lang>[A-Za-z#+]+(?: [A-Za-z#+]+)*) · (?P<run>`[^`]+`)\s*$")

INTRO_VIEJA = "Cada bloque es el archivo real de [`implementaciones/`](implementaciones/):"
INTRO_NUEVA = (
    "Cada bloque es el archivo real de [`implementaciones/`](implementaciones/): "
    "el enlace de cada lenguaje abre su fuente, y el comando de al lado lo ejecuta."
)


def fuente_de(dir_lang: Path, carpeta: str) -> Path | None:
    """Archivo fuente principal de un lenguaje dentro de implementaciones/<carpeta>/."""
    if not dir_lang.is_dir():
        return None
    candidatos = [f for f in sorted(dir_lang.iterdir()) if f.suffix in EXTENSIONES[carpeta]]
    if not candidatos:
        return None
    # Prioriza el punto de entrada convencional del lenguaje.
    for f in candidatos:
        if f.stem.lower() in {"main", "program", "index"}:
            return f
    return candidatos[0]


def procesar(readme: Path) -> int:
    impl = readme.parent / "implementaciones"
    if not impl.is_dir():
        return 0

    lineas = readme.read_text(encoding="utf-8").split("\n")
    enlazados = 0

    for i, linea in enumerate(lineas):
        if linea.strip() == INTRO_VIEJA:
            lineas[i] = linea.replace(INTRO_VIEJA, INTRO_NUEVA)
            continue
        if "](implementaciones/" in linea:  # ya enlazado
            continue
        m = ENCABEZADO.match(linea)
        if not m:
            continue
        carpeta = CARPETA.get(m.group("lang"))
        if not carpeta:
            continue
        fuente = fuente_de(impl / carpeta, carpeta)
        if not fuente:
            continue
        rel = fuente.relative_to(impl).as_posix()
        lineas[i] = f"### {m.group('lang')} · [`{rel}`](implementaciones/{rel}) · {m.group('run')}"
        enlazados += 1

    if enlazados:
        readme.write_text("\n".join(lineas), encoding="utf-8")
    return enlazados


def main() -> None:
    dry = "--dry-run" in sys.argv
    total_clases = total_enlaces = 0
    sin_enlazar: list[str] = []

    for readme in sorted(CLASES.glob("parte-*/[0-9][0-9][0-9]-*/README.md")):
        if not (readme.parent / "implementaciones").is_dir():
            continue
        total_clases += 1
        if dry:
            continue
        n = procesar(readme)
        total_enlaces += n
        if n and n != len(CARPETA):
            sin_enlazar.append(f"{readme.parent.name}: {n}/{len(CARPETA)}")

    if dry:
        print(f"[dry-run] {total_clases} clases con implementaciones/")
        return

    print(f"{total_clases} clases procesadas · {total_enlaces} bloques enlazados")
    if sin_enlazar:
        print("Clases con lenguajes sin archivo fuente localizado:")
        for s in sin_enlazar:
            print("  -", s)


if __name__ == "__main__":
    main()
