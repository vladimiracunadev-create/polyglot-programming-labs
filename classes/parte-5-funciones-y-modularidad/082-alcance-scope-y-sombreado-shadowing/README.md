# Clase 082 — Alcance (scope) y sombreado (shadowing)

> Parte **5 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Comprender el **alcance (scope)** de las variables y el **sombreado (shadowing)**: dónde vive una variable y qué pasa cuando una interna reusa el nombre de una externa. Al salir del bloque, reaparece la externa.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Explicar el alcance de bloque.
2. Predecir el efecto del sombreado.
3. Distinguir la variable interna de la externa.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Alcance (scope) | Dónde es visible una variable |
| 2 | Bloque | La región que delimita el alcance |
| 3 | Sombreado | Reusar un nombre en un bloque interno |
| 4 | Restauración | Al salir, vuelve la externa |

## 📖 Definiciones y características

- **Alcance** — región del código donde una variable es visible. Clave: de bloque en la mayoría.
- **Sombreado** — una variable interna con el mismo nombre oculta a la externa. Clave: dentro del bloque.
- **Bloque** — conjunto de sentencias con su propio alcance. Clave: `{ ... }`.
- **Vida de la variable** — cuánto existe. Clave: termina al salir de su alcance.

## 🧩 Situación

Dentro de un bloque defines `x` con el mismo nombre que una `x` externa: dentro vale lo interno, fuera vuelve lo externo. No entenderlo lleva a 'por qué mi variable no cambió'.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n`
- **Salida** (stdout): `interno=<n+10> externo=<n>`
- **Regla:** externo x = n; en un bloque interno x = n+10; al salir, x = n

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `5` | `interno=15 externo=5` |
| `0` | `interno=10 externo=0` |
| `-3` | `interno=7 externo=-3` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER n ; x <- n
BLOQUE: x_interno <- x + 10 ; imprimir interno
imprimir externo (x sigue siendo n)
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
| Sintáctica | Bloques `{ }` (C/Java/JS/Rust) vs. indentación (Python). |
| Semántica | Rust permite `let` que sombrea; Python no tiene alcance de bloque para `if`/`for`. |
| Paradigmática | SQL usa alias/subconsultas para acotar nombres. |

## 🧬 El concepto en la familia

En Kotlin y Rust el sombreado con `val`/`let` es idiomático. En Python las variables de un `if` no crean un nuevo alcance.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 082
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Creer que la interna cambió la externa** → causa: confundir sombreado con reasignación → solución: recordar que la interna es otra variable en su bloque
- **Usar una variable fuera de su alcance** → causa: error de 'no definida' → solución: declararla en el alcance donde la necesitas

## ❓ Preguntas frecuentes

- **¿Sombrear es mala práctica?** Puede confundir, pero en Rust/Kotlin es idiomático para transformar un valor manteniendo el nombre.
- **¿Python tiene alcance de bloque?** No para if/for; sí para funciones. Las variables 'se escapan' del bloque.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 081](../../parte-5-funciones-y-modularidad/081-semantica-de-movimiento-y-prestamo-rust/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 083 ⏭️](../../parte-5-funciones-y-modularidad/083-cierres-closures-y-captura-de-variables/README.md)
