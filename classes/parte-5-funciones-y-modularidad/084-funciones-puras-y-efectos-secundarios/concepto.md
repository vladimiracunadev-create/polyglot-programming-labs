# Concepto — Funciones puras y efectos secundarios

Conocimiento independiente del lenguaje.

Distinguir una **función pura** —su resultado depende solo de sus argumentos y no cambia nada externo— de una con **efectos secundarios**. Las puras son predecibles, testeables y seguras de paralelizar.

## Definiciones

- **Función pura** — su salida depende solo de sus entradas y no causa efectos externos. Clave: predecible.
- **Efecto secundario** — modificar estado externo, imprimir, leer archivos. Clave: rompe la pureza.
- **Transparencia referencial** — poder reemplazar la llamada por su resultado. Clave: propiedad de las puras.
- **Determinismo** — misma entrada, misma salida siempre. Clave: facilita las pruebas.

## Forma neutral

```text
FUNCION cuadrado(n): DEVOLVER n*n   // sin tocar nada externo
LEER n ; ESCRIBIR "puro=" cuadrado(n)
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
