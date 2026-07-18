# Clase 098 — Grafos

> Parte **6 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Conocer los **grafos**: nodos conectados por aristas. Representarlos como lista de aristas y contar nodos y aristas es el primer paso para modelar redes, mapas y dependencias.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Representar un grafo por sus aristas.
2. Contar aristas y nodos distintos.
3. Reconocer dónde aparecen los grafos.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Grafo | Nodos y aristas |
| 2 | Arista | Conexión entre dos nodos |
| 3 | Nodos distintos | El conjunto de vértices |

## 📖 Definiciones y características

- **Grafo** — conjunto de nodos conectados por aristas. Clave: modela relaciones.
- **Arista** — conexión entre dos nodos. Clave: aquí, un par de números.
- **Nodo (vértice)** — una entidad del grafo. Clave: contar los distintos = tamaño del conjunto.

## 🧩 Situación

Redes sociales, mapas de carreteras, dependencias de paquetes: todo son grafos. Contar nodos y aristas es la medida básica de su tamaño.

## 🧮 Modelo

- **Entrada** (stdin): una línea con pares de enteros (cada par es una arista)
- **Salida** (stdout): `aristas=<número de pares> nodos=<nodos distintos>`
- **Regla:** aristas = tokens/2 ; nodos = |conjunto de todos los números|

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `1 2 2 3` | `aristas=2 nodos=3` |
| `1 2` | `aristas=1 nodos=2` |
| `1 2 2 3 3 1` | `aristas=3 nodos=3` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER pares ; aristas <- pares ; nodos <- distintos
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
| Sintáctica | Conjunto de nodos + conteo de pares en cada lenguaje. |
| Semántica | El grafo puede guardarse como lista de aristas o de adyacencia. |
| Paradigmática | SQL modela grafos con tablas de nodos y aristas (relaciones). |

## 🧬 El concepto en la familia

En muchos lenguajes se usa un mapa de adyacencia `nodo → vecinos`. Aquí basta un conjunto para los nodos.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 098
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Contar nodos con repetición** → causa: sobreestimar los vértices → solución: usar un conjunto de nodos distintos
- **Suponer número impar de tokens** → causa: arista incompleta → solución: asumir pares completos (grafo bien formado)

## ❓ Preguntas frecuentes

- **¿Lista de aristas o adyacencia?** Aristas es simple para contar; adyacencia es mejor para recorrer vecinos.
- **¿Dirigido o no?** Aquí solo contamos; la dirección importaría para recorridos.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 097](../../parte-6-datos-y-estructuras/097-arboles/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 099 ⏭️](../../parte-6-datos-y-estructuras/099-registros-structs-y-clases/README.md)
