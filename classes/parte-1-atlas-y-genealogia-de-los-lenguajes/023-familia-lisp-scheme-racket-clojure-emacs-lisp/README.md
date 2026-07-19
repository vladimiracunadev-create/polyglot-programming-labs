# Clase 023 — Familia Lisp: Scheme, Racket, Clojure, Emacs Lisp

> Parte **1 — Atlas y genealogía de los lenguajes** · ⏱️ Duración estimada: **75 min** · Nivel: **Fundamentos**
> ✅ **Clase construida.**

---

## 🎯 Objetivo

Conocer la familia más antigua todavía viva: Lisp (1958). Su rasgo único es la homoiconicidad: el código se escribe con la misma estructura que los datos (listas entre paréntesis), lo que permite macros que reescriben el propio lenguaje. Ninguno está en el núcleo, pero sus ideas (funciones de primera clase, GC, REPL) hoy están en todos.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Explicar la homoiconicidad y por qué habilita macros potentes.
2. Leer una expresión Lisp (notación prefija entre paréntesis).
3. Reconocer ideas nacidas en Lisp que hoy son universales.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Homoiconicidad | Código y datos comparten forma (listas) |
| 2 | Notación prefija | (operador operando operando) |
| 3 | Macros | Programas que escriben programas |
| 4 | Herencia universal | GC, REPL, funciones de primera clase nacieron aquí |

## 📖 Definiciones y características

- **Lisp** — 1958 (John McCarthy), segundo lenguaje de alto nivel más antiguo. Clave: introdujo ideas hoy universales (GC, funciones de primera clase).
- **Homoiconicidad** — el código tiene la misma estructura que los datos que manipula. Clave: permite macros que transforman el lenguaje.
- **Scheme** — 1975, dialecto minimalista y elegante de Lisp. Clave: usado en enseñanza (SICP).
- **Clojure** — 2007, Lisp moderno sobre la JVM. Clave: acerca la familia Lisp al mundo mainstream con datos inmutables.

## 🧩 Situación

Un programador ve `(+ 1 2 3)` y lo descarta por 'raro'. Pero esa uniformidad —todo es una lista— es justo lo que permite a Lisp extenderse con macros que otros lenguajes no pueden igualar.

## 🔎 Ejemplo

La notación prefija: el operador va primero, todo entre paréntesis.

```text
Infija (C):    (1 + 2) * 3
Lisp:          (* (+ 1 2) 3)
Definir función (Scheme):
               (define (doble x) (* x 2))
```

## ✍️ Práctica

Traduce `(* (+ 2 3) (- 10 4))` a notación infija y calcula el resultado. (Respuesta: (2+3)*(10-4) = 30.)

## ⚠️ Errores comunes

- **Rechazar Lisp por los paréntesis** → causa: juzgar la forma, no las ideas → solución: ver que su uniformidad es su superpoder (macros)
- **Creer que Lisp es cosa del pasado** → causa: ignorar Clojure y Racket → solución: reconocer que sigue vivo e influyente

## ❓ Preguntas frecuentes

- **¿Para qué sirve hoy?** Clojure en backend/datos, Racket y Scheme en enseñanza e investigación, Emacs Lisp en el editor Emacs.
- **¿Qué idea de Lisp uso sin saberlo?** Las funciones de primera clase (pasar funciones como valores) y el recolector de basura.

## 🔗 Referencias

- R. W. Sebesta — *Concepts of Programming Languages* (12ª ed., Pearson).
- M. L. Scott — *Programming Language Pragmatics* (4ª ed., Morgan Kaufmann).
- B. A. Tate — *Seven Languages in Seven Weeks* (Pragmatic Bookshelf).
- P. Van Roy y S. Haridi — *Concepts, Techniques, and Models of Computer Programming* (MIT Press).

---

> [⏮️ Clase 022](../../parte-1-atlas-y-genealogia-de-los-lenguajes/022-familia-funcional-tipada-ml-haskell-ocaml-f-sharp-y-la-influencia-en-rust/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 024 ⏭️](../../parte-1-atlas-y-genealogia-de-los-lenguajes/024-familia-logica-y-declarativa-sql-prolog-datalog/README.md)
