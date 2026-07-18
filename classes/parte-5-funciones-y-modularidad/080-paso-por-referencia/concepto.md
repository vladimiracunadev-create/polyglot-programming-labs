# Concepto — Paso por referencia

Conocimiento independiente del lenguaje.

Comprender el **paso por referencia**: la función recibe un enlace a la variable original, así que modificar el parámetro **sí** cambia la variable de quien llama. C usa punteros, Go `*`, Rust `&mut`, C# `ref`.

## Definiciones

- **Paso por referencia** — la función accede a la variable original. Clave: puede modificarla.
- **Puntero** — valor que guarda la dirección de otra variable (C). Clave: permite modificarla.
- **Referencia mutable** — enlace que permite cambiar el valor (`&mut` en Rust, `ref` en C#). Clave: modificación explícita.
- **Efecto secundario** — cambiar algo fuera de la función. Clave: potente pero peligroso.

## Forma neutral

```text
LEER n ; antes <- n
doblar(referencia a n)   // modifica el original
ESCRIBIR "antes=" antes " despues=" n
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
