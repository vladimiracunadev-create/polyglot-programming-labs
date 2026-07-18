# Concepto — Concurrencia: procesos, hilos y memoria compartida

Conocimiento independiente del lenguaje.

Introducir la **concurrencia con memoria compartida**: varios hilos acceden a los mismos datos. Contar con un acumulador compartido ilustra el modelo; en concurrencia real, ese acceso debe protegerse.

## Definiciones

- **Proceso** — programa en ejecución con su propia memoria aislada. Clave: no comparte por defecto.
- **Hilo** — línea de ejecución dentro de un proceso; comparte su memoria. Clave: acceso concurrente a los datos.
- **Memoria compartida** — datos accesibles por varios hilos. Clave: requiere sincronización para ser segura.

## Forma neutral

```text
cuenta <- 0 ; PARA CADA elemento: cuenta <- cuenta + 1
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
