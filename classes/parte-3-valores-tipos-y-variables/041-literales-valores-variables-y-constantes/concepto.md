# Concepto — Literales, valores, variables y constantes

Conocimiento independiente del lenguaje.

Un **programa manipula valores**. Un *valor* es un dato concreto (el número `27000.0`, el texto
`"Total"`). Cuando ese valor se escribe directamente en el código se llama **literal**. Para
reutilizar o transformar un valor le damos un **nombre**: si ese nombre puede volver a apuntar a
otro valor es una **variable**; si no debe cambiar, es una **constante**.

Tres decisiones distinguen a los lenguajes:

1. **¿Hay que declarar el tipo?** Los estáticos (Java, C#, Go, Rust, C) sí; los dinámicos
   (Python, JS, PHP) lo infieren en ejecución. TypeScript infiere pero comprueba al compilar.
2. **¿Es mutable por defecto?** Rust dice *no* (`let` es inmutable, hace falta `let mut`). Casi
   todos los demás dicen *sí*. Una constante explícita (`const`, `final`, `CONST`) invierte esa
   decisión localmente.
3. **¿Existe siquiera la "variable que cambia"?** En los lenguajes declarativos (SQL) y
   funcionales puros (Haskell) no se asignan variables: se *definen* nombres para valores.

La forma neutral del cálculo de esta clase:

```text
total = precio_unitario * cantidad * (1 - descuento)
```

no depende de ninguna sintaxis. Lo que cambia entre lenguajes es cómo se nombran los valores,
si se anota su tipo y cómo se formatea el resultado.
