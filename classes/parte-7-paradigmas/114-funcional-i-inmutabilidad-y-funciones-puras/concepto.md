# Concepto — Funcional I: inmutabilidad y funciones puras

Conocimiento independiente del lenguaje.

Practicar el paradigma **funcional (I)**: inmutabilidad y funciones puras. Transformar una lista con `map` produce una lista nueva sin alterar la original ni usar estado mutable.

## Definiciones

- **Funcional** — paradigma basado en funciones puras e inmutabilidad. Clave: sin efectos ni estado mutable.
- **Inmutabilidad** — los datos no cambian; las transformaciones crean nuevos. Clave: más seguro.
- **map** — aplica una función a cada elemento y devuelve una colección nueva. Clave: no muta.

## Forma neutral

```text
doblados <- MAP(x -> 2x, lista) ; ESCRIBIR unidos por -
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
