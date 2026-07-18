# Comparación — Seguridad: entradas, memoria y dependencias

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | isalnum/regex en cada lenguaje. |
| Semántica | Se valida contra una lista blanca (más seguro que una negra). |
| Paradigmática | SQL usa consultas parametrizadas para evitar inyección. |

## El concepto en la familia

Toda plataforma web valida entradas; las consultas parametrizadas evitan la inyección SQL.
