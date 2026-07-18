# Comparación — La pila (stack) y el marco de llamada

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | Función recursiva en cada lenguaje. |
| Semántica | Cada llamada apila un marco; el retorno lo desapila. |
| Paradigmática | SQL usa recursión con CTE, sin pila visible. |

## El concepto en la familia

En Haskell la recursión es el modo natural de iterar; la recursión de cola puede optimizarse a un bucle.
