"""Andamiaje del programa: genera el manifest, las carpetas de clase/parte,
los README (con navegación ⏮️/⏭️) y el índice a partir de scripts/curriculo.py.

Idempotente: re-ejecutarlo actualiza el manifest y el índice. Por defecto crea
los README que falten SIN sobrescribir los ya construidos. Con --force-scaffold
regenera los README de las clases NO construidas (útil al cambiar la plantilla o
la navegación).

Uso:
    python scripts/build.py
    python scripts/build.py --force-scaffold
    python scripts/build.py --stats
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from curriculo import PARTES, slug, iter_clases, total_clases, NUCLEO  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
CLASSES = ROOT / "classes"

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

# Clases con contenido escrito a mano; el generador no las sobrescribe.
# Partes 0-2 (método, 1–40) + Partes 3-4 de código (041–072).
BUILT = set(range(1, 73))

NIVELES = ["Fundamentos", "Fundamentos", "Fundamentos", "Intermedio",
           "Intermedio", "Intermedio", "Intermedio", "Intermedio",
           "Intermedio", "Avanzado", "Avanzado", "Avanzado"]


def part_slug(idx, titulo):
    return f"parte-{idx}-{slug(titulo)}"


def class_slug(num, titulo):
    return f"{num:03d}-{slug(titulo)}"


def part_ranges():
    out, acc = [], 0
    for idx, (t, sub, clases) in enumerate(PARTES):
        ini, fin = acc + 1, acc + len(clases)
        acc = fin
        out.append((idx, t, sub, ini, fin, len(clases)))
    return out


# Secuencia global ordenada para la navegación ⏮️/⏭️.
ORDER = []
for _num, _idx, _titulo, _datos in iter_clases():
    ORDER.append((_num, _idx, _titulo))
_BY_NUM = {n: (n, i, t) for (n, i, t) in ORDER}


def nav_footer(num, idx):
    """Pie con clase anterior, índice de la parte, índice general y clase siguiente."""
    partes = []
    if num - 1 in _BY_NUM:
        pn, pi, pt = _BY_NUM[num - 1]
        partes.append(f"[⏮️ Clase {pn:03d}](../../{part_slug(pi, PARTES[pi][0])}/{class_slug(pn, pt)}/README.md)")
    partes.append("[📂 Parte](../README.md)")
    partes.append("[📚 Índice](../../README.md)")
    partes.append("[🌐 Atlas](../../../atlas/README.md)")
    if num + 1 in _BY_NUM:
        nn, ni, nt = _BY_NUM[num + 1]
        partes.append(f"[Clase {nn:03d} ⏭️](../../{part_slug(ni, PARTES[ni][0])}/{class_slug(nn, nt)}/README.md)")
    return " · ".join(partes)


def _bullets(items):
    return "\n".join(f"{i+1}. {x}" for i, x in enumerate(items))


def _temas(items):
    return "\n".join(f"| {i+1} | {tm} | {pq} |" for i, (tm, pq) in enumerate(items))


def _defs(items):
    return "\n".join(f"- **{t}** — {d}" for t, d in items)


def _errores(items):
    return "\n".join(f"- **{s}** → causa: {c} → solución: {so}" for s, c, so in items)


def _faq(items):
    return "\n".join(f"- **{q}** {a}" for q, a in items)


def clase_metodo(num, idx, titulo, d):
    """README de una clase conceptual/de método (Parte 0): sin implementaciones de código."""
    ptitulo = PARTES[idx][0]
    nivel = NIVELES[idx]
    dur = d.get("duracion", 75)
    ejemplo = ""
    if d.get("ejemplo"):
        ejemplo = f"## 🔎 Ejemplo\n\n{d['ejemplo']}\n\n"
    situacion = f"## 🧩 Situación\n\n{d['situacion']}\n\n" if d.get("situacion") else ""
    practica = f"## ✍️ Práctica\n\n{d['practica']}\n\n" if d.get("practica") else ""
    errores = f"## ⚠️ Errores comunes\n\n{_errores(d['errores'])}\n\n" if d.get("errores") else ""
    faq = f"## ❓ Preguntas frecuentes\n\n{_faq(d['faq'])}\n\n" if d.get("faq") else ""
    refs = d.get("referencias", ["Documentación de referencia de cada lenguaje del núcleo."])
    refs_md = "\n".join(f"- {r}" for r in refs)

    return f"""# Clase {num:03d} — {titulo}

