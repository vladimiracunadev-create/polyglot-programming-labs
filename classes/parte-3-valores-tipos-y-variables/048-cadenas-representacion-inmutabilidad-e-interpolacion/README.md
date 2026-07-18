# Clase 048 — Cadenas: representación, inmutabilidad e interpolación

> Parte **3 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Trabajar con **cadenas**: leer texto, interpolarlo en un saludo y medir su longitud. Verás que la longitud puede significar 'bytes' o 'caracteres' según el lenguaje (aquí, ASCII, coinciden).

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Interpolar una variable de texto en una cadena.
2. Obtener la longitud de una cadena.
3. Reconocer la inmutabilidad de las cadenas donde aplica.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Interpolación | Insertar valores dentro de una cadena |
| 2 | Longitud | Cuántos caracteres tiene |
| 3 | Inmutabilidad | En muchos lenguajes la cadena no se modifica, se recrea |
| 4 | Bytes vs. caracteres | La longitud puede medir distinto |

## 📖 Definiciones y características

- **Cadena** — secuencia de caracteres. Clave: el tipo para todo texto.
- **Interpolación** — insertar el valor de una variable dentro de una cadena. Clave: `f"...{x}"`, `${x}`, etc.
- **Longitud** — número de unidades (caracteres/bytes) de la cadena. Clave: en ASCII coinciden.
- **Inmutabilidad de cadenas** — en Java, C#, Python las cadenas no se modifican in situ. Clave: se crea una nueva.

## 🧩 Situación

Saludar por nombre y contar caracteres son de las operaciones más comunes. Cómo se interpola y cómo se mide la longitud revela decisiones de diseño de cada lenguaje.

## 🧮 Modelo

- **Entrada** (stdin): una palabra (ASCII, sin espacios)
- **Salida** (stdout): `hola=<palabra> longitud=<número de caracteres>`
- **Regla:** longitud = |palabra|

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `Ada` | `hola=Ada longitud=3` |
| `Bo` | `hola=Bo longitud=2` |
| `polyglot` | `hola=polyglot longitud=8` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER w
ESCRIBIR "hola=" w " longitud=" LONGITUD(w)
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
| Sintáctica | `len(w)` (Python), `w.length` (JS/Java), `len(w)` (Go, bytes), `w.len()` (Rust, bytes). |
| Semántica | En Go/Rust `len` cuenta bytes; en Java/JS cuenta unidades UTF-16 (aquí ASCII: igual). |
| Paradigmática | SQL usa la función `length(w)` sobre una columna. |

## 🧬 El concepto en la familia

En Ruby `w.length`. En Haskell `length w`. En C++ `w.size()`. Todos miden lo mismo en ASCII; difieren con Unicode multibyte.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 048
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Asumir que longitud = caracteres siempre** → causa: olvidar Unicode multibyte → solución: en Go/Rust `len` es bytes; usar el conteo de caracteres si hace falta
- **Modificar una cadena in situ** → causa: esperar mutación en Java/Python → solución: recordar que la cadena es inmutable: se crea una nueva

## ❓ Preguntas frecuentes

- **¿Por qué las cadenas son inmutables?** Seguridad y optimización (compartir, hashear). Modificar crea una copia.
- **¿`len` en Go da caracteres?** Da bytes; para caracteres Unicode se usa `utf8.RuneCountInString`.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 047](../../parte-3-valores-tipos-y-variables/047-caracteres-texto-y-unicode/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 049 ⏭️](../../parte-3-valores-tipos-y-variables/049-conversion-de-tipos-casting-explicito-vs-coercion-implicita/README.md)
