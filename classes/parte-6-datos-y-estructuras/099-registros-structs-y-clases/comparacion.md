# Comparación — Registros, structs y clases

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `class`/`@dataclass` (Python), `record` (Java), `struct` (Go/Rust/C), objeto (JS). |
| Semántica | Struct suele ser por valor; clase por referencia (Java/C#). |
| Paradigmática | SQL: una fila de una tabla es un registro. |

## El concepto en la familia

En Kotlin `data class Persona(val nombre: String, val edad: Int)`. En C++ `struct Persona`.
