# 🎈 Smalltalk — década de 1970

> [⬅️ Atlas](README.md) · [🧟 Lenguajes que siguen vivos](vivos.md) · [📚 Índice de clases](../classes/README.md)

**El lenguaje del que salió casi todo.** La orientación a objetos tal como la entendemos, el patrón
MVC, las pruebas unitarias, el refactoring como práctica, las metodologías ágiles y hasta la interfaz
gráfica con ventanas y ratón: todo eso se cocinó en el mismo sitio, alrededor de Smalltalk, en Xerox
PARC.

> **🎯 Por qué está en este programa**
>
> **Criterio de inclusión: Smalltalk se ejecuta hoy en producción**, en banca, seguros, *trading* y
> logística. Cincom desarrolla y vende **VisualWorks** y **ObjectStudio**, GemTalk mantiene
> **GemStone/S** (base de datos de objetos usada en sistemas financieros) y **Pharo** publica
> versiones nuevas cada año con una comunidad activa.
>
> Entra porque **lleva al extremo el concepto central de la
> [Parte 7](../classes/parte-7-paradigmas/README.md)**: aquí la orientación a objetos no es *una
> forma de organizar el código*, es **la única forma que existe**. No hay tipos primitivos fuera del
> sistema de objetos, no hay operadores, y —esto es lo que sorprende— **no hay estructuras de
> control**. `if`, `while` y `for` no son sintaxis: son mensajes enviados a objetos. Ver un lenguaje
> donde `ifTrue:` es un método de la clase `Boolean` es lo que hace que "todo es un objeto" deje de
> ser un eslogan y pase a ser una consecuencia comprobable.

| | |
|---|---|
| **Año** | Smalltalk-71/72/76 en Xerox PARC; **Smalltalk-80** es la versión difundida |
| **Autoría** | **Alan Kay**, **Dan Ingalls**, **Adele Goldberg** y el Learning Research Group de PARC |
| **Familia** | Orientada a objetos pura, con influencia de Simula y Lisp |
| **Paradigma** | **OO puro**, basado en paso de mensajes |
| **Tipado** | **Dinámico** y fuerte; sin declaraciones de tipo |
| **Memoria** | Recolector de basura (Smalltalk fue pionero en GC generacional) |
| **Ejecución** | Máquina virtual con **imagen** de estado persistente; JIT en las VM modernas |
| **Estado** | 🟡 **Nicho vivo** — banca, seguros, trading, telecomunicaciones, investigación |

---

## 📜 Historia

**Alan Kay** llegó a Xerox PARC a comienzos de los 70 con una pregunta que no era de ingeniería sino
casi filosófica: si los ordenadores iban a ser personales, ¿cómo debería ser un sistema que un niño
pudiera entender y modificar? Su respuesta —influida por Simula, por Lisp, por LOGO y por la biología
celular— fue construir un sistema donde todo estuviera hecho de **objetos autónomos que se comunican
enviándose mensajes**, sin poder tocar el interior de los demás.

Kay ha insistido después en que la palabra "objeto" desvió la atención: lo importante era el **paso de
mensajes**, no las clases. La distinción explica por qué Smalltalk se siente distinto de Java o C++,
que tomaron las clases y dejaron el resto.

De ese laboratorio salió, en pocos años, una cantidad desproporcionada de lo que hoy es normal:

- La **interfaz gráfica** con ventanas superpuestas, iconos, menús y ratón, que Steve Jobs vio en su
  visita de 1979 y llevó al Lisa y al Macintosh.
- El patrón **MVC** (*Model-View-Controller*), formulado por **Trygve Reenskaug** durante su estancia
  en PARC en 1979.
- **SUnit**, el marco de pruebas unitarias que **Kent Beck** escribió en Smalltalk y que, portado a
  Java como **JUnit**, definió cómo se prueban hoy casi todos los lenguajes.
- El **refactoring** como disciplina con herramienta: el *Refactoring Browser* de Ralph Johnson y
  John Brant fue el primero que automatizó transformaciones de código con seguridad.
