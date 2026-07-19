# Clase 004 — Descomposición y reconocimiento de patrones

> Parte **0 — Pensamiento computacional y el método políglota** · ⏱️ Duración estimada: **75 min** · Nivel: **Fundamentos**
> ✅ **Clase construida.**

---

## 🎯 Objetivo

Hay dos habilidades que separan a quien programa cosas pequeñas de quien construye sistemas: partir un problema grande en subproblemas manejables (**descomposición**) y notar cuándo un subproblema ya lo resolviste antes, quizá con otra forma (**reconocimiento de patrones**). Son las dos caras de una misma moneda: descomponer genera piezas, reconocer patrones evita resolver dos veces la misma pieza. Juntas hacen que la programación *escale*, que un problema el doble de grande no cueste el cuádruple de esfuerzo.

Esta es la segunda fase de Polya —*trazar un plan*— llevada a su forma más concreta. Un plan no es más que una descomposición: "para lograr esto, primero haré aquello, luego lo otro". Y una de las tácticas centrales de Polya para trazar planes es preguntarse "¿he visto este problema antes, o uno parecido?". Ese "parecido" es el reconocimiento de patrones. El objetivo de hoy es que conviertas ambas en un hábito deliberado, no en algo que a veces pasa por suerte.

## 🧩 Situación

Te piden "generar un reporte de ventas en PDF". Como enunciado es enorme y paraliza: no hay una función `generarReportePDF()` que baste. Pero descompuesto se vuelve tratable: (1) leer los datos de ventas de algún origen, (2) calcular los totales y agregados, (3) dar formato a esas cifras como texto o tabla, (4) exportar ese contenido a un archivo PDF. Cada una de esas cuatro piezas es un problema conocido, con solución probada, que puedes resolver y verificar por separado. Y hay un premio extra: la estructura "leer → transformar → escribir" que acabas de descubrir reaparece en casi todo el software que escribirás en tu vida. Reconocerla una vez te ahorra reinventarla mil.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Descomponer un problema en subproblemas independientes y verificables por separado.
2. Reconocer un patrón repetido y nombrarlo.
3. Explicar cómo la descomposición prefigura las funciones y los módulos.
4. Detectar cuándo dos partes distintas son en realidad el mismo patrón.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Descomposición | Divide y vencerás: partes pequeñas se resuelven y prueban solas |
| 2 | Reconocimiento de patrones | Reutilizar una solución conocida ahorra trabajo y errores |
| 3 | De subproblema a función | La descomposición prefigura la modularidad (Parte 5) |

## 📖 Definiciones y características

**Descomponer** es dividir un problema en subproblemas más simples, cada uno resoluble y verificable por separado. Su virtud es doble: reduce la carga mental —solo piensas una pieza a la vez— y localiza los errores —si algo falla, sabes en qué pieza mirar—. Cormen dedica un capítulo entero a la técnica de **divide y vencerás**, que es descomposición en su forma algorítmica más pura: partir el problema en subproblemas del mismo tipo, resolverlos y combinar sus resultados (así funcionan *merge sort* o la búsqueda binaria). Pero la descomposición no exige que las partes sean del mismo tipo; basta con que cada una sea más pequeña que el todo y se pueda atacar por su cuenta.

Un **patrón** es una estructura de solución que reaparece en problemas distintos. "Filtrar los elementos que cumplen una condición", "acumular un total recorriendo una colección", "buscar el primero que satisface algo": estas formas surgen una y otra vez bajo disfraces diferentes. Reconocer que un subproblema nuevo tiene la forma de un patrón conocido es lo que evita reinventar la rueda —y, más importante, reinventarla con los mismos bugs que ya alguien resolvió—. Polya llama a esto trabajar por analogía, y lo considera una de las herramientas más potentes del que resuelve problemas: la mayoría de los problemas "nuevos" son variaciones de problemas viejos.

La conexión entre ambas ideas y el código es directa y es una de las columnas del curso: **cada subproblema tiende a convertirse en una función, y cada patrón, en una función reutilizable**. La *abstracción de subproblema* —tratar una pieza ya resuelta como una caja negra de la que solo importa qué hace, no cómo— es exactamente lo que SICP identifica como el mecanismo que permite construir programas grandes: encapsulas una solución, le pones nombre y la usas como si fuera una operación primitiva. Descomponer bien hoy es tener funciones bien diseñadas mañana (Parte 5), y reconocer patrones hoy es anticipar el `map`/`filter`/`reduce` de la Parte 4 y los patrones de diseño de la Parte 9.

