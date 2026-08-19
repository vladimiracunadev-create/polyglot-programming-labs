#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verificador de fuentes — capa OFFLINE, determinista, la que corre en CI y bloquea.

No toca la red. Comprueba que el registro `sources/bibliography.json` y las citas de las
176 clases forman un sistema cerrado y comprobable:

  1. el registro parsea y cumple el esquema;
  2. todo `book` lleva ISBN-13 con dígito de control válido; todo `paper`, un DOI;
     toda `standard`/`reference` una URL https con fecha de consulta;
  3. el `locator` coincide con la forma canónica de su tipo;
  4. toda obra citada en una clase existe en el registro;
  5. ninguna entrada del registro queda sin usar;
  6. cada cita declara el uso que la clase hace de la obra;
  7. ningún bloque de fuentes se repite entre clases;
  8. `used_in` está sincronizado con las citas reales;
  9. las cifras que muestra el README coinciden con el recuento del registro.

Uso:
    python scripts/verificar_fuentes.py            # verifica; sale 1 si algo falla
    python scripts/verificar_fuentes.py --sync     # reescribe used_in y el bloque del README
    python scripts/verificar_fuentes.py --cifras   # imprime el recuento en JSON

La red vive en `scripts/refrescar_fuentes.py`, que NO bloquea. Las dos capas están
separadas a propósito: si la red entra en el CI, el CI se vuelve inestable y se acaba
ignorando.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys
import unicodedata

RAIZ = pathlib.Path(__file__).resolve().parent.parent
REGISTRO = RAIZ / "sources" / "bibliography.json"
CLASES = RAIZ / "classes"
README = RAIZ / "README.md"

MARCA_INI = "<!-- FUENTES:INICIO — generado por scripts/verificar_fuentes.py; no editar a mano -->"
MARCA_FIN = "<!-- FUENTES:FIN -->"

CABECERA_REFS = "## 🔗 Referencias"

# - Autores — *Título* (paréntesis opcional)[ — [texto](url)]. Uso de la clase.
RE_CITA = re.compile(r"^- (?P<aut>.+?) — \*(?P<tit>[^*]+)\*(?P<resto>.*)$")
RE_PAREN = re.compile(r"^\s*\(([^)]*)\)")
RE_ENLACE = re.compile(r"^\s*—\s*\[[^\]]*\]\((?P<url>[^)]*)\)")
RE_EDICION = re.compile(r"(\d+)ª ed\.")
RE_ID = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
RE_DOI = re.compile(r"^10\.\d{4,9}/\S+$")

TIPOS = {"book", "paper", "standard", "reference", "dataset"}
ESTADOS = {"verificada", "pendiente"}

# Nombre visible de cada lenguaje del núcleo, en el orden en que los presenta el curso.
LENGUAJES = [
    ("python", "Python"), ("javascript", "JavaScript"), ("typescript", "TypeScript"),
    ("java", "Java"), ("csharp", "C#"), ("go", "Go"), ("rust", "Rust"),
    ("c", "C"), ("sql", "SQL"), ("php", "PHP"),
]


class Errores:
    def __init__(self) -> None:
        self.items: list[str] = []

    def __call__(self, msg: str) -> None:
        self.items.append(msg)

    def __bool__(self) -> bool:
        return bool(self.items)


# --------------------------------------------------------------------------- localizadores
def isbn13_valido(s: str) -> bool:
    """Dígito de control del ISBN-13 (norma ISO 2108: pesos 1 y 3 alternos, módulo 10)."""
    if not (isinstance(s, str) and len(s) == 13 and s.isdigit()):
        return False
    suma = sum(int(d) * (1 if i % 2 == 0 else 3) for i, d in enumerate(s[:12]))
    return (10 - suma % 10) % 10 == int(s[12])


def locator_canonico(e: dict) -> str | None:
    if e["type"] == "book":
        return f"https://openlibrary.org/isbn/{e.get('isbn13')}"
    if e["type"] == "paper":
        return f"https://doi.org/{e.get('doi')}"
    return e.get("locator")  # normas y documentación: la URL primaria es el localizador


