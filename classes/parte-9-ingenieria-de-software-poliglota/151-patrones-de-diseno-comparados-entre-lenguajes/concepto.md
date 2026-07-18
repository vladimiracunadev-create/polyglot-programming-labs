# Concepto — Patrones de diseño comparados entre lenguajes

Conocimiento independiente del lenguaje.

Practicar los **patrones de diseño comparados**: el patrón **Estrategia** encapsula algoritmos intercambiables tras una interfaz común. Elegir la operación por su nombre selecciona la estrategia a aplicar.

## Definiciones

- **Patrón de diseño** — solución probada y reutilizable a un problema de diseño recurrente. Clave: vocabulario común.
- **Estrategia** — patrón que encapsula algoritmos intercambiables tras una interfaz. Clave: cambiar el comportamiento sin condicionales dispersos.
- **Despacho** — seleccionar qué código ejecutar según un valor. Clave: aquí, por el nombre de la operación.

## Forma neutral

```text
LEER estrategia, a, b ; seleccionar operación ; aplicar
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
