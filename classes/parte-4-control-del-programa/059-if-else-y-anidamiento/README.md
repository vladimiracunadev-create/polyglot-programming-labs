# Clase 059 — if / else y anidamiento

> Parte **4 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Practicar `if` / `else if` encadenados para clasificar en varios rangos. Es la estructura de decisión más común y la base de toda ramificación.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Encadenar if/else para varios rangos.
2. Ordenar los umbrales correctamente.
3. Cubrir el caso por defecto (else).

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | if / else if / else | Elegir entre varias ramas |
| 2 | Rangos ordenados | De mayor a menor umbral |
| 3 | Caso por defecto | El else que recoge lo demás |
| 4 | Exclusividad | Solo una rama se ejecuta |

## 📖 Definiciones y características

- **if** — ejecuta un bloque si la condición es verdadera. Clave: la decisión básica.
- **else if** — condición alternativa si la anterior falló. Clave: encadena rangos.
- **else** — rama por defecto si ninguna condición se cumple. Clave: cubre el resto.
- **Umbral** — valor límite que separa dos categorías. Clave: su orden importa.

## 🧩 Situación

Asignar una nota por tramos aparece en todas partes: descuentos por volumen, niveles de riesgo, categorías. Si los umbrales se comprueban en mal orden, la clasificación falla.

## 🧮 Modelo

- **Entrada** (stdin): un entero `score` (0-100)
- **Salida** (stdout): `nota=<A|B|C|F>`
- **Regla:** score>=90→A; >=80→B; >=70→C; si no→F

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `95` | `nota=A` |
| `72` | `nota=C` |
| `40` | `nota=F` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER score
SI score>=90: A
SINO SI score>=80: B
SINO SI score>=70: C
SINO: F
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
| Sintáctica | `elif` (Python) vs. `else if` (C/Java/JS) vs. `else if` con llaves. |
| Semántica | Solo se ejecuta la primera rama verdadera; el orden descendente es clave. |
| Paradigmática | SQL usa CASE WHEN con los umbrales en orden. |

## 🧬 El concepto en la familia

En Ruby se usa `if/elsif/else` o un `case` con rangos (`when 90..100`). En Kotlin, `when` con rangos es idiomático.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 059
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Comprobar los umbrales de menor a mayor** → causa: todo cae en la primera rama → solución: ordenar de mayor a menor umbral
- **Olvidar el else** → causa: no clasificar algunos valores → solución: incluir siempre un caso por defecto

## ❓ Preguntas frecuentes

- **¿Puedo usar switch aquí?** Para rangos, if/else o `when`/`match` con rangos; el switch clásico es para valores exactos.
- **¿Importa el orden?** Mucho: la primera condición verdadera gana, así que van de más a menos exigente.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 058](../../parte-4-control-del-programa/058-guardas-y-validacion-temprana/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 060 ⏭️](../../parte-4-control-del-programa/060-expresiones-condicionales-ternario-e-if-como-expresion/README.md)
