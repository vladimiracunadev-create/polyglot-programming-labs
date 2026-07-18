# Comparación — Registro (logging) y observabilidad

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | logging (Python), console/log4j (JS/Java), slog (Go). |
| Semántica | El nivel permite filtrar; el formato estructurado facilita el análisis. |
| Paradigmática | SQL registra con tablas de auditoría. |

## El concepto en la familia

log4j/SLF4J (Java), logging (Python), Serilog (.NET), zap/slog (Go): mismo concepto de niveles.
