# Concepto — Conjuntos (sets) y unicidad

Conocimiento independiente del lenguaje.

Usar un **conjunto (set)**: una colección sin duplicados. Contar los valores únicos es la operación natural del conjunto.

## Definiciones

- **Conjunto** — colección de elementos únicos (set, HashSet). Clave: sin duplicados.
- **Unicidad** — propiedad de no repetir. Clave: añadir un existente no hace nada.
- **Pertenencia** — comprobar si un elemento está, en O(1) típico. Clave: uso habitual del set.

## Forma neutral

```text
LEER lista ; conjunto <- SET(lista) ; ESCRIBIR |conjunto|
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
