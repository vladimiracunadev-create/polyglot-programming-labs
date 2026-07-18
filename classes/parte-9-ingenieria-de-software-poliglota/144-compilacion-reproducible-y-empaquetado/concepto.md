# Concepto — Compilación reproducible y empaquetado

Conocimiento independiente del lenguaje.

Entender la **compilación reproducible y el empaquetado**: una build reproducible produce siempre el mismo artefacto para la misma entrada, comprobable con una suma de verificación (checksum). Aquí el checksum es la suma de los valores.

## Definiciones

- **Compilación reproducible** — produce un artefacto idéntico byte a byte para la misma entrada. Clave: confianza y auditoría.
- **Checksum** — valor derivado de los datos que cambia si estos cambian. Clave: detecta alteraciones.
- **Artefacto** — salida de la build (binario, paquete). Clave: se verifica con su checksum.

## Forma neutral

```text
LEER lista ; checksum <- suma ; ESCRIBIR checksum
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
