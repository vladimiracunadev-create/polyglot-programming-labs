# Concepto — Errores: de sintaxis, de tipos, de enlace y de ejecución

Conocimiento independiente del lenguaje.

Clasificar los **tipos de error** por el momento en que aparecen: de sintaxis (al parsear), de tipos (al comprobar tipos), de enlace (al unir con librerías) y de ejecución (al correr). Saber cuándo ocurre cada uno acelera el diagnóstico.

## Definiciones

- **Error de sintaxis** — el código viola las reglas gramaticales. Clave: se detecta al parsear.
- **Error de tipos** — operación no válida para los tipos implicados. Clave: en compilación (estáticos) o ejecución (dinámicos).
- **Error de enlace** — no se encuentra una función/símbolo al unir con librerías. Clave: entre compilar y ejecutar.
- **Error de ejecución** — ocurre al correr (división por cero, índice fuera de rango). Clave: en tiempo de ejecución.

## Forma neutral

```text
LEER codigo ; SEGUN codigo: 1..4 -> nombre del error
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
