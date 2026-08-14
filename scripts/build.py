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
from curriculo import PARTES, slug, iter_clases, total_clases, NUCLEO, BIBLIO  # noqa: E402
from guias import GUIA, CLASES, HORAS, TIPO, ESTUDIAR  # noqa: E402

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

# Todas las clases construidas: Partes 0-2 de método (1–40) + Partes 3-11 de
# código (41–176). El programa está completo.
BUILT = set(range(1, 177))

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
    # Fuentes: los libros de la parte + las referencias propias de la clase.
    refs = list(BIBLIO.get(idx, [])) + list(d.get("referencias", []))
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


def _titulos_parte(idx):
    """{número global: título} de las clases de una parte."""
    ini = part_ranges()[idx][3]
    out, n = {}, ini
    for c in PARTES[idx][2]:
        out[n] = c[0] if isinstance(c, tuple) else c
        n += 1
    return out


def _recorrido(idx):
    """El cuerpo docente del README de parte: bloques con la descripción de cada clase.

    Cada clase se presenta con lo que se aprende en ella y por qué importa, no
    solo con su título: un índice de enlaces no enseña nada que el nombre de la
    carpeta no dijera ya.
    """
    titulos = _titulos_parte(idx)
    guia = GUIA.get(idx)
    if not guia:  # sin guía escrita: se degrada al listado simple, nunca a texto inventado.
        filas = [f"| {'✅' if n in BUILT else '🚧'} {n:03d} | [{t}]({class_slug(n, t)}/README.md) |"
                 for n, t in titulos.items()]
        return "| # | Clase |\n|---|---|\n" + "\n".join(filas)

    partes = []
    for titulo_bloque, porque, ini_b, fin_b in guia["bloques"]:
        rango = f"clase {ini_b:03d}" if ini_b == fin_b else f"clases {ini_b:03d}–{fin_b:03d}"
        partes.append(f"### 🔹 {titulo_bloque} · {rango}\n\n{porque}\n")
        for n in range(ini_b, fin_b + 1):
            t = titulos[n]
            estado = "" if n in BUILT else "🚧 "
            desc = CLASES.get(n, "")
            enlace = f"[{n:03d} · {t}]({class_slug(n, t)}/README.md)"
            partes.append(f"- {estado}**{enlace}** — {desc}" if desc else f"- {estado}**{enlace}**")
        partes.append("")
    return "\n".join(partes).rstrip()


