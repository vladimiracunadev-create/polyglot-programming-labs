# Comparación — Tipos primitivos: enteros, reales, booleanos, caracteres

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | El formato de real (`%.1f`, `toFixed(1)`, `F1`) y de booleano varían. |
| Semántica | C#/Go escriben `True`/`true` distinto: hay que forzar minúsculas para igualar. |
| Paradigmática | SQL expresa el booleano con `CASE WHEN`, no con un tipo booleano nativo universal. |

## El concepto en la familia

En Ruby `4.to_f` da el real y `4.even?` el booleano. En Haskell los tipos son explícitos (`Int`, `Double`, `Bool`) y la conversión es una función (`fromIntegral`).
