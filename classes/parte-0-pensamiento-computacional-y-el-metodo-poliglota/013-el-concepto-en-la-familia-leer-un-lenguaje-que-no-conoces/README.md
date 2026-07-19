# Clase 013 — El concepto en la familia: leer un lenguaje que no conoces

> Parte **0 — Pensamiento computacional y el método políglota** · ⏱️ Duración estimada: **75 min** · Nivel: **Fundamentos**
> ✅ **Clase construida.**

---

## 🎯 Objetivo

Esta clase enseña la habilidad más rentable del enfoque políglota: **leer con provecho código de un lenguaje que nunca estudiaste**. No escribirlo bien, no dominarlo, no discutir sus rincones oscuros. Leerlo: entender qué hace, seguir su lógica, opinar en una revisión, encontrar un fallo. Esa habilidad es alcanzable en minutos, no en meses, y descansa en un hecho estructural del mundo de los lenguajes: no son cuarenta invenciones independientes, sino unas pocas familias con descendientes. Si sabes C, ya reconoces buena parte de la superficie de Java, C#, JavaScript, Go y PHP, porque todos heredaron de él las llaves, los paréntesis de condición, la aritmética y la forma general de declarar funciones.

La razón de que esto funcione es genealógica. Sebesta dedica un capítulo entero de *Concepts of Programming Languages* a la evolución de los lenguajes precisamente porque cada uno se diseñó reaccionando a los anteriores: tomando lo que funcionaba, corrigiendo lo que dolía. Esa herencia deja huellas visibles. Cuando reconoces la familia de un fragmento, no estás adivinando: estás usando información real sobre su ascendencia. Y entonces el trabajo de lectura se reduce enormemente, porque en vez de aprender un lenguaje entero solo tienes que identificar el **delta**: aquello en lo que el descendiente se apartó de su antepasado.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Ubicar un lenguaje desconocido en su familia a partir de su aspecto y su vocabulario.
2. Leer y explicar un fragmento de un lenguaje no estudiado apoyándote en su parecido con uno que conoces.
3. Distinguir qué parte del fragmento es familiar y qué parte exige atención por ser una diferencia semántica.
4. Formular por escrito el delta entre un lenguaje nuevo y su representante de familia.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Familias y parecidos | Lenguajes primos comparten sintaxis y modelo |
| 2 | Leer por analogía | Mapear lo nuevo a lo conocido |
| 3 | Dónde poner atención | Las diferencias semánticas, no las cosméticas |
| 4 | El delta | Lo único que realmente hay que aprender de nuevo |

## 📖 Definiciones y características

Una **familia de lenguajes** es un grupo que comparte antepasado y, por herencia, rasgos de sintaxis y de modelo de ejecución. La familia de las llaves —C, C++, Java, C#, JavaScript, Go, PHP— comparte bloques delimitados por `{}`, condiciones entre paréntesis y un estilo imperativo de sentencias. La familia funcional tipada —ML, Haskell, OCaml, F#— comparte inferencia de tipos, ajuste de patrones y expresiones donde las otras tienen sentencias. Reconocer la familia de un fragmento en cinco segundos ya te da una hipótesis de trabajo enorme: sabes qué esperar de sus bucles, de sus funciones y de sus condicionales antes de leer una sola línea con atención.

La **lectura por analogía** es el procedimiento: eliges un representante de la familia que sí conoces y lees el lenguaje nuevo como una variación suya. Es el mismo mecanismo cognitivo con el que un hablante de español lee italiano escrito sin haberlo estudiado. El truco está en el orden: primero identificas lo que reconoces, no lo que te resulta extraño. Quien empieza por lo extraño se paraliza, porque lo extraño destaca y parece dominar el texto; quien empieza por lo familiar descubre que suele ser el ochenta o el noventa por ciento del fragmento y que lo desconocido son media docena de palabras clave. Hunt y Thomas recomiendan en *The Pragmatic Programmer* aprender un lenguaje nuevo cada año, y esta es la mecánica que hace ese consejo viable: cada lenguaje nuevo cuesta menos que el anterior porque cada vez conoces más familias.

