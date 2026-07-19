# Clase 007 — Pseudocódigo neutral: escribir sin lenguaje

> Parte **0 — Pensamiento computacional y el método políglota** · ⏱️ Duración estimada: **75 min** · Nivel: **Fundamentos**
> ✅ **Clase construida.**

---

## 🎯 Objetivo

El **pseudocódigo** es una notación para expresar un algoritmo de forma legible por humanos, estructurada pero informal, y deliberadamente independiente de cualquier lenguaje real. Es el puente entre la idea (que vive en tu cabeza) y las diez implementaciones (que viven en diez sintaxis distintas). Cuando escribes primero en pseudocódigo, capturas la *lógica* sin comprometerte con la *forma*, y luego la traducción a Python, Java o Go se vuelve casi mecánica. El objetivo de hoy es que aprendas a escribir pseudocódigo genuinamente neutral y a resistir la tentación de que se convierta en "un lenguaje disfrazado".

Este es el hábito que separa a quien piensa antes de teclear de quien teclea para pensar. Cormen escribe *todo* *Introduction to Algorithms* en pseudocódigo precisamente para que sus algoritmos sean independientes del lenguaje de moda: un algoritmo publicado en pseudocódigo en 1990 sigue siendo legible y traducible hoy, mientras que uno escrito en el lenguaje de moda de entonces habría envejecido. El pseudocódigo es el formato en que las ideas de programación se conservan y se comunican.

## 🧩 Situación

En una entrevista técnica te plantean un problema y añaden: "resuélvelo en el lenguaje que quieras". Si te lanzas directo al código, empiezas a pelear con la sintaxis —¿era `elif` o `else if`?, ¿lleva punto y coma?— y la lógica, que era lo que evaluaban, se te enreda entre detalles triviales. Si en cambio esbozas primero el pseudocódigo en la pizarra, ordenas la lógica sin ruido, el entrevistador ve tu razonamiento con claridad, y traducir ese esqueleto al lenguaje final es un trámite de dos minutos. El mismo hábito sirve en el trabajo real: ante un problema difícil, el pseudocódigo es donde resuelves *el problema*, y el editor de código es donde solo lo *transcribes*.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Escribir un algoritmo en pseudocódigo claro y neutral.
2. Traducir ese pseudocódigo a cualquier lenguaje del núcleo.
3. Reconocer y evitar el "pseudocódigo" que en realidad es un lenguaje concreto disfrazado.
4. Elegir el nivel de detalle correcto: ni tan vago que pierda la lógica, ni tan preciso que sea ya código.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Convenciones del pseudocódigo | Un vocabulario mínimo y consistente |
| 2 | Neutralidad | No favorecer la sintaxis de ningún lenguaje |
| 3 | Del pseudocódigo al código | Cómo cada lenguaje "rellena" la misma lógica |

## 📖 Definiciones y características

El **pseudocódigo** es una descripción de un algoritmo en lenguaje estructurado pero informal: tiene la disciplina de secuencia, decisión y repetición de un programa, pero la libertad de expresión de la prosa. Su virtud definitoria es la **neutralidad**: no usa la sintaxis específica de ningún lenguaje real, de modo que se traduce con igual facilidad a los diez del núcleo. Cuando escribes `PARA cada x en lista` no estás pensando en `for x in lista` (Python) ni en `for (auto x : lista)` (C++); estás pensando en la *idea* de recorrer, que ambos comparten. Cormen fija sus propias convenciones al inicio de su libro precisamente para que el lector sepa qué significa cada construcción sin atarla a un lenguaje.

Este curso adopta un vocabulario mínimo y consistente. Para la **asignación** usa la flecha `<-` (dar un valor a un nombre), deliberadamente distinta de `=`, `:=` o `let`, para no favorecer a nadie: `total <- 0`. Para el control de flujo usa palabras en mayúscula que son verbos claros: `SI`/`SINO` para decidir, `PARA`/`MIENTRAS` para repetir, `DEVOLVER` para dar un resultado. Para la entrada y salida usa `LEER` y `ESCRIBIR`, sin comprometerse con `input`, `Scanner`, `cin` o `readline`. La estructura se marca con la sangría, no con llaves ni con `end`. Este pequeño diccionario basta para expresar cualquier algoritmo del curso, y su consistencia es lo que hace que el paso a código sea mecánico.

El poder del pseudocódigo neutral se ve en la traducción: **cada lenguaje "rellena" la misma lógica con su forma particular**. Un `PARA cada x en lista` se convierte en un `for` en todos, pero cada uno lo escribe a su manera; un `SI ... SINO` se vuelve `if/else`, `if/elif`, o un `match`, según el lenguaje. La lógica —la secuencia de decisiones y repeticiones— es invariante; solo cambia el ropaje. Esta es la misma tesis de la clase 001 aplicada a la escritura: el pseudocódigo *es* la forma neutral del concepto, y las implementaciones son sus encarnaciones. El error que arruina todo esto es dejar que el pseudocódigo se contamine: si escribes `for i in range(len(lista))` o `System.out.println`, ya no es pseudocódigo, es Python o Java disfrazados, y pierdes la neutralidad que era todo el punto.

