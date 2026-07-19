# Clase 020 — Familia .NET: C#, F#, VB.NET

> Parte **1 — Atlas y genealogía de los lenguajes** · ⏱️ Duración estimada: **75 min** · Nivel: **Fundamentos**
> ✅ **Clase construida.**

---

## 🎯 Objetivo

Conocer la plataforma **.NET** de Microsoft y sus tres lenguajes principales: **C#** (el representante del núcleo, multiparadigma), **F#** (funcional, de la familia ML) y **VB.NET** (heredero accesible de Visual Basic). La idea genealógica es la misma que en la clase anterior sobre la JVM, pero desde el otro gran competidor: todos compilan a un **lenguaje intermedio común (IL)** que se ejecuta sobre el **CLR**, la máquina virtual de Microsoft. Es la prueba de que "plataforma de ejecución compartida por varios lenguajes" fue una idea tan buena que se implementó dos veces, en paralelo, a ambos lados de la industria.

Esto importa porque .NET nació explícitamente como respuesta a Java a comienzos de los 2000 y comparte con él su arquitectura fundamental, lo que hace del par JVM/CLR un caso de estudio perfecto sobre convergencia de diseño. Además, la historia de .NET ilustra algo que ningún libro de hace veinte años predijo: un ecosistema propietario y atado a Windows que, a partir de 2016, se abrió, se hizo multiplataforma y open source, y hoy corre en Linux y macOS con normalidad.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Explicar el rol del CLR y del IL (análogos a la JVM y su bytecode).
2. Distinguir C# (multiparadigma), F# (funcional, de raíz ML) y VB.NET (accesible).
3. Entender qué significa que .NET hoy sea multiplataforma y de código abierto.
4. Comparar la pareja JVM/Java con la pareja CLR/C# y ver la convergencia de diseño.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | El CLR y el IL | Runtime y lenguaje intermedio comunes a los tres |
| 2 | C#: el buque insignia | Multiparadigma, moderno, gran ecosistema |
| 3 | F#: el funcional | ML sobre .NET: inmutabilidad y tipos algebraicos |
| 4 | VB.NET y la interoperabilidad | Un mismo IL permite mezclarlos en una solución |
| 5 | .NET multiplataforma | De solo-Windows a Linux/macOS, open source |

## 📖 Definiciones y características

El **CLR** (Common Language Runtime) es a .NET lo que la JVM es a Java: una máquina virtual que ejecuta un formato intermedio, gestiona la memoria con un recolector de basura y compila en caliente (JIT) el código más usado a instrucciones nativas. Ese formato intermedio se llama **IL** (Intermediate Language, también CIL o MSIL). La pieza clave del diseño de Microsoft fue el **CTS** (Common Type System): un sistema de tipos común que todos los lenguajes .NET comparten, de modo que un `string` de C# y un `string` de F# son exactamente el mismo tipo en el IL. Gracias a eso, la interoperabilidad entre lenguajes .NET no es solo posible sino trivial: una clase escrita en un lenguaje se usa desde otro sin adaptadores. Sebesta señala esta arquitectura como la respuesta directa de Microsoft al modelo de la JVM, con la ambición añadida de soportar muchos lenguajes desde el diseño, no como añadido posterior.

**C#** (Anders Hejlsberg, Microsoft, 2000) es el buque insignia. Hejlsberg —que antes había creado Turbo Pascal y Delphi, y después crearía TypeScript— diseñó un lenguaje deliberadamente parecido a Java en lo básico, pero que fue incorporando ideas propias a gran velocidad: propiedades, delegados, `LINQ` (consultas integradas en el lenguaje, inspiradas en lo funcional), `async/await` (que popularizó ese modelo antes que casi nadie), structs por valor y tipos nullable. Es multiparadigma —imperativo, OO y cada vez más funcional— y domina el desarrollo empresarial Windows, el motor de juegos Unity y buena parte del backend web con ASP.NET. **F#** (Don Syme, Microsoft Research, 2005) es el miembro funcional: un descendiente directo de OCaml —y por tanto de la familia ML de la clase 022— adaptado a .NET, con inmutabilidad por defecto, inferencia de tipos y tipos algebraicos. **VB.NET** reencarnó el clásico Visual Basic sobre el CLR con una sintaxis verbosa y en lenguaje casi natural, pensada para accesibilidad; hoy está en mantenimiento, sin evolución activa.

La transformación más notable de esta familia es histórica. Durante más de una década, .NET fue sinónimo de "solo Windows, cerrado y propietario". A partir de 2014-2016, Microsoft giró: liberó .NET como open source, creó **.NET Core** (hoy simplemente ".NET") multiplataforma, y hoy el mismo C# corre igual en Linux, macOS y Windows. Es un recordatorio de que el ecosistema y la gobernanza de un lenguaje —temas de la clase 016— pueden cambiar tanto que invalidan lo que "todo el mundo sabía" hace pocos años.

