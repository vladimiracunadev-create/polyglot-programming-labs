# Concepto — Iteradores y generadores perezosos (lazy)

Conocimiento independiente del lenguaje.

Producir una secuencia bajo demanda, la idea detrás de los **iteradores y generadores perezosos**: calcular los valores uno a uno en lugar de tener toda la lista de antemano.

## Definiciones

- **Iterador** — objeto que produce valores uno a uno. Clave: no necesita toda la colección en memoria.
- **Generador** — función que produce una secuencia perezosa (yield). Clave: calcula al vuelo.
- **Evaluación perezosa** — calcular un valor solo cuando se pide. Clave: permite secuencias infinitas.
- **take** — tomar los primeros n de una secuencia. Clave: corta lo infinito.

## Forma neutral

```text
LEER n
PARA i de 1 a n: emitir 2*i
ESCRIBIR "pares=" UNIR(emitidos, "-")
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
