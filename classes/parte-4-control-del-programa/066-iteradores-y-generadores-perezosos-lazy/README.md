# Clase 066 — Iteradores y generadores perezosos (lazy)

> Parte **4 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Producir una secuencia bajo demanda, la idea detrás de los **iteradores y generadores perezosos**: calcular los valores uno a uno en lugar de tener toda la lista de antemano.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Generar una secuencia de longitud n.
2. Reconocer la evaluación perezosa (lazy).
3. Distinguir generar de tener ya calculado.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Generar bajo demanda | Producir valores al pedirlos |
| 2 | Perezoso (lazy) | No calcular hasta que se necesita |
| 3 | Iterador | Objeto que entrega el siguiente valor |
| 4 | take n | Tomar solo los primeros n |

## 📖 Definiciones y características

- **Iterador** — objeto que produce valores uno a uno. Clave: no necesita toda la colección en memoria.
- **Generador** — función que produce una secuencia perezosa (yield). Clave: calcula al vuelo.
- **Evaluación perezosa** — calcular un valor solo cuando se pide. Clave: permite secuencias infinitas.
- **take** — tomar los primeros n de una secuencia. Clave: corta lo infinito.

## 🧩 Situación

Los pares no tienen fin. Con un generador perezoso pides 'los primeros n' sin construir una lista infinita: cada valor se calcula cuando lo necesitas. Es como abrir el grifo solo lo justo.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n` (n >= 1)
- **Salida** (stdout): `pares=<2-4-...-2n>`
- **Regla:** pares_i = 2·i para i de 1 a n

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `3` | `pares=2-4-6` |
| `1` | `pares=2` |
| `5` | `pares=2-4-6-8-10` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER n
PARA i de 1 a n: emitir 2*i
ESCRIBIR "pares=" UNIR(emitidos, "-")
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
| Sintáctica | `(2*i for i in ...)` (Python) vs. `(1..=n).map(...)` (Rust) vs. bucle (C/Java). |
| Semántica | Python/Rust generan perezosamente; C/Java construyen la lista al vuelo. |
| Paradigmática | SQL genera con un CTE recursivo. |

## 🧬 El concepto en la familia

En Ruby `(1..n).map { |i| i*2 }` o un `Enumerator` perezoso. En Haskell `take n [2,4..]` sobre una lista infinita.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 066
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Construir una lista infinita entera** → causa: memoria agotada → solución: generar perezosamente y tomar solo n
- **Olvidar el separador en n=1** → causa: un guion sobrante → solución: unir con el separador, no anteponerlo

## ❓ Preguntas frecuentes

- **¿Qué gana la pereza?** Trabajar con secuencias enormes o infinitas usando solo lo que consumes.
- **¿Python genera perezoso?** Sí, con generadores (`yield`) y expresiones generadoras `( ... for ... )`.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 065](../../parte-4-control-del-programa/065-iteracion-por-coleccion-for-each-e-iteradores/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 067 ⏭️](../../parte-4-control-del-programa/067-comprensiones-de-listas-y-colecciones/README.md)
