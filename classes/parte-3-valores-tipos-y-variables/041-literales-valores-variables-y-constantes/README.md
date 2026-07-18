# Clase 041 — Literales, valores, variables y constantes

> Parte **3 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — clase insignia con las 10 implementaciones del núcleo verificadas en CI.

---

## 🎯 Objetivo

Entender los cuatro ladrillos con los que empieza todo programa: el **literal** (un valor escrito directamente en el código, como `15000`), el **valor** (el dato en memoria), la **variable** (un nombre que apunta a un valor y puede cambiar) y la **constante** (un nombre cuyo valor no debe cambiar). Verás que el concepto es idéntico en los 10 lenguajes del núcleo, pero **cómo se declara, si lleva tipo, si es mutable y cómo se formatea** cambia de una familia a otra.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. **Distinguir** literal, valor, variable y constante con ejemplos propios.
2. **Declarar** una constante y una variable en cada lenguaje del núcleo.
3. **Explicar** por qué en Rust todo es inmutable por defecto y en Python/PHP no.
4. **Implementar** el mismo cálculo de venta en los 10 lenguajes con salida idéntica.
5. **Reconocer** el mismo concepto en primos de otras familias (Ruby, Kotlin, Haskell).

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Literal vs. valor | Separa lo escrito en el código del dato en memoria |
| 2 | Variable | Es el nombre que permite reutilizar y cambiar un valor |
| 3 | Constante | Comunica intención: "esto no cambia" |
| 4 | Declaración e inicialización | Cada lenguaje exige (o infiere) el tipo de forma distinta |
| 5 | Mutabilidad por defecto | Rust/const vs. Python/PHP: decisiones de diseño opuestas |
| 6 | Formato de salida | La cultura/locale y el formateo decimal difieren entre runtimes |

## 📖 Definiciones y características

- **Literal** — valor escrito directamente en el código fuente (`15000`, `"hola"`, `true`). Clave: no tiene nombre.
- **Valor** — el dato concreto que existe en memoria durante la ejecución. Clave: es lo que se calcula y compara.
- **Variable** — nombre asociado a un valor que puede reasignarse. Clave: introduce estado que cambia en el tiempo.
- **Constante** — nombre asociado a un valor que no debe reasignarse. Clave: intención + seguridad.
- **Declaración** — acto de introducir un nombre en un ámbito. Clave: en lenguajes estáticos fija el tipo.
- **Inicialización** — dar el primer valor a una variable. Clave: usar una variable sin inicializar es un error clásico.
- **Mutabilidad** — si un enlace nombre→valor puede cambiar. Clave: Rust la niega por defecto; Python la permite siempre.

## 🧩 Situación

Una tienda calcula el total de una venta a partir de tres datos: el **precio unitario**, la **cantidad** y un **descuento** (0 a 1). Es el problema mínimo donde aparecen literales, variables y constantes, y una operación aritmética.

## 🧮 Modelo

- **Entrada** (stdin, una línea): `precio_unitario cantidad descuento`
- **Salida** (stdout): `Total: <total con 2 decimales>`
- **Regla:** `total = precio_unitario * cantidad * (1 - descuento)`
- **Casos límite:** cantidad `0` ⇒ total `0.00`; descuento `0` ⇒ sin rebaja.

Especificación y verificación en [`casos.json`](casos.json).

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER precio_unitario, cantidad, descuento
subtotal <- precio_unitario * cantidad
total    <- subtotal * (1 - descuento)
ESCRIBIR "Total: " + FORMATEAR(total, 2 decimales)
```

## 🌐 Implementaciones idiomáticas

Mismo algoritmo, forma idiomática en cada lenguaje. Todas producen la salida de `casos.json`:

| Lenguaje | Archivo | Cómo ejecutar |
|---|---|---|
| Python | [`implementaciones/python/main.py`](implementaciones/python/main.py) | `python main.py` |
| JavaScript | [`implementaciones/javascript/main.mjs`](implementaciones/javascript/main.mjs) | `node main.mjs` |
| TypeScript | [`implementaciones/typescript/main.ts`](implementaciones/typescript/main.ts) | `pnpm exec tsx main.ts` |
| Java | [`implementaciones/java/Main.java`](implementaciones/java/Main.java) | `java Main.java` |
| C# | [`implementaciones/csharp/Program.cs`](implementaciones/csharp/Program.cs) | `dotnet run` |
| Go | [`implementaciones/go/main.go`](implementaciones/go/main.go) | `go run main.go` |
| Rust | [`implementaciones/rust/main.rs`](implementaciones/rust/main.rs) | `rustc main.rs -o main && ./main` |
| C | [`implementaciones/c/main.c`](implementaciones/c/main.c) | `cc main.c -o main && ./main` |
| PHP | [`implementaciones/php/main.php`](implementaciones/php/main.php) | `php main.php` |
| SQL | [`implementaciones/sql/main.sql`](implementaciones/sql/main.sql) | `sqlite3 :memory: < main.sql` (ilustrativa) |

> SQL es declarativo: no lee de stdin como los demás. Su implementación muestra la misma fórmula
> sobre una tabla de casos, y por eso el verificador la marca como *ilustrativa*.

## 🔬 Comparación

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| **Sintáctica** | `PRECIO = 15000` (Python) vs. `const precio = 15000;` (JS) vs. `final double precio = 15000;` (Java). |
| **Semántica** | Python/PHP infieren y permiten reasignar; Java/C#/Go/Rust/C fijan tipo; Rust exige `mut` para mutar; C usa tamaños fijos. |
| **Paradigmática** | SQL no tiene "variable que se asigna": describe el resultado, no los pasos. |

## 🧬 El concepto en la familia

- **Familia scripting dinámico** (Ruby, Perl, Lua): como Python/PHP, sin declarar tipo. Ruby: `precio = 15000`, constante por convención con mayúscula (`PRECIO`).
- **Familia JVM** (Kotlin): `val precio = 15000.0` (inmutable) vs. `var` (mutable) — inferencia como en Rust.
- **Familia funcional** (Haskell): `precio = 15000` es una **definición inmutable**, no una asignación; no existe "variable que cambia".
- **Familia C/llaves** (C++): `const double precio = 15000;` — igual que C con `const`.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 041
```

El verificador alimenta cada caso por stdin, compara la salida y omite los lenguajes cuyo
toolchain no esté instalado (degradación silenciosa).

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md): añade un **impuesto** del 19 % después del descuento y resuélvelo en **Kotlin** (no explicado paso a paso), apoyándote en la implementación de Java.

## ⚠️ Errores comunes

- **Formato con coma decimal** (síntoma: `Total: 27000,00`) → causa: locale del sistema → solución: forzar cultura invariante (`Locale.US`, `CultureInfo.InvariantCulture`).
- **Porcentaje entero** (síntoma: descuento ignorado) → causa: `1 - descuento` calculado en enteros → solución: usar tipo real.
- **Usar variable sin inicializar** (C) → causa: valor basura → solución: inicializar siempre.

## ❓ Preguntas frecuentes

- **¿Por qué Rust obliga a `mut`?** Para que la mutación sea una decisión visible, no un accidente.
- **¿PHP es débilmente tipado?** Sí: convierte entre tipos automáticamente; por eso el `(float)`/`(int)` explícito documenta la intención.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo (Python, MDN, TypeScript, Oracle Java, Microsoft C#/.NET, Go, Rust, cppreference/C, SQLite, PHP).

---

> [⬅️ Parte 3](../README.md) · [📚 Índice completo](../../README.md) · [🌐 Atlas de lenguajes](../../../atlas/README.md)
