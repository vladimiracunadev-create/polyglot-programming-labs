# Comparación — Coincidencia de patrones: match / when

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `match` con guardas (Rust/Python) vs. if/else (C/Java) que no tienen match nativo clásico. |
| Semántica | Rust exige exhaustividad; C/Java no avisan si falta un caso. |
| Paradigmática | SQL expresa la clasificación con CASE WHEN. |

## El concepto en la familia

En Kotlin `when { n > 0 -> ... }`. En Haskell se usan guardas: `signo n | n > 0 = ...`. Todos favorecen cubrir cada caso.
