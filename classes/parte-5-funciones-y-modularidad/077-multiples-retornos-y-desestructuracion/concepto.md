# Concepto — Múltiples retornos y desestructuración

Conocimiento independiente del lenguaje.

Devolver **más de un valor** de una función y **desestructurarlos** al recibirlos. Go y Python lo hacen nativamente; otros usan tuplas, arreglos u objetos.

## Definiciones

- **Múltiple retorno** — una función devuelve varios valores. Clave: nativo en Go, Python, Rust.
- **Tupla** — grupo ordenado de valores. Clave: el vehículo habitual del multi-retorno.
- **Desestructuración** — repartir una tupla/objeto en variables. Clave: `q, r = divmod(a, b)`.
- **Struct/objeto de salida** — en Java/C se devuelve un objeto con campos. Clave: alternativa al multi-retorno.

## Forma neutral

```text
FUNCION divmod(a,b): DEVOLVER (a/b, a%b)
LEER a,b ; (q,r) <- divmod(a,b) ; ESCRIBIR q, r
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
