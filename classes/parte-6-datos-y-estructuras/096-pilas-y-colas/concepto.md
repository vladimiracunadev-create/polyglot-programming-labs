# Concepto — Pilas y colas

Conocimiento independiente del lenguaje.

Distinguir **pila (LIFO)** de **cola (FIFO)**: dos formas de ordenar la salida. La pila devuelve el último que entró; la cola, el primero.

## Definiciones

- **Pila** — estructura LIFO: se saca el último añadido. Clave: deshacer, llamadas.
- **Cola** — estructura FIFO: se saca el primero añadido. Clave: turnos, tareas.
- **LIFO/FIFO** — orden de salida. Clave: define la estructura.

## Forma neutral

```text
LEER lista ; pila <- sacar en LIFO ; cola <- sacar en FIFO
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
