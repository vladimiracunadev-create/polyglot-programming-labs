# Concepto — Gestión manual de memoria (C): malloc/free

Conocimiento independiente del lenguaje.

Practicar la **gestión manual de memoria** de C: reservar con malloc, usar y liberar con free. En los lenguajes con recolector esto es automático; en C es responsabilidad del programador.

## Definiciones

- **malloc** — reserva un bloque de memoria en el heap (C). Clave: devuelve un puntero.
- **free** — libera un bloque previamente reservado. Clave: olvidarlo causa fugas.
- **Fuga de memoria** — memoria reservada que nunca se libera. Clave: el programa la va acumulando.

## Forma neutral

```text
reservar(n) ; llenar 1..n ; sumar ; liberar
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
