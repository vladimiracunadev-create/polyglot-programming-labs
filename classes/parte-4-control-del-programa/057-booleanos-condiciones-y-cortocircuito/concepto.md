# Concepto — Booleanos, condiciones y cortocircuito

Conocimiento independiente del lenguaje.

Producir booleanos con operadores de comparación y combinarlos con **AND cortocircuitado**. El cortocircuito evita evaluar la segunda condición si la primera ya decide el resultado.

## Definiciones

- **Condición** — expresión que da verdadero o falso. Clave: gobierna las decisiones.
- **Cortocircuito** — en `a && b`, si `a` es falso no se evalúa `b`. Clave: evita trabajo y errores.
- **Operador relacional** — compara valores (>, <, ==). Clave: produce booleanos.
- **Predicado** — condición sobre un valor (es positivo, es par). Clave: bloque de la lógica.

## Forma neutral

```text
LEER n
ESCRIBIR positivo=(n>0), par=(n%2==0), ambos=((n>0) Y (n%2==0))
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
