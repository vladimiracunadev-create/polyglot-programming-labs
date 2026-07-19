# Clase 022 — Familia funcional tipada (ML): Haskell, OCaml, F# y la influencia en Rust

> Parte **1 — Atlas y genealogía de los lenguajes** · ⏱️ Duración estimada: **75 min** · Nivel: **Fundamentos**
> ✅ **Clase construida.**

---

## 🎯 Objetivo

Conocer la familia **ML**: lenguajes funcionales con sistemas de tipos potentes e inferencia automática. Ninguno de sus miembros clásicos —Haskell, OCaml, Standard ML— está en el núcleo del curso, pero su **influencia** sí lo está, y de forma profunda: Rust tomó de aquí sus tipos algebraicos (`enum`), el `match` exhaustivo y, sobre todo, el par `Option`/`Result` que reemplaza a los punteros nulos. Entender ML es entender por qué Rust se siente tan distinto de C aun compartiendo con él la sintaxis de llaves y la cercanía a la máquina.

Esto importa porque es el ejemplo más claro de que el árbol genealógico tiene **cruces**, no solo ramas puras (la idea que se introdujo en la clase 015). Rust no desciende de ML por su piel, pero recibe su esqueleto de seguridad de tipos de esa familia. Sebesta dedica un capítulo entero a los lenguajes funcionales, y Van Roy y Haridi construyen buena parte de su libro sobre el modelo declarativo funcional; ambos coinciden en que las ideas de ML, tras décadas en la academia, hoy están en el corazón de lenguajes mainstream.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Explicar los rasgos de la familia ML (funciones puras, inmutabilidad, inferencia, tipos algebraicos).
2. Reconocer qué tomó Rust de ML frente a lo que tomó de C.
3. Leer una expresión funcional simple (`match` sobre un tipo suma).
4. Argumentar por qué `Option`/`Result` es más seguro que un puntero nulo.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Raíces: ML (1973) | Inferencia Hindley-Milner y funciones como valores |
| 2 | Haskell: pureza y pereza | Sin efectos por defecto; evaluación perezosa |
| 3 | OCaml y F# | ML práctico; F# lleva ML a .NET |
| 4 | Tipos algebraicos y match | Modelar datos con alternativas exhaustivas |
| 5 | La huella en Rust | ADT, match, Option/Result sin nulos |

## 📖 Definiciones y características

La familia arranca con **ML** (Meta Language), creado por **Robin Milner** en Edimburgo hacia 1973 como el lenguaje de scripting de un demostrador de teoremas. De ahí nació su rasgo más célebre: la **inferencia de tipos Hindley-Milner**, un algoritmo capaz de deducir el tipo de cada expresión sin que el programador anote casi nada, manteniendo a la vez la seguridad de un lenguaje fuertemente tipado. Lo mejor de dos mundos: la comodidad aparente de un lenguaje dinámico con las garantías de uno estático. Sobre ese tronco crecieron **OCaml** (funcional-imperativo pragmático, muy usado en finanzas y en compiladores), **Standard ML** (el dialecto académico), **F#** (que lleva OCaml a .NET, como se vio en la clase 020) y **Haskell** (1990), el más purista de todos.

Los rasgos que definen a la familia son cuatro. Primero, las **funciones puras**: una función, dado el mismo argumento, devuelve siempre el mismo resultado y no modifica nada fuera de sí; esto hace el código predecible y fácil de razonar. Segundo, la **inmutabilidad por defecto**: los valores no se modifican, se transforman en valores nuevos. Tercero, los **tipos algebraicos de datos (ADT)**: tipos construidos combinando alternativas (tipos suma: "esto es *o bien* un círculo *o bien* un cuadrado") y agregados (tipos producto: "esto es un ancho *y* un alto"). Cuarto, el **pattern matching exhaustivo**: el `match`/`case` que descompone un valor según su forma y que el compilador obliga a cubrir por completo, de modo que olvidar un caso es un error de compilación, no un bug latente. Haskell añade dos señas propias: es **puro** —los efectos secundarios (imprimir, leer) se modelan explícitamente en el sistema de tipos mediante mónadas— y **perezoso** —una expresión no se evalúa hasta que se necesita su valor, lo que permite, por ejemplo, definir listas infinitas—.

Aquí está el puente con el núcleo. Cuando **Graydon Hoare** diseñó **Rust** (Mozilla, 2010; estable en 2015), tomó de C la sintaxis de llaves y el control de la memoria, pero fue a la familia ML a buscar la seguridad de tipos. El `enum` de Rust es un tipo algebraico suma; su `match` es el pattern matching exhaustivo de ML; y su `Option<T>` —que obliga a distinguir entre "hay un valor" (`Some`) y "no hay" (`None`)— es directamente la respuesta de ML al problema del puntero nulo, que Tony Hoare (otro Hoare, sin parentesco) llamó célebremente "mi error de mil millones de dólares". En un lenguaje con nulos, cualquier referencia puede ser nula y el compilador no te avisa; en uno con `Option`, la posibilidad de ausencia está en el tipo y el compilador te fuerza a tratarla. Reconocer esta herencia hace que Rust deje de parecer arbitrario: cada decisión que sorprende a un programador de C tiene una razón, y esa razón suele venir de ML.

