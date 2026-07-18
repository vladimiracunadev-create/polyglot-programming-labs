# Clase 073 — Firma, parámetros, argumentos y retorno

> Parte **5 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Entender la anatomía de una función: **firma** (nombre + parámetros + tipo de retorno), **argumentos** (los valores que se pasan) y **retorno** (el valor que devuelve). Es la unidad de reutilización de todo programa.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Definir una función con parámetros y retorno.
2. Distinguir parámetro de argumento.
3. Invocar la función y usar su valor.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Firma | Nombre, parámetros y tipo de retorno |
| 2 | Parámetro vs. argumento | El hueco vs. el valor real |
| 3 | Retorno | El valor que produce |
| 4 | Reutilización | Llamar en vez de repetir |

## 📖 Definiciones y características

- **Función** — bloque con nombre que recibe parámetros y devuelve un valor. Clave: la unidad de reutilización.
- **Firma** — nombre + parámetros + tipo de retorno. Clave: define cómo se usa.
- **Parámetro** — variable del hueco en la definición. Clave: recibe el argumento.
- **Argumento** — valor concreto que se pasa al llamar. Clave: llena el parámetro.

## 🧩 Situación

En vez de repetir `a + b` por todas partes, se define `suma(a, b)` una vez y se llama. La firma es el contrato: qué recibe y qué devuelve.

## 🧮 Modelo

- **Entrada** (stdin): una línea `a b` (dos enteros)
- **Salida** (stdout): `suma=<a+b>`
- **Regla:** suma(a, b) = a + b

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `3 4` | `suma=7` |
| `10 20` | `suma=30` |
| `-5 5` | `suma=0` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
FUNCION suma(a, b): DEVOLVER a+b
LEER a, b ; ESCRIBIR "suma=" suma(a,b)
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
| Sintáctica | `def` (Python), `func` (Go), `fn` (Rust), tipo de retorno explícito (Java/C). |
| Semántica | Estáticos declaran los tipos de parámetros y retorno; dinámicos no. |
| Paradigmática | SQL define la operación en la propia consulta. |

## 🧬 El concepto en la familia

En Ruby `def suma(a, b)`. En Haskell `suma a b = a + b`, con la firma inferida.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 073
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Confundir parámetro con argumento** → causa: usar mal los términos y el orden → solución: recordar: parámetro en la definición, argumento en la llamada
- **Olvidar el return** → causa: la función no devuelve nada → solución: asegurar que la función retorna el valor

## ❓ Preguntas frecuentes

- **¿Función o procedimiento?** Una función devuelve valor; un procedimiento solo actúa. Aquí devolvemos.
- **¿Por qué reutilizar?** Menos repetición, menos errores, un solo lugar que cambiar.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 072](../../parte-4-control-del-programa/072-manejo-de-errores-ii-resultados-y-valores-result-either-error-de-go/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 074 ⏭️](../../parte-5-funciones-y-modularidad/074-parametros-por-defecto-y-opcionales/README.md)
