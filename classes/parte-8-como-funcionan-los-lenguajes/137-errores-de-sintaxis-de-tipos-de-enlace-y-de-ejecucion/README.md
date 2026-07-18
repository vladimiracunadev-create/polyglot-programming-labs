# Clase 137 — Errores: de sintaxis, de tipos, de enlace y de ejecución

> Parte **8 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Clasificar los **tipos de error** por el momento en que aparecen: de sintaxis (al parsear), de tipos (al comprobar tipos), de enlace (al unir con librerías) y de ejecución (al correr). Saber cuándo ocurre cada uno acelera el diagnóstico.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Nombrar las cuatro clases de error.
2. Asociar cada error a su fase.
3. Diagnosticar según cuándo aparece.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Error de sintaxis | El código no se puede parsear |
| 2 | Error de tipos | Operación inválida para los tipos |
| 3 | Error de enlace y de ejecución | Al unir librerías o al correr |

## 📖 Definiciones y características

- **Error de sintaxis** — el código viola las reglas gramaticales. Clave: se detecta al parsear.
- **Error de tipos** — operación no válida para los tipos implicados. Clave: en compilación (estáticos) o ejecución (dinámicos).
- **Error de enlace** — no se encuentra una función/símbolo al unir con librerías. Clave: entre compilar y ejecutar.
- **Error de ejecución** — ocurre al correr (división por cero, índice fuera de rango). Clave: en tiempo de ejecución.

## 🧩 Situación

Un `;` olvidado es de sintaxis; sumar texto y número, de tipos; una librería ausente, de enlace; dividir por cero, de ejecución. Saber la fase reduce el tiempo de búsqueda del fallo.

## 🧮 Modelo

- **Entrada** (stdin): un entero `codigo` (1 a 4)
- **Salida** (stdout): `error=<sintaxis|tipos|enlace|ejecucion>`
- **Regla:** 1→sintaxis, 2→tipos, 3→enlace, 4→ejecucion

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `1` | `error=sintaxis` |
| `3` | `error=enlace` |
| `4` | `error=ejecucion` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER codigo ; SEGUN codigo: 1..4 -> nombre del error
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
| Sintáctica | switch/match sobre el código en cada lenguaje. |
| Semántica | En estáticos, los de tipos salen al compilar; en dinámicos, al ejecutar. |
| Paradigmática | SQL usa CASE. |

## 🧬 El concepto en la familia

Los compilados detectan sintaxis, tipos y enlace antes de ejecutar; los interpretados, muchos al correr.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 137
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Confundir error de tipos con de ejecución** → causa: buscar en la fase equivocada → solución: recordar cuándo comprueba tipos tu lenguaje
- **Ignorar el error de enlace** → causa: 'símbolo no encontrado' → solución: verificar librerías y su enlazado

## ❓ Preguntas frecuentes

- **¿Cuándo salen los errores de tipos?** En compilación (estáticos) o en ejecución (dinámicos).
- **¿Qué es un error de enlace?** Cuando el enlazador no encuentra una función/símbolo referenciado.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 136](../../parte-8-como-funcionan-los-lenguajes/136-el-modelo-de-memoria-y-las-condiciones-de-carrera/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 138 ⏭️](../../parte-8-como-funcionan-los-lenguajes/138-depuracion-como-se-diagnostica-en-cada-runtime/README.md)