El **delta** es lo que cambia respecto del representante y es, literalmente, lo único que hay que aprender de nuevo. Pero no todos los deltas son iguales, y aquí es donde la clase 002 se vuelve imprescindible. Un delta **sintáctico** —que Kotlin escriba `fun` donde Java escribe la firma completa, o que Go ponga el tipo después del nombre— se absorbe en segundos y no puede causar daño: si lo malinterpretas, no entiendes la línea y lo notas. Un delta **semántico** es otra cosa, porque el código se te parece a algo que ya sabes y por eso mismo no enciende ninguna alarma. Que `val` en Kotlin haga la referencia inmutable pero no el objeto apuntado, que `==` en Java compare identidad de objetos mientras en Python compara valor, que una asignación en Rust mueva el valor en vez de copiarlo: todo eso se lee igual que lo conocido y significa otra cosa. Por eso la lectura por analogía debe cerrarse siempre con la pregunta de control: *¿qué hay aquí que se parezca a lo que sé pero funcione distinto?* Sin ella, la analogía deja de ser una herramienta y se convierte en una trampa.

## 🧩 Situación

Te asignan revisar un pull request en Kotlin y nunca has escrito una línea de Kotlin. La reacción instintiva es declinar: "no sé ese lenguaje". La reacción entrenada es otra: miras el archivo, ves clases, tipos declarados, llaves y `import`, y concluyes en segundos que es familia JVM, prima directa de Java. A partir de ahí lees por analogía. `val` es una constante, el equivalente de un `final`; `fun` introduce una función; los tipos se infieren, como en Rust o en Go. Terminas entendiendo el noventa por ciento del cambio y puedes comentar sobre la lógica, que es de lo que trata una revisión de código.

Lo importante es qué haces con el diez por ciento restante. No lo ignoras ni lo adivinas: lo señalas. Ves un `?.` y no estás seguro de si esa llamada se salta cuando el valor es nulo o lanza una excepción, así que lo consultas o preguntas en el propio pull request. Ese gesto —leer por analogía y marcar explícitamente lo no verificado— es lo que separa a alguien que se apoya en la familia de alguien que se inventa el significado. La analogía te lleva hasta la puerta del delta; cruzarla exige comprobación.

## 🔎 Ejemplo

Leer Kotlin sabiendo Java (misma familia JVM):

```text
Kotlin:  val precio = 15000.0        // 'val' = final (constante)
         fun total(c: Int) = ...     // 'fun' = método
Java:    final double precio = 15000.0;
         double total(int c) { ... }
```

Mira cuánto es familiar. Hay un nombre asociado a un valor, hay una función con un parámetro entero, hay un literal decimal. Todo eso lo sabías. El delta visible es sintáctico y pequeño: Kotlin escribe `val` en vez de `final`, `fun` en vez de la firma con tipo de retorno al principio, pone el tipo después del nombre (`c: Int`) y omite el punto y coma. Cuatro decisiones cosméticas que se aprenden mirándolas una vez.

Pero debajo hay un delta que la comparación línea a línea no muestra y que conviene buscar activamente. En Kotlin, `val` significa que la **referencia** no se reasigna, no que el objeto sea inmutable: si `precio` fuera una lista mutable, seguirías pudiendo añadirle elementos. Y el sistema de tipos de Kotlin distingue `String` de `String?`, de modo que una variable no anulable no puede recibir `null` en absoluto, algo que Java no garantiza. Ninguna de esas dos cosas se ve en el fragmento, y ambas cambian el comportamiento. Esa es la lección: la analogía te entrega la sintaxis gratis y te deja el trabajo real, que es la semántica.

## ✍️ Práctica

Abre la sección "🧬 El concepto en la familia" de la clase 041 y elige un primo que no hayas estudiado —Ruby, Kotlin o Haskell— para hacer el ejercicio completo en tres pasos:

1. **Ubica la familia.** ¿A qué lenguaje del núcleo se parece más y por qué? Nombra dos rasgos concretos que lo delaten (llaves, palabras clave, uso de tipos, forma de las funciones).
2. **Traduce por analogía.** Escribe la línea equivalente en el lenguaje del núcleo que hayas elegido como representante y explica en una frase qué hace el fragmento original.
3. **Formula el delta y clasifícalo.** Lista qué cambia respecto del representante y marca cada punto como sintáctico o semántico. Si dudas de alguno, esa duda es exactamente lo que debes verificar: consúltalo y anota la respuesta.

