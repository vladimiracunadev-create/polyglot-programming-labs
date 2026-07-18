# Concepto — Iteración por condición: while y do-while

Conocimiento independiente del lenguaje.

Usar el bucle `while`: repetir mientras una condición sea verdadera. Es el bucle más básico y el que subyace a todos los demás.

## Definiciones

- **while** — bucle que repite mientras la condición sea verdadera. Clave: comprueba antes de cada vuelta.
- **do-while** — variante que ejecuta al menos una vez (comprueba al final). Clave: no en todos los lenguajes.
- **Condición de parada** — lo que hace terminar el bucle. Clave: algo debe acercarse a ella.
- **Acumulador** — variable que reúne el resultado. Clave: se actualiza cada vuelta.

## Forma neutral

```text
LEER n
suma <- 0 ; i <- 1
MIENTRAS i <= n: suma <- suma+i ; i <- i+1
ESCRIBIR "suma=" suma
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
