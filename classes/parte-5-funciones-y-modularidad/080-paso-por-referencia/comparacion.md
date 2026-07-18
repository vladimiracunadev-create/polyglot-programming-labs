# Comparación — Paso por referencia

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `*p` (C/Go), `&mut` (Rust), `ref` (C#), objeto/lista (Java/JS/Python). |
| Semántica | Referencia mutable cambia el original; los primitivos por valor no. |
| Paradigmática | SQL no modifica variables: usa UPDATE sobre datos. |

## El concepto en la familia

En Ruby los objetos se pasan por referencia (de valor); los enteros no se mutan. En C++ hay referencias `&` explícitas.
