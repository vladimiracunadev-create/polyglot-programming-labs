# Clase 068 — Funciones de orden superior: map, filter, reduce

> Parte **4 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Combinar las tres funciones de orden superior clásicas: **map** (transformar cada elemento), **filter** (seleccionar) y **reduce** (combinar en un valor). Aquí se usan map y reduce sobre una lista.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Transformar una colección con map.
2. Combinar una colección con reduce.
3. Encadenar operaciones de orden superior.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | map | Transformar cada elemento |
| 2 | reduce | Combinar en un solo valor |
| 3 | Funciones de orden superior | Reciben otra función |
| 4 | Encadenar | map y luego reduce |

## 📖 Definiciones y características

- **map** — aplica una función a cada elemento y devuelve una colección nueva. Clave: transforma sin mutar.
- **reduce** — combina todos los elementos en un valor (suma, producto). Clave: acumula.
- **Función de orden superior** — recibe o devuelve otra función. Clave: base del estilo funcional.
- **Encadenamiento** — conectar operaciones (map → reduce). Clave: pipeline de datos.

## 🧩 Situación

Calcular el total de una factura con IVA: `map` aplica el IVA a cada línea y `reduce` las suma. map/filter/reduce son el lenguaje común del procesamiento de datos.

## 🧮 Modelo

- **Entrada** (stdin): una línea con enteros separados por espacio
- **Salida** (stdout): `doblados=<cada x·2 unidos por -> total=<suma de los doblados>`
- **Regla:** doblados = map(x→2x) ; total = reduce(+, doblados)

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `1 2 3` | `doblados=2-4-6 total=12` |
| `5` | `doblados=10 total=10` |
| `2 4` | `doblados=4-8 total=12` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER lista
doblados <- MAP(x -> 2x, lista)
total <- REDUCE(+, doblados)
ESCRIBIR "doblados=" UNIR(doblados,"-") " total=" total
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
| Sintáctica | `map`/`sum` (Python) vs. `.map().reduce()` (JS) vs. `.iter().map().sum()` (Rust). |
| Semántica | map/reduce no mutan la lista original; devuelven valores nuevos. |
| Paradigmática | SQL hace el 'map' en el SELECT y el 'reduce' con SUM(). |

## 🧬 El concepto en la familia

En Ruby `lista.map { |x| x*2 }.sum`. En Haskell `sum (map (*2) xs)`, el origen de este estilo.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 068
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Mutar dentro del map** → causa: efectos secundarios inesperados → solución: usar map para transformar, sin cambiar estado externo
- **Confundir map con for-each** → causa: map devuelve una colección; for-each no → solución: usar map cuando quieres el resultado transformado

## ❓ Preguntas frecuentes

- **¿reduce es lo mismo que un bucle de suma?** Sí en esencia; reduce lo expresa de forma declarativa y reutilizable.
- **¿Y filter?** Selecciona elementos; aquí no se usó, pero completa el trío map/filter/reduce.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 067](../../parte-4-control-del-programa/067-comprensiones-de-listas-y-colecciones/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 069 ⏭️](../../parte-4-control-del-programa/069-recursion-y-recursion-de-cola/README.md)
