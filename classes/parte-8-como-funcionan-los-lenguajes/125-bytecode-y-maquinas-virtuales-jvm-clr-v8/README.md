# Clase 125 — Bytecode y máquinas virtuales (JVM, CLR, V8)

> Parte **8 — Cómo funcionan los lenguajes** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> 🚧 **Clase planificada** — página creada con la estructura y la navegación; contenido en desarrollo.

---

## 🎯 Objetivo

Estudiar **bytecode y máquinas virtuales (jvm, clr, v8)**: su forma independiente del lenguaje, cómo se expresa idiomáticamente en el núcleo de 10 lenguajes y qué cambia (sintáctica, semántica o paradigmáticamente) entre familias.

## 🧮 Modelo

Cuando esta clase se construya, tendrá su especificación neutral (entradas · salidas · reglas) y su
[`casos.json`](casos.json) para verificar equivalencia.

## 🌐 Implementaciones idiomáticas (previstas)

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

## 🔬 Comparación · 🧬 El concepto en la familia

Cada clase compara las tres clases de diferencia (sintáctica, semántica, paradigmática) y muestra el
concepto en los primos de cada familia. Consulta el [Atlas](../../../atlas/README.md).

---

> [⏮️ Clase 124](../../parte-8-como-funcionan-los-lenguajes/124-compilador-interprete-y-jit/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 126 ⏭️](../../parte-8-como-funcionan-los-lenguajes/126-aot-vs-jit-costos-y-beneficios/README.md)
