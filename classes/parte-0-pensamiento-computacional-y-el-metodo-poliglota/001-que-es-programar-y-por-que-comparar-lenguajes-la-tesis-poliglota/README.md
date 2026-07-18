# Clase 001 — Qué es programar y por qué comparar lenguajes: la tesis políglota

> Parte **0 — Pensamiento computacional y el método políglota** · ⏱️ Duración estimada: **90 min** · Nivel: **Fundamentos**
> ✅ **Clase construida.**

---

## 🎯 Objetivo

Entender la tesis del programa: el conocimiento de la programación es transferible. Un mismo concepto (una variable, un bucle, una función) existe en todos los lenguajes; lo que cambia es la forma. Aprender el concepto una vez permite reconocerlo, compararlo y aplicarlo en cualquier lenguaje.

## 📚 Resultados de aprendizaje

1. Explicar la diferencia entre aprender un lenguaje y aprender a programar.
2. Enunciar la tesis políglota: concepto → forma neutral → implementaciones → comparación → transferencia.
3. Distinguir conocimiento transferible de detalle sintáctico.
4. Justificar por qué comparar lenguajes acelera el aprendizaje en vez de dispersarlo.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Concepto vs. sintaxis | Separa lo que perdura de lo que cambia entre lenguajes |
| 2 | Los 10 lenguajes del núcleo | Definen el terreno práctico que se implementa y verifica |
| 3 | Las ~40 familias del Atlas | Amplían la comprensión sin multiplicar el mantenimiento |
| 4 | La ficha de transferencia | Es la unidad mínima de estudio del programa |
| 5 | Reconocer, comparar, aplicar | El ciclo que convierte teoría en habilidad transferible |

## 📖 Definiciones y características

- **Conocimiento transferible** — idea que sobrevive al cambio de lenguaje (p. ej. 'iterar una colección'). Clave: es lo que de verdad se aprende.
- **Núcleo** — los 10 lenguajes que se implementan y verifican en CI. Clave: profundidad práctica.
- **Atlas** — cobertura de ~40 lenguajes por sus características. Clave: amplitud de comprensión.
- **Ficha de transferencia** — unidad de estudio: concepto, algoritmo, implementaciones y comparación. Clave: mismo problema en todos los lenguajes.

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
python scripts/verificar_equivalencia.py 001-que-es-programar-y-por-que-comparar-lenguajes-la-tesis-poliglota
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

> [⬅️ Parte 0](../README.md) · [📚 Índice completo](../../README.md) · [🌐 Atlas de lenguajes](../../../atlas/README.md)
