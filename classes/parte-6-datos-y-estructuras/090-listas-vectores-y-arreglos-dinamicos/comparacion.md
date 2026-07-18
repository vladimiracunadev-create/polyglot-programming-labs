# Comparación — Listas, vectores y arreglos dinámicos

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `list[::-1]` (Python), `.reverse()` (JS/Rust), `Collections.reverse` (Java). |
| Semántica | Algunos invierten en sitio (mutando); otros crean una lista nueva. |
| Paradigmática | SQL invierte con ORDER BY descendente sobre una posición. |

## El concepto en la familia

En Ruby `lista.reverse`. En Go se invierte con un bucle de índices intercambiando extremos.
