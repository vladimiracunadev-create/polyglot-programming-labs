# Clase 060 — Expresiones condicionales: ternario e if como expresión

> Parte **4 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Usar el **operador ternario** o el `if` como expresión: elegir un valor en una sola línea. En Rust y Kotlin el propio `if` devuelve valor; en C/Java/JS/PHP se usa `?:`.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Elegir un valor con el operador ternario.
2. Distinguir if-sentencia de if-expresión.
3. Escribir código conciso sin perder claridad.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Ternario ?: | Elegir un valor en una expresión |
| 2 | if como expresión | En Rust/Kotlin el if devuelve valor |
| 3 | Expresión vs. sentencia | Producir un valor vs. ejecutar una acción |
| 4 | Concisión | Una línea en vez de cuatro |

## 📖 Definiciones y características

- **Operador ternario** — `cond ? a : b`: elige a o b según la condición. Clave: expresión, no sentencia.
- **Expresión** — código que produce un valor. Clave: se puede asignar.
- **Sentencia** — código que ejecuta una acción. Clave: no siempre produce valor.
- **if-expresión** — un if que devuelve un valor (Rust, Kotlin). Clave: no necesita ternario aparte.

## 🧩 Situación

`max = a > b ? a : b` dice en una línea lo que un if/else diría en cuatro. Bien usado, el ternario es claro; abusado (anidado), se vuelve ilegible.

## 🧮 Modelo

- **Entrada** (stdin): una línea `a b` (dos enteros)
- **Salida** (stdout): `max=<el mayor>`
- **Regla:** max = (a > b) ? a : b

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `3 7` | `max=7` |
| `9 2` | `max=9` |
| `5 5` | `max=5` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER a, b
max <- SI a > b ENTONCES a SINO b
ESCRIBIR "max=" max
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
| Sintáctica | `a if a>b else b` (Python) vs. `a>b ? a : b` (C/Java/JS) vs. `if a>b {a} else {b}` (Rust). |
| Semántica | Python invierte el orden; Rust/Kotlin no tienen ternario porque el if ya es expresión. |
| Paradigmática | SQL usa `CASE WHEN` o `max(a,b)` directamente. |

## 🧬 El concepto en la familia

En Ruby `a > b ? a : b`. En Kotlin `if (a > b) a else b`, como Rust: el if es una expresión.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 060
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Anidar ternarios en exceso** → causa: código ilegible → solución: usar if/else cuando hay más de dos ramas
- **Confundir el orden en Python** → causa: `a if cond else b` no es `cond ? a : b` → solución: recordar que la condición va en el medio en Python

## ❓ Preguntas frecuentes

- **¿Rust no tiene `?:`?** No: su `if` ya es una expresión que devuelve valor, así que no hace falta.
- **¿El ternario es más rápido?** No: es equivalente al if/else; es cuestión de concisión, no de velocidad.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 059](../../parte-4-control-del-programa/059-if-else-y-anidamiento/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 061 ⏭️](../../parte-4-control-del-programa/061-switch-case-y-fallthrough/README.md)
