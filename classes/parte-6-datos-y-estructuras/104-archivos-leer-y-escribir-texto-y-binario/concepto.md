# Concepto — Archivos: leer y escribir texto y binario

Conocimiento independiente del lenguaje.

Procesar **contenido textual** como el de un archivo: leer una línea y extraer información (palabras, caracteres). Es el modelo de la lectura de archivos, aquí por la entrada estándar para poder verificarlo.

## Definiciones

- **Contenido de texto** — los caracteres de un archivo o entrada. Clave: se procesa línea a línea.
- **Palabra** — secuencia separada por espacios. Clave: se cuenta partiendo por espacios.
- **Carácter** — cada símbolo, incluidos los espacios. Clave: la longitud total.

## Forma neutral

```text
LEER linea ; palabras <- partir por espacios ; caracteres <- longitud
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
