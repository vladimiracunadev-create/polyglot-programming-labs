# Clase 172 — Persistencia y almacenamiento

> Parte **11 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Construir la **persistencia y el almacenamiento**: guardar datos para recuperarlos después. Aquí se almacena un par clave/valor y se confirma lo guardado, como haría un almacén clave-valor.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Guardar un par clave/valor.
2. Confirmar el almacenamiento.
3. Reconocer tipos de almacenamiento.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Persistencia | Sobrevivir al reinicio |
| 2 | Clave/valor | Almacén simple |
| 3 | Almacenamiento | Dónde viven los datos |

## 📖 Definiciones y características

- **Persistencia** — guardar datos de forma duradera (disco, base de datos). Clave: sobreviven al reinicio.
- **Almacén clave-valor** — guarda valores indexados por una clave (Redis, mapas persistentes). Clave: acceso rápido por clave.
- **Durabilidad** — garantía de que lo guardado no se pierde. Clave: propiedad clave del almacenamiento.

## 🧩 Situación

El sistema guarda la configuración y el estado: un almacén clave-valor mapea `usuario → sesión`. Persistir bien es lo que permite apagar y volver a encender sin perder datos.

## 🧮 Modelo

- **Entrada** (stdin): una línea `clave valor`
- **Salida** (stdout): `guardado=<clave>=<valor>`
- **Regla:** almacenar el par y confirmar

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `x 5` | `guardado=x=5` |
| `nombre ada` | `guardado=nombre=ada` |
| `n 100` | `guardado=n=100` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER clave, valor ; guardar ; confirmar clave=valor
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
| Sintáctica | Un mapa/diccionario en cada lenguaje; una tabla en SQL. |
| Semántica | La persistencia hace duraderos los datos. |
| Paradigmática | SQL persiste en tablas con INSERT. |

## 🧬 El concepto en la familia

Redis (clave-valor), PostgreSQL (relacional), sistemas de archivos: opciones de persistencia según el caso.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 172
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Guardar sin durabilidad garantizada** → causa: pérdida ante caídas → solución: usar almacenamiento que confirme la escritura
- **Claves sin convención** → causa: colisiones y confusión → solución: definir un esquema de claves claro

## ❓ Preguntas frecuentes

- **¿Clave-valor o relacional?** Clave-valor para acceso simple y rápido; relacional para datos estructurados y consultas.
- **¿Persistir en disco o memoria?** Memoria para caché rápida; disco para durabilidad.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 171](../../parte-11-proyecto-integrador-poliglota/171-componente-de-automatizacion-scripting/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 173 ⏭️](../../parte-11-proyecto-integrador-poliglota/173-pruebas-end-to-end-del-sistema-completo/README.md)
