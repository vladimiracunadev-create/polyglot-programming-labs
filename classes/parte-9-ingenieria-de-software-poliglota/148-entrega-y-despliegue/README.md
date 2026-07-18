# Clase 148 — Entrega y despliegue

> Parte **9 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Introducir la **entrega y el despliegue**: llevar el artefacto probado a producción. Etiquetar la versión (p. ej. `v1.2.3`) es parte de una entrega ordenada y trazable.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Etiquetar una versión para desplegar.
2. Explicar entrega vs. despliegue.
3. Reconocer el valor de la trazabilidad.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Entrega | Preparar para publicar |
| 2 | Despliegue | Poner en producción |
| 3 | Etiqueta de versión | Trazabilidad |

## 📖 Definiciones y características

- **Entrega continua** — mantener el software siempre listo para desplegar. Clave: releases frecuentes y seguras.
- **Despliegue** — poner una versión en producción. Clave: puede ser manual o automático (CD).
- **Etiqueta (tag)** — marca de una versión en el historial (v1.2.3). Clave: trazabilidad.

## 🧩 Situación

Tras pasar el CI, se etiqueta la versión (`v1.2.3`) y se despliega. La etiqueta permite saber exactamente qué código está en producción y volver atrás si hace falta.

## 🧮 Modelo

- **Entrada** (stdin): una línea con una versión `mayor.menor.parche`
- **Salida** (stdout): `desplegado=v<versión>`
- **Regla:** prefijar la versión con 'v'

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `1.2.3` | `desplegado=v1.2.3` |
| `0.9.0` | `desplegado=v0.9.0` |
| `2.1.5` | `desplegado=v2.1.5` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER version ; ESCRIBIR 'desplegado=v' + version
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
| Sintáctica | Concatenación en cada lenguaje. |
| Semántica | La etiqueta identifica la versión desplegada. |
| Paradigmática | SQL concatena con \|\|. |

## 🧬 El concepto en la familia

Git tags, releases de GitHub, y las herramientas de CD (Argo, Spinnaker) gestionan despliegues versionados.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 148
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Desplegar sin etiquetar** → causa: no saber qué hay en producción → solución: etiquetar cada release
- **Desplegar sin pasar el CI** → causa: romper producción → solución: desplegar solo lo que está verde

## ❓ Preguntas frecuentes

- **¿Entrega o despliegue continuo?** Entrega deja el software listo; despliegue continuo lo publica automáticamente.
- **¿Por qué el prefijo 'v'?** Convención común para distinguir etiquetas de versión.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 147](../../parte-9-ingenieria-de-software-poliglota/147-integracion-continua-ci-multi-lenguaje/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 149 ⏭️](../../parte-9-ingenieria-de-software-poliglota/149-diseno-y-arquitectura-comparada/README.md)
