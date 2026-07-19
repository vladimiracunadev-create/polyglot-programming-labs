# Clase 009 — Complejidad y eficiencia: intuición de coste

> Parte **0 — Pensamiento computacional y el método políglota** · ⏱️ Duración estimada: **75 min** · Nivel: **Fundamentos**
> ✅ **Clase construida.**

---

## 🎯 Objetivo

Dos programas pueden dar exactamente el mismo resultado y, sin embargo, uno ser mil veces más lento que el otro cuando los datos crecen. La pregunta que separa a un programador de un ingeniero no es "¿funciona?", sino "¿cuánto **cuesta** cuando la entrada crece?". El objetivo de hoy es desarrollar la *intuición* de coste: estimar cómo escala un algoritmo en tiempo y en memoria a medida que la entrada se agranda, usando la notación **O-grande** de forma práctica, sin ahogarse en matemáticas.

Esto no es teoría por deporte. Es la razón por la que un programa que va perfecto con cien datos en tu portátil se derrumba con diez millones en producción. Cormen dedica el capítulo 3 de *Introduction to Algorithms* a exactamente esto —el crecimiento de las funciones— porque es el lenguaje universal con que los programadores comparan soluciones sin depender de una máquina concreta. Un cronómetro te dice qué es rápido *en tu ordenador, hoy*; la notación O te dice qué será rápido en *cualquier* ordenador cuando los datos crezcan. La segunda es la que importa para decidir.

## 🧩 Situación

Dos funciones ordenan una lista de nombres. Con diez elementos, ambas terminan en un parpadeo; en la demo son indistinguibles y el equipo elige cualquiera. Meses después, con la base de datos real de un millón de usuarios, una ordena en una fracción de segundo y la otra tarda horas y bloquea el servidor. La diferencia no era visible en la demo porque el coste solo se manifiesta *al escalar*: una era `O(n log n)` y la otra `O(n²)`, y esa brecha, invisible con `n = 10`, se vuelve un abismo con `n = 1 000 000`. Elegir el algoritmo por cómo se comporta en la demo, en lugar de por su orden de complejidad, es una de las decisiones que más caro cuestan y más tarde se descubren.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Estimar el orden de crecimiento —O(1), O(log n), O(n), O(n²)— de un algoritmo simple.
2. Comparar dos soluciones por su coste, no solo por si funcionan.
3. Reconocer el bucle anidado como fuente típica de O(n²).
4. Distinguir coste en tiempo de coste en memoria, y ver cuándo se intercambian.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Crecimiento con la entrada | Lo que importa es cómo escala, no el tiempo en un caso |
| 2 | O(1), O(n), O(n²), O(log n) | El vocabulario para comparar costes |
| 3 | Tiempo vs. memoria | A veces se cambia uno por el otro |

## 📖 Definiciones y características

La **complejidad temporal** describe cómo crece el número de operaciones de un algoritmo en función del tamaño `n` de la entrada. La palabra clave es *crece*: no medimos segundos, medimos la *forma* de la curva. Un algoritmo que hace un número fijo de operaciones sin importar `n` es de coste **constante**, `O(1)` —acceder a `lista[i]` cuesta lo mismo con diez o con diez millones de elementos—. Uno que recorre la entrada una vez es **lineal**, `O(n)` —buscar en una lista desordenada—. Uno que en cada paso descarta la mitad de lo que queda es **logarítmico**, `O(log n)`, asombrosamente eficiente: la búsqueda binaria encuentra un elemento entre un millón en unas veinte comparaciones. Y uno que compara cada elemento con todos los demás es **cuadrático**, `O(n²)`, el que se derrumba al escalar.

La notación **O-grande** es una *cota superior* del crecimiento: dice "este algoritmo no crece más rápido que esto" y describe el comportamiento en el peor caso cuando `n` se hace grande. Su gracia es que ignora deliberadamente los detalles que no escalan —las constantes, los términos menores—, porque para `n` grande solo domina el término mayor. Un algoritmo que hace `3n + 100` operaciones es `O(n)`: el `3` y el `100` no cambian la *forma* del crecimiento. Cormen formaliza esto en el capítulo 3, pero la intuición que necesitas hoy es más simple: **cuenta cuántas veces se repite el trabajo cuando la entrada crece**. Un bucle sobre la entrada, `O(n)`. Un bucle dentro de otro bucle, ambos sobre la entrada, `O(n²)` —y por eso el **bucle anidado** es la señal de alarma que hay que vigilar—. Partir el problema por la mitad en cada paso, `O(log n)`.

El coste tiene dos dimensiones, y a veces se negocian entre sí. La **complejidad temporal** mide operaciones; la **complejidad espacial** mide memoria. Con frecuencia se puede gastar más memoria para ganar tiempo o al revés: guardar resultados ya calculados en una tabla (más memoria) evita recalcularlos (menos tiempo). Este intercambio —el clásico *space-time tradeoff*— es una decisión de ingeniería, no una respuesta única. Y hay una advertencia que Cormen y toda la disciplina repiten: **la eficiencia se razona antes de optimizar**. Optimizar sin medir es atacar a ciegas; primero identificas el orden dominante —el cuello de botella real— y solo entonces inviertes esfuerzo donde de verdad cambia la curva. Optimizar un `O(n)` mientras ignoras un `O(n²)` al lado es pulir la manija de una puerta que se está incendiando.

