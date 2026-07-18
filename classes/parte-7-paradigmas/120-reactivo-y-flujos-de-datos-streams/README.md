# Clase 120 — Reactivo y flujos de datos (streams)

> Parte **7 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Practicar el paradigma **reactivo / de flujos (streams)**: procesar datos como una corriente que pasa por operadores (filtrar, mapear) encadenados. Aquí un flujo filtra pares y los duplica.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Encadenar operadores sobre un flujo.
2. Filtrar y transformar en pipeline.
3. Reconocer el estilo reactivo.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Flujo (stream) | Datos como corriente |
| 2 | Operadores encadenados | filter, map, … |
| 3 | Pipeline | El dato fluye por pasos |

## 📖 Definiciones y características

- **Flujo/stream** — secuencia de datos procesada por etapas. Clave: filter/map encadenados.
- **Operador** — etapa que transforma el flujo (filter, map). Clave: se encadenan.
- **Reactivo** — reaccionar a datos que llegan con el tiempo. Clave: streams y observables.

## 🧩 Situación

Procesar eventos que llegan, filas de un archivo grande o mensajes en tiempo real: el estilo de flujos encadena operadores (filtrar → transformar) sin materializar todo a la vez.

## 🧮 Modelo

- **Entrada** (stdin): una línea con enteros separados por espacio (al menos un par)
- **Salida** (stdout): `stream=<pares duplicados, unidos por ->`
- **Regla:** flujo: filtrar pares, luego map x → 2x

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `1 2 3 4` | `stream=4-8` |
| `2 4` | `stream=4-8` |
| `6 7 8` | `stream=12-16` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
flujo(lista) |> filtrar(par) |> mapear(x->2x) |> recolectar
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
| Sintáctica | `.filter().map()` (JS/Rust), Streams (Java), LINQ (C#), generadores (Python). |
| Semántica | Los operadores se encadenan; el dato fluye por el pipeline. |
| Paradigmática | SQL encadena WHERE + SELECT, un pipeline declarativo. |

## 🧬 El concepto en la familia

En Java, la API Streams; en el frontend, RxJS y observables son puro estilo reactivo.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 120
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Materializar todo en cada paso** → causa: gasto de memoria → solución: encadenar operadores perezosos cuando se pueda
- **Orden de operadores equivocado** → causa: resultado distinto → solución: filtrar antes de mapear si conviene

## ❓ Preguntas frecuentes

- **¿Stream o bucle?** El stream es más declarativo y componible; el bucle da control fino.
- **¿Reactivo es solo frontend?** No: también backend (Reactor, Akka Streams) y procesamiento de datos.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 119](../../parte-7-paradigmas/119-orientado-a-eventos-y-callbacks/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 121 ⏭️](../../parte-7-paradigmas/121-concurrente-hilos-tareas-y-canales/README.md)
