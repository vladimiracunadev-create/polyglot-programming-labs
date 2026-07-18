# Concepto — Contratos de API: REST, gRPC y esquemas

Conocimiento independiente del lenguaje.

Entender los **contratos de API (REST, gRPC)**: la frontera entre servicios se define con un contrato (qué operaciones, qué datos). Un endpoint REST combina un método (GET, POST) con un recurso (/users).

## Definiciones

- **Contrato de API** — acuerdo de qué operaciones y datos expone un servicio. Clave: frontera estable entre componentes.
- **REST** — estilo basado en recursos y métodos HTTP (GET, POST, PUT). Clave: simple y universal.
- **gRPC** — framework de RPC con contratos definidos en Protobuf. Clave: eficiente y tipado.

## Forma neutral

```text
LEER metodo, recurso ; ESCRIBIR metodo + ' /' + recurso
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
