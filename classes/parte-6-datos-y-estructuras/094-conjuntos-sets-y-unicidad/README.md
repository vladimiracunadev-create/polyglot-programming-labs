# Clase 094 — Conjuntos (sets) y unicidad

> Parte **6 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Usar un **conjunto (set)**: una colección sin duplicados. Contar los valores únicos es la operación natural del conjunto.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Eliminar duplicados con un conjunto.
2. Contar elementos distintos.
3. Reconocer que el conjunto no tiene orden garantizado.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Conjunto | Colección sin duplicados |
| 2 | Unicidad | Cada valor una vez |
| 3 | Pertenencia | Comprobar si algo está |

## 📖 Definiciones y características

- **Conjunto** — colección de elementos únicos (set, HashSet). Clave: sin duplicados.
- **Unicidad** — propiedad de no repetir. Clave: añadir un existente no hace nada.
- **Pertenencia** — comprobar si un elemento está, en O(1) típico. Clave: uso habitual del set.

## 🧩 Situación

¿Cuántos usuarios distintos entraron? ¿Cuántas etiquetas únicas hay? El conjunto elimina duplicados y responde al instante.

## 🧮 Modelo

- **Entrada** (stdin): una línea con enteros separados por espacio
- **Salida** (stdout): `unicos=<cantidad de valores distintos>`
- **Regla:** unicos = |conjunto(lista)|

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `1 2 2 3 3 3` | `unicos=3` |
| `5 5 5` | `unicos=1` |
| `1 2 3 4` | `unicos=4` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER lista ; conjunto <- SET(lista) ; ESCRIBIR |conjunto|
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
| Sintáctica | `set(x)` (Python), `new Set` (JS), `HashSet` (Java/Rust/C#). |
| Semántica | El conjunto no garantiza orden; C lo simula con un bucle. |
| Paradigmática | SQL usa `COUNT(DISTINCT x)`. |

## 🧬 El concepto en la familia

En Ruby `lista.uniq.size`. En Go, un `map[int]struct{}` hace de conjunto.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 094
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Asumir orden en un conjunto** → causa: esperar los elementos ordenados → solución: usar una lista/ordenar si necesitas orden
- **Contar con bucles O(n²) sin necesidad** → causa: lento en listas grandes → solución: usar un conjunto con pertenencia O(1)

## ❓ Preguntas frecuentes

- **¿El conjunto conserva el orden?** En general no; algunos lenguajes tienen variantes ordenadas.
- **¿Conjunto o lista?** Conjunto si te importa la unicidad y la pertenencia rápida.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 093](../../parte-6-datos-y-estructuras/093-cadenas-como-estructura-de-datos/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 095 ⏭️](../../parte-6-datos-y-estructuras/095-mapas-diccionarios-tablas-hash/README.md)
