# Concepto — OO basado en prototipos (JavaScript)

Conocimiento independiente del lenguaje.

Conocer la **OO basada en prototipos** de JavaScript: los objetos heredan directamente de otros objetos, no de clases. Aquí un objeto con un método `doble` calcula sobre su valor.

## Definiciones

- **Prototipo** — objeto del que otro hereda propiedades y métodos. Clave: cadena de prototipos en JS.
- **Objeto literal** — objeto creado directamente con sus campos y métodos. Clave: `{ v: n, doble() {...} }`.
- **this** — referencia al objeto sobre el que se llama el método. Clave: accede a su estado.

## Forma neutral

```text
obj <- { valor: n, doble() { DEVOLVER valor*2 } } ; ESCRIBIR obj.doble()
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
