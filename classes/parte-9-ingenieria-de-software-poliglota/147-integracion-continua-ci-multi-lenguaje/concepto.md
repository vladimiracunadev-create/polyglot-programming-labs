# Concepto — Integración continua (CI) multi-lenguaje

Conocimiento independiente del lenguaje.

Entender la **integración continua (CI)**: cada cambio dispara un pipeline de pasos (compilar, probar, lint); si todos pasan, el resultado es 'verde'. Si uno falla, es 'rojo' y el cambio se bloquea.

## Definiciones

- **Integración continua** — ejecutar automáticamente pruebas y checks en cada cambio. Clave: detecta errores pronto.
- **Pipeline** — secuencia de pasos (build, test, lint). Clave: todos deben pasar.
- **Verde/rojo** — estado del pipeline: todo pasa (verde) o algo falla (rojo). Clave: bloquea lo roto.

## Forma neutral

```text
LEER pasos ; verde <- todos == 1
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
