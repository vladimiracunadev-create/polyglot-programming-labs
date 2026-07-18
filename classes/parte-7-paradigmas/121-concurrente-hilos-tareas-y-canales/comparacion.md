# Comparación — Concurrente: hilos, tareas y canales

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | hilos (Java/C#), goroutines+canales (Go), async (Rust), workers (JS). |
| Semántica | El resultado es determinista; el orden de ejecución no. |
| Paradigmática | SQL delega el paralelismo al motor. |

## El concepto en la familia

Go (CSP con goroutines/canales) y Erlang/Elixir (actores) son los referentes de la concurrencia segura.
