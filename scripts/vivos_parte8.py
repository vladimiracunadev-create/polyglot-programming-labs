# -*- coding: utf-8 -*-
"""Parte 8 — Cómo funcionan los lenguajes: contenido de las páginas `vivos.md`.

Repartido en lotes `vivos_p8*.py`; este módulo únicamente los une.
Ver `gen_vivos.py`.
"""

from __future__ import annotations

import vivos_p8a

SPECS: dict[str, dict] = {}
for _lote in (vivos_p8a,):
    SPECS.update(_lote.SPECS)
