# Comparación — Actores y paso de mensajes (modelo BEAM)

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | En el núcleo se simula con una función que acumula; en Elixir, un proceso real. |
| Semántica | El actor no comparte estado: recibe mensajes uno a uno. |
| Paradigmática | SQL agrega sin actores. |

## El concepto en la familia

Erlang y Elixir (BEAM) son los referentes; también Akka (JVM) y el modelo de actores en muchos frameworks.
