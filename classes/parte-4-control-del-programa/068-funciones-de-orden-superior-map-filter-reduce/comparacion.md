# Comparación — Funciones de orden superior: map, filter, reduce

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `map`/`sum` (Python) vs. `.map().reduce()` (JS) vs. `.iter().map().sum()` (Rust). |
| Semántica | map/reduce no mutan la lista original; devuelven valores nuevos. |
| Paradigmática | SQL hace el 'map' en el SELECT y el 'reduce' con SUM(). |

## El concepto en la familia

En Ruby `lista.map { |x| x*2 }.sum`. En Haskell `sum (map (*2) xs)`, el origen de este estilo.
