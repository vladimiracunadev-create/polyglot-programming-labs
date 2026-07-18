# Concepto — Argumentos nombrados y de palabra clave

Conocimiento independiente del lenguaje.

Usar **argumentos nombrados** (por palabra clave): pasar los valores indicando a qué parámetro corresponden, mejorando la legibilidad y permitiendo cualquier orden. No todos los lenguajes los tienen.

## Definiciones

- **Argumento nombrado** — se pasa indicando el parámetro (`y=4`). Clave: claridad y orden libre.
- **Argumento posicional** — se pasa por su posición. Clave: depende del orden.
- **Palabra clave** — el nombre del parámetro usado al llamar (Python `**kwargs`). Clave: base de los nombrados.
- **Legibilidad de la llamada** — entender qué es cada valor sin ver la firma. Clave: menos errores.

## Forma neutral

```text
LEER a, b
ESCRIBIR punto(x=a, y=b)
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
