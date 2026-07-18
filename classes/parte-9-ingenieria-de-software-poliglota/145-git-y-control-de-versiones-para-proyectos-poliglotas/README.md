# Clase 145 — Git y control de versiones para proyectos políglotas

> Parte **9 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Introducir **Git y el control de versiones**: el historial es una secuencia de commits (instantáneas con mensaje). Contar los commits es la operación básica sobre ese historial.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Contar los commits de un historial.
2. Explicar qué es un commit.
3. Reconocer el valor del versionado.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Commit | Instantánea con mensaje |
| 2 | Historial | Secuencia de commits |
| 3 | Ramas | Líneas de desarrollo |

## 📖 Definiciones y características

- **Git** — sistema de control de versiones distribuido. Clave: historial completo en cada copia.
- **Commit** — instantánea del proyecto con un mensaje. Clave: unidad del historial.
- **Rama** — línea de desarrollo paralela. Clave: trabajar sin pisar la principal.

## 🧩 Situación

Cada cambio importante se registra como un commit con su mensaje. El historial permite volver atrás, ver quién cambió qué y colaborar sin sobrescribir el trabajo ajeno.

## 🧮 Modelo

- **Entrada** (stdin): una línea con mensajes de commit (palabras separadas por espacio)
- **Salida** (stdout): `commits=<cantidad>`
- **Regla:** contar los mensajes

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `fix add refactor` | `commits=3` |
| `init` | `commits=1` |
| `a b c d` | `commits=4` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER mensajes ; ESCRIBIR cantidad
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
| Sintáctica | Contar palabras en cada lenguaje. |
| Semántica | Cada commit es una instantánea inmutable. |
| Paradigmática | SQL cuenta filas. |

## 🧬 El concepto en la familia

Git es el estándar; Mercurial y otros comparten el modelo de instantáneas versionadas.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 145
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Commits enormes y sin mensaje claro** → causa: historial ilegible → solución: commits pequeños con mensajes descriptivos
- **Commitear archivos generados** → causa: ruido en el repo → solución: usar .gitignore

## ❓ Preguntas frecuentes

- **¿Cada cuánto commitear?** Cuando tienes un cambio coherente y funcional.
- **¿Git es solo para código?** No: sirve para cualquier texto versionable (docs, configuración).

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 144](../../parte-9-ingenieria-de-software-poliglota/144-compilacion-reproducible-y-empaquetado/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 146 ⏭️](../../parte-9-ingenieria-de-software-poliglota/146-revision-de-codigo-y-estandares/README.md)
