# Concepto — Comprensiones de listas y colecciones

Conocimiento independiente del lenguaje.

Filtrar una colección con una **comprensión** (list comprehension): construir una nueva lista seleccionando elementos que cumplen una condición, de forma declarativa y compacta.

## Definiciones

- **Comprensión de lista** — expresión que construye una lista filtrando/transformando otra. Clave: declarativa y compacta.
- **Filtro** — condición que decide qué elementos entran. Clave: `if x % 2 == 0`.
- **Predicado** — condición booleana sobre cada elemento. Clave: define el filtro.
- **Estilo declarativo** — describir el resultado, no los pasos. Clave: menos ruido que el bucle.

## Forma neutral

```text
LEER lista
pares <- [x EN lista SI x es par]
ESCRIBIR "pares=" UNIR(pares, "-")
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
