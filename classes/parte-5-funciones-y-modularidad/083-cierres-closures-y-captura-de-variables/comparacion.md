# Comparación — Cierres (closures) y captura de variables

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `lambda`/`=>`/`\|x\|` para el cierre; C usa un puntero a función + parámetro. |
| Semántica | La mayoría captura el entorno; C no tiene cierres (se pasa el dato aparte). |
| Paradigmática | SQL no tiene cierres; se parametriza con valores en la consulta. |

## El concepto en la familia

En Ruby los bloques y `lambda` capturan el entorno. En Haskell, la aplicación parcial produce cierres de forma natural.
