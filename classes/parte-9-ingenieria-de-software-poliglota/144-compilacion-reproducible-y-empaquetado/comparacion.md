# Comparación — Compilación reproducible y empaquetado

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | Suma en cada lenguaje (un checksum real usaría un hash). |
| Semántica | La misma entrada da el mismo checksum: reproducibilidad. |
| Paradigmática | SQL suma con SUM. |

## El concepto en la familia

Los gestores de paquetes verifican con SHA-256; aquí una suma simple ilustra el concepto.