> Parte **{idx} — {ptitulo}** · ⏱️ Duración estimada: **{dur} min** · Nivel: **{nivel}**
> ✅ **Clase construida.**

---

## 🎯 Objetivo

{d['objetivo']}

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

{_bullets(d['resultados'])}

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
{_temas(d['temas'])}

## 📖 Definiciones y características

{_defs(d['definiciones'])}

{situacion}{ejemplo}{practica}{errores}{faq}## 🔗 Referencias

{refs_md}

---

> {nav_footer(num, idx)}
"""


def clase_scaffold(num, idx, titulo):
    """Andamiaje honesto para una clase de código aún no escrita (con navegación)."""
    ptitulo = PARTES[idx][0]
    nivel = NIVELES[idx]
    objetivo = (
        f"Estudiar **{titulo.lower()}**: su forma independiente del lenguaje, cómo se expresa "
        f"idiomáticamente en el núcleo de 10 lenguajes y qué cambia (sintáctica, semántica o "
        f"paradigmáticamente) entre familias."
    )
    filas = "\n".join(
        f"| {LANG_META[l][0]} | `implementaciones/{l}/{LANG_META[l][1]}` | `{LANG_META[l][2]}` |"
        for l in NUCLEO
    )
    return f"""# Clase {num:03d} — {titulo}

> Parte **{idx} — {ptitulo}** · ⏱️ Duración estimada: **90 min** · Nivel: **{nivel}**
> 🚧 **Clase planificada** — página creada con la estructura y la navegación; contenido en desarrollo.

---

## 🎯 Objetivo

{objetivo}

## 🧮 Modelo

Cuando esta clase se construya, tendrá su especificación neutral (entradas · salidas · reglas) y su
[`casos.json`](casos.json) para verificar equivalencia.

## 🌐 Implementaciones idiomáticas (previstas)

| Lenguaje | Archivo | Cómo ejecutar |
|---|---|---|
{filas}

## 🔬 Comparación · 🧬 El concepto en la familia

Cada clase compara las tres clases de diferencia (sintáctica, semántica, paradigmática) y muestra el
concepto en los primos de cada familia. Consulta el [Atlas](../../../atlas/README.md).

---

> {nav_footer(num, idx)}
"""


def part_readme(idx, t, sub, ini, fin, count):
    prev = f"[⏮️ Parte {idx-1}](../{part_slug(idx-1, PARTES[idx-1][0])}/README.md) · " if idx > 0 else ""
    nxt = f" · [⏭️ Parte {idx+1}](../{part_slug(idx+1, PARTES[idx+1][0])}/README.md)" if idx < len(PARTES)-1 else ""
    filas, n = [], ini
    for c in PARTES[idx][2]:
        titulo = c[0] if isinstance(c, tuple) else c
        estado = "✅" if n in BUILT else "🚧"
        filas.append(f"| {estado} {n:03d} | [{titulo}]({class_slug(n, titulo)}/README.md) |")
        n += 1
    return f"""# Parte {idx} — {t}

> {prev}[⬅️ Programa](../../README.md) · [📚 Índice](../README.md){nxt}

**{count} clases** · rango {ini:03d}–{fin:03d}

{sub}

---

## 📚 Clases de esta parte

| # | Clase |
|---|---|
{chr(10).join(filas)}

---

