# Concepto — Mantenibilidad, documentación y deuda técnica

Conocimiento independiente del lenguaje.

Cerrar la parte con la **mantenibilidad, la documentación y la deuda técnica**: medir la complejidad ayuda a mantener el código sano. Contar los módulos es una métrica básica; la deuda técnica crece cuando se ignora.

## Definiciones

- **Mantenibilidad** — facilidad con que el código se entiende y modifica. Clave: reduce el coste futuro.
- **Deuda técnica** — coste acumulado de decisiones rápidas que habrá que pagar. Clave: crece si se ignora.
- **Documentación** — explicar el porqué del código. Clave: baja la barrera para mantenerlo.

## Forma neutral

```text
LEER módulos ; ESCRIBIR cantidad
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
