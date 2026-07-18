# Concepto — Interfaces, traits y clases abstractas

Conocimiento independiente del lenguaje.

Usar **interfaces / traits / clases abstractas**: un contrato que varios tipos implementan. Distintas figuras exponen `area()` y el programa las usa sin conocer el tipo concreto.

## Definiciones

- **Interfaz** — conjunto de métodos que un tipo promete implementar. Clave: contrato sin código.
- **Trait** — el equivalente en Rust; puede llevar métodos por defecto. Clave: composición de comportamiento.
- **Clase abstracta** — clase incompleta que otras extienden. Clave: contrato + estado parcial.

## Forma neutral

```text
LEER figura ; f: Forma ; ESCRIBIR f.area()
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
