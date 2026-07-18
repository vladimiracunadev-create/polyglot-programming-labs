# Concepto — Arreglos de tamaño fijo

Conocimiento independiente del lenguaje.

Usar un **arreglo de tamaño fijo**: una secuencia contigua con un número de elementos conocido. Es la estructura más básica y la más cercana a la memoria.

## Definiciones

- **Arreglo** — colección de elementos contiguos indexados. Clave: acceso O(1) por índice.
- **Tamaño fijo** — número de elementos definido al crear. Clave: no crece.
- **Índice** — posición de un elemento, empezando en 0. Clave: `arr[0]` es el primero.

## Forma neutral

```text
LEER arr[3]
suma <- Σ arr ; max <- MAX(arr)
ESCRIBIR suma, max
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
