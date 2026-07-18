# Clase 075 — Argumentos nombrados y de palabra clave

> Parte **5 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Usar **argumentos nombrados** (por palabra clave): pasar los valores indicando a qué parámetro corresponden, mejorando la legibilidad y permitiendo cualquier orden. No todos los lenguajes los tienen.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Pasar argumentos por nombre.
2. Explicar la ventaja de legibilidad y orden libre.
3. Reconocer lenguajes sin argumentos nombrados.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Argumento nombrado | Se indica el parámetro por su nombre |
| 2 | Orden libre | No depende de la posición |
| 3 | Legibilidad | Queda claro qué es cada valor |
| 4 | Soporte por lenguaje | Python/C# sí; Java/Go no |

## 📖 Definiciones y características

- **Argumento nombrado** — se pasa indicando el parámetro (`y=4`). Clave: claridad y orden libre.
- **Argumento posicional** — se pasa por su posición. Clave: depende del orden.
- **Palabra clave** — el nombre del parámetro usado al llamar (Python `**kwargs`). Clave: base de los nombrados.
- **Legibilidad de la llamada** — entender qué es cada valor sin ver la firma. Clave: menos errores.

## 🧩 Situación

`crear(ancho=800, alto=600)` se lee mejor que `crear(800, 600)`: nadie se pregunta cuál es cuál. Los argumentos nombrados evitan confundir el orden de parámetros parecidos.

## 🧮 Modelo

- **Entrada** (stdin): una línea `a b` (dos enteros: x, y)
- **Salida** (stdout): `punto(x=<a>, y=<b>)`
- **Regla:** punto(x=a, y=b)

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `3 4` | `punto(x=3, y=4)` |
| `0 -2` | `punto(x=0, y=-2)` |
| `5 5` | `punto(x=5, y=5)` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER a, b
ESCRIBIR punto(x=a, y=b)
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
| Sintáctica | `punto(x=a, y=b)` (Python/C#) vs. posicional (Java/Go/C). |
| Semántica | Con nombres el orden es libre; sin ellos, importa la posición. |
| Paradigmática | SQL nombra las columnas, algo análogo a nombrar argumentos. |

## 🧬 El concepto en la familia

En Ruby con argumentos de palabra clave: `punto(x: a, y: b)`. Kotlin permite `punto(x = a, y = b)`.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 075
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Confiar en el orden con parámetros parecidos** → causa: intercambiar x e y → solución: usar argumentos nombrados donde el lenguaje los ofrezca
- **Asumir nombres en Java/Go** → causa: no existen → solución: documentar bien o usar objetos/structs con campos nombrados

## ❓ Preguntas frecuentes

- **¿Qué lenguajes tienen nombrados?** Python, C#, Kotlin, Ruby, Swift. Java y Go no de forma nativa.
- **¿Y si no los hay?** Se usan structs/objetos con campos nombrados para lograr claridad.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 074](../../parte-5-funciones-y-modularidad/074-parametros-por-defecto-y-opcionales/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 076 ⏭️](../../parte-5-funciones-y-modularidad/076-parametros-variadicos/README.md)
