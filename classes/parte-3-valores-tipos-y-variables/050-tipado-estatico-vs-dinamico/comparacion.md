# Comparación — Tipado estático vs. dinámico

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | Python/PHP suman directo; Go exige `float64(a)+b`. |
| Semántica | En estáticos el tipo del resultado se decide en compilación; en dinámicos, al ejecutar. |
| Paradigmática | SQL trata los números de forma uniforme en la expresión. |

## El concepto en la familia

En Ruby `a + b` funciona por coerción numérica. En Haskell (estático fuerte) hace falta `fromIntegral a + b`, similar a Go pero más estricto.
