# Reto de transferencia — Impuesto sobre el total

## Enunciado

Extiende el cálculo: después de aplicar el descuento, súmale un **impuesto (IVA) del 19 %**.

```text
subtotal   = precio_unitario * cantidad
con_desc   = subtotal * (1 - descuento)
total      = con_desc * (1 + 0.19)
ESCRIBIR "Total: " + FORMATEAR(total, 2 decimales)
```

## Contrato

- **Entrada** (stdin, una línea): `precio_unitario cantidad descuento`
- **Salida** (stdout): `Total: <total con 2 decimales>`

## Casos de aceptación

| stdin | esperado |
|---|---|
| `15000 2 0.10` | `Total: 32130.00` |
| `999.9 3 0` | `Total: 3569.64` |
| `5000 0 0.20` | `Total: 0.00` |

## Restricción de transferencia

Resuélvelo en **Kotlin**, un lenguaje **no explicado paso a paso** en esta clase. Apóyate en la
implementación de Java (misma familia JVM) y observa qué cambia:

- `val` en vez de `final` para las constantes.
- Inferencia de tipos como en Rust/Go.
- `readLine()` y `String.format(...)`.

## Criterio de evaluación

- ✅ Las tres salidas coinciden exactamente.
- ✅ La constante `IVA = 0.19` se declara como inmutable (`val`).
- ✅ El formato usa dos decimales con punto (cultura invariante).
- ✅ Explicas en un comentario qué diferencia (sintáctica/semántica) viste respecto de Java.
