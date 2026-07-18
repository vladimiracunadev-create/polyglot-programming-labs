# Clase 175 — Documentación y defensa de las decisiones de lenguaje

> Parte **11 — Proyecto integrador políglota** · ⏱️ Duración estimada: **90 min** · Nivel: **Avanzado**
> 🚧 **Clase planificada** — página creada con la estructura y la navegación; contenido en desarrollo.

---

## 🎯 Objetivo

Estudiar **documentación y defensa de las decisiones de lenguaje**: su forma independiente del lenguaje, cómo se expresa idiomáticamente en el núcleo de 10 lenguajes y qué cambia (sintáctica, semántica o paradigmáticamente) entre familias.

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

> [⏮️ Clase 174](../../parte-11-proyecto-integrador-poliglota/174-empaquetado-contenedores-y-despliegue/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 176 ⏭️](../../parte-11-proyecto-integrador-poliglota/176-cierre-retrospectiva-y-transferencia-a-nuevos-lenguajes/README.md)
