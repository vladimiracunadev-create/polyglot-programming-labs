# Clase 100 — Enumeraciones y tipos algebraicos (ADT / sum types)

> Parte **6 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Usar **tipos algebraicos (suma)**: un valor que es una de varias alternativas, cada una con sus datos. `Forma = Cuadrado | Rectangulo`. El `match` decide y calcula según la variante.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Modelar alternativas con un tipo suma.
2. Decidir por variante con match/switch.
3. Reconocer la exhaustividad del tipo algebraico.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Tipo suma (ADT) | Una de varias alternativas |
| 2 | Variante | Cada caso con sus datos |
| 3 | Match por variante | Decidir según la forma |

## 📖 Definiciones y características

- **Tipo algebraico (suma)** — valor que es una de varias alternativas (Cuadrado o Rectangulo). Clave: modela 'o esto o lo otro'.
- **Variante** — cada alternativa del tipo suma, con sus propios datos. Clave: `Cuadrado(lado)`.
- **Exhaustividad** — cubrir todas las variantes. Clave: Rust lo exige al compilar.

## 🧩 Situación

Un pago es efectivo, tarjeta o transferencia; una figura es círculo, cuadrado o rectángulo. Los tipos suma modelan estas alternativas con seguridad, y el match obliga a considerarlas todas.

## 🧮 Modelo

- **Entrada** (stdin): una línea: `cuadrado <lado>` o `rectangulo <ancho> <alto>`
- **Salida** (stdout): `area=<área calculada>`
- **Regla:** cuadrado→lado²; rectangulo→ancho·alto

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `cuadrado 5` | `area=25` |
| `rectangulo 3 4` | `area=12` |
| `cuadrado 7` | `area=49` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER tipo y datos ; COINCIDIR tipo: cuadrado->l*l ; rectangulo->a*b
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
| Sintáctica | `enum` con datos (Rust), sealed/record (Java/C#), etiqueta + campos (Go/C). |
| Semántica | Rust/Haskell garantizan exhaustividad; C usa una etiqueta manual. |
| Paradigmática | SQL usa una columna 'tipo' + CASE. |

## 🧬 El concepto en la familia

En Haskell `data Forma = Cuadrado Int | Rectangulo Int Int`. En Kotlin, una `sealed class`.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 100
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Olvidar una variante** → causa: caso sin manejar → solución: en Rust el compilador avisa; en otros, incluir el default
- **Leer los datos de la variante equivocada** → causa: usar campos que no existen → solución: extraer solo los datos de la variante correcta

## ❓ Preguntas frecuentes

- **¿Tipo suma o herencia?** El tipo suma es cerrado y exhaustivo; la herencia es abierta. Distintas garantías.
- **¿Por qué 'algebraico'?** Combina 'sumas' (alternativas) y 'productos' (campos) de tipos.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 099](../../parte-6-datos-y-estructuras/099-registros-structs-y-clases/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 101 ⏭️](../../parte-6-datos-y-estructuras/101-igualdad-vs-identidad/README.md)
