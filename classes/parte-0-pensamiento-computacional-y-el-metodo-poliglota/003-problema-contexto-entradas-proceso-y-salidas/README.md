# Clase 003 — Problema, contexto, entradas, proceso y salidas

> Parte **0 — Pensamiento computacional y el método políglota** · ⏱️ Duración estimada: **90 min** · Nivel: **Fundamentos**
> ✅ **Clase construida.**

---

## 🎯 Objetivo

Antes de escribir una línea de código hay que modelar el problema: qué entra, qué sale, bajo qué reglas y en qué contexto. Este modelo es independiente del lenguaje y es lo primero que define cada ficha del curso.

## 📚 Resultados de aprendizaje

1. Descomponer un problema en entradas, proceso y salidas.
2. Identificar el contexto y las restricciones que condicionan la solución.
3. Escribir la especificación de un problema sin mencionar ningún lenguaje.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Entradas | Qué datos recibe el programa y de qué tipo |
| 2 | Proceso | Qué transformación ocurre entre entrada y salida |
| 3 | Salidas | Qué produce y cómo se observa el resultado |
| 4 | Contexto y restricciones | Condiciones que limitan las soluciones válidas |

## 📖 Definiciones y características

- **Especificación** — descripción de qué debe hacer un programa, no cómo. Clave: neutral al lenguaje.
- **Entrada** — dato que el programa recibe. Clave: define el dominio del problema.
- **Salida** — resultado observable. Clave: es lo que se verifica con casos.json.
- **Restricción** — condición que la solución debe respetar. Clave: acota el espacio de soluciones.

## 🧩 Situación

_El problema observable que motiva esta clase._

## 🧮 Modelo

Entradas · salidas · reglas · casos límite. La especificación es neutral al lenguaje y se
verifica con [`casos.json`](casos.json).

## 📐 Algoritmo (pseudocódigo neutral)

```text
# pseudocódigo independiente del lenguaje
```

## 🌐 Implementaciones idiomáticas

Cuando esta clase se construya, aquí vivirá una implementación idiomática por lenguaje del núcleo, verificadas contra `casos.json`:

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

## 🔬 Comparación

| Clase de diferencia | Qué observar |
|---|---|
| Sintáctica | Cómo se escribe lo mismo en cada lenguaje |
| Semántica | Tipos, mutabilidad, memoria y errores |
| Paradigmática | Si el lenguaje invita a estructurar la solución de otra forma |

## 🧬 El concepto en la familia

Cómo se ve este concepto en los **primos** de cada familia (Ruby, Kotlin, Haskell, Elixir,
Lua, C++…), como _delta_ respecto del representante del núcleo. Consulta el
[Atlas](../../../atlas/README.md).

## ✅ Prueba común

Los mismos casos de entrada/salida para todas las implementaciones:
[`casos.json`](casos.json). Verifica la equivalencia con:

```bash
python scripts/verificar_equivalencia.py 003-problema-contexto-entradas-proceso-y-salidas
```

## 🧪 Reto de transferencia

Resuelve una variante en un lenguaje **no explicado paso a paso**. Detalle en
[`reto.md`](reto.md).

## ⚠️ Errores comunes

_Síntoma → causa → solución (en desarrollo)._

## ❓ Preguntas frecuentes

_En desarrollo._

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⬅️ Parte 0](../README.md) · [📚 Índice completo](../../README.md) · [🌐 Atlas de lenguajes](../../../atlas/README.md)
