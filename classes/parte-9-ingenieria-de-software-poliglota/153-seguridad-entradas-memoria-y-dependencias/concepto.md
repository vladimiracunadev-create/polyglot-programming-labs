# Concepto — Seguridad: entradas, memoria y dependencias

Conocimiento independiente del lenguaje.

Introducir la **seguridad**: validar y sanear las entradas para evitar inyecciones y datos maliciosos. Comprobar que una entrada es alfanumérica es una validación básica que cierra muchos ataques.

## Definiciones

- **Validación de entrada** — comprobar que los datos cumplen lo esperado antes de usarlos. Clave: primera defensa.
- **Saneamiento** — eliminar o escapar caracteres peligrosos. Clave: evita inyecciones.
- **Inyección** — datos maliciosos que el programa interpreta como comando (SQL, shell). Clave: causa frecuente de brechas.

## Forma neutral

```text
LEER entrada ; seguro <- todos los caracteres alfanuméricos
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
