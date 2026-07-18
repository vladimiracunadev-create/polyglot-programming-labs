# Comparación — Conversión de tipos: casting explícito vs. coerción implícita

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `int(f)` (Python), `Math.trunc` (JS), `(long)f` (Java/C/C#), `f as i64` (Rust). |
| Semántica | El truncamiento va hacia cero; no confundir con redondeo (`round`). |
| Paradigmática | SQL usa `CAST(x AS INTEGER)`. |

## El concepto en la familia

En Ruby `f.to_i` trunca. En Haskell `truncate f`. En C++ `static_cast<long>(f)`. Todos truncan hacia cero (para positivos, igual que floor).
