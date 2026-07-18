# Concepto — JSON: serialización y deserialización

Conocimiento independiente del lenguaje.

Trabajar con **JSON**: el formato universal de intercambio de datos. Aquí se **serializa** (construye) un objeto JSON con un formato fijo; en la práctica también se deserializa (parsea).

## Definiciones

- **JSON** — formato de texto para datos estructurados (objetos, arreglos). Clave: universal entre lenguajes.
- **Serializar** — convertir datos en su representación de texto (JSON). Clave: para enviarlos o guardarlos.
- **Deserializar** — reconstruir datos desde el texto JSON. Clave: la operación inversa.

## Forma neutral

```text
LEER nombre, edad ; construir objeto ; serializar a JSON
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
