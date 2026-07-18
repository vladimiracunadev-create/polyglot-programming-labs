# Concepto — Registro (logging) y observabilidad

Conocimiento independiente del lenguaje.

Practicar el **registro (logging) y la observabilidad**: dejar rastros de lo que hace el programa para poder diagnosticarlo en producción, donde no hay depurador. Un log con nivel y datos es la unidad básica.

## Definiciones

- **Log** — mensaje que registra un evento del programa. Clave: diagnóstico en producción.
- **Nivel de log** — gravedad del mensaje (DEBUG, INFO, WARN, ERROR). Clave: filtrar el ruido.
- **Observabilidad** — capacidad de entender el estado interno desde las salidas (logs, métricas, trazas). Clave: operar en producción.

## Forma neutral

```text
LEER n ; ESCRIBIR log de nivel INFO con procesados=n
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
