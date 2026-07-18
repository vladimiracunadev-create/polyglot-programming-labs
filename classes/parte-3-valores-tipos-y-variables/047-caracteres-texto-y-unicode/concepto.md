# Concepto — Caracteres, texto y Unicode

Conocimiento independiente del lenguaje.

Entender que un **carácter** es, por dentro, un número: su punto de código. Verás cómo cada lenguaje lee un carácter y obtiene su código, y por qué el texto es, en el fondo, una secuencia de números.

## Definiciones

- **Carácter** — símbolo textual (letra, dígito, signo). Clave: internamente es un número.
- **Punto de código** — número que identifica un carácter en Unicode/ASCII. Clave: 'A' es 65.
- **ASCII** — codificación de 0-127 para el inglés básico. Clave: subconjunto de Unicode.
- **Unicode** — estándar que asigna un código a cada carácter de todo idioma. Clave: el texto moderno.

## Forma neutral

```text
LEER c
ESCRIBIR "char=" c " codigo=" CODIGO(c)
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
