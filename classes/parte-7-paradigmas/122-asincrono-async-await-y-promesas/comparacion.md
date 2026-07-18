# Comparación — Asíncrono: async/await y promesas

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `async/await` (JS/TS/Python/C#/Rust), goroutines+canales (Go). |
| Semántica | await no bloquea el hilo; libera para otras tareas. |
| Paradigmática | SQL no tiene async a nivel de lenguaje. |

## El concepto en la familia

JavaScript popularizó async/await; hoy está en Python, C#, Rust y otros. Go usa goroutines en su lugar.
