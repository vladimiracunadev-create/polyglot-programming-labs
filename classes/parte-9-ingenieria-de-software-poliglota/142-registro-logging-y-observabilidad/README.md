# Clase 142 — Registro (logging) y observabilidad

> Parte **9 — Valores, tipos y variables** · ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**
> ✅ **Clase construida** — 10 implementaciones del núcleo verificadas contra `casos.json`.

---

## 🎯 Objetivo

Practicar el **registro (logging) y la observabilidad**: dejar rastros de lo que hace el programa para poder diagnosticarlo en producción, donde no hay depurador. Un log con nivel y datos es la unidad básica.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Emitir un registro con nivel.
2. Explicar la observabilidad.
3. Distinguir niveles de log.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Logging | Dejar rastros de la ejecución |
| 2 | Nivel | INFO, WARN, ERROR |
| 3 | Observabilidad | Entender el sistema desde fuera |

## 📖 Definiciones y características

- **Log** — mensaje que registra un evento del programa. Clave: diagnóstico en producción.
- **Nivel de log** — gravedad del mensaje (DEBUG, INFO, WARN, ERROR). Clave: filtrar el ruido.
- **Observabilidad** — capacidad de entender el estado interno desde las salidas (logs, métricas, trazas). Clave: operar en producción.

## 🧩 Situación

En producción no puedes pausar el programa; te guías por los logs. Un registro estructurado ('[INFO] procesados=5') permite saber qué pasó sin estar delante.

## 🧮 Modelo

- **Entrada** (stdin): un entero `n` (elementos procesados)
- **Salida** (stdout): `log=[INFO] procesados=<n>`
- **Regla:** emitir un registro de nivel INFO con el conteo

Especificación y verificación en [`casos.json`](casos.json):

| stdin | esperado |
|---|---|
| `5` | `log=[INFO] procesados=5` |
| `0` | `log=[INFO] procesados=0` |
| `3` | `log=[INFO] procesados=3` |

## 📐 Algoritmo (pseudocódigo neutral)

```text
LEER n ; ESCRIBIR log de nivel INFO con procesados=n
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
| Sintáctica | logging (Python), console/log4j (JS/Java), slog (Go). |
| Semántica | El nivel permite filtrar; el formato estructurado facilita el análisis. |
| Paradigmática | SQL registra con tablas de auditoría. |

## 🧬 El concepto en la familia

log4j/SLF4J (Java), logging (Python), Serilog (.NET), zap/slog (Go): mismo concepto de niveles.

## ✅ Prueba común

Los mismos casos para todas las implementaciones: [`casos.json`](casos.json). Verifica la equivalencia:

```bash
python scripts/verificar_equivalencia.py 142
```

## 🧪 Reto de transferencia

Detalle en [`reto.md`](reto.md).

## ⚠️ Errores comunes

- **Loggear demasiado** → causa: ruido que oculta lo importante → solución: usar niveles y registrar lo relevante
- **Loggear datos sensibles** → causa: fuga de información → solución: no registrar contraseñas ni datos personales

## ❓ Preguntas frecuentes

- **¿Log o depurador?** El depurador para desarrollo; el log para producción.
- **¿Qué es observabilidad?** Logs, métricas y trazas que permiten entender el sistema en marcha.

## 🔗 Referencias

- Documentación oficial de cada lenguaje del núcleo.

---

> [⏮️ Clase 141](../../parte-9-ingenieria-de-software-poliglota/141-depuradores-gdb-lldb-pdb-y-los-de-ide/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 143 ⏭️](../../parte-9-ingenieria-de-software-poliglota/143-dependencias-versiones-y-lockfiles/README.md)
