# Clase 171 — Componente de automatización/scripting

> Parte **11 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Construir el **componente de automatización/scripting**: tareas repetitivas que se ejecutan sin intervención (limpieza, despliegue, informes). Aquí se procesan n tareas y se confirma su finalización.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Procesar un lote de tareas.
2. Confirmar la finalización.
3. Reconocer el rol de la automatización.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Automatización | Tareas sin intervención |
| 2 | Scripting | Pegamento entre componentes |
| 3 | Lote de tareas | Procesar en serie |

## 📖 Definiciones y características

- **Automatización** — ejecutar tareas repetitivas sin intervención humana. Clave: fiabilidad y ahorro de tiempo.
- **Script** — programa que orquesta o automatiza pasos. Clave: pegamento del sistema.
- **Lote** — conjunto de tareas procesadas juntas. Clave: eficiencia.

## 🧩 Situación

Un script nocturno procesa las tareas pendientes (limpiar, respaldar, notificar) y confirma su finalización. La automatización, a menudo en Python o Bash, mantiene el sistema funcionando solo.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n` (número de tareas)
- **Salida** (stdout): `tareas=<n> estado=completado`
- **Regla:** procesar n tareas y confirmar

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `5` | `tareas=5 estado=completado` |
| `0` | `tareas=0 estado=completado` |
| `3` | `tareas=3 estado=completado` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER n ; procesar n tareas ; ESCRIBIR completado
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
| Sintáctica | Formatear la salida en cada lenguaje. |
| Semántica | La automatización procesa y confirma. |
| Paradigmática | SQL automatiza con procedimientos/trabajos. |

## 🧬 El concepto en la familia

Python y Bash dominan el scripting; herramientas como cron y Airflow orquestan tareas.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 171
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Automatizar sin registrar** → causa: no saber si falló → solución: loggear el resultado de cada tarea
- **Sin manejo de errores** → causa: una tarea rota detiene todo → solución: aislar fallos y reintentar

## ❓ Preguntas frecuentes

- **¿Qué lenguaje para automatizar?** Python y Bash por su rapidez de escritura y ubicuidad.
- **¿Automatizar todo?** Lo repetitivo y propenso a error; lo puntual, a mano.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 170](../../parte-11-proyecto-integrador-poliglota/170-componente-de-datos-y-consultas-sql/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 172 ⏭️](../../parte-11-proyecto-integrador-poliglota/172-persistencia-y-almacenamiento/README.md)
