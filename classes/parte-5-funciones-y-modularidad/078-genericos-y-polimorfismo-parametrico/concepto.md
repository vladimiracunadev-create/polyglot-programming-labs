# Concepto — Genéricos y polimorfismo paramétrico

Conocimiento independiente del lenguaje.

Escribir una función **genérica**: la misma lógica para varios tipos, sin duplicar código. `max<T>` funciona con enteros, reales o texto porque solo exige que el tipo sea comparable.

## Definiciones

- **Genérico** — función/tipo parametrizado por otro tipo (`max<T>`). Clave: reutilización con seguridad de tipos.
- **Polimorfismo paramétrico** — un código que funciona para muchos tipos. Clave: distinto del de herencia.
- **Restricción de tipo** — condición sobre el parámetro de tipo (comparable). Clave: habilita las operaciones.
- **Inferencia de tipo genérico** — el compilador deduce T al llamar. Clave: no hay que anotarlo.

## Forma neutral

```text
FUNCION max<T comparable>(a,b): DEVOLVER a SI a>b SINO b
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
