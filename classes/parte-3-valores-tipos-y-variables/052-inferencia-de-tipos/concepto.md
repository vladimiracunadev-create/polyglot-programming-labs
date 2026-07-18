# Concepto — Inferencia de tipos

Conocimiento independiente del lenguaje.

Ver la **inferencia de tipos**: el compilador deduce el tipo sin que lo anotes. Un producto de dos enteros basta para comparar `x = a*b` (Python), `var`/`:=` (C#/Go), `let` (Rust) frente a la anotación explícita de Java o C.

## Definiciones

- **Inferencia de tipos** — el compilador deduce el tipo a partir del valor. Clave: menos ruido, mismo tipado estático.
- **Anotación de tipo** — escribir el tipo explícitamente (`int x`). Clave: obligatoria donde no hay inferencia.
- **var / := / let** — formas de declarar con inferencia (C#, Go, Rust). Clave: el tipo se fija igual.
- **Estático con inferencia** — tipos fijos que no hace falta anotar. Clave: no confundir con dinámico.

## Forma neutral

```text
LEER a, b
ESCRIBIR "producto=" (a*b)
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
