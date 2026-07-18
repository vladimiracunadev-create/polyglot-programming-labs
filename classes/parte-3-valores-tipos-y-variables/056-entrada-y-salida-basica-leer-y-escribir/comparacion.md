# Comparación — Entrada y salida básica: leer y escribir

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `input()`/`readline` (Python), `readFileSync(0)` (JS), `fgets` (C). |
| Semántica | Hay que quitar el salto de línea final para que el eco sea exacto. |
| Paradigmática | SQL no lee stdin: se muestra el eco sobre una tabla de textos. |

## El concepto en la familia

En Ruby `gets.chomp`. En Haskell `getLine`. En C++ `std::getline(std::cin, s)`. Todos leen una línea y recortan el salto.
