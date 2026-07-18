# Concepto — Control de flujo: break, continue, return, goto

Conocimiento independiente del lenguaje.

Usar `break` para salir de un bucle en cuanto se cumple una condición. Buscar el primer divisor es el caso típico: no hace falta seguir una vez encontrado.

## Definiciones

- **break** — termina el bucle inmediatamente. Clave: no sigue iterando.
- **continue** — salta al siguiente ciclo del bucle. Clave: ignora el resto de la vuelta.
- **Divisor** — número que divide a otro sin resto. Clave: el menor >1 revela si es primo.
- **goto** — salto incondicional (existe en C, desaconsejado). Clave: break/continue lo sustituyen.

## Forma neutral

```text
LEER n
PARA d de 2 a n: SI n%d==0: guardar d ; ROMPER
ESCRIBIR "primer_divisor=" d
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
