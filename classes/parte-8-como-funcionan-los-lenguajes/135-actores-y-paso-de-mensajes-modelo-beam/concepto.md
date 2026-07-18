# Concepto — Actores y paso de mensajes (modelo BEAM)

Conocimiento independiente del lenguaje.

Introducir el **modelo de actores y el paso de mensajes** (la máquina BEAM de Erlang/Elixir): actores aislados sin memoria compartida que se comunican por mensajes. Un actor acumula la suma recibiendo un mensaje por número.

## Definiciones

- **Actor** — unidad concurrente con estado propio que solo se comunica por mensajes. Clave: aislamiento.
- **Paso de mensajes** — enviar datos a un actor en vez de compartir memoria. Clave: sin carreras.
- **BEAM** — la máquina virtual de Erlang/Elixir, optimizada para millones de actores. Clave: tolerancia a fallos.

## Forma neutral

```text
PARA CADA número: enviar mensaje al actor ; el actor suma a su estado
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
