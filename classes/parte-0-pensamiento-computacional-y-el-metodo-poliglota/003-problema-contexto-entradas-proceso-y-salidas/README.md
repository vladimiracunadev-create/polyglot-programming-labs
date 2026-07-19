# Clase 003 — Problema, contexto, entradas, proceso y salidas

> Parte **0 — Pensamiento computacional y el método políglota** · ⏱️ Duración estimada: **75 min** · Nivel: **Fundamentos**
> ✅ **Clase construida.**

---

## 🎯 Objetivo

Antes de escribir una sola línea de código hay que **modelar** el problema: decidir qué datos entran, qué resultado sale, bajo qué reglas ocurre la transformación y en qué contexto todo esto tiene sentido. Ese modelo —entrada, proceso, salida, contexto y restricciones— es independiente del lenguaje y es lo primero que define cada ficha del curso. Es también el paso que más gente se salta y el que más caro cobra saltárselo.

Polya lo puso como la primera y más importante de sus cuatro fases: *entender el problema*. Antes de trazar un plan hay que saber qué se busca, con qué datos se cuenta y qué condiciones deben cumplirse. El objetivo de hoy es darte un esqueleto fijo para hacer ese entendimiento explícito y verificable, de modo que dos personas que lean tu especificación resuelvan el *mismo* problema y no dos problemas parecidos que solo coinciden en el enunciado.

## 🧩 Situación

Un jefe de proyecto dice: "Calcula el total de una venta". Suena trivial, casi ofensivamente simple. Pero en cuanto intentas escribirlo aparecen las preguntas que el enunciado escondía: ¿el descuento viene como porcentaje (0.15) o como monto en dinero? ¿La cantidad puede ser cero, y en ese caso el total es 0.00 o es un error? ¿El total incluye impuesto o se calcula aparte? ¿Con cuántos decimales? Dos programadores que reciban esa frase sin modelarla escribirán dos programas distintos, ambos "correctos" según su propia interpretación, y el bug aparecerá en la integración, cuando ya sea caro. La especificación no es burocracia: es el contrato que evita construir la cosa equivocada con excelencia técnica.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Descomponer un problema en entradas, proceso y salidas.
2. Identificar el contexto y las restricciones que condicionan la solución.
3. Escribir la especificación de un problema sin mencionar ningún lenguaje.
4. Detectar ambigüedades del enunciado antes de programar, convirtiéndolas en decisiones explícitas.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Entradas | Qué datos recibe el programa y de qué tipo |
| 2 | Proceso | Qué transformación ocurre entre entrada y salida |
| 3 | Salidas | Qué produce y cómo se observa el resultado |
| 4 | Contexto y restricciones | Condiciones que limitan las soluciones válidas |

## 📖 Definiciones y características

Una **especificación** describe *qué* debe hacer un programa, nunca *cómo* lo hace. Es deliberadamente neutral al lenguaje: la misma especificación sirve para las diez implementaciones del núcleo, porque describe el contrato, no la maquinaria. Esta separación entre el qué y el cómo es una de las ideas más productivas de toda la ingeniería de software; Hunt y Thomas insisten en ella al hablar de programar cerca del dominio del problema, y es la razón por la que los `casos.json` del curso pueden validar a la vez a Python y a Rust: ambos responden al mismo contrato.

El modelo se articula en tres piezas y dos condiciones. La **entrada** es todo dato que el programa recibe; define el *dominio* del problema, y precisar su tipo y su rango (¿entero?, ¿real?, ¿positivo?) es la mitad del trabajo. El **proceso** es la transformación que convierte entrada en salida: la regla, la fórmula, el algoritmo en su forma más abstracta, todavía sin comprometerse con ninguna sintaxis. La **salida** es el resultado observable, y es lo que de verdad se verifica: si no puedes describir exactamente qué debería producirse, no puedes saber si tu programa funciona. Alrededor de estas tres piezas viven el **contexto** (dónde y para qué se usa: una caja de supermercado no es lo mismo que un sistema contable) y las **restricciones**, las condiciones que la solución debe respetar —rangos válidos, formato de salida, casos que deben tratarse de una manera concreta—. Las restricciones acotan el espacio de soluciones aceptables; sin ellas, cualquier respuesta que "más o menos" funcione parece válida.

Modelar así tiene un efecto medible: la enorme mayoría de los defectos de software no nacen de mala sintaxis, sino de un problema mal entendido. Cormen abre *Introduction to Algorithms* con la misma disciplina: antes de diseñar un algoritmo, se enuncia formalmente el *problema computacional* —su entrada y la relación que la salida debe satisfacer—. El algoritmo viene después; la especificación es el terreno sobre el que se levanta. Un programa que resuelve brillantemente el problema equivocado es un fracaso caro, y ninguna elegancia posterior lo rescata.

