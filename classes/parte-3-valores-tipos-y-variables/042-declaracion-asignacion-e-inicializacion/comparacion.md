# Comparación — Declaración, asignación e inicialización

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `a, b = b, a` (Python/JS/Go/Rust) vs. `tmp=a;a=b;b=tmp;` (C/Java). |
| Semántica | La asignación múltiple evalúa el lado derecho antes de asignar; la temporal es manual. |
| Paradigmática | SQL no reasigna variables: se describe la salida intercambiando columnas. |

## El concepto en la familia

En Ruby (scripting dinámico) es `a, b = b, a`, igual que Python. En Kotlin (JVM) se usa `also` o una temporal; en Haskell no hay reasignación: se define un nuevo valor.
