# Concepto — Expresiones condicionales: ternario e if como expresión

Conocimiento independiente del lenguaje.

Usar el **operador ternario** o el `if` como expresión: elegir un valor en una sola línea. En Rust y Kotlin el propio `if` devuelve valor; en C/Java/JS/PHP se usa `?:`.

## Definiciones

- **Operador ternario** — `cond ? a : b`: elige a o b según la condición. Clave: expresión, no sentencia.
- **Expresión** — código que produce un valor. Clave: se puede asignar.
- **Sentencia** — código que ejecuta una acción. Clave: no siempre produce valor.
- **if-expresión** — un if que devuelve un valor (Rust, Kotlin). Clave: no necesita ternario aparte.

## Forma neutral

```text
LEER a, b
max <- SI a > b ENTONCES a SINO b
ESCRIBIR "max=" max
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
