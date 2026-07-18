# Comparación — Funcional I: inmutabilidad y funciones puras

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `map` (Python/JS/Rust), streams (Java), LINQ Select (C#). |
| Semántica | No muta la lista original; devuelve otra. |
| Paradigmática | SQL transforma en el SELECT, sin mutar. |

## El concepto en la familia

En Haskell `map (*2) xs` es el ejemplo puro. Casi todos ofrecen map.
