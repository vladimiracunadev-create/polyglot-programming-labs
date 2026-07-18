# Clase 077 — Múltiples retornos y desestructuración

> Parte **5 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Devolver **más de un valor** de una función y **desestructurarlos** al recibirlos. Go y Python lo hacen nativamente; otros usan tuplas, arreglos u objetos.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Devolver varios valores de una función.
2. Desestructurar el resultado en variables.
3. Comparar tuplas, arreglos y objetos como vehículo.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Múltiples retornos | Más de un valor de salida |
| 2 | Tupla | Agrupar valores sin nombre |
| 3 | Desestructuración | Repartir en variables |
| 4 | Vehículos | Tupla, arreglo, struct u objeto |

## 📖 Definiciones y características

- **Múltiple retorno** — una función devuelve varios valores. Clave: nativo en Go, Python, Rust.
- **Tupla** — grupo ordenado de valores. Clave: el vehículo habitual del multi-retorno.
- **Desestructuración** — repartir una tupla/objeto en variables. Clave: `q, r = divmod(a, b)`.
- **Struct/objeto de salida** — en Java/C se devuelve un objeto con campos. Clave: alternativa al multi-retorno.

## 🧩 Situación

`divmod(17, 5)` devuelve cociente 3 y resto 2 de una vez. Sin multi-retorno habría que llamar dos veces o crear un objeto solo para eso.

## 🧮 Modelo

- **Entrada** (stdin): una línea `a b` (enteros positivos, b != 0)
- **Salida** (stdout): `cociente=<a/b> resto=<a%b>`
- **Regla:** (cociente, resto) = (a/b, a%b)

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `17 5` | `cociente=3 resto=2` |
| `10 2` | `cociente=5 resto=0` |
| `7 3` | `cociente=2 resto=1` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
FUNCION divmod(a,b): DEVOLVER (a/b, a%b)
LEER a,b ; (q,r) <- divmod(a,b) ; ESCRIBIR q, r
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
| Sintáctica | `q, r = ...` (Python/Go/Rust) vs. objeto/arreglo (Java/JS). |
| Semántica | Go/Python devuelven varios valores; Java devuelve un objeto contenedor. |
| Paradigmática | SQL devuelve varias columnas por fila, un multi-retorno natural. |

## 🧬 El concepto en la familia

En Ruby `return q, r` (una tupla). En Kotlin, un `Pair` o un `data class`.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 077
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Devolver un objeto solo para dos valores** → causa: sobre-ingeniería en lenguajes con tuplas → solución: usar el multi-retorno nativo si existe
- **Orden de la desestructuración** → causa: asignar cociente al resto → solución: respetar el orden de los valores devueltos

## ❓ Preguntas frecuentes

- **¿Tupla o struct?** Tupla para pocos valores anónimos; struct/clase si quieren nombres y significado.
- **¿Java tiene multi-retorno?** No nativo: se devuelve un objeto (record) con los campos.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 076](../../parte-5-funciones-y-modularidad/076-parametros-variadicos/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 078 ⏭️](../../parte-5-funciones-y-modularidad/078-genericos-y-polimorfismo-parametrico/README.md)
