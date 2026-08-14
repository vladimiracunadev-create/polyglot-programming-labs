# -*- coding: utf-8 -*-
"""Parte 6 — Datos y estructuras: contenido de las páginas `vivos.md`.

Repartido en lotes: `vivos_p6a` (089–094), `vivos_p6b` (095–100) y
`vivos_p6c` (101–106). Este módulo únicamente los une. Ver `gen_vivos.py`.
"""

from __future__ import annotations

import vivos_p6a
import vivos_p6b
import vivos_p6c
import vivos_p6d
import vivos_p6e
import vivos_p6f
import vivos_p6g

SPECS: dict[str, dict] = {}
for _lote in (vivos_p6a, vivos_p6b, vivos_p6c, vivos_p6d, vivos_p6e,
              vivos_p6f, vivos_p6g):
    SPECS.update(_lote.SPECS)
