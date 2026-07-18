# Clase 089 — Arreglos de tamaño fijo

> Parte **6 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Usar un **arreglo de tamaño fijo**: una secuencia contigua con un número de elementos conocido. Es la estructura más básica y la más cercana a la memoria.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Declarar y recorrer un arreglo fijo.
2. Acumular suma y máximo.
3. Reconocer el acceso por índice.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Arreglo fijo | Tamaño conocido, memoria contigua |
| 2 | Índice | Acceso por posición (base 0) |
| 3 | Recorrido | Visitar cada posición |

## 📖 Definiciones y características

- **Arreglo** — colección de elementos contiguos indexados. Clave: acceso O(1) por índice.
- **Tamaño fijo** — número de elementos definido al crear. Clave: no crece.
- **Índice** — posición de un elemento, empezando en 0. Clave: `arr[0]` es el primero.

## 🧩 Situación

Un arreglo fijo de 3 sensores, 12 meses, 7 días: cuando el tamaño se conoce, el arreglo fijo es la estructura más eficiente.

## 🧮 Modelo

- **Entrada** (stdin): una línea `a b c` (tres enteros)
- **Salida** (stdout): `suma=<a+b+c> max=<el mayor>`
- **Regla:** suma y máximo de los tres elementos

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `3 1 4` | `suma=8 max=4` |
| `10 5 2` | `suma=17 max=10` |
| `1 1 1` | `suma=3 max=1` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER arr[3]
suma <- Σ arr ; max <- MAX(arr)
ESCRIBIR suma, max
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
| Sintáctica | `[a, b, c]` (Python/JS), `int[]` (Java/C#), `[i64; 3]` (Rust), `long[3]` (C). |
| Semántica | En C el tamaño es parte del tipo; en Python/JS el arreglo es dinámico. |
| Paradigmática | SQL agrega sobre filas, no índices. |

## 🧬 El concepto en la familia

En Go `[3]int` es fijo y `[]int` es slice dinámico. En C++ `std::array<int,3>`.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 089
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Salirse del índice** → causa: acceso fuera de rango → solución: recorrer solo dentro del tamaño
- **Confundir fijo con dinámico** → causa: esperar que crezca → solución: usar lista/vector si el tamaño cambia

## ❓ Preguntas frecuentes

- **¿Por qué base 0?** El índice es un desplazamiento desde el inicio; el primero está a distancia 0.
- **¿Arreglo o lista?** Arreglo fijo si el tamaño es constante; lista si varía (siguiente clase).

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 088](../../parte-5-funciones-y-modularidad/088-importar-exportar-y-organizar-un-proyecto/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 090 ⏭️](../../parte-6-datos-y-estructuras/090-listas-vectores-y-arreglos-dinamicos/README.md)
