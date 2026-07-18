# Clase 093 — Cadenas como estructura de datos

> Parte **6 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Tratar una **cadena como estructura de datos**: una secuencia de caracteres que se puede recorrer, indexar e invertir. Verás que la inmutabilidad obliga a construir una nueva cadena.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Recorrer una cadena carácter a carácter.
2. Construir una cadena invertida.
3. Reconocer la inmutabilidad de las cadenas.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Cadena como secuencia | Caracteres indexados |
| 2 | Inversión | Del último al primero |
| 3 | Inmutabilidad | Se crea una nueva cadena |

## 📖 Definiciones y características

- **Cadena** — secuencia de caracteres. Clave: se recorre como una colección.
- **Inmutable** — no se modifica en sitio (Java/Python/C#). Clave: invertir crea otra.
- **Índice de carácter** — posición dentro de la cadena. Clave: base 0.

## 🧩 Situación

Invertir texto, comprobar palíndromos, procesar entradas: tratar la cadena como una secuencia de caracteres es constante en programación.

## 🧮 Modelo

- **Entrada** (stdin): una palabra (ASCII, sin espacios)
- **Salida** (stdout): `invertido=<la palabra al revés>`
- **Regla:** invertir la secuencia de caracteres

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `hola` | `invertido=aloh` |
| `Ada` | `invertido=adA` |
| `abc` | `invertido=cba` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER w ; recorrer del final al inicio ; ESCRIBIR invertido
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
| Sintáctica | `w[::-1]` (Python), `.reverse()` sobre arreglo de chars (JS/Rust). |
| Semántica | En Rust hay que iterar por `chars()` (UTF-8); en C es por bytes. |
| Paradigmática | SQL tiene la función `reverse` en algunos motores; sqlite no de serie. |

## 🧬 El concepto en la familia

En Ruby `w.reverse`. En C se intercambian los caracteres por índices, sin función incorporada.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 093
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Invertir por bytes con Unicode** → causa: romper caracteres multibyte → solución: iterar por caracteres (aquí ASCII, sin problema)
- **Intentar mutar la cadena** → causa: es inmutable en varios lenguajes → solución: construir una nueva

## ❓ Preguntas frecuentes

- **¿Por qué invertir crea otra cadena?** Porque en muchos lenguajes las cadenas son inmutables.
- **¿ASCII o Unicode?** Aquí ASCII; con Unicode hay que respetar los límites de carácter.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 092](../../parte-6-datos-y-estructuras/092-rangos-y-secuencias/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 094 ⏭️](../../parte-6-datos-y-estructuras/094-conjuntos-sets-y-unicidad/README.md)
