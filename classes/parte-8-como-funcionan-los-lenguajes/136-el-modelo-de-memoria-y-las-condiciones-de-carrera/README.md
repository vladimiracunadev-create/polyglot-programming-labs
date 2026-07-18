# Clase 136 — El modelo de memoria y las condiciones de carrera

> Parte **8 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Entender el **modelo de memoria y las condiciones de carrera**: cuando dos hilos actualizan el mismo dato sin coordinación, el resultado puede corromperse. Incrementar de forma segura garantiza el valor correcto.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Explicar qué es una condición de carrera.
2. Reconocer la necesidad de sincronización.
3. Producir un conteo correcto.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Condición de carrera | Dos hilos, un dato, sin orden |
| 2 | Sección crítica | Código que solo un hilo debe ejecutar a la vez |
| 3 | Atomicidad | Operación indivisible |

## 📖 Definiciones y características

- **Condición de carrera** — el resultado depende del orden imprevisible de dos accesos concurrentes. Clave: corrompe datos.
- **Sección crítica** — código que accede a un recurso compartido y debe ejecutarse en exclusión. Clave: se protege con un lock.
- **Operación atómica** — indivisible: ocurre entera o nada. Clave: evita la carrera en incrementos.

## 🧩 Situación

Si dos hilos hacen `contador++` a la vez sin protección, pueden leer el mismo valor y perder un incremento. Un lock o una operación atómica garantiza el conteo correcto.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n` (número de incrementos)
- **Salida** (stdout): `cuenta=<n>`
- **Regla:** incrementar un contador n veces, con exclusión

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `5` | `cuenta=5` |
| `0` | `cuenta=0` |
| `3` | `cuenta=3` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
cuenta <- 0 ; REPETIR n veces (protegido): cuenta <- cuenta + 1
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
| Sintáctica | lock/mutex (Java/C#/Go), atómicos, o secuencial (aquí). |
| Semántica | Sin protección el resultado sería imprevisible con hilos reales. |
| Paradigmática | SQL usa transacciones para la consistencia. |

## 🧬 El concepto en la familia

Java (synchronized/AtomicInteger), Go (sync.Mutex/atomic), Rust (Mutex/Atomic) protegen la sección crítica.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 136
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Incrementar sin proteger** → causa: condición de carrera, conteo incorrecto → solución: usar lock o atómicos
- **Bloquear de más** → causa: cuello de botella → solución: minimizar la sección crítica

## ❓ Preguntas frecuentes

- **¿Toda variable compartida necesita lock?** Si más de un hilo la modifica, sí (o un tipo atómico).
- **¿Atómico o lock?** Atómico para operaciones simples; lock para secciones más complejas.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 135](../../parte-8-como-funcionan-los-lenguajes/135-actores-y-paso-de-mensajes-modelo-beam/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 137 ⏭️](../../parte-8-como-funcionan-los-lenguajes/137-errores-de-sintaxis-de-tipos-de-enlace-y-de-ejecucion/README.md)
