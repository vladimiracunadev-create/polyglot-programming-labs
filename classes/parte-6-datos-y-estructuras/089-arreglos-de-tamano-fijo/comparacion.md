# Comparación — Arreglos de tamaño fijo

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `[a, b, c]` (Python/JS), `int[]` (Java/C#), `[i64; 3]` (Rust), `long[3]` (C). |
| Semántica | En C el tamaño es parte del tipo; en Python/JS el arreglo es dinámico. |
| Paradigmática | SQL agrega sobre filas, no índices. |

## El concepto en la familia

En Go `[3]int` es fijo y `[]int` es slice dinámico. En C++ `std::array<int,3>`.
