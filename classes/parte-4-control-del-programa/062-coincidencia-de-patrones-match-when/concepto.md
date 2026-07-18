# Concepto — Coincidencia de patrones: match / when

Conocimiento independiente del lenguaje.

Usar **coincidencia de patrones** (`match`/`when`) para decidir según la forma o el rango de un valor. Es más expresiva y segura que el switch clásico: obliga a cubrir todos los casos.

## Definiciones

- **Coincidencia de patrones** — elegir una rama según la estructura o el rango de un valor. Clave: más potente que el switch.
- **Exhaustividad** — el compilador exige cubrir todos los casos (Rust). Clave: evita olvidos.
- **Guarda de patrón** — condición extra dentro de un caso (`n if n>0`). Clave: refina el patrón.
- **match** — construcción de coincidencia de patrones (Rust, Python 3.10+). Clave: sin fallthrough.

## Forma neutral

```text
LEER n
COINCIDIR n: (>0)->positivo ; (<0)->negativo ; (0)->cero
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
