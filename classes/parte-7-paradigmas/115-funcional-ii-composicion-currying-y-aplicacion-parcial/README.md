# Clase 115 — Funcional II: composición, currying y aplicación parcial

> Parte **7 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Practicar el paradigma **funcional (II)**: composición de funciones. Combinar funciones pequeñas (`doblar`, `incrementar`) en una mayor, aplicando primero una y luego la otra.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Componer dos funciones.
2. Aplicar la composición a un valor.
3. Reconocer la aplicación parcial/currying.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Composición | f(g(x)): encadenar funciones |
| 2 | Funciones pequeñas | Construir a partir de piezas |
| 3 | Currying | Funciones que devuelven funciones |

## 📖 Definiciones y características

- **Composición de funciones** — combinar funciones: `(f ∘ g)(x) = f(g(x))`. Clave: construir con piezas.
- **Currying** — transformar una función de varios argumentos en una cadena de funciones de uno. Clave: aplicación parcial.
- **Aplicación parcial** — fijar algunos argumentos y obtener una función nueva. Clave: reutilización.

## 🧩 Situación

En vez de escribir `x*2+1` a mano, se componen `doblar` e `incrementar`. Las funciones pequeñas y componibles son el corazón del estilo funcional.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n`
- **Salida** (stdout): `resultado=<2n+1>` (doblar y luego incrementar)
- **Regla:** resultado = incrementar(doblar(n)) = 2n + 1

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `5` | `resultado=11` |
| `0` | `resultado=1` |
| `3` | `resultado=7` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
doblar(x)=2x ; inc(x)=x+1 ; compuesta = inc ∘ doblar ; ESCRIBIR compuesta(n)
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
| Sintáctica | Composición explícita `inc(doblar(n))` o con operador de composición. |
| Semántica | El orden importa: doblar primero, luego incrementar. |
| Paradigmática | SQL anida funciones/expresiones. |

## 🧬 El concepto en la familia

En Haskell `(inc . doblar) n` con el operador `.`. En muchos lenguajes se anidan las llamadas.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 115
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Invertir el orden de composición** → causa: resultado distinto → solución: aplicar en el orden correcto
- **Componer funciones incompatibles** → causa: tipos que no encajan → solución: asegurar que la salida de una es la entrada de la otra

## ❓ Preguntas frecuentes

- **¿Composición o anidar llamadas?** Anidar es composición explícita; algunos lenguajes tienen un operador dedicado.
- **¿Currying para qué sirve?** Fijar argumentos y crear funciones especializadas reutilizables.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 114](../../parte-7-paradigmas/114-funcional-i-inmutabilidad-y-funciones-puras/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 116 ⏭️](../../parte-7-paradigmas/116-funcional-iii-functores-monadas-y-efectos-vision-practica/README.md)
