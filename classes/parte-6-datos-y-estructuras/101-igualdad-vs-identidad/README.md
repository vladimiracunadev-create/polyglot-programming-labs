# Clase 101 — Igualdad vs. identidad

> Parte **6 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Distinguir **igualdad** (mismo valor) de **identidad** (mismo objeto en memoria). Con valores primitivos coinciden; con objetos no siempre, y cada lenguaje ofrece operadores distintos (`==` vs. `is`/`===`).

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Comparar por valor.
2. Explicar la diferencia entre igualdad e identidad.
3. Reconocer los operadores de cada lenguaje.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Igualdad | Mismo valor |
| 2 | Identidad | Mismo objeto en memoria |
| 3 | Operadores | ==, is, ===, equals |

## 📖 Definiciones y características

- **Igualdad** — dos valores son iguales si representan lo mismo. Clave: `a == b`.
- **Identidad** — dos referencias apuntan al mismo objeto. Clave: `is` (Python), `===` no es exactamente eso en JS.
- **equals vs. ==** — en Java `==` compara referencias de objetos; `equals` compara valor. Clave: fuente de bugs.

## 🧩 Situación

En Java, dos cadenas con el mismo texto pueden ser `equals` pero no `==` (distintos objetos). Confundir igualdad con identidad es un error clásico.

## 🧮 Modelo

- **Entrada** (stdin): una línea `a b` (dos enteros)
- **Salida** (stdout): `iguales=<true|false>`
- **Regla:** iguales = (a == b)

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `5 5` | `iguales=true` |
| `3 7` | `iguales=false` |
| `0 0` | `iguales=true` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER a, b ; ESCRIBIR iguales=(a==b)
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
| Sintáctica | `==` en todos para valor; identidad con `is` (Python), `===` (JS), `equals`/`==` (Java). |
| Semántica | Con primitivos, igualdad e identidad coinciden; con objetos no. |
| Paradigmática | SQL compara valores con `=`; NULL requiere `IS`. |

## 🧬 El concepto en la familia

En Ruby `==` es valor y `equal?` es identidad. En C#, `==` puede sobrecargarse; `ReferenceEquals` da identidad.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 101
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Usar `==` para objetos en Java** → causa: compara referencias, no valor → solución: usar `equals` para comparar contenido
- **Comparar reales con `==`** → causa: imprecisión → solución: aquí son enteros; con reales usar tolerancia

## ❓ Preguntas frecuentes

- **¿`==` compara valor o referencia?** Depende del lenguaje y del tipo; con primitivos, valor.
- **¿Qué es `is` en Python?** Compara identidad (mismo objeto), no valor.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 100](../../parte-6-datos-y-estructuras/100-enumeraciones-y-tipos-algebraicos-adt-sum-types/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 102 ⏭️](../../parte-6-datos-y-estructuras/102-copia-superficial-vs-profunda-referencia-vs-valor/README.md)
