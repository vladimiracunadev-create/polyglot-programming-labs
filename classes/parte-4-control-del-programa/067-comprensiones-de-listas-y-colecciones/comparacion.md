# Comparación — Comprensiones de listas y colecciones

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `[x for x in l if x%2==0]` (Python) vs. `l.filter(...)` (JS/Rust) vs. bucle (C). |
| Semántica | La comprensión crea una lista nueva; el original no cambia. |
| Paradigmática | SQL filtra con `WHERE x % 2 = 0`. |

## El concepto en la familia

En Ruby `lista.select { |x| x.even? }`. En Haskell `[x | x <- xs, even x]`, de donde Python tomó la idea.
