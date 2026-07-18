# Comparación — Operadores y expresiones: aritméticos, lógicos, de comparación y bit a bit

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `//` (Python) vs. `/` entre enteros (C/Java/Go); `%` en casi todos. |
| Semántica | Con negativos, el módulo difiere: Python da signo del divisor; C/Java, del dividendo. |
| Paradigmática | SQL evalúa la expresión aritmética en la propia consulta. |

## El concepto en la familia

En Ruby `a / b` es entero si ambos lo son, como C. En Haskell `div` y `mod` (y `quot`/`rem` con otra regla de signo).