- La **programación extrema (XP)** y buena parte del movimiento ágil, nacidas en la comunidad
  Smalltalk de los 90 alrededor del proyecto C3 de Chrysler.
- Y, en gran medida, el libro ***Design Patterns*** de la Banda de los Cuatro, cuyos ejemplos y
  vocabulario vienen de esta tradición.

**Smalltalk-80** fue la versión que salió de PARC al mundo, documentada en el célebre "Libro Azul" de
Goldberg y Robson. Después vinieron las implementaciones comerciales —ParcPlace, Digitalk,
IBM VisualAge— y, cuando el mercado se movió a Java a finales de los 90, la retirada a los nichos
donde el software ya estaba escrito y funcionaba demasiado bien para tirarlo.

## 🏭 Dónde sobrevive hoy

- **Banca y finanzas**: sistemas de riesgo y valoración de derivados. El caso más documentado es
  **Kapital**, la plataforma de riesgo de JPMorgan, escrita en Smalltalk y mantenida durante décadas.
- **Seguros**: motores de tarificación y gestión de pólizas.
- **Logística y manufactura**: planificación y control de producción.
- **Telecomunicaciones**: sistemas de provisión y facturación.
- **Investigación y enseñanza**: **Pharo** y **Squeak** son entornos vivos; Squeak sostiene además
  **Scratch**, cuyo primer motor se escribió en Smalltalk.

## 🧠 Por qué no ha muerto

**1. La imagen: un sistema vivo, no un fichero fuente.** En Smalltalk no compilas y ejecutas: entras
en un **entorno que ya está corriendo** y lo modificas. La *imagen* es una instantánea completa del
estado del sistema —objetos, clases, ventanas abiertas, pilas de ejecución— que se guarda y se
restaura. Puedes detener un proceso en producción, abrir el depurador, **cambiar el método que
falló, y continuar la misma llamada** sin reiniciar. Ningún lenguaje del núcleo ofrece eso.

**2. Uniformidad absoluta.** Seis palabras reservadas y una sola regla: enviar mensajes. La sintaxis
completa cabe en una postal. Esa uniformidad es la que permite herramientas tan potentes: si todo es
un objeto y todo es un mensaje, el navegador de clases, el depurador y el refactorizador pueden
razonar sobre cualquier cosa.

**3. Productividad demostrada en dominios complejos.** En modelado de negocio con reglas intrincadas
—riesgo, seguros, planificación—, el ciclo de exploración interactiva de Smalltalk sigue siendo
competitivo. Por eso los sistemas que quedaron no se han reescrito.

**4. Reescribir tiene un coste desproporcionado.** Décadas de reglas modeladas como objetos vivos, sin
esquema externo que documente el dominio.

> **Y una honestidad necesaria:** la imagen también es su mayor problema. Es difícil de meter en un
> flujo moderno de Git, revisión de código y CI, porque el "fuente" no es un árbol de ficheros sino
> un estado binario. Las herramientas actuales (Tonel, Iceberg, Metacello en Pharo) resuelven bastante,
> pero la fricción cultural con el resto de la industria es real y explica parte de su declive.

## 🔄 Lo que se ha modernizado

- **Git de verdad.** El problema histórico —el código vive en una imagen binaria— está resuelto:
  **Tonel** guarda cada clase y método como ficheros de texto legibles, e **Iceberg** integra Pharo
  con Git y GitHub. Hoy un proyecto Smalltalk se revisa por *pull request* como cualquier otro.
- **Pharo publica una versión al año**, con máquina virtual JIT, compilación *ahead-of-time*
  experimental, soporte de ARM64 (Apple Silicon y Raspberry Pi) y 64 bits.
- **Web moderna**: **Seaside** (aplicaciones con estado sobre continuaciones), **Teapot** y **Zinc**
  para APIs REST y clientes HTTP, y **Pharo JS** para compilar a JavaScript.
- **Integración continua**: los proyectos Pharo se construyen en GitHub Actions con imágenes
  descargadas desde un guion, lo que hace posible el CI sobre un lenguaje basado en imágenes.
