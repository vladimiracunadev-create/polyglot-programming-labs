# Clase 175 — Documentación y defensa de las decisiones de lenguaje

> Parte **11 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Realizar la **documentación y la defensa de las decisiones de lenguaje**: explicar por qué cada componente usa su lenguaje y cómo encajan. Aquí se mide la documentación por su número de secciones.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Medir la cobertura de la documentación.
2. Explicar por qué documentar las decisiones.
3. Reconocer qué documentar.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Documentación | Explicar el porqué |
| 2 | Defensa de decisiones | Justificar cada lenguaje |
| 3 | Secciones | Cobertura del documento |

## 📖 Definiciones y características

- **Documentación** — explicación escrita del sistema y sus decisiones. Clave: el porqué, no solo el qué.
- **Defensa de decisiones** — justificar por qué cada componente usa su lenguaje. Clave: hace revisables las elecciones.
- **Cobertura** — cuánto del sistema está documentado. Clave: una métrica de calidad.

## 🧩 Situación

Al cerrar el proyecto, se documenta: por qué Rust en el núcleo, TypeScript en el frontend, SQL en los datos, y cómo se comunican. Esa defensa razonada es lo que distingue una decisión de ingeniería de un capricho.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n` (número de secciones documentadas)
- **Salida** (stdout): `documentado=<n> secciones`
- **Regla:** informar el número de secciones

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `5` | `documentado=5 secciones` |
| `1` | `documentado=1 secciones` |
| `8` | `documentado=8 secciones` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER n ; ESCRIBIR documentado=n secciones
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
| Sintáctica | Formatear la salida en cada lenguaje. |
| Semántica | La documentación explica el porqué de las decisiones. |
| Paradigmática | SQL se documenta con comentarios y vistas. |

## 🧬 El concepto en la familia

Markdown, docstrings, ADR (Architecture Decision Records) documentan sistemas y decisiones.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 175
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Documentar el qué en vez del porqué** → causa: comentarios redundantes → solución: explicar las decisiones y sus razones
- **Documentación desactualizada** → causa: engaña más que ayuda → solución: mantenerla junto al código

## ❓ Preguntas frecuentes

- **¿Qué documentar?** Las decisiones y el porqué; el qué suele leerse en el código.
- **¿Qué es un ADR?** Un registro breve de una decisión de arquitectura y su justificación.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 174](../../parte-11-proyecto-integrador-poliglota/174-empaquetado-contenedores-y-despliegue/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 176 ⏭️](../../parte-11-proyecto-integrador-poliglota/176-cierre-retrospectiva-y-transferencia-a-nuevos-lenguajes/README.md)
