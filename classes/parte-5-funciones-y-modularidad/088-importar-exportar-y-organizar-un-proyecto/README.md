# Clase 088 — Importar, exportar y organizar un proyecto

> Parte **5 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Cerrar la parte usando la **biblioteca estándar**: importar y usar funciones ya provistas por el lenguaje (aquí, valor absoluto). Organizar un proyecto también es saber qué reutilizar en vez de reescribir.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Importar una función de la biblioteca estándar.
2. Reconocer qué ya viene resuelto.
3. Explicar import/include/use en cada lenguaje.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Biblioteca estándar | Lo que trae el lenguaje |
| 2 | Importar | Traer una función incorporada |
| 3 | No reinventar | Reutilizar lo que existe |
| 4 | Organizar el proyecto | Estructura e imports |

## 📖 Definiciones y características

- **Biblioteca estándar** — conjunto de módulos incluidos con el lenguaje. Clave: funciones listas para usar.
- **Importar/incluir** — traer un módulo o cabecera (`import`, `#include`, `use`). Clave: acceder a sus funciones.
- **Valor absoluto** — distancia a cero, siempre no negativa. Clave: `abs(-5) = 5`.
- **Reutilización** — usar código existente en vez de reescribir. Clave: menos errores.

## 🧩 Situación

El valor absoluto ya está en la biblioteca estándar de todos los lenguajes. Saber importarlo y usarlo, en vez de escribir tu propio `if x<0`, es parte de organizar bien un proyecto.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n`
- **Salida** (stdout): `abs=<|n|>`
- **Regla:** abs(n) = |n|

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `-5` | `abs=5` |
| `3` | `abs=3` |
| `0` | `abs=0` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
IMPORTAR abs de la biblioteca
LEER n ; ESCRIBIR "abs=" abs(n)
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
| Sintáctica | `abs()` (Python built-in), `Math.abs` (JS/Java), `#include <stdlib.h>` (C), `n.abs()` (Rust). |
| Semántica | La función estándar maneja los casos; no hay que reimplementarla. |
| Paradigmática | SQL usa `abs()` incorporado. |

## 🧬 El concepto en la familia

En Ruby `n.abs`. En Go `math.Abs` opera con float; para enteros se usa una función propia o un condicional.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 088
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Reimplementar lo que ya existe** → causa: más código y más bugs → solución: buscar primero en la biblioteca estándar
- **Olvidar el import/include** → causa: función no encontrada → solución: importar el módulo correcto (math, stdlib)

## ❓ Preguntas frecuentes

- **¿Siempre usar la estándar?** Para lo común, sí: está probada y optimizada.
- **¿Go no tiene abs de enteros?** `math.Abs` es para float; para int se usa un condicional o una función propia.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 087](../../parte-5-funciones-y-modularidad/087-visibilidad-encapsulacion-y-contratos-public-private/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 089 ⏭️](../../parte-6-datos-y-estructuras/089-arreglos-de-tamano-fijo/README.md)
