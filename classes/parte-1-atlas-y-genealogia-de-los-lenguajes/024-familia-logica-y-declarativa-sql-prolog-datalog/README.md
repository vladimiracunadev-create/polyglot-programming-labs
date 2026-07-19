# Clase 024 — Familia lógica y declarativa: SQL, Prolog, Datalog

> Parte **1 — Atlas y genealogía de los lenguajes** · ⏱️ Duración estimada: **75 min** · Nivel: **Fundamentos**
> ✅ **Clase construida.**

---

## 🎯 Objetivo

Conocer los lenguajes en los que describes **QUÉ** quieres, no **CÓMO** obtenerlo. **SQL** (en el núcleo del curso) describe conjuntos de datos y deja que el motor decida cómo recorrerlos; **Prolog** describe hechos y reglas y deja que un motor de inferencia deduzca las respuestas. Es el salto **paradigmático** más grande respecto de todos los lenguajes imperativos que hemos visto: aquí no hay bucles ni variables que se reasignan, hay descripciones de la solución.

Esto importa porque el paradigma declarativo obliga a un cambio de mentalidad que, una vez adquirido, simplifica clases enteras de problemas. Sebesta dedica un capítulo a la programación lógica y otro a las bases de datos y SQL; Van Roy y Haridi construyen su libro alrededor de la idea de que la programación declarativa es el punto de partida más limpio, sobre el que los demás paradigmas añaden complejidad (estado, concurrencia). Entender SQL y Prolog como parientes revela que "describir en vez de ordenar" es una idea con raíces profundas en la lógica matemática.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Distinguir programación declarativa de imperativa con un ejemplo propio.
2. Explicar el modelo de SQL (consultas sobre conjuntos) y el de Prolog (hechos, reglas, unificación).
3. Reconocer cuándo el enfoque declarativo simplifica un problema y cuándo estorba.
4. Situar Datalog como puente entre Prolog y las consultas de datos.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Declarativo vs. imperativo | Describir el resultado vs. describir los pasos |
| 2 | SQL: consultas sobre datos | El motor y su optimizador deciden el "cómo" |
| 3 | Prolog: hechos y reglas | Deducción por unificación y backtracking |
| 4 | Datalog | Subconjunto de Prolog para consultas de datos |
| 5 | Cuándo usarlo | Problemas de "describir un resultado" |

## 📖 Definiciones y características

El paradigma **declarativo** invierte la relación habitual entre el programador y la máquina. En un lenguaje imperativo, tú escribes la receta paso a paso: inicializa un acumulador, recorre la lista, comprueba una condición, actualiza el acumulador. En uno declarativo, describes la propiedad que debe cumplir el resultado y dejas que el sistema encuentre cómo producirlo. Van Roy y Haridi lo definen con precisión: un programa declarativo especifica *qué* se computa, no *cómo*; el "cómo" es responsabilidad del intérprete o del motor. Esta separación tiene una ventaja enorme —el sistema puede optimizar el "cómo" mejor que tú— y un coste —pierdes el control fino sobre la ejecución—.

**SQL** (Structured Query Language) nació en IBM a mediados de los 70, a partir del modelo relacional que **Edgar F. Codd** había formalizado en 1970 sobre la teoría de conjuntos y la lógica de predicados. Cuando escribes una consulta SQL, no le dices a la base de datos que recorra tablas ni en qué orden: describes el conjunto de filas que quieres —qué columnas, de qué tablas, con qué condiciones, agrupadas cómo— y el **optimizador de consultas** del motor decide el plan de ejecución real (qué índices usar, en qué orden unir las tablas, cómo agrupar). Dos consultas escritas de forma distinta pero equivalentes pueden ejecutarse con el mismo plan, porque lo que cuenta es *qué* pides, no *cómo* lo escribes. Por eso, en el verificador de equivalencia del curso, SQL se trata como "ilustrativo": es declarativo y no encaja en el mismo molde de stdin/stdout que los lenguajes imperativos.

**Prolog** (Alain Colmerauer y Robert Kowalski, 1972) lleva el declarativismo aún más lejos, al terreno de la **programación lógica**. Un programa Prolog es un conjunto de **hechos** (`padre(juan, maria).`) y **reglas** (`abuelo(X, Z) :- padre(X, Y), padre(Y, Z).`, que se lee "X es abuelo de Z si X es padre de algún Y que es padre de Z"). No hay flujo de control explícito: tú planteas una consulta y el motor la resuelve mediante dos mecanismos. La **unificación** hace coincidir términos, ligando variables a valores para satisfacer los objetivos; y el **backtracking** deshace decisiones y explora alternativas cuando un camino no lleva a solución. El resultado es que el mismo programa puede responder preguntas en direcciones distintas —"¿quién es abuelo de María?" o "¿de quién es abuelo Juan?"— sin escribir código adicional. **Datalog** es un subconjunto de Prolog, sin ciertas construcciones problemáticas, que se usa para consultas de datos deductivas y análisis de programas. Sebesta subraya que, aunque la programación lógica ocupa hoy un nicho, sus ideas laten en los motores de reglas, en la verificación y en el propio SQL.

