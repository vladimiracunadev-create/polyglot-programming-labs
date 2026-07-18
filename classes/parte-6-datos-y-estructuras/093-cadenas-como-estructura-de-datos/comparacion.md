# Comparación — Cadenas como estructura de datos

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `w[::-1]` (Python), `.reverse()` sobre arreglo de chars (JS/Rust). |
| Semántica | En Rust hay que iterar por `chars()` (UTF-8); en C es por bytes. |
| Paradigmática | SQL tiene la función `reverse` en algunos motores; sqlite no de serie. |

## El concepto en la familia

En Ruby `w.reverse`. En C se intercambian los caracteres por índices, sin función incorporada.
