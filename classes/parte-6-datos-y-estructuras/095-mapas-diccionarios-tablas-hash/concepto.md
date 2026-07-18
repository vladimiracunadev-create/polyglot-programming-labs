# Concepto — Mapas / diccionarios / tablas hash

Conocimiento independiente del lenguaje.

Usar un **mapa (diccionario)**: asociar claves con valores. Contar frecuencias es el uso más común: la clave es el número y el valor, cuántas veces aparece.

## Definiciones

- **Mapa** — colección de pares clave→valor (dict, HashMap). Clave: búsqueda por clave en O(1).
- **Clave** — identificador único de una entrada. Clave: no se repite.
- **Frecuencia** — cuántas veces aparece un valor. Clave: uso típico del mapa.

## Forma neutral

```text
LEER lista ; construir mapa de frecuencias ; ESCRIBIR frecuencia del primero
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
