# -*- coding: utf-8 -*-
"""Parte 7 — Paradigmas: contenido de las páginas `vivos.md`.

Repartido en lotes `vivos_p7*.py`; este módulo únicamente los une.
Ver `gen_vivos.py`.
"""

from __future__ import annotations

import vivos_p7a

SPECS: dict[str, dict] = {}
for _lote in (vivos_p7a,):
    SPECS.update(_lote.SPECS)
