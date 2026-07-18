"""Andamiaje del programa: genera el manifest, las carpetas de clase/parte,
los README y el índice a partir de scripts/curriculo.py.

Idempotente: re-ejecutarlo actualiza el manifest y el índice, y crea los README
de clase que falten SIN sobrescribir los ya construidos a mano (a menos que se
pase --force-scaffold).

Uso:
    python scripts/build.py            # crea/actualiza estructura
    python scripts/build.py --stats    # solo imprime totales
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from curriculo import PARTES, slug, iter_clases, total_clases, NUCLEO  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
CLASSES = ROOT / "classes"

# Metadatos de ejecución del núcleo (para la tabla "cómo ejecutar").
LANG_META = {
    "python":     ("Python",     "main.py",     "python main.py"),
    "javascript": ("JavaScript", "main.mjs",    "node main.mjs"),
    "typescript": ("TypeScript", "main.ts",     "pnpm exec tsx main.ts"),
    "java":       ("Java",       "Main.java",   "java Main.java"),
    "csharp":     ("C#",         "Program.cs",  "dotnet run"),
    "go":         ("Go",         "main.go",     "go run main.go"),
    "rust":       ("Rust",       "main.rs",     "rustc main.rs -o main && ./main"),
    "c":          ("C",          "main.c",      "cc main.c -o main && ./main"),
    "sql":        ("SQL",        "main.sql",    "sqlite3 :memory: < main.sql"),
    "php":        ("PHP",        "main.php",    "php main.php"),
}

# Clases construidas a mano (contenido real); el resto son andamiaje honesto.
# Se marca por número global. La clase insignia 041 tiene las 10 implementaciones.
BUILT = {1, 2, 3, 41}

NIVELES = ["Fundamentos", "Fundamentos", "Fundamentos", "Intermedio",
           "Intermedio", "Intermedio", "Intermedio", "Intermedio",
           "Intermedio", "Avanzado", "Avanzado", "Avanzado"]


def part_slug(idx: int, titulo: str) -> str:
    return f"parte-{idx}-{slug(titulo)}"


def class_slug(num: int, titulo: str) -> str:
    return f"{num:03d}-{slug(titulo)}"


def part_ranges():
    """Devuelve por parte (idx, titulo, sub, ini, fin, count)."""
    out = []
    acc = 0
    for idx, (t, sub, clases) in enumerate(PARTES):
        ini = acc + 1
        fin = acc + len(clases)
        acc = fin
        out.append((idx, t, sub, ini, fin, len(clases)))
    return out


# --------------------------------------------------------------------------- #
# Manifest
# --------------------------------------------------------------------------- #

def build_manifest() -> dict:
    parts = []
    ranges = part_ranges()
    for idx, t, sub, ini, fin, count in ranges:
        clases = []
        n = ini
        for c in PARTES[idx][2]:
            titulo = c[0] if isinstance(c, tuple) else c
            clases.append({
                "num": n,
                "title": titulo,
                "slug": class_slug(n, titulo),
                "built": n in BUILT,
            })
            n += 1
        parts.append({
            "idx": idx,
            "title": t,
            "subtitle": sub,
            "slug": part_slug(idx, t),
            "start": ini,
            "end": fin,
            "count": count,
            "classes": clases,
        })
    return {
        "program": "Polyglot Programming Labs",
        "tagline": "Aprende el concepto una vez. Reconócelo, compáralo y aplícalo en cualquier lenguaje.",
        "nucleo": NUCLEO,
        "total_planned": total_clases(),
        "total_built": len(BUILT),
        "parts_built": len({idx for _n, idx, _t, _d in iter_clases() if _n in BUILT}),
        "parts_planned": len(PARTES),
        "parts": parts,
    }


# --------------------------------------------------------------------------- #
# README de clase (andamiaje)
# --------------------------------------------------------------------------- #

def scaffold_class_readme(num, idx, titulo, datos) -> str:
    ptitulo = PARTES[idx][0]
    nivel = NIVELES[idx]
    dur = 90
    built = num in BUILT

    def bullets(items):
        return "\n".join(f"{i+1}. {x}" for i, x in enumerate(items))

    if datos:
        objetivo = datos.get("objetivo", "")
        resultados = bullets(datos.get("resultados", []))
        temas = "\n".join(
            f"| {i+1} | {tm} | {pq} |" for i, (tm, pq) in enumerate(datos.get("temas", []))
        )
        defs = "\n".join(f"- **{t}** — {d}" for t, d in datos.get("definiciones", []))
    else:
        objetivo = (
            f"Comprender **{titulo.lower()}** como conocimiento transferible: su forma "
            f"independiente del lenguaje, cómo se expresa en el núcleo de 10 lenguajes y "
            f"qué cambia (sintáctica, semántica o paradigmáticamente) de una familia a otra."
        )
        resultados = "_🚧 Contenido en desarrollo — la estructura de la clase ya está fijada._"
        temas = "| 1 | _en desarrollo_ | _pendiente_ |"
        defs = "_🚧 En desarrollo._"

    estado = ("> ✅ **Clase construida.**" if built
              else "> 🚧 **Clase planificada** — página creada, contenido en desarrollo.")

    # Tabla de ejecución del núcleo.
    filas = "\n".join(
        f"| {LANG_META[l][0]} | `implementaciones/{l}/{LANG_META[l][1]}` | `{LANG_META[l][2]}` |"
        for l in NUCLEO
    )
    if built and num == 41:
        impl_intro = "Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`:"
    else:
        impl_intro = ("Cuando esta clase se construya, aquí vivirá una implementación idiomática "
                      "por lenguaje del núcleo, verificadas contra `casos.json`:")

    return f"""# Clase {num:03d} — {titulo}

