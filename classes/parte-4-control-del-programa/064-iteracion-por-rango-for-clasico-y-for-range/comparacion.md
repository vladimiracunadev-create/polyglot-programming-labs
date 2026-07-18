# Comparación — Iteración por rango: for clásico y for-range

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `for i in range(1,n+1)` (Python) vs. `for(i=1;i<=n;i++)` (C/Java) vs. `for i in 1..=n` (Rust). |
| Semántica | El for-range evita el error de límites; el for clásico lo deja en tus manos. |
| Paradigmática | SQL usa un CTE recursivo o una agregación, no un for. |

## El concepto en la familia

En Ruby `(1..n).reduce(1, :*)`. En Go `for i := 1; i <= n; i++`. Kotlin `for (i in 1..n)`.
