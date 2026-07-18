# Comparación — Números reales: punto flotante, precisión y decimales

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `%.2f` (Python/C/Go), `toFixed(2)` (JS), `F2` (C#), `{:.2}` (Rust). |
| Semántica | El locale puede imprimir coma; se fuerza el punto (Locale.US, InvariantCulture). |
| Paradigmática | SQL formatea con `printf('%.2f', ...)` dentro de la consulta. |

## El concepto en la familia

En Ruby: `format('%.2f', x)`. En Haskell: `printf "%.2f" x` (de Text.Printf). El problema del punto flotante es idéntico en toda la familia porque todos usan IEEE 754.
