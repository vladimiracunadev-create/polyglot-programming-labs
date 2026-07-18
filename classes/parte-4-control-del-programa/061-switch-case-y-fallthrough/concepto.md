# Concepto — switch, case y fallthrough

Conocimiento independiente del lenguaje.

Usar `switch` / `case` (o su equivalente) para elegir entre valores exactos, con un caso por defecto. Verás el `fallthrough` (caída) de C/Java y cómo otros lenguajes lo evitan.

## Definiciones

- **switch** — estructura que elige una rama según el valor exacto. Clave: para muchos valores concretos.
- **case** — una de las ramas del switch. Clave: coincide con un valor.
- **fallthrough** — en C/Java, un case sigue al siguiente si falta `break`. Clave: fuente de bugs.
- **default** — rama que se ejecuta si ningún case coincide. Clave: cubre lo inesperado.

## Forma neutral

```text
LEER d
SEGUN d: 1..7 -> nombre ; otro -> invalido
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
