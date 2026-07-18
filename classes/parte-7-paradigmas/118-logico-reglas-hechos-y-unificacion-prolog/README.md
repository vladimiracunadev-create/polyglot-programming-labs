# Clase 118 — Lógico: reglas, hechos y unificación (Prolog)

> Parte **7 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Asomarse al paradigma **lógico** (Prolog): en vez de calcular paso a paso, se declaran hechos y reglas y se consulta si algo se cumple. Aquí la regla `es_divisor(a, b)` es verdadera si a divide a b.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Expresar una relación como regla lógica.
2. Consultar si la relación se cumple.
3. Contrastar lógico con imperativo.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Programación lógica | Hechos y reglas |
| 2 | Regla | Relación que se cumple o no |
| 3 | Consulta | Preguntar por la verdad de algo |

## 📖 Definiciones y características

- **Lógico** — paradigma en el que se declaran hechos y reglas y se consultan (Prolog). Clave: el motor deduce.
- **Regla** — relación condicional entre términos. Clave: `es_divisor(A,B) :- B mod A =:= 0`.
- **Consulta** — pregunta al sistema sobre si algo se cumple. Clave: devuelve verdadero/falso o soluciones.

## 🧩 Situación

En Prolog no dices cómo comprobar la divisibilidad: declaras la regla y preguntas `es_divisor(3, 12)`. El motor responde. Es el estilo de los sistemas expertos y el razonamiento.

## 🧮 Modelo

- **Entrada** (stdin): una línea `a b` (dos enteros, a != 0)
- **Salida** (stdout): `divisor=<true|false>` (¿a divide a b?)
- **Regla:** divisor = (b mod a == 0)

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `3 12` | `divisor=true` |
| `5 12` | `divisor=false` |
| `4 12` | `divisor=true` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
REGLA es_divisor(a,b) SI b mod a == 0 ; CONSULTAR es_divisor(a,b)
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
| Sintáctica | En los del núcleo es un `if (b % a == 0)`; en Prolog, una regla. |
| Semántica | El lógico deduce; los imperativos comprueban. |
| Paradigmática | SQL (declarativo) es primo del lógico: describe condiciones. |

## 🧬 El concepto en la familia

En Prolog: `es_divisor(A, B) :- 0 is B mod A.` y la consulta `?- es_divisor(3, 12).`. Datalog es un subconjunto para datos.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 118
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Confundir lógico con imperativo** → causa: querer controlar el cómo → solución: declarar la relación y consultar
- **División por cero en la regla** → causa: a = 0 → solución: aquí a != 0

## ❓ Preguntas frecuentes

- **¿Dónde se usa Prolog?** IA simbólica, sistemas expertos, análisis de lenguaje, verificación.
- **¿SQL es lógico?** Es declarativo, primo cercano; describe condiciones sobre datos.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 117](../../parte-7-paradigmas/117-declarativo-consultas-y-transformacion-sql/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 119 ⏭️](../../parte-7-paradigmas/119-orientado-a-eventos-y-callbacks/README.md)
