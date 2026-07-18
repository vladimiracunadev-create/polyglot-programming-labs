# Clase 114 — Funcional I: inmutabilidad y funciones puras

> Parte **7 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Practicar el paradigma **funcional (I)**: inmutabilidad y funciones puras. Transformar una lista con `map` produce una lista nueva sin alterar la original ni usar estado mutable.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Transformar una colección sin mutarla.
2. Reconocer la inmutabilidad.
3. Usar map en lugar de un bucle con estado.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Inmutabilidad | No modificar, crear nuevo |
| 2 | map | Transformar cada elemento |
| 3 | Sin estado mutable | Sin acumuladores |

## 📖 Definiciones y características

- **Funcional** — paradigma basado en funciones puras e inmutabilidad. Clave: sin efectos ni estado mutable.
- **Inmutabilidad** — los datos no cambian; las transformaciones crean nuevos. Clave: más seguro.
- **map** — aplica una función a cada elemento y devuelve una colección nueva. Clave: no muta.

## 🧩 Situación

En vez de recorrer y mutar, el estilo funcional describe la transformación: 'la lista de los dobles'. La original queda intacta, lo que evita errores por estado compartido.

## 🧮 Modelo

- **Entrada** (stdin): una línea con enteros separados por espacio
- **Salida** (stdout): `doblados=<cada x·2 unidos por ->`
- **Regla:** doblados = map(x → 2x, lista)

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `1 2 3` | `doblados=2-4-6` |
| `5` | `doblados=10` |
| `2 4` | `doblados=4-8` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
doblados <- MAP(x -> 2x, lista) ; ESCRIBIR unidos por -
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
| Sintáctica | `map` (Python/JS/Rust), streams (Java), LINQ Select (C#). |
| Semántica | No muta la lista original; devuelve otra. |
| Paradigmática | SQL transforma en el SELECT, sin mutar. |

## 🧬 El concepto en la familia

En Haskell `map (*2) xs` es el ejemplo puro. Casi todos ofrecen map.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 114
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Mutar dentro del map** → causa: efecto secundario → solución: mantener la transformación pura
- **Confundir map con for-each** → causa: map devuelve; for-each no → solución: usar map cuando quieres el resultado

## ❓ Preguntas frecuentes

- **¿Map es más lento que un bucle?** Generalmente comparable; y evita errores de estado.
- **¿Inmutabilidad no gasta memoria?** Crea nuevos datos, pero permite compartir y razonar mejor.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 113](../../parte-7-paradigmas/113-oo-basado-en-prototipos-javascript/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 115 ⏭️](../../parte-7-paradigmas/115-funcional-ii-composicion-currying-y-aplicacion-parcial/README.md)
