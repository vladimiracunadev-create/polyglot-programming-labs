# Clase 050 — Tipado estático vs. dinámico

> Parte **3 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Ver la diferencia entre **tipado estático** (el tipo se fija y comprueba al compilar) y **dinámico** (se resuelve al ejecutar). Sumar un entero con un real obliga, en los estáticos, a una conversión explícita que en los dinámicos ocurre sola.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Sumar valores de tipos distintos (entero + real).
2. Reconocer dónde hace falta convertir explícitamente.
3. Explicar estático vs. dinámico con un ejemplo.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Tipado estático | El compilador conoce y comprueba los tipos |
| 2 | Tipado dinámico | El tipo se conoce al ejecutar |
| 3 | Promoción numérica | Entero que se convierte a real para operar |
| 4 | Errores en compilación vs. ejecución | Cuándo se detecta un tipo mal usado |

## 📖 Definiciones y características

- **Tipado estático** — los tipos se fijan y comprueban en compilación (Java, C#, Go, Rust, C). Clave: errores antes de ejecutar.
- **Tipado dinámico** — los tipos se resuelven en ejecución (Python, PHP, JS). Clave: flexible, errores más tarde.
- **Promoción** — convertir un entero a real para operar con otro real. Clave: en estáticos suele ser explícita.
- **Comprobación de tipos** — verificar que las operaciones son válidas para los tipos. Clave: estática o dinámica.

## 🧩 Situación

Sumar `2 + 3.5`: en Python simplemente da `5.5`; en Go debes convertir el entero a `float64` primero. La misma operación revela la filosofía de tipos de cada lenguaje.

## 🧮 Modelo

- **Entrada** (stdin): una línea `a b` (a entero, b real)
- **Salida** (stdout): `suma=<a+b con 2 decimales>`
- **Regla:** suma = a + b (a entero promovido a real)

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `2 3.5` | `suma=5.50` |
| `10 0.25` | `suma=10.25` |
| `0 0` | `suma=0.00` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER a (entero), b (real)
ESCRIBIR "suma=" FORMATEAR(a+b, 2)
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
| Sintáctica | Python/PHP suman directo; Go exige `float64(a)+b`. |
| Semántica | En estáticos el tipo del resultado se decide en compilación; en dinámicos, al ejecutar. |
| Paradigmática | SQL trata los números de forma uniforme en la expresión. |

## 🧬 El concepto en la familia

En Ruby `a + b` funciona por coerción numérica. En Haskell (estático fuerte) hace falta `fromIntegral a + b`, similar a Go pero más estricto.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 050
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Sumar int y float sin convertir en Go/Rust** → causa: el compilador rechaza tipos mezclados → solución: convertir el entero a real explícitamente
- **Confiar en el tipo en un dinámico** → causa: un dato inesperado rompe en ejecución → solución: validar la entrada donde el compilador no ayuda

## ❓ Preguntas frecuentes

- **¿Cuál es mejor?** Estático atrapa errores antes; dinámico itera más rápido. Depende del proyecto.
- **¿Por qué Go obliga a convertir?** Para que la promoción sea visible y no haya conversiones silenciosas.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 049](../../parte-3-valores-tipos-y-variables/049-conversion-de-tipos-casting-explicito-vs-coercion-implicita/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 051 ⏭️](../../parte-3-valores-tipos-y-variables/051-tipado-fuerte-vs-debil/README.md)
