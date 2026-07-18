# Concepto — El heap y la asignación dinámica

Conocimiento independiente del lenguaje.

Entender el **heap y la asignación dinámica**: cuando el tamaño de los datos no se conoce en compilación, se reservan en el heap. Una lista dinámica que crece con n vive en el heap.

## Definiciones

- **Heap** — región de memoria para datos de tamaño/vida no conocidos en compilación. Clave: más flexible que la pila.
- **Asignación dinámica** — reservar memoria en ejecución (una lista que crece). Clave: heap.
- **Stack vs. heap** — la pila es automática y rápida; el heap es flexible pero requiere gestión. Clave: distinto uso.

## Forma neutral

```text
reservar lista ; añadir n, n-1, ..., 1 ; unir por -
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
