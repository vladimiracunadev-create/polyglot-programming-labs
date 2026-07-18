# Clase 054 — Mutabilidad e inmutabilidad

> Parte **3 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Ver la diferencia entre construir un resultado **mutando** un acumulador (StringBuilder, lista que crece) y hacerlo de forma **inmutable**. Construir una secuencia numérica muestra el patrón acumulador en cada lenguaje.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Construir un resultado acumulando en un bucle.
2. Reconocer estructuras mutables (builder, lista).
3. Explicar el coste de concatenar cadenas inmutables.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Acumulador | Una variable que crece en cada vuelta |
| 2 | Mutable vs. inmutable | Modificar en sitio o crear nuevo |
| 3 | StringBuilder | Construir texto eficientemente |
| 4 | Coste de la inmutabilidad | Concatenar cadenas puede recrear todo |

## 📖 Definiciones y características

- **Mutabilidad** — capacidad de cambiar un valor in situ. Clave: eficiente para construir por partes.
- **Inmutabilidad** — el valor no cambia; toda 'modificación' crea uno nuevo. Clave: más seguro, a veces más caro.
- **Acumulador** — variable que reúne el resultado a lo largo de un bucle. Clave: patrón universal.
- **Builder** — estructura mutable para construir cadenas/colecciones (StringBuilder). Clave: evita recrear en cada paso.

## 🧩 Situación

Concatenar 10.000 cadenas con `+` en un bucle puede ser lentísimo si cada `+` recrea toda la cadena. Por eso existen los builders mutables. Construir '1-2-...-n' ilustra el patrón.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n` (n >= 1)
- **Salida** (stdout): `sec=1-2-...-n` (números de 1 a n separados por guiones)
- **Regla:** sec = unir([1..n], separador='-')

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `3` | `sec=1-2-3` |
| `1` | `sec=1` |
| `5` | `sec=1-2-3-4-5` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER n
acc <- vacío
PARA i de 1 a n: añadir i a acc
ESCRIBIR "sec=" UNIR(acc, "-")
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
| Sintáctica | `'-'.join(...)` (Python), `StringBuilder` (Java/C#), `strings.Builder` (Go). |
| Semántica | Java/C#/Go usan builders mutables; Python/Rust juntan una lista al final. |
| Paradigmática | SQL usa `group_concat` sobre filas generadas, no un bucle. |

## 🧬 El concepto en la familia

En Ruby `(1..n).to_a.join('-')`. En Haskell `intercalate "-" (map show [1..n])`, puramente inmutable. En C++ un `std::ostringstream`.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 054
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Concatenar con `+` en bucle grande** → causa: recrear la cadena cada vuelta (O(n²)) → solución: usar un builder mutable o juntar al final
- **Olvidar el caso n=1** → causa: poner un guion de más → solución: no añadir separador antes del primer elemento

## ❓ Preguntas frecuentes

- **¿Siempre es mejor mutar?** Para construir por partes, el builder es eficiente; para compartir datos, la inmutabilidad es más segura.
- **¿Por qué las cadenas suelen ser inmutables?** Seguridad y para poder compartirlas/hashearlas sin copiar.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 053](../../parte-3-valores-tipos-y-variables/053-nulabilidad-null-nil-none-option-y-valores-ausentes/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 055 ⏭️](../../parte-3-valores-tipos-y-variables/055-operadores-y-expresiones-aritmeticos-logicos-de-comparacion-y-bit-a-bit/README.md)
