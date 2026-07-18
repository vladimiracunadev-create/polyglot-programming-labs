# Comparación — Gestión manual de memoria (C): malloc/free

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | malloc/free (C); las colecciones automáticas en los demás. |
| Semántica | C libera a mano; GC/ownership liberan por ti. |
| Paradigmática | SQL no expone gestión de memoria. |

## El concepto en la familia

C y C++ (con new/delete) gestionan a mano; Rust automatiza vía ownership sin GC; el resto usa GC.
