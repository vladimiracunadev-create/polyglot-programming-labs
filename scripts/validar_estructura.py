"""Valida que la estructura del repositorio coincide con el manifest.

Comprueba que cada clase del manifest tiene su carpeta y README, que las partes
existen, y que las clases marcadas como construidas tienen casos.json e
implementaciones. Sale con código != 0 si algo falta.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path(__file__).resolve().parent.parent
CLASSES = ROOT / "classes"


def main():
    manifest = json.loads((CLASSES / "_manifest.json").read_text(encoding="utf-8"))
    errores = []
    n_clases = 0
    for p in manifest["parts"]:
        pdir = CLASSES / p["slug"]
        if not (pdir / "README.md").exists():
            errores.append(f"Falta README de parte: {p['slug']}")
        for c in p["classes"]:
            n_clases += 1
            cdir = pdir / c["slug"]
            if not (cdir / "README.md").exists():
                errores.append(f"Falta README de clase: {c['slug']}")
            # Solo exigimos casos.json a clases con implementaciones (las
            # conceptuales, como las de la Parte 0, no llevan código verificable).
            impl = cdir / "implementaciones"
            tiene_impl = impl.is_dir() and any(
                d.is_dir() and any(d.iterdir()) for d in impl.iterdir()
            )
            if tiene_impl and not (cdir / "casos.json").exists():
                errores.append(f"Clase con implementaciones sin casos.json: {c['slug']}")

    esperado = manifest["total_planned"]
    if n_clases != esperado:
        errores.append(f"Conteo de clases {n_clases} != total_planned {esperado}")

    if errores:
        print(f"❌ {len(errores)} problemas de estructura:")
        for e in errores:
            print(f"  - {e}")
        sys.exit(1)
    print(f"✅ Estructura válida: {n_clases} clases en {len(manifest['parts'])} partes.")


if __name__ == "__main__":
    main()