## 🔎 Ejemplo

Los órdenes más comunes, cada uno con una operación cotidiana que lo produce:

```text
Operación                              Trabajo al crecer n     Orden
-------------------------------------  ----------------------  --------
Acceder a lista[i]                     siempre 1 paso          O(1)
Buscar en una lista NO ordenada        recorrer todo           O(n)
Buscar en una lista ordenada           partir por la mitad     O(log n)
Ordenar bien (merge/quicksort)         ~n pasadas de log n     O(n log n)
Comparar todos los pares (bucle x2)    n por cada uno de n     O(n²)
```

Fíjate en el salto entre `O(n)` y `O(n²)`: con `n = 1000`, uno hace mil operaciones y el otro un millón. Con `n = 1 000 000`, uno hace un millón y el otro un billón. La misma tarea, la misma máquina, y una tarda milisegundos donde la otra tarda horas. Ese salto es invisible en `n = 10` y decisivo en producción, y toda la clase existe para que lo veas *antes* de elegir.

## ✍️ Práctica

Analiza el orden de este algoritmo sin ejecutarlo: "para cada persona de una lista de `n` personas, compararla con todas las demás para ver si hay nombres repetidos". La pista está en las palabras "para cada... con todas las demás": es un bucle dentro de un bucle, ambos recorriendo las `n` personas, así que el trabajo es proporcional a `n × n`, es decir, `O(n²)`. Ahora la parte de ingeniería: piensa cómo bajarlo a `O(n)` usando más memoria —por ejemplo, guardando los nombres ya vistos en un conjunto y preguntando si un nombre nuevo ya está—. Ese rediseño cambia el orden de la curva, no solo la constante, y es la clase de mejora que de verdad importa. Habrás hecho un *space-time tradeoff* consciente.

## ⚠️ Errores comunes

| Síntoma / mensaje | Causa y cómo corregirlo |
|-------------------|--------------------------|
| "En mi máquina va rápido" y en producción no | Mediste con entrada pequeña. Razona el orden; el coste solo se nota al escalar |
| Optimizas y no mejora nada | Atacaste algo que no era el cuello de botella. Identifica primero el orden dominante |
| No ves por qué un algoritmo es lento | Bucle anidado escondido. Búscalo: es la fuente típica de O(n²) |
| Cuentas constantes y términos menores | Te ahogas en detalles que no escalan. Quédate solo con el término dominante |
| El programa se queda sin memoria | Ignoraste la complejidad espacial. Mide también la memoria, no solo el tiempo |

## ❓ Preguntas frecuentes

**❓ ¿Siempre gana el algoritmo de menor O?** Para entradas grandes, sí. Para entradas pequeñas, no necesariamente: un `O(n²)` simple, con constantes bajas, puede ganarle a un `O(n log n)` sofisticado cuando `n` es diminuto. Por eso muchas bibliotecas de ordenación usan un método simple para tramos pequeños y uno avanzado para los grandes. La notación O describe el comportamiento *al escalar*; para `n` diminuto, las constantes que O ignora pueden decidir.

**❓ ¿Necesito las matemáticas formales de límites y demostraciones?** No en este curso. Basta la intuición: contar cuántas veces se repite el trabajo cuando `n` crece. Un bucle simple, lineal; un bucle anidado, cuadrático; partir por la mitad, logarítmico. La formalización rigurosa está en Cormen si la quieres, pero la decisión práctica se toma con la intuición.

**❓ ¿Debo optimizar siempre al máximo?** No: "primero haz que funcione, luego que sea rápido, y solo donde midas que hace falta". Optimizar código que no es el cuello de botella añade complejidad sin beneficio. La complejidad importa para *elegir el algoritmo correcto* desde el diseño, no para microoptimizar cada línea.

## 🔗 Referencias

- T. Cormen, C. Leiserson, R. Rivest y C. Stein — *Introduction to Algorithms* (4ª ed., MIT Press), cap. 3: crecimiento de funciones y notación asintótica.
- H. Abelson y G. J. Sussman — *Structure and Interpretation of Computer Programs* (2ª ed., MIT Press), órdenes de crecimiento — [gratis online](https://mitpress.mit.edu/9780262510875/).
- A. Hunt y D. Thomas — *The Pragmatic Programmer* (2ª ed., Addison-Wesley), sobre estimar y no optimizar prematuramente.
- G. Polya — *How to Solve It* (Princeton University Press), buscar una solución mejor tras la primera.

---

> [⏮️ Clase 008](../../parte-0-pensamiento-computacional-y-el-metodo-poliglota/008-trazado-manual-y-ejecucion-simbolica/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 010 ⏭️](../../parte-0-pensamiento-computacional-y-el-metodo-poliglota/010-legibilidad-estilo-e-idiomatica/README.md)