> Parte **{idx} — {ptitulo}** · ⏱️ Duración estimada: **{dur} min** · Nivel: **{nivel}**
{estado}

---

## 🎯 Objetivo

{objetivo}

## 📚 Resultados de aprendizaje

{resultados}

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
{temas}

## 📖 Definiciones y características

{defs}

## 🧩 Situación

_El problema observable que motiva esta clase._

## 🧮 Modelo

Entradas · salidas · reglas · casos límite. La especificación es neutral al lenguaje y se
verifica con [`casos.json`](casos.json).

## 📐 Algoritmo (pseudocódigo neutral)

```text
# pseudocódigo independiente del lenguaje
```

## 🌐 Implementaciones idiomáticas

{impl_intro}

| Lenguaje | Archivo | Cómo ejecutar |
|---|---|---|
{filas}

## 🔬 Comparación

| Clase de diferencia | Qué observar |
|---|---|
| Sintáctica | Cómo se escribe lo mismo en cada lenguaje |
| Semántica | Tipos, mutabilidad, memoria y errores |
| Paradigmática | Si el lenguaje invita a estructurar la solución de otra forma |

## 🧬 El concepto en la familia

Cómo se ve este concepto en los **primos** de cada familia (Ruby, Kotlin, Haskell, Elixir,
Lua, C++…), como _delta_ respecto del representante del núcleo. Consulta el
[Atlas](../../../atlas/README.md).

## ✅ Prueba común

Los mismos casos de entrada/salida para todas las implementaciones:
[`casos.json`](casos.json). Verifica la equivalencia con:

```bash
python scripts/verificar_equivalencia.py {class_slug(num, titulo)}
```

## 🧪 Reto de transferencia

Resuelve una variante en un lenguaje **no explicado paso a paso**. Detalle en
[`reto.md`](reto.md).

## ⚠️ Errores comunes

_Síntoma → causa → solución (en desarrollo)._

## ❓ Preguntas frecuentes

