# Concepto — Serialización entre lenguajes: JSON, Protobuf, MessagePack

Conocimiento independiente del lenguaje.

Entender la **serialización entre lenguajes** (JSON, Protobuf, MessagePack): convertir datos a un formato común para que un componente en un lenguaje los envíe y otro en otro lenguaje los reciba. Aquí se serializa un par a texto.

## Definiciones

- **Serialización** — convertir datos en un formato transmisible (texto o binario). Clave: cruzar la frontera de lenguaje.
- **Formato de intercambio** — representación común (JSON, Protobuf). Clave: independiente del lenguaje.
- **Esquema** — estructura acordada de los datos. Clave: emisor y receptor lo comparten.

## Forma neutral

```text
LEER clave, valor ; ESCRIBIR clave:valor
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
