# Clase 042 — Declaración, asignación e inicialización

> Parte **3 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Distinguir tres actos que a menudo se confunden: **declarar** (introducir un nombre), **inicializar** (darle su primer valor) y **asignar** (cambiarlo después). El intercambio de dos variables los ejercita todos y revela cómo cada lenguaje los expresa (variable temporal vs. asignación múltiple).

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Diferenciar declaración, inicialización y (re)asignación.
2. Intercambiar dos variables con y sin temporal según el lenguaje.
3. Reconocer la asignación múltiple (desestructuración) donde existe.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Declarar vs. inicializar | Introducir un nombre no es lo mismo que darle valor |
| 2 | Reasignación | Cambiar el valor de una variable ya inicializada |
| 3 | Variable temporal | El patrón clásico para intercambiar |
| 4 | Asignación múltiple | a, b = b, a donde el lenguaje lo permite |

## 📖 Definiciones y características

- **Declaración** — introducir un nombre en un ámbito. Clave: en lenguajes estáticos fija el tipo.
- **Inicialización** — dar el primer valor a una variable. Clave: usarla sin inicializar es un error clásico.
- **Asignación** — cambiar el valor de una variable existente. Clave: solo posible si es mutable.
- **Asignación múltiple** — asignar varias variables a la vez (a, b = b, a). Clave: evita la temporal en Python, JS, Go, Rust.

## 🧩 Situación

Intercambiar dos valores parece trivial, pero es donde se ve si un lenguaje ofrece asignación múltiple (Python, Go, Rust, JS) o exige la variable temporal de toda la vida (C, Java).

## 🧮 Modelo

- **Entrada** (stdin): una línea `a b` (dos enteros)
- **Salida** (stdout): `a=<nuevo a> b=<nuevo b>` tras intercambiar
- **Regla:** intercambiar a y b

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `3 7` | `a=7 b=3` |
| `0 5` | `a=5 b=0` |
| `-2 9` | `a=9 b=-2` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER a, b
tmp <- a ; a <- b ; b <- tmp   (o bien: a, b <- b, a)
ESCRIBIR "a=" a " b=" b
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
| Sintáctica | `a, b = b, a` (Python/JS/Go/Rust) vs. `tmp=a;a=b;b=tmp;` (C/Java). |
| Semántica | La asignación múltiple evalúa el lado derecho antes de asignar; la temporal es manual. |
| Paradigmática | SQL no reasigna variables: se describe la salida intercambiando columnas. |

## 🧬 El concepto en la familia

En Ruby (scripting dinámico) es `a, b = b, a`, igual que Python. En Kotlin (JVM) se usa `also` o una temporal; en Haskell no hay reasignación: se define un nuevo valor.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 042
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Perder un valor al intercambiar sin temporal** → causa: asignar a=b antes de guardar a → solución: usar una temporal o la asignación múltiple del lenguaje
- **Usar una variable sin inicializar** → causa: declararla y no darle valor (C) → solución: inicializar siempre en la declaración

## ❓ Preguntas frecuentes

- **¿La asignación múltiple es más lenta?** No de forma apreciable; es más legible y evita el error de la temporal.
- **¿Por qué C no la tiene?** Es un lenguaje minimalista; el patrón con temporal es explícito y suficiente.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 041](../../parte-3-valores-tipos-y-variables/041-literales-valores-variables-y-constantes/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 043 ⏭️](../../parte-3-valores-tipos-y-variables/043-tipos-primitivos-enteros-reales-booleanos-caracteres/README.md)
