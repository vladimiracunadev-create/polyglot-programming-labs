# Comparación — Booleanos y valores de verdad

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `and/or/not` (Python) vs. `&&/\|\|/!` (C/Java/JS/Go/Rust/PHP). |
| Semántica | C# imprime `True`/`False`; C no tiene tipo bool nativo hasta C99; se normaliza a minúsculas. |
| Paradigmática | SQL usa `CASE WHEN a<>0 AND b<>0 ...` en vez de un tipo booleano nativo. |

## El concepto en la familia

En Ruby `a && b`, y `true`/`false` en minúscula por defecto. En Haskell son `&&`, `||`, `not`, con el tipo `Bool` explícito y valores `True`/`False`.
