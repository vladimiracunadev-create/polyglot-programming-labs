# Concepto — Tipado estático vs. dinámico

Conocimiento independiente del lenguaje.

Ver la diferencia entre **tipado estático** (el tipo se fija y comprueba al compilar) y **dinámico** (se resuelve al ejecutar). Sumar un entero con un real obliga, en los estáticos, a una conversión explícita que en los dinámicos ocurre sola.

## Definiciones

- **Tipado estático** — los tipos se fijan y comprueban en compilación (Java, C#, Go, Rust, C). Clave: errores antes de ejecutar.
- **Tipado dinámico** — los tipos se resuelven en ejecución (Python, PHP, JS). Clave: flexible, errores más tarde.
- **Promoción** — convertir un entero a real para operar con otro real. Clave: en estáticos suele ser explícita.
- **Comprobación de tipos** — verificar que las operaciones son válidas para los tipos. Clave: estática o dinámica.

## Forma neutral

```text
LEER a (entero), b (real)
ESCRIBIR "suma=" FORMATEAR(a+b, 2)
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