- **CLR** — Common Language Runtime: la máquina virtual de .NET. Clave: ejecuta el IL y gestiona memoria con GC; análogo a la JVM.
- **C#** — 2000 (Anders Hejlsberg, Microsoft), multiparadigma sobre el CLR. Clave: núcleo del curso; empresa, juegos (Unity) y web.
- **F#** — 2005 (Don Syme), funcional tipado derivado de OCaml, sobre .NET. Clave: pureza y tipos algebraicos en la plataforma Microsoft.
- **IL / CTS** — código y sistema de tipos intermedios comunes. Clave: permiten mezclar lenguajes .NET en una misma solución.

## 🧩 Situación

Un estudio de videojuegos escribe la lógica de su juego en C# porque es el lenguaje de scripting de Unity. Cuando necesita un servicio en la nube para guardar partidas, lo construye en C# con ASP.NET. Y cuando quiere una herramienta interna de escritorio para su equipo de arte, vuelve a C#. Una sola plataforma, un solo lenguaje, tres destinos completamente distintos —cliente de juego, backend web y app de escritorio—, todos compartiendo tipos y bibliotecas. Esa uniformidad, respaldada por el CLR, es exactamente lo que Microsoft prometió con .NET.

## 🔎 Ejemplo

Los tres lenguajes .NET expresando la misma suma, sobre el mismo runtime:

```text
C#:      int r = a + b;               // multiparadigma, tipo explícito
F#:      let r = a + b                // funcional, inmutable por defecto
VB.NET:  Dim r As Integer = a + b     ' verboso, cercano al lenguaje natural
```

El **delta** revela el paradigma de cada uno: C# declara el tipo y usa llaves; F# usa `let` con inferencia e inmutabilidad, herencia clarísima de ML; VB.NET escribe casi una frase en inglés (`Dim … As Integer`). Tras compilar, los tres producen IL que comparte el mismo `System.Int32`, por lo que una función escrita en F# puede llamarse desde C# sin ninguna conversión.

## ✍️ Práctica

F# es a .NET lo que Kotlin y Clojure son a la JVM: otro paradigma sobre el mismo runtime. Enumera dos lenguajes del núcleo comparables a C# por su modelo (pista: Java por su OO nominal, y por dónde se diferencian: propiedades, `LINQ`, structs por valor). Luego busca qué introdujo primero C#, `async/await`, y en qué otros lenguajes del núcleo aparece hoy esa misma palabra clave.

## ⚠️ Errores comunes

- **Creer que ".NET es solo Windows"** → causa: quedarse con la imagen anterior a 2016 → solución: recordar que .NET moderno es open source y corre en Linux y macOS.
- **Confundir C# con Java por parecerse** → causa: asumir que son intercambiables → solución: notar diferencias reales: propiedades, `LINQ`, structs por valor, `async/await` temprano.
- **Ignorar que F# es de la familia ML** → causa: tratarlo como "C# raro" → solución: reconocer su herencia de OCaml (inmutabilidad, ADT, inferencia) que se estudia en la clase 022.

## ❓ Preguntas frecuentes

- **¿C# o Java?** Son muy parecidos en su modelo OO; la elección suele depender del ecosistema (Microsoft frente a JVM), del equipo y de la plataforma de destino, más que del lenguaje en sí.
- **¿VB.NET sigue vivo?** Existe y funciona, pero está en mantenimiento: Microsoft ya no lo evoluciona con características nuevas y recomienda C# para proyectos nuevos.
- **¿Por qué Microsoft abrió .NET?** Para competir en la nube y en Linux, donde un runtime cerrado y atado a Windows lo dejaba fuera de gran parte del mercado de servidores.

## 🔗 Referencias

- J. Skeet — *C# in Depth* (4ª ed., Manning).
- R. W. Sebesta — *Concepts of Programming Languages* (12ª ed., Pearson), cap. 1-2 (el CLR como respuesta a la JVM).
- M. L. Scott — *Programming Language Pragmatics* (4ª ed., Morgan Kaufmann).
- P. Van Roy y S. Haridi — *Concepts, Techniques, and Models of Computer Programming* (MIT Press).

---

> [⏮️ Clase 019](../../parte-1-atlas-y-genealogia-de-los-lenguajes/019-familia-jvm-java-kotlin-scala-groovy-clojure/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 021 ⏭️](../../parte-1-atlas-y-genealogia-de-los-lenguajes/021-familia-javascript-y-web-js-typescript-dart/README.md)
