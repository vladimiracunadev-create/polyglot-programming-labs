# Concepto — Tuplas y registros posicionales

Conocimiento independiente del lenguaje.

Usar **tuplas**: agrupar un número fijo de valores, posiblemente de tipos distintos, sin definir una clase. Se accede por posición y se desestructuran fácilmente.

## Definiciones

- **Tupla** — grupo ordenado de valores de tamaño fijo. Clave: liviana, sin definir un tipo.
- **Componente** — cada elemento de la tupla, por posición. Clave: `.0`, `[0]`.
- **Registro posicional** — estructura cuyos campos se identifican por orden. Clave: la tupla lo es.

## Forma neutral

```text
LEER (a, b) ; intercambiar ; ESCRIBIR (b, a)
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
