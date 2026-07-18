# Clase 069 — Recursión y recursión de cola

> Parte **4 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Escribir una función **recursiva**: que se llama a sí misma con un caso base y un caso recursivo. Fibonacci es el ejemplo clásico; también sirve para hablar de eficiencia y de recursión de cola.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Escribir una función recursiva con caso base.
2. Traducir una definición recursiva a código.
3. Reconocer el coste de la recursión ingenua.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Recursión | Una función que se llama a sí misma |
| 2 | Caso base | Dónde para la recursión |
| 3 | Caso recursivo | Reducir hacia el caso base |
| 4 | Coste | Fibonacci ingenuo es exponencial |

## 📖 Definiciones y características

- **Recursión** — técnica en que una función se invoca a sí misma. Clave: necesita un caso base.
- **Caso base** — el que se resuelve sin recursión. Clave: evita la recursión infinita.
- **Caso recursivo** — reduce el problema hacia el caso base. Clave: debe acercarse a él.
- **Recursión de cola** — la llamada recursiva es lo último que se hace. Clave: algunos lenguajes la optimizan.

## 🧩 Situación

Fibonacci se define recursivamente: F(n)=F(n-1)+F(n-2). Traducirlo a código es directo, pero la versión ingenua repite cálculos: un buen punto para hablar de eficiencia (Parte 3, clase 045 de complejidad).

## 🧮 Modelo

- **Entrada** (stdin): un entero `n` (0 <= n <= 30)
- **Salida** (stdout): `fib=<F(n)>`
- **Regla:** F(0)=0, F(1)=1, F(n)=F(n-1)+F(n-2)

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `10` | `fib=55` |
| `1` | `fib=1` |
| `0` | `fib=0` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
FUNCION fib(n): SI n<2 DEVOLVER n ; SINO DEVOLVER fib(n-1)+fib(n-2)
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
| Sintáctica | `def fib` (Python), `func fib` (Go), `fn fib` (Rust) — todas se auto-invocan igual. |
| Semántica | La pila de llamadas crece con la profundidad; ojo con el desbordamiento en recursiones profundas. |
| Paradigmática | SQL expresa la recursión con un CTE recursivo, no con funciones. |

## 🧬 El concepto en la familia

En Ruby `def fib(n); n < 2 ? n : fib(n-1)+fib(n-2); end`. En Haskell la recursión es el modo natural de iterar.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 069
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Olvidar el caso base** → causa: recursión infinita → desbordamiento de pila → solución: definir siempre el caso que corta la recursión
- **Recursión ingenua para n grande** → causa: coste exponencial → solución: usar memoización o una versión iterativa (aquí n<=30)

## ❓ Preguntas frecuentes

- **¿La recursión es peor que el bucle?** No en general; para Fibonacci ingenuo sí. Con memoización o cola, es eficiente.
- **¿Qué es la recursión de cola?** Cuando la llamada recursiva es la última operación; permite optimizarla como un bucle.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 068](../../parte-4-control-del-programa/068-funciones-de-orden-superior-map-filter-reduce/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 070 ⏭️](../../parte-4-control-del-programa/070-control-de-flujo-break-continue-return-goto/README.md)
