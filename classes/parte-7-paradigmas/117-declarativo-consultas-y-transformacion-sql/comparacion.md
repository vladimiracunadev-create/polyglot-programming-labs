# Comparación — Declarativo: consultas y transformación (SQL)

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `sum(x for x in l if x%2==0)` (Python), `filter+reduce` (JS), `WHERE+SUM` (SQL). |
| Semántica | Se describe el resultado; el cómo queda implícito. |
| Paradigmática | El imperativo recorrería y acumularía a mano. |

## El concepto en la familia

En Haskell `sum (filter even xs)`. SQL es el declarativo por excelencia.
