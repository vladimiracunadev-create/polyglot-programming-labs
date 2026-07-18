# Concepto — Funciones de orden superior: map, filter, reduce

Conocimiento independiente del lenguaje.

Combinar las tres funciones de orden superior clásicas: **map** (transformar cada elemento), **filter** (seleccionar) y **reduce** (combinar en un valor). Aquí se usan map y reduce sobre una lista.

## Definiciones

- **map** — aplica una función a cada elemento y devuelve una colección nueva. Clave: transforma sin mutar.
- **reduce** — combina todos los elementos en un valor (suma, producto). Clave: acumula.
- **Función de orden superior** — recibe o devuelve otra función. Clave: base del estilo funcional.
- **Encadenamiento** — conectar operaciones (map → reduce). Clave: pipeline de datos.

## Forma neutral

```text
LEER lista
doblados <- MAP(x -> 2x, lista)
total <- REDUCE(+, doblados)
ESCRIBIR "doblados=" UNIR(doblados,"-") " total=" total
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
