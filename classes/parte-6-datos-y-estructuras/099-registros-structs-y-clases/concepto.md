# Concepto — Registros, structs y clases

Conocimiento independiente del lenguaje.

Agrupar datos relacionados en un **registro/struct/clase** con campos nombrados. En vez de variables sueltas, un tipo compuesto con significado.

## Definiciones

- **Registro/struct** — tipo con campos nombrados. Clave: agrupa datos relacionados.
- **Campo** — cada dato con nombre dentro del registro. Clave: `persona.edad`.
- **Instancia** — un valor concreto del tipo. Clave: `Persona("Ada", 36)`.

## Forma neutral

```text
LEER nombre, edad ; crear Persona ; ESCRIBIR formateado
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
