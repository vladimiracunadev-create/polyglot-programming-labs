# Clase 074 — Parámetros por defecto y opcionales

> Parte **5 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Usar **parámetros por defecto**: un parámetro que toma un valor predefinido si no se pasa. Permite funciones flexibles sin sobrecargarlas. C y Go no los tienen; se simula.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Definir un parámetro con valor por defecto.
2. Llamar la función con y sin ese argumento.
3. Reconocer lenguajes sin parámetros por defecto.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Parámetro por defecto | Valor usado si no se pasa |
| 2 | Argumento opcional | Se puede omitir |
| 3 | Flexibilidad | Una función, varios usos |
| 4 | Sin soporte nativo | C y Go lo simulan |

## 📖 Definiciones y características

- **Parámetro por defecto** — toma un valor predefinido si el argumento se omite. Clave: `exp=2`.
- **Argumento opcional** — el que se puede no pasar. Clave: cae en el valor por defecto.
- **Sobrecarga** — varias funciones con el mismo nombre y distinta firma. Clave: alternativa en Java/C.
- **Simular defecto** — en C/Go, con dos funciones o comprobando la ausencia. Clave: no es nativo.

## 🧩 Situación

`potencia(base, exp=2)` permite `potencia(3)` = 9 y `potencia(2, 3)` = 8 con una sola definición. Sin defectos habría que escribir dos funciones o pasar siempre el exponente.

## 🧮 Modelo

- **Entrada** (stdin): una línea: `base` (exp por defecto 2) o `base exp`
- **Salida** (stdout): `resultado=<base^exp>`
- **Regla:** potencia(base, exp=2) = base^exp

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `3` | `resultado=9` |
| `2 3` | `resultado=8` |
| `5` | `resultado=25` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER tokens
base <- tokens[0] ; exp <- tokens[1] SI EXISTE SINO 2
ESCRIBIR "resultado=" base^exp
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
| Sintáctica | `def f(base, exp=2)` (Python) vs. simulación con comprobación (C/Go). |
| Semántica | Python/JS/C#/PHP tienen defectos nativos; C/Go no. |
| Paradigmática | SQL usa COALESCE para valores por defecto. |

## 🧬 El concepto en la familia

En Ruby `def potencia(base, exp = 2)`. En Kotlin `fun potencia(base: Int, exp: Int = 2)`.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 074
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Poner el parámetro con defecto antes de uno obligatorio** → causa: error de definición → solución: los parámetros con defecto van al final
- **Asumir defectos en C/Go** → causa: no existen → solución: simular con dos funciones o comprobando argumentos

## ❓ Preguntas frecuentes

- **¿Todos los lenguajes tienen defectos?** No: C y Go no; se simulan con sobrecarga o comprobación.
- **¿El defecto se evalúa una vez?** Cuidado en Python con defectos mutables (lista): se comparten entre llamadas.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 073](../../parte-5-funciones-y-modularidad/073-firma-parametros-argumentos-y-retorno/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 075 ⏭️](../../parte-5-funciones-y-modularidad/075-argumentos-nombrados-y-de-palabra-clave/README.md)
