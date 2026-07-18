# Comparación — Semántica de movimiento y préstamo (Rust)

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `&s` (préstamo) y move implícito en Rust; los demás copian o comparten referencia. |
| Semántica | Rust invalida el valor movido en compilación; con GC el valor sigue vivo mientras se use. |
| Paradigmática | SQL no tiene propiedad de memoria: opera sobre datos. |

## El concepto en la familia

C++ tiene semántica de movimiento (`std::move`) y referencias, cercana a Rust pero sin comprobación en compilación. Java/Go/Python usan GC.
