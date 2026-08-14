# -*- coding: utf-8 -*-
"""Parte 5 — Funciones y modularidad: contenido de las páginas `vivos.md`.

Repartido en lotes: `vivos_p5a` (073–078), `vivos_p5b` (079–084) y
`vivos_p5c` (085–088). Este módulo únicamente los une. Ver `gen_vivos.py`.
"""

from __future__ import annotations

import vivos_p5a
import vivos_p5b
import vivos_p5c

SPECS: dict[str, dict] = {}
for _lote in (vivos_p5a, vivos_p5b, vivos_p5c):
    SPECS.update(_lote.SPECS)
