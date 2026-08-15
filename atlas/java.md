# ☕ Java — 1995

> [⬅️ Atlas](README.md) · [🗂️ Todas las fichas](lenguajes.md) · [📚 Índice de clases](../classes/README.md)

Java es el lenguaje que llevó la máquina virtual y la recolección de basura al software empresarial
del mundo entero. Treinta años después sigue moviendo los sistemas de banca, seguros y comercio de
media Europa — y, después de una década de fama de lento y verboso, **ha cambiado más en los últimos
seis años que en los veinte anteriores**.

> **🎯 Por qué está en este programa**
>
> **Java es uno de los diez lenguajes del núcleo** y el **representante de la familia JVM**
> ([Atlas](README.md#jvm)): quien entiende la versión Java de una clase reconoce después
> [Kotlin](kotlin.md), [Scala](scala.md), [Groovy](groovy.md) y —con más esfuerzo—
> [Clojure](clojure.md), porque **los cuatro compilan al mismo bytecode y comparten biblioteca**.
>
> Y aporta al programa los conceptos de **máquina virtual con JIT**
> ([clases 125 y 126](../classes/parte-8-como-funcionan-los-lenguajes/README.md)), **recolección de
> basura generacional** (clase 131) y **orientación a objetos nominal con interfaces** (clase 112),
> que son los que definieron la práctica de la industria durante veinte años.

| | |
|---|---|
| **Año** | 1995; **5** con genéricos (2004); **8** con lambdas (2014); **cada 6 meses** desde 2017 |
| **Autoría** | **James Gosling** y equipo, Sun Microsystems (hoy Oracle) |
| **Familia** | JVM; sintaxis de C, semántica influida por [Smalltalk](smalltalk.md) y Objective-C |
| **Paradigma** | Orientado a objetos con clases; funcional desde Java 8 |
| **Tipado** | **Estático, nominal y fuerte**; con genéricos por borrado |
| **Memoria** | **Recolección de basura**; varios recolectores intercambiables |
| **Ejecución** | Bytecode sobre la JVM, con **JIT** de dos niveles; también AOT con GraalVM |
| **Estado** | 🟢 **Dominante** en sistemas empresariales y en el ecosistema de datos |

---

## 📜 Historia

En **1991**, Sun montó el proyecto *Green* para hacer software de electrodomésticos: un mando a
distancia inteligente. **James Gosling** diseñó un lenguaje llamado **Oak** —por un roble que veía
desde su ventana— con dos requisitos que resultaron proféticos: **portabilidad entre chips distintos**
y **seguridad**, porque el código iba a viajar.

El mercado de la televisión interactiva no llegó, pero en **1995** llegó la web, y Sun reposicionó el
lenguaje como **Java**, con el eslogan **"write once, run anywhere"** y los *applets* en el navegador.
Los applets murieron; **la máquina virtual sobrevivió y ganó**.

Los hitos que lo formaron:

- **Java 2 / J2EE (1999)**: el servidor de aplicaciones y toda la arquitectura empresarial.
- **Java 5 (2004)**: **genéricos** —implementados por *borrado* para no romper la compatibilidad
  binaria, una decisión que se discute desde entonces (clase 143)—, anotaciones, `enum`, `for-each`.
- **Java 7 (2011)**: `try-with-resources` (clase 132), NIO.2.
- **Java 8 (2014)**: **lambdas y `Stream`** — el cambio más grande de su historia, que llevó lo
  funcional al lenguaje empresarial (clase 115).
- **2017**: cambio a **una versión cada seis meses**, con versiones de soporte largo cada dos años
  (11, 17, 21, 25).
- **Java 21 (2023)**: **hilos virtuales** (Project Loom), emparejamiento de patrones, clases selladas.

Y por el camino, el **juicio Oracle contra Google** sobre las APIs de Java —resuelto en 2021 a favor
del uso legítimo— definió jurisprudencia sobre si una interfaz de programación se puede copiar.

## 🏭 Dónde vive hoy

- **Banca, seguros y administración**: el lenguaje al que se migra el [COBOL](cobol.md) cuando se
  migra (clase 175).
- **Android**: durante quince años el lenguaje oficial; hoy comparte sitio con [Kotlin](kotlin.md).
- **Datos a gran escala**: Hadoop, Spark, Kafka, Flink, Elasticsearch, Cassandra — el ecosistema de
  datos está escrito en Java y en [Scala](scala.md).
- **Servidores de aplicaciones**: Spring y Jakarta EE mueven una parte enorme del software corporativo.
- **Herramientas**: Maven, Gradle, IntelliJ, Jenkins.

## 🧠 Lo que enseña: la máquina virtual como decisión de arquitectura

Java es el sitio donde mejor se ve el compromiso central de las clases 125 y 126:

```text
Compilar a bytecode y ejecutarlo en una máquina virtual con JIT da:
  + portabilidad real entre sistemas y arquitecturas
  + optimización con información de EJECUCIÓN, que un compilador estático no tiene
  + recolección de basura, seguridad de memoria y verificación del bytecode
  − arranque más lento y consumo de memoria mayor
  − y pausas del recolector, que en latencia baja importan (clase 152)
```

**El JIT con información de ejecución merece el detalle**, porque es contraintuitivo: **la JVM puede
generar código más rápido que un compilador estático** en ciertos casos, porque sabe **qué rama se
toma siempre** y **qué tipo llega de verdad a un método polimórfico**, y compila especializando —con
una comprobación de guarda por si cambia—.

Es exactamente la **caché de envío en línea** que se inventó en [Smalltalk](smalltalk.md) y en Self
(clase 152), y es la razón por la que el despacho dinámico dejó de ser caro.

Y el otro concepto que Java llevó a la industria es el de la clase 112: **la interfaz como contrato
sin implementación**, con herencia simple de clases y múltiple de interfaces — la respuesta al problema
del diamante que [C++](cpp.md) tiene abierto.

## 🔄 Lo que se ha modernizado

- **Hilos virtuales (Java 21)**: millones de hilos ligeros gestionados por la JVM, con **código
  secuencial** en lugar de asíncrono (clases 133 y 135). Es la respuesta de Java al modelo de
  [Go](go.md) y de [Erlang](erlang.md), y sin cambiar la forma de escribir el código.
- **Registros, clases selladas y emparejamiento de patrones**: tipos de datos algebraicos, la idea de
  [Haskell](haskell.md) y [OCaml](ocaml.md) llegando al lenguaje empresarial (clase 100).
- **`var`** para inferencia local, y ficheros de una sola clase ejecutables sin `main` ceremonioso.
- **GraalVM con imagen nativa**: compilación anticipada a binario, con **arranque de milisegundos** —
  lo que hace competitivo a Java en funciones sin servidor y en contenedores (clase 174).
- **Recolectores modernos**: **ZGC** y **Shenandoah**, con pausas por debajo del milisegundo incluso
  con montones de terabytes.
- **Panama**: interoperabilidad con C **sin JNI** (clase 156), con memoria fuera del montón segura.

## ⚙️ Cómo se ejecuta hoy

```bash
javac Main.java && java Main < entrada.txt     # el camino de la clase 041
java Main.java                                  # desde Java 11: sin compilar antes

mvn verify        # o: gradle build             (clase 143)
java -jar app.jar
native-image -jar app.jar                        # GraalVM: binario nativo (clase 174)
```

## 🧪 El programa de la clase 041 en Java

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Locale;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] p = br.readLine().trim().split("\\s+");

        // Tipado estático nominal: cada valor declara su tipo.
        final double precioUnitario = Double.parseDouble(p[0]);
        final int cantidad = Integer.parseInt(p[1]);
        final double descuento = Double.parseDouble(p[2]);

        double subtotal = precioUnitario * cantidad;
        double total = subtotal * (1 - descuento);

        System.out.printf(Locale.US, "Total: %.2f%n", total);
    }
}
```

**Lo que hay que ver, comparando con las otras fichas.**

- **La ceremonia es la seña de identidad**: clase, método estático, tipos declarados y excepción
  propagada. [Kotlin](kotlin.md) y [Groovy](groovy.md) hacen lo mismo en tres líneas sobre la misma
  máquina virtual, y esa comparación es exactamente el contenido del Atlas.
- **`final` sí es una constante**, a diferencia de la convención de mayúsculas de
  [Python](python.md) (clase 041) — aunque `final` sobre una referencia solo fija **el nombre**, no
  el objeto (clase 102).
- **`Locale.US` no es decorativo**: sin él, en una máquina con configuración española, `%.2f`
  imprimiría `27000,00` con coma. Es la misma trampa que `CultureInfo.InvariantCulture` en
  [C#](csharp.md) y [VB.NET](vbnet.md), y una de las causas más frecuentes de que una prueba pase en
  local y falle en el servidor (clase 147).
- **`int` y `double` son primitivos**, no objetos: Java tiene dos mundos de tipos, y el
  autoboxing entre ellos cuesta memoria y tiempo (clase 128). Es una de las cosas que Project Valhalla
  está en camino de resolver.

## 📚 Fuentes y bibliografía

- [Documentación de Java (Oracle)](https://docs.oracle.com/en/java/javase/) y las
  [JEP](https://openjdk.org/jeps/0) — cada característica nueva, con su motivación.
- [Especificación del lenguaje y de la JVM](https://docs.oracle.com/javase/specs/) — para la clase 125.
- **Joshua Bloch**, *Effective Java*, 3.ª ed., Addison-Wesley — el libro de referencia; 90 elementos
  que explican no solo qué hacer sino por qué.
- **Brian Goetz et al.**, *Java Concurrency in Practice* — anterior a Loom y todavía imprescindible
  para entender el modelo de memoria (clase 136).
- **Ben Evans, Jason Clark, Martijn Verburg**, *The Well-Grounded Java Developer*, 2.ª ed., Manning —
  Java moderno, con la JVM por dentro.

---

⏮️ [Volver al Atlas](README.md) · 🗂️ [Todas las fichas](lenguajes.md) ·
🔗 Relacionadas: [Kotlin](kotlin.md) · [Scala](scala.md) · [Groovy](groovy.md) ·
[Clojure](clojure.md) · [C#](csharp.md) · [Smalltalk](smalltalk.md)
