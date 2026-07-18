# Concepto — Firma, parámetros, argumentos y retorno

Conocimiento independiente del lenguaje.

Entender la anatomía de una función: **firma** (nombre + parámetros + tipo de retorno), **argumentos** (los valores que se pasan) y **retorno** (el valor que devuelve). Es la unidad de reutilización de todo programa.

## Definiciones

- **Función** — bloque con nombre que recibe parámetros y devuelve un valor. Clave: la unidad de reutilización.
- **Firma** — nombre + parámetros + tipo de retorno. Clave: define cómo se usa.
- **Parámetro** — variable del hueco en la definición. Clave: recibe el argumento.
- **Argumento** — valor concreto que se pasa al llamar. Clave: llena el parámetro.

## Forma neutral

```text
FUNCION suma(a, b): DEVOLVER a+b
LEER a, b ; ESCRIBIR "suma=" suma(a,b)
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
