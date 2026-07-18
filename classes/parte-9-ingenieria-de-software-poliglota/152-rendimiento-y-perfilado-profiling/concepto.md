# Concepto — Rendimiento y perfilado (profiling)

Conocimiento independiente del lenguaje.

Introducir el **rendimiento y el perfilado (profiling)**: medir dónde se gasta el tiempo o cuántas operaciones se hacen para optimizar con datos, no por intuición. Contar las operaciones de una suma es un perfilado en miniatura.

## Definiciones

- **Perfilado** — medir el uso de tiempo/recursos de un programa. Clave: optimizar con evidencia.
- **Operación** — unidad de trabajo (una suma, una comparación). Clave: contarlas estima el coste.
- **Cuello de botella** — la parte que domina el coste. Clave: optimizar ahí primero.

## Forma neutral

```text
ops <- 0 ; suma <- 0 ; PARA i de 1 a n: suma+=i ; ops++
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
