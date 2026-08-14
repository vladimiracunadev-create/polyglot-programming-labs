# Parte 4 — Control del programa

> [⏮️ Parte 3](../parte-3-valores-tipos-y-variables/README.md) · [⬅️ Programa](../../README.md) · [📚 Índice](../README.md) · [⏭️ Parte 5](../parte-5-funciones-y-modularidad/README.md)

**16 clases** · rango 057–072 · clases de **código** · nivel intermedio · **~40 h** ([cronograma](../../docs/syllabus.md))

> 🧭 **Decidir, repetir y fallar: el flujo del programa y sus formas en diez lenguajes.**

---

## 🧭 De qué trata esta parte

Un programa que solo calcula expresiones no es todavía un programa. La Parte 4 añade las dos operaciones que lo convierten en uno —**decidir** y **repetir**— y termina con la tercera que nadie llama control de flujo y lo es: **fallar**.

El recorrido va de lo más concreto a lo más expresivo. Empieza por la condición y sus formas (`if`, ternario, `switch`, `match`), sigue por los bucles en sus tres sabores (por condición, por rango, por colección) y llega a la iteración perezosa y a las comprensiones, donde el «cómo recorro» empieza a desaparecer del código. Después, `map`/`filter`/`reduce` y la recursión muestran que se puede repetir sin escribir un solo bucle.

El cierre son las dos filosofías del error: la **excepción**, que salta por la pila hasta quien sepa atenderla, y el **resultado como valor**, que obliga a mirarlo en el sitio. Es una de las divisiones más profundas entre los lenguajes del núcleo y se ve mejor con las dos implementadas lado a lado.

## 🎒 Qué necesitas traer

La Parte 3 completa: booleanos (046), operadores (055) y entrada/salida (056) se usan en todas las clases de esta parte.

## 🎯 Qué sabrás hacer al terminar

Resultados comprobables: si no puedes hacerlos, la parte no está cerrada.

1. Elegir entre `if`, `switch` y `match` con un criterio explícito y no por costumbre.
2. Escribir un bucle con su invariante y su condición de parada argumentadas.
3. Reescribir un bucle imperativo como comprensión o como `map`/`filter`/`reduce`.
4. Explicar qué hace el cortocircuito y por qué es semántica y no optimización.
5. Implementar el mismo fallo con excepciones y con `Result`, y defender cuál conviene.
6. Reconocer cuándo la recursión es la forma natural y cuándo va a desbordar la pila.

## 🗺️ El recorrido, clase a clase

Las clases están agrupadas en bloques por la razón que las une. El orden es secuencial: cada una asume la anterior.

### 🔹 Decidir · clases 057–062

De la condición booleana a la coincidencia de patrones, pasando por las guardas y el `switch`.

- **[057 · Booleanos, condiciones y cortocircuito](057-booleanos-condiciones-y-cortocircuito/README.md)** — Todo programa que decide algo fabrica antes un valor de verdad. El **cortocircuito** (`&&`, `||`) no es una optimización: es semántica observable, porque determina si el segundo operando —y sus efectos— llega a evaluarse.
- **[058 · Guardas y validación temprana](058-guardas-y-validacion-temprana/README.md)** — Una **guarda** atiende primero todo lo que puede salir mal y sale de inmediato, dejando el resto del cuerpo para un solo camino: el correcto. Es la técnica más barata para eliminar anidamiento y la que más legibilidad devuelve por línea escrita.
- **[059 · if / else y anidamiento](059-if-else-y-anidamiento/README.md)** — La cadena `if` / `else if` / `else` elige entre alternativas mutuamente excluyentes. Aquí se ve por qué el anidamiento profundo es un problema de comprensión y no de estilo, y cómo cada lenguaje lo aplana con recursos distintos.
- **[060 · Expresiones condicionales: ternario e if como expresión](060-expresiones-condicionales-ternario-e-if-como-expresion/README.md)** — Muchas veces no queremos *ejecutar* una de dos acciones sino *elegir* uno de dos valores. La diferencia entre `if` como sentencia y como **expresión** separa a Rust y Kotlin de C y Java, y explica por qué unos necesitan el operador ternario y otros no.
- **[061 · switch, case y fallthrough](061-switch-case-y-fallthrough/README.md)** — El `switch` nace de una necesidad concreta: elegir entre muchos valores exactos sin una escalera ilegible de `else if`. El **fallthrough** —caer al siguiente caso— es la trampa clásica, y los lenguajes modernos la han invertido por defecto.
- **[062 · Coincidencia de patrones: match / when](062-coincidencia-de-patrones-match-when/README.md)** — La coincidencia de patrones da un salto conceptual sobre el `switch`: en vez de preguntar «¿es igual a esta constante?», pregunta «¿tiene esta **forma**?», y desestructura al mismo tiempo que decide. Es la puerta de entrada a los tipos algebraicos.

### 🔹 Repetir · clases 063–067

Los tres sabores de bucle, la evaluación perezosa y las comprensiones.

