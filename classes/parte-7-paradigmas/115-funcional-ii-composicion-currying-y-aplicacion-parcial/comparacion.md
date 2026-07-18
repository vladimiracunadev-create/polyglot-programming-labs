# Comparación — Funcional II: composición, currying y aplicación parcial

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | Composición explícita `inc(doblar(n))` o con operador de composición. |
| Semántica | El orden importa: doblar primero, luego incrementar. |
| Paradigmática | SQL anida funciones/expresiones. |

## El concepto en la familia

En Haskell `(inc . doblar) n` con el operador `.`. En muchos lenguajes se anidan las llamadas.
