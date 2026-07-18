# Comparación — Rangos y secuencias

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `range(a, b+1)` (Python), `a..=b` (Rust), bucle (C/Java/Go). |
| Semántica | Python `range` es exclusivo del final; Rust distingue `..` y `..=`. |
| Paradigmática | SQL genera rangos con CTE recursivo. |

## El concepto en la familia

En Ruby `(a..b)` es inclusivo, `(a...b)` exclusivo. En Kotlin `a..b` es inclusivo.
