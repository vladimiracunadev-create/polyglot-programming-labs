# Clase 047 — Caracteres, texto y Unicode

> Parte **3 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Entender que un **carácter** es, por dentro, un número: su punto de código. Verás cómo cada lenguaje lee un carácter y obtiene su código, y por qué el texto es, en el fondo, una secuencia de números.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Obtener el punto de código de un carácter.
2. Leer un único carácter de la entrada.
3. Explicar la relación entre carácter y número.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Carácter como número | Cada carácter tiene un código (ASCII/Unicode) |
| 2 | Leer un carácter | Distinto de leer una línea |
| 3 | ASCII y Unicode | Del código 0-127 a todo el texto humano |
| 4 | char vs. string | Un carácter no es una cadena de longitud 1 en todos |

## 📖 Definiciones y características

- **Carácter** — símbolo textual (letra, dígito, signo). Clave: internamente es un número.
- **Punto de código** — número que identifica un carácter en Unicode/ASCII. Clave: 'A' es 65.
- **ASCII** — codificación de 0-127 para el inglés básico. Clave: subconjunto de Unicode.
- **Unicode** — estándar que asigna un código a cada carácter de todo idioma. Clave: el texto moderno.

## 🧩 Situación

La letra 'A' y el número 65 son, para la máquina, lo mismo. Comprender que el texto son códigos numéricos explica el orden alfabético, las conversiones y por qué 'a' y 'A' son distintos.

## 🧮 Modelo

- **Entrada** (stdin): un único carácter (ASCII)
- **Salida** (stdout): `char=<c> codigo=<punto de código>`
- **Regla:** codigo = punto_de_codigo(c)

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `A` | `char=A codigo=65` |
| `z` | `char=z codigo=122` |
| `0` | `char=0 codigo=48` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER c
ESCRIBIR "char=" c " codigo=" CODIGO(c)
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
| Sintáctica | `ord(c)` (Python/PHP), `charCodeAt` (JS), `c as u32` (Rust). |
| Semántica | Java/C leen un byte/char; en C el carácter ya es un `int`. |
| Paradigmática | SQL usa la función `unicode(c)` sobre una columna de texto. |

## 🧬 El concepto en la familia

En Ruby `c.ord`. En Haskell `Data.Char.ord c`. En C++ un `char` es directamente convertible a `int`, como en C.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 047
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Confundir carácter con cadena** → causa: tratar 'A' como texto de longitud 1 → solución: usar el tipo carácter y su código donde corresponde
- **Asumir solo ASCII** → causa: fallar con acentos o emoji → solución: recordar que Unicode va más allá de 0-127 (aquí usamos ASCII)

## ❓ Preguntas frecuentes

- **¿'A' y 'a' tienen el mismo código?** No: 65 y 97. Por eso las comparaciones distinguen mayúsculas.
- **¿Un emoji es un carácter?** Un punto de código Unicode, sí; pero puede ocupar varios bytes al codificarse.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 046](../../parte-3-valores-tipos-y-variables/046-booleanos-y-valores-de-verdad/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 048 ⏭️](../../parte-3-valores-tipos-y-variables/048-cadenas-representacion-inmutabilidad-e-interpolacion/README.md)
