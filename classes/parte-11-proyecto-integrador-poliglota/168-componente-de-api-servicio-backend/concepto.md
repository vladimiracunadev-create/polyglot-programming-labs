# Concepto — Componente de API/servicio (backend)

Conocimiento independiente del lenguaje.

Construir el **componente de API/servicio** (backend): recibe una petición y devuelve una respuesta con un código de estado y datos. Aquí responde 200 (OK) con el dato recibido.

## Definiciones

- **Componente de API** — servicio que atiende peticiones y devuelve respuestas. Clave: la lógica del sistema.
- **Código de estado** — número que indica el resultado (200 OK, 404 no encontrado). Clave: comunica el desenlace.
- **Respuesta** — estado más datos que el servicio devuelve. Clave: lo que consume el cliente.

## Forma neutral

```text
LEER n ; ESCRIBIR estado 200 y datos=n
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
