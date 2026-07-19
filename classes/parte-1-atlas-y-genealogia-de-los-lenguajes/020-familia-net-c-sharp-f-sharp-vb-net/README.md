# Clase 020 — Familia .NET: C#, F#, VB.NET

> Parte **1 — Atlas y genealogía de los lenguajes** · ⏱️ Duración estimada: **75 min** · Nivel: **Fundamentos**
> ✅ **Clase construida.**

---

## 🎯 Objetivo

Conocer la plataforma .NET de Microsoft y sus tres lenguajes: C# (el representante del núcleo, multiparadigma), F# (funcional) y VB.NET (heredero de Visual Basic). Todos compilan a un lenguaje intermedio común (IL) que corre sobre el CLR, el equivalente de la JVM en el mundo Microsoft.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Explicar el rol del CLR y el IL (análogo a la JVM y su bytecode).
2. Distinguir C# (multiparadigma), F# (funcional) y VB.NET (accesible).
3. Entender qué significa que .NET hoy sea multiplataforma y de código abierto.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | El CLR y el IL | Runtime y lenguaje intermedio comunes a los tres |
| 2 | C#: el buque insignia | Multiparadigma, moderno, gran ecosistema |
| 3 | F#: el funcional | ML sobre .NET: inmutabilidad y tipos algebraicos |
| 4 | .NET multiplataforma | De Windows a Linux/macOS, open source |

## 📖 Definiciones y características

- **CLR** — Common Language Runtime: la máquina virtual de .NET. Clave: ejecuta el IL, gestiona memoria (GC); análogo a la JVM.
- **C#** — 2000 (Anders Hejlsberg, Microsoft), multiparadigma sobre el CLR. Clave: núcleo del curso; empresa, juegos (Unity) y web.
- **F#** — 2005 (Don Syme), funcional tipado derivado de OCaml, sobre .NET. Clave: pureza y tipos algebraicos en la plataforma Microsoft.
- **IL (bytecode de .NET)** — código intermedio al que compilan todos los lenguajes .NET. Clave: permite mezclarlos en una solución.

## 🧩 Situación

Un estudio de videojuegos usa Unity, cuyo scripting es C#. El mismo lenguaje sirve luego para el backend web con ASP.NET y para una herramienta de escritorio: una plataforma, muchos destinos.

## 🔎 Ejemplo

Los tres lenguajes .NET, mismo runtime:

```text
C#:      int r = a + b;
F#:      let r = a + b            // funcional, inmutable por defecto
VB.NET:  Dim r As Integer = a + b  ' sintaxis verbosa, accesible
```

## ✍️ Práctica

F# es a .NET lo que Kotlin/Clojure son a la JVM: otro paradigma sobre el mismo runtime. Enumera dos lenguajes del núcleo comparables a C# por su modelo (Pista: Java).

## ⚠️ Errores comunes

- **Creer que .NET es solo Windows** → causa: quedarse con la imagen antigua → solución: recordar que .NET moderno corre en Linux y macOS y es open source
- **Confundir C# con Java por parecerse** → causa: asumir que son intercambiables → solución: notar diferencias reales: propiedades, LINQ, structs por valor

## ❓ Preguntas frecuentes

- **¿C# o Java?** Muy parecidos en modelo; la elección suele depender del ecosistema (Microsoft vs. JVM) y del equipo.
- **¿VB.NET sigue vivo?** En mantenimiento: existe y funciona, pero Microsoft ya no lo evoluciona activamente.

## 🔗 Referencias

- R. W. Sebesta — *Concepts of Programming Languages* (12ª ed., Pearson).
- M. L. Scott — *Programming Language Pragmatics* (4ª ed., Morgan Kaufmann).
- B. A. Tate — *Seven Languages in Seven Weeks* (Pragmatic Bookshelf).
- P. Van Roy y S. Haridi — *Concepts, Techniques, and Models of Computer Programming* (MIT Press).

---

> [⏮️ Clase 019](../../parte-1-atlas-y-genealogia-de-los-lenguajes/019-familia-jvm-java-kotlin-scala-groovy-clojure/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 021 ⏭️](../../parte-1-atlas-y-genealogia-de-los-lenguajes/021-familia-javascript-y-web-js-typescript-dart/README.md)
