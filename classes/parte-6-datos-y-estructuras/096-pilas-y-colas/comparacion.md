# Comparación — Pilas y colas

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `append`/`pop` (Python), `push`/`shift` (JS), `Deque` (Java). |
| Semántica | La pila saca por el final; la cola por el frente. |
| Paradigmática | SQL ordena por la posición ascendente o descendente. |

## El concepto en la familia

En Go una pila/cola se hace con un slice. En C++ `std::stack` y `std::queue`.
