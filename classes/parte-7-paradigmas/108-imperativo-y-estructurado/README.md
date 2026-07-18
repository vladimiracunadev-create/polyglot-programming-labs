# Clase 108 — Imperativo y estructurado

> Parte **7 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Practicar el **paradigma imperativo y estructurado**: describir la solución como una secuencia de pasos que modifican el estado (un acumulador), usando bucles y condiciones.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Resolver con estado mutable y bucles.
2. Reconocer la secuencia de pasos.
3. Contrastar con el estilo funcional.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Imperativo | Pasos que cambian el estado |
| 2 | Estructurado | Secuencia, selección, iteración |
| 3 | Estado mutable | Variables que cambian |

## 📖 Definiciones y características

- **Imperativo** — paradigma que describe cómo cambiar el estado paso a paso. Clave: bucles y asignaciones.
- **Estructurado** — usa solo secuencia, selección e iteración (sin goto). Clave: código claro.
- **Estado mutable** — variables que cambian durante la ejecución. Clave: el acumulador.

## 🧩 Situación

El estilo imperativo es el más cercano a cómo funciona la máquina: 'haz esto, luego esto'. Sumar con un acumulador y un bucle es su ejemplo puro.

## 🧮 Modelo

- **Entrada** (stdin): una línea con enteros separados por espacio
- **Salida** (stdout): `suma=<suma de todos>`
- **Regla:** acumular la suma recorriendo la lista

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `1 2 3` | `suma=6` |
| `5` | `suma=5` |
| `10 20` | `suma=30` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
suma <- 0 ; PARA CADA x: suma <- suma + x
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
| Sintáctica | Bucle explícito en todos los imperativos. |
| Semántica | Modifica un acumulador; el estado evoluciona. |
| Paradigmática | El funcional evitaría el acumulador mutable con reduce. |

## 🧬 El concepto en la familia

Casi todos los lenguajes del núcleo soportan el estilo imperativo de forma nativa.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 108
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **No inicializar el acumulador** → causa: resultado incorrecto → solución: empezar en 0
- **Efectos secundarios ocultos** → causa: estado difícil de seguir → solución: mantener el estado local y claro

## ❓ Preguntas frecuentes

- **¿Imperativo o funcional?** Imperativo es directo y eficiente; funcional es más declarativo. Depende.
- **¿Estructurado significa sin goto?** Sí: solo secuencia, selección e iteración.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 107](../../parte-7-paradigmas/107-que-es-un-paradigma-y-por-que-importa/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 109 ⏭️](../../parte-7-paradigmas/109-procedimental-y-modular/README.md)
