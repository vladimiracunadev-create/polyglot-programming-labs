# Comparación — Paso por valor

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | Igual en todos: se llama y se recibe el retorno. |
| Semántica | Los primitivos se copian; el original nunca se altera. |
| Paradigmática | SQL no tiene variables mutables del llamador; todo es expresión. |

## El concepto en la familia

En Ruby los enteros son inmutables: se comportan como paso por valor. En Java/Go/C, los primitivos siempre se pasan por valor.
