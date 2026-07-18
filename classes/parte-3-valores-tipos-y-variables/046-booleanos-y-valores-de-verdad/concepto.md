# Concepto — Booleanos y valores de verdad

Conocimiento independiente del lenguaje.

Dominar el álgebra booleana básica: **AND** (ambos), **OR** (alguno) y **NOT** (negación). Es la base de toda condición y decisión. Cada lenguaje representa e imprime los booleanos de forma propia (`true`/`True`), lo que obliga a normalizar la salida.

## Definiciones

- **Booleano** — valor de verdad: verdadero o falso. Clave: resultado de comparaciones y condiciones.
- **AND (∧)** — verdadero solo si ambos lo son. Clave: conjunción.
- **OR (∨)** — verdadero si al menos uno lo es. Clave: disyunción.
- **NOT (¬)** — invierte el valor de verdad. Clave: negación.

## Forma neutral

```text
LEER a, b
ba <- (a != 0) ; bb <- (b != 0)
ESCRIBIR "and=" (ba Y bb) " or=" (ba O bb) " not_a=" (NO ba)
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
