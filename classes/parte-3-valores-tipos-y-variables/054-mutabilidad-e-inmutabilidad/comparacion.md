# Comparación — Mutabilidad e inmutabilidad

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `'-'.join(...)` (Python), `StringBuilder` (Java/C#), `strings.Builder` (Go). |
| Semántica | Java/C#/Go usan builders mutables; Python/Rust juntan una lista al final. |
| Paradigmática | SQL usa `group_concat` sobre filas generadas, no un bucle. |

## El concepto en la familia

En Ruby `(1..n).to_a.join('-')`. En Haskell `intercalate "-" (map show [1..n])`, puramente inmutable. En C++ un `std::ostringstream`.