def part_readme(idx, t, sub, ini, fin, count):
    prev = f"[⏮️ Parte {idx-1}](../{part_slug(idx-1, PARTES[idx-1][0])}/README.md) · " if idx > 0 else ""
    nxt = f" · [⏭️ Parte {idx+1}](../{part_slug(idx+1, PARTES[idx+1][0])}/README.md)" if idx < len(PARTES)-1 else ""
    libros = "\n".join(f"- {b}" for b in BIBLIO.get(idx, []))
    guia = GUIA.get(idx, {})
    tipo, horas, nivel = TIPO.get(idx, "código"), HORAS.get(idx), NIVELES[idx]
    cab = f"**{count} clases** · rango {ini:03d}–{fin:03d} · clases de **{tipo}** · nivel {nivel.lower()}"
    if horas:
        cab += f" · **~{horas} h** ([cronograma](../../docs/syllabus.md))"

    secciones = [f"# Parte {idx} — {t}",
                 f"> {prev}[⬅️ Programa](../../README.md) · [📚 Índice](../README.md){nxt}",
                 cab]
    if guia.get("gancho"):
        secciones.append(f"> 🧭 **{guia['gancho']}**")
    secciones.append("---")

    resumen = guia.get("resumen") or [sub]
    secciones.append("## 🧭 De qué trata esta parte\n\n" + "\n\n".join(resumen))

    if guia.get("asume"):
        secciones.append("## 🎒 Qué necesitas traer\n\n" + guia["asume"])

    if guia.get("logros"):
        logros = "\n".join(f"{i}. {x}" for i, x in enumerate(guia["logros"], 1))
        secciones.append("## 🎯 Qué sabrás hacer al terminar\n\n"
                         "Resultados comprobables: si no puedes hacerlos, la parte no está cerrada.\n\n" + logros)

    secciones.append("## 🗺️ El recorrido, clase a clase\n\n"
                     "Las clases están agrupadas en bloques por la razón que las une. "
                     "El orden es secuencial: cada una asume la anterior.\n\n" + _recorrido(idx))

    if guia.get("malentendidos"):
        filas = "\n".join(f"| {a} | {b} |" for a, b in guia["malentendidos"])
        secciones.append("## ⚠️ Los malentendidos que esta parte corrige\n\n"
                         "| Se suele creer | Lo que ocurre en realidad |\n|---|---|\n" + filas)

    pasos = ESTUDIAR.get(tipo)
    if pasos:
        secciones.append("## 🧪 Cómo estudiar esta parte\n\n"
                         + "\n".join(f"{i}. {p}" for i, p in enumerate(pasos, 1)))

    if libros:
        secciones.append("## 📚 Fuentes de referencia de esta parte\n\n"
                         "Cada clase cita estos libros en su sección de referencias. "
                         "No se reproduce su contenido: la redacción es original.\n\n" + libros)

    if guia.get("abre"):
        secciones.append("## 🔗 Qué abre esta parte\n\n" + guia["abre"])

    secciones.append("---")
    secciones.append(f"> {prev}[⬅️ Programa](../../README.md) · [📚 Índice](../README.md){nxt}")
    return "\n\n".join(secciones) + "\n"


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
    """Índice general: el mapa. La docencia de cada parte vive en su README."""
    built, planned = manifest["total_built"], manifest["total_planned"]
    bloques, resumen = [], []
    for p in manifest["parts"]:
        idx = p["idx"]
        guia = GUIA.get(idx, {})
        gancho = guia.get("gancho", p["subtitle"])
        resumen.append(f"| {idx} | [{p['title']}]({p['slug']}/README.md) | {p['count']} | "
                       f"{p['start']:03d}–{p['end']:03d} | {TIPO.get(idx, '—')} | ~{HORAS.get(idx, '—')} h |")

        head = (f"## Parte {idx} — {p['title']} · clases {p['start']:03d}–{p['end']:03d}\n\n"
                f"> 🧭 {gancho}\n>\n"
                f"> [📂 Abrir el README de la parte]({p['slug']}/README.md) — de qué trata, "
                f"qué necesitas traer, qué sabrás hacer al terminar y qué se aprende en cada clase.\n")
        # Los bloques temáticos de la parte, para que el índice muestre la estructura
        # y no solo una lista plana de dieciséis títulos seguidos.
        if guia.get("bloques"):
            for titulo_bloque, _porque, ini_b, fin_b in guia["bloques"]:
                rango = f"{ini_b:03d}" if ini_b == fin_b else f"{ini_b:03d}–{fin_b:03d}"
                filas = [f"| {'✅' if c['built'] else '🚧'} {c['num']:03d} | [{c['title']}]({p['slug']}/{c['slug']}/README.md) |"
                         for c in p["classes"] if ini_b <= c["num"] <= fin_b]
                head += f"\n**{titulo_bloque}** · {rango}\n\n| # | Clase |\n|---|---|\n" + "\n".join(filas) + "\n"
            bloques.append(head.rstrip())
        else:
            filas = [f"| {'✅' if c['built'] else '🚧'} {c['num']:03d} | [{c['title']}]({p['slug']}/{c['slug']}/README.md) |"
                     for c in p["classes"]]
            bloques.append(head + "\n| # | Clase |\n|---|---|\n" + "\n".join(filas))

    return f"""# 📚 Índice completo de clases

> [⬅️ Volver al programa](../README.md) · [🗺️ Roadmap](../ROADMAP.md) · [🌐 Atlas](../atlas/README.md) · [📅 Syllabus](../docs/syllabus.md)

Programa secuencial de **{planned} clases** en **{len(manifest['parts'])} partes**. La numeración es
global (001→…) y el orden importa: cada clase asume la anterior.

**Estado:** {built} de {planned} clases construidas · núcleo de {len(NUCLEO)} lenguajes.
{"Programa completo ✅." if built >= planned else "Leyenda: ✅ construida · 🚧 planificada."}

Este índice es el **mapa**: cada parte con su gancho y sus bloques temáticos. La
explicación de qué se aprende en cada clase está en el **README de cada parte**,
que es donde conviene entrar antes de abrir la primera clase.

## 🗂️ Las {len(manifest['parts'])} partes de un vistazo

| # | Parte | Clases | Rango | Tipo | Horas |
|---:|---|---:|---|---|---:|
{chr(10).join(resumen)}

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
        elif force and num not in BUILT:
            # Solo con --force-scaffold se reescriben las clases NO construidas.
            # Las clases ya construidas (incluidas las de método) tienen contenido
            # editado a mano y NO se sobrescriben.
            readme.write_text(contenido, encoding="utf-8")
            reescritos += 1

    (CLASSES / "README.md").write_text(index_readme(manifest), encoding="utf-8")
    print(f"Manifest: {manifest['total_planned']} clases, {manifest['total_built']} construidas.")
    print(f"README de clase creados: {creados} · reescritos: {reescritos}.")


if __name__ == "__main__":
    main()
