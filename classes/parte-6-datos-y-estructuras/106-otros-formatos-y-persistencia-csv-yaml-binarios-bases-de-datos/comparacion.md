# Comparación — Otros formatos y persistencia: CSV, YAML, binarios, bases de datos

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | `','.join(...)` (Python), `.join(',')` (JS), bucle (C). |
| Semántica | CSV real necesita escapar comas y comillas; aquí los datos son simples. |
| Paradigmática | SQL exporta/importa CSV con comandos del motor. |

## El concepto en la familia

En Ruby `arr.join(',')`. Casi todos tienen una librería CSV que maneja comillas y saltos correctamente.
