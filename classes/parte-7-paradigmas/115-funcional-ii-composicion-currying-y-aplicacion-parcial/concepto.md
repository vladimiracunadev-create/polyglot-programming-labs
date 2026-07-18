# Concepto — Funcional II: composición, currying y aplicación parcial

Conocimiento independiente del lenguaje.

Practicar el paradigma **funcional (II)**: composición de funciones. Combinar funciones pequeñas (`doblar`, `incrementar`) en una mayor, aplicando primero una y luego la otra.

## Definiciones

- **Composición de funciones** — combinar funciones: `(f ∘ g)(x) = f(g(x))`. Clave: construir con piezas.
- **Currying** — transformar una función de varios argumentos en una cadena de funciones de uno. Clave: aplicación parcial.
- **Aplicación parcial** — fijar algunos argumentos y obtener una función nueva. Clave: reutilización.

## Forma neutral

```text
doblar(x)=2x ; inc(x)=x+1 ; compuesta = inc ∘ doblar ; ESCRIBIR compuesta(n)
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
