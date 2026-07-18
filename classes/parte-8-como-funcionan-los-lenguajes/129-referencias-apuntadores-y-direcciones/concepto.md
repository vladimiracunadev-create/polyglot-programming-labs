# Concepto — Referencias, apuntadores y direcciones

Conocimiento independiente del lenguaje.

Entender **referencias, apuntadores y direcciones**: acceder a un dato a través de su posición o dirección, no directamente. Indexar una lista es aritmética de direcciones: base + índice.

## Definiciones

- **Referencia** — un valor que designa a otro dato. Clave: acceso indirecto.
- **Puntero** — referencia explícita que guarda una dirección (C). Clave: `arr + i` = dirección del elemento i.
- **Índice** — posición dentro de una secuencia. Clave: equivale a un desplazamiento desde la base.

## Forma neutral

```text
LEER indice y lista ; ESCRIBIR lista[indice]
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