## 🔎 Ejemplo

Descompongamos "calcular el promedio de las notas aprobadas de un curso" y nombremos el patrón de cada pieza:

```text
Problema: promedio de las notas >= 4 (escala de 1 a 7)

Descomposición:
  1. filtrar las notas que son >= 4        → patrón: FILTRAR
  2. sumar las notas que quedaron          → patrón: REDUCIR (acumular)
  3. contar cuántas quedaron               → patrón: CONTAR
  4. dividir la suma entre la cuenta       → operación final

Caso límite: si ninguna nota es >= 4, la cuenta es 0
             ⇒ decidir qué devolver (¿0? ¿"sin aprobados"?)
```

Tres de las cuatro piezas son patrones con nombre propio —filtrar, reducir, contar— que reaparecerán literalmente en la Parte 4 como `filter`, `reduce` y `count`/`len`. La cuarta pieza esconde un caso límite (división entre cero si no hay aprobados) que la descomposición hace visible: al separar "contar" de "dividir", saltar el peligro de dividir entre cero se vuelve imposible de ignorar.

## ✍️ Práctica

Descompón el problema "corregir automáticamente un test de opción múltiple" en tres o cuatro subproblemas y, junto a cada uno, nombra su patrón. Piensa en voz alta: necesitas comparar las respuestas del alumno con las correctas (¿qué patrón es comparar par a par dos listas?), contar los aciertos (¿cuál cuenta?), quizá calcular una nota a partir del conteo. Cuando termines, subraya cuáles de esos patrones ya aparecieron en el ejemplo del promedio. Si descubres que "contar aciertos" es el mismo patrón CONTAR que ya viste, has hecho reconocimiento de patrones de verdad: eso es el objetivo.

## ⚠️ Errores comunes

| Síntoma / mensaje | Causa y cómo corregirlo |
|-------------------|--------------------------|
| Una sola función gigante que hace de todo | No descompusiste. Extrae cada subproblema a su propia función con nombre |
| Copiar y pegar el mismo bloque en tres sitios | No reconociste el patrón repetido. Nómbralo y conviértelo en una función reutilizable |
| Descomponer hasta el infinito, funciones de una línea inútiles | Descomposición sin criterio. Detente cuando cada pieza quepa en tu cabeza y se pruebe sola |
| No sabes por dónde empezar un problema grande | Intentas resolverlo entero de golpe. Pártelo primero; ataca una pieza después |

## ❓ Preguntas frecuentes

**❓ ¿Hasta dónde debo descomponer?** Hasta que cada parte quepa cómodamente en tu cabeza y se pueda probar por sí sola. Ni menos (funciones que hacen cinco cosas) ni más (funciones de una línea que solo añaden ruido). El criterio es humano, no mecánico: si puedes explicar la pieza en una frase, tiene el tamaño correcto.

**❓ ¿Los "patrones" de esta clase son los "patrones de diseño" famosos?** No, o todavía no. Aquí hablamos de estructuras de solución elementales: filtrar, acumular, buscar. Los patrones de diseño formales (Observer, Factory, Strategy...) son construcciones mayores que llegan en la Parte 9. Pero el músculo es el mismo: reconocer que "esto ya lo vi con otra forma".

**❓ ¿Descomponer no hace el programa más lento por tantas funciones?** En la práctica, casi nunca: los compiladores e intérpretes optimizan bien las llamadas, y la claridad que ganas vale mucho más que los nanosegundos que podrías perder. Primero descompón para entender; optimiza solo donde midas que hace falta (clase 009).

## 🔗 Referencias

- G. Polya — *How to Solve It* (Princeton University Press), fase "Devising a Plan" y el trabajo por analogía.
- T. Cormen, C. Leiserson, R. Rivest y C. Stein — *Introduction to Algorithms* (4ª ed., MIT Press), cap. de "divide y vencerás".
- H. Abelson y G. J. Sussman — *Structure and Interpretation of Computer Programs* (2ª ed., MIT Press), sobre abstracción — [gratis online](https://mitpress.mit.edu/9780262510875/).
- A. Hunt y D. Thomas — *The Pragmatic Programmer* (2ª ed., Addison-Wesley), principio DRY.

---

> [⏮️ Clase 003](../../parte-0-pensamiento-computacional-y-el-metodo-poliglota/003-problema-contexto-entradas-proceso-y-salidas/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 005 ⏭️](../../parte-0-pensamiento-computacional-y-el-metodo-poliglota/005-abstraccion-restricciones-y-casos-limite/README.md)
