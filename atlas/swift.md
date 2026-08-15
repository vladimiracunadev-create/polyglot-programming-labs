# 🕊️ Swift — 2014

> [⬅️ Atlas](README.md) · [🗂️ Todas las fichas](lenguajes.md) · [📚 Índice de clases](../classes/README.md)

Swift es el sucesor de [Objective-C](objective-c.md), y su diseño se puede resumir en una frase:
**tomar todo lo que la investigación en lenguajes había demostrado y meterlo en un lenguaje que
millones de personas iban a usar el mes siguiente**. Tipos algebraicos, opcionales, inmutabilidad por
defecto y concurrencia estructurada — con la interfaz gráfica de Apple detrás.

> **🎯 Por qué está en este programa**
>
> Swift es un **primo de la familia móvil / moderno** ([Atlas](README.md#movil-moderno)), junto a
> [Dart](dart.md), y desciende directamente de [Objective-C](objective-c.md).
>
> Aporta al programa **la gestión de memoria por conteo automático de referencias sin recolector**
> ([clase 131](../classes/parte-8-como-funcionan-los-lenguajes/131-recoleccion-de-basura/README.md)),
> con el problema de los ciclos a la vista; y **la concurrencia estructurada con actores integrados en
> el sistema de tipos** (clases 133 y 136), que es de las implementaciones más completas que existen.

| | |
|---|---|
| **Año** | 2014; **ABI estable** en 2019; **Swift 6** en 2024, con concurrencia estricta |
| **Autoría** | **Chris Lattner** —creador de LLVM— y equipo, Apple |
| **Familia** | Móvil / moderno; con [Objective-C](objective-c.md), Rust, Haskell y C# dentro |
| **Paradigma** | Multiparadigma: OO por protocolos, funcional e imperativo |
| **Tipado** | **Estático, fuerte, con inferencia** y opcionales en el tipo |
| **Memoria** | **ARC**: conteo automático de referencias, sin recolector y sin pausas |
| **Ejecución** | Compilado a nativo sobre **LLVM** |
| **Estado** | 🟢 **Dominante** en el ecosistema Apple; creciendo en servidor y embebido |

---

## 📜 Historia

**Chris Lattner** había creado **LLVM** como proyecto de máster y lo había llevado a Apple, donde se
convirtió en la base de todas sus herramientas. En **2010** empezó Swift **en secreto**, y Apple lo
presentó en la WWDC de **2014** sin previo aviso.

El encargo era difícil: **sustituir a [Objective-C](objective-c.md)** —treinta años de marcos y de
código— **sin romper nada**. La solución fue la interoperabilidad total: **Swift y Objective-C
conviven en el mismo proyecto**, y Swift importa las APIs de Objective-C con tipos precisos gracias a
las anotaciones de nulabilidad que Apple añadió a Objective-C **precisamente para eso**.

Los hitos:

- **Swift 3 (2016)**: rediseño de la biblioteca y de los nombres; **la última ruptura grande**.
- **Swift 5 (2019)**: **ABI estable** —el lenguaje deja de tener que incluir su biblioteca en cada
  aplicación (clase 157)—.
- **Swift 5.5 (2021)**: `async`/`await`, **actores** y concurrencia estructurada.
- **Swift 6 (2024)**: **comprobación estricta de concurrencia** — el compilador detecta las carreras
  de datos, con un modelo emparentado con el de [Rust](rust.md) (clase 136).

Y desde **2015 es de código abierto**, con versiones para Linux y Windows y un empuje serio hacia el
servidor y los sistemas embebidos.

## 🏭 Dónde vive hoy

- **Todo el ecosistema Apple**: iOS, macOS, watchOS, visionOS — con **SwiftUI** como marco declarativo
  de interfaz (clase 169).
- **Servidores**: **Vapor** y **Hummingbird**; Apple lo usa en su propia infraestructura.
- **Sistemas embebidos**: *Embedded Swift* (2024), un subconjunto sin tiempo de ejecución para
  microcontroladores — el mismo camino que [Ada](ada.md) con su perfil reducido (clase 162).
- **Y en interoperabilidad con [C++](cpp.md)**, un desarrollo reciente que le abre bibliotecas
  existentes (clase 156).

## 🧠 Lo que enseña: ARC y concurrencia en el tipo

**Uno, el conteo automático de referencias** (clase 131):

```swift
class Nodo {
    var siguiente: Nodo?          // referencia FUERTE: mantiene vivo
    weak var padre: Nodo?          // DÉBIL: no cuenta, y se pone a nil al morir
    unowned let dueño: Documento    // sin dueño: no cuenta y NO se pone a nil
}
```

**El compilador inserta `retain` y `release`**, así que no hay recolector y **no hay pausas** — lo que
importa mucho en una animación a 120 fotogramas por segundo (clase 152).

**Y el precio es el que la clase 131 explica: los ciclos no se recogen.** Dos objetos que se apuntan
mutuamente con referencias fuertes **no se liberan nunca**, y **el programador tiene que romper el
ciclo** con `weak` o `unowned`.

**Es el mismo modelo que [Objective-C](objective-c.md) con ARC, que [Rust](rust.md) con `Rc`/`Weak` y
que el conteo de referencias de [Python](python.md) y [PHP](php.md)** — con la diferencia de que estos
dos últimos **sí** tienen un detector de ciclos adicional.

**Dos, la concurrencia en el sistema de tipos** (clase 136):

```swift
actor Banco {
    private var saldo = 0.0            // ← nadie puede tocarlo desde fuera sin await
    func depositar(_ x: Double) { saldo += x }
}

let b = Banco()
await b.depositar(100)                  // ← el await marca el cruce de frontera
```

**Un actor aísla su estado**: solo se accede desde dentro, y desde fuera **hay que esperar**. El
compilador lo garantiza (clase 133).

**Y `Sendable`** es el otro lado: un tipo marcado como `Sendable` **puede cruzar fronteras de
concurrencia con seguridad**, y **el compilador comprueba que no se envía nada que no lo sea**. Es
exactamente el papel de `Send`/`Sync` en [Rust](rust.md), integrado en un lenguaje con ARC.

**Y tres, los opcionales**, que ya no sorprenden a nadie precisamente porque Swift ayudó a
popularizarlos:

```swift
var nombre: String = "Ana"      // no puede ser nil
var apodo: String? = nil         // puede
if let a = apodo { ... }          // desempaquetado seguro
guard let a = apodo else { return }
```

## 🔄 Lo que se ha modernizado

- **Swift 6 con concurrencia estricta**: las carreras de datos pasan a ser errores de compilación.
- **Macros** (5.9): metaprogramación con transformación del árbol sintáctico, comprobada y depurable
  (clase 122) — a diferencia de las macros de texto de [C](c.md).
- **SwiftUI y Observation**: interfaz declarativa con estado observable (clase 169).
- **Embedded Swift**: sin recolector, sin reflexión y sin metadatos, para microcontroladores.
- **Interoperabilidad con C++** bidireccional, y **Swift en Windows y Linux** con soporte oficial.
- **Y `swift-format` y SwiftLint** para el estilo (clase 146).

## ⚙️ Cómo se ejecuta hoy

```bash
swift main.swift < entrada.txt        # ejecutar como guion
swiftc -O main.swift -o venta          # compilar optimizado

swift build && swift test               # con Swift Package Manager (clases 143 y 139)
swift package init --type executable
```

## 🧪 El programa de la clase 041 en Swift

Esta versión se escribe aquí y **no está verificada en CI** (clase 040).

```swift
import Foundation

guard let linea = readLine() else { exit(1) }
let v = linea.split(separator: " ").compactMap { Double($0) }
guard v.count == 3 else { exit(1) }

let total = v[0] * v[1] * (1 - v[2])
print(String(format: "Total: %.2f", total))
```

**Lo que hay que ver.**

- **`guard let ... else`** es la forma idiomática de Swift para el camino de error: **desempaqueta el
  opcional y sale si no hay valor**, dejando el resto de la función sin anidamiento. Compárese con el
  `!` de [Kotlin](kotlin.md) y de [Dart](dart.md), que afirma en lugar de comprobar.
- **`readLine()` devuelve `String?`** porque puede no haber línea — **la posibilidad de fallo está en
  el tipo**, y el compilador obliga a tratarla (clase 116).
- **`compactMap` convierte y descarta los nulos a la vez**: `Double($0)` devuelve `Double?`, y
  `compactMap` se queda con los que valen. Es un idioma muy del lenguaje.
- **`let` es inmutable**, `var` es mutable, y la convención es `let` por defecto (clase 102) — como
  [Rust](rust.md), [Kotlin](kotlin.md) y [Scala](scala.md).
- **Y `String(format:)` viene de Foundation**, que es **la biblioteca de
  [Objective-C](objective-c.md)**: la herencia se ve en la primera línea del programa.

## 📚 Fuentes y bibliografía

- [The Swift Programming Language](https://docs.swift.org/swift-book/) — el libro oficial, libre y
  muy bien escrito.
- [Swift Evolution](https://github.com/swiftlang/swift-evolution) — **todas las propuestas con su
  discusión pública**; de lo mejor que hay para entender por qué un lenguaje toma sus decisiones
  (clase 175).
- [Swift.org](https://www.swift.org/documentation/) — para el uso en servidor y multiplataforma.
- **Paul Hudson**, *Hacking with Swift* — libre en línea; el recurso práctico más usado.
- **Chris Lattner**, entrevistas y charlas sobre el diseño de Swift y de LLVM (clase 123).

---

⏮️ [Volver al Atlas](README.md) · 🗂️ [Todas las fichas](lenguajes.md) ·
🔗 Relacionadas: [Objective-C](objective-c.md) · [Rust](rust.md) · [Kotlin](kotlin.md) ·
[Dart](dart.md) · [C++](cpp.md)
