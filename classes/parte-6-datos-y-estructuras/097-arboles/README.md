# Clase 097 — Árboles

> Parte **6 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Conocer los **árboles**: estructuras jerárquicas. En un árbol binario de búsqueda (BST), el recorrido in-order devuelve los elementos ordenados. Aquí el efecto observable es la ordenación.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Entender la propiedad del BST.
2. Reconocer el recorrido in-order.
3. Relacionar el árbol con el orden.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Árbol | Nodos con hijos, jerárquico |
| 2 | BST | Menores a la izquierda, mayores a la derecha |
| 3 | Recorrido in-order | Produce el orden ascendente |

## 📖 Definiciones y características

- **Árbol** — estructura jerárquica de nodos con hijos. Clave: sin ciclos, una raíz.
- **BST** — árbol binario ordenado: izquierda < nodo < derecha. Clave: búsqueda O(log n) equilibrado.
- **In-order** — recorrido izquierda-raíz-derecha. Clave: en un BST da los valores ordenados.

## 🧩 Situación

Índices de bases de datos, sistemas de archivos, autocompletado: los árboles organizan datos jerárquicos y permiten búsquedas rápidas. En un BST, recorrer in-order ordena.

## 🧮 Modelo

- **Entrada** (stdin): una línea con enteros distintos separados por espacio
- **Salida** (stdout): `inorden=<los valores ordenados ascendente unidos por ->`
- **Regla:** in-order de un BST = orden ascendente

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `3 1 4` | `inorden=1-3-4` |
| `5 2 8 1` | `inorden=1-2-5-8` |
| `9 7` | `inorden=7-9` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER lista ; insertar en BST ; recorrer in-order
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
| Sintáctica | Ordenar (`sorted`) equivale al in-order del BST en esta clase. |
| Semántica | El BST mantiene el orden al insertar; ordenar lo hace de una vez. |
| Paradigmática | SQL usa ORDER BY, que el motor implementa con árboles/índices. |

## 🧬 El concepto en la familia

En muchos lenguajes se usa un TreeSet/TreeMap (árbol equilibrado) que ya mantiene el orden.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 097
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Confundir in-order con otros recorridos** → causa: pre/post-order no ordenan → solución: usar in-order para obtener el orden
- **Insertar duplicados sin política** → causa: árbol ambiguo → solución: aquí los valores son distintos

## ❓ Preguntas frecuentes

- **¿Por qué in-order ordena?** Porque visita izquierda (menores), raíz, derecha (mayores) recursivamente.
- **¿BST o array ordenado?** El BST permite inserciones/borrados eficientes manteniendo el orden.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 096](../../parte-6-datos-y-estructuras/096-pilas-y-colas/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 098 ⏭️](../../parte-6-datos-y-estructuras/098-grafos/README.md)
