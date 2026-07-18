# Comparación — Enumeraciones y tipos algebraicos (ADT / sum types)

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `enum` con datos (Rust), sealed/record (Java/C#), etiqueta + campos (Go/C). |
| Semántica | Rust/Haskell garantizan exhaustividad; C usa una etiqueta manual. |
| Paradigmática | SQL usa una columna 'tipo' + CASE. |

## El concepto en la familia

En Haskell `data Forma = Cuadrado Int | Rectangulo Int Int`. En Kotlin, una `sealed class`.
