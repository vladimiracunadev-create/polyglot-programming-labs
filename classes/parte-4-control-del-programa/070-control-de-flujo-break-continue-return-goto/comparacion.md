# Comparación — Control de flujo: break, continue, return, goto

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `break` es igual en casi todos; C mantiene `goto` (evitar). |
| Semántica | break sale del bucle más interno; algunos lenguajes tienen break etiquetado. |
| Paradigmática | SQL evita el bucle: usa MIN sobre los divisores o una consulta. |

## El concepto en la familia

En Ruby `break`. En Go `break` (y `break label` para bucles anidados). Rust tiene `break` que incluso puede devolver un valor.
