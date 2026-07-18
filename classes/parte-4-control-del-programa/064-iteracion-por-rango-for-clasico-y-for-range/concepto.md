# Concepto — Iteración por rango: for clásico y for-range

Conocimiento independiente del lenguaje.

Usar el bucle `for` cuando el número de vueltas se conoce. El factorial multiplica de 1 a n y muestra el `for` clásico y el `for`-range de cada lenguaje.

## Definiciones

- **for** — bucle con inicialización, condición e incremento. Clave: para un número conocido de vueltas.
- **for-range** — recorrer un rango o colección sin gestionar el índice (Python, Rust, Go). Clave: menos errores.
- **Factorial** — n! = 1·2·…·n. Clave: 0! = 1 por definición.
- **Acumulador de producto** — variable que empieza en 1 y se multiplica. Clave: 1 es el neutro del producto.

## Forma neutral

```text
LEER n
f <- 1
PARA i de 1 a n: f <- f*i
ESCRIBIR "factorial=" f
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
