# Clase 019 — Familia JVM: Java, Kotlin, Scala, Groovy, Clojure

> Parte **1 — Atlas y genealogía de los lenguajes** · ⏱️ Duración estimada: **75 min** · Nivel: **Fundamentos**
> ✅ **Clase construida.**

---

## 🎯 Objetivo

Conocer los lenguajes que corren sobre la **Máquina Virtual de Java (JVM)** y entender una idea genealógica poderosa: una familia no siempre se define por su sintaxis, a veces se define por su **plataforma de ejecución**. Java es el representante del núcleo; Kotlin, Scala, Groovy y Clojure comparten con él el mismo bytecode, el mismo recolector de basura y la misma enorme biblioteca de clases, pero ofrecen paradigmas radicalmente distintos. Un solo runtime, varias formas de programar sobre él.

Esto importa porque la JVM es una de las plataformas más exitosas de la historia del software. Cuando Sun lanzó Java en 1995 con el lema "write once, run anywhere", separó por completo el lenguaje del hardware: el compilador produce bytecode y la JVM lo ejecuta en cualquier sistema. Ese diseño abrió la puerta a que, décadas después, aparecieran lenguajes nuevos que aprovecharan toda la infraestructura sin reinventarla. Entender la JVM explica por qué puedes mezclar Java y Kotlin en un mismo proyecto, archivo con archivo, sin fricción.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Explicar qué comparten los lenguajes JVM (bytecode, GC, interoperabilidad, biblioteca estándar).
2. Distinguir el paradigma de cada uno (OO nominal, moderno pragmático, funcional-OO, Lisp).
3. Entender por qué se pueden mezclar Java y Kotlin en un mismo proyecto.
4. Reconocer el coste de la JVM (tiempo de calentamiento) y cuándo pesa.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | La JVM como plataforma | Compilan a bytecode; comparten GC y librerías |
| 2 | Java: el estándar | OO nominal, verboso pero robusto y predecible |
| 3 | Kotlin y Scala | Java moderno (null-safety, corrutinas) y funcional-OO |
| 4 | Clojure y Groovy | Un Lisp inmutable y un dinámico ágil sobre la JVM |
| 5 | Interoperabilidad | Por qué conviven en un mismo proyecto |

## 📖 Definiciones y características

La **JVM** es una máquina abstracta que ejecuta **bytecode**, un formato intermedio independiente del procesador. Cualquier lenguaje que compile a ese bytecode hereda automáticamente tres regalos: portabilidad ("compila una vez, corre en cualquier JVM"), recolección de basura automática y acceso a la biblioteca de clases de Java, una de las más completas y probadas que existen. Sebesta describe la JVM como el ejemplo canónico de máquina virtual y de compilación híbrida —a medio camino entre compilar a nativo e interpretar—, con un compilador **JIT** (Just-In-Time) que traduce el bytecode más usado a código máquina en caliente, lo que hace que Java, tras un breve calentamiento, alcance rendimiento cercano al nativo.

**Java** (James Gosling, Sun Microsystems, 1995) es OO **nominal**: todo vive dentro de clases, la herencia y las interfaces se declaran explícitamente, y el compilador comprueba los tipos con severidad. Es verboso, pero esa verbosidad compra robustez y predecibilidad, razón por la que domina el backend empresarial. Sobre esa misma base nacieron alternativas con filosofías distintas. **Scala** (Martin Odersky, 2003) fusiona la orientación a objetos con la programación funcional pura: funciones de primera clase, inmutabilidad, pattern matching y un sistema de tipos muy expresivo. **Kotlin** (JetBrains, 2011) buscó un objetivo más pragmático —"un Java mejor"—: seguridad frente a nulos en el sistema de tipos (`String` vs `String?`), inferencia, corrutinas para asincronía y una sintaxis mucho más concisa; Google lo hizo lenguaje oficial de Android en 2017. **Groovy** (2003) añadió tipado dinámico y azúcar sintáctico, popular en scripts y en Gradle. Y **Clojure** (Rich Hickey, 2007) es lo más sorprendente del grupo: un dialecto moderno de Lisp, con su sintaxis de paréntesis y su énfasis radical en datos inmutables, corriendo sobre la misma VM que Java.

La consecuencia práctica de compartir bytecode es la **interoperabilidad total**. Un método escrito en Kotlin puede llamar a una clase de Java, y viceversa, porque tras compilar ambos son bytecode indistinguible que comparte el mismo modelo de objetos y la misma biblioteca. Esto permite migrar un proyecto gradualmente —archivo a archivo— en lugar de reescribirlo de golpe, algo que ninguna familia definida solo por sintaxis puede ofrecer. Van Roy y Haridi lo enmarcan bien: aquí la unidad no es un lenguaje, sino un **entorno de ejecución compartido** sobre el que conviven varios modelos de computación.

