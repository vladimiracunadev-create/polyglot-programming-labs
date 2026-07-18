# Concepto — Pruebas end-to-end del sistema completo

Conocimiento independiente del lenguaje.

Realizar una **prueba end-to-end (e2e)**: ejercitar el sistema completo, de la entrada a la salida, como lo haría un usuario real. Aquí se comprueba que, dadas dos entradas, el sistema devuelve el total esperado.

## Definiciones

- **Prueba end-to-end** — verifica el sistema completo desde la perspectiva del usuario. Clave: cubre todos los componentes juntos.
- **Flujo** — el recorrido de una acción a través del sistema. Clave: lo que se ejercita en e2e.
- **Pirámide de pruebas** — muchas unitarias, algunas de integración, pocas e2e. Clave: equilibrio coste/valor.

## Forma neutral

```text
LEER a, b, esperado ; SI a+b == esperado: pasa SINO falla
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
