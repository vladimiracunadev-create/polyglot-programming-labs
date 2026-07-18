# Concepto — Persistencia y almacenamiento

Conocimiento independiente del lenguaje.

Construir la **persistencia y el almacenamiento**: guardar datos para recuperarlos después. Aquí se almacena un par clave/valor y se confirma lo guardado, como haría un almacén clave-valor.

## Definiciones

- **Persistencia** — guardar datos de forma duradera (disco, base de datos). Clave: sobreviven al reinicio.
- **Almacén clave-valor** — guarda valores indexados por una clave (Redis, mapas persistentes). Clave: acceso rápido por clave.
- **Durabilidad** — garantía de que lo guardado no se pierde. Clave: propiedad clave del almacenamiento.

## Forma neutral

```text
LEER clave, valor ; guardar ; confirmar clave=valor
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
