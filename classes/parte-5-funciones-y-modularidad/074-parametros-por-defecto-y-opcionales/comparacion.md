# Comparación — Parámetros por defecto y opcionales

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `def f(base, exp=2)` (Python) vs. simulación con comprobación (C/Go). |
| Semántica | Python/JS/C#/PHP tienen defectos nativos; C/Go no. |
| Paradigmática | SQL usa COALESCE para valores por defecto. |

## El concepto en la familia

En Ruby `def potencia(base, exp = 2)`. En Kotlin `fun potencia(base: Int, exp: Int = 2)`.