# --------------------------------------------------------------------------- registro
def cargar_registro(err: Errores) -> dict:
    try:
        doc = json.loads(REGISTRO.read_text(encoding="utf-8"))
    except FileNotFoundError:
        err(f"no existe el registro {REGISTRO.relative_to(RAIZ)}")
        return {"entries": []}
    except json.JSONDecodeError as exc:
        err(f"el registro no es JSON válido: {exc}")
        return {"entries": []}

    if doc.get("schema_version") != 1:
        err(f"schema_version debe ser 1, es {doc.get('schema_version')!r}")
    for campo in ("verified_on", "policy", "entries"):
        if campo not in doc:
            err(f"falta el campo obligatorio «{campo}» en la raíz del registro")
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", str(doc.get("verified_on", ""))):
        err("verified_on debe tener la forma AAAA-MM-DD")

    vistos: set[str] = set()
    for i, e in enumerate(doc.get("entries", [])):
        ref = e.get("id") or f"#{i}"
        for campo in ("id", "type", "authors", "title", "published",
                      "locator", "authority", "accessed", "cite", "status", "used_in"):
            if campo not in e:
                err(f"[{ref}] falta el campo obligatorio «{campo}»")
        if not RE_ID.match(str(e.get("id", ""))):
            err(f"[{ref}] el id debe ser kebab-case estable")
        if e.get("id") in vistos:
            err(f"[{ref}] id duplicado")
        vistos.add(e.get("id"))
        if e.get("type") not in TIPOS:
            err(f"[{ref}] type debe ser uno de {sorted(TIPOS)}, es {e.get('type')!r}")
        if e.get("status") not in ESTADOS:
            err(f"[{ref}] status debe ser «verificada» o «pendiente», es {e.get('status')!r}")
        if not isinstance(e.get("authors"), list) or not e.get("authors"):
            err(f"[{ref}] authors debe ser una lista no vacía")
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", str(e.get("accessed", ""))):
            err(f"[{ref}] accessed debe tener la forma AAAA-MM-DD")
        if not isinstance(e.get("cite"), dict) or "title" not in e.get("cite", {}):
            err(f"[{ref}] cite debe llevar al menos «title»")

        if e.get("status") == "verificada":
            if e.get("type") == "book" and not isbn13_valido(str(e.get("isbn13", ""))):
                err(f"[{ref}] ISBN-13 ausente o con dígito de control inválido: {e.get('isbn13')!r}")
            if e.get("type") == "paper" and not RE_DOI.match(str(e.get("doi", ""))):
                err(f"[{ref}] DOI ausente o mal formado: {e.get('doi')!r}")
            if e.get("type") in {"standard", "reference", "dataset"}:
                if not str(e.get("locator", "")).startswith("https://"):
                    err(f"[{ref}] una fuente de tipo {e['type']} necesita URL https como localizador")

        canon = locator_canonico(e)
        if canon and e.get("locator") != canon:
            err(f"[{ref}] locator no canónico: {e.get('locator')!r} debería ser {canon!r}")
        for campo in ("online",):
            if campo in e and not str(e[campo]).startswith("https://"):
                err(f"[{ref}] «{campo}» debe ser una URL https")
    return doc


# --------------------------------------------------------------------------- citas
def normaliza(s: str) -> str:
    """Compara títulos ignorando acentos, mayúsculas y espacios repetidos."""
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", s).strip().casefold()


def clave_cita(titulo: str, parentesis: str) -> tuple[str, str | None]:
    m = RE_EDICION.search(parentesis or "")
    return normaliza(titulo), (f"{m.group(1)}ª ed." if m else None)


