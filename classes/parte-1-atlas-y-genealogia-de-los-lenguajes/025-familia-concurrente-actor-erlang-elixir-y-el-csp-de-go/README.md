# Clase 025 — Familia concurrente/actor: Erlang, Elixir y el CSP de Go

> Parte **1 — Atlas y genealogía de los lenguajes** · ⏱️ Duración estimada: **90 min** · Nivel: **Fundamentos**
> 🚧 **Clase planificada** — página creada, contenido en desarrollo.

---

## 🎯 Objetivo

Comprender **familia concurrente/actor: erlang, elixir y el csp de go** como conocimiento transferible: su forma independiente del lenguaje, cómo se expresa en el núcleo de 10 lenguajes y qué cambia (sintáctica, semántica o paradigmáticamente) de una familia a otra.

## 📚 Resultados de aprendizaje

_🚧 Contenido en desarrollo — la estructura de la clase ya está fijada._

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | _en desarrollo_ | _pendiente_ |

## 📖 Definiciones y características

_🚧 En desarrollo._

## 🧩 Situación

_El problema observable que motiva esta clase._

## 🧮 Modelo

Entradas · salidas · reglas · casos límite. La especificación es neutral al lenguaje y se
verifica con [`casos.json`](casos.json).

## 📐 Algoritmo (pseudocódigo neutral)

```text
# pseudocódigo independiente del lenguaje
```

## 🌐 Implementaciones idiomáticas

Cuando esta clase se construya, aquí vivirá una implementación idiomática por lenguaje del núcleo, verificadas contra `casos.json`:

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

## 🔬 Comparación

| Clase de diferencia | Qué observar |
|---|---|
| Sintáctica | Cómo se escribe lo mismo en cada lenguaje |
| Semántica | Tipos, mutabilidad, memoria y errores |
| Paradigmática | Si el lenguaje invita a estructurar la solución de otra forma |

## 🧬 El concepto en la familia

Cómo se ve este concepto en los **primos** de cada familia (Ruby, Kotlin, Haskell, Elixir,
Lua, C++…), como _delta_ respecto del representante del núcleo. Consulta el
[Atlas](../../../atlas/README.md).

## ✅ Prueba común

Los mismos casos de entrada/salida para todas las implementaciones:
[`casos.json`](casos.json). Verifica la equivalencia con:

```bash
python scripts/verificar_equivalencia.py 025-familia-concurrente-actor-erlang-elixir-y-el-csp-de-go
```

## 🧪 Reto de transferencia

Resuelve una variante en un lenguaje **no explicado paso a paso**. Detalle en
[`reto.md`](reto.md).

## ⚠️ Errores comunes

_Síntoma → causa → solución (en desarrollo)._

## ❓ Preguntas frecuentes

_En desarrollo._

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⬅️ Parte 1](../README.md) · [📚 Índice completo](../../README.md) · [🌐 Atlas de lenguajes](../../../atlas/README.md)
