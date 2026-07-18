# Concepto — Tipos primitivos: enteros, reales, booleanos, caracteres

Conocimiento independiente del lenguaje.

Ver los tipos primitivos en acción: el mismo número tratado como **entero**, convertido a **real** y evaluado como **booleano**. Cada lenguaje formatea y convierte de forma propia, pero el concepto de 'tipo primitivo' es universal.

## Definiciones

- **Tipo primitivo** — tipo básico incorporado al lenguaje (entero, real, booleano, carácter). Clave: bloque elemental de todo dato.
- **Entero** — número sin decimales, de tamaño fijo en los estáticos. Clave: aritmética exacta.
- **Real** — número en coma flotante. Clave: aproximado; se formatea con un número de decimales.
- **Booleano** — valor de verdad (verdadero/falso). Clave: gobierna las decisiones del programa.

## Forma neutral

```text
LEER n
real <- CONVERTIR_A_REAL(n)
par <- (n MOD 2 == 0)
ESCRIBIR "entero=" n " real=" FORMATEAR(real,1) " par=" par
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
