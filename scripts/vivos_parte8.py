# -*- coding: utf-8 -*-
"""Parte 8 — Cómo funcionan los lenguajes: contenido de las páginas `vivos.md`.

Repartido en lotes `vivos_p8*.py`; este módulo únicamente los une.
Ver `gen_vivos.py`.
"""

from __future__ import annotations

import vivos_p8a
import vivos_p8b
import vivos_p8c
import vivos_p8d
import vivos_p8e

SPECS: dict[str, dict] = {}
for _lote in (vivos_p8a, vivos_p8b, vivos_p8c, vivos_p8d, vivos_p8e):
    SPECS.update(_lote.SPECS)
