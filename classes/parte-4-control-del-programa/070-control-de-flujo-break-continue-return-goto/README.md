# Clase 070 — Control de flujo: break, continue, return, goto

> Parte **4 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Usar `break` para salir de un bucle en cuanto se cumple una condición. Buscar el primer divisor es el caso típico: no hace falta seguir una vez encontrado.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Salir de un bucle con break.
2. Reconocer cuándo continue u otras salidas ayudan.
3. Evitar trabajo innecesario tras encontrar lo buscado.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | break | Salir del bucle inmediatamente |
| 2 | continue | Saltar a la siguiente vuelta |
| 3 | Búsqueda con parada | Detenerse al encontrar |
| 4 | return dentro del bucle | Otra forma de salir |

## 📖 Definiciones y características

- **break** — termina el bucle inmediatamente. Clave: no sigue iterando.
- **continue** — salta al siguiente ciclo del bucle. Clave: ignora el resto de la vuelta.
- **Divisor** — número que divide a otro sin resto. Clave: el menor >1 revela si es primo.
- **goto** — salto incondicional (existe en C, desaconsejado). Clave: break/continue lo sustituyen.

## 🧩 Situación

Para saber si un número es primo, buscas su primer divisor >1: si es él mismo, es primo. En cuanto lo encuentras, `break` evita seguir dividiendo en vano.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n` (n >= 2)
- **Salida** (stdout): `primer_divisor=<el menor divisor > 1>`
- **Regla:** el menor d en [2..n] tal que n % d == 0

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `15` | `primer_divisor=3` |
| `7` | `primer_divisor=7` |
| `12` | `primer_divisor=2` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER n
PARA d de 2 a n: SI n%d==0: guardar d ; ROMPER
ESCRIBIR "primer_divisor=" d
```

## 🌐 Implementaciones idiomáticas

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`:

| Lenguaje | Archivo | Cómo ejecutar |
|---|---|---|
| Python | `implementaciones/python/main.py` | `python main.py` |
| JavaScript | `implementaciones/javascript/main.mjs` | `node main.mjs` |
| TypeScript | `implementaciones/typescript/main.ts` | `pnpm exec tsx main.ts` |
| Java | `implementaciones/java/Main.java` | `java Main.java` |
| C# | `implementaciones/csharp/Program.cs` | `dotnet run` |
| Go | `implementaciones/go/main.go` | `go run main.go` |
| Rust | `implementaciones/rust/main.rs` | `rustc main.rs -o main && ./main` |
| C | `implementaciones/c/main.c` | `cc main.c -o main && ./main` |
| SQL | `implementaciones/sql/main.sql` | `sqlite3 :memory: < main.sql` |
| PHP | `implementaciones/php/main.php` | `php main.php` |

> SQL es declarativo: no lee de stdin como los demás; su implementación muestra la misma idea sobre
> una tabla de casos, y el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `break` es igual en casi todos; C mantiene `goto` (evitar). |
| Semántica | break sale del bucle más interno; algunos lenguajes tienen break etiquetado. |
| Paradigmática | SQL evita el bucle: usa MIN sobre los divisores o una consulta. |

## 🧬 El concepto en la familia

En Ruby `break`. En Go `break` (y `break label` para bucles anidados). Rust tiene `break` que incluso puede devolver un valor.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 070
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Seguir iterando tras encontrar** → causa: trabajo desperdiciado → solución: usar break en cuanto se cumple la condición
- **Confundir break con continue** → causa: no salir cuando debías → solución: break termina el bucle; continue solo salta una vuelta

## ❓ Preguntas frecuentes

- **¿break sale de todos los bucles?** Solo del más interno; para varios, usa etiquetas (Java/Go) o reestructura.
- **¿Y goto?** Existe en C pero se evita; break/continue/return cubren casi todo de forma clara.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 069](../../parte-4-control-del-programa/069-recursion-y-recursion-de-cola/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 071 ⏭️](../../parte-4-control-del-programa/071-manejo-de-errores-i-excepciones-try-catch-finally/README.md)
