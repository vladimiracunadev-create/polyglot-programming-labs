# Concepto — La pila (stack) y el marco de llamada

Conocimiento independiente del lenguaje.

Entender la **pila (stack) y el marco de llamada**: cada llamada a función crea un marco con sus variables; la recursión los apila. La profundidad de la recursión es cuántos marcos hay a la vez.

## Definiciones

- **Pila (stack)** — región de memoria para los marcos de llamada. Clave: LIFO, rápida.
- **Marco de llamada** — espacio de una llamada: parámetros, locales, dirección de retorno. Clave: se apila al llamar.
- **Desbordamiento de pila** — cuando hay demasiados marcos. Clave: recursión muy profunda lo causa.

## Forma neutral

```text
sumar(n) = n + sumar(n-1) ; sumar(0) = 0 ; profundidad = n
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
