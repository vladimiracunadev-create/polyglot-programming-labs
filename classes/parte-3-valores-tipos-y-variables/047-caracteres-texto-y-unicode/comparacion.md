# Comparación — Caracteres, texto y Unicode

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `ord(c)` (Python/PHP), `charCodeAt` (JS), `c as u32` (Rust). |
| Semántica | Java/C leen un byte/char; en C el carácter ya es un `int`. |
| Paradigmática | SQL usa la función `unicode(c)` sobre una columna de texto. |

## El concepto en la familia

En Ruby `c.ord`. En Haskell `Data.Char.ord c`. En C++ un `char` es directamente convertible a `int`, como en C.
