# -*- coding: utf-8 -*-
"""Parte 10 — Interoperabilidad: contenido de las páginas `vivos.md`.

Repartido en lotes `vivos_p10*.py`; este módulo únicamente los une.
Ver `gen_vivos.py`.
"""

from __future__ import annotations

import vivos_p10a
import vivos_p10b
import vivos_p10c

SPECS: dict[str, dict] = {}
for _lote in (vivos_p10a, vivos_p10b, vivos_p10c):
    SPECS.update(_lote.SPECS)
