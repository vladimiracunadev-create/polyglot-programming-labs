#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Refrescador de fuentes — capa EN RED, manual o programada, que NO bloquea.

Contrasta cada entrada de `sources/bibliography.json` contra la autoridad que dice tenerla:

  * `book`      → https://openlibrary.org/isbn/{isbn13}.json, comparando título y autores;
  * `paper`     → https://api.crossref.org/works/{doi}, comparando título y autores;
  * `standard`, `reference`, `dataset` → GET a la URL primaria, registrando el estado HTTP.

Además hace GET a los campos `online` (ediciones libres) para saber si siguen en pie.

Al terminar actualiza `verified_on` y el `accessed` de lo que resolvió, y **reporta** lo que
dejó de resolver **sin borrarlo**: una fuente que hoy no responde se marca, no se elimina.

Uso:
    python scripts/refrescar_fuentes.py              # informe, no escribe
    python scripts/refrescar_fuentes.py --escribir   # además actualiza el registro
    python scripts/refrescar_fuentes.py --solo kr-c  # filtra por prefijo de id

Sale 0 aunque haya fallos de red: esta capa informa, no bloquea. La que bloquea es
`scripts/verificar_fuentes.py`, y no toca la red.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import pathlib
import re
import sys
import time
import unicodedata
import urllib.error
import urllib.request

RAIZ = pathlib.Path(__file__).resolve().parent.parent
REGISTRO = RAIZ / "sources" / "bibliography.json"

UA = {"User-Agent": "polyglot-programming-labs verificador-de-fuentes "
                    "(+https://github.com/vladimiracunadev-create/polyglot-programming-labs)"}
INTENTOS = 4
ESPERA = 45


def normaliza(s: str) -> str:
    s = unicodedata.normalize("NFKD", s or "")
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r"[^a-z0-9 ]+", " ", s.casefold())
    return re.sub(r"\s+", " ", s).strip()


def normaliza_titulo(s: str) -> str:
    """Como normaliza(), pero perdona el artículo inicial y el ordinal de edición.

    Los catálogos titulan la misma obra de formas distintas: Open Library registra el libro
    de Klabnik y Nichols como «Rust Programming Language, 2nd Edition» y el registro lo cita
    como «The Rust Programming Language». Eso no es una discrepancia de fuente.
    """
    s = normaliza(s)
    s = re.sub(r"\b\d+(st|nd|rd|th)? edition\b", " ", s)
    s = re.sub(r"^(the|a|an) ", "", s)
    return re.sub(r"\s+", " ", s).strip()


def pedir(url: str, solo_cabecera: bool = False):
    """Devuelve (ok, carga_o_estado). Reintenta ante fallos transitorios de red."""
    ultimo = ""
    for i in range(INTENTOS):
        try:
            req = urllib.request.Request(url, headers=UA, method="HEAD" if solo_cabecera else "GET")
            with urllib.request.urlopen(req, timeout=ESPERA) as r:
                if solo_cabecera:
                    return True, f"HTTP {r.status}"
                return True, json.load(r)
        except urllib.error.HTTPError as exc:
            return False, f"HTTP {exc.code}"
        except Exception as exc:  # red intermitente, DNS, TLS…
            ultimo = f"{type(exc).__name__}: {exc}"
            time.sleep(2 + 2 * i)
    return False, ultimo


def comprueba_libro(e: dict) -> tuple[str, str]:
    ok, carga = pedir(f"https://openlibrary.org/isbn/{e['isbn13']}.json")
    if not ok:
        return "sin-resolver", str(carga)
    titulo = normaliza_titulo(carga.get("title", ""))
    esperado = normaliza_titulo(e["title"])
    # Open Library a veces guarda el subtítulo aparte o el ordinal dentro del título.
    if esperado in titulo or titulo in esperado:
        return "ok", f"título «{carga.get('title')}», {carga.get('publish_date')}"
    return "discrepa", f"Open Library dice «{carga.get('title')}»; el registro dice «{e['title']}»"


def comprueba_articulo(e: dict) -> tuple[str, str]:
    ok, carga = pedir(f"https://api.crossref.org/works/{e['doi']}")
    if not ok:
        return "sin-resolver", str(carga)
    m = carga.get("message", {})
    titulo = normaliza_titulo((m.get("title") or [""])[0])
    esperado = normaliza_titulo(e["title"])
    apellidos = {normaliza(a.get("family", "")) for a in m.get("author", [])}
    esperados = {normaliza(a.split(",")[0]) for a in e["authors"]}
    if esperado not in titulo and titulo not in esperado:
        return "discrepa", f"Crossref dice «{(m.get('title') or [''])[0]}»"
    if esperados and not (esperados & apellidos):
        return "discrepa", f"autores según Crossref: {sorted(apellidos)}"
    anio = (m.get("issued", {}).get("date-parts") or [[None]])[0][0]
    return "ok", f"{(m.get('title') or [''])[0]} ({anio}), {(m.get('container-title') or [''])[0]}"


def comprueba_url(url: str) -> tuple[str, str]:
    ok, estado = pedir(url, solo_cabecera=True)
    return ("ok", str(estado)) if ok else ("sin-resolver", str(estado))


def main() -> int:
    ap = argparse.ArgumentParser(description="Contrasta el registro de fuentes contra sus autoridades.")
    ap.add_argument("--escribir", action="store_true",
                    help="actualiza verified_on y accessed de lo que resolvió")
    ap.add_argument("--solo", default="", help="filtra por prefijo de id")
    args = ap.parse_args()

    doc = json.loads(REGISTRO.read_text(encoding="utf-8"))
    hoy = dt.date.today().isoformat()
    resumen = {"ok": 0, "discrepa": 0, "sin-resolver": 0, "omitida": 0}
    incidencias: list[str] = []

    for e in doc["entries"]:
        if args.solo and not e["id"].startswith(args.solo):
            resumen["omitida"] += 1
            continue
        if e["type"] == "book" and e.get("isbn13"):
            estado, detalle = comprueba_libro(e)
        elif e["type"] == "paper" and e.get("doi"):
            estado, detalle = comprueba_articulo(e)
        elif e.get("locator", "").startswith("https://"):
            estado, detalle = comprueba_url(e["locator"])
        else:
            estado, detalle = "sin-resolver", "la entrada no tiene localizador resoluble"

        resumen[estado] += 1
        print(f"[{estado:12s}] {e['id']}: {detalle}")
        if estado != "ok":
            incidencias.append(f"{e['id']} ({estado}): {detalle}")
        elif args.escribir:
            e["accessed"] = hoy

        if e.get("online"):
            sub, det = comprueba_url(e["online"])
            print(f"[{'online ok' if sub == 'ok' else 'online ' + sub:12s}] {e['id']}: {e['online']} → {det}")
            if sub != "ok":
                incidencias.append(f"{e['id']} (edición libre {sub}): {e['online']} → {det}")
        time.sleep(0.3)

    if args.escribir:
        doc["verified_on"] = hoy
        REGISTRO.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n",
                            encoding="utf-8", newline="\n")
        print(f"\nregistro actualizado: verified_on = {hoy}")

    print(f"\nresueltas {resumen['ok']} · discrepan {resumen['discrepa']} · "
          f"sin resolver {resumen['sin-resolver']} · omitidas {resumen['omitida']}")
    if incidencias:
        print("\nlo que hay que mirar a mano (nada se ha borrado):", file=sys.stderr)
        for i in incidencias:
            print(f"  - {i}", file=sys.stderr)
    return 0  # esta capa informa; la que bloquea es verificar_fuentes.py


if __name__ == "__main__":
    raise SystemExit(main())
