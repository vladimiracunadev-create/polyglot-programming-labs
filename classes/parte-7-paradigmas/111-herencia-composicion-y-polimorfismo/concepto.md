# Concepto — Herencia, composición y polimorfismo

Conocimiento independiente del lenguaje.

Practicar **herencia, composición y polimorfismo**: distintos tipos que comparten una interfaz común (`sonido`) y responden cada uno a su manera. Llamar al mismo método da resultados distintos según el tipo real.

## Definiciones

- **Herencia** — un tipo hereda estado/comportamiento de otro. Clave: reutiliza y especializa.
- **Polimorfismo** — el mismo método se comporta distinto según el tipo real. Clave: `animal.sonido()`.
- **Composición** — construir un objeto a partir de otros (tiene-un) en vez de heredar (es-un). Clave: más flexible.

## Forma neutral

```text
LEER tipo ; crear animal ; ESCRIBIR animal.sonido()
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