Repite el ejercicio con Haskell y notarás algo interesante: la analogía rinde mucho menos, porque no es de tu familia. Ahí el trabajo de lectura es real, y saberlo de antemano también forma parte de la habilidad.

## ⚠️ Errores comunes

| Síntoma / creencia | Causa y cómo corregirlo |
|--------------------|--------------------------|
| "No sé este lenguaje, luego no puedo leerlo" | Ignorar el parecido de familia. Identifica primero a qué familia pertenece y lee por analogía desde un representante conocido |
| Empezar por lo que resulta extraño | Lo desconocido destaca y parece dominar el texto. Empieza inventariando lo que sí reconoces: suele ser la mayor parte |
| Confiar en la analogía sin verificar el delta | Es el fallo caro: lo que se parece pero significa otra cosa no dispara ninguna alarma. Pregunta siempre qué se comporta distinto y compruébalo |
| Asumir familia por un solo rasgo | Que use llaves no lo convierte en primo de C: Rust las usa y su modelo de memoria no se parece a nada de esa familia. Busca varios indicios, no uno |
| Traducir palabra a palabra en vez de leer la intención | Se pierde el sentido del fragmento. Lee primero qué intenta lograr el bloque completo y luego baja al detalle |

## ❓ Preguntas frecuentes

**❓ ¿Esto reemplaza estudiar el lenguaje?** No para escribirlo bien. Escribir código idiomático exige conocer las convenciones, la biblioteca estándar y las trampas del lenguaje, y eso lleva tiempo. Pero para **leer** y entender —que es la mayor parte del trabajo real: revisar código ajeno, depurar un servicio que no es tuyo, evaluar una biblioteca— la lectura por analogía basta y se adquiere en una tarde.

**❓ ¿Y si el lenguaje no se parece a ninguno que conozca?** Entonces la analogía rinde poco y toca estudiar de verdad, lo cual también es información valiosa: saber que estás ante una familia nueva te evita el error de leerlo con las expectativas equivocadas. Prolog, APL o Haskell le hacen esto a quien solo conoce la familia de las llaves, y por eso la Parte 1 recorre las familias: para que ninguna te resulte del todo ajena.

**❓ ¿Dónde veo las familias?** En el [Atlas](../../../atlas/README.md) y a lo largo de toda la Parte 1, que dedica una clase a cada familia con sus rasgos distintivos y sus representantes. Cada clase de código del curso incluye además la sección "🧬 El concepto en la familia", que muestra el mismo concepto en primos fuera del núcleo: es lectura por analogía en dosis pequeñas y frecuentes.

**❓ ¿Cuánto tarda uno en leer un lenguaje nuevo de una familia conocida?** Menos de lo que parece, y cada vez menos. El primer salto dentro de una familia es el que más cuesta; el cuarto es casi inmediato, porque ya has aprendido a buscar el delta en vez de leerlo todo como si fuera nuevo.

## 🔗 Referencias

- G. Polya — *How to Solve It* (Princeton University Press), sobre resolver un problema recordando otro parecido ya resuelto.
- H. Abelson y G. J. Sussman — *Structure and Interpretation of Computer Programs* (2ª ed., MIT Press) — [gratis online](https://mitpress.mit.edu/9780262510875/).
- A. Hunt y D. Thomas — *The Pragmatic Programmer* (2ª ed., Addison-Wesley), sobre ampliar la cartera de conocimiento con un lenguaje nuevo al año.
- T. Cormen, C. Leiserson, R. Rivest y C. Stein — *Introduction to Algorithms* (4ª ed., MIT Press), sobre el pseudocódigo como forma neutral que cualquiera puede leer.

---

> [⏮️ Clase 012](../../parte-0-pensamiento-computacional-y-el-metodo-poliglota/012-casos-json-y-el-verificador-de-equivalencia/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 014 ⏭️](../../parte-0-pensamiento-computacional-y-el-metodo-poliglota/014-como-elegir-lenguaje-para-un-problema/README.md)
