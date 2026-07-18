# Concepto — Otros formatos y persistencia: CSV, YAML, binarios, bases de datos

Conocimiento independiente del lenguaje.

Cerrar la parte con **persistencia y formatos tabulares**: CSV (valores separados por comas) es el formato más simple para guardar y compartir datos en tabla. Aquí se serializa una fila y se cuentan sus campos.

## Definiciones

- **CSV** — formato tabular: filas de valores separados por comas. Clave: simple y universal.
- **Campo** — cada valor de una fila CSV. Clave: separado por el delimitador.
- **Persistencia** — guardar datos para recuperarlos después. Clave: archivos, bases de datos.

## Forma neutral

```text
LEER lista ; csv <- unir con , ; campos <- longitud
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
