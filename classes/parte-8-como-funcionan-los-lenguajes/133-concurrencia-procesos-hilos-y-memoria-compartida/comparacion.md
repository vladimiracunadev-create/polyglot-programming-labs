# Comparación — Concurrencia: procesos, hilos y memoria compartida

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | Un contador compartido en cada lenguaje. |
| Semántica | Con hilos reales haría falta un mutex; aquí es secuencial. |
| Paradigmática | SQL delega el paralelismo al motor. |

## El concepto en la familia

Java/C#/C++ comparten memoria entre hilos (con locks); Go y Erlang prefieren comunicar en vez de compartir.
