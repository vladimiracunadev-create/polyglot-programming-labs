# -*- coding: utf-8 -*-
"""Parte 9 — Ingeniería de software poliglota: contenido de las páginas `vivos.md`.

Repartido en lotes `vivos_p9*.py`; este módulo únicamente los une.
Ver `gen_vivos.py`.
"""

from __future__ import annotations

import vivos_p9a
import vivos_p9b

SPECS: dict[str, dict] = {}
for _lote in (vivos_p9a, vivos_p9b):
    SPECS.update(_lote.SPECS)
