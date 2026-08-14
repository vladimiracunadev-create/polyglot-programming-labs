# Parte 1 — Atlas y genealogía de los lenguajes

> [⏮️ Parte 0](../parte-0-pensamiento-computacional-y-el-metodo-poliglota/README.md) · [⬅️ Programa](../../README.md) · [📚 Índice](../README.md) · [⏭️ Parte 2](../parte-2-herramientas-toolchains-y-anatomia-de-comandos/README.md)

**14 clases** · rango 015–028 · clases de **método** · nivel fundamentos · **~21 h** ([cronograma](../../docs/syllabus.md))

> 🧭 **El árbol genealógico completo: por qué diez lenguajes bastan para leer decenas.**

---

## 🧭 De qué trata esta parte

La programación se percibe como una lista inabarcable de tecnologías rivales, y esa percepción es un accidente de cómo se enseña. En realidad hay un puñado de **linajes** con antepasados comunes: cuando ves de dónde salió cada lenguaje y qué problema vino a resolver, sus decisiones dejan de parecer arbitrarias.

Esta parte recorre las familias una a una: la de C y las llaves, la del scripting dinámico, la de la JVM, la de .NET, la de la web, la funcional tipada, Lisp, la lógica, la de actores, la de sistemas, la científica y la de los lenguajes que sobreviven en su nicho. Cada una aporta una **idea** que el resto del curso reencuentra con código delante.

Es la parte que sostiene la tesis del Atlas: *aprende el representante, reconoce la familia entera*. Si dominas C lees la superficie de cinco lenguajes más; si entiendes por qué existe la JVM entiendes de golpe a Kotlin, Scala, Groovy y Clojure.

## 🎒 Qué necesitas traer

La Parte 0 completa, sobre todo las tres clases de diferencia (002): sin ese criterio, comparar familias degenera en preferencias.

## 🎯 Qué sabrás hacer al terminar

Resultados comprobables: si no puedes hacerlos, la parte no está cerrada.

1. Situar cualquier lenguaje conocido en su familia y nombrar a sus parientes cercanos.
2. Distinguir estándar, implementación, versión y ecosistema al hablar de un lenguaje.
3. Explicar qué idea aporta cada familia y qué problema histórico vino a resolver.
4. Predecir qué te resultará familiar y qué te sorprenderá al abrir un lenguaje nuevo.
5. Usar el [Atlas](../../atlas/README.md) como material de consulta durante el resto del programa.

## 🗺️ El recorrido, clase a clase

Las clases están agrupadas en bloques por la razón que las une. El orden es secuencial: cada una asume la anterior.

### 🔹 Cómo se lee el árbol · clases 015–016

El mapa general y el ciclo de vida de un lenguaje: sin esto, las familias son una lista de nombres.

- **[015 · El árbol genealógico de los lenguajes: mapa general](015-el-arbol-genealogico-de-los-lenguajes-mapa-general/README.md)** — El mapa completo de familias y antepasados comunes. Sirve para dejar de percibir la programación como una lista inabarcable de tecnologías rivales y empezar a verla como lo que es: un puñado de linajes descendientes de unos pocos experimentos fundacionales.
- **[016 · Cómo nace y evoluciona un lenguaje: estándares, versiones y ecosistemas](016-como-nace-y-evoluciona-un-lenguaje-estandares-versiones-y-ecosistemas/README.md)** — Un lenguaje no es un objeto fijo sino un proceso: nace de una necesidad, se formaliza en un **estándar**, se materializa en **implementaciones** y publica **versiones** con reglas de compatibilidad. Distinguir esas cuatro cosas explica por qué «Python» y «CPython» no son sinónimos.

### 🔹 Las familias con representante en el núcleo · clases 017–021

Cinco familias cuyos representantes vas a implementar y verificar a partir de la Parte 3.

