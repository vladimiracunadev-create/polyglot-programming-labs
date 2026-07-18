# Concepto — Rangos y secuencias

Conocimiento independiente del lenguaje.

Usar **rangos y secuencias**: describir una serie de valores consecutivos sin listarlos. Los rangos alimentan bucles y comprensiones de forma expresiva.

## Definiciones

- **Rango** — intervalo de valores consecutivos (`2..5`). Clave: describe sin enumerar.
- **Inclusivo** — incluye el extremo final. Clave: `1..=n` en Rust, `range` en Python es exclusivo.
- **Secuencia** — serie ordenada de valores. Clave: puede ser perezosa.

## Forma neutral

```text
LEER a, b ; generar a..b ; sumar
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
