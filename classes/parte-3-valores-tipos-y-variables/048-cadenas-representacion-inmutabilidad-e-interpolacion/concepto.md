# Concepto — Cadenas: representación, inmutabilidad e interpolación

Conocimiento independiente del lenguaje.

Trabajar con **cadenas**: leer texto, interpolarlo en un saludo y medir su longitud. Verás que la longitud puede significar 'bytes' o 'caracteres' según el lenguaje (aquí, ASCII, coinciden).

## Definiciones

- **Cadena** — secuencia de caracteres. Clave: el tipo para todo texto.
- **Interpolación** — insertar el valor de una variable dentro de una cadena. Clave: `f"...{x}"`, `${x}`, etc.
- **Longitud** — número de unidades (caracteres/bytes) de la cadena. Clave: en ASCII coinciden.
- **Inmutabilidad de cadenas** — en Java, C#, Python las cadenas no se modifican in situ. Clave: se crea una nueva.

## Forma neutral

```text
LEER w
ESCRIBIR "hola=" w " longitud=" LONGITUD(w)
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
