# Clase 008 — Trazado manual y ejecución simbólica

> Parte **0 — Pensamiento computacional y el método políglota** · ⏱️ Duración estimada: **75 min** · Nivel: **Fundamentos**
> ✅ **Clase construida.**

---

## 🎯 Objetivo

Antes de ejecutar un algoritmo en una máquina, puedes ejecutarlo con papel y lápiz: seguir el valor de cada variable, paso a paso, para comprobar que hace lo que crees. A esto se le llama **trazado manual**, y es la habilidad de depuración más fundamental que existe, la que todas las demás presuponen. Su hermana mayor es la **ejecución simbólica**: trazar no con números concretos, sino con símbolos, para cubrir muchos casos a la vez. El objetivo de hoy es que puedas "correr" un algoritmo en tu cabeza y en una tabla, detectar un error de lógica sin ejecutar nada, y predecir la salida de un fragmento con solo leerlo.

Esta es la cuarta fase de Polya —*looking back*, revisar el resultado— pero llevada al interior del algoritmo: en vez de revisar solo la respuesta final, sigues el estado en cada paso intermedio. Es también lo que un depurador hace por ti; la diferencia es que si no sabes trazar a mano, tampoco entiendes lo que el depurador te muestra. El trazado es el músculo; el depurador es solo una máquina que lo ejercita más rápido.

## 🧩 Situación

Escribes un bucle que debería sumar `1 + 2 + 3` y dar `6`, pero devuelve `3`. La reacción instintiva —y perdedora— es cambiar cosas al azar: mueves una línea, pruebas, mueves otra, pruebas, veinte veces, sin entender nada. La reacción experta es trazar a mano: haces una tabla con las variables y anotas su valor vuelta a vuelta. A la segunda fila descubres el problema: inicializaste `suma <- 0` *dentro* del bucle, así que cada vuelta la reinicias a cero y solo sobrevive el último sumando. El trazado no adivinó la respuesta; te la *mostró*, señalando el paso exacto donde el estado se desvió de lo que esperabas. Cinco minutos de tabla contra media hora de cambios a ciegas: esa es la diferencia que enseña esta clase.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Trazar la ejecución de un algoritmo con una tabla de estado de variables.
2. Detectar un error de lógica sin ejecutar el programa.
3. Predecir la salida de un fragmento leyéndolo.
4. Usar ejecución simbólica para razonar sobre todos los casos, no solo uno concreto.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Tabla de trazado | Registrar el estado de las variables vuelta a vuelta |
| 2 | Ejecución simbólica | Razonar con valores generales, no solo concretos |
| 3 | Trazar para depurar | Encontrar el punto donde el estado se desvía |

## 📖 Definiciones y características

El **trazado** es seguir a mano el valor de cada variable en cada paso de la ejecución. Su producto es una tabla: una columna por variable, una fila por paso o iteración. Lo que revela no es la respuesta final —esa ya la tenías— sino *dónde* la lógica empieza a desviarse de lo que esperabas. Ese punto de divergencia es el bug. Trazar convierte la depuración de un juego de adivinanzas en una búsqueda dirigida: comparas, fila a fila, lo que el algoritmo *hace* con lo que *debería hacer*, y el primer desacuerdo es el culpable.

El concepto central que el trazado hace tangible es el de **estado**: el conjunto de valores de todas las variables en un instante dado. Un programa, visto así, no es más que una máquina que transforma estados: empieza en un estado inicial y cada instrucción lo modifica hasta llegar al estado final. Esta es una de las ideas más profundas de SICP —la de un proceso computacional como una sucesión de estados que evolucionan según reglas fijas— y trazar es, literalmente, escribir esa sucesión. Cuando entiendes que "ejecutar" significa "cambiar el estado paso a paso", el trazado deja de ser una técnica escolar y se revela como la forma directa de ver lo que el programa realmente hace, por debajo de lo que crees que hace.

La **ejecución simbólica** eleva el trazado un nivel: en vez de trazar con un número concreto (`x = 5`), trazas con un símbolo (`x = n`, donde `n` es cualquier valor válido). El resultado es un razonamiento que cubre *todos* los casos de una vez, no solo el que elegiste. Si trazas `mitad <- n / 2` simbólicamente, concluyes algo verdadero para todo `n`, mientras que trazar con `n = 8` solo te dice qué pasa con el 8. Esta es la conexión directa con la corrección de la clase 006: un invariante de bucle es, en el fondo, el resultado de una ejecución simbólica —una afirmación sobre el estado que vale en cada vuelta sin importar los valores concretos—. Trazar con números concretos atrapa bugs; trazar simbólicamente prueba corrección. Hunt y Thomas insisten en que no hay que "adivinar" al depurar, sino razonar sobre lo que el código realmente hace; el trazado, concreto o simbólico, es ese razonamiento hecho visible.

