# Clase 080 — Paso por referencia

> Parte **5 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Comprender el **paso por referencia**: la función recibe un enlace a la variable original, así que modificar el parámetro **sí** cambia la variable de quien llama. C usa punteros, Go `*`, Rust `&mut`, C# `ref`.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Modificar una variable del llamador desde una función.
2. Distinguir referencia de copia.
3. Reconocer cómo cada lenguaje pasa referencias.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Paso por referencia | Se pasa un enlace, no una copia |
| 2 | Punteros/referencias | &, *, ref, &mut |
| 3 | Efecto en el llamador | El original cambia |
| 4 | Riesgo | Modificaciones a distancia |

## 📖 Definiciones y características

- **Paso por referencia** — la función accede a la variable original. Clave: puede modificarla.
- **Puntero** — valor que guarda la dirección de otra variable (C). Clave: permite modificarla.
- **Referencia mutable** — enlace que permite cambiar el valor (`&mut` en Rust, `ref` en C#). Clave: modificación explícita.
- **Efecto secundario** — cambiar algo fuera de la función. Clave: potente pero peligroso.

## 🧩 Situación

Una función `doblar(&n)` cambia `n` para siempre. Es útil (evita copiar datos grandes) pero peligroso: modificaciones 'a distancia' que sorprenden si no se esperan.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n`
- **Salida** (stdout): `antes=<n> despues=<2n>`
- **Regla:** la función duplica la variable original vía referencia

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `5` | `antes=5 despues=10` |
| `3` | `antes=3 despues=6` |
| `7` | `antes=7 despues=14` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER n ; antes <- n
doblar(referencia a n)   // modifica el original
ESCRIBIR "antes=" antes " despues=" n
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
| Sintáctica | `*p` (C/Go), `&mut` (Rust), `ref` (C#), objeto/lista (Java/JS/Python). |
| Semántica | Referencia mutable cambia el original; los primitivos por valor no. |
| Paradigmática | SQL no modifica variables: usa UPDATE sobre datos. |

## 🧬 El concepto en la familia

En Ruby los objetos se pasan por referencia (de valor); los enteros no se mutan. En C++ hay referencias `&` explícitas.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 080
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Modificar sin querer el original** → causa: efecto secundario inesperado → solución: pasar por valor si no debes cambiar el original
- **Confundir puntero con valor** → causa: modificar la copia del puntero → solución: desreferenciar (`*p`) para tocar el valor apuntado

## ❓ Preguntas frecuentes

- **¿Referencia o valor?** Referencia para modificar o evitar copiar datos grandes; valor para aislar.
- **¿Java pasa por referencia?** Pasa la referencia por valor: puedes mutar el objeto, no reasignar la variable del llamador.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 079](../../parte-5-funciones-y-modularidad/079-paso-por-valor/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 081 ⏭️](../../parte-5-funciones-y-modularidad/081-semantica-de-movimiento-y-prestamo-rust/README.md)
