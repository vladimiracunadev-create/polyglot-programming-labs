# Comparación — Orientado a eventos y callbacks

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | Callback como función pasada (Python/JS/Go), delegate (C#), interfaz (Java). |
| Semántica | El emisor invoca el callback; el flujo no es lineal. |
| Paradigmática | SQL no tiene eventos; procesa datos. |

## El concepto en la familia

En JS los EventEmitter y los `addEventListener` del navegador son puro estilo de eventos.