- **Metacello** como gestor de dependencias y versiones de proyecto.
- **Glamorous Toolkit**, construido sobre Pharo, propone el "entorno moldeable": herramientas de
  análisis y visualización creadas a medida del sistema que estás estudiando. Es de las ideas más
  originales que ha salido de la comunidad en la última década.

## ⚙️ Cómo se ejecuta hoy

**[Pharo](https://pharo.org/)** es hoy la puerta de entrada: libre, activo y con excelente material
de aprendizaje.

```bash
# Descargar el lanzador o la imagen desde pharo.org
./pharo Pharo.image eval "3 + 4"
# 7

# Ejecutar un script desde fichero
./pharo Pharo.image st total.st
```

**Implementaciones actuales:** **Pharo** (libre, la más activa), **Squeak** (libre, descendiente
directa del Smalltalk-80 original con parte del equipo de PARC detrás), **Cincom VisualWorks** y
**ObjectStudio** (comerciales, las de los grandes sistemas empresariales), **GemStone/S** (base de
datos de objetos), **VA Smalltalk** de Instantiations, y **Glamorous Toolkit**, un entorno de
"programación moldeable" construido sobre Pharo.

## 🧪 El programa de la clase 041 en Smalltalk

> ⚠️ **Material de lectura, no verificado.** Ejecutar Pharo en modo *headless* dentro del CI es
> posible pero pesado; no está en los *runners* de este repositorio.

```smalltalk
| linea partes precio cantidad descuento total |

linea := stdin nextLine.
partes := linea substrings collect: [ :cada | cada asNumber ].

precio    := partes first.
cantidad  := partes second.
descuento := partes third.

total := precio * cantidad * (1 - descuento).

Transcript
    show: 'Total: ', (total printShowingDecimalPlaces: 2);
    cr.
```

**Recorrido, línea a línea.**

- `| linea partes ... |` declara las variables temporales. No llevan tipo: cualquier variable puede
  referirse a cualquier objeto.
- `:=` es la asignación. El `=` a secas es **igualdad**, y es un mensaje como cualquier otro.
- `linea substrings` es un **mensaje unario**: se envía `substrings` al objeto cadena y devuelve una
  colección de trozos. Los mensajes unarios se escriben pegados detrás del receptor, sin paréntesis
  ni punto.
- `collect: [ :cada | cada asNumber ]` es un **mensaje de palabra clave**, y el corchete es un
  **bloque**: un trozo de código que es a su vez un objeto, con su parámetro declarado como `:cada`.
  `collect:` es el `map` de Smalltalk. El bloque es la construcción que, cuarenta años después,
  reapareció como *lambda* en Java 8, C# y Python.
- `precio * cantidad` **no usa operadores**: `*` es un **mensaje binario** enviado al objeto `precio`
  con `cantidad` como argumento. La clase `Number` implementa `*`. Se puede definir `*` en tus
  propias clases sin ninguna sintaxis especial de "sobrecarga de operadores", porque nunca hubo
  operadores que sobrecargar.
- **El orden de evaluación es la trampa clásica.** Smalltalk no tiene precedencia aritmética: los
  mensajes unarios van primero, luego **todos** los binarios de izquierda a derecha, y por último los
  de palabra clave. Es decir, `2 + 3 * 4` da **20**, no 14. Por eso `(1 - descuento)` lleva
  paréntesis: no por costumbre, sino porque sin ellos el resultado sería otro.
- `printShowingDecimalPlaces: 2` es un mensaje al número, no una función de formateo externa. La
  responsabilidad de saber presentarse es del propio objeto.
- El `;` es la **cascada**: envía el siguiente mensaje al *mismo* receptor (`Transcript`). Es la forma
  idiomática de encadenar varias operaciones sobre un objeto sin repetir su nombre.
- El `.` separa sentencias, como el punto y coma de otros lenguajes.

**Y ahora lo que de verdad hay que ver.** En Smalltalk esto también es cierto:

```smalltalk
(total > 0)
    ifTrue:  [ Transcript show: 'hay venta' ]
    ifFalse: [ Transcript show: 'venta vacía' ]
```

Eso **no es una estructura de control**. `ifTrue:ifFalse:` es un **método implementado en la clase
`Boolean`**: `True` lo implementa evaluando el primer bloque, `False` evaluando el segundo. El
condicional es polimorfismo. Lo mismo ocurre con `1 to: 10 do: [...]` (un método de `Number`) y
`[...] whileTrue: [...]` (un método de `BlockClosure`). Puedes abrir el navegador de clases y **leer
el código fuente del `if`**. Ese es el momento en que se entiende de verdad qué significa "todo es
un objeto".

## 🔍 Qué reconocer si vienes de otro lenguaje

| Si conoces… | En Smalltalk es… |
|---|---|
| `obj.metodo()` | `obj metodo` — sin punto, sin paréntesis |
| `obj.metodo(a, b)` | `obj conA: a conB: b` — el nombre del mensaje se **intercala** |
| `lista.map(f)` | `lista collect: [ :x \| f value: x ]` |
| `lista.filter(f)` | `lista select: [ :x \| ... ]` |
| `lista.reduce(f)` | `lista inject: 0 into: [ :acc :x \| acc + x ]` |
| `if / else` | `ifTrue: [...] ifFalse: [...]` — mensajes a un booleano |
| `while (c) { }` | `[ c ] whileTrue: [ ... ]` |
| Lambda / closure | Bloque `[ :x \| ... ]` |
| `this` / `self` | `self`; y `super` para el método de la superclase |
| `null` | `nil` — que también es un objeto, instancia de `UndefinedObject` |

## ⚠️ Errores comunes al leerlo

- **Aplicar precedencia aritmética.** `2 + 3 * 4` es `20`. Es el error número uno y no da ningún aviso.
- **Buscar el fichero fuente.** El código vive en la **imagen**, organizado por clases y categorías,
  y se explora con el navegador. Los ficheros `.st` son un formato de intercambio, no la fuente de
  verdad. Herramientas como **Iceberg** y el formato **Tonel** son las que reconcilian eso con Git.
- **Confundir `=` con `==`.** `=` es igualdad de valor (redefinible); `==` es identidad del objeto.
- **Olvidar el `^` del retorno.** Un método sin `^` devuelve `self`, no el valor de la última
  expresión. Es la diferencia con casi todos los lenguajes funcionales y con Ruby.
- **Creer que la clase es lo importante.** Lo importante es el mensaje. Si un objeto responde al
  mensaje, sirve: *duck typing* en su forma original.
- **Tratar el depurador como último recurso.** En Smalltalk, programar *dentro* del depurador —dejar
  que falle, implementar el método que faltaba y continuar— es el flujo normal, no una emergencia.

## 📚 Fuentes y bibliografía

- [Pharo](https://pharo.org/) — la implementación libre más activa, con MOOCs gratuitos.
- [Squeak](https://squeak.org/) — descendiente directa del Smalltalk-80 de PARC.
- [Cincom Smalltalk](https://www.cincomsmalltalk.com/) — VisualWorks y ObjectStudio, en desarrollo
  comercial continuo.
- **Adele Goldberg, David Robson**, *Smalltalk-80: The Language and its Implementation* — el "Libro
  Azul", el documento fundacional; disponible libremente en línea.
- **Stéphane Ducasse et al.**, *Pharo by Example* — libro gratuito y actual, la mejor entrada práctica
  ([books.pharo.org](https://books.pharo.org/)).
- **Sherman Alpert, Kyle Brown, Bobby Woolf**, *The Design Patterns Smalltalk Companion* — los
  patrones de diseño en el lenguaje del que salieron.
- **Alan Kay**, *The Early History of Smalltalk*, ACM HOPL-II, 1993 — el relato de primera mano de
  por qué el lenguaje es como es.

---

⏮️ [Volver al Atlas](README.md) · 🧟 [Los lenguajes que siguen vivos](vivos.md) ·
🔗 Relacionadas: [Common Lisp](common-lisp.md) · [M / MUMPS](mumps.md) · [Delphi](delphi.md)
