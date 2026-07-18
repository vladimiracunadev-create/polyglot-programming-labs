# Concepto — Procesos y comunicación: stdin/stdout, sockets, colas

Conocimiento independiente del lenguaje.

Entender la **comunicación entre procesos**: procesos separados intercambian datos por tuberías (stdin/stdout), sockets o colas. Una cola FIFO entrega los datos en orden a un consumidor que los suma.

## Definiciones

- **Comunicación entre procesos (IPC)** — mecanismos para que procesos separados intercambien datos. Clave: tuberías, sockets, colas.
- **Tubería** — conecta la salida de un proceso con la entrada de otro. Clave: base de los comandos Unix encadenados.
- **Cola** — buffer FIFO que desacopla productor y consumidor. Clave: comunicación asíncrona.

## Forma neutral

```text
PARA CADA mensaje de la cola: acumular ; ESCRIBIR suma
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
