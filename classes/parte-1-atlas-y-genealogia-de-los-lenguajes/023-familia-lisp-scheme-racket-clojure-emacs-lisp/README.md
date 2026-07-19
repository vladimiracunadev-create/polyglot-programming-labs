# Clase 023 — Familia Lisp: Scheme, Racket, Clojure, Emacs Lisp

> Parte **1 — Atlas y genealogía de los lenguajes** · ⏱️ Duración estimada: **75 min** · Nivel: **Fundamentos**
> ✅ **Clase construida.**

---

## 🎯 Objetivo

Conocer la familia más antigua todavía viva y una de las más influyentes de toda la historia: **Lisp**, creado por John McCarthy en el MIT en 1958. Su rasgo único es la **homoiconicidad**: el código se escribe con la misma estructura que los datos que manipula —listas anidadas entre paréntesis—, lo que permite escribir **macros** capaces de reescribir el propio lenguaje. Ninguno de sus dialectos (Scheme, Racket, Clojure, Emacs Lisp, Common Lisp) está en el núcleo del curso, pero sus ideas —funciones de primera clase, recolección de basura, tipado dinámico, el REPL interactivo— hoy están en absolutamente todos los lenguajes que usas.

Esto importa porque Lisp es la mayor demostración de que unas pocas ideas radicales pueden difundirse por todo el árbol genealógico durante más de medio siglo. Sebesta lo señala como el segundo lenguaje de alto nivel más antiguo tras Fortran, y buena parte del influyente libro *SICP* (Abelson y Sussman), pilar del pensamiento computacional, está escrito en Scheme precisamente porque su minimalismo deja ver la esencia de la computación sin ruido sintáctico.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Explicar la homoiconicidad y por qué habilita macros más potentes que las de otros lenguajes.
2. Leer una expresión Lisp en notación prefija entre paréntesis.
3. Reconocer ideas nacidas en Lisp que hoy son universales.
4. Situar los dialectos principales (Scheme, Racket, Clojure, Emacs Lisp) y su uso.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Homoiconicidad | Código y datos comparten forma (listas) |
| 2 | Notación prefija | `(operador operando operando)`, sin ambigüedad |
| 3 | Macros | Programas que escriben programas antes de compilar |
| 4 | Herencia universal | GC, REPL y funciones de primera clase nacieron aquí |
| 5 | Dialectos vivos | Scheme, Racket, Clojure, Emacs Lisp |

## 📖 Definiciones y características

**Lisp** (LISt Processor) fue diseñado por **John McCarthy** en 1958 como notación para el razonamiento simbólico en inteligencia artificial. En el proceso, McCarthy inventó o popularizó ideas que hoy damos por sentadas: las **funciones de primera clase** (una función es un valor que se puede pasar, devolver y guardar), la **recursión** como forma natural de computar, la **recolección de basura** automática y el **REPL** (Read-Eval-Print Loop), el bucle interactivo donde escribes una expresión y ves su resultado al instante. Cada una de esas ideas viajó al resto del árbol: la recolección de basura llegó a Java y a Python, las funciones de primera clase a JavaScript y a casi todos, el REPL a innumerables lenguajes. Cuando usas una lambda o dejas que el runtime libere memoria por ti, estás usando Lisp sin saberlo.

El rasgo verdaderamente distintivo, el que ningún otro lenguaje mainstream iguala del todo, es la **homoiconicidad**. En Lisp, `(+ 1 2)` es a la vez una llamada a función *y* una lista de tres elementos: el símbolo `+` y los números `1` y `2`. Código y datos tienen exactamente la misma representación. Esto suena a curiosidad teórica hasta que se entiende su consecuencia: como el programa es una estructura de datos que el propio programa puede manipular, se pueden escribir **macros** que reciben trozos de código sin evaluar, los transforman y devuelven código nuevo, todo antes de la ejecución. No son las macros de texto de C, torpes y ciegas; son transformaciones de la estructura misma del programa. Con macros, un programador de Lisp puede añadir construcciones sintácticas nuevas al lenguaje —bucles, sistemas de objetos, DSLs enteros— sin tocar el compilador. Van Roy y Haridi describen esto como la capacidad de Lisp de "crecer hacia el problema" en lugar de forzar el problema al lenguaje.

La familia sigue muy viva a través de sus dialectos. **Scheme** (Sussman y Steele, 1975) es el minimalista y elegante, favorito en enseñanza e investigación (es el lenguaje de *SICP*). **Racket** desciende de Scheme y se especializa en la creación de lenguajes. **Clojure** (Rich Hickey, 2007) es el dialecto moderno y pragmático: corre sobre la JVM —por eso también aparece en la clase 019—, pone un énfasis radical en los datos inmutables y ha llevado a Lisp de vuelta al desarrollo comercial de backends y procesamiento de datos. **Emacs Lisp** es el lenguaje de extensión del editor Emacs, donde millones de líneas configuran y amplían el programa en caliente. El aire de familia entre todos ellos es inmediato: paréntesis, notación prefija y la misma promesa de que el lenguaje es maleable.