> {prev}[⬅️ Programa](../../README.md) · [📚 Índice](../README.md){nxt}
"""


def build_manifest():
    parts = []
    for idx, t, sub, ini, fin, count in part_ranges():
        clases, n = [], ini
        for c in PARTES[idx][2]:
            titulo = c[0] if isinstance(c, tuple) else c
            clases.append({"num": n, "title": titulo, "slug": class_slug(n, titulo), "built": n in BUILT})
            n += 1
        parts.append({"idx": idx, "title": t, "subtitle": sub, "slug": part_slug(idx, t),
                      "start": ini, "end": fin, "count": count, "classes": clases})
    return {
        "program": "Polyglot Programming Labs",
        "tagline": "Aprende el concepto una vez. Reconócelo, compáralo y aplícalo en cualquier lenguaje.",
        "nucleo": NUCLEO,
        "total_planned": total_clases(),
        "total_built": len(BUILT),
        "parts_built": len({idx for n, idx, _t in ORDER if n in BUILT}),
        "parts_planned": len(PARTES),
        "parts": parts,
    }


def index_readme(manifest):
    built, planned = manifest["total_built"], manifest["total_planned"]
    bloques = []
    for p in manifest["parts"]:
        head = (f"## Parte {p['idx']} — {p['title']} · clases {p['start']:03d}–{p['end']:03d}\n\n"
                f"> [📂 README de la parte]({p['slug']}/README.md)\n\n| # | Clase |\n|---|---|")
        filas = [f"| {'✅' if c['built'] else '🚧'} {c['num']:03d} | [{c['title']}]({p['slug']}/{c['slug']}/README.md) |"
                 for c in p["classes"]]
        bloques.append(head + "\n" + "\n".join(filas))
    return f"""# 📚 Índice completo de clases

> [⬅️ Volver al programa](../README.md) · [🗺️ Roadmap](../ROADMAP.md) · [🌐 Atlas](../atlas/README.md)

Programa secuencial de **{planned} clases** en **{len(manifest['parts'])} partes**. La numeración es
global (001→…) y el orden importa: cada clase asume la anterior.

**Estado:** {built} clases construidas · {planned - built} planificadas · núcleo de {len(NUCLEO)} lenguajes.
Leyenda: ✅ construida · 🚧 planificada.

---

{(chr(10) + chr(10)).join(bloques)}
"""


def main():
    if "--stats" in sys.argv:
        print(f"Partes: {len(PARTES)} · Clases: {total_clases()} · Construidas: {len(BUILT)}")
        return

    force = "--force-scaffold" in sys.argv
    manifest = build_manifest()
    CLASSES.mkdir(exist_ok=True)
    (CLASSES / "_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=1), encoding="utf-8")

    for idx, t, sub, ini, fin, count in part_ranges():
        pdir = CLASSES / part_slug(idx, t)
        pdir.mkdir(exist_ok=True)
        (pdir / "README.md").write_text(part_readme(idx, t, sub, ini, fin, count), encoding="utf-8")

    creados = reescritos = 0
    for num, idx, titulo, datos in iter_clases():
        cdir = CLASSES / part_slug(idx, PARTES[idx][0]) / class_slug(num, titulo)
        cdir.mkdir(exist_ok=True)
        readme = cdir / "README.md"
        # Contenido: si hay datos con tipo "metodo", se renderiza rico; si no, andamiaje.
        if datos and datos.get("tipo") == "metodo":
            contenido = clase_metodo(num, idx, titulo, datos)
        else:
            contenido = clase_scaffold(num, idx, titulo)

        if not readme.exists():
            readme.write_text(contenido, encoding="utf-8")
            creados += 1
        elif datos and datos.get("tipo") == "metodo":
            # Las clases de método viven en los datos: se regeneran siempre.
            readme.write_text(contenido, encoding="utf-8")
            reescritos += 1
        elif force and num not in BUILT:
            readme.write_text(contenido, encoding="utf-8")
            reescritos += 1

    (CLASSES / "README.md").write_text(index_readme(manifest), encoding="utf-8")
    print(f"Manifest: {manifest['total_planned']} clases, {manifest['total_built']} construidas.")
    print(f"README de clase creados: {creados} · reescritos: {reescritos}.")


if __name__ == "__main__":
    main()
