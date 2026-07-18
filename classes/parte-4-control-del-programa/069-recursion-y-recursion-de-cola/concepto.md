# Concepto — Recursión y recursión de cola

Conocimiento independiente del lenguaje.

Escribir una función **recursiva**: que se llama a sí misma con un caso base y un caso recursivo. Fibonacci es el ejemplo clásico; también sirve para hablar de eficiencia y de recursión de cola.

## Definiciones

- **Recursión** — técnica en que una función se invoca a sí misma. Clave: necesita un caso base.
- **Caso base** — el que se resuelve sin recursión. Clave: evita la recursión infinita.
- **Caso recursivo** — reduce el problema hacia el caso base. Clave: debe acercarse a él.
- **Recursión de cola** — la llamada recursiva es lo último que se hace. Clave: algunos lenguajes la optimizan.

## Forma neutral

```text
FUNCION fib(n): SI n<2 DEVOLVER n ; SINO DEVOLVER fib(n-1)+fib(n-2)
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