- **JVM** — máquina virtual que ejecuta bytecode. Clave: da portabilidad, GC y compilación JIT.
- **Java** — 1995 (Gosling, Sun), OO nominal sobre la JVM. Clave: núcleo del curso; pilar del backend empresarial.
- **Kotlin** — 2011 (JetBrains), Java moderno con null-safety y corrutinas. Clave: oficial en Android; interopera 100% con Java.
- **Scala** — 2003 (Odersky), fusión funcional-OO con tipos potentes. Clave: lleva el paradigma funcional al ecosistema JVM.
- **Clojure** — 2007 (Rich Hickey), dialecto de Lisp sobre la JVM. Clave: inmutabilidad y homoiconicidad en una plataforma mainstream.

## 🧩 Situación

Un equipo mantiene una app de Android escrita en Java desde hace años y quiere adoptar corrutinas y seguridad frente a nulos sin detener el desarrollo ni reescribir cientos de miles de líneas. La solución no es un salto arriesgado, sino una migración incremental: escriben los archivos nuevos en Kotlin y convierten los viejos poco a poco. Java y Kotlin conviven en el mismo módulo porque ambos compilan al mismo bytecode y comparten la misma biblioteca. Lo que en otras familias sería una reescritura traumática, en la JVM es un cambio de archivo.

## 🔎 Ejemplo

Cuatro maneras de sumar dos números sobre exactamente la misma plataforma:

```text
Java:    int r = a + b;                // OO nominal, tipo explícito
Kotlin:  val r = a + b                 // inferencia, valor inmutable
Scala:   val r = a + b                 // funcional-OO, inmutable por defecto
Groovy:  def r = a + b                 // dinámico, tipo en ejecución
Clojure: (def r (+ a b))               // Lisp: prefijo y paréntesis
```

El **delta** entre los tres primeros es mínimo: `val` en vez de `int` para pedir inferencia e inmutabilidad. Clojure es el que rompe la piel de C —notación prefija, paréntesis— pero corre sobre la misma JVM y puede invocar cualquier clase de Java. Es la mejor ilustración de que "misma familia" aquí significa "mismo runtime", no "misma sintaxis".

## ✍️ Práctica

Kotlin distingue `val` (inmutable, no reasignable) de `var` (mutable). ¿A qué lenguaje del núcleo se parece esa distinción y en qué se diferencia (pista: Rust y su `let` vs `let mut`)? Luego busca en la documentación de Kotlin un tipo `String?` frente a `String` y explica en una frase qué garantía nueva ofrece el sistema de tipos que Java no da.

## ⚠️ Errores comunes

- **Creer que "lenguaje JVM" equivale a "Java"** → causa: ignorar la diversidad de paradigmas sobre la misma VM → solución: recordar que Clojure (Lisp) y Java conviven en la JVM.
- **Asumir arranque instantáneo** → causa: la JVM necesita tiempo de calentamiento (carga de clases + JIT) → solución: tenerlo en cuenta en herramientas de línea de comandos de vida corta o funciones serverless.
- **Mezclar mutabilidad de Java con inmutabilidad de Clojure sin cuidado** → causa: pasar estructuras mutables a código que asume inmutabilidad → solución: conocer las garantías de cada lado de la frontera.

## ❓ Preguntas frecuentes

- **¿Puedo llamar a Java desde Kotlin y al revés?** Sí, en ambos sentidos: comparten bytecode, modelo de objetos y biblioteca, así que la interoperabilidad es prácticamente total.
- **¿Clojure es "raro"?** Su sintaxis Lisp asusta al principio, pero su modelo de datos inmutables es muy elegante y encaja bien en sistemas concurrentes.
- **¿Por qué elegir la JVM hoy?** Por madurez: décadas de bibliotecas probadas, herramientas excelentes y un GC muy afinado, además de la libertad de elegir el lenguaje sin cambiar de plataforma.

## 🔗 Referencias

- J. Bloch — *Effective Java* (3ª ed., Addison-Wesley).
- R. W. Sebesta — *Concepts of Programming Languages* (12ª ed., Pearson), cap. 1 (compilación híbrida y máquinas virtuales) y cap. 2.
- B. A. Tate — *Seven Languages in Seven Weeks* (Pragmatic Bookshelf), cap. de Scala y Clojure.
- P. Van Roy y S. Haridi — *Concepts, Techniques, and Models of Computer Programming* (MIT Press).

---

> [⏮️ Clase 018](../../parte-1-atlas-y-genealogia-de-los-lenguajes/018-familia-scripting-dinamico-python-ruby-perl-php-lua/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 020 ⏭️](../../parte-1-atlas-y-genealogia-de-los-lenguajes/020-familia-net-c-sharp-f-sharp-vb-net/README.md)
