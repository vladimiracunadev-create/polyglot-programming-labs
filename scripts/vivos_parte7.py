# -*- coding: utf-8 -*-
"""Parte 7 — Paradigmas: contenido de las páginas `vivos.md`.

Repartido en lotes `vivos_p7*.py`; este módulo únicamente los une.
Ver `gen_vivos.py`.
"""

from __future__ import annotations

import vivos_p7a
import vivos_p7b
import vivos_p7c
import vivos_p7d
import vivos_p7e
import vivos_p7f
import vivos_p7g
import vivos_p7h
import vivos_p7i
import vivos_p7j
import vivos_p7k
import vivos_p7l
import vivos_p7m
import vivos_p7n
import vivos_p7o
import vivos_p7p

SPECS: dict[str, dict] = {}
for _lote in (vivos_p7a, vivos_p7b, vivos_p7c, vivos_p7d, vivos_p7e, vivos_p7f,
              vivos_p7g, vivos_p7h, vivos_p7i, vivos_p7j, vivos_p7k, vivos_p7l,
              vivos_p7m, vivos_p7n, vivos_p7o, vivos_p7p):
    SPECS.update(_lote.SPECS)
