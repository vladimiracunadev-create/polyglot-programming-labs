# Concepto — Enlaces (bindings) y wrappers

Conocimiento independiente del lenguaje.

Entender los **enlaces (bindings) y wrappers**: una capa que adapta una librería nativa a un uso cómodo e idiomático en tu lenguaje. El wrapper traduce entre la frontera y tu código.

## Definiciones

- **Binding** — capa que expone una librería de otro lenguaje en el tuyo. Clave: reutilizar sin reescribir.
- **Wrapper** — función que envuelve otra, adaptando su interfaz. Clave: uso más cómodo o seguro.
- **Adaptación** — traducir tipos y convenciones entre la librería nativa y tu código. Clave: ocultar la frontera.

## Forma neutral

```text
r <- doble(n) ; ESCRIBIR 'wrap(' + r + ')'
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
