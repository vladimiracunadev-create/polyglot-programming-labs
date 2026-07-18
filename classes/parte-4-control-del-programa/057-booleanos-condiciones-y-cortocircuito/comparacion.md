# Comparación — Booleanos, condiciones y cortocircuito

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `and` (Python) vs. `&&` (C/Java/JS/Go/Rust/PHP). |
| Semántica | Todos cortocircuitan `&&`/`and`; C# imprime True/False (normalizar). |
| Paradigmática | SQL usa AND en la expresión y CASE WHEN para el texto. |

## El concepto en la familia

En Ruby `n > 0 && n.even?`. En Haskell `n > 0 && even n`, con el mismo cortocircuito.
