# Comparación — Recursión y recursión de cola

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `def fib` (Python), `func fib` (Go), `fn fib` (Rust) — todas se auto-invocan igual. |
| Semántica | La pila de llamadas crece con la profundidad; ojo con el desbordamiento en recursiones profundas. |
| Paradigmática | SQL expresa la recursión con un CTE recursivo, no con funciones. |

## El concepto en la familia

En Ruby `def fib(n); n < 2 ? n : fib(n-1)+fib(n-2); end`. En Haskell la recursión es el modo natural de iterar.
