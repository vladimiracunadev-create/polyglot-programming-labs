# Comparación — Propiedad y ciclo de vida de los datos

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `Drop` (Rust), `defer` (Go), `using`/`try-with-resources` (C#/Java). |
| Semántica | Rust/C++ liberan determinísticamente; Java/Python dependen del GC salvo cierre explícito. |
| Paradigmática | SQL gestiona transacciones (COMMIT/ROLLBACK) como ciclo de vida. |

## El concepto en la familia

En C++ el destructor libera al salir del ámbito, como el `Drop` de Rust. En Python, el `with` (context manager).
