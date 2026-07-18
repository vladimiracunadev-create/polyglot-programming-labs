# Clase 170 — Componente de datos y consultas (SQL)

> Parte **11 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Construir el **componente de datos y consultas** (SQL): la capa de persistencia responde consultas. Aquí agrega (suma) un conjunto de valores, como haría una consulta de agregación.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Agregar un conjunto de datos.
2. Explicar el rol de la capa de datos.
3. Reconocer SQL como su lenguaje.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Capa de datos | Persistencia y consultas |
| 2 | Agregación | Resumir muchos en uno |
| 3 | Consulta | Pedir datos declarativamente |

## 📖 Definiciones y características

- **Componente de datos** — la capa que almacena y consulta la información. Clave: fuente de verdad del sistema.
- **Agregación** — combinar muchas filas en un valor (SUM, AVG). Clave: resumen de datos.
- **Consulta declarativa** — describir qué datos se quieren, no cómo obtenerlos. Clave: propio de SQL.

## 🧩 Situación

El backend pide 'el total de ventas': la capa de datos ejecuta una consulta de agregación (`SELECT SUM(...)`) y devuelve el número. SQL es el lenguaje natural de este componente.

## 🧮 Modelo

- **Entrada** (stdin): una línea con enteros separados por espacio (valores a agregar)
- **Salida** (stdout): `total=<suma de los valores>`
- **Regla:** total = suma de los valores

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `10 20 30` | `total=60` |
| `5` | `total=5` |
| `1 2 3 4` | `total=10` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER valores ; total <- suma ; ESCRIBIR total
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
| Sintáctica | Suma en el núcleo; SUM en SQL. |
| Semántica | La agregación resume el conjunto. |
| Paradigmática | SQL es declarativo: SELECT SUM(x). |

## 🧬 El concepto en la familia

Bases de datos relacionales (PostgreSQL, SQLite) y sus consultas SQL dominan este componente.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 170
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Agregar en el backend lo que la BD hace mejor** → causa: traer todos los datos → solución: delegar la agregación a la base de datos
- **Consultas sin índices** → causa: lentitud → solución: indexar las columnas de filtrado/orden

## ❓ Preguntas frecuentes

- **¿Agregar en la BD o en el backend?** En la BD: es más eficiente y evita mover datos.
- **¿Por qué SQL para datos?** Es declarativo y el motor optimiza las consultas.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 169](../../parte-11-proyecto-integrador-poliglota/169-componente-web-frontend-js-ts/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 171 ⏭️](../../parte-11-proyecto-integrador-poliglota/171-componente-de-automatizacion-scripting/README.md)
