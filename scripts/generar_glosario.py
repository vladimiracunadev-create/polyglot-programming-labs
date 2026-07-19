"""Genera glosario/README.md a partir de las clases construidas.

Recorre cada `classes/parte-N-.../NNN-.../README.md`, extrae la sección
"📖 Definiciones y características" y recopila las entradas con formato

    - **Término** — definición. Clave: ...

El glosario resultante ordena los términos alfabéticamente y enlaza cada uno a
todas las clases donde se define. No se edita a mano: se corrige la definición
en la clase de origen y se vuelve a ejecutar este script.

    python scripts/generar_glosario.py
"""

from __future__ import annotations

import re
import unicodedata
from itertools import groupby
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
CLASES = RAIZ / "classes"
SALIDA = RAIZ / "glosario" / "README.md"

# - **Término** — definición
ENTRADA = re.compile(r"^\s*-\s+\*\*(?P<termino>[^*]+)\*\*\s*[—–-]\s*(?P<definicion>.+?)\s*$")
ENCABEZADO_DEFINICIONES = re.compile(r"^##\s+.*Definiciones")
OTRO_ENCABEZADO = re.compile(r"^##\s+")


def sin_acentos(texto: str) -> str:
    """Clave de ordenación que ignora acentos, mayúsculas y comillas de código."""
    normalizado = unicodedata.normalize("NFD", texto.lower().lstrip("`"))
    return "".join(c for c in normalizado if unicodedata.category(c) != "Mn")


def inicial_de(termino: str) -> str:
    """Letra de agrupación; los símbolos y el código van a una sección aparte."""
    letra = sin_acentos(termino)[:1].upper()
    return letra if letra.isalpha() else "Símbolos"


def primera_frase(texto: str, maximo: int = 320) -> str:
    """Recorta la definición a su primera frase: el glosario resume, la clase explica."""
    # Corta en el primer punto seguido de mayúscula (evita partir `.clone()` o «p. ej.»).
    corte = re.search(r"(?<=[a-z0-9)»\"'])\.\s+(?=[A-ZÁÉÍÓÚÑ¿¡«])", texto)
    if corte:
        texto = texto[: corte.start()]
    if len(texto) > maximo:
        texto = texto[:maximo].rsplit(" ", 1)[0] + "…"
    return texto.strip().rstrip(".")


def definiciones_de(readme: Path) -> list[tuple[str, str]]:
    """Devuelve los pares (término, definición) de la sección de definiciones."""
    dentro = False
    encontradas: list[tuple[str, str]] = []
    for linea in readme.read_text(encoding="utf-8").splitlines():
        if ENCABEZADO_DEFINICIONES.match(linea):
            dentro = True
            continue
        if dentro and OTRO_ENCABEZADO.match(linea):
            break
        if not dentro:
            continue
        m = ENTRADA.match(linea)
        if m:
            termino = m.group("termino").strip()
            # La parte tras "Clave:" es un matiz didáctico, no la definición.
            definicion = primera_frase(m.group("definicion").split("Clave:")[0].strip())
            if termino and definicion:
                encontradas.append((termino, definicion))
    return encontradas


def recopilar() -> dict[str, dict]:
    """Term -> {definicion, clases: [(numero, enlace)]}."""
    glosario: dict[str, dict] = {}
    for readme in sorted(CLASES.glob("parte-*/[0-9][0-9][0-9]-*/README.md")):
        numero = readme.parent.name[:3]
        enlace = "../" + readme.relative_to(RAIZ).as_posix()
        for termino, definicion in definiciones_de(readme):
            entrada = glosario.setdefault(termino, {"definicion": definicion, "clases": []})
            if (numero, enlace) not in entrada["clases"]:
                entrada["clases"].append((numero, enlace))
    return glosario


def render(glosario: dict[str, dict]) -> str:
    terminos = sorted(glosario, key=sin_acentos)
    total_clases = len({c for e in glosario.values() for c in e["clases"]})

    lineas = [
        "# 📖 Glosario",
        "",
        "> [⬅️ Volver al programa](../README.md) · [📚 Índice completo](../classes/README.md)",
        "",
        f"**{len(terminos)} términos** recopilados de las secciones *Definiciones y características* "
        f"de las {total_clases} clases que las definen. Cada término enlaza a la clase (o clases) "
        "donde se explica **en contexto**: el glosario da la definición corta; la clase da el porqué, "
        "la comparación entre lenguajes y el código.",
        "",
        "> ⚙️ Este archivo se genera con `python scripts/generar_glosario.py`. **No se edita a mano**: "
        "para corregir una definición, edítala en la clase de origen y vuelve a generar.",
        "",
    ]

    for inicial, grupo in groupby(terminos, key=inicial_de):
        lineas += [f"## {inicial}", ""]
        for termino in grupo:
            entrada = glosario[termino]
            refs = " · ".join(f"[{num}]({enlace})" for num, enlace in sorted(entrada["clases"]))
            lineas.append(f"- **{termino}** — {entrada['definicion']}. · {refs}")
        lineas.append("")

    return "\n".join(lineas).rstrip() + "\n"


def main() -> None:
    glosario = recopilar()
    if not glosario:
        raise SystemExit("No se encontró ninguna definición. ¿Cambió el formato de las clases?")
    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    SALIDA.write_text(render(glosario), encoding="utf-8")
    total_refs = sum(len(e["clases"]) for e in glosario.values())
    print(f"Glosario generado: {len(glosario)} términos, {total_refs} referencias -> {SALIDA.relative_to(RAIZ)}")


if __name__ == "__main__":
    main()
