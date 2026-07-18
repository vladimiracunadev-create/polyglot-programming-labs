# Concepto — Tipado fuerte vs. débil

Conocimiento independiente del lenguaje.

Distinguir **tipado fuerte** (no mezcla tipos sin permiso) de **débil** (convierte soluto). El mismo `+` puede sumar números o concatenar texto: verlo lado a lado aclara por qué `'5' + '5'` puede ser `10` o `'55'` según el lenguaje.

## Definiciones

- **Tipado fuerte** — no permite operar entre tipos incompatibles sin conversión (Python, Java). Clave: menos sorpresas.
- **Tipado débil** — convierte tipos automáticamente para operar (PHP, JS). Clave: `'5'+5` puede dar cosas raras.
- **Concatenación** — unir dos cadenas. Clave: en muchos lenguajes también con `+`.
- **Sobrecarga de operador** — un operador con distinto significado según los tipos. Clave: `+` suma o concatena.

## Forma neutral

```text
LEER n
ESCRIBIR "suma=" (n+n) " texto=" (TEXTO(n) ++ TEXTO(n))
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
