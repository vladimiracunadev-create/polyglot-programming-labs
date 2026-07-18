# Concepto — La FFI (Foreign Function Interface): llamar a C desde todos

Conocimiento independiente del lenguaje.

Entender la **FFI (Foreign Function Interface)**: el mecanismo para llamar a código escrito en otro lenguaje, típicamente C. Casi todos los lenguajes pueden llamar a C, lo que hace de C el 'idioma común' entre lenguajes.

## Definiciones

- **FFI** — interfaz para llamar a funciones de otro lenguaje. Clave: reutilizar librerías nativas.
- **Función externa** — definida en otro lenguaje (C) y llamada desde el tuyo. Clave: se declara su firma.
- **C como lingua franca** — casi todos los lenguajes exponen una FFI hacia C. Clave: puente universal.

## Forma neutral

```text
declarar doble (externa) ; ESCRIBIR doble(n)
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