- **Lisp** — 1958 (John McCarthy), segundo lenguaje de alto nivel más antiguo. Clave: introdujo GC, funciones de primera clase y el REPL.
- **Homoiconicidad** — el código tiene la misma estructura que los datos que manipula. Clave: habilita macros que transforman el lenguaje.
- **Scheme** — 1975, dialecto minimalista y elegante. Clave: usado en enseñanza; el lenguaje de *SICP*.
- **Clojure** — 2007, Lisp moderno e inmutable sobre la JVM. Clave: acerca la familia al mundo mainstream.

## 🧩 Situación

Un desarrollador ve por primera vez `(+ 1 2 3)` y lo descarta como "raro" por los paréntesis y el operador delante. Pero un par de meses después necesita, en otro lenguaje, generar código repetitivo a partir de una plantilla y descubre que su lenguaje no puede tratar su propio código como datos: tiene que recurrir a generadores externos, plantillas de texto o reflexión frágil. En Lisp, eso sería una macro de diez líneas. La uniformidad que al principio le pareció fea —"todo es una lista"— resulta ser justo el superpoder que a su lenguaje le falta. Juzgó la forma y se perdió la idea.

## 🔎 Ejemplo

La notación prefija: el operador va primero y todo se agrupa con paréntesis, sin reglas de precedencia que memorizar.

```text
Infija (C, JS):   (1 + 2) * 3
Lisp:             (* (+ 1 2) 3)

Definir una función (Scheme):
                  (define (doble x) (* x 2))
                  (doble 21)   ; => 42
```

El **delta** frente a la familia C es total en la piel: no hay operadores infijos, no hay precedencia, no hay comas; solo listas anidadas donde el primer elemento es qué hacer y el resto son los argumentos. Pero fíjate en lo que se gana: `(* (+ 1 2) 3)` no tiene ninguna ambigüedad sobre qué se evalúa antes, porque la estructura de paréntesis *es* el árbol de evaluación. Esa correspondencia exacta entre lo que escribes y cómo se computa es la homoiconicidad en acción.

## ✍️ Práctica

Traduce `(* (+ 2 3) (- 10 4))` a notación infija y calcula el resultado a mano. (Respuesta: `(2 + 3) * (10 - 4) = 30`.) Como segundo ejercicio, escribe en notación prefija de Lisp la expresión infija `10 * 2 + 5`. Fíjate en que tienes que decidir el orden explícitamente con los paréntesis: no hay precedencia que lo decida por ti.

## ⚠️ Errores comunes

- **Rechazar Lisp por los paréntesis** → causa: juzgar la forma en vez de las ideas → solución: ver que la uniformidad "todo es una lista" es exactamente lo que habilita las macros.
- **Creer que Lisp es cosa del pasado** → causa: ignorar Clojure, Racket y Emacs Lisp → solución: reconocer que la familia sigue viva, en producción y en editores usados a diario.
- **Confundir las macros de Lisp con las de C** → causa: asumir que "macro" es sustitución de texto → solución: entender que las de Lisp transforman la estructura del programa, no cadenas.

## ❓ Preguntas frecuentes

- **¿Para qué sirve Lisp hoy?** Clojure en backend y procesamiento de datos; Racket y Scheme en enseñanza e investigación; Emacs Lisp en el editor Emacs; Common Lisp en nichos que valoran su potencia.
- **¿Qué idea de Lisp uso sin saberlo?** Casi seguro las funciones de primera clase (pasar funciones como valores) y la recolección de basura; ambas nacieron aquí.
- **¿La homoiconicidad existe en otros lenguajes?** En grado pleno, casi solo en la familia Lisp. Otros la aproximan con macros o metaprogramación, pero sin la identidad total entre código y datos.

## 🔗 Referencias

- H. Abelson y G. J. Sussman — *Structure and Interpretation of Computer Programs* (2ª ed., MIT Press) — [gratis online](https://mitpress.mit.edu/9780262510875/).
- R. W. Sebesta — *Concepts of Programming Languages* (12ª ed., Pearson), cap. 2 (Lisp) y cap. 15 (funcional).
- B. A. Tate — *Seven Languages in Seven Weeks* (Pragmatic Bookshelf), cap. de Clojure.
- P. Van Roy y S. Haridi — *Concepts, Techniques, and Models of Computer Programming* (MIT Press).

---

> [⏮️ Clase 022](../../parte-1-atlas-y-genealogia-de-los-lenguajes/022-familia-funcional-tipada-ml-haskell-ocaml-f-sharp-y-la-influencia-en-rust/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 024 ⏭️](../../parte-1-atlas-y-genealogia-de-los-lenguajes/024-familia-logica-y-declarativa-sql-prolog-datalog/README.md)
