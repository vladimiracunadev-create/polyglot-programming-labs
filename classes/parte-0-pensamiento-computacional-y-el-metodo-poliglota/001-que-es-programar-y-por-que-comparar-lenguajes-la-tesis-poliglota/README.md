# Clase 001 — Qué es programar y por qué comparar lenguajes: la tesis políglota

> Parte **0 — Pensamiento computacional y el método políglota** · ⏱️ Duración estimada: **75 min** · Nivel: **Fundamentos**
> ✅ **Clase construida.**

---

## 🎯 Objetivo

Programar no es "escribir código en Python" ni "saberse la sintaxis de Java". Programar es **resolver un problema expresándolo como una secuencia de instrucciones tan precisas que una máquina, que no entiende nada, pueda ejecutarlas sin ambigüedad**. Esa distinción es el corazón de esta clase y de todo el curso. Cuando la interiorizas, dejas de coleccionar lenguajes y empiezas a acumular una habilidad que ninguno de ellos te puede quitar.

La tesis de este programa es que el conocimiento de programación es **transferible**. Un mismo concepto —guardar un valor con un nombre, repetir un cálculo, decidir entre dos caminos, agrupar pasos en una función— existe en todos los lenguajes; lo único que cambia entre ellos es la *forma* de escribirlo. Aprender el concepto una sola vez, en su versión neutral, te permite reconocerlo, compararlo y aplicarlo en cualquier lenguaje, incluso en uno que nunca estudiaste. El objetivo de hoy es que salgas convencido de que aprender *a programar* y aprender *un lenguaje* son dos cosas distintas, y que la primera es la que de verdad importa.

## 🧩 Situación

Imagina a alguien que aprende Python, completa cincuenta ejercicios y se siente competente. Un día le asignan mantener un servicio escrito en Go. Abre el archivo, ve `:=`, `func`, llaves por todas partes, y se paraliza: concluye que "no sabe programar". Pero es falso. Sí sabe: sabe qué es una variable, qué es un bucle, qué es una función. Lo que no sabe es reconocer esos mismos conceptos con **otra piel**. Su problema no es de programación, es de traducción, y es mucho más pequeño de lo que cree.

Esta escena se repite en cada equipo real. El software de producción casi nunca vive en un solo lenguaje: hay un frontend en JavaScript, un backend en Go o Java, consultas en SQL, quizá un módulo crítico en Rust o C. Quien entiende que todo eso comparte los mismos conceptos se mueve entre capas con soltura; quien aprendió "un lenguaje" en vez de "a programar" se queda atrapado en su isla. Este curso ataca justamente esa diferencia, y por eso empieza aquí.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Explicar la diferencia entre aprender *un* lenguaje y aprender *a programar*.
2. Enunciar la tesis políglota: concepto → forma neutral → implementaciones → comparación → transferencia.
3. Distinguir el conocimiento transferible del detalle sintáctico de un lenguaje concreto.
4. Justificar por qué comparar lenguajes acelera el aprendizaje en lugar de dispersarlo.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Programar = resolver con precisión | Separa la idea (algoritmo) de su escritura (lenguaje) |
| 2 | Concepto vs. sintaxis | Lo que perdura frente a lo que cambia entre lenguajes |
| 3 | Los 10 lenguajes del núcleo | El terreno práctico que se implementa y verifica |
| 4 | Las ~40 familias del Atlas | Amplían la comprensión sin multiplicar el mantenimiento |
| 5 | Reconocer, comparar, aplicar | El ciclo que convierte teoría en habilidad |

## 📖 Definiciones y características

**Programar** es expresar la solución de un problema como instrucciones que una máquina ejecuta. La palabra clave es *solución*: antes de que exista código, existe una idea de cómo resolver el problema, y esa idea es independiente del lenguaje. George Polya, en *How to Solve It*, describió la resolución de problemas en cuatro fases —entender el problema, trazar un plan, ejecutarlo y revisar— y ninguna de ellas menciona un lenguaje de programación. El lenguaje solo aparece en la tercera fase, la ejecución, y es la menos intelectual de las cuatro. Cuando alguien dice "no sé por dónde empezar", casi nunca es un problema de sintaxis: es que aún no ha entendido el problema ni trazado el plan.

El **conocimiento transferible** es la idea que sobrevive al cambio de lenguaje. "Iterar sobre una colección" es transferible; `for x in lista` es una forma particular de expresarlo en Python. Abelson y Sussman lo enmarcan en el prefacio de *Structure and Interpretation of Computer Programs* con una frase que conviene grabarse: los programas deben escribirse para que las personas los lean, y solo de forma incidental para que las máquinas los ejecuten. Si el destinatario primario es humano, entonces lo esencial de un programa son sus **ideas**, no los símbolos concretos con que se teclean. Esas ideas son justo lo transferible.

