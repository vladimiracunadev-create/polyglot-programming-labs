# Comparación — Funciones de primera clase y como valores

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | Pasar `suma` directamente (Python/JS/Go/Rust) vs. puntero a función (C) o interfaz funcional (Java). |
| Semántica | La función es un valor; se invoca con `f(a, b)`. |
| Paradigmática | SQL no pasa funciones; usa operadores/funciones incorporadas. |

## El concepto en la familia

En Ruby se pasan `Proc`/bloques o `method(:suma)`. En Haskell pasar funciones es lo más natural del lenguaje.
