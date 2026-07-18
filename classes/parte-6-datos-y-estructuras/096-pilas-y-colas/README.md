# Clase 096 — Pilas y colas

> Parte **6 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Distinguir **pila (LIFO)** de **cola (FIFO)**: dos formas de ordenar la salida. La pila devuelve el último que entró; la cola, el primero.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Simular una pila y una cola.
2. Explicar LIFO frente a FIFO.
3. Reconocer sus usos típicos.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Pila (LIFO) | Último en entrar, primero en salir |
| 2 | Cola (FIFO) | Primero en entrar, primero en salir |
| 3 | push/pop, enqueue/dequeue | Sus operaciones |

## 📖 Definiciones y características

- **Pila** — estructura LIFO: se saca el último añadido. Clave: deshacer, llamadas.
- **Cola** — estructura FIFO: se saca el primero añadido. Clave: turnos, tareas.
- **LIFO/FIFO** — orden de salida. Clave: define la estructura.

## 🧩 Situación

La pila modela el 'deshacer' y la pila de llamadas; la cola modela una fila de impresión o de tareas. La misma entrada sale en orden opuesto según la estructura.

## 🧮 Modelo

- **Entrada** (stdin): una línea con enteros separados por espacio
- **Salida** (stdout): `pila=<orden LIFO> cola=<orden FIFO>`
- **Regla:** pila = inverso(lista); cola = lista

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `1 2 3` | `pila=3-2-1 cola=1-2-3` |
| `5` | `pila=5 cola=5` |
| `1 2 3 4` | `pila=4-3-2-1 cola=1-2-3-4` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER lista ; pila <- sacar en LIFO ; cola <- sacar en FIFO
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
| Sintáctica | `append`/`pop` (Python), `push`/`shift` (JS), `Deque` (Java). |
| Semántica | La pila saca por el final; la cola por el frente. |
| Paradigmática | SQL ordena por la posición ascendente o descendente. |

## 🧬 El concepto en la familia

En Go una pila/cola se hace con un slice. En C++ `std::stack` y `std::queue`.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 096
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Confundir el extremo de salida** → causa: pila y cola invertidas → solución: pila saca por el final; cola por el frente
- **Usar shift/remove(0) en listas grandes** → causa: coste O(n) → solución: usar una estructura de cola eficiente (deque)

## ❓ Preguntas frecuentes

- **¿Pila o cola?** Pila para LIFO (deshacer, recursión); cola para FIFO (turnos, tareas).
- **¿La recursión usa pila?** Sí: la pila de llamadas es una pila real del programa.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 095](../../parte-6-datos-y-estructuras/095-mapas-diccionarios-tablas-hash/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 097 ⏭️](../../parte-6-datos-y-estructuras/097-arboles/README.md)
