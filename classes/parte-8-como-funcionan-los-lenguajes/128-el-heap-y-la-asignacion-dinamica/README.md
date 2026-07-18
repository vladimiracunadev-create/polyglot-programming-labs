# Clase 128 — El heap y la asignación dinámica

> Parte **8 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Entender el **heap y la asignación dinámica**: cuando el tamaño de los datos no se conoce en compilación, se reservan en el heap. Una lista dinámica que crece con n vive en el heap.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Construir una estructura de tamaño dinámico.
2. Distinguir stack de heap.
3. Reconocer la asignación dinámica.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Heap | Memoria de vida y tamaño flexibles |
| 2 | Asignación dinámica | Reservar en ejecución |
| 3 | Stack vs. heap | Automático vs. gestionado |

## 📖 Definiciones y características

- **Heap** — región de memoria para datos de tamaño/vida no conocidos en compilación. Clave: más flexible que la pila.
- **Asignación dinámica** — reservar memoria en ejecución (una lista que crece). Clave: heap.
- **Stack vs. heap** — la pila es automática y rápida; el heap es flexible pero requiere gestión. Clave: distinto uso.

## 🧩 Situación

Una lista cuyo tamaño depende de la entrada (n) no cabe en la pila con tamaño fijo: se asigna en el heap. Casi todas las colecciones dinámicas viven ahí.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n` (n >= 1)
- **Salida** (stdout): `lista=<n-(n-1)-...-1>`
- **Regla:** lista dinámica con los valores de n a 1

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `3` | `lista=3-2-1` |
| `1` | `lista=1` |
| `5` | `lista=5-4-3-2-1` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
reservar lista ; añadir n, n-1, ..., 1 ; unir por -
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
| Sintáctica | list/Vec/ArrayList (heap) en cada lenguaje. |
| Semántica | El tamaño dinámico obliga al heap; C usa malloc. |
| Paradigmática | SQL genera la secuencia con un CTE. |

## 🧬 El concepto en la familia

En C la lista dinámica se hace con malloc/realloc; en los demás, las colecciones ya viven en el heap.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 128
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Asumir tamaño fijo** → causa: no cabe en la pila → solución: usar una estructura dinámica
- **Fugas al no liberar (C)** → causa: memoria perdida → solución: liberar con free lo asignado

## ❓ Preguntas frecuentes

- **¿Todo va al heap?** No: los locales pequeños van a la pila; lo dinámico o grande, al heap.
- **¿El heap es más lento?** Su asignación cuesta más que la pila, pero permite tamaños flexibles.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 127](../../parte-8-como-funcionan-los-lenguajes/127-la-pila-stack-y-el-marco-de-llamada/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 129 ⏭️](../../parte-8-como-funcionan-los-lenguajes/129-referencias-apuntadores-y-direcciones/README.md)
