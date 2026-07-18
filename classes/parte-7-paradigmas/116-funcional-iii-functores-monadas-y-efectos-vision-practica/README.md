# Clase 116 — Funcional III: functores, mónadas y efectos (visión práctica)

> Parte **7 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Practicar el paradigma **funcional (III)**: functores y mónadas en su forma práctica. `Option`/`Maybe` envuelve 'hay valor' o 'no hay', y `map` aplica una función solo si hay valor, sin comprobaciones dispersas.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Envolver un valor opcional.
2. Aplicar map sobre Option (functor).
3. Explicar la ventaja frente a null.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Option/Maybe | Contenedor de 'quizá hay valor' |
| 2 | map sobre contenedor | Aplicar sin desenvolver |
| 3 | Functor | Algo sobre lo que se puede mapear |

## 📖 Definiciones y características

- **Functor** — contenedor sobre el que se puede aplicar `map` (Option, listas). Clave: transformar el contenido sin sacarlo.
- **Option/Maybe** — envuelve un valor presente (Some) o ausente (None). Clave: ausencia explícita y segura.
- **map sobre Option** — aplica la función si hay valor; si no, propaga la ausencia. Clave: sin ifs dispersos.

## 🧩 Situación

En vez de `if (x != null) usar(x)` por todas partes, `option.map(usar)` aplica la función solo si hay valor y propaga la ausencia. Menos ruido, menos errores de null.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n`
- **Salida** (stdout): `resultado=<2n>` si n>0 (hay valor), o `resultado=nada` si no
- **Regla:** Option(n si n>0).map(x → 2x)

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `5` | `resultado=10` |
| `0` | `resultado=nada` |
| `-3` | `resultado=nada` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
opcion <- Some(n) SI n>0 SINO None ; ESCRIBIR opcion.map(x->2x) o 'nada'
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
| Sintáctica | `Option`/`map` (Rust), `Optional` (Java), if/else (otros). |
| Semántica | El functor evita comprobar la ausencia en cada paso. |
| Paradigmática | SQL propaga NULL automáticamente por las operaciones. |

## 🧬 El concepto en la familia

En Haskell `fmap (*2) (Just n)`. En Kotlin, `?.let { it * 2 }` sobre un tipo nullable.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 116
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Desenvolver sin comprobar** → causa: usar un valor ausente → solución: usar map/flatMap en vez de extraer a la fuerza
- **Confundir functor con mónada** → causa: map vs. flatMap → solución: map transforma; flatMap encadena operaciones que devuelven Option

## ❓ Preguntas frecuentes

- **¿Functor o mónada?** Functor solo mapea; la mónada además encadena (flatMap). Aquí basta map.
- **¿Por qué mejor que null?** El tipo obliga a considerar la ausencia; el null se cuela silenciosamente.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 115](../../parte-7-paradigmas/115-funcional-ii-composicion-currying-y-aplicacion-parcial/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 117 ⏭️](../../parte-7-paradigmas/117-declarativo-consultas-y-transformacion-sql/README.md)
