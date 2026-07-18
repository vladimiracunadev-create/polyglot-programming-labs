# Concepto — Módulos, paquetes y espacios de nombres

Conocimiento independiente del lenguaje.

Organizar el código en **módulos** (o paquetes/espacios de nombres): agrupar funciones relacionadas y usarlas con un prefijo o importándolas. Es lo que evita que un proyecto grande sea un solo archivo caótico.

## Definiciones

- **Módulo** — unidad que agrupa funciones/tipos relacionados. Clave: organización y reutilización.
- **Espacio de nombres** — prefijo que evita colisiones de nombres. Clave: `math.sqrt` vs. `otro.sqrt`.
- **Importar** — traer un módulo al alcance actual (import/require/use). Clave: acceder a su contenido.
- **Encapsulación de módulo** — exponer solo lo público. Clave: oculta detalles internos.

## Forma neutral

```text
IMPORTAR modulo
LEER n ; ESCRIBIR "resultado=" modulo.doble(n)
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
