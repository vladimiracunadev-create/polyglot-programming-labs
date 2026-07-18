# Clase 125 — Bytecode y máquinas virtuales (JVM, CLR, V8)

> Parte **8 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Entender el **bytecode y las máquinas virtuales**: una VM ejecuta instրucciones simples sobre una pila. La notación polaca inversa (RPN) es exactamente cómo trabaja una VM de pila: apila operandos y aplica operadores.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Evaluar RPN con una pila.
2. Relacionar RPN con las VM de pila.
3. Explicar qué es el bytecode.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Máquina de pila | Opera sobre una pila de valores |
| 2 | RPN | Operandos primero, operador después |
| 3 | Bytecode | Instrucciones simples para la VM |

## 📖 Definiciones y características

- **Bytecode** — código intermedio de instrucciones simples que ejecuta una VM. Clave: portable (JVM, CLR).
- **Máquina virtual de pila** — VM que opera apilando y desapilando valores. Clave: `push 3, push 4, add`.
- **RPN** — notación donde el operador va tras los operandos. Clave: `3 4 +` = 7.

## 🧩 Situación

La JVM y el CLR ejecutan bytecode sobre una pila: apilan operandos y aplican operadores. Evaluar '3 4 +' con una pila reproduce ese mecanismo en pequeño.

## 🧮 Modelo

- **Entrada** (stdin): una línea `a b op` (dos enteros y un operador +, -, *)
- **Salida** (stdout): `resultado=<a op b>`
- **Regla:** apilar a y b; aplicar op; el tope es el resultado

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `3 4 +` | `resultado=7` |
| `5 6 *` | `resultado=30` |
| `10 2 -` | `resultado=8` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
PARA cada token: SI número, apilar; SI operador, desapilar 2, aplicar, apilar
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
| Sintáctica | Una pila (lista) en cada lenguaje. |
| Semántica | La VM de pila es el mismo modelo que la JVM/CLR. |
| Paradigmática | SQL no tiene pila explícita; evalúa la expresión. |

## 🧬 El concepto en la familia

La JVM (bytecode Java) y el CLR (.NET) son máquinas de pila. Python también usa una VM de pila.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 125
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Desapilar en orden equivocado** → causa: resta/división invertidas → solución: el primero desapilado es el segundo operando
- **Pila vacía al operar** → causa: expresión mal formada → solución: asumir RPN bien formada

## ❓ Preguntas frecuentes

- **¿Por qué VM de pila?** Simplicidad y portabilidad: las instrucciones no nombran registros.
- **¿RPN se usa de verdad?** Sí: calculadoras HP, PostScript y muchas VM internamente.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 124](../../parte-8-como-funcionan-los-lenguajes/124-compilador-interprete-y-jit/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 126 ⏭️](../../parte-8-como-funcionan-los-lenguajes/126-aot-vs-jit-costos-y-beneficios/README.md)
