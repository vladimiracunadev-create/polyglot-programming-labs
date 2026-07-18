# Concepto — Enumeraciones y tipos algebraicos (ADT / sum types)

Conocimiento independiente del lenguaje.

Usar **tipos algebraicos (suma)**: un valor que es una de varias alternativas, cada una con sus datos. `Forma = Cuadrado | Rectangulo`. El `match` decide y calcula según la variante.

## Definiciones

- **Tipo algebraico (suma)** — valor que es una de varias alternativas (Cuadrado o Rectangulo). Clave: modela 'o esto o lo otro'.
- **Variante** — cada alternativa del tipo suma, con sus propios datos. Clave: `Cuadrado(lado)`.
- **Exhaustividad** — cubrir todas las variantes. Clave: Rust lo exige al compilar.

## Forma neutral

```text
LEER tipo y datos ; COINCIDIR tipo: cuadrado->l*l ; rectangulo->a*b
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