def leer_clases(err: Errores) -> tuple[list[dict], dict[str, list[str]]]:
    """Devuelve (citas, bloques) leyendo el apartado de referencias de cada clase."""
    citas: list[dict] = []
    bloques: dict[str, list[str]] = {}
    ficheros = sorted(CLASES.glob("*/*/README.md"))
    if not ficheros:
        err("no se encontró ninguna clase en classes/*/*/README.md")
    for f in ficheros:
        rel = f.relative_to(RAIZ).as_posix()
        txt = f.read_text(encoding="utf-8")
        m = re.search(rf"^{re.escape(CABECERA_REFS)}\s*$(.*?)(?=^---\s*$|\Z)", txt, re.M | re.S)
        if not m:
            err(f"{rel}: no tiene apartado «{CABECERA_REFS}»")
            continue
        bloque = m.group(1).strip()
        bloques.setdefault(bloque, []).append(rel)
        vinetas = [l.strip() for l in bloque.splitlines() if l.strip().startswith("- ")]
        if not vinetas:
            err(f"{rel}: el apartado de referencias no tiene ninguna cita")
        for linea in vinetas:
            mm = RE_CITA.match(linea)
            if not mm:
                err(f"{rel}: cita fuera de forma canónica → {linea[:90]}")
                continue
            resto = mm.group("resto")
            paren = ""
            mp = RE_PAREN.match(resto)
            if mp:
                paren = mp.group(1)
                resto = resto[mp.end():]
            me = RE_ENLACE.match(resto)
            if me:
                resto = resto[me.end():]
                mp2 = RE_PAREN.match(resto)
                if mp2:
                    paren = paren or mp2.group(1)
                    resto = resto[mp2.end():]
            uso = resto.strip().lstrip(",.").strip()
            if not uso:
                err(f"{rel}: la cita de «{mm.group('tit')}» no declara el uso que la clase hace de ella")
            citas.append({"clase": rel, "titulo": mm.group("tit").strip(),
                          "clave": clave_cita(mm.group("tit"), paren), "linea": linea})
    return citas, bloques


# --------------------------------------------------------------------------- cifras y README
def calcular(doc: dict, citas: list[dict]) -> dict:
    entradas = doc.get("entries", [])
    indice: dict[tuple[str, str | None], dict] = {}
    for e in entradas:
        c = e.get("cite", {})
        indice[(normaliza(c.get("title", "")), c.get("edition"))] = e
    usos: dict[str, list[str]] = {e["id"]: [] for e in entradas}
    huerfanas: dict[tuple[str, str | None], set[str]] = {}
    for c in citas:
        e = indice.get(c["clave"])
        if e is None:
            huerfanas.setdefault(c["clave"], set()).add(c["clase"])
        else:
            if c["clase"] not in usos[e["id"]]:
                usos[e["id"]].append(c["clase"])
    obras_citadas = {c["clave"] for c in citas}
    declaradas = obras_citadas - set(huerfanas)
    return {
        "clases": len({c["clase"] for c in citas}),
        "citas": len(citas),
        "obras_citadas": len(obras_citadas),
        "obras_declaradas": len(declaradas),
        "cobertura_pct": round(100.0 * len(declaradas) / len(obras_citadas), 1) if obras_citadas else 0.0,
        "entradas": len(entradas),
        "verificadas": sum(1 for e in entradas if e.get("status") == "verificada"),
        "pendientes": sum(1 for e in entradas if e.get("status") == "pendiente"),
        "libros": sum(1 for e in entradas if e.get("type") == "book"),
        "articulos": sum(1 for e in entradas if e.get("type") == "paper"),
        "_usos": usos,
        "_huerfanas": huerfanas,
        "_indice": indice,
    }


def bloque_readme(doc: dict, cif: dict) -> str:
    por_lang = {e.get("lang"): e for e in doc["entries"] if e.get("lang")}
    filas = []
    for clave, nombre in LENGUAJES:
        e = por_lang.get(clave)
        if not e:
            continue
        autores = "; ".join(a.split(",")[0] for a in e["authors"])
        ed = f" ({e['edition']})" if e.get("edition") else ""
        libre = f" · [edición libre]({e['online']})" if e.get("online") else ""
        filas.append(f"| **{nombre}** | {autores} — *{e['title']}*{ed} | "
                     f"[`{e['isbn13']}`]({e['locator']}){libre} |")
    return "\n".join([
        MARCA_INI,
        "",
        f"| Cifra | Valor |",
        f"|---|---:|",
        f"| Clases con apartado de fuentes | **{cif['clases']}** |",
        f"| Citas en total | **{cif['citas']}** |",
        f"| Obras distintas citadas | **{cif['obras_citadas']}** |",
        f"| Obras presentes en el registro | **{cif['obras_declaradas']}** |",
        f"| **Cobertura del registro** | **{cif['cobertura_pct']:.1f} %** |",
        f"| Entradas del registro (libros / artículos) | **{cif['entradas']}** ({cif['libros']} / {cif['articulos']}) |",
        f"| Entradas verificadas / pendientes | **{cif['verificadas']}** / **{cif['pendientes']}** |",
        "",
        "### Obra rectora de cada lenguaje del núcleo",
        "",
        "| Lenguaje | Obra rectora | ISBN-13 |",
        "|---|---|---|",
        *filas,
        "",
        MARCA_FIN,
    ])


