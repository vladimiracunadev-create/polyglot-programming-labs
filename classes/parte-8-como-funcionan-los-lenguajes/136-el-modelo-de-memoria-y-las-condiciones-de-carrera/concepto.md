# Concepto — El modelo de memoria y las condiciones de carrera

Conocimiento independiente del lenguaje.

Entender el **modelo de memoria y las condiciones de carrera**: cuando dos hilos actualizan el mismo dato sin coordinación, el resultado puede corromperse. Incrementar de forma segura garantiza el valor correcto.

## Definiciones

- **Condición de carrera** — el resultado depende del orden imprevisible de dos accesos concurrentes. Clave: corrompe datos.
- **Sección crítica** — código que accede a un recurso compartido y debe ejecutarse en exclusión. Clave: se protege con un lock.
- **Operación atómica** — indivisible: ocurre entera o nada. Clave: evita la carrera en incrementos.

## Forma neutral

```text
cuenta <- 0 ; REPETIR n veces (protegido): cuenta <- cuenta + 1
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
