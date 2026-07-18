# Comparación — Igualdad vs. identidad

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `==` en todos para valor; identidad con `is` (Python), `===` (JS), `equals`/`==` (Java). |
| Semántica | Con primitivos, igualdad e identidad coinciden; con objetos no. |
| Paradigmática | SQL compara valores con `=`; NULL requiere `IS`. |

## El concepto en la familia

En Ruby `==` es valor y `equal?` es identidad. En C#, `==` puede sobrecargarse; `ReferenceEquals` da identidad.
