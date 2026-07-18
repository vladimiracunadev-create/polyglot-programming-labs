# Comparación — Expresiones condicionales: ternario e if como expresión

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `a if a>b else b` (Python) vs. `a>b ? a : b` (C/Java/JS) vs. `if a>b {a} else {b}` (Rust). |
| Semántica | Python invierte el orden; Rust/Kotlin no tienen ternario porque el if ya es expresión. |
| Paradigmática | SQL usa `CASE WHEN` o `max(a,b)` directamente. |

## El concepto en la familia

En Ruby `a > b ? a : b`. En Kotlin `if (a > b) a else b`, como Rust: el if es una expresión.
