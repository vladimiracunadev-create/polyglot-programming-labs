# Comparación — switch, case y fallthrough

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `switch` con `break` (C/Java/JS) vs. `match` (Rust) vs. `when` (Kotlin). |
| Semántica | C/Java caen sin `break`; Go, Rust y el switch de Python (match) no caen. |
| Paradigmática | SQL usa CASE WHEN valor. |

## El concepto en la familia

En Ruby `case d; when 1 then 'lunes'`. En Kotlin `when (d) { 1 -> ... }`. Ninguno cae como C.
