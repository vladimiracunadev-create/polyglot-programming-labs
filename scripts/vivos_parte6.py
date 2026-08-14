# -*- coding: utf-8 -*-
"""Parte 6 — Datos y estructuras: contenido de las páginas `vivos.md`.

Repartido en lotes: `vivos_p6a` (089–094), `vivos_p6b` (095–100) y
`vivos_p6c` (101–106). Este módulo únicamente los une. Ver `gen_vivos.py`.
"""

from __future__ import annotations

import vivos_p6a
import vivos_p6b

SPECS: dict[str, dict] = {}
for _lote in (vivos_p6a, vivos_p6b):
    SPECS.update(_lote.SPECS)
