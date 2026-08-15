# 👑 Nim — 2008

> [⬅️ Atlas](README.md) · [🗂️ Todas las fichas](lenguajes.md) · [📚 Índice de clases](../classes/README.md)

Nim demuestra que **"parecerse a Python" y "compilar como C" no son incompatibles**. Tiene sangría
significativa, inferencia de tipos y una sintaxis ligera — y produce un binario nativo sin tiempo de
ejecución pesado, con macros que operan sobre el árbol sintáctico.

> **🎯 Por qué está en este programa**
>
> Nim es un **primo de la familia C / llaves** ([Atlas](README.md#c-llaves)) en el eje de sistemas,
> junto a [Zig](zig.md) y [D](d.md).
>
> Aporta al programa una comparación muy útil: **es la prueba de que la sintaxis y el modelo de
> ejecución son decisiones independientes**. Quien crea que un lenguaje "de guion" es lento por su
> aspecto, aquí ve lo contrario. Y aporta **macros higiénicas sobre el árbol sintáctico** en un
> lenguaje de tipado estático (clase 122), que es una combinación poco frecuente.

| | |
|---|---|
| **Año** | 2008 (como Nimrod); **1.0** en 2019; **2.0** en 2023 |
| **Autoría** | **Andreas Rumpf**, con una comunidad pequeña y activa |
| **Familia** | Sistemas; sintaxis de [Python](python.md), semántica de [Pascal](pascal.md)/Modula y C |
| **Paradigma** | Multiparadigma: imperativo, orientado a objetos, funcional y metaprogramación |
| **Tipado** | **Estático y fuerte**, con inferencia; genéricos y conceptos |
| **Memoria** | **ARC/ORC**: conteo de referencias con detección de ciclos, en compilación |
| **Ejecución** | **Compila a C, C++ o JavaScript**, y de ahí a nativo |
| **Estado** | 🟡 **Estable y minoritario**: excelente y con poca adopción industrial |

---

## 📜 Historia

**Andreas Rumpf** empezó Nimrod en **2008** con un objetivo poco común: **un lenguaje tan expresivo
como Python, tan rápido como C y tan seguro como Ada**. La estrategia para conseguirlo fue pragmática
y muy eficaz: **no generar código máquina, sino generar C**.

Esa decisión —la misma que tomó [GnuCOBOL](cobol.md) y que en su día tomó C++ con `cfront`— le dio
gratis lo que a un lenguaje nuevo le cuesta años: **portabilidad a cualquier plataforma con un
compilador de C**, incluidos microcontroladores, y **acceso directo a todas las bibliotecas de C**
(clase 156).

El cambio de nombre a **Nim** llegó en 2014 —Nimrod tiene connotaciones desafortunadas en inglés—, la
**1.0** en 2019, y la **2.0** en 2023 con **ORC por defecto**: gestión de memoria determinista, sin
recolector con pausas.

Y ahí está su posición actual: **un lenguaje técnicamente muy logrado con una comunidad pequeña** —
que es, como la clase 164 explica, un factor que pesa más que casi cualquier característica.

## 🏭 Dónde vive hoy

- **Herramientas de línea de comandos y utilidades** donde se quiere un binario pequeño y rápido con
  poco código (clase 167).
- **Sistemas embebidos**: al generar C, llega a plataformas donde no hay LLVM.
- **Extensiones nativas para Python**, con `nimpy` (clase 158).
- **Desarrollo web**: Karax compila Nim a JavaScript para el navegador (clase 169).
- **Bioinformática y ciencia**: `hts-nim` y varias herramientas de genómica.

## 🧠 Lo que enseña: la sintaxis no determina el rendimiento

```nim
import std/[strutils, sequtils]

let numeros = "1 2 3 4".splitWhitespace().map(parseInt)
echo numeros.sum()
```

**Eso podría ser Python**, y **compila a un binario nativo sin intérprete**. Es la demostración más
directa de una idea que este curso repite (clases 123 y 164): **el aspecto de un lenguaje y su modelo
de ejecución son decisiones separadas**.

Y Nim tiene tres características que merecen conocerse:

**Uno, la identificación de nombres es *insensible al estilo***:

```nim
proc miFuncion() = discard
mifuncion()      # ✓ lo mismo
mi_funcion()      # ✓ también: se ignoran los guiones bajos y las mayúsculas (menos la primera)
```

Es una decisión discutida —y muy práctica— para acabar con las guerras de estilo de nombres
(clase 146): **cada quien escribe como quiera y el compilador los une**.

**Dos, la notación uniforme de llamada:**

```nim
len(cadena)      # y
cadena.len        # son EXACTAMENTE lo mismo
```

**No hace falta que la función sea un método** para escribirla con punto. Eso permite encadenar sin
que la biblioteca lo haya previsto, y es lo que [D](d.md) también tiene.

**Y tres, las macros**, que son lo más potente del lenguaje:

```nim
macro miDsl(cuerpo: untyped): untyped =
  # recibe el ÁRBOL SINTÁCTICO y devuelve otro árbol
```

**Son macros sobre el AST, higiénicas y con tipos** — la potencia de [Lisp](common-lisp.md) (clase
122) en un lenguaje estático. Con ellas se construyen los generadores de HTML, los ORM y los DSL del
ecosistema, sin coste en ejecución.

## 🔄 Lo que se ha modernizado

- **ORC por defecto (2.0)**: conteo de referencias insertado por el compilador **con detección de
  ciclos**, sin recolector con pausas — determinista, apto para tiempo real (clase 131).
- **`nimble`** como gestor de paquetes con fichero de bloqueo (clase 143).
- **Comprobación de efectos**: se puede declarar que una función **no lanza excepciones** o **no
  reserva memoria**, y el compilador lo verifica — la idea de la clase 146 llevada al sistema de tipos.
- **Objetivo JavaScript** como destino de primera clase (clase 162).

## ⚙️ Cómo se ejecuta hoy

```bash
nim c -r main.nim < entrada.txt          # compilar y ejecutar
nim c -d:release --opt:speed main.nim     # binario optimizado
nim js main.nim                            # ← el mismo código, a JavaScript

nimble install && nimble test              # dependencias y pruebas
```

## 🧪 El programa de la clase 041 en Nim

```nim
import std/[strutils, sequtils, strformat]

let v = stdin.readLine().splitWhitespace().map(parseFloat)
let total = v[0] * v[1] * (1 - v[2])
echo &"Total: {total:.2f}"
```

**Lo que hay que ver.**

- **Tres líneas, y compila a un ejecutable nativo.** Compárese con la versión de [C](c.md) —que hace
  lo mismo en quince— y con la de [Python](python.md), que se le parece y necesita un intérprete.
- **`let` es inmutable**, como en [Rust](rust.md); para poder reasignar hay que escribir `var`
  (clase 102).
- **`&"..."` es una macro de interpolación** con formato comprobado **en compilación**: si el formato
  no encaja con el tipo, **no compila** (clase 142). Es la macro del punto anterior aplicada a algo
  cotidiano.
- **La sangría marca los bloques**, como en Python — pero el tipo de `v` está inferido y comprobado,
  y `v[0] * v[1]` es aritmética de coma flotante nativa, sin objetos ni despacho.

## 📚 Fuentes y bibliografía

- [nim-lang.org/documentation](https://nim-lang.org/documentation.html) — manual, referencia de la
  biblioteca y el tutorial oficial.
- [Nim by Example](https://nim-by-example.github.io/) — introducción práctica corta.
- [Nim in Action](https://www.manning.com/books/nim-in-action) — **Dominik Picheta**, Manning; el
  libro de referencia, escrito por uno de los principales colaboradores.
- [Foro y repositorio de Nim](https://forum.nim-lang.org/) — comunidad pequeña y muy accesible, con
  el propio autor respondiendo.

---

⏮️ [Volver al Atlas](README.md) · 🗂️ [Todas las fichas](lenguajes.md) ·
🔗 Relacionadas: [Python](python.md) · [C](c.md) · [D](d.md) · [Zig](zig.md) · [Pascal](pascal.md)
