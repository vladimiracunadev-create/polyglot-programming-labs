# Clase 072 — Manejo de errores II: resultados y valores (Result/Either/error de Go)

> Parte **4 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Manejar errores con **valores** en vez de excepciones: `Result`/`Either` (Rust, Haskell), el par `(valor, error)` de Go, u `Option`. El error deja de ser un salto de flujo y pasa a ser un dato que se maneja explícitamente.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Representar el error como un valor de retorno.
2. Manejar el resultado con match o comprobación.
3. Comparar excepciones con valores de error.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Errores como valores | El error es un dato, no un salto |
| 2 | Result / Either | Éxito o fallo tipado |
| 3 | El par (valor, error) de Go | Convención idiomática |
| 4 | Manejo explícito | No se puede ignorar por accidente |

## 📖 Definiciones y características

- **Result/Either** — tipo que contiene un valor de éxito o uno de error (Rust, Haskell). Clave: obliga a manejar ambos.
- **Valor de error** — devolver el error como dato en lugar de lanzarlo. Clave: flujo explícito.
- **Convención de Go** — devolver `(valor, error)` y comprobar `if err != nil`. Clave: errores visibles.
- **Manejo explícito** — el compilador o el estilo obligan a tratar el error. Clave: menos fallos silenciosos.

## 🧩 Situación

En Go y Rust el error no se lanza: se devuelve. `func div(a,b) (int, error)` obliga a comprobar `err` antes de usar el valor. El error se vuelve visible en la firma, no una sorpresa.

## 🧮 Modelo

- **Entrada** (stdin): una línea `a b` (dos enteros)
- **Salida** (stdout): `ok=<a/b entera>` o `err=division` si b es 0
- **Regla:** si b != 0 → Ok(a/b); si b == 0 → Err(division)

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `10 2` | `ok=5` |
| `7 0` | `err=division` |
| `8 4` | `ok=2` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER a, b
res <- dividir(a,b)  // devuelve Ok(v) o Err
SEGUN res: Ok(v)->"ok="v ; Err->"err=division"
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
| Sintáctica | `Result`/`match` (Rust) vs. `(v, err)` (Go) vs. if/else (otros). |
| Semántica | Rust/Go obligan a manejar el error; ignorarlo es visible o imposible. |
| Paradigmática | SQL usa CASE WHEN, sin tipo de error. |

## 🧬 El concepto en la familia

En Haskell `Either String Int` con `case`. En Kotlin, un `sealed class` o `Result`. Es el estilo opuesto a las excepciones de la clase anterior.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 072
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Ignorar el error devuelto** → causa: usar un valor inválido → solución: comprobar siempre el error antes del valor (Go) o usar match (Rust)
- **Mezclar excepciones y valores sin criterio** → causa: manejo de errores inconsistente → solución: elegir un estilo por proyecto y ser coherente

## ❓ Preguntas frecuentes

- **¿Result o excepciones?** Result para errores esperables y explícitos; excepciones para lo verdaderamente excepcional.
- **¿Por qué Go no tiene excepciones?** Prefiere errores como valores para que el manejo sea explícito y visible.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 071](../../parte-4-control-del-programa/071-manejo-de-errores-i-excepciones-try-catch-finally/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 073 ⏭️](../../parte-5-funciones-y-modularidad/073-firma-parametros-argumentos-y-retorno/README.md)
