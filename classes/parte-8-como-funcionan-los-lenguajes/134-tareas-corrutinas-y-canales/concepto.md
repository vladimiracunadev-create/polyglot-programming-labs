# Concepto — Tareas, corrutinas y canales

Conocimiento independiente del lenguaje.

Introducir **tareas, corrutinas y canales**: en vez de compartir memoria, las tareas se comunican enviando datos por canales. Un productor envía los valores y un consumidor calcula el máximo.

## Definiciones

- **Canal** — conducto para enviar datos entre tareas concurrentes. Clave: comunicar sin compartir memoria.
- **Corrutina/goroutine** — tarea ligera que el runtime planifica. Clave: miles a bajo coste (Go).
- **Productor/consumidor** — un patrón: una tarea produce datos, otra los consume. Clave: se coordinan por el canal.

## Forma neutral

```text
productor envía cada valor ; consumidor actualiza el máximo
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
