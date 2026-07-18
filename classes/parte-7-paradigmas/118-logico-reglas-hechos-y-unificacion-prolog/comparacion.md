# Comparación — Lógico: reglas, hechos y unificación (Prolog)

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | En los del núcleo es un `if (b % a == 0)`; en Prolog, una regla. |
| Semántica | El lógico deduce; los imperativos comprueban. |
| Paradigmática | SQL (declarativo) es primo del lógico: describe condiciones. |

## El concepto en la familia

En Prolog: `es_divisor(A, B) :- 0 is B mod A.` y la consulta `?- es_divisor(3, 12).`. Datalog es un subconjunto para datos.
