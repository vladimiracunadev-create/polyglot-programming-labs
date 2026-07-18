# Clase 140 — Pruebas de integración y el verificador de equivalencia

> Parte **9 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Entender las **pruebas de integración** y el **verificador de equivalencia**: en vez de una unidad aislada, se comprueba que dos partes (o dos implementaciones) producen el mismo resultado. Es exactamente lo que hace el CI de este curso.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Comparar dos salidas.
2. Explicar prueba de integración vs. unitaria.
3. Relacionarlo con el verificador del curso.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Integración | Varias partes juntas |
| 2 | Equivalencia | Mismos resultados |
| 3 | Verificador | Compara implementaciones |

## 📖 Definiciones y características

- **Prueba de integración** — verifica que varias partes funcionan juntas. Clave: más allá de la unidad.
- **Equivalencia** — dos implementaciones dan el mismo resultado. Clave: base del verificador.
- **Regresión** — un cambio rompe algo que funcionaba. Clave: las pruebas la detectan.

## 🧩 Situación

El verificador de este curso comprueba que las 10 implementaciones de una clase dan la misma salida. Aquí, en pequeño, se comparan dos resultados y se declara si son equivalentes.

## 🧮 Modelo

- **Entrada** (stdin): una línea `x y` (dos resultados a comparar)
- **Salida** (stdout): `equivalente=<true|false>`
- **Regla:** equivalente si x == y

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `6 6` | `equivalente=true` |
| `5 7` | `equivalente=false` |
| `0 0` | `equivalente=true` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER x, y ; ESCRIBIR equivalente=(x==y)
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
| Sintáctica | Comparación de igualdad en cada lenguaje. |
| Semántica | Se compara la salida observable, no la implementación. |
| Paradigmática | SQL compara con =. |

## 🧬 El concepto en la familia

El patrón 'mismas entradas → misma salida' es universal en pruebas de equivalencia.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 140
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Comparar implementaciones en vez de salidas** → causa: acoplamiento a detalles → solución: comparar el resultado observable
- **No fijar el formato** → causa: diferencias espurias → solución: normalizar la salida antes de comparar

## ❓ Preguntas frecuentes

- **¿Unitaria o integración?** Unitaria prueba una función; integración, varias juntas.
- **¿Qué garantiza el verificador?** Que las implementaciones son equivalentes, no que la prosa sea correcta.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 139](../../parte-9-ingenieria-de-software-poliglota/139-pruebas-unitarias-por-lenguaje/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 141 ⏭️](../../parte-9-ingenieria-de-software-poliglota/141-depuradores-gdb-lldb-pdb-y-los-de-ide/README.md)
