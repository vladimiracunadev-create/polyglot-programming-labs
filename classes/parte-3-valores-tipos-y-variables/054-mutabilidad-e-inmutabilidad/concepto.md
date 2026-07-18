# Concepto — Mutabilidad e inmutabilidad

Conocimiento independiente del lenguaje.

Ver la diferencia entre construir un resultado **mutando** un acumulador (StringBuilder, lista que crece) y hacerlo de forma **inmutable**. Construir una secuencia numérica muestra el patrón acumulador en cada lenguaje.

## Definiciones

- **Mutabilidad** — capacidad de cambiar un valor in situ. Clave: eficiente para construir por partes.
- **Inmutabilidad** — el valor no cambia; toda 'modificación' crea uno nuevo. Clave: más seguro, a veces más caro.
- **Acumulador** — variable que reúne el resultado a lo largo de un bucle. Clave: patrón universal.
- **Builder** — estructura mutable para construir cadenas/colecciones (StringBuilder). Clave: evita recrear en cada paso.

## Forma neutral

```text
LEER n
acc <- vacío
PARA i de 1 a n: añadir i a acc
ESCRIBIR "sec=" UNIR(acc, "-")
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
