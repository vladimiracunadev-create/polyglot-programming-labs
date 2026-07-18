# Concepto — AOT vs. JIT: costos y beneficios

Conocimiento independiente del lenguaje.

Comparar **AOT (compilación anticipada)** con **JIT (compilación en tiempo de ejecución)**. AOT compila todo antes de arrancar (rápido al iniciar); JIT compila sobre la marcha las partes calientes (arranque más lento, luego rápido).

## Definiciones

- **AOT** — compilación anticipada a código máquina (C, Rust, Go). Clave: arranque instantáneo.
- **JIT** — compilación durante la ejecución de lo más usado (JVM, V8). Clave: se calienta y acelera.
- **Código caliente** — el que se ejecuta muchas veces. Clave: el JIT lo optimiza.

## Forma neutral

```text
multiplicar 2 por sí mismo n veces (o desplazar bits)
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
