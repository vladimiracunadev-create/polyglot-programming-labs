# Concepto — Concurrente: hilos, tareas y canales

Conocimiento independiente del lenguaje.

Asomarse al paradigma **concurrente**: hacer varias cosas a la vez con hilos, tareas o canales. Sumar una lista puede repartirse entre trabajadores; el resultado combinado es la suma total.

## Definiciones

- **Concurrencia** — estructurar el programa como tareas que progresan a la vez. Clave: aprovecha varios núcleos.
- **Hilo/goroutine** — unidad de ejecución concurrente. Clave: comparte o no memoria según el modelo.
- **Combinar** — reunir los resultados parciales en el final. Clave: la suma total.

## Forma neutral

```text
dividir lista ; sumar cada parte (concurrente) ; combinar sumas
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
