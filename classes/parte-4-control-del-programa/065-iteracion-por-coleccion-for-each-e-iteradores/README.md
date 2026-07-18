# Clase 065 — Iteración por colección: for-each e iteradores

> Parte **4 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Recorrer una colección con `for-each` (para cada elemento), sin gestionar índices. Es la forma idiomática de procesar listas en casi todos los lenguajes.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Recorrer una colección con for-each.
2. Acumular un resultado sobre todos los elementos.
3. Leer una lista de longitud variable.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | for-each | Para cada elemento, sin índice |
| 2 | Colección | Una secuencia de valores |
| 3 | Acumulación | Sumar recorriendo |
| 4 | Longitud variable | No se sabe cuántos hay de antemano |

## 📖 Definiciones y características

- **for-each** — bucle que recorre cada elemento de una colección. Clave: sin índice manual.
- **Colección** — estructura que agrupa varios valores (lista, arreglo). Clave: se recorre en orden.
- **Iterar** — visitar cada elemento una vez. Clave: base del procesamiento de datos.
- **Acumulación** — reunir un resultado (suma) recorriendo. Clave: patrón universal.

## 🧩 Situación

Sumar una lista de precios, contar elementos, buscar un máximo: todo empieza recorriendo la colección. El for-each expresa 'para cada elemento' sin el ruido del índice.

## 🧮 Modelo

- **Entrada** (stdin): una línea con enteros separados por espacio
- **Salida** (stdout): `suma=<suma de todos>`
- **Regla:** suma = Σ elementos

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `3 1 4` | `suma=8` |
| `10 20 30` | `suma=60` |
| `5` | `suma=5` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER lista
suma <- 0
PARA CADA x EN lista: suma <- suma + x
ESCRIBIR "suma=" suma
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
| Sintáctica | `for x in lista` (Python) vs. `for (int x : arr)` (Java) vs. `for x in &v` (Rust). |
| Semántica | Todos recorren sin índice; C aún usa índice o puntero. |
| Paradigmática | SQL suma con `SUM()` sobre filas, sin bucle explícito. |

## 🧬 El concepto en la familia

En Ruby `lista.each` o `lista.sum`. En Go `for _, x := range xs`. Kotlin `for (x in xs)`.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 065
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Usar índice cuando no hace falta** → causa: código más largo y con más errores → solución: usar for-each cuando solo necesitas el valor
- **Olvidar inicializar el acumulador** → causa: resultado incorrecto → solución: empezar la suma en 0

## ❓ Preguntas frecuentes

- **¿for-each o for con índice?** for-each si solo necesitas el valor; con índice si también necesitas la posición.
- **¿Cómo leo una lista de tamaño desconocido?** Leyendo toda la línea/entrada y separando por espacios.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 064](../../parte-4-control-del-programa/064-iteracion-por-rango-for-clasico-y-for-range/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 066 ⏭️](../../parte-4-control-del-programa/066-iteradores-y-generadores-perezosos-lazy/README.md)
