# Clase 090 — Listas, vectores y arreglos dinámicos

> Parte **6 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Usar una **lista/vector dinámico**: una secuencia que crece y encoge. Invertirla ejercita el recorrido y la construcción de una nueva secuencia.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Construir y recorrer una lista dinámica.
2. Invertir el orden de los elementos.
3. Distinguir lista dinámica de arreglo fijo.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Lista dinámica | Crece según haga falta |
| 2 | Invertir | Recorrer al revés |
| 3 | Redimensionar | Añadir/quitar elementos |

## 📖 Definiciones y características

- **Lista/vector dinámico** — arreglo que cambia de tamaño (list, Vec, ArrayList). Clave: flexible.
- **append** — añadir un elemento al final. Clave: operación base.
- **Inversión** — producir la secuencia en orden contrario. Clave: primero pasa a último.

## 🧩 Situación

Cuando no sabes cuántos elementos habrá (líneas de un archivo, respuestas de un usuario), la lista dinámica es la elección natural.

## 🧮 Modelo

- **Entrada** (stdin): una línea con enteros separados por espacio
- **Salida** (stdout): `invertido=<elementos en orden inverso unidos por ->`
- **Regla:** invertido = reverse(lista)

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `1 2 3` | `invertido=3-2-1` |
| `5` | `invertido=5` |
| `10 20 30 40` | `invertido=40-30-20-10` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER lista ; invertir ; ESCRIBIR unidos por -
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
| Sintáctica | `list[::-1]` (Python), `.reverse()` (JS/Rust), `Collections.reverse` (Java). |
| Semántica | Algunos invierten en sitio (mutando); otros crean una lista nueva. |
| Paradigmática | SQL invierte con ORDER BY descendente sobre una posición. |

## 🧬 El concepto en la familia

En Ruby `lista.reverse`. En Go se invierte con un bucle de índices intercambiando extremos.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 090
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Confundir invertir en sitio con crear copia** → causa: modificar el original sin querer → solución: elegir según necesites conservar el original
- **Bucle de intercambio mal** → causa: invertir de más y volver al inicio → solución: intercambiar solo hasta la mitad

## ❓ Preguntas frecuentes

- **¿Lista o arreglo?** Lista si el tamaño varía; arreglo fijo si es constante.
- **¿Invertir es caro?** Es O(n): hay que tocar cada elemento una vez.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 089](../../parte-6-datos-y-estructuras/089-arreglos-de-tamano-fijo/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 091 ⏭️](../../parte-6-datos-y-estructuras/091-tuplas-y-registros-posicionales/README.md)
