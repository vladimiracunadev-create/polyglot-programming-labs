# Clase 071 — Manejo de errores I: excepciones (try/catch/finally)

> Parte **4 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Manejar errores con **excepciones** (`try`/`catch`/`finally`): separar el camino feliz del manejo del error. Dividir por cero es el caso clásico que dispara una excepción en varios lenguajes.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Capturar una excepción con try/catch.
2. Distinguir el flujo normal del de error.
3. Reconocer qué lenguajes lanzan y cuáles no.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Excepción | Un error que interrumpe el flujo |
| 2 | try/catch | Intentar y capturar el fallo |
| 3 | finally | Código que corre pase lo que pase |
| 4 | Lanzar vs. comprobar | No todos lanzan en /0 |

## 📖 Definiciones y características

- **Excepción** — objeto que representa un error y desvía el flujo. Clave: se captura con try/catch.
- **try** — bloque que puede fallar. Clave: envuelve la operación arriesgada.
- **catch** — bloque que maneja la excepción. Clave: el plan B ante el error.
- **finally** — bloque que se ejecuta siempre (haya error o no). Clave: liberar recursos.

## 🧩 Situación

Dividir entre cero es un error clásico. En Java, C#, Python y PHP la división entera por cero lanza una excepción; capturarla evita que el programa termine abruptamente.

## 🧮 Modelo

- **Entrada** (stdin): una línea `a b` (dos enteros)
- **Salida** (stdout): `resultado=<a/b entera>` o `error=division por cero` si b es 0
- **Regla:** si b != 0 → a/b (entera); si b == 0 → mensaje de error

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `10 2` | `resultado=5` |
| `7 0` | `error=division por cero` |
| `9 3` | `resultado=3` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER a, b
INTENTAR: r <- a/b ; ESCRIBIR "resultado=" r
CAPTURAR division_por_cero: ESCRIBIR "error=division por cero"
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
| Sintáctica | `try/except` (Python), `try/catch` (Java/C#/JS/PHP). |
| Semántica | Java/C#/Python/PHP lanzan en /0 entero; JS da Infinity (hay que comprobar); Go/Rust no usan excepciones. |
| Paradigmática | SQL evita el error con CASE WHEN b=0. |

## 🧬 El concepto en la familia

En Ruby `begin/rescue/ensure`. En Kotlin `try/catch/finally`, como Java. Go y Rust prefieren valores de error (siguiente clase).

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 071
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Capturar todo con un catch vacío** → causa: ocultar errores reales → solución: capturar solo lo esperado y actuar
- **Asumir que /0 siempre lanza** → causa: en JS da Infinity, no excepción → solución: comprobar el divisor o el resultado según el lenguaje

## ❓ Preguntas frecuentes

- **¿Excepciones o valores de error?** Excepciones para lo excepcional; valores (Result) para errores esperables. La siguiente clase compara.
- **¿Para qué el finally?** Para liberar recursos (archivos, conexiones) ocurra o no un error.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 070](../../parte-4-control-del-programa/070-control-de-flujo-break-continue-return-goto/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 072 ⏭️](../../parte-4-control-del-programa/072-manejo-de-errores-ii-resultados-y-valores-result-either-error-de-go/README.md)
