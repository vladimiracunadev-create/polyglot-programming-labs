# Clase 067 — Comprensiones de listas y colecciones

> Parte **4 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Filtrar una colección con una **comprensión** (list comprehension): construir una nueva lista seleccionando elementos que cumplen una condición, de forma declarativa y compacta.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Filtrar una colección con una comprensión.
2. Expresar 'los que cumplen X' de forma declarativa.
3. Comparar la comprensión con el bucle equivalente.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Comprensión | Construir una lista describiéndola |
| 2 | Filtro | Quedarse con los que cumplen |
| 3 | Declarativo | Decir qué, no cómo |
| 4 | Comprensión vs. bucle | Más compacto y legible |

## 📖 Definiciones y características

- **Comprensión de lista** — expresión que construye una lista filtrando/transformando otra. Clave: declarativa y compacta.
- **Filtro** — condición que decide qué elementos entran. Clave: `if x % 2 == 0`.
- **Predicado** — condición booleana sobre cada elemento. Clave: define el filtro.
- **Estilo declarativo** — describir el resultado, no los pasos. Clave: menos ruido que el bucle.

## 🧩 Situación

Quedarse con los pedidos pagados, los usuarios activos, los números pares: filtrar es constante. La comprensión `[x for x in lista if x%2==0]` dice justo eso en una línea.

## 🧮 Modelo

- **Entrada** (stdin): una línea con enteros separados por espacio (al menos un par)
- **Salida** (stdout): `pares=<los pares unidos por -, en orden>`
- **Regla:** pares = [x ∈ lista : x par]

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `1 2 3 4` | `pares=2-4` |
| `10 15 20` | `pares=10-20` |
| `6 7 8` | `pares=6-8` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER lista
pares <- [x EN lista SI x es par]
ESCRIBIR "pares=" UNIR(pares, "-")
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
| Sintáctica | `[x for x in l if x%2==0]` (Python) vs. `l.filter(...)` (JS/Rust) vs. bucle (C). |
| Semántica | La comprensión crea una lista nueva; el original no cambia. |
| Paradigmática | SQL filtra con `WHERE x % 2 = 0`. |

## 🧬 El concepto en la familia

En Ruby `lista.select { |x| x.even? }`. En Haskell `[x | x <- xs, even x]`, de donde Python tomó la idea.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 067
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Modificar la lista mientras la recorres** → causa: resultados imprevisibles → solución: construir una lista nueva con la comprensión
- **Confundir filtrar con transformar** → causa: cambiar valores en vez de seleccionarlos → solución: filtrar mantiene los elementos; map los transforma

## ❓ Preguntas frecuentes

- **¿Comprensión o filter?** Equivalentes; la comprensión es más legible en Python, `filter` en JS/Rust.
- **¿Es más lento que un bucle?** No de forma significativa; suele ser igual o más rápido y más claro.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 066](../../parte-4-control-del-programa/066-iteradores-y-generadores-perezosos-lazy/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 068 ⏭️](../../parte-4-control-del-programa/068-funciones-de-orden-superior-map-filter-reduce/README.md)
