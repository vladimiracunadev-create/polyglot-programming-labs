# Concepto — Nulabilidad: null, nil, None, Option y valores ausentes

Conocimiento independiente del lenguaje.

Modelar la **ausencia de valor**: null, nil, None, Option. Usando 0 como centinela de 'ausente', verás cómo cada lenguaje representa y maneja la falta de un dato, y por qué las opciones tipadas (Option/Result) evitan el temido puntero nulo.

## Definiciones

- **Nulabilidad** — posibilidad de que un valor esté ausente. Clave: fuente clásica de errores.
- **null / nil / None** — representación de 'sin valor'. Clave: cada lenguaje lo llama distinto.
- **Option / Maybe** — tipo que envuelve 'hay valor' o 'no hay' (Rust, Haskell). Clave: obliga a manejar la ausencia.
- **Valor centinela** — un valor normal usado para significar 'ausente' (aquí, 0). Clave: sencillo pero frágil.

## Forma neutral

```text
LEER n
SI n == 0: ESCRIBIR "valor=ausente"
SINO: ESCRIBIR "valor=" n
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
