# Comparación — Cadenas: representación, inmutabilidad e interpolación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `len(w)` (Python), `w.length` (JS/Java), `len(w)` (Go, bytes), `w.len()` (Rust, bytes). |
| Semántica | En Go/Rust `len` cuenta bytes; en Java/JS cuenta unidades UTF-16 (aquí ASCII: igual). |
| Paradigmática | SQL usa la función `length(w)` sobre una columna. |

## El concepto en la familia

En Ruby `w.length`. En Haskell `length w`. En C++ `w.size()`. Todos miden lo mismo en ASCII; difieren con Unicode multibyte.
