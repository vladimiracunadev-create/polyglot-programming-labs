# Concepto — Operadores y expresiones: aritméticos, lógicos, de comparación y bit a bit

Conocimiento independiente del lenguaje.

Repasar los **operadores aritméticos** y ver diferencias sutiles: la división entera y el módulo se comportan distinto con negativos según el lenguaje (aquí usamos positivos para que coincidan). Es la base del cálculo en todo programa.

## Definiciones

- **Operador** — símbolo que combina valores para producir otro (+, *, %). Clave: bloque de las expresiones.
- **División entera** — cociente sin decimales. Clave: `7/2 = 3`, no 3.5.
- **Módulo** — resto de la división entera. Clave: `7 % 2 = 1`.
- **Precedencia** — el orden de evaluación (`*` antes que `+`). Clave: los paréntesis mandan.

## Forma neutral

```text
LEER a, b
ESCRIBIR suma, resta, mult, división entera y módulo
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
