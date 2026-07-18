# Clase 064 — Iteración por rango: for clásico y for-range

> Parte **4 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Usar el bucle `for` cuando el número de vueltas se conoce. El factorial multiplica de 1 a n y muestra el `for` clásico y el `for`-range de cada lenguaje.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Escribir un bucle for con contador.
2. Acumular un producto.
3. Reconocer el for-range frente al for clásico.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | for clásico | init; condición; incremento |
| 2 | for-range | Recorrer un rango directamente |
| 3 | Acumular un producto | Multiplicar en cada vuelta |
| 4 | Caso base 0! = 1 | El bucle no se ejecuta y queda 1 |

## 📖 Definiciones y características

- **for** — bucle con inicialización, condición e incremento. Clave: para un número conocido de vueltas.
- **for-range** — recorrer un rango o colección sin gestionar el índice (Python, Rust, Go). Clave: menos errores.
- **Factorial** — n! = 1·2·…·n. Clave: 0! = 1 por definición.
- **Acumulador de producto** — variable que empieza en 1 y se multiplica. Clave: 1 es el neutro del producto.

## 🧩 Situación

El factorial aparece en combinatoria y probabilidad. Con un for de 1 a n se calcula directo; el caso `0! = 1` sale gratis porque el bucle no se ejecuta y el acumulador queda en 1.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n` (0 <= n <= 20)
- **Salida** (stdout): `factorial=<n!>`
- **Regla:** n! = 1·2·…·n ; 0! = 1

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `5` | `factorial=120` |
| `1` | `factorial=1` |
| `0` | `factorial=1` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER n
f <- 1
PARA i de 1 a n: f <- f*i
ESCRIBIR "factorial=" f
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
| Sintáctica | `for i in range(1,n+1)` (Python) vs. `for(i=1;i<=n;i++)` (C/Java) vs. `for i in 1..=n` (Rust). |
| Semántica | El for-range evita el error de límites; el for clásico lo deja en tus manos. |
| Paradigmática | SQL usa un CTE recursivo o una agregación, no un for. |

## 🧬 El concepto en la familia

En Ruby `(1..n).reduce(1, :*)`. En Go `for i := 1; i <= n; i++`. Kotlin `for (i in 1..n)`.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 064
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Empezar el acumulador en 0** → causa: el producto siempre da 0 → solución: iniciar el acumulador de producto en 1
- **Límites del rango mal** → causa: un factor de más o de menos → solución: verificar con 0! y 1! que el rango es correcto

## ❓ Preguntas frecuentes

- **¿Por qué long y no int?** El factorial crece muy rápido; 21! ya desborda 64 bits. Aquí n<=20.
- **¿0! por qué es 1?** Es el producto vacío: el neutro de la multiplicación es 1.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 063](../../parte-4-control-del-programa/063-iteracion-por-condicion-while-y-do-while/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 065 ⏭️](../../parte-4-control-del-programa/065-iteracion-por-coleccion-for-each-e-iteradores/README.md)
