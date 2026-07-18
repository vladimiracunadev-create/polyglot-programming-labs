# Concepto — Diseño: responsabilidades y contratos entre componentes

Conocimiento independiente del lenguaje.

Diseñar el sistema definiendo **responsabilidades y contratos entre componentes**. Dos componentes encajan si respetan el mismo contrato en su frontera; aquí se comprueba comparando sus valores.

## Definiciones

- **Contrato de frontera** — acuerdo de datos y formato entre dos componentes. Clave: permite evolucionar por separado.
- **Compatibilidad** — que emisor y receptor esperan lo mismo. Clave: sin ella, la integración falla.
- **Responsabilidad** — la tarea única de un componente. Clave: define qué expone en el contrato.

## Forma neutral

```text
LEER a, b ; compatible <- (a == b)
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
