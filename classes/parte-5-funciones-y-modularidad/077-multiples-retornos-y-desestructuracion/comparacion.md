# Comparación — Múltiples retornos y desestructuración

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `q, r = ...` (Python/Go/Rust) vs. objeto/arreglo (Java/JS). |
| Semántica | Go/Python devuelven varios valores; Java devuelve un objeto contenedor. |
| Paradigmática | SQL devuelve varias columnas por fila, un multi-retorno natural. |

## El concepto en la familia

En Ruby `return q, r` (una tupla). En Kotlin, un `Pair` o un `data class`.
