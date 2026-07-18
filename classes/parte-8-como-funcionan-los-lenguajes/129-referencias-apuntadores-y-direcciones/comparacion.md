# Comparación — Referencias, apuntadores y direcciones

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `arr[i]` en casi todos; en C, también `*(arr + i)`. |
| Semántica | El índice se traduce a una dirección de memoria. |
| Paradigmática | SQL accede por condición, no por índice. |

## El concepto en la familia

En C `arr[i]` y `*(arr+i)` son equivalentes: puro puntero. En los demás, el índice abstrae la dirección.
