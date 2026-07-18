# Clase 062 — Coincidencia de patrones: match / when

> Parte **4 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Usar **coincidencia de patrones** (`match`/`when`) para decidir según la forma o el rango de un valor. Es más expresiva y segura que el switch clásico: obliga a cubrir todos los casos.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Clasificar con match/when o su equivalente.
2. Usar guardas dentro de los patrones.
3. Explicar por qué el match exhaustivo es más seguro.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Coincidencia de patrones | Decidir por la forma del valor |
| 2 | Guardas en patrones | Condiciones dentro del caso |
| 3 | Exhaustividad | Cubrir todos los casos, obligatorio en Rust |
| 4 | match vs. switch | Más expresivo y sin caída |

## 📖 Definiciones y características

- **Coincidencia de patrones** — elegir una rama según la estructura o el rango de un valor. Clave: más potente que el switch.
- **Exhaustividad** — el compilador exige cubrir todos los casos (Rust). Clave: evita olvidos.
- **Guarda de patrón** — condición extra dentro de un caso (`n if n>0`). Clave: refina el patrón.
- **match** — construcción de coincidencia de patrones (Rust, Python 3.10+). Clave: sin fallthrough.

## 🧩 Situación

Clasificar el signo con `match` deja explícitos los tres casos (positivo, negativo, cero). En Rust, si olvidas uno, el programa no compila: la exhaustividad te protege.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n`
- **Salida** (stdout): `signo=<positivo|negativo|cero>`
- **Regla:** n>0→positivo; n<0→negativo; n==0→cero

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `5` | `signo=positivo` |
| `-3` | `signo=negativo` |
| `0` | `signo=cero` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER n
COINCIDIR n: (>0)->positivo ; (<0)->negativo ; (0)->cero
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
| Sintáctica | `match` con guardas (Rust/Python) vs. if/else (C/Java) que no tienen match nativo clásico. |
| Semántica | Rust exige exhaustividad; C/Java no avisan si falta un caso. |
| Paradigmática | SQL expresa la clasificación con CASE WHEN. |

## 🧬 El concepto en la familia

En Kotlin `when { n > 0 -> ... }`. En Haskell se usan guardas: `signo n | n > 0 = ...`. Todos favorecen cubrir cada caso.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 062
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Dejar un caso sin cubrir** → causa: comportamiento indefinido o error → solución: en Rust el compilador obliga; en otros, añadir el caso por defecto
- **Usar == con reales para 'cero'** → causa: imprecisión del punto flotante → solución: aquí son enteros; con reales, comparar con tolerancia

## ❓ Preguntas frecuentes

- **¿match es solo de Rust?** No: Python 3.10+ tiene `match`, Kotlin `when`, Scala `match`, Haskell guardas/patrones.
- **¿Por qué es más seguro que switch?** Puede exigir exhaustividad y no tiene fallthrough accidental.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 061](../../parte-4-control-del-programa/061-switch-case-y-fallthrough/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 063 ⏭️](../../parte-4-control-del-programa/063-iteracion-por-condicion-while-y-do-while/README.md)
