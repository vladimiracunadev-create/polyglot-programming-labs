# Concepto — Visibilidad, encapsulación y contratos (public/private)

Conocimiento independiente del lenguaje.

Aplicar **encapsulación**: ocultar el estado interno (el saldo) y exponer solo operaciones controladas (depositar, consultar). El contrato público protege los datos de modificaciones inválidas.

## Definiciones

- **Encapsulación** — agrupar datos y operaciones ocultando el estado interno. Clave: se accede solo por métodos.
- **Privado** — accesible solo desde dentro del tipo. Clave: protege el estado.
- **Público** — parte visible desde fuera (el contrato). Clave: lo que otros usan.
- **Invariante** — regla que el objeto siempre cumple (saldo >= 0). Clave: la encapsulación la protege.

## Forma neutral

```text
LEER n
cuenta <- nueva Cuenta()
cuenta.depositar(n) ; cuenta.depositar(n)
ESCRIBIR "saldo=" cuenta.saldo()
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
