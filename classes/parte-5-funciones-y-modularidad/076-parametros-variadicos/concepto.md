# Concepto — Parámetros variádicos

Conocimiento independiente del lenguaje.

Definir una función **variádica**: acepta un número variable de argumentos. Es lo que hay detrás de `print(...)` o `sum(...)`. Cada lenguaje lo expresa con `*args`, `...`, `params` o slices.

## Definiciones

- **Función variádica** — acepta un número variable de argumentos. Clave: `sum(1,2,3,...)`.
- ***args / ...** — sintaxis para recolectar argumentos variables. Clave: llegan como colección.
- **Empaquetar** — reunir los argumentos sueltos en una lista. Clave: dentro de la función.
- **Desempaquetar** — expandir una lista en argumentos sueltos. Clave: la operación inversa.

## Forma neutral

```text
FUNCION suma(...nums): DEVOLVER Σ nums
LEER lista ; ESCRIBIR "suma=" suma(lista)
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
