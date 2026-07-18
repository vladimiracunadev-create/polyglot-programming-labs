# Concepto — WebAssembly como objetivo común

Conocimiento independiente del lenguaje.

Entender **WebAssembly (Wasm)** como objetivo común: un formato binario portable al que compilan muchos lenguajes (Rust, C, Go) y que corre en el navegador o en runtimes. Es un 'punto de encuentro' entre lenguajes.

## Definiciones

- **WebAssembly** — formato binario portable y eficiente, objetivo de compilación de varios lenguajes. Clave: corre en el navegador y en runtimes.
- **Objetivo (target)** — el formato al que compila un lenguaje. Clave: Rust, C, Go pueden apuntar a Wasm.
- **WASI** — interfaz de sistema para Wasm fuera del navegador. Clave: Wasm del lado servidor.

## Forma neutral

```text
LEER n ; ESCRIBIR n*n
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
