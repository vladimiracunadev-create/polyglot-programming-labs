# 🌐 Atlas y genealogía de los lenguajes

> [⬅️ Volver al programa](../README.md) · [📚 Índice completo](../classes/README.md)

El Atlas es la **segunda capa** del programa. Mientras el **núcleo** (10 lenguajes) se implementa y
se verifica, el Atlas te deja **comprender ~40 lenguajes más por sus características**: su historia,
su familia, su paradigma, su modelo de memoria y con qué software se ejecutan. La tesis:
**aprende el representante, reconoce la familia entera.**

> Este material es **de lectura** (historia, características, toolchain). No se ejecuta en CI. Cada
> ficha se fecha y enlaza a la documentación oficial, porque las versiones y herramientas cambian.

**Última revisión: 2026-07.** Los datos históricos (autor, año, motivo) son estables; las
herramientas y versiones no. Ante cualquier detalle operativo, la fuente de verdad es siempre la
documentación oficial enlazada en cada cápsula.

## 🌳 El árbol, en una tabla

| Familia | Representante del núcleo | Primos (se comprenden por características) | Idea que aporta |
|---|---|---|---|
| C / llaves | **C** | C++, Objective-C, Zig, Nim, D | Memoria, punteros, sintaxis brace |
| Scripting dinámico | **Python** / **PHP** | Ruby, Perl, Lua, Tcl, R | Tipado dinámico, rapidez de escritura |
| JavaScript / web | **JavaScript** → **TypeScript** | Dart, Elm, ActionScript | Prototipos, asincronía, web |
| JVM | **Java** | Kotlin, Scala, Groovy, Clojure | OO nominal en máquina virtual |
| .NET | **C#** | F#, VB.NET | Multiparadigma sobre el CLR |
| Funcional tipada (ML) | — (influye en **Rust**) | Haskell, OCaml, Elm, F# | Pureza, tipos algebraicos, inferencia |
| Lisp | — | Scheme, Racket, Common Lisp, Emacs Lisp | Homoiconicidad, macros |
| Lógica y declarativa | **SQL** | Prolog, Datalog | Describir el qué, no el cómo |
| Concurrente / actor | — (CSP en **Go**) | Erlang, Elixir | Procesos, mensajes, tolerancia a fallos |
| Array / científica | — | APL, J, Julia, Fortran, MATLAB | Operar sobre vectores completos |
| Móvil / moderno | — | Swift, Dart | Apps nativas y multiplataforma |
| Históricos / shell | — | COBOL, Pascal, BASIC, Bash, PowerShell | Contexto histórico y automatización |

## 📇 Fichas de lenguaje

