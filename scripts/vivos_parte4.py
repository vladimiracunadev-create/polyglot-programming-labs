# -*- coding: utf-8 -*-
"""Parte 4 — Control del programa: contenido de las páginas `vivos.md`.

Repartido en lotes porque cada clase lleva doce programas con su explicación:
`vivos_p4a` (057–062), `vivos_p4b` (063–068) y `vivos_p4c` (069–072).
Este módulo únicamente los une. Ver `scripts/gen_vivos.py`.
"""

from __future__ import annotations

import vivos_p4a
import vivos_p4b
import vivos_p4c

SPECS: dict[str, dict] = {}
for _lote in (vivos_p4a, vivos_p4b, vivos_p4c):
    SPECS.update(_lote.SPECS)
