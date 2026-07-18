# Comparación — Iteración por colección: for-each e iteradores

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `for x in lista` (Python) vs. `for (int x : arr)` (Java) vs. `for x in &v` (Rust). |
| Semántica | Todos recorren sin índice; C aún usa índice o puntero. |
| Paradigmática | SQL suma con `SUM()` sobre filas, sin bucle explícito. |

## El concepto en la familia

En Ruby `lista.each` o `lista.sum`. En Go `for _, x := range xs`. Kotlin `for (x in xs)`.
