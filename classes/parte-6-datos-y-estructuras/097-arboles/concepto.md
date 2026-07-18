# Concepto — Árboles

Conocimiento independiente del lenguaje.

Conocer los **árboles**: estructuras jerárquicas. En un árbol binario de búsqueda (BST), el recorrido in-order devuelve los elementos ordenados. Aquí el efecto observable es la ordenación.

## Definiciones

- **Árbol** — estructura jerárquica de nodos con hijos. Clave: sin ciclos, una raíz.
- **BST** — árbol binario ordenado: izquierda < nodo < derecha. Clave: búsqueda O(log n) equilibrado.
- **In-order** — recorrido izquierda-raíz-derecha. Clave: en un BST da los valores ordenados.

## Forma neutral

```text
LEER lista ; insertar en BST ; recorrer in-order
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