## 🔎 Ejemplo

Tracemos el fragmento `suma <- 0; PARA i EN 1..3: suma <- suma + i` con una tabla de estado:

```text
paso  |  i  |  suma
------|-----|------
inic  |  -  |   0
  1   |  1  |   1      (suma = 0 + 1)
  2   |  2  |   3      (suma = 1 + 2)
  3   |  3  |   6      (suma = 3 + 3)   ⇐ salida: 6
```

La tabla no solo confirma que el resultado es `6`; muestra el *camino*: `0 → 1 → 3 → 6`. Ahora compáralo con la versión con el bug de la situación, donde `suma <- 0` está dentro del bucle: la columna `suma` sería `1`, luego `2` (reiniciada a 0 y sumado 2), luego `3`, y la salida sería `3`. Poniendo las dos tablas lado a lado, el error salta a la vista en la primera fila donde difieren. Eso es depurar por trazado: no adivinas, comparas estados.

## ✍️ Práctica

Traza a mano, con una tabla de estado, el fragmento `x <- 5; MIENTRAS x > 0: ESCRIBIR x; x <- x - 2`. Responde dos preguntas con tu tabla delante: ¿qué imprime exactamente (en qué orden)? y ¿termina o no? Sigue el valor de `x` fila a fila —5, 3, 1, y luego...— y presta atención a la condición `x > 0` justo cuando `x` vale 1: tras restar 2, `x` es −1, la condición se vuelve falsa y el bucle para. Esto conecta con la clase 006: tu tabla es, de hecho, una comprobación de terminación, porque muestras que `x` decrece hacia el límite. Como reto extra, hazlo de nuevo simbólicamente con `x <- k` para un `k` impar cualquiera y describe qué imprime en general.

## ⚠️ Errores comunes

| Síntoma / mensaje | Causa y cómo corregirlo |
|-------------------|--------------------------|
| Depurar cambiando líneas al azar sin entender | No sigues el estado real. Traza a mano hasta ver la fila donde se desvía |
| El depurador te muestra valores que no entiendes | No sabes trazar. Practica el trazado manual: el depurador solo automatiza lo que ya deberías saber hacer |
| Concluyes de un solo caso que "siempre funciona" | Trazaste un valor concreto. Usa ejecución simbólica para cubrir todos los casos |
| No detectas el error aunque lees el código diez veces | Lees, no ejecutas. Fuerza el trazado en una tabla: leer y ejecutar mentalmente son cosas distintas |

## ❓ Preguntas frecuentes

**❓ ¿No es más rápido usar el depurador que trazar a mano?** El depurador traza por ti, sí, y es más rápido para programas largos. Pero si no sabes trazar, no entiendes lo que el depurador muestra: ves valores cambiar sin saber cuál está mal. El trazado manual es la comprensión; el depurador es la velocidad. Necesitas la primera antes de que la segunda te sirva.

**❓ ¿Cuándo debo trazar en lugar de simplemente ejecutar?** Cuando un resultado te sorprende. Si el programa da lo esperado, no hace falta trazar. Pero en el momento en que devuelve algo que no entiendes, ejecutar otra vez no añade información: trazar localiza el paso exacto donde tu modelo mental y la realidad divergen.

**❓ ¿Trazar sirve en cualquier lenguaje?** Sí, y esa es su gracia: el estado y su evolución son conceptos neutrales, igual que el pseudocódigo. Trazas la *lógica*, no la sintaxis. La misma tabla de estado sirve para razonar sobre un bucle en Python, en Go o en C, porque todos comparten la idea de estado que cambia paso a paso.

## 🔗 Referencias

- G. Polya — *How to Solve It* (Princeton University Press), fase "Looking Back".
- H. Abelson y G. J. Sussman — *Structure and Interpretation of Computer Programs* (2ª ed., MIT Press), procesos y estado — [gratis online](https://mitpress.mit.edu/9780262510875/).
- A. Hunt y D. Thomas — *The Pragmatic Programmer* (2ª ed., Addison-Wesley), capítulo sobre depuración.
- T. Cormen, C. Leiserson, R. Rivest y C. Stein — *Introduction to Algorithms* (4ª ed., MIT Press), invariantes como trazado simbólico.

---

> [⏮️ Clase 007](../../parte-0-pensamiento-computacional-y-el-metodo-poliglota/007-pseudocodigo-neutral-escribir-sin-lenguaje/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 009 ⏭️](../../parte-0-pensamiento-computacional-y-el-metodo-poliglota/009-complejidad-y-eficiencia-intuicion-de-coste/README.md)
