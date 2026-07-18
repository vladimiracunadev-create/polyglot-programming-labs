# Comparación — El modelo de memoria y las condiciones de carrera

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | lock/mutex (Java/C#/Go), atómicos, o secuencial (aquí). |
| Semántica | Sin protección el resultado sería imprevisible con hilos reales. |
| Paradigmática | SQL usa transacciones para la consistencia. |

## El concepto en la familia

Java (synchronized/AtomicInteger), Go (sync.Mutex/atomic), Rust (Mutex/Atomic) protegen la sección crítica.
