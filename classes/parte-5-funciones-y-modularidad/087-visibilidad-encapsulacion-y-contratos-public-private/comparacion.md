# Comparación — Visibilidad, encapsulación y contratos (public/private)

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `private`/`public` (Java/C#), `_` por convención (Python), campos en minúscula (Go = privado del paquete). |
| Semántica | Java/C#/Rust hacen cumplir la privacidad; Python confía en la convención. |
| Paradigmática | SQL encapsula con vistas y permisos. |

## El concepto en la familia

En Ruby los atributos son privados y se exponen con `attr_reader`/métodos. En Go, la mayúscula/minúscula del nombre define la visibilidad.
