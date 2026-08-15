# -*- coding: utf-8 -*-
"""Parte 11 — Proyecto integrador poliglota: contenido de las páginas `vivos.md`.

Repartido en lotes `vivos_p11*.py`; este módulo únicamente los une.
Ver `gen_vivos.py`.
"""

from __future__ import annotations

import vivos_p11a
import vivos_p11b

SPECS: dict[str, dict] = {}
for _lote in (vivos_p11a, vivos_p11b):
    SPECS.update(_lote.SPECS)
