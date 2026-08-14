# -*- coding: utf-8 -*-
"""Parte 3 — Valores, tipos y variables: contenido de las páginas `vivos.md`.

El material se reparte en lotes (`vivos_p3a`, `vivos_p3b`, `vivos_p3c`) porque
cada clase lleva doce programas con su explicación y un solo fichero se vuelve
inmanejable. Este módulo únicamente los une.

La clase 041 no está aquí: su `vivos.md` se escribió a mano como página de
referencia del formato.
"""

from __future__ import annotations

import vivos_p3a
import vivos_p3b
import vivos_p3c

SPECS: dict[str, dict] = {}
for _lote in (vivos_p3a, vivos_p3b, vivos_p3c):
    SPECS.update(_lote.SPECS)
