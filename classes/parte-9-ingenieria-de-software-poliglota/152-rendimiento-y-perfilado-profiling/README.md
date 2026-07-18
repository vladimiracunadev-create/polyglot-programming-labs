# Clase 152 — Rendimiento y perfilado (profiling)

> Parte **9 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Introducir el **rendimiento y el perfilado (profiling)**: medir dónde se gasta el tiempo o cuántas operaciones se hacen para optimizar con datos, no por intuición. Contar las operaciones de una suma es un perfilado en miniatura.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Contar las operaciones de un algoritmo.
2. Explicar el perfilado.
3. Relacionar operaciones con complejidad.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Perfilado | Medir dónde se gasta el coste |
| 2 | Conteo de operaciones | Cuánto trabajo se hace |
| 3 | Optimizar con datos | No por intuición |

## 📖 Definiciones y características

- **Perfilado** — medir el uso de tiempo/recursos de un programa. Clave: optimizar con evidencia.
- **Operación** — unidad de trabajo (una suma, una comparación). Clave: contarlas estima el coste.
- **Cuello de botella** — la parte que domina el coste. Clave: optimizar ahí primero.

## 🧩 Situación

Antes de optimizar, se perfila: ¿dónde se gasta el tiempo? Contar operaciones (aquí, n sumas para sumar 1..n) revela la complejidad y guía las mejoras hacia donde importan.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n` (n >= 1)
- **Salida** (stdout): `operaciones=<n> resultado=<1+...+n>`
- **Regla:** sumar 1..n contando cada suma

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `5` | `operaciones=5 resultado=15` |
| `1` | `operaciones=1 resultado=1` |
| `3` | `operaciones=3 resultado=6` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
ops <- 0 ; suma <- 0 ; PARA i de 1 a n: suma+=i ; ops++
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
| Sintáctica | Contador de operaciones en el bucle. |
| Semántica | El conteo estima el coste (O(n) aquí). |
| Paradigmática | SQL se perfila con EXPLAIN. |

## 🧬 El concepto en la familia

perf, valgrind (C), cProfile (Python), pprof (Go), el profiler de la JVM/.NET miden el rendimiento real.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 152
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Optimizar sin medir** → causa: atacar lo que no es el cuello de botella → solución: perfilar primero
- **Micro-optimizar lo irrelevante** → causa: esfuerzo desperdiciado → solución: optimizar el cuello de botella real

## ❓ Preguntas frecuentes

- **¿Contar operaciones o cronometrar?** El conteo estima la complejidad; el cronómetro mide el tiempo real.
- **¿Perfilar en desarrollo o producción?** Ambos: en desarrollo para iterar; en producción para casos reales.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 151](../../parte-9-ingenieria-de-software-poliglota/151-patrones-de-diseno-comparados-entre-lenguajes/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 153 ⏭️](../../parte-9-ingenieria-de-software-poliglota/153-seguridad-entradas-memoria-y-dependencias/README.md)
