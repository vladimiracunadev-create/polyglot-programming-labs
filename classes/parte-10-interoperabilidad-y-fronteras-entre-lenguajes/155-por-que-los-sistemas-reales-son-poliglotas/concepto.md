# Concepto — Por qué los sistemas reales son políglotas

Conocimiento independiente del lenguaje.

Entender **por qué los sistemas reales son políglotas**: cada componente usa el lenguaje que mejor le sirve. Contar los componentes es la medida básica de un sistema hecho de piezas heterogéneas.

## Definiciones

- **Sistema políglota** — software compuesto por partes en distintos lenguajes. Clave: es lo normal en producción.
- **Componente** — pieza con una responsabilidad y su propio lenguaje. Clave: se integra con las demás.
- **Frontera** — el punto donde dos componentes se comunican. Clave: necesita un contrato claro.

## Forma neutral

```text
LEER componentes ; ESCRIBIR cantidad
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
