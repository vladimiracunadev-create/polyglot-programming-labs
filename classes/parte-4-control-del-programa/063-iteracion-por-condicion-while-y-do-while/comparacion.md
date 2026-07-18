# Comparación — Iteración por condición: while y do-while

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `while cond:` (Python) vs. `while (cond) {}` (C/Java/JS). |
| Semántica | El while comprueba antes; el do-while (C/Java/JS) al menos una vez. |
| Paradigmática | SQL evita el bucle: suma con un CTE recursivo o una fórmula. |

## El concepto en la familia

En Ruby `while i <= n`. En Go solo hay `for` (que hace de while): `for i <= n`. Rust `while i <= n`.
