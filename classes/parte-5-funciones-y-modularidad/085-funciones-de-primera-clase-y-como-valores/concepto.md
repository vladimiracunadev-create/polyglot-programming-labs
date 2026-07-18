# Concepto — Funciones de primera clase y como valores

Conocimiento independiente del lenguaje.

Tratar las funciones como **valores de primera clase**: guardarlas en variables y pasarlas como argumentos. `aplicar(suma, a, b)` ejecuta la función recibida; es la base de map/filter/reduce y de los callbacks.

## Definiciones

- **Valor de primera clase** — algo que se puede guardar, pasar y devolver. Clave: las funciones lo son en casi todos los lenguajes.
- **Función de orden superior** — recibe o devuelve funciones. Clave: `aplicar(f, a, b)`.
- **Callback** — función pasada para ejecutarse después. Clave: base de eventos y asincronía.
- **Puntero a función** — en C, un valor que apunta a una función. Clave: su forma de primera clase.

## Forma neutral

```text
FUNCION aplicar(f, a, b): DEVOLVER f(a, b)
ESCRIBIR "suma=" aplicar(suma,a,b) " producto=" aplicar(producto,a,b)
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
