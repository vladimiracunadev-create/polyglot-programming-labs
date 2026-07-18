# Clase 127 — La pila (stack) y el marco de llamada

> Parte **8 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Entender la **pila (stack) y el marco de llamada**: cada llamada a función crea un marco con sus variables; la recursión los apila. La profundidad de la recursión es cuántos marcos hay a la vez.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Reconocer la pila de llamadas.
2. Relacionar recursión con marcos apilados.
3. Explicar el desbordamiento de pila.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Pila de llamadas | Marcos de las funciones activas |
| 2 | Marco de llamada | Variables y retorno de una llamada |
| 3 | Profundidad | Cuántos marcos hay a la vez |

## 📖 Definiciones y características

- **Pila (stack)** — región de memoria para los marcos de llamada. Clave: LIFO, rápida.
- **Marco de llamada** — espacio de una llamada: parámetros, locales, dirección de retorno. Clave: se apila al llamar.
- **Desbordamiento de pila** — cuando hay demasiados marcos. Clave: recursión muy profunda lo causa.

## 🧩 Situación

Cada llamada recursiva apila un marco; sumar 1..n con recursión usa n marcos a la vez. Si n es enorme, la pila se desborda. La pila explica cómo el programa recuerda dónde volver.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n` (1 <= n <= 1000)
- **Salida** (stdout): `suma=<1+...+n> profundidad=<n>`
- **Regla:** suma recursiva; profundidad = número de marcos = n

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `5` | `suma=15 profundidad=5` |
| `3` | `suma=6 profundidad=3` |
| `1` | `suma=1 profundidad=1` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
sumar(n) = n + sumar(n-1) ; sumar(0) = 0 ; profundidad = n
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
| Sintáctica | Función recursiva en cada lenguaje. |
| Semántica | Cada llamada apila un marco; el retorno lo desapila. |
| Paradigmática | SQL usa recursión con CTE, sin pila visible. |

## 🧬 El concepto en la familia

En Haskell la recursión es el modo natural de iterar; la recursión de cola puede optimizarse a un bucle.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 127
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Recursión sin caso base** → causa: desbordamiento de pila → solución: definir el caso base
- **Recursión demasiado profunda** → causa: límite de pila → solución: usar iteración o recursión de cola para n enorme

## ❓ Preguntas frecuentes

- **¿Por qué existe la pila?** Para recordar dónde volver y los datos locales de cada llamada.
- **¿Stack o heap?** La pila guarda marcos (rápida, automática); el heap, datos de vida flexible.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 126](../../parte-8-como-funcionan-los-lenguajes/126-aot-vs-jit-costos-y-beneficios/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 128 ⏭️](../../parte-8-como-funcionan-los-lenguajes/128-el-heap-y-la-asignacion-dinamica/README.md)