## 🔎 Ejemplo

El mismo algoritmo de la venta de la clase 003, ahora en pseudocódigo neutral, listo para traducir a cualquier lenguaje:

```text
LEER precio, cantidad, descuento
subtotal <- precio * cantidad
total    <- subtotal * (1 - descuento)
ESCRIBIR "Total: " + FORMATEAR(total, 2 decimales)
```

Observa que no hay ningún compromiso sintáctico: `<-` no es de ningún lenguaje, `LEER`/`ESCRIBIR` son verbos neutrales, `FORMATEAR(total, 2 decimales)` describe *qué* se quiere (dos decimales) sin decir *cómo* (que en Python es `f"{total:.2f}"`, en Java `String.format`, en C `printf("%.2f")`). Cada una de las diez implementaciones de la [clase 041](../../parte-3-valores-tipos-y-variables/041-literales-valores-variables-y-constantes/README.md) no es más que este esqueleto rellenado con la forma de su lenguaje. Escribe el esqueleto bien una vez y tendrás diez traducciones casi gratis.

## ✍️ Práctica

Escribe en pseudocódigo neutral el algoritmo "invertir una cadena de texto" (dado "hola", producir "aloh"). La disciplina es estricta: no puedes usar ninguna función específica de un lenguaje (nada de `[::-1]` de Python ni `StringBuilder.reverse()` de Java); tienes que expresar la lógica con `PARA`/`MIENTRAS`, `<-` y verbos neutrales, recorriendo la cadena y construyendo el resultado carácter a carácter. Cuando termines, traduce tu pseudocódigo a dos lenguajes que conozcas y comprueba que ambas traducciones salen casi solas. Si te costó traducir, probablemente tu pseudocódigo era demasiado vago; si copiaste una función de biblioteca, era demasiado concreto. El punto dulce está en el medio.

## ⚠️ Errores comunes

| Síntoma / mensaje | Causa y cómo corregirlo |
|-------------------|--------------------------|
| Tu "pseudocódigo" es Python con acentos | Usaste `for i in range`, métodos y sintaxis reales. Cambia a `PARA`/`MIENTRAS`/`SI` y verbos neutrales |
| Al traducir, la lógica no encaja en el lenguaje | El pseudocódigo asumía features de un solo lenguaje. Manténlo en operaciones que todos tengan |
| El pseudocódigo es tan vago que no se puede traducir | Perdiste la lógica en ambigüedad. Cada paso esencial debe estar, aunque sin sintaxis |
| El pseudocódigo es tan detallado como el código | Te pasaste de concreto. Describe el *qué* (formatear a 2 decimales), no el *cómo* |

## ❓ Preguntas frecuentes

**❓ ¿Existe un estándar oficial de pseudocódigo?** No hay uno universal; cada libro y cada curso fija el suyo. Lo que importa es la *consistencia*: este curso usa `<-`, `PARA`, `MIENTRAS`, `SI`/`SINO`, `LEER`, `ESCRIBIR` y `DEVOLVER` siempre igual. Cormen, por ejemplo, usa su propio conjunto de convenciones, distinto en los detalles pero idéntico en el espíritu.

**❓ ¿Tengo que escribir pseudocódigo siempre, incluso para lo trivial?** No. Para un problema trivial, el pseudocódigo vive en tu cabeza y vas directo al código. La herramienta rinde en los problemas *nuevos o difíciles*, donde separar "resolver la lógica" de "escribir la sintaxis" te ahorra enredarte en dos cosas a la vez.

**❓ ¿No es una pérdida de tiempo escribir dos veces (pseudocódigo y luego código)?** No lo es, porque no escribes lo mismo dos veces: en el pseudocódigo resuelves *el problema* y en el código solo lo *transcribes*. La transcripción es rápida y casi libre de errores cuando la lógica ya está clara. Saltarse el pseudocódigo en un problema difícil suele costar más tiempo en depuración del que habría costado escribirlo.

## 🔗 Referencias

- T. Cormen, C. Leiserson, R. Rivest y C. Stein — *Introduction to Algorithms* (4ª ed., MIT Press), convenciones de pseudocódigo.
- H. Abelson y G. J. Sussman — *Structure and Interpretation of Computer Programs* (2ª ed., MIT Press) — [gratis online](https://mitpress.mit.edu/9780262510875/).
- G. Polya — *How to Solve It* (Princeton University Press), sobre expresar el plan antes de ejecutarlo.
- A. Hunt y D. Thomas — *The Pragmatic Programmer* (2ª ed., Addison-Wesley), sobre prototipar la lógica.

---

> [⏮️ Clase 006](../../parte-0-pensamiento-computacional-y-el-metodo-poliglota/006-algoritmos-correccion-y-terminacion/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 008 ⏭️](../../parte-0-pensamiento-computacional-y-el-metodo-poliglota/008-trazado-manual-y-ejecucion-simbolica/README.md)
