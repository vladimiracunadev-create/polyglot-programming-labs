# Clase 084 — Funciones puras y efectos secundarios

> Parte **5 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Distinguir una **función pura** —su resultado depende solo de sus argumentos y no cambia nada externo— de una con **efectos secundarios**. Las puras son predecibles, testeables y seguras de paralelizar.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Definir una función pura.
2. Explicar qué es un efecto secundario.
3. Argumentar las ventajas de la pureza.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Función pura | Mismo entrada → mismo resultado |
| 2 | Efecto secundario | Cambiar algo externo |
| 3 | Transparencia referencial | Sustituir la llamada por su valor |
| 4 | Ventajas | Testeable, cacheable, paralelizable |

## 📖 Definiciones y características

- **Función pura** — su salida depende solo de sus entradas y no causa efectos externos. Clave: predecible.
- **Efecto secundario** — modificar estado externo, imprimir, leer archivos. Clave: rompe la pureza.
- **Transparencia referencial** — poder reemplazar la llamada por su resultado. Clave: propiedad de las puras.
- **Determinismo** — misma entrada, misma salida siempre. Clave: facilita las pruebas.

## 🧩 Situación

`cuadrado(n)` siempre da lo mismo para el mismo `n` y no toca nada más: es pura. Una función que además escribe en un log tiene un efecto secundario. Las puras son las más fáciles de probar y razonar.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n`
- **Salida** (stdout): `puro=<n²>`
- **Regla:** cuadrado(n) = n * n (sin efectos)

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `4` | `puro=16` |
| `-3` | `puro=9` |
| `0` | `puro=0` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
FUNCION cuadrado(n): DEVOLVER n*n   // sin tocar nada externo
LEER n ; ESCRIBIR "puro=" cuadrado(n)
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
| Sintáctica | Idéntica en todos: una función que devuelve un cálculo. |
| Semántica | La pureza es una propiedad del diseño, no de la sintaxis. |
| Paradigmática | SQL (declarativo) y Haskell (puro) empujan hacia la pureza por defecto. |

## 🧬 El concepto en la familia

En Haskell casi todo es puro; los efectos se aíslan con el tipo IO. En Rust, la pureza es una convención, no forzada.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 084
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Mezclar cálculo con impresión/estado** → causa: función difícil de testear → solución: separar el cálculo puro del efecto (I/O)
- **Depender de estado global** → causa: resultados no reproducibles → solución: pasar todo por parámetros

## ❓ Preguntas frecuentes

- **¿Todo debe ser puro?** No: los efectos son necesarios (I/O). La idea es aislarlos y mantener puro el núcleo.
- **¿Por qué importan las puras?** Se prueban fácil, se cachean (memoización) y se pueden paralelizar sin riesgo.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 083](../../parte-5-funciones-y-modularidad/083-cierres-closures-y-captura-de-variables/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 085 ⏭️](../../parte-5-funciones-y-modularidad/085-funciones-de-primera-clase-y-como-valores/README.md)