- **ML** — familia de 1973 (Robin Milner) con inferencia de tipos Hindley-Milner. Clave: raíz de OCaml, Haskell y F#.
- **Haskell** — 1990, funcional puro y perezoso. Clave: modela los efectos con tipos (mónadas); el más purista de la familia.
- **Tipo algebraico (ADT)** — tipo compuesto por alternativas (suma) o agregados (producto). Clave: Rust lo tomó como `enum`.
- **Inferencia de tipos** — el compilador deduce los tipos sin anotarlos. Clave: rasgo de ML heredado por Rust, Kotlin, F# y otros.

## 🧩 Situación

Un programador con años de C prueba Rust por primera vez y choca con dos cosas que no esperaba: no hay `NULL` que asignar a un puntero, y en su lugar debe envolver la posible ausencia en un `Option<T>` que el `match` le obliga a desempaquetar. Su primera reacción es de fastidio: "esto es ceremonia inútil". Pero cuando entiende que viene de ML —y que ese pequeño fastidio es justo lo que hace imposible el `null pointer dereference` que le costó tantas noches en C— la fricción se convierte en aprecio. Rust no le está estorbando: le está pasando, gratis, cuarenta años de investigación en teoría de tipos.

## 🔎 Ejemplo

El `match` sobre un tipo suma, de Haskell a Rust: misma idea, casi la misma forma.

```text
Haskell:  area forma = case forma of
              Circulo r  -> pi * r * r
              Cuadrado l -> l * l

Rust:     fn area(forma: Forma) -> f64 {
              match forma {
                  Forma::Circulo(r)  => PI * r * r,
                  Forma::Cuadrado(l) => l * l,
              }
          }
```

El **delta** es casi solo sintáctico: Haskell usa `case … of` y Rust usa `match`; Haskell infiere el tipo de `forma`, Rust lo anota. Pero la semántica profunda es idéntica y viene de ML: `Forma` es un tipo suma con dos variantes, y en ambos el compilador **exige** que cubras las dos; si añades un `Triangulo` y olvidas su caso, ninguno de los dos compila. Esa exhaustividad comprobada es la herencia funcional dentro de Rust.

## ✍️ Práctica

Busca en material de Rust (o en la clase 041 del curso) un `Option` o un `Result`. Explica por escrito, en tres o cuatro frases, por qué esa idea es más segura que un puntero que puede ser nulo, y de qué familia proviene. Como reto: ¿qué palabra clave te obliga Rust a usar para "sacar" el valor de dentro de un `Option`, y qué pasa si intentas ignorar el caso `None`?

## ⚠️ Errores comunes

- **Ver Rust como "C moderno" y nada más** → causa: ignorar su mitad ML → solución: reconocer que su seguridad de tipos, su `enum` y su `match` vienen de la familia funcional.
- **Creer que "funcional" significa "académico e inútil"** → causa: prejuicio heredado de los 90 → solución: notar que sus ideas ya son mainstream en Rust, Kotlin, Swift, TypeScript y hasta Java moderno.
- **Confundir inmutabilidad con lentitud** → causa: asumir que crear valores nuevos siempre copia todo → solución: entender que compiladores e estructuras persistentes hacen esto eficiente.

## ❓ Preguntas frecuentes

- **¿Necesito aprender Haskell?** No para el núcleo, pero entender sus ideas mejora tu Rust, tu Kotlin y, sobre todo, tu forma de pensar sobre datos y efectos.
- **¿Qué es la "pereza" de Haskell?** Evaluar una expresión solo cuando se necesita su valor; permite, entre otras cosas, definir y usar listas infinitas de forma natural.
- **¿Qué es una mónada, en una frase?** Un patrón para encadenar cómputos que llevan un "contexto" (posible fallo, efecto, estado) manteniendo la pureza; en Haskell modela la entrada/salida.

## 🔗 Referencias

- R. W. Sebesta — *Concepts of Programming Languages* (12ª ed., Pearson), cap. 15 "Functional Programming Languages".
- P. Van Roy y S. Haridi — *Concepts, Techniques, and Models of Computer Programming* (MIT Press), cap. 3-4 (modelo declarativo).
- B. A. Tate — *Seven Languages in Seven Weeks* (Pragmatic Bookshelf), cap. de Haskell.
- S. Klabnik y C. Nichols — *The Rust Programming Language* — [gratis online](https://doc.rust-lang.org/book/) (cap. de `enum`, `match` y `Option`).

---

> [⏮️ Clase 021](../../parte-1-atlas-y-genealogia-de-los-lenguajes/021-familia-javascript-y-web-js-typescript-dart/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 023 ⏭️](../../parte-1-atlas-y-genealogia-de-los-lenguajes/023-familia-lisp-scheme-racket-clojure-emacs-lisp/README.md)
