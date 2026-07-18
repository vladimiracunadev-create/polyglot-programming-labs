# Concepto — Importar, exportar y organizar un proyecto

Conocimiento independiente del lenguaje.

Cerrar la parte usando la **biblioteca estándar**: importar y usar funciones ya provistas por el lenguaje (aquí, valor absoluto). Organizar un proyecto también es saber qué reutilizar en vez de reescribir.

## Definiciones

- **Biblioteca estándar** — conjunto de módulos incluidos con el lenguaje. Clave: funciones listas para usar.
- **Importar/incluir** — traer un módulo o cabecera (`import`, `#include`, `use`). Clave: acceder a sus funciones.
- **Valor absoluto** — distancia a cero, siempre no negativa. Clave: `abs(-5) = 5`.
- **Reutilización** — usar código existente en vez de reescribir. Clave: menos errores.

## Forma neutral

```text
IMPORTAR abs de la biblioteca
LEER n ; ESCRIBIR "abs=" abs(n)
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
