# Clase 164 — Elegir el lenguaje correcto para cada componente

> Parte **10 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Cerrar la parte con la decisión clave del enfoque políglota: **elegir el lenguaje correcto para cada componente**. Según la naturaleza del componente (sistemas, web, datos), un lenguaje encaja mejor que otro.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Asociar un tipo de componente con un lenguaje.
2. Justificar la elección por la tarea.
3. Aplicar el criterio a un sistema real.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Elegir por componente | El mejor lenguaje para cada parte |
| 2 | Fortalezas | Qué destaca cada lenguaje |
| 3 | Sistema políglota | Varias elecciones coherentes |

## 📖 Definiciones y características

- **Idoneidad** — cuánto encaja un lenguaje con una tarea. Clave: rendimiento, ecosistema, plataforma.
- **Componente de sistemas** — cercano al hardware o de alto rendimiento. Clave: Rust/C encajan.
- **Componente web/datos** — interfaz interactiva o consulta de datos. Clave: TypeScript/SQL encajan.

## 🧩 Situación

Para un núcleo de rendimiento eliges Rust; para el frontend, TypeScript; para las consultas, SQL. Elegir por componente es lo que hace de un sistema políglota una decisión de ingeniería, no un capricho.

## 🧮 Modelo

- **Entrada** (stdin): una palabra: `sistemas`, `web` o `datos`
- **Salida** (stdout): `lenguaje=<Rust|TypeScript|SQL>`
- **Regla:** sistemas→Rust, web→TypeScript, datos→SQL

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `sistemas` | `lenguaje=Rust` |
| `web` | `lenguaje=TypeScript` |
| `datos` | `lenguaje=SQL` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER tipo ; SEGUN tipo: recomendar lenguaje
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
| Sintáctica | switch/match/lookup en cada lenguaje. |
| Semántica | La recomendación se basa en las fortalezas de cada lenguaje. |
| Paradigmática | SQL usa CASE. |

## 🧬 El concepto en la familia

La elección por componente es la esencia del programa: cada lenguaje del núcleo brilla en su terreno.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 164
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Elegir por moda** → causa: usar la herramienta equivocada → solución: elegir por la tarea y el contexto
- **Un solo lenguaje para todo** → causa: forzar la uniformidad → solución: aceptar que lo políglota suele ser mejor

## ❓ Preguntas frecuentes

- **¿Y si el equipo solo sabe un lenguaje?** El talento disponible es un criterio legítimo y a menudo decisivo.
- **¿No es más simple un solo lenguaje?** A veces; pero elegir por componente aprovecha lo mejor de cada uno.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 163](../../parte-10-interoperabilidad-y-fronteras-entre-lenguajes/163-incrustar-un-lenguaje-en-otro-lua-python-embebido/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 165 ⏭️](../../parte-11-proyecto-integrador-poliglota/165-el-proyecto-un-sistema-con-componentes-en-varios-lenguajes/README.md)
