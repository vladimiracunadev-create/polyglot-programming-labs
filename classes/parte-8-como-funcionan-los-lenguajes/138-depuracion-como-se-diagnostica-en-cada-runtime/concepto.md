# Concepto — Depuración: cómo se diagnostica en cada runtime

Conocimiento independiente del lenguaje.

Cerrar la parte con la **depuración**: cómo se diagnostica un programa. Inspeccionar el valor de las variables (aquí, el número y sus potencias) es lo que hace un depurador al pausar la ejecución.

## Definiciones

- **Depurador** — herramienta para pausar, inspeccionar y avanzar un programa (gdb, lldb, pdb). Clave: ver el estado real.
- **Punto de ruptura** — lugar donde el depurador pausa la ejecución. Clave: para inspeccionar ahí.
- **Inspección** — examinar el valor de las variables en un momento. Clave: la base del diagnóstico.

## Forma neutral

```text
LEER n ; ESCRIBIR n, n*n, n*n*n
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
