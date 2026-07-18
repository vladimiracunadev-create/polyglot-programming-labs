# Clase 049 — Conversión de tipos: casting explícito vs. coerción implícita

> Parte **3 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Distinguir **conversión explícita** (casting) de **coerción implícita**. Convertir un texto a real, y ese real a entero (truncando), muestra cómo cada lenguaje exige o realiza la conversión.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Convertir texto a número.
2. Convertir un real a entero por truncamiento.
3. Diferenciar casting explícito de coerción implícita.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | De texto a número | Parsear la entrada |
| 2 | Truncamiento | Quitar la parte decimal hacia cero |
| 3 | Casting explícito | El programador ordena la conversión |
| 4 | Coerción implícita | El lenguaje convierte solo |

## 📖 Definiciones y características

- **Conversión (casting)** — cambiar el tipo de un valor explícitamente. Clave: `int(x)`, `(long)f`.
- **Coerción** — conversión automática que hace el lenguaje. Clave: fuente de sorpresas en los débilmente tipados.
- **Truncamiento** — descartar la parte decimal hacia cero. Clave: distinto de redondear.
- **Parseo** — interpretar un texto como un número. Clave: primer paso de casi toda entrada.

## 🧩 Situación

Un formulario entrega '3.7' como texto. Para calcular hay que convertirlo a número, y quizá a entero. Cada lenguaje exige un grado distinto de explicitud, y truncar no es redondear.

## 🧮 Modelo

- **Entrada** (stdin): un número real como texto
- **Salida** (stdout): `entero=<parte entera truncada> real=<valor con 2 decimales>`
- **Regla:** entero = truncar(real) ; real formateado a 2 decimales

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `3.7` | `entero=3 real=3.70` |
| `5.0` | `entero=5 real=5.00` |
| `8.9` | `entero=8 real=8.90` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER texto
real <- A_REAL(texto)
entero <- TRUNCAR(real)
ESCRIBIR "entero=" entero " real=" FORMATEAR(real,2)
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
| Sintáctica | `int(f)` (Python), `Math.trunc` (JS), `(long)f` (Java/C/C#), `f as i64` (Rust). |
| Semántica | El truncamiento va hacia cero; no confundir con redondeo (`round`). |
| Paradigmática | SQL usa `CAST(x AS INTEGER)`. |

## 🧬 El concepto en la familia

En Ruby `f.to_i` trunca. En Haskell `truncate f`. En C++ `static_cast<long>(f)`. Todos truncan hacia cero (para positivos, igual que floor).

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 049
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Confundir truncar con redondear** → causa: esperar 4 de 3.7 → solución: usar la conversión a entero (trunca), no round
- **Sumar texto y número** → causa: olvidar convertir la entrada → solución: parsear siempre el texto antes de operar

## ❓ Preguntas frecuentes

- **¿Truncar y floor son lo mismo?** Para positivos sí; para negativos no (trunc va a cero, floor hacia abajo).
- **¿Qué es coerción implícita?** Que el lenguaje convierta sin pedirlo (p. ej. PHP suma '3'+4). Puede sorprender.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 048](../../parte-3-valores-tipos-y-variables/048-cadenas-representacion-inmutabilidad-e-interpolacion/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 050 ⏭️](../../parte-3-valores-tipos-y-variables/050-tipado-estatico-vs-dinamico/README.md)
