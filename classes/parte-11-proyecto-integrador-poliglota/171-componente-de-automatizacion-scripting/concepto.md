# Concepto — Componente de automatización/scripting

Conocimiento independiente del lenguaje.

Construir el **componente de automatización/scripting**: tareas repetitivas que se ejecutan sin intervención (limpieza, despliegue, informes). Aquí se procesan n tareas y se confirma su finalización.

## Definiciones

- **Automatización** — ejecutar tareas repetitivas sin intervención humana. Clave: fiabilidad y ahorro de tiempo.
- **Script** — programa que orquesta o automatiza pasos. Clave: pegamento del sistema.
- **Lote** — conjunto de tareas procesadas juntas. Clave: eficiencia.

## Forma neutral

```text
LEER n ; procesar n tareas ; ESCRIBIR completado
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
