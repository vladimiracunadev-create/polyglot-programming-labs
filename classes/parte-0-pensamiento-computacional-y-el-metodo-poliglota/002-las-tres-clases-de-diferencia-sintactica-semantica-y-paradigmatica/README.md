# Clase 002 — Las tres clases de diferencia: sintáctica, semántica y paradigmática

> Parte **0 — Pensamiento computacional y el método políglota** · ⏱️ Duración estimada: **75 min** · Nivel: **Fundamentos**
> ✅ **Clase construida.**

---

## 🎯 Objetivo

Cada vez que este curso pone dos lenguajes lado a lado, aparece una pregunta: ¿en qué se diferencian *realmente*? La respuesta nunca es "en todo" ni "en nada". Toda diferencia entre dos lenguajes cae en una de **tres clases**, y saber distinguirlas es la brújula que usarás en cada comparación del programa. Una diferencia puede ser **sintáctica** (se escribe distinto pero significa lo mismo), **semántica** (cambia lo que ocurre: el tipo, la memoria, el comportamiento) o **paradigmática** (invita a estructurar la solución de otra manera).

El objetivo de hoy es que puedas mirar cualquier par de fragmentos y clasificar su diferencia con seguridad. Esto no es taxonomía por deporte: confundir una clase con otra es la causa número uno de bugs al portar código. Quien cree que todo es sintáctico traduce mecánicamente, cambiando llaves por dos puntos, y se estrella contra las diferencias semánticas que compilan pero se comportan distinto. Quien ignora el paradigma escribe código que funciona pero que ningún experto del lenguaje destino reconocería como natural.

## 🧩 Situación

Un desarrollador porta un bucle de JavaScript a Rust. Cambia los `var` por `let`, ajusta las llaves, quita algún `;` de más. Compila y celebra. Pero el programa se comporta distinto: en una línea pasó un valor a una función y luego intentó volver a usarlo, y en Rust ese valor se **movió** —dejó de ser suyo— mientras que en JavaScript seguía disponible. Donde esperaba un dato tiene un error del compilador sobre un valor "usado tras moverse", algo que en JavaScript era perfectamente válido. La diferencia que lo mordió no era sintáctica, aunque él la trató como tal: era **semántica**. Toda la clase de hoy existe para que reconozcas ese momento *antes* de que te cueste una tarde de depuración.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Clasificar una diferencia entre lenguajes como sintáctica, semántica o paradigmática.
2. Dar ejemplos propios de cada una de las tres clases.
3. Explicar por qué confundirlas conduce a traducir mecánicamente en vez de programar idiomáticamente.
4. Anticipar cuál de las tres clases es la más peligrosa al portar código y por qué.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Diferencia sintáctica | La más superficial: solo cambia cómo se escribe |
| 2 | Diferencia semántica | Cambia qué ocurre: tipos, mutabilidad, memoria, errores |
| 3 | Diferencia paradigmática | Cambia cómo se piensa la solución |
| 4 | Traducción vs. idiomática | Por qué copiar sintaxis produce código antinatural |

## 📖 Definiciones y características

Una **diferencia sintáctica** es distinta escritura con el mismo significado esencial. Es la más fácil de salvar porque es puramente superficial: `for (i=0; i<n; i++)` en C y `for i in range(n)` en Python describen el mismo bucle con vocabularios distintos. La sintaxis es la *gramática* del lenguaje, las reglas de cómo se combinan los símbolos. Robert Sebesta, en *Concepts of Programming Languages*, la trata como la capa más externa de un lenguaje, la que se aprende y se olvida con menos coste. Si dos fragmentos producen el mismo resultado y solo difieren en puntuación, palabras clave u orden cosmético, la diferencia es sintáctica.

Una **diferencia semántica** es distinto *comportamiento observable* con, a veces, la misma escritura. La semántica es el *significado*: qué hace realmente el programa cuando corre. Aquí viven las trampas. `x = y` copia un valor en C pero mueve la propiedad en Rust; `a == b` compara valor en Python pero identidad del objeto para objetos en Java; una división entre enteros trunca en C y Go pero da un flotante en Python 3. La escritura puede ser casi idéntica y el resultado, opuesto. Por eso la diferencia semántica es la más peligrosa: el código compila, parece correcto en la demo y falla en un caso que no probaste. Reconocerla exige preguntarse siempre, más allá de "¿se escribe igual?", la pregunta que de verdad importa: "¿*hace* lo mismo?".

Una **diferencia paradigmática** cambia la forma misma de estructurar la solución. Un paradigma es un modelo mental de cómo se construye un programa: imperativo (describir los pasos), funcional (describir transformaciones de datos), declarativo (describir el resultado deseado y dejar que el sistema encuentre el cómo). Recorrer una lista con un bucle es imperativo; pedir el resultado con un `SELECT` de SQL es declarativo. No es que uno esté mal: es que piensan el problema de manera distinta. Van Roy y Haridi organizan buena parte de las ciencias de la computación alrededor de esta idea de modelos de cómputo, y SICP dedica su arquitectura a mostrar que un mismo problema admite formulaciones radicalmente distintas según el paradigma. De aquí sale el concepto de **código idiomático**: la solución escrita como la escribiría un experto de ese lenguaje, aprovechando su paradigma en vez de imponerle el de otro. Traducir palabra por palabra desde el paradigma equivocado produce código que funciona pero que se lee como un texto pasado por diccionario: gramaticalmente posible, humanamente extraño.

