# Concepto — Orientado a objetos: clases, objetos y estado

Conocimiento independiente del lenguaje.

Practicar el paradigma **orientado a objetos**: agrupar estado (datos) y comportamiento (métodos) en objetos. Un contador con su método `incrementar` es el ejemplo mínimo de estado encapsulado.

## Definiciones

- **Objeto** — instancia que agrupa estado y comportamiento. Clave: datos + métodos juntos.
- **Clase** — molde que define objetos. Clave: describe estado y métodos.
- **Método** — función asociada a un objeto que opera sobre su estado. Clave: `contador.incrementar()`.

## Forma neutral

```text
c <- Contador() ; REPETIR n veces: c.incrementar() ; ESCRIBIR c.cuenta
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
