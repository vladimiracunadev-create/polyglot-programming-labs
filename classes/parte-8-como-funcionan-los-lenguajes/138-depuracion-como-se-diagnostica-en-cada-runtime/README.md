# Clase 138 — Depuración: cómo se diagnostica en cada runtime

> Parte **8 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Cerrar la parte con la **depuración**: cómo se diagnostica un programa. Inspeccionar el valor de las variables (aquí, el número y sus potencias) es lo que hace un depurador al pausar la ejecución.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Inspeccionar el estado de un cálculo.
2. Explicar qué hace un depurador.
3. Nombrar los depuradores por runtime.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Depuración | Encontrar y entender fallos |
| 2 | Inspección de variables | Ver los valores en un punto |
| 3 | Puntos de ruptura | Pausar la ejecución |

## 📖 Definiciones y características

- **Depurador** — herramienta para pausar, inspeccionar y avanzar un programa (gdb, lldb, pdb). Clave: ver el estado real.
- **Punto de ruptura** — lugar donde el depurador pausa la ejecución. Clave: para inspeccionar ahí.
- **Inspección** — examinar el valor de las variables en un momento. Clave: la base del diagnóstico.

## 🧩 Situación

Cuando un resultado sorprende, se pausa en un punto de ruptura y se inspeccionan las variables. Mostrar el número, su cuadrado y su cubo simula esa inspección del estado.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n`
- **Salida** (stdout): `valor=<n> cuadrado=<n²> cubo=<n³>`
- **Regla:** inspeccionar n, n² y n³

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `3` | `valor=3 cuadrado=9 cubo=27` |
| `2` | `valor=2 cuadrado=4 cubo=8` |
| `5` | `valor=5 cuadrado=25 cubo=125` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER n ; ESCRIBIR n, n*n, n*n*n
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
| Sintáctica | Idéntica: calcular potencias. |
| Semántica | Cada runtime tiene su depurador (pdb, gdb, lldb, el del IDE). |
| Paradigmática | SQL se depura con EXPLAIN y consultas de prueba. |

## 🧬 El concepto en la familia

gdb/lldb (C/C++/Rust), pdb (Python), el depurador de la JVM y de .NET, y los integrados en los IDE.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 138
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Depurar cambiando al azar** → causa: no observar el estado → solución: inspeccionar variables en puntos clave
- **Llenar el código de prints y olvidarlos** → causa: ruido y regresiones → solución: preferir el depurador o quitar los prints al terminar

## ❓ Preguntas frecuentes

- **¿print o depurador?** El print es rápido; el depurador permite inspeccionar sin recompilar y avanzar paso a paso.
- **¿Cómo se depura SQL?** Con EXPLAIN (plan de ejecución) y consultas de prueba sobre subconjuntos.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 137](../../parte-8-como-funcionan-los-lenguajes/137-errores-de-sintaxis-de-tipos-de-enlace-y-de-ejecucion/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 139 ⏭️](../../parte-9-ingenieria-de-software-poliglota/139-pruebas-unitarias-por-lenguaje/README.md)