_En desarrollo._

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⬅️ Parte {idx}](../README.md) · [📚 Índice completo](../../README.md) · [🌐 Atlas de lenguajes](../../../atlas/README.md)
"""


# --------------------------------------------------------------------------- #
# README de parte
# --------------------------------------------------------------------------- #

def part_readme(idx, t, sub, ini, fin, count) -> str:
    prev = f"[⏮️ Parte {idx-1}](../{part_slug(idx-1, PARTES[idx-1][0])}/README.md) · " if idx > 0 else ""
    nxt = f" · [⏭️ Parte {idx+1}](../{part_slug(idx+1, PARTES[idx+1][0])}/README.md)" if idx < len(PARTES)-1 else ""
    filas = []
    n = ini
    for c in PARTES[idx][2]:
        titulo = c[0] if isinstance(c, tuple) else c
        cs = class_slug(n, titulo)
        estado = "✅" if n in BUILT else "🚧"
        filas.append(f"| {estado} {n:03d} | [{titulo}]({cs}/README.md) |")
        n += 1
    tabla = "\n".join(filas)
    return f"""# Parte {idx} — {t}

> {prev}[⬅️ Volver al programa](../../README.md) · [📚 Índice completo](../README.md){nxt}

**{count} clases** · rango {ini:03d}–{fin:03d}

{sub}

---

## 🎯 ¿De qué trata esta parte?

{sub}

## 📚 Clases

| # | Clase |
|---|---|
{tabla}

---

> [⬅️ Volver al programa](../../README.md) · [📚 Índice completo](../README.md)
"""


# --------------------------------------------------------------------------- #
# Índice general
# --------------------------------------------------------------------------- #

def index_readme(manifest) -> str:
    built = manifest["total_built"]
    planned = manifest["total_planned"]
    bloques = []
    for p in manifest["parts"]:
        idx, t = p["idx"], p["title"]
        ps = p["slug"]
        head = f"## Parte {idx} — {t} · clases {p['start']:03d}–{p['end']:03d}\n\n> [📂 README de la parte]({ps}/README.md)\n\n| # | Clase |\n|---|---|"
        filas = []
        for c in p["classes"]:
            estado = "✅" if c["built"] else "🚧"
            filas.append(f"| {estado} {c['num']:03d} | [{c['title']}]({ps}/{c['slug']}/README.md) |")
        bloques.append(head + "\n" + "\n".join(filas))
    cuerpo = "\n\n".join(bloques)
    return f"""# 📚 Índice completo de clases

> [⬅️ Volver al programa](../README.md) · [🗺️ Roadmap](../ROADMAP.md) · [🌐 Atlas](../atlas/README.md)

Programa secuencial de **{planned} clases** en **{len(manifest['parts'])} partes**. La numeración es
global (001→…) y el orden importa: cada clase asume la anterior.

**Estado:** {built} clases construidas · {planned - built} planificadas · núcleo de {len(NUCLEO)} lenguajes.
Leyenda: ✅ construida · 🚧 planificada.

---

{cuerpo}
"""


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #

def main():
    if "--stats" in sys.argv:
        print(f"Partes: {len(PARTES)} · Clases: {total_clases()} · Construidas: {len(BUILT)}")
        return

    manifest = build_manifest()
    CLASSES.mkdir(exist_ok=True)
    (CLASSES / "_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=1), encoding="utf-8")

    ranges = part_ranges()
    created = 0
    for idx, t, sub, ini, fin, count in ranges:
        pdir = CLASSES / part_slug(idx, t)
        pdir.mkdir(exist_ok=True)
        (pdir / "README.md").write_text(part_readme(idx, t, sub, ini, fin, count), encoding="utf-8")

    for num, idx, titulo, datos in iter_clases():
        pdir = CLASSES / part_slug(idx, PARTES[idx][0])
        cdir = pdir / class_slug(num, titulo)
        cdir.mkdir(exist_ok=True)
        readme = cdir / "README.md"
        # No sobrescribir clases construidas a mano si ya existen con contenido propio.
        if not readme.exists():
            readme.write_text(scaffold_class_readme(num, idx, titulo, datos), encoding="utf-8")
            created += 1
        elif "--force-scaffold" in sys.argv and num not in BUILT:
            readme.write_text(scaffold_class_readme(num, idx, titulo, datos), encoding="utf-8")

    (CLASSES / "README.md").write_text(index_readme(manifest), encoding="utf-8")
    print(f"Manifest: {manifest['total_planned']} clases, {manifest['total_built']} construidas.")
    print(f"README de clase creados: {created}.")
    print(f"Índice y {len(ranges)} README de parte generados.")


if __name__ == "__main__":
    main()
