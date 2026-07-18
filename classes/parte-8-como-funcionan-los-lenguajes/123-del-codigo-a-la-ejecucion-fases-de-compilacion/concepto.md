# Concepto — Del código a la ejecución: fases de compilación

Conocimiento independiente del lenguaje.

Ver las **fases de compilación** en miniatura: separar la entrada en tokens (léxico), reconocer su estructura (sintáctico) y calcular el resultado (evaluación). Todo compilador o intérprete hace esto a mayor escala.

## Definiciones

- **Análisis léxico (lexer)** — divide el texto en tokens. Clave: '3 + 4' → [3, +, 4].
- **Análisis sintáctico (parser)** — reconoce la estructura de los tokens. Clave: expresión = número op número.
- **Evaluación** — calcula el resultado a partir de la estructura. Clave: aplica el operador.

## Forma neutral

```text
TOKENIZAR ; RECONOCER (num op num) ; EVALUAR
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
