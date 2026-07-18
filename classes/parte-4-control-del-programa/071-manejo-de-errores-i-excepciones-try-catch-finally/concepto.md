# Concepto — Manejo de errores I: excepciones (try/catch/finally)

Conocimiento independiente del lenguaje.

Manejar errores con **excepciones** (`try`/`catch`/`finally`): separar el camino feliz del manejo del error. Dividir por cero es el caso clásico que dispara una excepción en varios lenguajes.

## Definiciones

- **Excepción** — objeto que representa un error y desvía el flujo. Clave: se captura con try/catch.
- **try** — bloque que puede fallar. Clave: envuelve la operación arriesgada.
- **catch** — bloque que maneja la excepción. Clave: el plan B ante el error.
- **finally** — bloque que se ejecuta siempre (haya error o no). Clave: liberar recursos.

## Forma neutral

```text
LEER a, b
INTENTAR: r <- a/b ; ESCRIBIR "resultado=" r
CAPTURAR division_por_cero: ESCRIBIR "error=division por cero"
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
