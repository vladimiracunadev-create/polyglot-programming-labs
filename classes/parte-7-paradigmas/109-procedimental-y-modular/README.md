# Clase 109 — Procedimental y modular

> Parte **7 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Practicar el **paradigma procedimental y modular**: descomponer el programa en procedimientos con nombre que se llaman entre sí. Es el imperativo organizado en unidades reutilizables.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Encapsular un cálculo en un procedimiento.
2. Llamarlo desde el programa principal.
3. Reconocer la modularidad procedimental.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Procedimiento | Bloque con nombre reutilizable |
| 2 | Modularidad | Dividir en unidades |
| 3 | Reutilización | Llamar en vez de repetir |

## 📖 Definiciones y características

- **Procedimental** — paradigma que organiza el código en procedimientos/funciones. Clave: imperativo modular.
- **Procedimiento** — unidad con nombre que realiza una tarea. Clave: se invoca cuando se necesita.
- **Modularidad** — dividir el problema en piezas manejables. Clave: cada una con una responsabilidad.

## 🧩 Situación

En vez de un `main` gigante, se define `promedio(lista)` y se llama. El estilo procedimental (C, Pascal) organiza el imperativo en procedimientos.

## 🧮 Modelo

- **Entrada** (stdin): una línea con enteros separados por espacio
- **Salida** (stdout): `promedio=<suma dividida entre la cantidad, entera>`
- **Regla:** promedio = suma / cantidad (división entera)

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `2 4 6` | `promedio=4` |
| `10` | `promedio=10` |
| `3 5` | `promedio=4` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
PROCEDIMIENTO promedio(lista): DEVOLVER suma(lista)/|lista|
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
| Sintáctica | Cada lenguaje define el procedimiento a su manera. |
| Semántica | El procedimiento agrupa pasos imperativos bajo un nombre. |
| Paradigmática | SQL usa AVG (declarativo). |

## 🧬 El concepto en la familia

C y Pascal son los ejemplos clásicos del estilo procedimental; casi todos lo soportan.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 109
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Dividir sin controlar cantidad 0** → causa: división por cero → solución: aquí siempre hay elementos
- **Todo en el main** → causa: sin modularidad → solución: extraer procedimientos con responsabilidad clara

## ❓ Preguntas frecuentes

- **¿Procedimiento o función?** Un procedimiento actúa; una función devuelve valor. Aquí devolvemos el promedio.
- **¿Procedimental es viejo?** Es la base; sigue vigente y presente en todos los lenguajes.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 108](../../parte-7-paradigmas/108-imperativo-y-estructurado/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 110 ⏭️](../../parte-7-paradigmas/110-orientado-a-objetos-clases-objetos-y-estado/README.md)
