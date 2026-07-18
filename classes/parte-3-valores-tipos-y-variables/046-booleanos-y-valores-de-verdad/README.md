# Clase 046 — Booleanos y valores de verdad

> Parte **3 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Dominar el álgebra booleana básica: **AND** (ambos), **OR** (alguno) y **NOT** (negación). Es la base de toda condición y decisión. Cada lenguaje representa e imprime los booleanos de forma propia (`true`/`True`), lo que obliga a normalizar la salida.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Calcular AND, OR y NOT sobre valores booleanos.
2. Construir un booleano a partir de una entrada (0/1).
3. Normalizar la impresión de booleanos entre lenguajes.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | AND, OR, NOT | Las tres operaciones lógicas fundamentales |
| 2 | Representar la verdad | 0/1, true/false, según el lenguaje |
| 3 | Impresión de booleanos | true vs. True: hay que normalizar |
| 4 | Base de las condiciones | Todo if depende de un booleano |

## 📖 Definiciones y características

- **Booleano** — valor de verdad: verdadero o falso. Clave: resultado de comparaciones y condiciones.
- **AND (∧)** — verdadero solo si ambos lo son. Clave: conjunción.
- **OR (∨)** — verdadero si al menos uno lo es. Clave: disyunción.
- **NOT (¬)** — invierte el valor de verdad. Clave: negación.

## 🧩 Situación

"Si es fin de semana Y no llueve, salgo": toda decisión combina booleanos con AND/OR/NOT. Verlos aislados, con su tabla de verdad, prepara para las condiciones de la Parte 4.

## 🧮 Modelo

- **Entrada** (stdin): una línea `a b` (cada uno 0 o 1)
- **Salida** (stdout): `and=<true|false> or=<true|false> not_a=<true|false>`
- **Regla:** and = a ∧ b ; or = a ∨ b ; not_a = ¬a (con a,b interpretados como booleanos)

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `1 0` | `and=false or=true not_a=false` |
| `1 1` | `and=true or=true not_a=false` |
| `0 0` | `and=false or=false not_a=true` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER a, b
ba <- (a != 0) ; bb <- (b != 0)
ESCRIBIR "and=" (ba Y bb) " or=" (ba O bb) " not_a=" (NO ba)
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
| Sintáctica | `and/or/not` (Python) vs. `&&/\|\|/!` (C/Java/JS/Go/Rust/PHP). |
| Semántica | C# imprime `True`/`False`; C no tiene tipo bool nativo hasta C99; se normaliza a minúsculas. |
| Paradigmática | SQL usa `CASE WHEN a<>0 AND b<>0 ...` en vez de un tipo booleano nativo. |

## 🧬 El concepto en la familia

En Ruby `a && b`, y `true`/`false` en minúscula por defecto. En Haskell son `&&`, `||`, `not`, con el tipo `Bool` explícito y valores `True`/`False`.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 046
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Imprimir `True`/`False`** → causa: usar el formato por defecto de C#/Python → solución: normalizar a minúsculas con un ayudante `tf`
- **Confundir cortocircuito con bit a bit** → causa: usar `&`/`|` en vez de `&&`/`||` → solución: usar los operadores lógicos, no los de bits

## ❓ Preguntas frecuentes

- **¿`&&` y `&` son lo mismo?** No: `&&` es lógico con cortocircuito; `&` es bit a bit. Para booleanos, usa `&&`.
- **¿Qué es el cortocircuito?** En `a && b`, si `a` es falso no se evalúa `b`. Importa cuando `b` tiene efectos.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 045](../../parte-3-valores-tipos-y-variables/045-numeros-reales-punto-flotante-precision-y-decimales/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 047 ⏭️](../../parte-3-valores-tipos-y-variables/047-caracteres-texto-y-unicode/README.md)
