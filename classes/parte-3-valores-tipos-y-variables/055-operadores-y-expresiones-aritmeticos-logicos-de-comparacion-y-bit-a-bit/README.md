# Clase 055 — Operadores y expresiones: aritméticos, lógicos, de comparación y bit a bit

> Parte **3 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Repasar los **operadores aritméticos** y ver diferencias sutiles: la división entera y el módulo se comportan distinto con negativos según el lenguaje (aquí usamos positivos para que coincidan). Es la base del cálculo en todo programa.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Aplicar los cinco operadores aritméticos básicos.
2. Distinguir división entera de división real.
3. Reconocer que el módulo con negativos varía entre lenguajes.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Operadores aritméticos | +, -, *, / y % |
| 2 | División entera | Descarta la parte decimal |
| 3 | Módulo (resto) | Lo que sobra de la división |
| 4 | Precedencia | El orden en que se evalúan |

## 📖 Definiciones y características

- **Operador** — símbolo que combina valores para producir otro (+, *, %). Clave: bloque de las expresiones.
- **División entera** — cociente sin decimales. Clave: `7/2 = 3`, no 3.5.
- **Módulo** — resto de la división entera. Clave: `7 % 2 = 1`.
- **Precedencia** — el orden de evaluación (`*` antes que `+`). Clave: los paréntesis mandan.

## 🧩 Situación

Repartir 7 caramelos entre 2 niños: cada uno recibe 3 (división entera) y sobra 1 (módulo). Estos operadores están en todo cálculo; sus reglas con negativos son una trampa clásica entre lenguajes.

## 🧮 Modelo

- **Entrada** (stdin): una línea `a b` (enteros positivos, b != 0)
- **Salida** (stdout): `suma=<a+b> resta=<a-b> mult=<a*b> div=<a/b entera> mod=<a%b>`
- **Regla:** las cinco operaciones aritméticas sobre a y b

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `10 3` | `suma=13 resta=7 mult=30 div=3 mod=1` |
| `20 4` | `suma=24 resta=16 mult=80 div=5 mod=0` |
| `7 2` | `suma=9 resta=5 mult=14 div=3 mod=1` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER a, b
ESCRIBIR suma, resta, mult, división entera y módulo
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
| Sintáctica | `//` (Python) vs. `/` entre enteros (C/Java/Go); `%` en casi todos. |
| Semántica | Con negativos, el módulo difiere: Python da signo del divisor; C/Java, del dividendo. |
| Paradigmática | SQL evalúa la expresión aritmética en la propia consulta. |

## 🧬 El concepto en la familia

En Ruby `a / b` es entero si ambos lo son, como C. En Haskell `div` y `mod` (y `quot`/`rem` con otra regla de signo).

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 055
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Esperar decimales de `/` entre enteros** → causa: en C/Java la división de enteros trunca → solución: usar reales si quieres decimales, o `//` en Python
- **Asumir el mismo módulo con negativos** → causa: Python y C difieren en el signo del resto → solución: usar entradas positivas o conocer la regla de cada lenguaje

## ❓ Preguntas frecuentes

- **¿`7/2` es 3 o 3.5?** Entre enteros, 3 (división entera). Con un real, 3.5.
- **¿Por qué el módulo varía con negativos?** Cada lenguaje elige el signo del resto; por eso aquí usamos positivos.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 054](../../parte-3-valores-tipos-y-variables/054-mutabilidad-e-inmutabilidad/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 056 ⏭️](../../parte-3-valores-tipos-y-variables/056-entrada-y-salida-basica-leer-y-escribir/README.md)
