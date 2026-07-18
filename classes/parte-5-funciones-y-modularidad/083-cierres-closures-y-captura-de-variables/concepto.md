# Concepto — Cierres (closures) y captura de variables

Conocimiento independiente del lenguaje.

Entender los **cierres (closures)**: funciones que capturan y recuerdan variables de su entorno. Un `sumador(base)` devuelve una función que suma `base` a lo que reciba, recordándolo entre llamadas.

## Definiciones

- **Cierre** — función que captura variables de su entorno de definición. Clave: las recuerda al ejecutarse después.
- **Captura** — recordar una variable externa dentro del cierre. Clave: por valor o por referencia.
- **Función de orden superior** — la que devuelve o recibe funciones. Clave: fábrica de cierres.
- **Estado capturado** — el valor que el cierre conserva. Clave: como una variable privada.

## Forma neutral

```text
LEER base
sumar <- hacer_sumador(base)   // captura base
ESCRIBIR "r1=" sumar(1) " r2=" sumar(2)
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
