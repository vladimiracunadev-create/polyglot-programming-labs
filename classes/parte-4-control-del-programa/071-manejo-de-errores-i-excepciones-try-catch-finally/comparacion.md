# Comparación — Manejo de errores I: excepciones (try/catch/finally)

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `try/except` (Python), `try/catch` (Java/C#/JS/PHP). |
| Semántica | Java/C#/Python/PHP lanzan en /0 entero; JS da Infinity (hay que comprobar); Go/Rust no usan excepciones. |
| Paradigmática | SQL evita el error con CASE WHEN b=0. |

## El concepto en la familia

En Ruby `begin/rescue/ensure`. En Kotlin `try/catch/finally`, como Java. Go y Rust prefieren valores de error (siguiente clase).