- **Declarativo** — paradigma en el que se describe el resultado deseado, no el algoritmo. Clave: el motor decide el "cómo".
- **SQL** — años 70 (IBM, sobre el modelo relacional de Codd), consulta de bases relacionales. Clave: núcleo del curso; declarativo sobre conjuntos.
- **Prolog** — 1972 (Colmerauer, Kowalski), programación lógica. Clave: describes hechos y reglas; el motor deduce por unificación y backtracking.
- **Unificación** — mecanismo que hace coincidir términos ligando variables para satisfacer una consulta. Clave: motor de la deducción en Prolog.

## 🧩 Situación

Para obtener "los clientes con más de tres pedidos", un lenguaje imperativo te obliga a escribir el algoritmo: crear un diccionario, recorrer todos los pedidos, contar por cliente, y luego recorrer el diccionario filtrando los que superen tres. Son quince líneas y cuatro decisiones sobre el "cómo". En SQL lo dices en una frase —`SELECT cliente FROM pedidos GROUP BY cliente HAVING COUNT(*) > 3`— y el motor se encarga de todo: elige el índice, decide el orden, agrupa como mejor le convenga. Además, si mañana la tabla crece a millones de filas, tu consulta no cambia; el optimizador se adapta. Ese cambio de mentalidad —de dar órdenes a describir resultados— es el corazón del paradigma declarativo.

## 🔎 Ejemplo

Un mismo objetivo, tres mentalidades:

```text
Imperativo (pseudocódigo):
  crea contador vacío
  PARA cada pedido: contador[pedido.cliente] += 1
  PARA cada cliente en contador: SI contador[cliente] > 3, añadir a resultado

Declarativo (SQL):
  SELECT cliente FROM pedidos GROUP BY cliente HAVING COUNT(*) > 3;

Lógico (Prolog):
  abuelo(X, Z) :- padre(X, Y), padre(Y, Z).
  ?- abuelo(juan, Quien).      % el motor deduce todos los nietos de Juan
```

El **delta** no es sintáctico, es de paradigma. El imperativo enumera pasos y estados intermedios; el SQL describe el conjunto buscado y calla sobre el método; el Prolog ni siquiera dirige la búsqueda: declara la relación "abuelo" y deja que el motor la recorra en la dirección que pidas. Cuanto más a la derecha, menos dices sobre el "cómo" y más confías en el sistema.

## ✍️ Práctica

Toma un problema cotidiano —por ejemplo, "los alumnos que aprobaron todas las asignaturas"— y escríbelo primero como una frase que describa *qué* quieres, sin mencionar bucles ni pasos. Nota que acabas de "pensar declarativamente". Luego bosqueja cómo lo harías con bucles y compara cuántas decisiones sobre el "cómo" te ahorra la versión declarativa.

## ⚠️ Errores comunes

- **Programar SQL como si fuera imperativo** → causa: querer controlar el orden y el método de ejecución → solución: confiar en el optimizador y describir solo el "qué"; medir antes de intentar "ayudarlo".
- **Creer que lo declarativo sirve para todo** → causa: forzarlo donde el control paso a paso es esencial → solución: reservarlo para problemas de "describir un resultado", no para lógica de control fina.
- **Ignorar el backtracking de Prolog** → causa: esperar una sola respuesta → solución: entender que el motor explora todas las soluciones posibles y deshace decisiones automáticamente.

## ❓ Preguntas frecuentes

- **¿SQL es "de verdad" un lenguaje de programación?** Es un lenguaje declarativo especializado en datos; con extensiones procedurales es Turing-completo, pero su fuerte es consultar conjuntos, no programación general.
- **¿Dónde se usa Prolog hoy?** En IA simbólica, sistemas expertos, análisis de lenguaje natural y verificación; es un nicho, pero muy potente cuando el problema es "deducir a partir de reglas".
- **¿Qué relación hay entre SQL y Prolog?** Ambos descienden de la lógica de predicados; SQL sobre el modelo relacional de Codd, Prolog sobre la resolución lógica. Son primos declarativos por rama distinta.

## 🔗 Referencias

- C. J. Date — *SQL and Relational Theory* (3ª ed., O'Reilly).
- R. W. Sebesta — *Concepts of Programming Languages* (12ª ed., Pearson), cap. 16 "Logic Programming Languages".
- P. Van Roy y S. Haridi — *Concepts, Techniques, and Models of Computer Programming* (MIT Press), cap. 9 (programación relacional).
- M. L. Scott — *Programming Language Pragmatics* (4ª ed., Morgan Kaufmann).

---

> [⏮️ Clase 023](../../parte-1-atlas-y-genealogia-de-los-lenguajes/023-familia-lisp-scheme-racket-clojure-emacs-lisp/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 025 ⏭️](../../parte-1-atlas-y-genealogia-de-los-lenguajes/025-familia-concurrente-actor-erlang-elixir-y-el-csp-de-go/README.md)
