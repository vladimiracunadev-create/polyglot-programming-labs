# Comparación — Genéricos y polimorfismo paramétrico

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `<T>` (Java/C#/Rust), `[T any]` (Go), sin anotación (Python dinámico). |
| Semántica | Estáticos comprueban T al compilar; Python confía en pato (duck typing). |
| Paradigmática | SQL usa `max()` polimórfico incorporado. |

## El concepto en la familia

En Kotlin `fun <T: Comparable<T>> maxOf`. En Haskell la firma `Ord a => a -> a -> a` expresa la restricción.