Este curso organiza esa transferencia en dos niveles. El **núcleo** son diez lenguajes —Python, JavaScript, TypeScript, Java, C#, Go, Rust, C, SQL y PHP— que se implementan de verdad y se verifican automáticamente: aportan profundidad práctica. El **Atlas** cubre alrededor de cuarenta lenguajes agrupados por familias, no para que los domines todos, sino para que reconozcas sus rasgos: aporta amplitud de comprensión sin multiplicar el mantenimiento. El puente entre ambos es la **tesis políglota**: un concepto se enuncia en forma neutral, se implementa en varios lenguajes, se comparan las implementaciones y de esa comparación nace la transferencia. Hunt y Thomas, en *The Pragmatic Programmer*, recomiendan aprender un lenguaje nuevo cada año precisamente porque comparar amplía la caja de herramientas mentales: cada lenguaje resuelve las mismas necesidades con decisiones distintas, y ver esas decisiones lado a lado enseña más que profundizar en una sola.

## 🔎 Ejemplo

Tomemos el concepto más elemental de todos: "guardar un valor con un nombre". Aquí está en tres lenguajes del núcleo:

```text
Python:  total = 27000
Go:      total := 27000
Rust:    let total = 27000;
```

Las tres líneas hacen lo mismo: crean un nombre `total` que apunta al valor `27000`. Cambia la puntuación —Python no marca nada especial, Go usa `:=` para declarar-y-asignar, Rust exige `let` y termina en `;`— pero **la idea es idéntica**. Si entiendes qué es "asociar un nombre a un valor", ya puedes leer las tres, aunque solo hayas estudiado una.

Lo interesante llega cuando la comparación revela una diferencia que *no* es cosmética. En Rust, esa variable es inmutable por defecto: si intentas reasignarla el compilador te detiene. En Python y Go puedes reasignarla sin problema. Esa diferencia ya no es de escritura, es de *comportamiento*, y es exactamente el tipo de cosa que la comparación pone sobre la mesa y el estudio de un solo lenguaje esconde. La clase 002 le pondrá nombre a estas tres capas de diferencia.

## ✍️ Práctica

Toma la expresión `precio * cantidad` y realiza tres pasos, en orden y sin saltarte ninguno:

1. Escribe en **una sola frase, en español y sin mencionar ningún lenguaje**, qué calcula ese programa. (Algo como: "multiplica el precio unitario por la cantidad para obtener el importe".) Esa frase es el concepto neutral.
2. Busca cómo se escribiría esa multiplicación en dos lenguajes que conozcas o puedas consultar. Cópialas una debajo de otra.
3. Subraya qué es **idéntico** en ambas (el operador `*`, el orden de los operandos, la idea de multiplicar) y qué **cambia** (nombres, punto y coma, declaración de tipos).

Cuando termines, habrás hecho en pequeño lo que el curso hace en grande: destilar el concepto, verlo encarnado en varios lenguajes y separar lo que perdura de lo que cambia.

## ⚠️ Errores comunes

| Síntoma / creencia | Causa y cómo corregirlo |
|--------------------|--------------------------|
| "Sé Python, luego sé programar" | Confundir el lenguaje con la disciplina. Estudia el concepto y oblígate a reconocerlo en otro lenguaje distinto |
| Memorizar sintaxis sin el concepto detrás | Aprender la forma sin el fondo. Para cada línea, pregunta "¿qué idea neutral expresa esto?" |
| Creer que aprender varios lenguajes dispersa | Verlos como listas de sintaxis inconexas. Enfócalos como variaciones de un mismo puñado de conceptos |
| Bloquearse ante un lenguaje nuevo | Buscar lo desconocido en vez de lo familiar. Empieza identificando qué conceptos ya reconoces |

## ❓ Preguntas frecuentes

**❓ ¿Necesito saber los 10 lenguajes del núcleo antes de empezar?** No. Empiezas por el concepto, siempre en forma neutral, y los lenguajes se van introduciendo comparándolos. No hace falta dominar ninguno para entender la idea que ilustran.

**❓ ¿No es más fácil dominar uno solo y ya?** Para conseguir tu primer empleo, quizá. Para *entender de verdad* la programación, no: comparar es lo que revela por qué cada lenguaje decide lo que decide (por qué Rust es inmutable por defecto, por qué SQL no tiene bucles). Sin comparación, cada decisión parece arbitraria en vez de deliberada.

**❓ Entonces, ¿la sintaxis no importa?** Importa, pero es lo más barato de adquirir: se consulta en segundos y se olvida sin consecuencias. El concepto, en cambio, tardas en construirlo y no se consulta en una tabla. Invierte tu esfuerzo donde rinde.

## 🔗 Referencias

- G. Polya — *How to Solve It* (Princeton University Press). Las cuatro fases de la resolución de problemas.
- H. Abelson y G. J. Sussman — *Structure and Interpretation of Computer Programs* (2ª ed., MIT Press), Prefacio — [gratis online](https://mitpress.mit.edu/9780262510875/).
- A. Hunt y D. Thomas — *The Pragmatic Programmer* (2ª ed., Addison-Wesley), tema "Your Knowledge Portfolio".
- T. Cormen, C. Leiserson, R. Rivest y C. Stein — *Introduction to Algorithms* (4ª ed., MIT Press), cap. 1.

---

> [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 002 ⏭️](../../parte-0-pensamiento-computacional-y-el-metodo-poliglota/002-las-tres-clases-de-diferencia-sintactica-semantica-y-paradigmatica/README.md)
