# 🟠 Kotlin — 2011

> [⬅️ Atlas](README.md) · [🗂️ Todas las fichas](lenguajes.md) · [📚 Índice de clases](../classes/README.md)

Kotlin es lo que pasa cuando una empresa que hace herramientas de desarrollo —JetBrains— diseña un
lenguaje: **cada decisión responde a un problema concreto que habían visto miles de veces en código
[Java](java.md) real**. No inventa paradigmas; **quita fricción**, y esa modestia es la razón de su
éxito.

> **🎯 Por qué está en este programa**
>
> Kotlin es un **primo de la familia JVM** ([Atlas](README.md#jvm)), cuyo representante en el núcleo
> es [Java](java.md).
>
> Aporta al programa la comparación más didáctica de todo el Atlas: **el mismo programa, en la misma
> máquina virtual, con la misma biblioteca — y la mitad de líneas**. Y aporta dos conceptos concretos:
> **la nulabilidad en el sistema de tipos** (clase 100) y **las corrutinas con concurrencia
> estructurada**
> ([clase 134](../classes/parte-8-como-funcionan-los-lenguajes/134-corrutinas-generadores-y-canales/README.md)).

| | |
|---|---|
| **Año** | 2011; **1.0** en 2016; oficial en Android desde 2017; **2.0** en 2024 |
| **Autoría** | **JetBrains**, con Andrey Breslav al frente del diseño inicial |
| **Familia** | JVM; con influencia de [Scala](scala.md), [C#](csharp.md), Groovy y ML |
| **Paradigma** | Multiparadigma: OO y funcional, con orientación a DSL |
| **Tipado** | **Estático, con inferencia** y **nulabilidad en el tipo** |
| **Memoria** | La de la JVM; en Native, con conteo de referencias |
| **Ejecución** | Bytecode JVM; también **Kotlin/Native**, **Kotlin/JS** y **Kotlin/Wasm** |
| **Estado** | 🟢 **Oficial en Android**, en crecimiento en servidor y multiplataforma |

---

## 📜 Historia

JetBrains hacía **IntelliJ IDEA**, y su producto estaba escrito en Java. En **2010** tenían dos
problemas: Java evolucionaba despacio —los genéricos habían tardado ocho años, las lambdas tardarían
diez— y [Scala](scala.md), que les gustaba, **compilaba demasiado lento** para una base de código de
su tamaño.

Así que hicieron el suyo, con dos requisitos poco habituales y muy reveladores:

1. **Interoperabilidad total con Java, en las dos direcciones.** Nada de migrar: **poder mezclar
   ficheros `.java` y `.kt` en el mismo proyecto**.
2. **Compilar tan rápido como Java.**

Esa primera decisión es la que explica la adopción: **no hubo que elegir**. Es la estrategia opuesta a
la de [D](d.md) frente a C++ (clase 175), y funcionó.

El punto de inflexión llegó en **2017**, cuando **Google anunció Kotlin como lenguaje oficial de
Android**, y en **2019** lo declaró preferente. El contexto ayudaba: Google estaba en pleito con
Oracle por las APIs de Java, y Kotlin ofrecía una salida.

**Kotlin 2.0 (2024)** trajo el compilador **K2**, con mejoras grandes de velocidad, y consolidó
**Kotlin Multiplatform**: el mismo código de negocio compilado a JVM, a nativo para iOS, a JavaScript
y a WebAssembly.

## 🏭 Dónde vive hoy

- **Android**: es el lenguaje por defecto; la mayoría de las aplicaciones nuevas se escriben en
  Kotlin.
- **Servidores**: Spring Boot tiene soporte de primera clase, y **Ktor** es el marco nativo del
  ecosistema.
- **Multiplataforma móvil**: **Compose Multiplatform** comparte interfaz y lógica entre Android, iOS,
  escritorio y web.
- **Guiones de construcción**: **Gradle** usa Kotlin como DSL de configuración (clase 163).
- **Herramientas y datos**: como sustituto de Java en proyectos nuevos de la JVM.

## 🧠 Lo que enseña: la nulabilidad en el tipo

Es la aportación más transferible de esta ficha (clase 100):

```kotlin
var nombre: String = "Ana"
nombre = null           // ✗ NO COMPILA

var apodo: String? = null    // ← el ? declara que puede faltar
println(apodo?.length)        // llamada segura: si es nulo, da nulo
println(apodo ?: "sin apodo")  // operador Elvis: valor por defecto
println(apodo!!.length)         // afirmación: falla si es nulo
```

**Tony Hoare llamó a la referencia nula "su error del billón de dólares"**, y Kotlin lo resuelve como
[Rust](rust.md), [Swift](swift.md) y [Elm](elm.md): **separando en el sistema de tipos lo que puede
faltar de lo que no**.

Y el segundo concepto, las **corrutinas con concurrencia estructurada**:

```kotlin
coroutineScope {                       // ← el ÁMBITO es la clave
    val a = async { pedirUsuario() }
    val b = async { pedirPedidos() }
    procesar(a.await(), b.await())
}   // si algo falla aquí dentro, se CANCELA todo lo lanzado en este ámbito
```

**La concurrencia estructurada** significa que **una tarea no puede sobrevivir al ámbito que la lanzó**
(clase 135). Eso elimina de raíz las tareas huérfanas y las cancelaciones a medias, que son el
problema clásico del código asíncrono — y es una idea que después han adoptado Java (Loom), Swift y
Python.

Y hay una tercera cosa que Kotlin hace especialmente bien y que la clase 163 aprovecha: **los DSL**.

```kotlin
dependencies {                 // ← esto es Kotlin, no un formato de configuración
    implementation("org.jetbrains:annotations:24.0.0")
}
```

**Las lambdas con receptor y las funciones de extensión** permiten construir lenguajes de dominio que
parecen configuración y **están comprobados por el compilador** — que es lo que Gradle usa.

## 🔄 Lo que se ha modernizado

- **Compilador K2 (2.0)**: mucho más rápido, con mejor inferencia y análisis compartido entre
  plataformas.
- **Kotlin Multiplatform** estable: lógica compartida y interfaz nativa, con `expect`/`actual` para
  lo específico de cada plataforma.
- **Kotlin/Wasm** con WasmGC (clase 162).
- **Clases de valor** (`value class`) sin coste en ejecución, y **contratos** que ayudan al análisis
  de flujo.
- **Y `kotlinx` completo**: serialización con generación de código en compilación —sin reflexión
  (clase 159)—, fechas, corrutinas y entrada/salida.

## ⚙️ Cómo se ejecuta hoy

```bash
kotlinc main.kt -include-runtime -d venta.jar && java -jar venta.jar
kotlin main.kts                                     # como guion, sin compilar

./gradlew build test                                 # lo habitual (clases 143 y 147)
./gradlew ktlintCheck detekt                          # estilo y análisis (clase 146)
```

## 🧪 El programa de la clase 041 en Kotlin

```kotlin
fun main() {
    val (precio, cantidad, descuento) = readLine()!!.split(" ").map { it.toDouble() }
    val total = precio * cantidad * (1 - descuento)
    println("Total: %.2f".format(total))
}
```

**Lo que hay que ver, comparando con [Java](java.md) línea a línea.**

- **Cuatro líneas frente a quince**, sobre la misma máquina virtual y con la misma biblioteca. Esa
  comparación es, por sí sola, el argumento del lenguaje.
- **La desestructuración `val (a, b, c)`** no existe en Java, y es de las cosas que más se echan de
  menos al volver.
- **El `!!` después de `readLine()`** es la nulabilidad en acción: `readLine()` devuelve `String?`
  porque **puede no haber línea**, y `!!` afirma que la hay. **En Java eso sería un `null` silencioso
  esperando a explotar**, y aquí está escrito en el código.
- **`val` es inmutable** —`var` es la mutable—, y la convención del ecosistema es usar `val` por
  defecto (clase 102), igual que [Rust](rust.md) y [Scala](scala.md).
- **`"%.2f".format(total)`** llama por debajo a `String.format` de Java: **la interoperabilidad no es
  una capa, es el mismo objeto**. Y por eso `Locale` sigue siendo una trampa a vigilar, igual que en
  Java.

## 📚 Fuentes y bibliografía

- [kotlinlang.org/docs](https://kotlinlang.org/docs/home.html) — documentación oficial, con el
  [tour interactivo](https://kotlinlang.org/docs/kotlin-tour-welcome.html).
- [Guía de convenciones de código](https://kotlinlang.org/docs/coding-conventions.html) — la de la
  clase 146.
- **Dmitry Jemerov, Svetlana Isakova, Roman Elizarov**, *Kotlin in Action*, 2.ª ed., Manning — el
  libro de referencia; Elizarov diseñó las corrutinas.
- **Marcin Moskała**, *Effective Kotlin* — 50 elementos al estilo de *Effective Java*.
- [Blog de Kotlin y KEEP](https://github.com/Kotlin/KEEP) — las propuestas de evolución, con su
  discusión.

---

⏮️ [Volver al Atlas](README.md) · 🗂️ [Todas las fichas](lenguajes.md) ·
🔗 Relacionadas: [Java](java.md) · [Scala](scala.md) · [Swift](swift.md) · [Groovy](groovy.md) ·
[C#](csharp.md)
