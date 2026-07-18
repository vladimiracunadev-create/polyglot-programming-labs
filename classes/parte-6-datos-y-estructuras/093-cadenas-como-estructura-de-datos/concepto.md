# Concepto — Cadenas como estructura de datos

Conocimiento independiente del lenguaje.

Tratar una **cadena como estructura de datos**: una secuencia de caracteres que se puede recorrer, indexar e invertir. Verás que la inmutabilidad obliga a construir una nueva cadena.

## Definiciones

- **Cadena** — secuencia de caracteres. Clave: se recorre como una colección.
- **Inmutable** — no se modifica en sitio (Java/Python/C#). Clave: invertir crea otra.
- **Índice de carácter** — posición dentro de la cadena. Clave: base 0.

## Forma neutral

```text
LEER w ; recorrer del final al inicio ; ESCRIBIR invertido
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
