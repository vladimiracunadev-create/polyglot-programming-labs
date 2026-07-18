# Concepto — Entrega y despliegue

Conocimiento independiente del lenguaje.

Introducir la **entrega y el despliegue**: llevar el artefacto probado a producción. Etiquetar la versión (p. ej. `v1.2.3`) es parte de una entrega ordenada y trazable.

## Definiciones

- **Entrega continua** — mantener el software siempre listo para desplegar. Clave: releases frecuentes y seguras.
- **Despliegue** — poner una versión en producción. Clave: puede ser manual o automático (CD).
- **Etiqueta (tag)** — marca de una versión en el historial (v1.2.3). Clave: trazabilidad.

## Forma neutral

```text
LEER version ; ESCRIBIR 'desplegado=v' + version
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
