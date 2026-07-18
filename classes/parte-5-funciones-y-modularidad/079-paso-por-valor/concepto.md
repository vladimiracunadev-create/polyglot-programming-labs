# Concepto — Paso por valor

Conocimiento independiente del lenguaje.

Comprender el **paso por valor**: la función recibe una copia del argumento, así que modificar el parámetro dentro no afecta a la variable original de quien llama.

## Definiciones

- **Paso por valor** — la función recibe una copia del argumento. Clave: el original no cambia.
- **Copia** — un duplicado independiente del valor. Clave: vive dentro de la función.
- **Parámetro local** — la variable de la función que contiene la copia. Clave: aislada del exterior.
- **Efecto en el llamador** — aquí, ninguno. Clave: la seguridad del paso por valor.

## Forma neutral

```text
LEER n
local <- doblar(n)   // dentro trabaja una copia
ESCRIBIR "original=" n " local=" local
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
