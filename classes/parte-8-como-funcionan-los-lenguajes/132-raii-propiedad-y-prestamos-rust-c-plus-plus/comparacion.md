# Comparación — RAII, propiedad y préstamos (Rust/C++)

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `&valor` (Rust/C++) vs. paso normal en los demás. |
| Semántica | Rust libera determinísticamente sin GC; el préstamo no copia. |
| Paradigmática | SQL no expone propiedad de memoria. |

## El concepto en la familia

C++ tiene RAII y referencias; Rust lo lleva más lejos comprobando los préstamos en compilación.
