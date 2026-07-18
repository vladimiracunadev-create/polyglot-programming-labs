# Concepto — Lógico: reglas, hechos y unificación (Prolog)

Conocimiento independiente del lenguaje.

Asomarse al paradigma **lógico** (Prolog): en vez de calcular paso a paso, se declaran hechos y reglas y se consulta si algo se cumple. Aquí la regla `es_divisor(a, b)` es verdadera si a divide a b.

## Definiciones

- **Lógico** — paradigma en el que se declaran hechos y reglas y se consultan (Prolog). Clave: el motor deduce.
- **Regla** — relación condicional entre términos. Clave: `es_divisor(A,B) :- B mod A =:= 0`.
- **Consulta** — pregunta al sistema sobre si algo se cumple. Clave: devuelve verdadero/falso o soluciones.

## Forma neutral

```text
REGLA es_divisor(a,b) SI b mod a == 0 ; CONSULTAR es_divisor(a,b)
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
