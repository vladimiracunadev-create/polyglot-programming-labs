# Concepto — Funcional III: functores, mónadas y efectos (visión práctica)

Conocimiento independiente del lenguaje.

Practicar el paradigma **funcional (III)**: functores y mónadas en su forma práctica. `Option`/`Maybe` envuelve 'hay valor' o 'no hay', y `map` aplica una función solo si hay valor, sin comprobaciones dispersas.

## Definiciones

- **Functor** — contenedor sobre el que se puede aplicar `map` (Option, listas). Clave: transformar el contenido sin sacarlo.
- **Option/Maybe** — envuelve un valor presente (Some) o ausente (None). Clave: ausencia explícita y segura.
- **map sobre Option** — aplica la función si hay valor; si no, propaga la ausencia. Clave: sin ifs dispersos.

## Forma neutral

```text
opcion <- Some(n) SI n>0 SINO None ; ESCRIBIR opcion.map(x->2x) o 'nada'
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
