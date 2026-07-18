# Clase 053 — Nulabilidad: null, nil, None, Option y valores ausentes

> Parte **3 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Modelar la **ausencia de valor**: null, nil, None, Option. Usando 0 como centinela de 'ausente', verás cómo cada lenguaje representa y maneja la falta de un dato, y por qué las opciones tipadas (Option/Result) evitan el temido puntero nulo.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Distinguir un valor presente de uno ausente.
2. Nombrar cómo cada lenguaje representa la ausencia.
3. Explicar por qué Option/None es más seguro que null.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Ausencia de valor | No todo dato existe siempre |
| 2 | null / nil / None | Nombres del 'nada' por lenguaje |
| 3 | Option / Maybe | Ausencia tipada y segura |
| 4 | El error del billón de dólares | Los NullPointerException |

## 📖 Definiciones y características

- **Nulabilidad** — posibilidad de que un valor esté ausente. Clave: fuente clásica de errores.
- **null / nil / None** — representación de 'sin valor'. Clave: cada lenguaje lo llama distinto.
- **Option / Maybe** — tipo que envuelve 'hay valor' o 'no hay' (Rust, Haskell). Clave: obliga a manejar la ausencia.
- **Valor centinela** — un valor normal usado para significar 'ausente' (aquí, 0). Clave: sencillo pero frágil.

## 🧩 Situación

Buscar un usuario que no existe: ¿qué devuelves? null puede reventar el programa más tarde con un NullPointerException. Modelar la ausencia explícitamente (Option/None) obliga a tratarla.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n` (0 significa ausente)
- **Salida** (stdout): `valor=<n>` si hay valor, o `valor=ausente` si n es 0
- **Regla:** si n == 0 → 'ausente'; si no → n

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `5` | `valor=5` |
| `0` | `valor=ausente` |
| `42` | `valor=42` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER n
SI n == 0: ESCRIBIR "valor=ausente"
SINO: ESCRIBIR "valor=" n
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
| Sintáctica | Operador ternario o `if` para decidir presente/ausente. |
| Semántica | Rust modela la ausencia con `Option<T>`; Java/C con null o un centinela. |
| Paradigmática | SQL tiene `NULL` nativo y `CASE WHEN` para tratarlo. |

## 🧬 El concepto en la familia

En Rust idiomático sería `Option<i64>` y un `match`. En Haskell `Maybe Int`. En Kotlin el tipo `Int?` marca la nulabilidad en el propio tipo.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 053
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Usar un valor ausente como si existiera** → causa: el NullPointerException clásico → solución: comprobar la ausencia antes de usar el valor
- **Elegir un centinela que es un dato válido** → causa: 0 podría ser legítimo → solución: preferir un tipo Option explícito cuando el lenguaje lo ofrece

## ❓ Preguntas frecuentes

- **¿Por qué null es peligroso?** Se cuela sin avisar y estalla al usarlo. Los tipos Option obligan a manejarlo.
- **¿Qué lenguajes del núcleo tienen Option?** Rust (`Option`). Otros usan null/nil; Kotlin (primo JVM) marca nulabilidad en el tipo.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 052](../../parte-3-valores-tipos-y-variables/052-inferencia-de-tipos/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 054 ⏭️](../../parte-3-valores-tipos-y-variables/054-mutabilidad-e-inmutabilidad/README.md)
