# Comparación — Guardas y validación temprana

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `if ...: return` (Python) vs. `if (...) { return; }` (C/Java). |
| Semántica | El orden de las guardas define la clasificación; cambiarlo cambia el resultado. |
| Paradigmática | SQL encadena condiciones con CASE WHEN en orden. |

## El concepto en la familia

En Ruby `return 'invalido' if edad < 0`. En Go es común la guarda con `if ...{ return }` al inicio de la función.
