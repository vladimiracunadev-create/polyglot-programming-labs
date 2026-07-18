# Comparación — Rendimiento y perfilado (profiling)

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | Contador de operaciones en el bucle. |
| Semántica | El conteo estima el coste (O(n) aquí). |
| Paradigmática | SQL se perfila con EXPLAIN. |

## El concepto en la familia

perf, valgrind (C), cProfile (Python), pprof (Go), el profiler de la JVM/.NET miden el rendimiento real.
