# Comparación — Alcance (scope) y sombreado (shadowing)

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | Bloques `{ }` (C/Java/JS/Rust) vs. indentación (Python). |
| Semántica | Rust permite `let` que sombrea; Python no tiene alcance de bloque para `if`/`for`. |
| Paradigmática | SQL usa alias/subconsultas para acotar nombres. |

## El concepto en la familia

En Kotlin y Rust el sombreado con `val`/`let` es idiomático. En Python las variables de un `if` no crean un nuevo alcance.
