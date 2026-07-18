# Comparación — Inferencia de tipos

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `p = a*b` (Python), `p := a*b` (Go), `let p = a*b` (Rust), `int p = a*b` (Java/C). |
| Semántica | En Go/Rust/C# el tipo se infiere pero es fijo; en Java/C se anota. |
| Paradigmática | SQL no declara variables: la expresión produce el valor. |

## El concepto en la familia

En Kotlin `val p = a * b` infiere. En C++ `auto p = a * b`. En Haskell la inferencia (Hindley-Milner) es total: casi nunca anotas tipos.
