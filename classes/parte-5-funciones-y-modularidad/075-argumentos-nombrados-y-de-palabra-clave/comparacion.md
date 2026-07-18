# Comparación — Argumentos nombrados y de palabra clave

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `punto(x=a, y=b)` (Python/C#) vs. posicional (Java/Go/C). |
| Semántica | Con nombres el orden es libre; sin ellos, importa la posición. |
| Paradigmática | SQL nombra las columnas, algo análogo a nombrar argumentos. |

## El concepto en la familia

En Ruby con argumentos de palabra clave: `punto(x: a, y: b)`. Kotlin permite `punto(x = a, y = b)`.
