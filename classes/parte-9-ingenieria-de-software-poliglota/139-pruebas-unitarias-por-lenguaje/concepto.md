# Concepto — Pruebas unitarias por lenguaje

Conocimiento independiente del lenguaje.

Escribir una **prueba unitaria**: código que comprueba automáticamente que otro código produce el resultado esperado. Es la base de la calidad y el corazón del verificador de este curso.

## Definiciones

- **Prueba unitaria** — código que verifica una unidad (función) de forma automática. Clave: repetible.
- **Aserción** — comprobación de que un valor es el esperado. Clave: si falla, la prueba se pone en rojo.
- **Runner** — herramienta que ejecuta las pruebas (pytest, cargo test). Clave: un comando corre todas.

## Forma neutral

```text
LEER a, b, esperado ; SI a+b == esperado: pasa SINO falla
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
