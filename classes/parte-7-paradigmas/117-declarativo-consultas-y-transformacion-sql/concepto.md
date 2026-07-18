# Concepto — Declarativo: consultas y transformación (SQL)

Conocimiento independiente del lenguaje.

Practicar el paradigma **declarativo**: describir *qué* resultado se quiere, no *cómo* obtenerlo. Sumar los pares se expresa como 'la suma de los que son pares', dejando el cómo al lenguaje.

## Definiciones

- **Declarativo** — paradigma que describe el resultado deseado, no los pasos. Clave: el motor decide el cómo.
- **Filtro** — seleccionar los elementos que cumplen una condición. Clave: `WHERE`, `filter`.
- **Agregación** — combinar varios valores en uno (suma). Clave: `SUM`, `reduce`.

## Forma neutral

```text
suma_pares <- SUMA(FILTRAR(par, lista))
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
