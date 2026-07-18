# Concepto — Recolección de basura (GC)

Conocimiento independiente del lenguaje.

Entender la **recolección de basura (GC)**: el runtime libera automáticamente la memoria de los objetos que ya no son alcanzables. El programador no llama a free; el GC lo hace.

## Definiciones

- **Recolección de basura** — liberación automática de objetos ya inalcanzables. Clave: sin free manual.
- **Alcanzable** — objeto accesible desde una variable viva. Clave: lo inalcanzable es basura.
- **Pausa del GC** — momento en que el recolector trabaja. Clave: puede introducir latencia.

## Forma neutral

```text
crear n objetos ; descartar referencias ; el GC recolecta
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
