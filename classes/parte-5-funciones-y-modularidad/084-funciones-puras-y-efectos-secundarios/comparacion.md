# Comparación — Funciones puras y efectos secundarios

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | Idéntica en todos: una función que devuelve un cálculo. |
| Semántica | La pureza es una propiedad del diseño, no de la sintaxis. |
| Paradigmática | SQL (declarativo) y Haskell (puro) empujan hacia la pureza por defecto. |

## El concepto en la familia

En Haskell casi todo es puro; los efectos se aíslan con el tipo IO. En Rust, la pureza es una convención, no forzada.
