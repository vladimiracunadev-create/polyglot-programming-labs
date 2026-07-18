# Clase 134 — Tareas, corrutinas y canales

> Parte **8 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Introducir **tareas, corrutinas y canales**: en vez de compartir memoria, las tareas se comunican enviando datos por canales. Un productor envía los valores y un consumidor calcula el máximo.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Comunicar datos por un canal (concepto).
2. Separar productor de consumidor.
3. Contrastar canales con memoria compartida.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Canal | Tubería entre tareas |
| 2 | Productor/consumidor | Uno envía, otro recibe |
| 3 | Corrutina/goroutine | Tarea ligera |

## 📖 Definiciones y características

- **Canal** — conducto para enviar datos entre tareas concurrentes. Clave: comunicar sin compartir memoria.
- **Corrutina/goroutine** — tarea ligera que el runtime planifica. Clave: miles a bajo coste (Go).
- **Productor/consumidor** — un patrón: una tarea produce datos, otra los consume. Clave: se coordinan por el canal.

## 🧩 Situación

En Go, un productor manda los números por un canal y un consumidor los procesa; no comparten variables, se comunican. Calcular el máximo así modela ese flujo.

## 🧮 Modelo

- **Entrada** (stdin): una línea con enteros separados por espacio
- **Salida** (stdout): `max=<el mayor>`
- **Regla:** enviar los valores por un canal; el consumidor guarda el máximo

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `3 1 4` | `max=4` |
| `5` | `max=5` |
| `10 20 5` | `max=20` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
productor envía cada valor ; consumidor actualiza el máximo
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
| Sintáctica | canales (Go), colas/streams (otros), simple recorrido aquí. |
| Semántica | Comunicar por canal evita compartir estado mutable. |
| Paradigmática | SQL usa MAX; el motor decide el cómo. |

## 🧬 El concepto en la familia

Go (canales) y Kotlin (corrutinas + channels) son referentes; también las colas concurrentes en Java.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 134
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Bloquearse esperando un canal** → causa: deadlock → solución: cerrar el canal o usar tamaño/estructura adecuada
- **Compartir estado además del canal** → causa: condiciones de carrera → solución: comunicar solo por el canal

## ❓ Preguntas frecuentes

- **¿Canal o memoria compartida?** El canal evita muchos errores de concurrencia al no compartir estado.
- **¿Corrutina es un hilo?** Es más ligera: muchas corrutinas se multiplexan sobre pocos hilos.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 133](../../parte-8-como-funcionan-los-lenguajes/133-concurrencia-procesos-hilos-y-memoria-compartida/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 135 ⏭️](../../parte-8-como-funcionan-los-lenguajes/135-actores-y-paso-de-mensajes-modelo-beam/README.md)
