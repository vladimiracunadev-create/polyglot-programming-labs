# Clase 019 — Familia JVM: Java, Kotlin, Scala, Groovy, Clojure

> Parte **1 — Atlas y genealogía de los lenguajes** · ⏱️ Duración estimada: **75 min** · Nivel: **Fundamentos**
> ✅ **Clase construida.**

---

## 🎯 Objetivo

Conocer los lenguajes que corren sobre la Máquina Virtual de Java (JVM). Java es el representante del núcleo; Kotlin, Scala, Groovy y Clojure comparten la misma plataforma (bytecode, GC, librerías) pero ofrecen paradigmas distintos. Un mismo runtime, varias formas de programar.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Explicar qué comparten los lenguajes JVM (bytecode, GC, interoperabilidad).
2. Distinguir el paradigma de cada uno (OO nominal, moderno, funcional-OO, Lisp).
3. Entender por qué se puede mezclar Java y Kotlin en un mismo proyecto.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | La JVM como plataforma | Compilan a bytecode; comparten GC y librerías |
| 2 | Java: el estándar | OO nominal, verboso pero robusto |
| 3 | Kotlin y Scala | Java moderno (null-safety, corrutinas) y funcional-OO |
| 4 | Clojure | Un Lisp sobre la JVM: datos inmutables y macros |

## 📖 Definiciones y características

- **JVM** — máquina virtual que ejecuta bytecode Java. Clave: da portabilidad ('escribe una vez, corre en todas partes') y GC.
- **Java** — 1995 (Gosling, Sun), OO nominal sobre la JVM. Clave: núcleo del curso; pilar del backend empresarial.
- **Kotlin** — 2011 (JetBrains), Java moderno con null-safety y corrutinas. Clave: oficial para Android; interopera 100% con Java.
- **Clojure** — 2007 (Rich Hickey), dialecto de Lisp sobre la JVM. Clave: inmutabilidad y homoiconicidad en una plataforma mainstream.

## 🧩 Situación

Un proyecto Android en Java quiere adoptar corrutinas y null-safety sin reescribir todo. Migra archivo a archivo a Kotlin, que convive con Java en el mismo proyecto porque ambos compilan al mismo bytecode.

## 🔎 Ejemplo

Cuatro maneras de sumar sobre la MISMA plataforma:

```text
Java:    int r = a + b;
Kotlin:  val r = a + b            // inferencia, inmutable
Scala:   val r = a + b            // funcional-OO
Clojure: (def r (+ a b))          // Lisp: paréntesis y prefijo
```

## ✍️ Práctica

Kotlin usa `val` (inmutable) y `var` (mutable). ¿A qué lenguaje del núcleo se parece esa distinción? (Pista: Rust.)

## ⚠️ Errores comunes

- **Creer que 'lenguaje JVM' = 'Java'** → causa: ignorar la diversidad de paradigmas sobre la misma VM → solución: recordar que Clojure (Lisp) y Java conviven en la JVM
- **Asumir arranque instantáneo** → causa: la JVM tiene tiempo de calentamiento → solución: considerarlo en herramientas de línea de comandos de vida corta

## ❓ Preguntas frecuentes

- **¿Puedo llamar a Java desde Kotlin?** Sí, y viceversa: comparten bytecode y librerías; la interoperabilidad es total.
- **¿Clojure es raro?** Su sintaxis Lisp asusta al principio, pero su modelo de datos inmutables es muy elegante.

## 🔗 Referencias

- Documentación de referencia de cada lenguaje del núcleo.

---

> [⏮️ Clase 018](../../parte-1-atlas-y-genealogia-de-los-lenguajes/018-familia-scripting-dinamico-python-ruby-perl-php-lua/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 020 ⏭️](../../parte-1-atlas-y-genealogia-de-los-lenguajes/020-familia-net-c-sharp-f-sharp-vb-net/README.md)
