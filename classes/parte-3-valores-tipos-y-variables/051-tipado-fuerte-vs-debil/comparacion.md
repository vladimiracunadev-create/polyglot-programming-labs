# Comparación — Tipado fuerte vs. débil

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `str(n)+str(n)` (Python) vs. `n + "" + n` (Java) vs. `$n.$n` (PHP). |
| Semántica | Python (fuerte) exige `str(n)` para concatenar; JS/PHP (débil) convierten solos. |
| Paradigmática | SQL usa `\|\|` para concatenar y `+` no existe para texto. |

## El concepto en la familia

En Ruby (fuerte) `n.to_s + n.to_s`. En JS (débil) `n + '' + n` concatena por coerción. Haskell (muy fuerte) obliga `show n ++ show n`.
