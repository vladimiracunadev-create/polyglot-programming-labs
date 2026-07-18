# Clase 061 — switch, case y fallthrough

> Parte **4 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Usar `switch` / `case` (o su equivalente) para elegir entre valores exactos, con un caso por defecto. Verás el `fallthrough` (caída) de C/Java y cómo otros lenguajes lo evitan.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Seleccionar por valor exacto con switch/case.
2. Usar el caso por defecto.
3. Explicar el fallthrough y cómo lo maneja cada lenguaje.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | switch/case | Elegir por valor exacto |
| 2 | default | El caso por defecto |
| 3 | Fallthrough | Caída de un caso al siguiente (C/Java) |
| 4 | Alternativas | match/when sin caída |

## 📖 Definiciones y características

- **switch** — estructura que elige una rama según el valor exacto. Clave: para muchos valores concretos.
- **case** — una de las ramas del switch. Clave: coincide con un valor.
- **fallthrough** — en C/Java, un case sigue al siguiente si falta `break`. Clave: fuente de bugs.
- **default** — rama que se ejecuta si ningún case coincide. Clave: cubre lo inesperado.

## 🧩 Situación

Traducir un código a un nombre (día, mes, estado) es el caso típico de switch. Olvidar un `break` en C/Java hace 'caer' al siguiente case: un error clásico que otros lenguajes evitan por diseño.

## 🧮 Modelo

- **Entrada** (stdin): un entero `d` (día)
- **Salida** (stdout): `dia=<nombre>` o `dia=invalido`
- **Regla:** 1→lunes … 7→domingo; otro→invalido

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `1` | `dia=lunes` |
| `6` | `dia=sabado` |
| `8` | `dia=invalido` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER d
SEGUN d: 1..7 -> nombre ; otro -> invalido
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
| Sintáctica | `switch` con `break` (C/Java/JS) vs. `match` (Rust) vs. `when` (Kotlin). |
| Semántica | C/Java caen sin `break`; Go, Rust y el switch de Python (match) no caen. |
| Paradigmática | SQL usa CASE WHEN valor. |

## 🧬 El concepto en la familia

En Ruby `case d; when 1 then 'lunes'`. En Kotlin `when (d) { 1 -> ... }`. Ninguno cae como C.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 061
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Olvidar `break` en C/Java** → causa: el flujo cae al siguiente case → solución: poner `break` en cada case o usar match/when
- **No manejar valores fuera de rango** → causa: salida vacía o error → solución: incluir siempre el caso por defecto

## ❓ Preguntas frecuentes

- **¿Por qué existe el fallthrough?** Herencia de C; a veces útil, pero suele ser un error olvidar el break.
- **¿Go tiene fallthrough?** No por defecto: hay que pedirlo con la palabra `fallthrough` explícita.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 060](../../parte-4-control-del-programa/060-expresiones-condicionales-ternario-e-if-como-expresion/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 062 ⏭️](../../parte-4-control-del-programa/062-coincidencia-de-patrones-match-when/README.md)