Cada cápsula resume **historia** (autor, año, motivo, de quién hereda), **características**
(paradigma, tipos, memoria y ejecución), **con qué se ejecuta** (compilador o intérprete y gestor
de paquetes), el mapa **"si ya sabes X…"** hacia un lenguaje del núcleo, y su **estado** actual.
El núcleo (Python, JavaScript, TypeScript, Java, C#, Go, Rust, C, SQL, PHP) no lleva ficha aquí:
se estudia a fondo en las clases.

## 🧱 Familia C / llaves

### C++

Bjarne Stroustrup empezó en 1979 en Bell Labs un proyecto llamado "C con clases", que en 1985 se
publicó como **C++**. La meta era añadir abstracción orientada a objetos a C sin sacrificar su
rendimiento ni su acceso al hardware. Hereda toda la sintaxis y el modelo de memoria de C, y suma
clases, plantillas (programación genérica), sobrecarga de operadores, excepciones y una enorme
biblioteca estándar (STL). Es **multiparadigma** (OO, genérico, procedimental y cada vez más
funcional), de **tipado estático** y **compilado a código nativo**, con **gestión manual** de
memoria apoyada hoy en punteros inteligentes (RAII) en lugar del `malloc`/`free` crudo. Se compila
con **g++**, **clang++** o **MSVC**, y sus dependencias se gestionan con **vcpkg** o **Conan**.
Si ya sabes **C**, C++ te sonará familiar en lo básico pero mucho más grande y con abstracciones
de coste cero. Está **muy vivo**: motores de juego, navegadores, sistemas embebidos, HPC y
finanzas. El estándar lo mantiene ISO ([isocpp.org](https://isocpp.org/)).

### Objective-C

Brad Cox y Tom Love lo crearon a inicios de los años 80 (hacia 1984) fusionando el modelo de
**mensajería de Smalltalk** con el lenguaje C. NeXT lo adoptó y, tras la compra por Apple, fue
durante décadas el lenguaje oficial de macOS e iOS. Es un **superconjunto estricto de C**: cualquier
programa C es válido, y encima se añade una capa OO dinámica con su característica sintaxis de
corchetes `[objeto mensaje]`. Es **multiparadigma** con **tipado estático** (con dinamismo en el
despacho de mensajes) y memoria gestionada por **conteo de referencias** (ARC, automático desde
2011). Se compila con **clang** dentro de **Xcode**; la gestión de dependencias histórica es
**CocoaPods**. Si ya sabes **C** y algo de OO, reconocerás el núcleo, pero el envío dinámico de
mensajes es su gran diferencia. Hoy está en **declive gestionado**: sigue vivo en bases de código
Apple heredadas, pero Swift lo ha reemplazado como lenguaje recomendado
([documentación de Apple](https://developer.apple.com/documentation/objectivec)).

### Zig

Andrew Kelley presentó Zig en 2016 como un lenguaje de sistemas moderno que pretende ser **"un mejor
C"** sin la complejidad de C++. Su lema es la ausencia de comportamientos ocultos: no hay
asignaciones de memoria implícitas, no hay flujo de control oculto y no hay preprocesador. Es
**procedimental**, de **tipado estático** y **compilado a código nativo**, con **gestión manual**
de memoria mediante *allocators* explícitos que se pasan como parámetros. Su rasgo estrella es
`comptime`: ejecución de código en tiempo de compilación que sustituye a las macros y a los
genéricos tradicionales. Trae **compilador propio** (que además puede compilar código C) y un
**sistema de build y gestor de paquetes integrados** desde la propia herramienta `zig`. Si ya sabes
**C**, Zig te resultará el pariente que arregla sus asperezas conservando el control total. Está en
**crecimiento activo pero aún pre-1.0**, popular en tooling y proyectos de sistemas
([ziglang.org](https://ziglang.org/)).

### Nim

Andreas Rumpf comenzó Nim en 2008 (bajo el nombre *Nimrod*) buscando un lenguaje tan expresivo como
Python pero tan eficiente como C. Su sintaxis usa **indentación significativa** al estilo Python,
pero **compila a C, C++ o JavaScript** y de ahí a un binario nativo veloz. Es **multiparadigma**
(imperativo, OO y funcional), de **tipado estático con inferencia**, y ofrece un **recolector de
basura configurable** (incluida la opción ORC, o gestión manual cuando hace falta). Destaca por su
sistema de **macros higiénicas** que operan sobre el AST, dándole poder de metaprogramación. Se usa
el **compilador `nim`** y el gestor de paquetes **Nimble**. Si ya sabes **Python** te enamorará la
sintaxis, y si vienes de **C** apreciarás el rendimiento y el binario autocontenido. Es un lenguaje
de **nicho pero maduro y estable**, con comunidad pequeña y dedicada
([nim-lang.org](https://nim-lang.org/)).

### D

Walter Bright, autor del primer compilador nativo de C++, diseñó D en 2001 en Digital Mars como un
rediseño de C++ que conservara su potencia eliminando su carga histórica. Es **multiparadigma**
(imperativo, OO, funcional y metaprogramación), de **tipado estático con inferencia** y **compilado
a nativo**. Su modelo de memoria es flexible: **recolección de basura por defecto**, pero permite
gestión manual y un subconjunto `@nogc` para código de tiempo real. Brilla en metaprogramación con
plantillas y ejecución en tiempo de compilación (CTFE). Cuenta con tres compiladores —**dmd**
(referencia), **ldc** (backend LLVM) y **gdc** (backend GCC)— y el gestor de paquetes **dub**. Si
ya sabes **C++**, D se siente como su versión ordenada y más rápida de escribir. Su estado es
**vivo pero de nicho**: comunidad estable, uso puntual en la industria
([dlang.org](https://dlang.org/)).

## 🐍 Familia Scripting dinámico

### Ruby

Yukihiro "Matz" Matsumoto publicó Ruby en Japón en 1995, buscando un lenguaje **optimizado para la
felicidad del programador**: elegante, consistente y agradable de leer. Es **totalmente orientado a
objetos** (hasta los números son objetos), con fuerte influencia de Smalltalk, Perl y Lisp. Su
tipado es **dinámico y de pato**, se **interpreta** (con compilación JIT en versiones recientes) y
gestiona memoria con **recolector de basura**. Es célebre por sus bloques, su expresividad y por el
framework web **Ruby on Rails**, que popularizó la "convención sobre configuración". Se ejecuta con
el intérprete de referencia **CRuby/MRI**, y sus dependencias se manejan con **RubyGems** y
**Bundler**. Si ya sabes **Python**, Ruby te resultará un primo cercano igual de dinámico pero más
orientado a expresiones y con una cultura de DSLs muy marcada. Sigue **vivo**, sobre todo en
desarrollo web y automatización ([ruby-lang.org](https://www.ruby-lang.org/)).

### Perl

Larry Wall creó Perl en 1987 como una "navaja suiza" para procesar texto y administrar sistemas
Unix, combinando ideas de C, sed, awk y los shells. Su filosofía es "hay más de una forma de
hacerlo" (TMTOWTDI). Es **multiparadigma**, de **tipado dinámico** con las famosas variables de
contexto (`$` escalar, `@` array, `%` hash), **interpretado** y con memoria gestionada por conteo
de referencias. Su gran fortaleza son las **expresiones regulares**, tan integradas que definieron
un estándar de facto (PCRE). Se ejecuta con el intérprete **`perl`** y su ecosistema histórico es
**CPAN**, uno de los repositorios de módulos más grandes y antiguos. Si ya sabes **Python** o
**PHP**, reconocerás el terreno del scripting, pero Perl es más denso y simbólico. Su estado es
**legado activo**: dominó la web de los 90 y hoy persiste en administración de sistemas, bioinformática
y scripts heredados ([perl.org](https://www.perl.org/)).

### Lua

Roberto Ierusalimschy, Luiz Henrique de Figueiredo y Waldemar Celes crearon Lua en 1993 en la
PUC-Rio de Brasil como un **lenguaje de scripting embebible**, ligero y portable. Su diseño prioriza
un intérprete diminuto que se incrusta fácilmente dentro de aplicaciones escritas en C. Es
**multiparadigma** apoyado en una única estructura de datos, la **tabla**, y en **tipado dinámico**;
se **interpreta** (con la variante **LuaJIT** para máxima velocidad) y usa **recolector de basura**.
No trae gran biblioteca estándar a propósito: su valor es ser el motor de scripting de otra cosa.
Se ejecuta con el intérprete **`lua`** y el gestor de paquetes **LuaRocks**. Si ya sabes
**JavaScript**, reconocerás las tablas como objetos y los prototipos. Está **muy vivo** como
lenguaje incrustado: videojuegos (Roblox, World of Warcraft), Redis, Nginx y Neovim
([lua.org](https://www.lua.org/)).

### Tcl

John Ousterhout diseñó Tcl (*Tool Command Language*) en 1988 como un lenguaje de comandos simple y
embebible para dar scripting a herramientas de ingeniería. Su principio radical es que **todo es una
cadena de texto**: comandos, valores y estructuras se representan como strings, lo que hace su
sintaxis minúscula y uniforme. Es **imperativo**, de **tipado dinámico** (con conversión perezosa
según el uso), **interpretado** y con memoria automática. Su compañero histórico es **Tk**, un kit
de widgets gráfico multiplataforma que también adoptaron Python y Perl. Se ejecuta con el intérprete
**`tclsh`** (o **`wish`** para GUI), y sus bibliotecas se distribuyen vía **Tcllib** y el sistema de
paquetes propio. Si ya sabes **Bash** o **Python**, encontrarás un scripting familiar pero con un
modelo de "todo texto" peculiar. Su estado es **legado de nicho**: automatización de EDA, testing
(Expect) y aplicaciones industriales de larga vida
([tcl-lang.org](https://www.tcl-lang.org/)).

### R

Ross Ihaka y Robert Gentleman crearon R en 1993 en la Universidad de Auckland como una
implementación libre del lenguaje **S** de Bell Labs, orientada a **estadística y análisis de
datos**. Es **multiparadigma** con un fuerte sesgo funcional y **vectorizado**: las operaciones se
aplican de forma natural a vectores y data frames completos. Su tipado es **dinámico**, se
**interpreta** y gestiona memoria con **recolector de basura**. Su verdadera potencia está en el
ecosistema: **CRAN**, con miles de paquetes estadísticos, y el conjunto **tidyverse** para
manipulación y visualización de datos (ggplot2). Se ejecuta con el intérprete **`R`** y los paquetes
se instalan con `install.packages()` desde **CRAN**. Si ya sabes **Python** con pandas y numpy,
verás un rival directo, pero R nació desde la estadística en vez de adaptarla. Está **muy vivo** en
academia, ciencia de datos, bioestadística y análisis
([r-project.org](https://www.r-project.org/)).

## ☕ Familia JVM

### Kotlin

JetBrains anunció Kotlin en 2011 y lanzó la versión 1.0 en 2016 como un lenguaje moderno para la
**JVM** que corrigiera las asperezas de Java manteniendo interoperabilidad total con él. Google lo
adoptó como lenguaje preferente para Android en 2017. Es **multiparadigma** (OO y funcional), de
**tipado estático con inferencia**, y destaca por su **seguridad frente a nulos** integrada en el
sistema de tipos. Corre sobre la **JVM** con **recolector de basura**, pero también compila a
**JavaScript** y a **binario nativo** (Kotlin/Native), lo que habilita proyectos multiplataforma.
Se compila con **kotlinc** y se construye con **Gradle** o **Maven**, reutilizando todo el
ecosistema de librerías de Java. Si ya sabes **Java**, Kotlin se siente como su versión concisa y
segura; la migración es gradual porque conviven en el mismo proyecto. Está **muy vivo**, dominante
en Android y creciente en backend ([kotlinlang.org](https://kotlinlang.org/)).

### Scala

Martin Odersky creó Scala en 2004 en la EPFL para **fusionar programación orientada a objetos y
funcional** de forma elegante sobre la JVM. Su nombre viene de "scalable language". Es
**multiparadigma** con un sistema de tipos muy potente (tipos algebraicos, inferencia, *traits*,
implicits/`given`), **estático**, ejecutado sobre la **JVM** con **recolector de basura** (con
backends a JS y nativo). Popularizó en el mundo JVM las funciones de orden superior, la coincidencia
de patrones y la inmutabilidad por defecto; es el lenguaje de **Apache Spark**. Se compila con
**scalac** y se construye con **sbt** o Maven. Si ya sabes **Java**, Scala te abre la puerta a la
programación funcional tipada sin salir de la JVM, aunque su curva es más pronunciada. Su estado es
**vivo pero maduro**: fuerte en big data, backend financiero y sistemas distribuidos
([scala-lang.org](https://www.scala-lang.org/)).

### Groovy

James Strachan propuso Groovy en 2003 (versión 1.0 en 2007) como un lenguaje **dinámico para la
JVM** con sintaxis cercana a Java pero mucho más ágil, inspirado en Ruby y Python. Es
**multiparadigma**, con **tipado dinámico opcionalmente estático**, ejecutado sobre la **JVM** con
**recolector de basura**. Reduce la ceremonia de Java (menos punto y coma, menos tipos explícitos)
y brilla creando **DSLs**, lo que lo hizo el lenguaje de scripting de **Gradle** y de la
automatización en **Jenkins**. Es casi un superconjunto de Java: pegar código Java suele funcionar.
Se ejecuta con **`groovy`** (o se compila con **`groovyc`**) y aprovecha dependencias vía **Grape**
o Gradle/Maven. Si ya sabes **Java**, Groovy es la manera más rápida de scriptear sobre la misma
plataforma sin recompilar todo. Su estado es **vivo de nicho**: build scripts, pipelines de CI y
testing (Spock) ([groovy-lang.org](https://groovy-lang.org/)).

### Clojure

Rich Hickey creó Clojure en 2007 como un **Lisp moderno para la JVM**, centrado en la
**inmutabilidad** y la programación funcional práctica. Es un dialecto de Lisp: código
**homoicónico** escrito con paréntesis, con macros potentes. Su tipado es **dinámico**, corre sobre
la **JVM** con **recolector de basura** (también existe ClojureScript hacia JavaScript), y sus
estructuras de datos son **persistentes e inmutables**. Su modelo de concurrencia —basado en STM,
átomos y agentes— busca eludir los problemas del estado mutable compartido. Se ejecuta como código
sobre la JVM y se gestiona con **Leiningen** o **tools.deps** (`deps.edn`), con acceso a todo el
ecosistema Java. Si vienes de **Java**, el salto conceptual es grande (de OO mutable a datos
funcionales), pero comparten plataforma y librerías. Está **vivo de nicho**: backend de datos,
fintech y equipos que valoran el enfoque funcional
([clojure.org](https://clojure.org/)).

## 🟦 Familia .NET

### F\#

Don Syme y Microsoft Research desarrollaron F#, lanzado en 2005, para llevar la tradición **ML** al
ecosistema **.NET**. Es un lenguaje **funcional primero** (aunque multiparadigma) con **tipado
estático e inferencia fuerte**, ejecutado sobre el **CLR** con **recolector de basura**. Ofrece
tipos algebraicos, coincidencia de patrones, inmutabilidad por defecto y *computation expressions*,
manteniendo interoperabilidad total con las librerías de .NET. Su indentación es significativa, al
estilo de OCaml, del que hereda directamente. Se compila con **`fsc`** dentro de las herramientas
**`dotnet`** y usa **NuGet** como gestor de paquetes. Si ya sabes **C#**, F# es la puerta a la
programación funcional tipada sin cambiar de plataforma: comparten runtime y bibliotecas, pero el
estilo es muy distinto (expresiones e inmutabilidad frente a OO imperativo). Está **vivo de nicho**:
finanzas, análisis de datos y equipos .NET que buscan robustez funcional
([fsharp.org](https://fsharp.org/)).

### VB.NET

Microsoft lanzó Visual Basic .NET en 2002 como la reencarnación del clásico Visual Basic (1991)
sobre la plataforma **.NET**, rompiendo la compatibilidad con el VB6 anterior a cambio de un modelo
OO completo. Su seña es una **sintaxis verbosa en inglés** (`If … Then … End If`) pensada para ser
legible y accesible a principiantes. Es **multiparadigma** con **tipado estático** (con opción de
enlace tardío), ejecutado sobre el **CLR** con **recolector de basura**; es funcionalmente
equivalente a C# porque comparten el mismo runtime y biblioteca base. Se compila con **`vbc`** vía
las herramientas **`dotnet`** y usa **NuGet**. Si ya sabes **C#**, VB.NET es literalmente el mismo
modelo con otra sintaxis más prosaica. Su estado es **legado en mantenimiento**: Microsoft ya no le
añade características de lenguaje nuevas, pero sigue soportado para las muchas aplicaciones
empresariales existentes
([documentación de Visual Basic](https://learn.microsoft.com/dotnet/visual-basic/)).

## λ Familia Funcional tipada (ML)

### Haskell

Haskell nació en 1990 del trabajo de un comité académico que buscaba unificar los lenguajes
funcionales perezosos en un estándar común; lleva el nombre del lógico **Haskell Curry**. Es el
lenguaje funcional puro por excelencia: **evaluación perezosa** por defecto, **funciones puras** y
efectos secundarios controlados mediante **mónadas**. Su tipado es **estático con inferencia
Hindley-Milner** y un sistema de clases de tipos muy expresivo; se **compila a nativo** con
**recolector de basura**. Es célebre por permitir razonamiento matemático sobre los programas y por
su influencia en casi todos los lenguajes modernos (incluidas las características funcionales de
Rust, Scala y Swift). Se compila con **GHC** y se gestiona con **Cabal** o **Stack**. Si ya sabes
las partes funcionales de **Rust** o de otro lenguaje tipado, Haskell las lleva al extremo purista.
Su estado es **vivo de nicho**: investigación, compiladores, fintech y verificación
([haskell.org](https://www.haskell.org/)).

### OCaml

OCaml procede del linaje **ML** desarrollado en el INRIA francés; la versión con objetos data de
1996 (Caml existía desde finales de los 80). Combina programación **funcional, imperativa y
orientada a objetos** con un énfasis en la practicidad y la velocidad de compilación. Su tipado es
**estático con inferencia** y tipos algebraicos con coincidencia de patrones; **compila a código
nativo** muy eficiente (o a bytecode) y usa **recolector de basura**. Es conocido por su solidez y
por ser la base de proyectos como el compilador de Rust en sus inicios, la herramienta de facto en
verificación y el lenguaje de trading de Jane Street. Se compila con **ocamlopt/ocamlc** y se
gestiona con **opam** (paquetes) y **dune** (build). Si ya sabes **Rust**, reconocerás las
enumeraciones, el pattern matching y la inferencia: Rust bebió directamente de aquí. Está **vivo de
nicho**: finanzas, compiladores y herramientas formales
([ocaml.org](https://ocaml.org/)).

### Elm

Evan Czaplicki presentó Elm en 2012 como su tesis: un lenguaje **funcional puro dedicado a
interfaces web** que compila a JavaScript y promete **cero excepciones en tiempo de ejecución**. Es
funcional al estilo ML —**tipado estático con inferencia**, tipos algebraicos, inmutabilidad total—
pero con un diseño deliberadamente pequeño y amable con los principiantes. Introdujo **la
Arquitectura Elm** (modelo, actualización, vista), un patrón unidireccional que inspiró a Redux en
el mundo React. No hay efectos secundarios sueltos: todo pasa por un runtime controlado, y su
compilador es famoso por mensajes de error extraordinariamente claros. Se usa el **compilador
`elm`**, que trae su propio gestor de paquetes (`elm install`). Si ya sabes **JavaScript** o
**TypeScript**, Elm te ofrece garantías mucho más fuertes a cambio de un ecosistema más cerrado. Su
estado es **vivo de nicho**, con desarrollo pausado pero comunidad fiel
([elm-lang.org](https://elm-lang.org/)).

## 🔬 Familia Lisp

### Scheme

Guy Steele y Gerald Sussman crearon Scheme en 1975 en el MIT como un dialecto **minimalista y
elegante de Lisp**, diseñado para ser conceptualmente limpio y fácil de razonar. Su filosofía es
dar pocas primitivas muy poderosas en lugar de muchas características. Es **funcional primero** (con
soporte imperativo), de **tipado dinámico**, **homoicónico** (código y datos comparten forma) y con
**recolección de basura**. Fue pionero en tratar las funciones como ciudadanos de primera clase con
alcance léxico y en formalizar las **continuaciones** y la **recursión de cola**. Durante décadas
fue el lenguaje del célebre libro y curso *SICP*. Tiene muchas implementaciones (Chez Scheme, Guile,
Racket, MIT/GNU Scheme), cada una con su propio empaquetado. Si ya sabes cualquier lenguaje del
núcleo, Scheme te enseña los fundamentos desde la raíz. Su estado es **vivo de nicho**: enseñanza,
investigación y scripting embebido (GNU Guile)
([sitio de R7RS](https://standards.scheme.org/)).

### Racket

Racket comenzó en 1995 como *PLT Scheme* y se renombró en 2010; es un descendiente de Scheme
convertido en **plataforma para crear lenguajes**. Su gran idea es que construir lenguajes de
dominio específico es una actividad de primera clase: incluye herramientas para definir tu propia
sintaxis y semántica. Es **multiparadigma** (funcional, OO, lógico según el módulo), de **tipado
dinámico** (con un dialecto tipado, Typed Racket), **homoicónico** y con **recolección de basura**.
Trae un entorno completo, **DrRacket**, muy usado en educación. Se ejecuta con **`racket`** y se
gestiona con **`raco pkg`**. Si ya sabes **Python** como lenguaje de propósito general, Racket
ofrece una experiencia comparable de "baterías incluidas" pero con la potencia de macros de Lisp.
Está **vivo de nicho**: enseñanza de programación (libro *How to Design Programs*), investigación en
lenguajes y prototipado ([racket-lang.org](https://racket-lang.org/)).

### Common Lisp

Common Lisp surgió a mediados de los 80 (estandarizado por ANSI en 1994) para **unificar la dispersa
familia de dialectos Lisp** en un estándar industrial común. Es un Lisp grande y pragmático,
**multiparadigma**, con un potente sistema de objetos (**CLOS**) que incluye herencia múltiple y
métodos multi-despacho. Su tipado es **dinámico** (con anotaciones opcionales), **homoicónico** con
un sistema de macros muy potente, y usa **recolección de basura**. Su rasgo distintivo es la
**imagen viva**: se desarrolla modificando un sistema en ejecución, con recompilación incremental de
funciones. Implementaciones comunes son **SBCL** (compila a nativo) y **CCL**, y las librerías se
obtienen con **Quicklisp**. Si vienes de cualquier lenguaje del núcleo, Common Lisp representa un
paradigma interactivo y maleable distinto a todos. Su estado es **legado vivo de nicho**: sistemas
expertos, aviación (antes), y una comunidad pequeña muy productiva
([common-lisp.net](https://common-lisp.net/)).

### Emacs Lisp

Richard Stallman escribió Emacs Lisp en 1985 como el lenguaje de extensión del editor **GNU Emacs**.
Es un dialecto de Lisp diseñado no para programas autónomos, sino para **configurar y programar el
propio editor**: casi toda la funcionalidad de Emacs está escrita en él y puede redefinirse en
caliente. Es **multiparadigma**, de **tipado dinámico**, **interpretado** (con compilación a
bytecode y, desde 2021, compilación nativa vía libgccjit) y con **recolección de basura**. No tiene
gestor de paquetes independiente: los paquetes se instalan **dentro de Emacs** mediante `package.el`
desde archivos como **MELPA**. Si ya sabes algo de **Scheme** o Lisp, reconocerás el modelo; si no,
es el ejemplo vivo de una aplicación completamente programable por su usuario. Su estado es **vivo**
mientras Emacs lo esté: sigue siendo el corazón de uno de los editores más longevos y extensibles
([manual de Emacs Lisp](https://www.gnu.org/software/emacs/manual/eintr.html)).

## 🔗 Familia Lógica y declarativa

### Prolog

Alain Colmerauer y Philippe Roussel crearon Prolog en 1972 en Marsella como el lenguaje insignia de
la **programación lógica**. En lugar de describir pasos, el programador declara **hechos y reglas**,
y el motor busca soluciones mediante **unificación** y **backtracking** automático. Es
**declarativo**, de **tipado dinámico**, **interpretado** (o compilado a bytecode) y con memoria
automática. Un programa es esencialmente una base de conocimiento sobre la que se hacen consultas;
el orden de ejecución lo decide el resolutor, no una secuencia de instrucciones. Fue central en la
IA simbólica y en el proyecto japonés de "quinta generación". Implementaciones habituales son
**SWI-Prolog** y **GNU Prolog**, con un sistema de paquetes propio (`pack` en SWI). Si ya sabes
**SQL**, reconocerás el enfoque declarativo de "describir el qué"; Prolog lo extiende a inferencia
lógica general. Está **vivo de nicho**: procesamiento de lenguaje, razonamiento y enseñanza de IA
([swi-prolog.org](https://www.swi-prolog.org/)).

### Datalog

Datalog surgió en la comunidad de bases de datos deductivas a finales de los años 70 y 80 como un
**subconjunto de Prolog** deliberadamente restringido para garantizar **terminación y consultas
decidibles**. Elimina las funciones y limita la recursión de forma que toda consulta finaliza, lo
que lo hace ideal como lenguaje de consulta declarativo sobre grandes conjuntos de hechos. Es
**declarativo** y lógico: se definen relaciones mediante reglas, y el motor calcula el cierre de
todo lo derivable (evaluación *bottom-up*). No es un único producto sino una familia de dialectos
integrados en herramientas: **Soufflé** (análisis estático de programas), motores de bases de datos
como **Datomic** y sistemas de análisis. Si ya sabes **SQL**, Datalog te resultará familiar como
lenguaje declarativo, pero maneja con naturalidad la **recursión** (grafos, jerarquías) que en SQL
es engorrosa. Su estado es **vivo de nicho** y en auge dentro de análisis de código y razonamiento
sobre datos ([Soufflé, un motor Datalog](https://souffle-lang.github.io/)).

## 📨 Familia Concurrente / actor

### Erlang

Joe Armstrong, Robert Virding y Mike Williams crearon Erlang en Ericsson en 1986 (liberado como
software libre en 1998) para construir **sistemas de telecomunicaciones** con alta disponibilidad y
tolerancia a fallos. Su modelo es el de **actores**: procesos ligerísimos y aislados que solo se
comunican por **paso de mensajes**, sin memoria compartida. Es **funcional**, de **tipado dinámico**,
ejecutado sobre la máquina virtual **BEAM** con **recolección de basura por proceso**. Su filosofía
distintiva es "**deja que falle**": los procesos que fallan son supervisados y reiniciados en vez de
programarse a la defensiva, y el código puede actualizarse **en caliente** sin detener el sistema.
Se ejecuta con **`erl`** (BEAM) y se construye con **rebar3**. Si ya conoces la concurrencia CSP de
**Go**, Erlang ofrece un modelo emparentado pero con actores aislados y supervisión. Está **vivo**:
mensajería (WhatsApp), telecomunicaciones y sistemas de alta disponibilidad
([erlang.org](https://www.erlang.org/)).

### Elixir

José Valim creó Elixir en 2011 para llevar la **robustez de la plataforma Erlang/BEAM** a una
sintaxis moderna y productiva inspirada en Ruby. Compila a la máquina virtual **BEAM** y hereda todo
su modelo: **actores** ligeros, paso de mensajes, supervisión y tolerancia a fallos. Es
**funcional**, de **tipado dinámico**, con **recolección de basura** e inmutabilidad por defecto.
Añade sobre Erlang herramientas de primera clase: **macros** para metaprogramación, tuberías (`|>`)
y una excelente experiencia de desarrollo. Su framework web **Phoenix** (con LiveView) lo hizo
popular para aplicaciones en tiempo real. Se ejecuta con **`elixir`** sobre BEAM y se gestiona con
**Mix** y el repositorio de paquetes **Hex**. Si ya sabes **Ruby**, la sintaxis te encantará; si
vienes de **Go**, reconocerás el foco en concurrencia. Está **vivo y en crecimiento**: web en tiempo
real, sistemas distribuidos y streaming ([elixir-lang.org](https://elixir-lang.org/)).

## 🔢 Familia Array / científica

### APL

Kenneth Iverson desarrolló APL (*A Programming Language*) en IBM; su notación es de 1962 y la
implementación ejecutable llegó hacia 1966. Es el pionero de la **programación de arrays**: las
operaciones se aplican a **matrices y vectores completos** de una vez, sin bucles explícitos. Su
rasgo más famoso es un **conjunto de símbolos especiales** (`⍴`, `⍳`, `⌿`…) que expresan operaciones
complejas en muy pocos caracteres, lo que produce programas extraordinariamente concisos. Es
**funcional y de arrays**, de **tipado dinámico**, **interpretado** y con memoria automática.
Requiere teclado o mapeo especial para sus glifos. La implementación de referencia moderna es
**Dyalog APL** (comercial), y existe **GNU APL** libre. Si ya sabes trabajar vectorizado (como con
numpy en **Python**), APL es la raíz filosófica de todo eso, llevada al extremo. Su estado es
**legado vivo de nicho**: finanzas cuantitativas y actuariales
([dyalog.com](https://www.dyalog.com/)).

### J

Kenneth Iverson (autor de APL) y Roger Hui diseñaron J en 1990 como sucesor de APL que usara
únicamente **caracteres ASCII** en lugar de los símbolos especiales, para portabilidad. Conserva la
esencia de la **programación de arrays** —operar sobre datos multidimensionales completos— pero
reemplaza los glifos por combinaciones de signos de puntuación (`+/`, `i.`, `#`). Es **funcional y
de arrays**, de **tipado dinámico**, **interpretado** y con memoria automática, y añade una potente
**programación tácita** (definir funciones combinando otras sin nombrar los argumentos). Se ejecuta
con el intérprete **`jconsole`** y tiene su propio sistema de addons. Si ya sabes el estilo
vectorizado de **Python** con numpy, J te muestra hasta dónde llega esa idea, aunque su sintaxis es
críptica al principio. Su estado es **nicho vivo**: análisis matemático, finanzas y programación
recreativa, con una comunidad pequeña y entusiasta
([jsoftware.com](https://www.jsoftware.com/)).

### Julia

Jeff Bezanson, Stefan Karpinski, Viral Shah y Alan Edelman presentaron Julia en 2012 (desde el MIT)
para resolver el "problema de los dos lenguajes": tener la **facilidad de Python** y la **velocidad
de C** en uno solo, orientado a la **computación científica**. Es **multiparadigma** con un modelo
central de **despacho múltiple**, **tipado dinámico con inferencia** y **compilación JIT** vía LLVM,
lo que le da rendimiento cercano al nativo. Trae operaciones vectorizadas, aritmética de alto nivel
y excelente interoperabilidad con C, Fortran y Python. Se ejecuta con **`julia`** y su gestor de
paquetes integrado, **Pkg**, muy cuidado. Si ya sabes **Python** para ciencia de datos, Julia ofrece
una sintaxis parecida pero sin el cuello de botella de rendimiento que obliga a reescribir en C. Está
**vivo y en crecimiento**: computación numérica, machine learning, investigación y HPC
([julialang.org](https://julialang.org/)).

### Fortran

John Backus dirigió en IBM la creación de Fortran (*Formula Translation*) en 1957, el **primer
lenguaje de alto nivel** ampliamente usado y compilado. Nació para expresar **fórmulas matemáticas**
de cálculo científico de forma legible en vez de en ensamblador. Es **imperativo y procedimental**
(con módulos y programación orientada a objetos añadidos en estándares modernos), de **tipado
estático**, **compilado a nativo** y con **gestión de memoria** manual/estática pensada para
rendimiento máximo. Sigue siendo referencia en **álgebra lineal y cálculo numérico** (BLAS, LAPACK
están escritos en Fortran) por sus arreglos multidimensionales eficientes y su optimización madura.
Se compila con **gfortran** o **ifx**, y ya cuenta con un gestor de paquetes moderno, **fpm**. Si
ya sabes **C**, reconocerás la compilación a nativo, pero Fortran es más orientado a arreglos y
menos a punteros. Su estado es **legado muy vivo**: supercomputación, clima, física e ingeniería
([fortran-lang.org](https://fortran-lang.org/)).

### MATLAB

Cleve Moler creó MATLAB (*Matrix Laboratory*) a finales de los años 70 como interfaz sencilla a las
librerías de álgebra lineal LINPACK/EISPACK, y en 1984 se fundó **MathWorks** para comercializarlo.
Su unidad fundamental es la **matriz**, y todo el lenguaje gira en torno a operar sobre arreglos
completos. Es **imperativo y vectorizado**, de **tipado dinámico**, **interpretado** (con JIT
interno) y memoria automática. Su fuerza no es solo el lenguaje sino el **entorno integrado**:
editor, depurador, visualización y sobre todo los **toolboxes** especializados (control, señales,
imágenes) que dominan la ingeniería. Es **software comercial y propietario**, con extensiones desde
su Add-On Explorer; la alternativa libre más cercana es **GNU Octave**. Si ya sabes **Python** con
numpy, verás un competidor directo enfocado a ingeniería. Su estado es **muy vivo** en la industria
y la academia de ingeniería, biomédica y control
([mathworks.com](https://www.mathworks.com/products/matlab.html)).

## 📱 Familia Móvil / moderno

### Swift

Apple presentó Swift en 2014, liderado por Chris Lattner (creador de LLVM), como el **sucesor de
Objective-C** para desarrollar en todo su ecosistema, con una sintaxis moderna, segura y agradable.
Es **multiparadigma** (OO, funcional y protocolar), de **tipado estático con inferencia**, con
**seguridad frente a nulos** mediante *optionals* y coincidencia de patrones. **Compila a nativo**
vía LLVM y gestiona memoria con **conteo automático de referencias (ARC)**, sin recolector de basura
en pausa. Se volvió de **código abierto** en 2015 y hoy corre también en Linux y Windows. Se compila
con **swiftc** y se gestiona con el **Swift Package Manager**. Si ya sabes **TypeScript** o **Rust**,
reconocerás los optionals, la inferencia y los enums con datos asociados; Swift mezcla esa seguridad
con una ergonomía muy pulida. Está **muy vivo**: es el lenguaje principal de iOS, macOS y demás
plataformas Apple, además de algo de backend ([swift.org](https://www.swift.org/)).

### Dart

Lars Bak y Kasper Lund crearon Dart en Google en 2011, inicialmente como alternativa a JavaScript
para la web. Encontró su verdadero propósito con **Flutter**, el framework de UI multiplataforma que
lo convirtió en la elección para apps móviles, web y escritorio desde una sola base de código. Es
**orientado a objetos** con clases, de **tipado estático con inferencia** (y seguridad frente a
nulos), y tiene un modelo de ejecución dual: **compilación JIT** durante el desarrollo (recarga en
caliente) y **compilación AOT a nativo** para producción, además de transpilar a **JavaScript**.
Usa **recolección de basura**. Se ejecuta con la herramienta **`dart`** y el gestor de paquetes
**pub** (pub.dev). Si ya sabes **JavaScript** o **TypeScript**, Dart te resultará muy familiar en
sintaxis pero más estructurado y con tipos sólidos. Está **muy vivo**, impulsado por la adopción de
Flutter ([dart.dev](https://dart.dev/)).

## 🗄️ Familia Históricos / shell

### COBOL

COBOL (*Common Business-Oriented Language*) fue definido en 1959 por el comité CODASYL, con fuerte
influencia del trabajo de **Grace Hopper**, para estandarizar el **procesamiento de datos de
negocio** en un lenguaje legible por gestores. Su sintaxis es **verbosa y parecida al inglés**
(`ADD TAX TO PRICE GIVING TOTAL`), pensada para claridad administrativa más que para concisión. Es
**imperativo y procedimental**, de **tipado estático** con precisión decimal exacta (crucial en
finanzas), **compilado** y con memoria estática. Domina la lógica de **bancos, seguros y gobiernos**
desde hace más de sesenta años, procesando volúmenes enormes de transacciones en mainframes. Se
compila con **IBM Enterprise COBOL** en entornos corporativos o con el libre **GnuCOBOL**. No se
parece a ningún lenguaje del núcleo en estilo, pero conceptualmente su tratamiento de registros y
datos anticipa a las estructuras y a **SQL**. Su estado es **legado crítico y muy vivo**: sostiene
infraestructura financiera esencial y hay demanda de mantenimiento
([sitio de GnuCOBOL](https://gnucobol.sourceforge.io/)).

### Pascal

Niklaus Wirth diseñó Pascal en 1970 como un lenguaje **para enseñar buena programación
estructurada**, claro y disciplinado, en reacción a la permisividad de otros lenguajes de la época.
Es **imperativo y procedimental**, de **tipado estático fuerte**, **compilado a nativo** y con
gestión de memoria manual mediante punteros. Introdujo o popularizó estructuras limpias
(`begin`/`end`, tipos definidos por el usuario, records) que influyeron en generaciones de
lenguajes. Su descendiente comercial **Object Pascal / Delphi** añadió orientación a objetos y
dominó el desarrollo rápido de aplicaciones Windows en los 90. Hoy se compila sobre todo con el
libre **Free Pascal (`fpc`)**, con Delphi vivo en el ámbito comercial. Si ya sabes **C**,
reconocerás el modelo compilado y los punteros, pero Pascal es más estricto y legible. Su estado es
**legado de nicho**: enseñanza histórica, mantenimiento de aplicaciones Delphi y algunos proyectos
nuevos con Free Pascal/Lazarus ([freepascal.org](https://www.freepascal.org/)).

### BASIC

John Kemeny y Thomas Kurtz crearon BASIC en el Dartmouth College en 1964 con un objetivo explícito:
un lenguaje **fácil para principiantes** de cualquier disciplina, no solo para ingenieros. Es
**imperativo y procedimental**, de **tipado dinámico o débil** según el dialecto, e históricamente
**interpretado** línea a línea, lo que lo hacía inmediato para experimentar. Con la microinformática
de los 80 (con sus versiones con números de línea y `GOTO`) fue el primer contacto con la
programación para millones de personas en los ordenadores domésticos. Evolucionó en muchos
dialectos: **Visual Basic**, **VBA** (dentro de Office), **FreeBASIC** y **QB64**. No es un único
producto ni tiene un gestor de paquetes común. Si ya sabes **Python**, reconocerás la vocación de
accesibilidad, pero BASIC es mucho más antiguo y fragmentado. Su estado es **legado**: histórico en
su forma clásica, pero vivo en VBA para automatización de ofimática
([documentación de VBA](https://learn.microsoft.com/office/vba/api/overview/)).

### Bash

Brian Fox escribió Bash (*Bourne Again SHell*) en 1989 para el proyecto GNU como reemplazo libre del
shell **Bourne** (`sh`) de Unix. Es a la vez el **intérprete de comandos interactivo** por defecto
en la mayoría de sistemas Linux y macOS (durante años) y un **lenguaje de scripting** para
automatizar tareas del sistema. Es **imperativo**, de **tipado dinámico basado en cadenas** (todo es
texto), **interpretado** y orientado a **encadenar programas** mediante tuberías y redirecciones. No
compila ni tiene gestor de paquetes propio: su fuerza es orquestar las utilidades del sistema
operativo. Se ejecuta con el intérprete **`bash`**. Si ya sabes cualquier lenguaje del núcleo, Bash
es la pegatina que conecta procesos, archivos y programas en la línea de comandos, con una sintaxis
peculiar y llena de trampas de comillas. Su estado es **omnipresente y muy vivo**: automatización,
CI/CD, despliegues y administración de sistemas
([manual de GNU Bash](https://www.gnu.org/software/bash/manual/)).

### PowerShell

Microsoft lanzó PowerShell en 2006, diseñado por Jeffrey Snover, como un shell de automatización
moderno para Windows y, desde 2016 en su versión **multiplataforma y de código abierto**, también
para Linux y macOS. Su idea rompedora frente a los shells Unix es que la tubería transporta
**objetos .NET**, no texto plano: los comandos (*cmdlets*, con nombres `Verbo-Sustantivo`) pasan
datos estructurados que se pueden filtrar por propiedades sin analizar cadenas. Es **imperativo y
orientado a objetos**, de **tipado dinámico** apoyado en el sistema de tipos del **CLR**,
**interpretado**, con acceso completo a la plataforma .NET. Se ejecuta con **`pwsh`** (o
`powershell` en Windows heredado) y sus módulos se instalan desde la **PowerShell Gallery** con
`Install-Module`. Si ya sabes **Bash**, reconocerás la vocación de automatización pero con un
paradigma de objetos en lugar de texto; y si sabes **C#**, verás la plataforma .NET por debajo. Está
**muy vivo** en administración de Windows, la nube y DevOps
([documentación de PowerShell](https://learn.microsoft.com/powershell/)).

## Por qué esta capa existe

Meter 40 lenguajes con implementación completa multiplicaría el mantenimiento sin multiplicar el
aprendizaje: **muchos son casi el mismo lenguaje con otra piel**. El Atlas captura esa amplitud por
comprensión; el núcleo captura la profundidad por práctica verificada.

## Mantenimiento de las fichas

Estas cápsulas se **revisan periódicamente** (última revisión: 2026-07). Los hechos históricos son
estables, pero las herramientas, versiones y gestores de paquetes cambian: ante cualquier detalle
operativo, la documentación oficial enlazada manda. El **núcleo** de 10 lenguajes —Python,
JavaScript, TypeScript, Java, C#, Go, Rust, C, SQL y PHP— no se resume aquí porque **se estudia e
implementa a fondo en las clases** ([índice completo](../classes/README.md)).
