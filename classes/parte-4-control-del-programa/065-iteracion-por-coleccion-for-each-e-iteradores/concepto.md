# Concepto — Iteración por colección: for-each e iteradores

Conocimiento independiente del lenguaje.

Recorrer una colección con `for-each` (para cada elemento), sin gestionar índices. Es la forma idiomática de procesar listas en casi todos los lenguajes.

## Definiciones

- **for-each** — bucle que recorre cada elemento de una colección. Clave: sin índice manual.
- **Colección** — estructura que agrupa varios valores (lista, arreglo). Clave: se recorre en orden.
- **Iterar** — visitar cada elemento una vez. Clave: base del procesamiento de datos.
- **Acumulación** — reunir un resultado (suma) recorriendo. Clave: patrón universal.

## Forma neutral

```text
LEER lista
suma <- 0
PARA CADA x EN lista: suma <- suma + x
ESCRIBIR "suma=" suma
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