## 🔎 Ejemplo

Especifiquemos por completo "calcular el total de una venta", en forma neutral y verificable:

```text
Contexto:  punto de venta; el cajero introduce precio, cantidad y descuento.
Entrada:   precio_unitario  (real, >= 0)
           cantidad         (entero, >= 0)
           descuento        (real, entre 0 y 1; 0 = sin descuento)
Proceso:   subtotal = precio_unitario * cantidad
           total    = subtotal * (1 - descuento)
Salida:    "Total: <total con exactamente 2 decimales>"
Restricción / caso límite:
           cantidad = 0   ⇒  total = 0.00  (no es error)
           descuento = 1  ⇒  total = 0.00  (venta gratuita, válida)
```

Fíjate en lo que hemos ganado. El descuento quedó fijado como fracción, no como monto; el caso `cantidad = 0` se decidió explícitamente en vez de dejarlo al azar; el formato de salida (dos decimales) es parte del contrato. Esta especificación es la base literal de la clase 041, idéntica para los diez lenguajes. Ninguno de esos detalles habría sobrevivido si hubiéramos ido directo al teclado.

## ✍️ Práctica

Especifica por completo, sin escribir código, el problema "contar cuántas palabras tiene una frase". Usa el mismo esqueleto del ejemplo: contexto, entrada (¿la frase es una cadena?, ¿puede estar vacía?), proceso (¿qué separa una palabra de otra: espacios, signos de puntuación, varios espacios seguidos?), salida (un entero) y al menos dos casos límite (frase vacía, frase con espacios dobles al inicio). Verás que "contar palabras" esconde tantas decisiones como "calcular un total": ¿"hola, mundo" son dos palabras?, ¿y "   hola   "? Toma cada decisión de forma explícita. Esa es toda la clase.

## ⚠️ Errores comunes

| Síntoma / mensaje | Causa y cómo corregirlo |
|-------------------|--------------------------|
| Empezar a codificar y reescribir tres veces | Saltarse el modelo. Escribe entrada/proceso/salida antes de tocar el teclado |
| El programa falla en producción con datos raros | Olvidaste los casos límite. Enuméralos (vacío, 0, negativo, máximo) en la especificación |
| Dos personas implementan cosas distintas | Enunciado ambiguo no resuelto. Convierte cada ambigüedad en una decisión escrita |
| No sabes si tu programa "está bien" | No definiste la salida esperada. Sin salida precisa no hay corrección que comprobar |

## ❓ Preguntas frecuentes

**❓ ¿Por qué no empezar a programar directamente si el problema es fácil?** Porque "fácil" suele significar "aún no le he visto las aristas". La mayoría de los bugs nacen de un problema mal entendido, no de mala sintaxis. Cinco minutos de especificación ahorran horas de reescritura, y en los problemas triviales el modelo cabe en tu cabeza sin coste.

**❓ ¿La especificación cambia según el lenguaje?** No, y esa es justamente su virtud. Es la parte que permanece cuando todo lo demás cambia. Por eso un mismo `casos.json` puede validar las diez implementaciones: todas responden al mismo contrato de entrada y salida.

**❓ ¿Qué diferencia hay entre una restricción y un caso límite?** La restricción es una regla general que la solución debe cumplir ("el descuento está entre 0 y 1"); el caso límite es una entrada concreta en la frontera de esa regla ("descuento exactamente 1"). Los casos límite son la clase 005 y la semilla de los tests.

## 🔗 Referencias

- G. Polya — *How to Solve It* (Princeton University Press), primera fase: "Understanding the Problem".
- T. Cormen, C. Leiserson, R. Rivest y C. Stein — *Introduction to Algorithms* (4ª ed., MIT Press), cap. 1: definición formal de un problema.
- A. Hunt y D. Thomas — *The Pragmatic Programmer* (2ª ed., Addison-Wesley), sobre especificar el dominio.
- H. Abelson y G. J. Sussman — *Structure and Interpretation of Computer Programs* (2ª ed., MIT Press) — [gratis online](https://mitpress.mit.edu/9780262510875/).

---

> [⏮️ Clase 002](../../parte-0-pensamiento-computacional-y-el-metodo-poliglota/002-las-tres-clases-de-diferencia-sintactica-semantica-y-paradigmatica/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 004 ⏭️](../../parte-0-pensamiento-computacional-y-el-metodo-poliglota/004-descomposicion-y-reconocimiento-de-patrones/README.md)
