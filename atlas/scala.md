# 🔺 Scala — 2004

> [⬅️ Atlas](README.md) · [🗂️ Todas las fichas](lenguajes.md) · [📚 Índice de clases](../classes/README.md)

Scala es el intento más serio de **fundir la orientación a objetos con la programación funcional en un
solo sistema de tipos coherente**. Lo consiguió — y el precio fue un lenguaje que se puede escribir de
muchas formas distintas, lo que produjo a la vez ideas que hoy están en todas partes y una reputación
de complejidad.

> **🎯 Por qué está en este programa**
>
> Scala es un **primo de la familia JVM** ([Atlas](README.md#jvm)), cuyo representante en el núcleo
> es [Java](java.md).
>
> Aporta al programa el sistema de tipos más expresivo de todos los lenguajes de esta lista, y en
> particular dos conceptos: **el emparejamiento de patrones sobre tipos algebraicos**
> ([clase 100](../classes/parte-6-datos-y-estructuras/100-igualdad-e-identidad/README.md) y clase 116)
> y **las colecciones inmutables persistentes** (clase 102). Y aporta un caso de estudio de la clase
> 175: **Scala 3 rompió la compatibilidad para simplificarse**, y eso tiene un coste.

| | |
|---|---|
| **Año** | 2004; **2.x** durante quince años; **Scala 3** en 2021 |
| **Autoría** | **Martin Odersky**, EPFL — coautor de los genéricos de Java y del compilador javac |
| **Familia** | JVM; con influencia de [Java](java.md), [Haskell](haskell.md), ML y Erlang |
| **Paradigma** | **OO y funcional a la vez**, sin costuras |
| **Tipado** | **Estático muy expresivo**: tipos superiores, implícitos, dependientes de ruta |
| **Memoria** | La de la JVM |
| **Ejecución** | Bytecode JVM; también **Scala.js** y **Scala Native** |
| **Estado** | 🟢 **Sólido** en datos y en sistemas distribuidos; en descenso frente a Kotlin |

---

## 📜 Historia

**Martin Odersky** no es un desconocido en esta historia: **escribió el compilador javac** y **diseñó
los genéricos de Java** con Philip Wadler. Sabía exactamente qué limitaciones tenía la plataforma y
por qué.

En **2004** publicó Scala —*scalable language*— con una tesis: **la orientación a objetos y la
programación funcional no son opuestas, y se pueden unificar**. En Scala **todo es un objeto** —como
en [Smalltalk](smalltalk.md)— y **todas las funciones son valores** —como en
[Lisp](common-lisp.md)—, y las dos cosas encajan en el mismo sistema de tipos.

Y su influencia fue enorme, sobre todo por dos proyectos:

- **Apache Spark (2012)**, escrito en Scala, que se convirtió en el estándar del procesamiento de
  datos masivos.
- **Akka**, que llevó el **modelo de actores** de [Erlang](erlang.md) a la JVM (clase 133).

También aportó al debate del lenguaje: **las lambdas de Java 8 llegaron en parte por la presión de
Scala**, y su biblioteca de colecciones influyó en la de Kotlin y en la de Java.

**Scala 3 (2021)** fue una reescritura profunda —basada en la teoría DOT y en el compilador Dotty—
que **simplificó** el lenguaje: sustituyó los `implicit`, que eran su rincón más difícil, por
`given`/`using`; añadió sintaxis por sangría opcional; y unificó los tipos. **Rompió compatibilidad**,
y la migración del ecosistema ha sido lenta — la lección de la clase 175 que también vivieron
[Python](python.md) 3 y [D](d.md).

## 🏭 Dónde vive hoy

- **Datos a gran escala**: **Spark**, Kafka Streams, Flink, Delta Lake.
- **Sistemas distribuidos**: **Akka** y Pekko, en telecomunicaciones, finanzas y videojuegos en línea.
- **Servicios financieros**: bancos de inversión con requisitos de corrección alta.
- **Empresas conocidas**: Twitter (histórico), LinkedIn, Netflix, Zalando, Disney Streaming.
- **Y en investigación**: por su sistema de tipos, es una plataforma habitual de experimentación.

## 🧠 Lo que enseña: patrones y tipos algebraicos

**El emparejamiento de patrones sobre tipos sellados** es la aportación más transferible:

```scala
sealed trait Forma
case class Circulo(r: Double) extends Forma
case class Rectangulo(a: Double, b: Double) extends Forma

def area(f: Forma): Double = f match
  case Circulo(r)        => math.Pi * r * r
  case Rectangulo(a, b)  => a * b
  // ← si falta un caso, el COMPILADOR AVISA
```

**La exhaustividad comprobada** es lo que hace valioso el patrón: **al añadir una forma nueva, el
compilador señala todos los sitios que hay que actualizar** (clase 100). Es lo que
[Rust](rust.md), [Kotlin](kotlin.md), [Java](java.md) 21, [C#](csharp.md) y [Swift](swift.md) han
adoptado después, y viene de ML y de [Haskell](haskell.md).

Y las **colecciones inmutables persistentes**:

```scala
val a = List(1, 2, 3)
val b = 0 :: a        // ← b es una lista nueva... que COMPARTE la estructura de a
```

**No se copia nada**: las estructuras persistentes comparten las partes que no cambian (clase 102).
Eso hace la inmutabilidad asequible, y es la base de las colecciones de [Clojure](clojure.md) y de
las bibliotecas inmutables de JavaScript.

> **Y el rincón difícil merece nombrarse con honestidad**: los **implícitos** de Scala 2 —valores que
> el compilador inserta buscándolos por tipo— son a la vez lo más potente del lenguaje y la razón
> principal de su fama. Permiten clases de tipos al estilo de Haskell, conversiones automáticas y
> extensión de tipos ajenos; y también producen código donde **no se ve de dónde sale lo que se
> ejecuta**. **Scala 3 los rediseñó** con `given`/`using`, precisamente para hacerlos explícitos.

## 🔄 Lo que se ha modernizado

- **Scala 3**: `given`/`using` en lugar de `implicit`, uniones e intersecciones de tipos, `enum`,
  métodos de extensión y sintaxis por sangría opcional.
- **Scala Native** y **Scala.js**: el mismo lenguaje a binario nativo y al navegador.
- **Efectos tipados**: **ZIO** y **Cats Effect** modelan los efectos secundarios en el tipo —la idea
  de [Haskell](haskell.md) llevada a la práctica industrial (clase 118).
- **`scala-cli`**: ejecutar un fichero sin proyecto, con dependencias declaradas en un comentario —
  arranque de fricción cero (clase 167).
- **Y el compilador más rápido** de Scala 3, aunque sigue siendo lento comparado con Java o Kotlin.

## ⚙️ Cómo se ejecuta hoy

```bash
scala-cli run main.scala < entrada.txt      # sin proyecto ni configuración
scalac Venta.scala && scala Venta

sbt compile test                              # el sistema de construcción clásico
sbt scalafmtCheck scalafixAll                  # estilo y correcciones (clase 146)
```

## 🧪 El programa de la clase 041 en Scala

```scala
object Venta extends App {
  val Array(precio, cantidad, descuento) =
    scala.io.StdIn.readLine().split(" ").map(_.toDouble)
  val total = precio * cantidad * (1 - descuento)
  println(f"Total: $total%.2f")
}
```

**Lo que hay que ver.**

- **`val Array(a, b, c) = ...` no es una asignación múltiple: es un emparejamiento de patrones.** Se
  compara el valor con el patrón `Array(_, _, _)` y se extraen los tres. **Si la línea trajera cuatro
  campos, esto fallaría en ejecución** — y esa es la diferencia con la desestructuración de
  [Kotlin](kotlin.md) o [Python](python.md).
- **`_.toDouble`** es una función anónima con parámetro implícito: el guion bajo **es** el argumento.
  Es de los idiomas más reconocibles del lenguaje, y también de los que más confunden al principio.
- **`f"Total: $total%.2f"`** es un interpolador de cadenas **comprobado en compilación**: si el
  formato no encaja con el tipo, no compila (clase 142). El prefijo `f` selecciona el interpolador, y
  se pueden definir otros — es una característica del lenguaje, no de la biblioteca.
- **`val`, otra vez inmutable por defecto**, como en Kotlin y Rust (clase 102).

## 📚 Fuentes y bibliografía

- [docs.scala-lang.org](https://docs.scala-lang.org/) — el tour del lenguaje y la
  [guía de migración a Scala 3](https://docs.scala-lang.org/scala3/guides/migration/).
- **Martin Odersky, Lex Spoon, Bill Venners**, *Programming in Scala*, 5.ª ed. — el libro del autor;
  la referencia.
- **Noel Welsh, Dave Gurnell**, *Essential Scala* / *Scala with Cats* — libres en línea; excelentes
  para entender los tipos y los efectos.
- [Rock the JVM](https://rockthejvm.com/) — cursos y artículos con muy buenas explicaciones de tipos
  avanzados.
- **Odersky et al.**, *The Essence of Dependent Object Types* — el fundamento teórico de Scala 3, para
  quien quiera llegar al final.

---

⏮️ [Volver al Atlas](README.md) · 🗂️ [Todas las fichas](lenguajes.md) ·
🔗 Relacionadas: [Java](java.md) · [Kotlin](kotlin.md) · [Haskell](haskell.md) · [OCaml](ocaml.md) ·
[Clojure](clojure.md)
