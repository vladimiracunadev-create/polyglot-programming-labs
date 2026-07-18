# Clase 043 — Tipos primitivos: enteros, reales, booleanos, caracteres

> Parte **3 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Ver los tipos primitivos en acción: el mismo número tratado como **entero**, convertido a **real** y evaluado como **booleano**. Cada lenguaje formatea y convierte de forma propia, pero el concepto de 'tipo primitivo' es universal.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Distinguir entero, real y booleano como tipos primitivos.
2. Convertir un entero a real y formatearlo con decimales.
3. Producir un valor booleano a partir de una condición.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Entero | Número sin parte fraccionaria |
| 2 | Real (punto flotante) | Número con decimales; se formatea explícitamente |
| 3 | Booleano | Verdadero o falso, resultado de una condición |
| 4 | Formato de salida | true/false y decimales difieren entre lenguajes |

## 📖 Definiciones y características

- **Tipo primitivo** — tipo básico incorporado al lenguaje (entero, real, booleano, carácter). Clave: bloque elemental de todo dato.
- **Entero** — número sin decimales, de tamaño fijo en los estáticos. Clave: aritmética exacta.
- **Real** — número en coma flotante. Clave: aproximado; se formatea con un número de decimales.
- **Booleano** — valor de verdad (verdadero/falso). Clave: gobierna las decisiones del programa.

## 🧩 Situación

Un mismo `4` puede verse como entero (`4`), como real (`4.0`) o dar lugar a un booleano (`4 es par → true`). Reconocer que el valor es uno y los tipos son lentes distintas es clave.

## 🧮 Modelo

- **Entrada** (stdin): una línea `n` (un entero)
- **Salida** (stdout): `entero=<n> real=<n con 1 decimal> par=<true|false>`
- **Regla:** real = (double) n ; par = (n módulo 2 == 0)

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `4` | `entero=4 real=4.0 par=true` |
| `7` | `entero=7 real=7.0 par=false` |
| `0` | `entero=0 real=0.0 par=true` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER n
real <- CONVERTIR_A_REAL(n)
par <- (n MOD 2 == 0)
ESCRIBIR "entero=" n " real=" FORMATEAR(real,1) " par=" par
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
| Sintáctica | El formato de real (`%.1f`, `toFixed(1)`, `F1`) y de booleano varían. |
| Semántica | C#/Go escriben `True`/`true` distinto: hay que forzar minúsculas para igualar. |
| Paradigmática | SQL expresa el booleano con `CASE WHEN`, no con un tipo booleano nativo universal. |

## 🧬 El concepto en la familia

En Ruby `4.to_f` da el real y `4.even?` el booleano. En Haskell los tipos son explícitos (`Int`, `Double`, `Bool`) y la conversión es una función (`fromIntegral`).

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 043
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Imprimir `True` con mayúscula** → causa: el `ToString` de C# capitaliza los booleanos → solución: formatear el booleano a minúsculas manualmente
- **Esperar `4` en vez de `4.0`** → causa: olvidar el formato de real → solución: formatear con el número de decimales fijado por el contrato

## ❓ Preguntas frecuentes

- **¿`4` y `4.0` son el mismo valor?** Matemáticamente sí; para el tipo del lenguaje, no: uno es entero y otro real.
- **¿Por qué C# escribe True/False?** Su `bool.ToString()` capitaliza; por eso se formatea a minúsculas para el contrato.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 042](../../parte-3-valores-tipos-y-variables/042-declaracion-asignacion-e-inicializacion/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 044 ⏭️](../../parte-3-valores-tipos-y-variables/044-enteros-tamano-signo-desbordamiento-y-bases/README.md)