- **[017 · Familia C y de las llaves: C, C++, Objective-C](017-familia-c-y-de-las-llaves-c-c-plus-plus-objective-c/README.md)** — La familia que fijó la sintaxis dominante de la programación actual: llaves, punto y coma, `for` de tres partes. Si dominas C, ya lees la superficie de Java, C#, JavaScript, Go y PHP — aquí se explica exactamente por qué, y dónde el parecido deja de serlo.
- **[018 · Familia scripting dinámico: Python, Ruby, Perl, PHP, Lua](018-familia-scripting-dinamico-python-ruby-perl-php-lua/README.md)** — Los lenguajes **dinámicos**: interpretados, sin declaración obligatoria de tipos, diseñados para que un humano escriba la solución en minutos. Python y PHP están en el núcleo; Ruby, Perl y Lua son los primos cercanos que además se ejecutan en CI en cada clase de código.
- **[019 · Familia JVM: Java, Kotlin, Scala, Groovy, Clojure](019-familia-jvm-java-kotlin-scala-groovy-clojure/README.md)** — Una familia que no se define por la sintaxis sino por la **plataforma de ejecución**: todo lo que corre sobre la JVM. Java representa al núcleo; Kotlin, Scala, Groovy y Clojure comparten bytecode y biblioteca con sintaxis y paradigmas radicalmente distintos.
- **[020 · Familia .NET: C#, F#, VB.NET](020-familia-net-c-sharp-f-sharp-vb-net/README.md)** — El mismo fenómeno de la JVM, ahora sobre el CLR de .NET: **C#** (núcleo, multiparadigma), **F#** (funcional, de la familia ML) y **VB.NET** conviven sobre un runtime común. Dos plataformas distintas llegando a la misma idea genealógica.
- **[021 · Familia JavaScript y web: JS, TypeScript, Dart](021-familia-javascript-y-web-js-typescript-dart/README.md)** — La familia que domina la web. JavaScript nació en 1995 para animar páginas y hoy corre en navegador, servidor, móvil y embebidos; TypeScript le añade tipos sin cambiar su semántica de ejecución. Aquí se entiende por qué ambos están en el núcleo y no como uno solo.

### 🔹 Las familias que aportan ideas · clases 022–025

ML, Lisp, la lógica y los actores: poco código propio en el curso, influencia enorme en el resto.

- **[022 · Familia funcional tipada (ML): Haskell, OCaml, F# y la influencia en Rust](022-familia-funcional-tipada-ml-haskell-ocaml-f-sharp-y-la-influencia-en-rust/README.md)** — Ningún miembro clásico de la familia ML —Haskell, OCaml, Standard ML— está en el núcleo, pero su **influencia** sí lo está y de forma profunda: los tipos algebraicos, `Option`/`Result` y la inferencia de Rust vienen de aquí. Explica por qué Rust «se siente» distinto a C.
- **[023 · Familia Lisp: Scheme, Racket, Clojure, Emacs Lisp](023-familia-lisp-scheme-racket-clojure-emacs-lisp/README.md)** — La familia viva más antigua (1958) y una de las más influyentes: su rasgo único es la **homoiconicidad**, el código escrito con la misma estructura que los datos. Aunque nunca escribas Lisp, sus ideas están en los cierres, las comprensiones y la metaprogramación de tu lenguaje.
- **[024 · Familia lógica y declarativa: SQL, Prolog, Datalog](024-familia-logica-y-declarativa-sql-prolog-datalog/README.md)** — Los lenguajes donde describes **QUÉ** quieres y no **CÓMO** obtenerlo: SQL en el núcleo, Prolog y Datalog como primos. Es el primer choque frontal con un paradigma que no es una variante del imperativo, sino su opuesto.
- **[025 · Familia concurrente/actor: Erlang, Elixir y el CSP de Go](025-familia-concurrente-actor-erlang-elixir-y-el-csp-de-go/README.md)** — Lenguajes diseñados desde su base para hacer muchas cosas a la vez: el modelo de **actores** de Erlang y Elixir (procesos aislados, sin memoria compartida) frente al **CSP** de Go (canales). Aquí queda claro que «concurrencia» no es una técnica sino varios modelos incompatibles entre sí.

### 🔹 Sistemas, cálculo y legado · clases 026–028

Los lenguajes cercanos a la máquina, los del cálculo numérico y los que sobreviven en su nicho.

- **[026 · Familia de sistemas: C, C++, Rust, Zig](026-familia-de-sistemas-c-c-plus-plus-rust-zig/README.md)** — Los lenguajes hechos para escribir sistemas operativos, drivers, motores de bases de datos y runtimes: C, C++, Rust y Zig. Control explícito de la memoria, sin runtime pesado y con el coste puesto donde el programador pueda verlo.
- **[027 · Familia array y científica: APL, R, Julia, Fortran, MATLAB](027-familia-array-y-cientifica-apl-r-julia-fortran-matlab/README.md)** — APL, R, Julia, Fortran y MATLAB traen un estilo de pensamiento distinto: la **vectorización**, operar sobre arreglos completos de una vez en lugar de elemento a elemento con bucles. Cambia la unidad de razonamiento, no solo la sintaxis.
- **[028 · Lenguajes históricos y de nicho: COBOL, Fortran, Pascal, BASIC, Bash](028-lenguajes-historicos-y-de-nicho-cobol-fortran-pascal-basic-bash/README.md)** — COBOL, Fortran, Pascal, BASIC y Bash no forman familia por parentesco sino por destino: marcaron una época y, en vez de desaparecer, se replegaron a un nicho donde siguen siendo insustituibles. Explican decisiones de diseño que todavía heredamos.

## ⚠️ Los malentendidos que esta parte corrige

| Se suele creer | Lo que ocurre en realidad |
|---|---|
| «Una familia se define por la sintaxis.» | A veces se define por la plataforma: Kotlin y Clojure no se parecen en nada escritos y comparten JVM, bytecode y bibliotecas. |
| «Los lenguajes viejos están muertos.» | COBOL mueve transacciones bancarias hoy y Fortran sigue en cálculo científico. Sobreviven donde son insustituibles, no por inercia. |
| «Aprender más lenguajes es acumular sintaxis.» | Es reconocer familias. El undécimo lenguaje cuesta una fracción del primero si sabes de qué linaje viene. |

## 🧪 Cómo estudiar esta parte

1. **Lee la clase entera antes de opinar.** Son clases de razonamiento: el valor está en el argumento completo, no en la definición suelta.
2. **Contesta la pregunta que abre cada clase** con tus palabras antes de seguir a la siguiente. Si no puedes, vuelve al párrafo del objetivo.
3. **Aplícalo a un problema tuyo.** Estas clases no se verifican con una máquina; se verifican usándolas sobre código real que ya escribiste.
4. **Anota los términos nuevos.** Aparecen otra vez, con código delante, a partir de la Parte 3 — y están todos en el [glosario](../../glosario/README.md).

## 📚 Fuentes de referencia de esta parte

Cada clase cita estos libros en su sección de referencias. No se reproduce su contenido: la redacción es original.

- R. W. Sebesta — *Concepts of Programming Languages* (12ª ed., Pearson).
- M. L. Scott — *Programming Language Pragmatics* (4ª ed., Morgan Kaufmann).
- B. A. Tate — *Seven Languages in Seven Weeks* (Pragmatic Bookshelf).
- P. Van Roy y S. Haridi — *Concepts, Techniques, and Models of Computer Programming* (MIT Press).

## 🔗 Qué abre esta parte

Sabiendo qué lenguajes existen y de dónde vienen, la Parte 2 responde a la pregunta práctica: cómo se ejecutan.

---

> [⏮️ Parte 0](../parte-0-pensamiento-computacional-y-el-metodo-poliglota/README.md) · [⬅️ Programa](../../README.md) · [📚 Índice](../README.md) · [⏭️ Parte 2](../parte-2-herramientas-toolchains-y-anatomia-de-comandos/README.md)
