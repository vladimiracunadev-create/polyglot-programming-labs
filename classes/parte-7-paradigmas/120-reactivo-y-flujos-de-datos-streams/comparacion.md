# Comparación — Reactivo y flujos de datos (streams)

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `.filter().map()` (JS/Rust), Streams (Java), LINQ (C#), generadores (Python). |
| Semántica | Los operadores se encadenan; el dato fluye por el pipeline. |
| Paradigmática | SQL encadena WHERE + SELECT, un pipeline declarativo. |

## El concepto en la familia

En Java, la API Streams; en el frontend, RxJS y observables son puro estilo reactivo.
