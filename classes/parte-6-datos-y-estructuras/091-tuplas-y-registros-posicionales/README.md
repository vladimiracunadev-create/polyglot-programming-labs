# Clase 091 — Tuplas y registros posicionales

> Parte **6 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Usar **tuplas**: agrupar un número fijo de valores, posiblemente de tipos distintos, sin definir una clase. Se accede por posición y se desestructuran fácilmente.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Crear y desestructurar una tupla.
2. Acceder a los componentes por posición.
3. Distinguir tupla de lista.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Tupla | Grupo fijo y ordenado |
| 2 | Componentes | Acceso por posición |
| 3 | Desestructuración | Repartir en variables |

## 📖 Definiciones y características

- **Tupla** — grupo ordenado de valores de tamaño fijo. Clave: liviana, sin definir un tipo.
- **Componente** — cada elemento de la tupla, por posición. Clave: `.0`, `[0]`.
- **Registro posicional** — estructura cuyos campos se identifican por orden. Clave: la tupla lo es.

## 🧩 Situación

Devolver coordenadas `(x, y)`, un par clave/valor, o un resultado con dos partes: la tupla agrupa sin la ceremonia de una clase.

## 🧮 Modelo

- **Entrada** (stdin): una línea `a b` (dos enteros)
- **Salida** (stdout): `tupla=(<b>, <a>)` (componentes intercambiados)
- **Regla:** (a, b) → (b, a)

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `3 4` | `tupla=(4, 3)` |
| `0 -2` | `tupla=(-2, 0)` |
| `5 5` | `tupla=(5, 5)` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER (a, b) ; intercambiar ; ESCRIBIR (b, a)
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
| Sintáctica | `(a, b)` (Python/Rust/Go pares), arreglo (JS), record (Java). |
| Semántica | Rust/Python tienen tuplas nativas; Java usa records/objetos. |
| Paradigmática | SQL: una fila con varias columnas es una tupla. |

## 🧬 El concepto en la familia

En Ruby `[a, b]` funciona como tupla. En Haskell `(a, b)` es una tupla nativa con `fst`/`snd`.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 091
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Confundir tupla con lista** → causa: esperar que crezca → solución: la tupla tiene tamaño fijo
- **Acceder a un índice inexistente** → causa: error de posición → solución: respetar el número de componentes

## ❓ Preguntas frecuentes

- **¿Tupla o clase?** Tupla para agrupaciones pequeñas y anónimas; clase cuando los campos merecen nombre.
- **¿Las tuplas son inmutables?** En muchos lenguajes sí (Python, Rust): no se cambian tras crearlas.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 090](../../parte-6-datos-y-estructuras/090-listas-vectores-y-arreglos-dinamicos/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 092 ⏭️](../../parte-6-datos-y-estructuras/092-rangos-y-secuencias/README.md)
