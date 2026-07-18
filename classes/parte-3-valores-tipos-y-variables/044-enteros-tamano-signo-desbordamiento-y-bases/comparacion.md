# Comparación — Enteros: tamaño, signo, desbordamiento y bases

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `f"{n:x}"` (Python), `n.toString(16)` (JS), `%x/%o/%b` (Go/Rust). |
| Semántica | C **no** tiene `%b`: el binario se genera con un bucle sobre los bits. |
| Paradigmática | SQL (sqlite) solo formatea hex con `%x`; octal y binario no son nativos. |

## El concepto en la familia

En Ruby: `n.to_s(16)`, `to_s(8)`, `to_s(2)`. En C++ se usa `std::hex`/`std::oct` con streams, pero el binario también requiere ayuda (`std::bitset`).
