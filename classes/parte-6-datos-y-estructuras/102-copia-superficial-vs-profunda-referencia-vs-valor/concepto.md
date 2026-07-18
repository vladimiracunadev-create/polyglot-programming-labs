# Concepto — Copia superficial vs. profunda; referencia vs. valor

Conocimiento independiente del lenguaje.

Distinguir **copia** de **referencia compartida**, y **copia superficial** de **profunda**. Copiar una lista de valores y modificar la copia no altera el original; con referencias compartidas, sí.

## Definiciones

- **Copia** — duplicado independiente. Clave: modificarlo no afecta al original.
- **Referencia compartida** — dos nombres para el mismo dato. Clave: cambiar uno cambia el otro.
- **Superficial vs. profunda** — copiar solo el nivel externo o todo el contenido. Clave: importa con datos anidados.

## Forma neutral

```text
LEER lista ; copia <- COPIA(lista) ; copia[fin] <- 99 ; ESCRIBIR original y copia
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
