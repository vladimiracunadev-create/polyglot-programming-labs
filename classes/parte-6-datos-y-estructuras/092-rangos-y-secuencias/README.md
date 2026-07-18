# Clase 092 — Rangos y secuencias

> Parte **6 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Usar **rangos y secuencias**: describir una serie de valores consecutivos sin listarlos. Los rangos alimentan bucles y comprensiones de forma expresiva.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Generar un rango inclusivo.
2. Sumar los valores del rango.
3. Reconocer rangos inclusivos vs. exclusivos.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Rango | Serie de valores consecutivos |
| 2 | Inclusivo/exclusivo | Si incluye el extremo |
| 3 | Secuencia perezosa | No se materializa entera |

## 📖 Definiciones y características

- **Rango** — intervalo de valores consecutivos (`2..5`). Clave: describe sin enumerar.
- **Inclusivo** — incluye el extremo final. Clave: `1..=n` en Rust, `range` en Python es exclusivo.
- **Secuencia** — serie ordenada de valores. Clave: puede ser perezosa.

## 🧩 Situación

`for i in 1..=100` recorre cien valores sin crear una lista de cien. Los rangos son la forma idiomática de iterar por posiciones.

## 🧮 Modelo

- **Entrada** (stdin): una línea `a b` (enteros, a <= b)
- **Salida** (stdout): `rango=<a-...-b> suma=<suma del rango>`
- **Regla:** rango [a..b] y su suma

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `2 5` | `rango=2-3-4-5 suma=14` |
| `1 1` | `rango=1 suma=1` |
| `3 6` | `rango=3-4-5-6 suma=18` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER a, b ; generar a..b ; sumar
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
| Sintáctica | `range(a, b+1)` (Python), `a..=b` (Rust), bucle (C/Java/Go). |
| Semántica | Python `range` es exclusivo del final; Rust distingue `..` y `..=`. |
| Paradigmática | SQL genera rangos con CTE recursivo. |

## 🧬 El concepto en la familia

En Ruby `(a..b)` es inclusivo, `(a...b)` exclusivo. En Kotlin `a..b` es inclusivo.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 092
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Error por el extremo (off-by-one)** → causa: incluir o excluir de más → solución: tener claro si el rango incluye el final
- **Materializar rangos enormes** → causa: gasto de memoria → solución: iterar perezosamente cuando se pueda

## ❓ Preguntas frecuentes

- **¿Rango inclusivo o exclusivo?** Depende del lenguaje; conócelo para no equivocar el extremo.
- **¿Rango consume memoria?** En Python/Rust es perezoso; no crea la lista completa.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 091](../../parte-6-datos-y-estructuras/091-tuplas-y-registros-posicionales/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 093 ⏭️](../../parte-6-datos-y-estructuras/093-cadenas-como-estructura-de-datos/README.md)
