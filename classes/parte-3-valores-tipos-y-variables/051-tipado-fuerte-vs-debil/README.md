# Clase 051 — Tipado fuerte vs. débil

> Parte **3 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Distinguir **tipado fuerte** (no mezcla tipos sin permiso) de **débil** (convierte soluto). El mismo `+` puede sumar números o concatenar texto: verlo lado a lado aclara por qué `'5' + '5'` puede ser `10` o `'55'` según el lenguaje.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Diferenciar suma numérica de concatenación de texto.
2. Explicar tipado fuerte vs. débil con `+`.
3. Producir ambos resultados de forma explícita.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Suma vs. concatenación | El mismo símbolo, dos operaciones |
| 2 | Tipado fuerte | No convierte tipos sin que lo pidas |
| 3 | Tipado débil | Convierte automáticamente (a veces sorprende) |
| 4 | El operador + | Sobrecargado en muchos lenguajes |

## 📖 Definiciones y características

- **Tipado fuerte** — no permite operar entre tipos incompatibles sin conversión (Python, Java). Clave: menos sorpresas.
- **Tipado débil** — convierte tipos automáticamente para operar (PHP, JS). Clave: `'5'+5` puede dar cosas raras.
- **Concatenación** — unir dos cadenas. Clave: en muchos lenguajes también con `+`.
- **Sobrecarga de operador** — un operador con distinto significado según los tipos. Clave: `+` suma o concatena.

## 🧩 Situación

En JavaScript `'5' + 5` da `'55'` (concatena) y `'5' - 5` da `0` (resta). Esa es la marca del tipado débil. Verlo explícito evita bugs difíciles de rastrear.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n`
- **Salida** (stdout): `suma=<n+n> texto=<n concatenado consigo mismo>`
- **Regla:** suma = n + n ; texto = str(n) ++ str(n)

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `5` | `suma=10 texto=55` |
| `3` | `suma=6 texto=33` |
| `12` | `suma=24 texto=1212` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER n
ESCRIBIR "suma=" (n+n) " texto=" (TEXTO(n) ++ TEXTO(n))
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
| Sintáctica | `str(n)+str(n)` (Python) vs. `n + "" + n` (Java) vs. `$n.$n` (PHP). |
| Semántica | Python (fuerte) exige `str(n)` para concatenar; JS/PHP (débil) convierten solos. |
| Paradigmática | SQL usa `\|\|` para concatenar y `+` no existe para texto. |

## 🧬 El concepto en la familia

En Ruby (fuerte) `n.to_s + n.to_s`. En JS (débil) `n + '' + n` concatena por coerción. Haskell (muy fuerte) obliga `show n ++ show n`.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 051
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Esperar que `n + n` concatene** → causa: confundir suma con concatenación → solución: convertir a texto explícitamente para concatenar
- **Confiar en la coerción débil** → causa: resultados inesperados con `+` → solución: convertir de forma explícita para que la intención sea clara

## ❓ Preguntas frecuentes

- **¿Por qué `'5'+5` es `'55'` en JS?** Tipado débil: ante texto y número, `+` concatena convirtiendo el número a texto.
- **¿Python es fuerte o débil?** Fuerte: `'5' + 5` es un error; hay que convertir explícitamente.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 050](../../parte-3-valores-tipos-y-variables/050-tipado-estatico-vs-dinamico/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 052 ⏭️](../../parte-3-valores-tipos-y-variables/052-inferencia-de-tipos/README.md)
