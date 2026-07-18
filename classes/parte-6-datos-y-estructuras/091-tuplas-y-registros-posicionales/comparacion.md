# Comparación — Tuplas y registros posicionales

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `(a, b)` (Python/Rust/Go pares), arreglo (JS), record (Java). |
| Semántica | Rust/Python tienen tuplas nativas; Java usa records/objetos. |
| Paradigmática | SQL: una fila con varias columnas es una tupla. |

## El concepto en la familia

En Ruby `[a, b]` funciona como tupla. En Haskell `(a, b)` es una tupla nativa con `fst`/`snd`.
