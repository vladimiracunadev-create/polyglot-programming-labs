# Comparación — Funcional III: functores, mónadas y efectos (visión práctica)

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `Option`/`map` (Rust), `Optional` (Java), if/else (otros). |
| Semántica | El functor evita comprobar la ausencia en cada paso. |
| Paradigmática | SQL propaga NULL automáticamente por las operaciones. |

## El concepto en la familia

En Haskell `fmap (*2) (Just n)`. En Kotlin, `?.let { it * 2 }` sobre un tipo nullable.
