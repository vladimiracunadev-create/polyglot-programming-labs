# Comparación — Conjuntos (sets) y unicidad

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `set(x)` (Python), `new Set` (JS), `HashSet` (Java/Rust/C#). |
| Semántica | El conjunto no garantiza orden; C lo simula con un bucle. |
| Paradigmática | SQL usa `COUNT(DISTINCT x)`. |

## El concepto en la familia

En Ruby `lista.uniq.size`. En Go, un `map[int]struct{}` hace de conjunto.
