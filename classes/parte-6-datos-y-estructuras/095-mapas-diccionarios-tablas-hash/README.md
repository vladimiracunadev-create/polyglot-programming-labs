# Clase 095 — Mapas / diccionarios / tablas hash

> Parte **6 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Usar un **mapa (diccionario)**: asociar claves con valores. Contar frecuencias es el uso más común: la clave es el número y el valor, cuántas veces aparece.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Construir un mapa de frecuencias.
2. Consultar el valor de una clave.
3. Reconocer el acceso por clave en O(1).

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Mapa/diccionario | Clave → valor |
| 2 | Frecuencias | Contar apariciones |
| 3 | Acceso por clave | Búsqueda rápida |

## 📖 Definiciones y características

- **Mapa** — colección de pares clave→valor (dict, HashMap). Clave: búsqueda por clave en O(1).
- **Clave** — identificador único de una entrada. Clave: no se repite.
- **Frecuencia** — cuántas veces aparece un valor. Clave: uso típico del mapa.

## 🧩 Situación

Contar palabras, votos, visitas por página: el mapa asocia cada cosa con su cuenta y la actualiza al instante.

## 🧮 Modelo

- **Entrada** (stdin): una línea con enteros separados por espacio
- **Salida** (stdout): `cuenta=<veces que aparece el primer elemento>`
- **Regla:** cuenta = frecuencia[lista[0]]

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `3 1 3 3` | `cuenta=3` |
| `5 5` | `cuenta=2` |
| `7 1 2` | `cuenta=1` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER lista ; construir mapa de frecuencias ; ESCRIBIR frecuencia del primero
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
| Sintáctica | `dict` (Python), `{}`/Map (JS), `HashMap` (Java/Rust), `Dictionary` (C#). |
| Semántica | El mapa no garantiza orden de claves; C lo simula con arreglos. |
| Paradigmática | SQL agrupa con GROUP BY. |

## 🧬 El concepto en la familia

En Ruby `Hash.new(0)` para contar. En Go `map[int]int` es idiomático.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 095
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Leer una clave inexistente sin defecto** → causa: error o valor nulo → solución: inicializar con 0 o comprobar la existencia
- **Asumir orden de inserción** → causa: no siempre garantizado → solución: usar mapas ordenados si lo necesitas

## ❓ Preguntas frecuentes

- **¿Mapa o lista de pares?** Mapa para búsqueda rápida por clave; lista de pares si el orden importa.
- **¿Las claves pueden ser cualquier cosa?** Suelen requerir ser hashables/comparables; números y cadenas siempre valen.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 094](../../parte-6-datos-y-estructuras/094-conjuntos-sets-y-unicidad/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 096 ⏭️](../../parte-6-datos-y-estructuras/096-pilas-y-colas/README.md)
