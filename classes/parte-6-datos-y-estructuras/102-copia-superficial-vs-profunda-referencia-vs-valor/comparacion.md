# Comparación — Copia superficial vs. profunda; referencia vs. valor

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `list(x)`/`x[:]` (Python), `[...x]` (JS), `clone()` (Rust/Java). |
| Semántica | Sin copiar, `b=a` comparte; hay que copiar explícitamente. |
| Paradigmática | SQL trabaja con conjuntos; no comparte referencias mutables. |

## El concepto en la familia

En Ruby `dup` copia superficial; en muchos lenguajes la copia profunda requiere recorrer.
