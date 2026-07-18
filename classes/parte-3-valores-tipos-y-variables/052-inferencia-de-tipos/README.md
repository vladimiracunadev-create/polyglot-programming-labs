# Clase 052 — Inferencia de tipos

> Parte **3 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Ver la **inferencia de tipos**: el compilador deduce el tipo sin que lo anotes. Un producto de dos enteros basta para comparar `x = a*b` (Python), `var`/`:=` (C#/Go), `let` (Rust) frente a la anotación explícita de Java o C.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Reconocer dónde el lenguaje infiere el tipo.
2. Comparar inferencia con anotación explícita.
3. Escribir el mismo cálculo con y sin anotar tipos.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Inferencia | El compilador deduce el tipo del valor |
| 2 | Anotación explícita | El programador escribe el tipo |
| 3 | var/:=/let | Palabras de inferencia por lenguaje |
| 4 | Inferencia no es dinámico | El tipo sigue siendo fijo, solo no se escribe |

## 📖 Definiciones y características

- **Inferencia de tipos** — el compilador deduce el tipo a partir del valor. Clave: menos ruido, mismo tipado estático.
- **Anotación de tipo** — escribir el tipo explícitamente (`int x`). Clave: obligatoria donde no hay inferencia.
- **var / := / let** — formas de declarar con inferencia (C#, Go, Rust). Clave: el tipo se fija igual.
- **Estático con inferencia** — tipos fijos que no hace falta anotar. Clave: no confundir con dinámico.

## 🧩 Situación

`var total = a * b;` en C# infiere que `total` es entero. No es tipado dinámico: el tipo es fijo, solo no lo escribiste. Distinguir inferencia de dinamismo evita malentendidos.

## 🧮 Modelo

- **Entrada** (stdin): una línea `a b` (dos enteros)
- **Salida** (stdout): `producto=<a*b>`
- **Regla:** producto = a * b

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `3 4` | `producto=12` |
| `0 9` | `producto=0` |
| `-2 5` | `producto=-10` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER a, b
ESCRIBIR "producto=" (a*b)
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
| Sintáctica | `p = a*b` (Python), `p := a*b` (Go), `let p = a*b` (Rust), `int p = a*b` (Java/C). |
| Semántica | En Go/Rust/C# el tipo se infiere pero es fijo; en Java/C se anota. |
| Paradigmática | SQL no declara variables: la expresión produce el valor. |

## 🧬 El concepto en la familia

En Kotlin `val p = a * b` infiere. En C++ `auto p = a * b`. En Haskell la inferencia (Hindley-Milner) es total: casi nunca anotas tipos.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 052
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Creer que inferencia = dinámico** → causa: confundir no-anotar con no-tipar → solución: recordar que el tipo inferido es fijo y se comprueba
- **No anotar donde hace falta** → causa: Java/C exigen el tipo → solución: anotar cuando el lenguaje no infiere

## ❓ Preguntas frecuentes

- **¿La inferencia hace el código más lento?** No: ocurre en compilación; el binario es idéntico al anotado.
- **¿Siempre puede inferir?** No siempre; a veces el tipo es ambiguo y hay que anotar.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 051](../../parte-3-valores-tipos-y-variables/051-tipado-fuerte-vs-debil/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 053 ⏭️](../../parte-3-valores-tipos-y-variables/053-nulabilidad-null-nil-none-option-y-valores-ausentes/README.md)
