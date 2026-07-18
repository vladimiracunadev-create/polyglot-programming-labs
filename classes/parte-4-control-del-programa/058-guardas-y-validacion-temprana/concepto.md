# Concepto — Guardas y validación temprana

Conocimiento independiente del lenguaje.

Aplicar **guardas** (validación temprana): comprobar primero los casos inválidos o especiales y salir cuanto antes, dejando el camino principal limpio. Reduce el anidamiento y hace el código más legible.

## Definiciones

- **Guarda** — condición al inicio que corta el flujo si no se cumple. Clave: evita anidar.
- **Validación temprana** — rechazar entradas inválidas antes del cálculo. Clave: el camino feliz queda limpio.
- **Retorno temprano** — salir de la función en cuanto hay respuesta. Clave: menos ramas abiertas.
- **Camino feliz** — el flujo principal sin errores. Clave: se lee de corrido tras las guardas.

## Forma neutral

```text
LEER edad
SI edad < 0: ESCRIBIR "invalido" ; FIN
SI edad < 18: ESCRIBIR "menor" ; FIN
ESCRIBIR "adulto"
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
