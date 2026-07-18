# Comparación — Iteradores y generadores perezosos (lazy)

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `(2*i for i in ...)` (Python) vs. `(1..=n).map(...)` (Rust) vs. bucle (C/Java). |
| Semántica | Python/Rust generan perezosamente; C/Java construyen la lista al vuelo. |
| Paradigmática | SQL genera con un CTE recursivo. |

## El concepto en la familia

En Ruby `(1..n).map { |i| i*2 }` o un `Enumerator` perezoso. En Haskell `take n [2,4..]` sobre una lista infinita.
