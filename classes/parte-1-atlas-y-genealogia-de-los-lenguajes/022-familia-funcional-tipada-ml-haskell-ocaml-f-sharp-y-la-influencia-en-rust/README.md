# Clase 022 — Familia funcional tipada (ML): Haskell, OCaml, F# y la influencia en Rust

> Parte **1 — Atlas y genealogía de los lenguajes** · ⏱️ Duración estimada: **75 min** · Nivel: **Fundamentos**
> ✅ **Clase construida.**

---

## 🎯 Objetivo

Conocer la familia ML: lenguajes funcionales con sistemas de tipos potentes e inferencia. Aunque ninguno está en el núcleo, su influencia sí: Rust tomó de aquí los tipos algebraicos, el `match` y `Option`/`Result`. Entender ML explica por qué Rust se siente distinto a C.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Explicar los rasgos de la familia ML (funciones puras, inmutabilidad, inferencia, ADT).
2. Reconocer qué tomó Rust de ML frente a lo que tomó de C.
3. Leer una expresión funcional simple (match sobre un tipo suma).

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Raíces: ML (1973) | Inferencia de tipos y funciones como valores |
| 2 | Haskell: pureza y pereza | Sin efectos secundarios por defecto; evaluación perezosa |
| 3 | OCaml y F# | ML práctico; F# lleva ML a .NET |
| 4 | La huella en Rust | ADT, match exhaustivo, Option/Result |

## 📖 Definiciones y características

- **ML** — familia de 1973 (Robin Milner) con inferencia de tipos Hindley-Milner. Clave: raíz de OCaml, Haskell y F#.
- **Haskell** — 1990, funcional puro y perezoso. Clave: los efectos se modelan con tipos (mónadas); el más 'purista' de la familia.
- **Tipo algebraico (ADT)** — tipo compuesto por alternativas (suma) o productos. Clave: Rust los tomó de aquí como `enum`.
- **Inferencia de tipos** — el compilador deduce los tipos sin anotarlos. Clave: rasgo de ML heredado por Rust, Kotlin, Go y otros.

## 🧩 Situación

Un programador de C prueba Rust y se sorprende con `match` exhaustivo y `Option<T>` en vez de punteros nulos. Eso no viene de C: viene de ML. Reconocer la herencia hace que Rust deje de parecer arbitrario.

## 🔎 Ejemplo

El `match` sobre un tipo suma, de ML a Rust:

```text
Haskell:  case forma of
            Circulo r -> pi * r * r
            Cuadrado l -> l * l
Rust:     match forma {
            Forma::Circulo(r) => PI * r * r,
            Forma::Cuadrado(l) => l * l,
          }
```

## ✍️ Práctica

Busca en la clase 041 (o en material de Rust) un `Option`/`Result`. Explica por qué esa idea es más segura que un puntero nulo, y de qué familia proviene.

## ⚠️ Errores comunes

- **Ver Rust como 'C moderno' solamente** → causa: ignorar su mitad ML → solución: reconocer que su seguridad de tipos viene de la familia funcional
- **Creer que funcional = académico e inútil** → causa: prejuicio → solución: notar que sus ideas ya están en lenguajes mainstream (Rust, Kotlin, Swift)

## ❓ Preguntas frecuentes

- **¿Necesito aprender Haskell?** No para el núcleo, pero entender sus ideas mejora tu Rust, tu Kotlin y tu forma de pensar.
- **¿Qué es la 'pereza' de Haskell?** Evalúa una expresión solo cuando se necesita su valor; permite listas infinitas, entre otras cosas.

## 🔗 Referencias

- Documentación de referencia de cada lenguaje del núcleo.

---

> [⏮️ Clase 021](../../parte-1-atlas-y-genealogia-de-los-lenguajes/021-familia-javascript-y-web-js-typescript-dart/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 023 ⏭️](../../parte-1-atlas-y-genealogia-de-los-lenguajes/023-familia-lisp-scheme-racket-clojure-emacs-lisp/README.md)
