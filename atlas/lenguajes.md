# 🗂️ Todas las fichas de lenguaje

> [⬅️ Atlas](README.md) · [🧟 Lenguajes que siguen vivos](vivos.md) ·
> [📚 Índice de clases](../classes/README.md)

**Este es el índice de las 60 fichas de lenguaje del repositorio: una por cada lenguaje que aparece en
el programa**, sea del núcleo que se implementa en las 136 clases, de los primos del Atlas que
aparecen en cada `primos.md`, o de los lenguajes vivos que aparecen en cada `vivos.md`.

Todas siguen la misma estructura: **por qué está en el programa**, tabla de identidad, **historia**,
dónde vive hoy, **lo que enseña y no enseña ningún otro**, lo que se ha modernizado, cómo se ejecuta
hoy con órdenes reales, **el programa de la clase 041 explicado línea a línea**, y bibliografía con
libros y fuentes concretas.

> **⚠️ Qué está verificado y qué no.** El **programa de la clase 041** de cada ficha es el mismo de la
> clase, y su estado de verificación es el que declara la clase 040: **las 10 implementaciones del
> núcleo y 3 primos (Ruby, Perl, Lua) se ejecutan en CI**; los **8 lenguajes vivos compilables**
> también. El resto son **material de lectura**: están escritos para ser correctos y **no llevan el
> sello de la máquina**. Cada ficha lo dice en su apartado.

---

## 🔟 Los diez lenguajes del núcleo

Se implementan y se verifican en CI en **las 136 clases de código**. Son los representantes de familia
del programa.