# --------------------------------------------------------------------------- principal
def main() -> int:
    ap = argparse.ArgumentParser(description="Verifica el registro de fuentes y las citas de las clases.")
    ap.add_argument("--sync", action="store_true",
                    help="reescribe used_in en el registro y el bloque generado del README")
    ap.add_argument("--cifras", action="store_true", help="imprime el recuento en JSON y termina")
    args = ap.parse_args()

    err = Errores()
    doc = cargar_registro(err)
    citas, bloques = leer_clases(err)
    cif = calcular(doc, citas)

    if args.cifras:
        print(json.dumps({k: v for k, v in cif.items() if not k.startswith("_")},
                         ensure_ascii=False, indent=2))
        return 0

    # 4. toda obra citada existe en el registro
    for (tit, ed), clases in sorted(cif["_huerfanas"].items()):
        muestra = sorted(clases)[0]
        err(f"obra citada y no declarada en el registro: «{tit}»"
            f"{' ' + ed if ed else ''} (p. ej. {muestra}; {len(clases)} clases)")

    # 5. ninguna entrada del registro queda sin usar
    for e in doc.get("entries", []):
        if not cif["_usos"].get(e["id"]):
            err(f"[{e['id']}] entrada del registro que ninguna clase cita")

    # 7. ningún bloque de fuentes se repite entre clases
    for bloque, clases in bloques.items():
        if len(clases) > 1:
            err(f"bloque de fuentes repetido en {len(clases)} clases: {', '.join(sorted(clases)[:3])}…")

    # 8. used_in sincronizado
    if args.sync:
        for e in doc.get("entries", []):
            e["used_in"] = sorted(cif["_usos"].get(e["id"], []))
        REGISTRO.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n",
                            encoding="utf-8", newline="\n")
    else:
        for e in doc.get("entries", []):
            if list(e.get("used_in") or []) != sorted(cif["_usos"].get(e["id"], [])):
                err(f"[{e['id']}] used_in desincronizado; ejecuta «python scripts/verificar_fuentes.py --sync»")

    # 9. el bloque del README lo produce el verificador, no la mano
    texto = README.read_text(encoding="utf-8")
    esperado = bloque_readme(doc, cif)
    if MARCA_INI not in texto or MARCA_FIN not in texto:
        err(f"el README no contiene el bloque generado ({MARCA_INI})")
    else:
        ini = texto.index(MARCA_INI)
        fin = texto.index(MARCA_FIN) + len(MARCA_FIN)
        if args.sync:
            README.write_text(texto[:ini] + esperado + texto[fin:],
                              encoding="utf-8", newline="\n")
        elif texto[ini:fin] != esperado:
            err("las cifras del README no coinciden con el registro; "
                "ejecuta «python scripts/verificar_fuentes.py --sync»")

    print(f"registro   : {cif['entradas']} entradas "
          f"({cif['verificadas']} verificadas, {cif['pendientes']} pendientes)")
    print(f"clases     : {cif['clases']} con apartado de fuentes, {cif['citas']} citas")
    print(f"cobertura  : {cif['obras_declaradas']}/{cif['obras_citadas']} obras citadas "
          f"están en el registro ({cif['cobertura_pct']:.1f} %)")
    print(f"bloques    : {len(bloques)} distintos sobre {cif['clases']} clases")

    if err:
        print(f"\n✗ {len(err.items)} problema(s):", file=sys.stderr)
        for m in err.items:
            print(f"  - {m}", file=sys.stderr)
        return 1
    print("\n✓ fuentes verificadas")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
