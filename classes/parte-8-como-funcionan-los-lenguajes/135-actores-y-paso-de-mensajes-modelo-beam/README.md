# Clase 135 — Actores y paso de mensajes (modelo BEAM)

> Parte **8 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Introducir el **modelo de actores y el paso de mensajes** (la máquina BEAM de Erlang/Elixir): actores aislados sin memoria compartida que se comunican por mensajes. Un actor acumula la suma recibiendo un mensaje por número.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Explicar el modelo de actores.
2. Simular el paso de mensajes.
3. Contrastar actores con memoria compartida.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Actor | Proceso aislado con estado propio |
| 2 | Mensaje | Única forma de comunicarse |
| 3 | Sin memoria compartida | No hay condiciones de carrera |

## 📖 Definiciones y características

- **Actor** — unidad concurrente con estado propio que solo se comunica por mensajes. Clave: aislamiento.
- **Paso de mensajes** — enviar datos a un actor en vez de compartir memoria. Clave: sin carreras.
- **BEAM** — la máquina virtual de Erlang/Elixir, optimizada para millones de actores. Clave: tolerancia a fallos.

## 🧩 Situación

En Erlang/Elixir no hay memoria compartida: cada actor tiene su estado y recibe mensajes. Un actor 'acumulador' suma cada número que le llega, sin riesgo de condiciones de carrera.

## 🧮 Modelo

- **Entrada** (stdin): una línea con enteros separados por espacio
- **Salida** (stdout): `total=<suma de todos>`
- **Regla:** cada número es un mensaje al actor; el actor acumula

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `1 2 3` | `total=6` |
| `5` | `total=5` |
| `10 20` | `total=30` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
PARA CADA número: enviar mensaje al actor ; el actor suma a su estado
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
| Sintáctica | En el núcleo se simula con una función que acumula; en Elixir, un proceso real. |
| Semántica | El actor no comparte estado: recibe mensajes uno a uno. |
| Paradigmática | SQL agrega sin actores. |

## 🧬 El concepto en la familia

Erlang y Elixir (BEAM) son los referentes; también Akka (JVM) y el modelo de actores en muchos frameworks.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 135
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Compartir estado entre actores** → causa: rompe el aislamiento → solución: comunicar solo por mensajes
- **Buzón que crece sin control** → causa: actor saturado → solución: procesar los mensajes a ritmo suficiente

## ❓ Preguntas frecuentes

- **¿Actor o hilo?** El actor no comparte memoria: se comunica por mensajes, evitando muchos errores.
- **¿Qué es 'let it crash'?** Dejar morir un actor con error y reiniciarlo desde un supervisor.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 134](../../parte-8-como-funcionan-los-lenguajes/134-tareas-corrutinas-y-canales/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 136 ⏭️](../../parte-8-como-funcionan-los-lenguajes/136-el-modelo-de-memoria-y-las-condiciones-de-carrera/README.md)
