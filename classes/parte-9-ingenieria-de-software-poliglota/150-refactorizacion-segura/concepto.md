# Concepto — Refactorización segura

Conocimiento independiente del lenguaje.

Practicar la **refactorización segura**: mejorar la estructura interna del código sin cambiar su comportamiento observable, respaldado por pruebas. Cambiar `n*2` por `n+n` es una refactorización que las pruebas confirman equivalente.

## Definiciones

- **Refactorización** — reestructurar el código sin alterar su comportamiento observable. Clave: mejora interna.
- **Comportamiento observable** — lo que el usuario/prueba percibe. Clave: no debe cambiar al refactorizar.
- **Red de seguridad** — las pruebas que confirman que la refactorización no rompió nada. Clave: sin ellas, refactorizar es arriesgado.

## Forma neutral

```text
viejo <- n*2 ; nuevo <- n+n ; equivalente <- (viejo==nuevo) ; ESCRIBIR
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