- **[063 · Iteración por condición: while y do-while](063-iteracion-por-condicion-while-y-do-while/README.md)** — El `while` es el bucle en su forma más pura: repetir mientras algo siga siendo cierto, sin presuponer contador ni número de vueltas. Es más fundamental que el `for`, y por eso es donde se estudian el invariante y la condición de parada.
- **[064 · Iteración por rango: for clásico y for-range](064-iteracion-por-rango-for-clasico-y-for-range/README.md)** — El bucle `for` cubre el caso más común: saber de antemano cuántas veces o sobre qué rango. La distancia entre el `for` clásico de C y el `for-range` de Go o Python muestra cuánta ceremonia era accidental.
- **[065 · Iteración por colección: for-each e iteradores](065-iteracion-por-coleccion-for-each-e-iteradores/README.md)** — «Para cada elemento de esto, haz aquello»: sin índices, sin contadores, sin la posibilidad de equivocarse en el límite. Detrás está el **iterador**, el protocolo que cada lenguaje implementa a su manera y que conviene conocer.
- **[066 · Iteradores y generadores perezosos (lazy)](066-iteradores-y-generadores-perezosos-lazy/README.md)** — La evaluación **perezosa** invierte una suposición tan arraigada que casi nunca se enuncia: que para trabajar con una secuencia hay que tenerla entera en memoria. Generadores y flujos permiten procesar lo infinito y lo enorme con memoria constante.
- **[067 · Comprensiones de listas y colecciones](067-comprensiones-de-listas-y-colecciones/README.md)** — Una **comprensión** construye una colección describiéndola en lugar de fabricarla paso a paso. Su forma —«los `x` de la lista tales que `x` es par»— viene de la notación matemática de conjuntos, y es el punto donde lo imperativo empieza a ceder terreno.

### 🔹 Repetir sin bucles · clases 068–069

Funciones de orden superior y recursión: el mismo trabajo sin escribir el recorrido.

- **[068 · Funciones de orden superior: map, filter, reduce](068-funciones-de-orden-superior-map-filter-reduce/README.md)** — `map`, `filter` y `reduce` son la prueba de que una función puede recibir otra función. Con esos tres verbos se expresa la mayoría de los bucles que escribes, y se hace visible qué parte era recorrido y qué parte era lógica.
- **[069 · Recursión y recursión de cola](069-recursion-y-recursion-de-cola/README.md)** — La recursión existe porque hay estructuras que son recursivas por naturaleza —árboles, listas, gramáticas—. Aquí se ve también su coste real en la pila y qué lenguajes optimizan la **recursión de cola** (spoiler: menos de los que se cree).

### 🔹 Salir del flujo y fallar bien · clases 070–072

Saltos controlados y las dos grandes filosofías del manejo de errores.

- **[070 · Control de flujo: break, continue, return, goto](070-control-de-flujo-break-continue-return-goto/README.md)** — `break`, `continue`, `return` y el proscrito `goto` son salidas del flujo natural. Ninguno es malo por sí mismo: lo que importa es si hacen el código más fácil o más difícil de razonar, y esa evaluación se puede argumentar.
- **[071 · Manejo de errores I: excepciones (try/catch/finally)](071-manejo-de-errores-i-excepciones-try-catch-finally/README.md)** — Una excepción es una transferencia de control **no local**: el flujo salta hasta el manejador más cercano en la pila. Potente y peligrosa a partes iguales, porque su camino no se ve leyendo la función donde ocurre el fallo.
- **[072 · Manejo de errores II: resultados y valores (Result/Either/error de Go)](072-manejo-de-errores-ii-resultados-y-valores-result-either-error-de-go/README.md)** — El enfoque opuesto: si una función puede fallar, que lo diga en su **tipo de retorno**. `Result` en Rust, `error` en Go, `Either` en la familia ML. El error deja de ser un canal aparte y pasa a ser un valor que el compilador te obliga a mirar.

## ⚠️ Los malentendidos que esta parte corrige

| Se suele creer | Lo que ocurre en realidad |
|---|---|
| «`match` es un `switch` más bonito.» | El `switch` compara con constantes; el `match` compara **formas** y desestructura. Son operaciones distintas. |
| «La recursión siempre es más elegante.» | Es más natural sobre estructuras recursivas y desastrosa sobre secuencias largas en lenguajes sin optimización de cola. |
| «Las excepciones son el manejo de errores moderno.» | Go y Rust demuestran lo contrario: el error como valor es igual de moderno y mucho más visible en la firma. |

## 🧪 Cómo estudiar esta parte

1. **Lee el modelo y el pseudocódigo primero.** Si entiendes el algoritmo neutral, las diez implementaciones son diez traducciones, no diez problemas.
2. **Lee las diez implementaciones, no solo la de tu lenguaje.** El aprendizaje está en el contraste: ahí se distingue lo esencial del accidente sintáctico.
3. **Ejecuta el verificador** (`python scripts/verificar_equivalencia.py NNN`) y comprueba tú mismo que coinciden. Fuerza después un caso límite y observa quién se rompe primero.
4. **Lee `primos.md`** para ver el mismo programa en la familia de cada lenguaje: es donde el concepto deja de estar atado a diez nombres concretos.
5. **Haz el reto de transferencia.** Portarlo a un lenguaje que no dominas es la única prueba real de que aprendiste el concepto y no la sintaxis.

## 📚 Fuentes de referencia de esta parte

Cada clase cita estos libros en su sección de referencias. No se reproduce su contenido: la redacción es original.

- O.-J. Dahl, E. W. Dijkstra y C. A. R. Hoare — *Structured Programming* (Academic Press).
- R. W. Sebesta — *Concepts of Programming Languages* (12ª ed., Pearson), cap. control de flujo.

## 🔗 Qué abre esta parte

Con flujo y datos elementales, la Parte 5 introduce la abstracción que lo ordena todo: la función y el módulo.

---

> [⏮️ Parte 3](../parte-3-valores-tipos-y-variables/README.md) · [⬅️ Programa](../../README.md) · [📚 Índice](../README.md) · [⏭️ Parte 5](../parte-5-funciones-y-modularidad/README.md)
