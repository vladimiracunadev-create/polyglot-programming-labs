# Concepto — Depuradores: gdb, lldb, pdb y los de IDE

Conocimiento independiente del lenguaje.

Usar la idea de un **depurador**: avanzar paso a paso viendo cómo evoluciona el estado. La traza de sumas acumuladas (1, 3, 6, …) muestra el valor del acumulador en cada paso, como haría un depurador.

## Definiciones

- **Depurador** — herramienta para pausar y avanzar viendo el estado (gdb, pdb). Clave: diagnóstico.
- **Traza** — secuencia de estados por los que pasa el programa. Clave: revela dónde se desvía.
- **Paso a paso (step)** — avanzar una instrucción a la vez. Clave: inspeccionar cada cambio.

## Forma neutral

```text
acc <- 0 ; PARA i de 1 a n: acc <- acc+i ; emitir acc
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
