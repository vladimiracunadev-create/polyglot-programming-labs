# Clase 123 — Del código a la ejecución: fases de compilación

> Parte **8 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Ver las **fases de compilación** en miniatura: separar la entrada en tokens (léxico), reconocer su estructura (sintáctico) y calcular el resultado (evaluación). Todo compilador o intérprete hace esto a mayor escala.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Separar una entrada en tokens.
2. Interpretar la estructura de una expresión.
3. Nombrar las fases de compilación.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Análisis léxico | De texto a tokens |
| 2 | Análisis sintáctico | Reconocer la estructura |
| 3 | Evaluación | Producir el resultado |

## 📖 Definiciones y características

- **Análisis léxico (lexer)** — divide el texto en tokens. Clave: '3 + 4' → [3, +, 4].
- **Análisis sintáctico (parser)** — reconoce la estructura de los tokens. Clave: expresión = número op número.
- **Evaluación** — calcula el resultado a partir de la estructura. Clave: aplica el operador.

## 🧩 Situación

Cuando compilas o ejecutas código, el lenguaje primero lo tokeniza, luego lo parsea y por fin lo evalúa o traduce. Este mini-evaluador muestra esas fases con una operación simple.

## 🧮 Modelo

- **Entrada** (stdin): una línea `a op b` (dos enteros y un operador +, -, *)
- **Salida** (stdout): `resultado=<a op b>`
- **Regla:** aplicar el operador a los dos operandos

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `3 + 4` | `resultado=7` |
| `10 - 2` | `resultado=8` |
| `5 * 6` | `resultado=30` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
TOKENIZAR ; RECONOCER (num op num) ; EVALUAR
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
| Sintáctica | Cada lenguaje tokeniza y evalúa a su manera. |
| Semántica | Las fases son universales: lexer, parser, evaluador. |
| Paradigmática | SQL evalúa expresiones en la consulta. |

## 🧬 El concepto en la familia

Todo compilador (gcc, javac, rustc) y todo intérprete (CPython, V8) sigue estas fases.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 123
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Mezclar léxico con sintaxis** → causa: confundir tokens con estructura → solución: separar las fases mentalmente
- **Operador no soportado** → causa: caso sin manejar → solución: cubrir los operadores esperados

## ❓ Preguntas frecuentes

- **¿Compilar es solo estas fases?** Son el núcleo; hay más (optimización, generación de código).
- **¿Un intérprete parsea?** Sí: también tokeniza y parsea antes de ejecutar.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 122](../../parte-7-paradigmas/122-asincrono-async-await-y-promesas/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 124 ⏭️](../../parte-8-como-funcionan-los-lenguajes/124-compilador-interprete-y-jit/README.md)