| Ficha | Año | Familia que representa | Lo que aporta al programa |
|---|---|---|---|
| [Python](python.md) | 1991 | Scripting dinámico | Legibilidad como criterio; el pegamento del sistema |
| [JavaScript](javascript.md) | 1995 | JavaScript / web | Prototipos, bucle de eventos, coerción débil |
| [TypeScript](typescript.md) | 2012 | JavaScript / web | Tipado gradual y **borrado** de tipos |
| [Java](java.md) | 1995 | JVM | Máquina virtual con JIT, recolector, interfaces |
| [C#](csharp.md) | 2000 | .NET | Genéricos **reificados**; origen de `async`/`await` |
| [Go](go.md) | 2009 | Sistemas | **CSP**: gorrutinas y canales; lenguaje pequeño |
| [Rust](rust.md) | 2010 | Sistemas | **Propiedad y préstamo**; concurrencia sin carreras |
| [C](c.md) | 1972 | C / llaves | La **ABI** común; memoria manual |
| [SQL](sql.md) | 1974 | Lógica y declarativa | Declarar el **qué**, no el cómo |
| [PHP](php.md) | 1995 | Scripting dinámico | Ejecución **sin estado** por petición |

## 🧟 Los dieciocho lenguajes que siguen vivos

Aparecen en el `vivos.md` de cada clase. **Ocho se ejecutan en CI**; el resto se declaran como
adaptados o de lectura. Su índice propio, con los tres niveles de rigor, está en
**[vivos.md](vivos.md)**.

| Ficha | Año | Dónde sobrevive | Lo que enseña |
|---|---|---|---|
| [COBOL](cobol.md) | 1959 | Banca, seguros, administración | Decimal exacto; el lote |
| [Fortran](fortran.md) | 1957 | Cálculo científico, HPC | Arreglos y vectorización |
| [Ada](ada.md) | 1980 | Aviónica, ferrocarril, defensa | Tipos con dominio; contratos; SPARK |
| [Pascal](pascal.md) | 1970 | Enseñanza; Free Pascal | Lenguaje pequeño y legible |
| [Delphi](delphi.md) | 1995 | Escritorio de empresa | Componentes, RTTI, `of object` |
| [Common Lisp](common-lisp.md) | 1984 | IA simbólica, herramientas | Código como dato; imagen viva |
| [AutoLISP](autolisp.md) | 1986 | AutoCAD | Lisp incrustado en un producto |
| [Tcl](tcl.md) | 1988 | Diseño de circuitos, Expect | El lenguaje **para ser incrustado** |
| [Perl](perl.md) | 1987 | Texto, integración, bioinformática | Expresiones regulares; CPAN; taint |
| [C++](cpp.md) | 1985 | Motores, navegadores, BD | RAII; plantillas; comportamiento indefinido |
| [RPG](rpg.md) | 1959 | IBM i: gestión | Firma de programa de servicio; ILE |
| [PL/I](pl-i.md) | 1964 | z/OS: seguros, banca | Ambición total y su precio |
| [M / MUMPS](mumps.md) | 1966 | Sanidad (VistA, Epic) | El dato persistente sin impedancia |
| [Smalltalk](smalltalk.md) | 1972 | Nicho; enorme influencia | Todo es objeto; MVC; refactorización |
| [JCL](jcl.md) | 1964 | z/OS | Orquestación de trabajos con dependencias |
| [Assembler](assembler.md) | 1949 | Firmware, núcleos, mainframe | Lo que hay debajo de todo |
| [VBA](vba.md) | 1993 | Excel, Access, Office | El lenguaje incrustado con más usuarios |
| [VB.NET](vbnet.md) | 2002 | Gestión de empresa | La ruptura de compatibilidad como lección |

---

## 🌳 Por familias

### 🧱 C / llaves

**Representante del núcleo:** [C](c.md). Memoria explícita, tipos declarados, sintaxis de llaves.

| Ficha | Año | Lo que aporta |
|---|---|---|
| [C](c.md) | 1972 | La ABI común de la interoperabilidad (clase 157) |
| [C++](cpp.md) | 1985 | RAII, plantillas, abstracción sin coste (clase 132) |
| [Objective-C](objective-c.md) | 1984 | Despacho dinámico de mensajes sobre C (clase 111) |
| [Zig](zig.md) | 2016 | Asignador explícito y `comptime` (clases 128 y 122) |
| [Nim](nim.md) | 2008 | Sintaxis de guion, binario nativo, macros sobre el AST |
| [D](d.md) | 2001 | CTFE, contratos y pruebas en el lenguaje (clase 139) |

### 🐍 Scripting dinámico

**Representantes del núcleo:** [Python](python.md) · [PHP](php.md).

| Ficha | Año | Lo que aporta |
|---|---|---|
| [Python](python.md) | 1991 | Legibilidad como decisión de diseño |
| [PHP](php.md) | 1995 | El modelo sin estado por petición (clase 168) |
| [Ruby](ruby.md) | 1995 | Todo es objeto; bloques; clases abiertas |
| [Perl](perl.md) | 1987 | Texto, CPAN, TAP y el modo *taint* (clase 153) |
| [Lua](lua.md) | 1993 | El lenguaje incrustado por excelencia (clase 163) |
| [Tcl](tcl.md) | 1988 | Todo es cadena; todo es canal; Safe-Tcl |
| [R](r.md) | 1993 | Pensar en vectores; evaluación no estándar |

### 🌐 JavaScript / web

**Representantes del núcleo:** [JavaScript](javascript.md) → [TypeScript](typescript.md).

| Ficha | Año | Lo que aporta |
|---|---|---|
| [JavaScript](javascript.md) | 1995 | Prototipos y bucle de eventos (clases 112 y 134) |
| [TypeScript](typescript.md) | 2012 | Tipado gradual estructural, con borrado |
| [Dart](dart.md) | 2011 | **JIT para desarrollar, AOT para publicar** (clase 174) |
| [Elm](elm.md) | 2012 | Sin excepciones en ejecución; la arquitectura Elm |
| [ActionScript](actionscript.md) | 1998 | **Extinto**: la dependencia de plataforma (clase 164) |

### ☕ JVM

**Representante del núcleo:** [Java](java.md). Todos compilan al mismo bytecode.

| Ficha | Año | Lo que aporta |
|---|---|---|
| [Java](java.md) | 1995 | JIT, recolector generacional, interfaces |
| [Kotlin](kotlin.md) | 2011 | Nulabilidad en el tipo; concurrencia estructurada |
| [Scala](scala.md) | 2004 | OO + funcional unificados; colecciones persistentes |
| [Groovy](groovy.md) | 2003 | El DSL de Gradle y Jenkins (clase 163) |
| [Clojure](clojure.md) | 2007 | Inmutabilidad total; identidad frente a valor |

### 🟦 .NET

**Representante del núcleo:** [C#](csharp.md). Un ABI común para varios lenguajes (clase 157).

| Ficha | Año | Lo que aporta |
|---|---|---|
| [C#](csharp.md) | 2000 | Genéricos reificados; LINQ; `async`/`await` |
| [F#](fsharp.md) | 2005 | Inferencia total; unidades de medida; proveedores de tipos |
| [VB.NET](vbnet.md) | 2002 | El lenguaje intercambiable; la migración forzada |

### λ Funcional tipada (ML)

**Sin representante en el núcleo** — su influencia llega por [Rust](rust.md), [Scala](scala.md) y
[F#](fsharp.md).

| Ficha | Año | Lo que aporta |
|---|---|---|
| [Haskell](haskell.md) | 1990 | Pereza por defecto; efectos en el tipo (clase 118) |
| [OCaml](ocaml.md) | 1996 | Módulos y functores; ML pragmático (clase 149) |
| [F#](fsharp.md) | 2005 | ML en un ecosistema empresarial |
| [Elm](elm.md) | 2012 | La garantía que sale de la renuncia |

### 🔬 Lisp

**Sin representante en el núcleo.**

| Ficha | Año | Lo que aporta |
|---|---|---|
| [Common Lisp](common-lisp.md) | 1984 | Macros, condiciones con reinicios, imagen viva |
| [Scheme](scheme.md) | 1975 | Continuaciones; recursión de cola; macros higiénicas |
| [Racket](racket.md) | 1995 | **Crear lenguajes** como biblioteca (clases 122 y 163) |
| [Clojure](clojure.md) | 2007 | Lisp inmutable sobre la JVM |
| [Emacs Lisp](emacs-lisp.md) | 1985 | Alcance dinámico, en vivo (clase 088) |
| [AutoLISP](autolisp.md) | 1986 | Treinta años de rutinas en despachos de ingeniería |

### 🔗 Lógica y declarativa

**Representante del núcleo:** [SQL](sql.md).

| Ficha | Año | Lo que aporta |
|---|---|---|
| [SQL](sql.md) | 1974 | El optimizador decide el cómo (clase 118) |
| [Prolog](prolog.md) | 1972 | Unificación, vuelta atrás, relaciones reversibles |
| [Datalog](datalog.md) | 1977 | **Termina siempre**: la garantía que sale de renunciar |

### 📨 Concurrente / actor

**Sin representante en el núcleo** — lo más cercano es el CSP de [Go](go.md).

| Ficha | Año | Lo que aporta |
|---|---|---|
| [Erlang](erlang.md) | 1986 | Actores, supervisión y **"déjalo fallar"** (clase 133) |
| [Elixir](elixir.md) | 2011 | El mismo modelo con otra puerta de entrada (clase 164) |

### 🔢 Array / científica

**Sin representante en el núcleo.**

| Ficha | Año | Lo que aporta |
|---|---|---|
| [Fortran](fortran.md) | 1957 | BLAS/LAPACK; el rendimiento es memoria (clase 152) |
| [APL](apl.md) | 1966 | La notación como herramienta de pensamiento |
| [J](j.md) | 1990 | Programación **tácita**: componer sin nombrar |
| [Julia](julia.md) | 2012 | Despacho múltiple con JIT especializante (clase 111) |
| [MATLAB](matlab.md) | 1984 | Generación de código desde el modelo (clase 155) |
| [R](r.md) | 1993 | Estadística con el vector como unidad |

### 📱 Móvil / moderno

| Ficha | Año | Lo que aporta |
|---|---|---|
| [Swift](swift.md) | 2014 | ARC sin recolector; actores en el tipo (clases 131 y 136) |
| [Dart](dart.md) | 2011 | Dos compiladores para un lenguaje |

### 🗄️ Históricos / shell

| Ficha | Año | Lo que aporta |
|---|---|---|
| [COBOL](cobol.md) | 1959 | Decimal exacto; el lote; el sistema que sobrevive |
| [BASIC](basic.md) | 1964 | Accesibilidad como diseño; el `GOTO` (clase 083) |
| [Bash](bash.md) | 1989 | Tuberías: la composición de procesos (clase 161) |
| [PowerShell](powershell.md) | 2006 | **Objetos** por la tubería en vez de texto (clase 159) |
| [JCL](jcl.md) | 1964 | Orquestación con reanudación y recursos (clase 171) |
| [Assembler](assembler.md) | 1949 | El suelo: registros, pila y ABI (clases 127 y 157) |

---

## 📐 Cómo leer estas fichas

**Todas responden a las mismas preguntas, y en el mismo orden:**

1. **🎯 Por qué está en este programa** — el criterio de inclusión, explícito. Nunca "porque es
   antiguo" ni "porque es popular": **qué concepto aporta que los demás esconden**.
2. **Tabla de identidad** — año, autoría, familia, paradigma, tipado, memoria, ejecución y estado.
3. **📜 Historia** — de dónde viene, qué problema resolvía y qué decisiones lo formaron.
4. **🏭 Dónde vive hoy** — sectores y productos concretos, verificables.
5. **🧠 Lo que enseña** — el apartado central: **el concepto propio, con su coste dicho en voz alta**.
6. **🔄 Lo que se ha modernizado** — porque casi ninguno se quedó donde estaba.
7. **⚙️ Cómo se ejecuta hoy** — órdenes reales, que funcionan.
8. **🧪 El programa de la clase 041** — el mismo problema en todos, explicado línea a línea **por
   comparación con las demás fichas**.
9. **📚 Fuentes y bibliografía** — documentación oficial y libros concretos, con autoría.

**Y todas comparten una regla**: cuando un lenguaje **no puede** cumplir el contrato de la clase 041
—[SQL](sql.md), [Datalog](datalog.md), [Elm](elm.md), [ActionScript](actionscript.md),
[JCL](jcl.md)— **se declara la adaptación** en lugar de inventar un programa que no existiría
(clase 040).

## 🧭 Y de vuelta al programa

- **[Atlas de familias](README.md)** — el árbol completo, con las cápsulas por familia.
- **[Lenguajes que siguen vivos](vivos.md)** — el índice de los 18, con los niveles de rigor.
- **[Índice de clases](../classes/README.md)** — las 176 clases del programa.
- **[Clase 164: elegir el lenguaje correcto](../classes/parte-10-interoperabilidad-y-fronteras-entre-lenguajes/164-elegir-el-lenguaje-correcto-para-cada-componente/README.md)**
  — donde estas 60 fichas se convierten en una decisión.
- **[Clase 176: transferencia a nuevos lenguajes](../classes/parte-11-proyecto-integrador-poliglota/176-cierre-retrospectiva-y-transferencia-a-nuevos-lenguajes/README.md)**
  — y donde se explica para qué sirvió mirarlos todos.

---

⏮️ [Volver al Atlas](README.md) · 🧟 [Los lenguajes que siguen vivos](vivos.md) ·
📚 [Índice de clases](../classes/README.md)
