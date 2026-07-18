# Clase 076 — Parámetros variádicos

> Parte **5 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Definir una función **variádica**: acepta un número variable de argumentos. Es lo que hay detrás de `print(...)` o `sum(...)`. Cada lenguaje lo expresa con `*args`, `...`, `params` o slices.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Definir una función que acepta N argumentos.
2. Recorrer los argumentos variádicos.
3. Reconocer la sintaxis de cada lenguaje.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Función variádica | Número variable de argumentos |
| 2 | Recolectar en una colección | Los argumentos llegan como lista/slice |
| 3 | Sintaxis por lenguaje | *args, ..., params[] |
| 4 | Usos comunes | print, sum, format |

## 📖 Definiciones y características

- **Función variádica** — acepta un número variable de argumentos. Clave: `sum(1,2,3,...)`.
- ***args / ...** — sintaxis para recolectar argumentos variables. Clave: llegan como colección.
- **Empaquetar** — reunir los argumentos sueltos en una lista. Clave: dentro de la función.
- **Desempaquetar** — expandir una lista en argumentos sueltos. Clave: la operación inversa.

## 🧩 Situación

`printf`, `sum`, `max` aceptan cuantos argumentos quieras. Una función variádica los recibe como una colección y los procesa; es la base de muchas utilidades.

## 🧮 Modelo

- **Entrada** (stdin): una línea con enteros separados por espacio
- **Salida** (stdout): `suma=<suma de todos>`
- **Regla:** suma(...nums) = Σ nums

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `1 2 3` | `suma=6` |
| `5` | `suma=5` |
| `10 20 30 40` | `suma=100` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
FUNCION suma(...nums): DEVOLVER Σ nums
LEER lista ; ESCRIBIR "suma=" suma(lista)
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
| Sintáctica | `*nums` (Python), `...nums` (JS/Java), `nums ...int` (Go), `&[i64]` (Rust). |
| Semántica | Los argumentos se recolectan en una colección dentro de la función. |
| Paradigmática | SQL agrega filas con SUM(), no argumentos. |

## 🧬 El concepto en la familia

En Ruby `def suma(*nums)`. En C, `stdarg.h` con `va_list` (más manual).

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 076
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Confundir empaquetar con desempaquetar** → causa: pasar una lista donde se esperan sueltos → solución: usar el operador de expansión (`*`, `...`) al desempaquetar
- **Olvidar el caso de cero argumentos** → causa: error o suma indefinida → solución: que la función maneje la lista vacía (suma 0)

## ❓ Preguntas frecuentes

- **¿Variádica o pasar una lista?** Variádica para llamadas cómodas; lista cuando ya la tienes construida.
- **¿C tiene variádicas?** Sí, con `stdarg.h`, pero es más manual y propenso a errores.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 075](../../parte-5-funciones-y-modularidad/075-argumentos-nombrados-y-de-palabra-clave/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 077 ⏭️](../../parte-5-funciones-y-modularidad/077-multiples-retornos-y-desestructuracion/README.md)
