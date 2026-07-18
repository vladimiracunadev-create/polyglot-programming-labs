# Concepto — Diseño y arquitectura comparada

Conocimiento independiente del lenguaje.

Introducir el **diseño y la arquitectura**: un sistema se organiza en capas o componentes con responsabilidades claras. Contar las capas es la medida más básica de su estructura.

## Definiciones

- **Arquitectura** — estructura de alto nivel de un sistema y sus componentes. Clave: guía las decisiones grandes.
- **Capa** — grupo de componentes con una responsabilidad (presentación, lógica, datos). Clave: separa preocupaciones.
- **Acoplamiento** — grado de dependencia entre componentes. Clave: bajo acoplamiento facilita el cambio.

## Forma neutral

```text
LEER capas ; ESCRIBIR cantidad
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