## 🔎 Ejemplo

Las tres clases de diferencia, una debajo de otra, sobre el mismo terreno:

```text
Sintáctica:    for (i=0; i<n; i++) { ... }     vs   for i in range(n): ...
               mismo bucle, otra escritura, mismo comportamiento

Semántica:     x = y  (copia el valor, en C)   vs   x = y  (mueve, en Rust)
               misma escritura, distinto comportamiento observable

Paradigmática: recorrer la lista con un bucle sumando cada elemento
               vs   SELECT SUM(precio) FROM ventas
               distinta forma de estructurar la misma tarea
```

Fíjate en el patrón: la sintáctica cambia el *aspecto* y nada más; la semántica puede mantener el aspecto y cambiar el *fondo*; la paradigmática cambia la *estrategia* entera. Cuando compares lenguajes en el resto del curso, esta escalera será tu diagnóstico.

## ✍️ Práctica

Analiza estos tres pares y clasifica cada uno. No basta con acertar: escribe en una frase *por qué*.

1. `println!("hola")` en Rust frente a `print("hola")` en Python.
2. En Java, `a == b` para dos objetos `String` con el mismo texto, frente a Python, donde `a == b` compara el contenido.
3. Sumar los pares de una lista con un bucle `for` que acumula, frente a hacerlo con `filter` y luego `sum` sobre la colección.

Las respuestas son, respectivamente: sintáctica (solo cambia el nombre de la operación de salida), semántica (Java compara identidad de objeto y puede dar `false` aun con el mismo texto; Python compara valor) y paradigmática (imperativo acumulador frente a estilo funcional de transformación). Si dudaste en el segundo, es normal: la semántica es precisamente la que engaña.

## ⚠️ Errores comunes

| Síntoma / mensaje | Causa y cómo corregirlo |
|-------------------|--------------------------|
| Portar código cambiando solo la sintaxis y que "casi" funcione | Asumir que toda diferencia es sintáctica. Verifica tipos, memoria y mutabilidad antes de dar por buena la traducción |
| Código que compila pero da otro resultado | Diferencia semántica no detectada. Compara comportamientos con casos de prueba, no solo la compilación |
| Escribir todos los lenguajes con el mismo estilo | Ignorar el paradigma del lenguaje destino. Adapta la estructura, no solo las palabras |
| Insistir en usar bucles donde el lenguaje pide otra cosa (p. ej. SQL) | Forzar un paradigma ajeno. Pregúntate cuál es la forma natural del lenguaje |

## ❓ Preguntas frecuentes

**❓ ¿Cuál de las tres es la más peligrosa?** La semántica, sin duda. La sintáctica te detiene con un error de compilación evidente; la paradigmática produce código feo pero honesto. La semántica, en cambio, deja pasar código que parece correcto y falla en producción, en el caso que no probaste. Es la que justifica el verificador de equivalencia de la clase 012.

**❓ ¿La diferencia paradigmática se puede evitar siempre?** A veces sí: casi todos los lenguajes admiten un estilo imperativo, así que podrías escribir Python "a la C" con índices y bucles manuales. Podrías, pero perderías la ventaja del lenguaje destino. Evitar el paradigma es como conducir en primera todo el viaje: llegas, pero desaprovechas el motor.

**❓ ¿Una misma diferencia puede tener varias capas?** Sí. `map` en JavaScript y en Haskell se escriben parecido (algo sintáctico), pero Haskell es perezoso y no evalúa hasta que hace falta (algo semántico), y todo el estilo funcional que lo rodea es paradigmático. Cuando ocurra, nombra la capa más profunda que importe para tu tarea.

## 🔗 Referencias

- R. W. Sebesta — *Concepts of Programming Languages* (Pearson), caps. de sintaxis y semántica.
- H. Abelson y G. J. Sussman — *Structure and Interpretation of Computer Programs* (2ª ed., MIT Press) — [gratis online](https://mitpress.mit.edu/9780262510875/).
- A. Hunt y D. Thomas — *The Pragmatic Programmer* (2ª ed., Addison-Wesley), sobre escribir código idiomático.
- P. Van Roy y S. Haridi — *Concepts, Techniques, and Models of Computer Programming* (MIT Press), sobre paradigmas.

---

> [⏮️ Clase 001](../../parte-0-pensamiento-computacional-y-el-metodo-poliglota/001-que-es-programar-y-por-que-comparar-lenguajes-la-tesis-poliglota/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 003 ⏭️](../../parte-0-pensamiento-computacional-y-el-metodo-poliglota/003-problema-contexto-entradas-proceso-y-salidas/README.md)
