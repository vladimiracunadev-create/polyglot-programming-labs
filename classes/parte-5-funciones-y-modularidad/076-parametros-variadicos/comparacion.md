# Comparación — Parámetros variádicos

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `*nums` (Python), `...nums` (JS/Java), `nums ...int` (Go), `&[i64]` (Rust). |
| Semántica | Los argumentos se recolectan en una colección dentro de la función. |
| Paradigmática | SQL agrega filas con SUM(), no argumentos. |

## El concepto en la familia

En Ruby `def suma(*nums)`. En C, `stdarg.h` con `va_list` (más manual).
