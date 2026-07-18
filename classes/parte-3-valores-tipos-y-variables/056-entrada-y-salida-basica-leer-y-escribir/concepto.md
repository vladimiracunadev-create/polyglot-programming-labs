# Concepto — Entrada y salida básica: leer y escribir

Conocimiento independiente del lenguaje.

Cerrar la Parte 3 con lo más elemental: **leer de la entrada estándar y escribir en la salida estándar**. Todo el curso se apoya en este contrato (stdin → stdout), y aquí se ve desnudo en los 10 lenguajes.

## Definiciones

- **stdin** — canal de entrada estándar de un programa. Clave: de donde se leen los datos por defecto.
- **stdout** — canal de salida estándar. Clave: donde se escribe el resultado que se verifica.
- **Leer una línea** — obtener texto hasta el salto de línea. Clave: incluye espacios internos.
- **Eco** — devolver la entrada tal cual (con un prefijo). Clave: el ejemplo mínimo de E/S.

## Forma neutral

```text
LEER linea
ESCRIBIR "eco: " linea
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
