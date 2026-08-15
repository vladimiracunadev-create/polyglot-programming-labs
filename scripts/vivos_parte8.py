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
import vivos_p8f
import vivos_p8g
import vivos_p8h
import vivos_p8i

SPECS: dict[str, dict] = {}
for _lote in (vivos_p8a, vivos_p8b, vivos_p8c, vivos_p8d, vivos_p8e, vivos_p8f,
              vivos_p8g, vivos_p8h, vivos_p8i):
    SPECS.update(_lote.SPECS)
