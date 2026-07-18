# Comparación — Nulabilidad: null, nil, None, Option y valores ausentes

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | Operador ternario o `if` para decidir presente/ausente. |
| Semántica | Rust modela la ausencia con `Option<T>`; Java/C con null o un centinela. |
| Paradigmática | SQL tiene `NULL` nativo y `CASE WHEN` para tratarlo. |

## El concepto en la familia

En Rust idiomático sería `Option<i64>` y un `match`. En Haskell `Maybe Int`. En Kotlin el tipo `Int?` marca la nulabilidad en el propio tipo.
