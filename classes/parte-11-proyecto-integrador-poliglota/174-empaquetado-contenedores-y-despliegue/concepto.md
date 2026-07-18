# Concepto — Empaquetado, contenedores y despliegue

Conocimiento independiente del lenguaje.

Realizar el **empaquetado, los contenedores y el despliegue**: meter el sistema y su entorno en una imagen de contenedor reproducible. Aquí se construye el nombre de la imagen a partir de la versión.

## Definiciones

- **Contenedor** — empaqueta el programa con su entorno mínimo. Clave: elimina el 'funciona en mi máquina'.
- **Imagen** — plantilla de la que se crean contenedores, etiquetada con una versión. Clave: `app:1.2.3`.
- **Despliegue** — poner en marcha la imagen en un entorno. Clave: reproducible y versionado.

## Forma neutral

```text
LEER version ; ESCRIBIR 'imagen=app:' + version
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
