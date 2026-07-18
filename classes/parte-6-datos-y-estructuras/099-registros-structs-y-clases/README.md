# Clase 099 — Registros, structs y clases

> Parte **6 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Agrupar datos relacionados en un **registro/struct/clase** con campos nombrados. En vez de variables sueltas, un tipo compuesto con significado.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Definir un tipo con campos nombrados.
2. Crear una instancia y acceder a sus campos.
3. Distinguir struct de clase donde aplique.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Registro/struct | Campos nombrados juntos |
| 2 | Instancia | Un valor del tipo |
| 3 | Acceso a campos | `.nombre`, `.edad` |

## 📖 Definiciones y características

- **Registro/struct** — tipo con campos nombrados. Clave: agrupa datos relacionados.
- **Campo** — cada dato con nombre dentro del registro. Clave: `persona.edad`.
- **Instancia** — un valor concreto del tipo. Clave: `Persona("Ada", 36)`.

## 🧩 Situación

En vez de pasar `nombre` y `edad` sueltos por todas partes, un `Persona` los agrupa con significado y viaja como una sola cosa.

## 🧮 Modelo

- **Entrada** (stdin): una línea `nombre edad` (una palabra y un entero)
- **Salida** (stdout): `Persona(nombre=<nombre>, edad=<edad>)`
- **Regla:** registro con campos nombre y edad

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `Ada 36` | `Persona(nombre=Ada, edad=36)` |
| `Bo 5` | `Persona(nombre=Bo, edad=5)` |
| `Cy 99` | `Persona(nombre=Cy, edad=99)` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER nombre, edad ; crear Persona ; ESCRIBIR formateado
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
| Sintáctica | `class`/`@dataclass` (Python), `record` (Java), `struct` (Go/Rust/C), objeto (JS). |
| Semántica | Struct suele ser por valor; clase por referencia (Java/C#). |
| Paradigmática | SQL: una fila de una tabla es un registro. |

## 🧬 El concepto en la familia

En Kotlin `data class Persona(val nombre: String, val edad: Int)`. En C++ `struct Persona`.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 099
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Usar variables sueltas en vez de agrupar** → causa: datos que se desincronizan → solución: agruparlos en un registro con significado
- **Confundir struct (valor) con clase (referencia)** → causa: copias inesperadas → solución: conocer la semántica del lenguaje

## ❓ Preguntas frecuentes

- **¿Struct o clase?** Struct para datos por valor; clase para identidad y comportamiento (según el lenguaje).
- **¿Registro inmutable?** A menudo conviene: un record de Java o una data class con val.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 098](../../parte-6-datos-y-estructuras/098-grafos/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 100 ⏭️](../../parte-6-datos-y-estructuras/100-enumeraciones-y-tipos-algebraicos-adt-sum-types/README.md)
