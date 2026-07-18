# Concepto — Alcance (scope) y sombreado (shadowing)

Conocimiento independiente del lenguaje.

Comprender el **alcance (scope)** de las variables y el **sombreado (shadowing)**: dónde vive una variable y qué pasa cuando una interna reusa el nombre de una externa. Al salir del bloque, reaparece la externa.

## Definiciones

- **Alcance** — región del código donde una variable es visible. Clave: de bloque en la mayoría.
- **Sombreado** — una variable interna con el mismo nombre oculta a la externa. Clave: dentro del bloque.
- **Bloque** — conjunto de sentencias con su propio alcance. Clave: `{ ... }`.
- **Vida de la variable** — cuánto existe. Clave: termina al salir de su alcance.

## Forma neutral

```text
LEER n ; x <- n
BLOQUE: x_interno <- x + 10 ; imprimir interno
imprimir externo (x sigue siendo n)
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
