# Comparación — Recolección de basura (GC)

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | No hay free: se crean objetos y se olvidan. |
| Semántica | GC (Java/Python/Go) vs. ownership (Rust) vs. manual (C). |
| Paradigmática | SQL no expone memoria. |

## El concepto en la familia

Java, C#, Go, Python, JS usan GC. Rust evita el GC con ownership; C es manual.
