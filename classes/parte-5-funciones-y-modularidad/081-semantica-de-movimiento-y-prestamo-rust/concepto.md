# Concepto — Semántica de movimiento y préstamo (Rust)

Conocimiento independiente del lenguaje.

Entender la **semántica de movimiento y préstamo** de Rust: un valor tiene un dueño; se puede **prestar** (borrow) para leerlo sin copiar, o **mover** (move) transfiriendo la propiedad. Otros lenguajes copian o comparten referencias con GC.

## Definiciones

- **Propiedad** — cada valor tiene un único dueño responsable de liberarlo. Clave: base de la seguridad de Rust.
- **Préstamo** — referencia temporal para leer/usar sin tomar la propiedad. Clave: `&valor`.
- **Movimiento** — transferir la propiedad a otra variable. Clave: la original deja de ser válida.
- **Copia vs. GC** — otros lenguajes copian o rastrean referencias con recolector. Clave: modelo distinto.

## Forma neutral

```text
LEER w ; len <- longitud(prestar w)
mostrar(mover w)
ESCRIBIR "movido=" w " longitud=" len
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
