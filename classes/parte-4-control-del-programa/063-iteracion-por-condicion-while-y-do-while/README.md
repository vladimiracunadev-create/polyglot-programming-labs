# Clase 063 — Iteración por condición: while y do-while

> Parte **4 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Usar el bucle `while`: repetir mientras una condición sea verdadera. Es el bucle más básico y el que subyace a todos los demás.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Escribir un bucle while con una condición de parada.
2. Actualizar el estado en cada vuelta.
3. Evitar el bucle infinito.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | while | Repetir mientras se cumpla una condición |
| 2 | Condición de parada | Cuándo termina el bucle |
| 3 | Acumulador | Sumar en cada vuelta |
| 4 | Bucle infinito | El peligro de no avanzar |

## 📖 Definiciones y características

- **while** — bucle que repite mientras la condición sea verdadera. Clave: comprueba antes de cada vuelta.
- **do-while** — variante que ejecuta al menos una vez (comprueba al final). Clave: no en todos los lenguajes.
- **Condición de parada** — lo que hace terminar el bucle. Clave: algo debe acercarse a ella.
- **Acumulador** — variable que reúne el resultado. Clave: se actualiza cada vuelta.

## 🧩 Situación

Sumar 1..n con while obliga a manejar el contador y la condición a mano. Si el contador no avanza, el bucle no termina: el error más clásico de los bucles.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n` (n >= 1)
- **Salida** (stdout): `suma=<1+2+...+n>`
- **Regla:** suma = 1 + 2 + ... + n

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `5` | `suma=15` |
| `1` | `suma=1` |
| `10` | `suma=55` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER n
suma <- 0 ; i <- 1
MIENTRAS i <= n: suma <- suma+i ; i <- i+1
ESCRIBIR "suma=" suma
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
| Sintáctica | `while cond:` (Python) vs. `while (cond) {}` (C/Java/JS). |
| Semántica | El while comprueba antes; el do-while (C/Java/JS) al menos una vez. |
| Paradigmática | SQL evita el bucle: suma con un CTE recursivo o una fórmula. |

## 🧬 El concepto en la familia

En Ruby `while i <= n`. En Go solo hay `for` (que hace de while): `for i <= n`. Rust `while i <= n`.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 063
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **No avanzar el contador** → causa: bucle infinito → solución: asegurar que algo cambia hacia la condición de parada
- **Condición mal puesta** → causa: una vuelta de más o de menos (off-by-one) → solución: verificar los límites con un caso pequeño

## ❓ Preguntas frecuentes

- **¿while o for?** El for es más compacto cuando el número de vueltas se conoce; el while, cuando depende de una condición.
- **¿Go no tiene while?** No como palabra: usa `for cond {}`, que es lo mismo.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 062](../../parte-4-control-del-programa/062-coincidencia-de-patrones-match-when/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 064 ⏭️](../../parte-4-control-del-programa/064-iteracion-por-rango-for-clasico-y-for-range/README.md)
