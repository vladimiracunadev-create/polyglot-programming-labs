# Concepto — Componente de datos y consultas (SQL)

Conocimiento independiente del lenguaje.

Construir el **componente de datos y consultas** (SQL): la capa de persistencia responde consultas. Aquí agrega (suma) un conjunto de valores, como haría una consulta de agregación.

## Definiciones

- **Componente de datos** — la capa que almacena y consulta la información. Clave: fuente de verdad del sistema.
- **Agregación** — combinar muchas filas en un valor (SUM, AVG). Clave: resumen de datos.
- **Consulta declarativa** — describir qué datos se quieren, no cómo obtenerlos. Clave: propio de SQL.

## Forma neutral

```text
LEER valores ; total <- suma ; ESCRIBIR total
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
