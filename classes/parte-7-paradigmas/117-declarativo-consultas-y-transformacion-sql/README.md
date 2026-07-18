# Clase 117 — Declarativo: consultas y transformación (SQL)

> Parte **7 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Practicar el paradigma **declarativo**: describir *qué* resultado se quiere, no *cómo* obtenerlo. Sumar los pares se expresa como 'la suma de los que son pares', dejando el cómo al lenguaje.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Expresar un cálculo de forma declarativa.
2. Combinar filtro y agregación.
3. Contrastar con el estilo imperativo.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Declarativo | Describir el resultado |
| 2 | Filtro + agregación | Seleccionar y combinar |
| 3 | SQL como declarativo | WHERE + SUM |

## 📖 Definiciones y características

- **Declarativo** — paradigma que describe el resultado deseado, no los pasos. Clave: el motor decide el cómo.
- **Filtro** — seleccionar los elementos que cumplen una condición. Clave: `WHERE`, `filter`.
- **Agregación** — combinar varios valores en uno (suma). Clave: `SUM`, `reduce`.

## 🧩 Situación

'La suma de los pedidos pagados', 'el total de las ventas del mes': el estilo declarativo describe el resultado. SQL es su máximo exponente: `SELECT SUM(x) WHERE ...`.

## 🧮 Modelo

- **Entrada** (stdin): una línea con enteros separados por espacio
- **Salida** (stdout): `suma_pares=<suma de los pares>`
- **Regla:** suma de los x tales que x es par

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `1 2 3 4` | `suma_pares=6` |
| `2 4 6` | `suma_pares=12` |
| `1 3 5` | `suma_pares=0` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
suma_pares <- SUMA(FILTRAR(par, lista))
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
| Sintáctica | `sum(x for x in l if x%2==0)` (Python), `filter+reduce` (JS), `WHERE+SUM` (SQL). |
| Semántica | Se describe el resultado; el cómo queda implícito. |
| Paradigmática | El imperativo recorrería y acumularía a mano. |

## 🧬 El concepto en la familia

En Haskell `sum (filter even xs)`. SQL es el declarativo por excelencia.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 117
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Mezclar el cómo con el qué** → causa: perder la claridad declarativa → solución: describir el resultado, dejar el cómo al lenguaje
- **Olvidar el caso sin pares** → causa: esperar error en vez de 0 → solución: la suma vacía es 0

## ❓ Preguntas frecuentes

- **¿Declarativo siempre es mejor?** Es más legible para transformaciones de datos; el imperativo da más control fino.
- **¿SQL es declarativo?** Sí, el ejemplo canónico: describes el resultado, no el algoritmo.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 116](../../parte-7-paradigmas/116-funcional-iii-functores-monadas-y-efectos-vision-practica/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 118 ⏭️](../../parte-7-paradigmas/118-logico-reglas-hechos-y-unificacion-prolog/README.md)
