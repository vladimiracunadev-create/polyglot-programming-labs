# 🎸 Groovy — 2003

> [⬅️ Atlas](README.md) · [🗂️ Todas las fichas](lenguajes.md) · [📚 Índice de clases](../classes/README.md)

Groovy es **[Java](java.md) sin la ceremonia**: casi todo programa Java es un programa Groovy válido,
y a partir de ahí se puede ir quitando —los tipos, los puntos y coma, los `getters`— hasta que quede
algo que parece [Python](python.md) o [Ruby](ruby.md). Su mayor éxito no fue como lenguaje de
aplicación, sino **como lenguaje de configuración programable**.

> **🎯 Por qué está en este programa**
>
> Groovy es un **primo de la familia JVM** ([Atlas](README.md#jvm)), cuyo representante en el núcleo
> es [Java](java.md).
>
> Aporta al programa el caso más visible de **lenguaje incrustado como DSL**
> ([clase 163](../classes/parte-10-interoperabilidad-y-fronteras-entre-lenguajes/163-incrustar-un-lenguaje-en-otro-lua-python-embebido/README.md)):
> **los `build.gradle` y los `Jenkinsfile` que millones de personas editan sin saber que están
> escribiendo Groovy**. Y aporta el concepto de **tipado dinámico y estático en el mismo lenguaje,
> elegible por anotación** (clase 146).

| | |
|---|---|
| **Año** | 2003; **1.0** en 2007; **2.0** con compilación estática (2012); **4.x** actual |
| **Autoría** | **James Strachan** y **Bob McWhirter**; hoy proyecto de Apache |
| **Familia** | JVM; sintaxis de Java con influencia de [Python](python.md), [Ruby](ruby.md) y Smalltalk |
| **Paradigma** | OO y funcional; muy orientado a construir DSL |
| **Tipado** | **Dinámico por defecto**, con `@CompileStatic` para comprobación estática |
| **Memoria** | La de la JVM |
| **Ejecución** | Bytecode JVM, con despacho dinámico; estático con la anotación |
| **Estado** | 🟢 **Muy usado como DSL** (Gradle, Jenkins); poco como lenguaje de aplicación |

---

## 📜 Historia

**James Strachan** empezó Groovy en **2003** con una idea directa: **la JVM es excelente y Java es
verboso**; hagamos un lenguaje dinámico que se apoye en toda la biblioteca de Java y que se lea como
Python.

El proyecto pasó por dificultades —Strachan lo abandonó, y en 2009 comentó que si hubiera conocido
[Scala](scala.md) antes probablemente no lo habría empezado— y lo rescató la comunidad, con SpringSource
y después **Apache**.

Su éxito real llegó por un camino lateral, que es lo interesante de esta ficha:

- **Gradle (2007)** eligió Groovy como lenguaje de sus ficheros de construcción, y Gradle acabó siendo
  el sistema de construcción de **Android** y de buena parte del mundo JVM.
- **Jenkins (2016)** adoptó Groovy para sus canalizaciones declarativas — los `Jenkinsfile` que
  definen la integración continua de miles de empresas (clase 147).
- **Grails** llevó la filosofía de [Rails](ruby.md) a la JVM.

Y de ahí una situación curiosa: **muchísima gente edita Groovy a diario sin saber que lo hace**.

**Groovy 2.0 (2012)** añadió `@CompileStatic` y `@TypeChecked`, que permiten pedir comprobación
estática y rendimiento de Java **por clase o por método**.

## 🏭 Dónde vive hoy

- **Gradle**: los `build.gradle` clásicos son Groovy (hoy compite con el DSL de
  [Kotlin](kotlin.md)).
- **Jenkins**: las canalizaciones, declarativas o de guion, son Groovy (clase 171).
- **Pruebas**: **Spock**, un marco de pruebas con una sintaxis de especificación excelente, muy usado
  incluso en proyectos Java (clase 139).
- **Guiones de administración en la JVM**, con acceso directo a todas las bibliotecas Java.
- **Grails**, en aplicaciones heredadas y en algunos proyectos nuevos.

## 🧠 Lo que enseña: un lenguaje que se convierte en configuración

Este bloque es Groovy, y casi nadie lo piensa así:

```groovy
plugins { id 'java' }

repositories { mavenCentral() }

dependencies {
    implementation 'org.apache.commons:commons-lang3:3.14.0'
    testImplementation 'junit:junit:4.13.2'
}
```

**Cada línea es una llamada a un método con un bloque** — el mecanismo es el de la clase 163: **una
sintaxis que permite omitir paréntesis y pasar bloques hace que el código parezca configuración**.

**Y la consecuencia buena**: cuando la configuración se queda corta, **no hay que salir a otro
lenguaje**, porque ya se está en uno completo. Se puede poner un `if`, un bucle o una función.

**Y la consecuencia mala, que la clase 163 advierte**: un `build.gradle` puede ejecutar cualquier
cosa. **La configuración deja de ser declarativa**, se vuelve imposible de analizar sin ejecutarla, y
es una superficie de ataque en la cadena de suministro (clase 153).

Es exactamente la tensión que la clase 163 plantea, y Groovy es su mejor ejemplo cotidiano.

Y el segundo concepto es el tipado elegible:

```groovy
def suma(a, b) { a + b }                    // dinámico: se resuelve en ejecución

@CompileStatic
int sumaRapida(int a, int b) { a + b }       // ← estático: bytecode como el de Java
```

**El mismo lenguaje, dos modos**, decididos con una anotación. Es tipado gradual (clase 146) llevado
al nivel del método.

## 🔄 Lo que se ha modernizado

- **`@CompileStatic`** y `@TypeChecked` con extensiones de comprobación propias.
- **Groovy 4** sobre Java 17+, con registros, `switch` de expresión y soporte de las novedades de la
  JVM.
- **`invokedynamic`** como mecanismo de despacho, que acercó el rendimiento del modo dinámico al de
  Java.
- **Spock** como marco de pruebas de referencia, con bloques `given/when/then` y **aserciones que
  muestran todos los valores intermedios al fallar** — lo mismo que Catch2 hace en
  [C++](cpp.md) (clase 139).
- **Y la competencia sana con el DSL de Kotlin en Gradle**, que ha empujado a los dos.

## ⚙️ Cómo se ejecuta hoy

```bash
groovy main.groovy < entrada.txt         # el comando de la clase 041
groovyc Venta.groovy && java -cp .:$GROOVY_HOME/lib/groovy.jar Venta

gradle build                              # ← esto ejecuta Groovy (o Kotlin)
```

## 🧪 El programa de la clase 041 en Groovy

```groovy
def (precio, cantidad, descuento) = System.in.newReader().readLine().split(' ')*.toDouble()
def total = precio * cantidad * (1 - descuento)
printf("Total: %.2f%n", total)
```

**Lo que hay que ver.**

- **Una sola línea hace lo que en [Java](java.md) ocupa cinco**, y usa **exactamente las mismas
  clases**: `System.in`, `BufferedReader`, `String.split`. La interoperabilidad es total.
- **`*.toDouble()` es el operador de expansión (*spread*)**: aplica el método **a cada elemento** de
  la colección. Es el `map` de otros lenguajes convertido en sintaxis, y no existe en Java.
- **`def` no significa "sin tipo"**: significa **tipo dinámico**. Con `@CompileStatic` estas mismas
  líneas se comprobarían en compilación.
- **`printf` con `%n`** en lugar de `\n` — el separador de línea de la plataforma, herencia de Java.
- **Y no hay clase ni `main`**: un guion Groovy se ejecuta tal cual, lo que es la razón de que sirva
  como lenguaje de configuración.

## 📚 Fuentes y bibliografía

- [groovy-lang.org](https://groovy-lang.org/documentation.html) — documentación oficial de Apache
  Groovy; el apartado de DSL es directamente material de la clase 163.
- [Guía de Gradle](https://docs.gradle.org/current/userguide/userguide.html) — para ver el lenguaje
  en su uso real.
- [Spock Framework](https://spockframework.org/) — el marco de pruebas; merece conocerse aunque el
  proyecto sea Java (clase 139).
- **Ken Kousen**, *Making Java Groovy*, Manning — cómo se combinan los dos en un proyecto real.
- **Dierk König et al.**, *Groovy in Action*, 2.ª ed., Manning — la referencia completa.

---

⏮️ [Volver al Atlas](README.md) · 🗂️ [Todas las fichas](lenguajes.md) ·
🔗 Relacionadas: [Java](java.md) · [Kotlin](kotlin.md) · [Ruby](ruby.md) · [Python](python.md) ·
[Tcl](tcl.md)
