# Comparación — Manejo de errores II: resultados y valores (Result/Either/error de Go)

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `Result`/`match` (Rust) vs. `(v, err)` (Go) vs. if/else (otros). |
| Semántica | Rust/Go obligan a manejar el error; ignorarlo es visible o imposible. |
| Paradigmática | SQL usa CASE WHEN, sin tipo de error. |

## El concepto en la familia

En Haskell `Either String Int` con `case`. En Kotlin, un `sealed class` o `Result`. Es el estilo opuesto a las excepciones de la clase anterior.
