# Concepto — Componente CLI (lenguaje de sistemas)

Conocimiento independiente del lenguaje.

Construir el **componente CLI** del sistema (idóneo para un lenguaje de sistemas): una interfaz de línea de comandos que recibe un comando y argumentos. Aquí se parsea el comando y se cuentan sus argumentos.

## Definiciones

- **Componente CLI** — interfaz por terminal del sistema. Clave: automatizable y componible.
- **Comando** — la acción a ejecutar (el primer token). Clave: selecciona qué hacer.
- **Argumento** — dato que modifica la acción. Clave: se cuentan tras el comando.

## Forma neutral

```text
LEER tokens ; comando <- tokens[0] ; args <- tokens - 1
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
