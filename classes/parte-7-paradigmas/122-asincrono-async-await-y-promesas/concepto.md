# Concepto — Asíncrono: async/await y promesas

Conocimiento independiente del lenguaje.

Asomarse al paradigma **asíncrono**: iniciar una operación que tardará y continuar sin bloquear, esperando su resultado con `async/await`. Aquí una tarea calcula el doble y se espera su valor.

## Definiciones

- **Asíncrono** — iniciar algo que tarda y seguir sin bloquear. Clave: eficiente para I/O.
- **async/await** — sintaxis para escribir código asíncrono como si fuera secuencial. Clave: legible.
- **Promesa/Future/Task** — objeto que representa un resultado futuro. Clave: se espera con await.

## Forma neutral

```text
async doble(x): DEVOLVER 2x ; resultado <- await doble(n)
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
