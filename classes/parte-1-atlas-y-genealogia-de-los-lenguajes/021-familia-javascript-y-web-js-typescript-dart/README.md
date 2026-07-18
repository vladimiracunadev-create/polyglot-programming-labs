# Clase 021 — Familia JavaScript y web: JS, TypeScript, Dart

> Parte **1 — Atlas y genealogía de los lenguajes** · ⏱️ Duración estimada: **75 min** · Nivel: **Fundamentos**
> ✅ **Clase construida.**

---

## 🎯 Objetivo

Conocer los lenguajes de la web. JavaScript (1995) nació para animar páginas y hoy corre en todas partes; TypeScript le añade tipos estáticos; Dart (Google) es su primo para apps (Flutter). Comparten sintaxis de llaves y un modelo asíncrono basado en eventos.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Explicar por qué JavaScript es omnipresente (navegador, servidor, móvil).
2. Entender qué añade TypeScript sobre JavaScript y por qué.
3. Reconocer el modelo asíncrono/eventos común a la familia.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | JavaScript: el lenguaje de la web | Único en el navegador; también en servidor (Node) |
| 2 | TypeScript: tipos sobre JS | Comprobación estática que transpila a JS |
| 3 | Prototipos y asincronía | Herencia por prototipos; eventos y promesas |
| 4 | Dart y otros primos | Alternativas que compilan a/para la web y móvil |

## 📖 Definiciones y características

- **JavaScript** — 1995 (Brendan Eich, Netscape), dinámico y basado en prototipos. Clave: el único lenguaje nativo del navegador; núcleo del curso.
- **TypeScript** — 2012 (Microsoft), superset de JS con tipos estáticos. Clave: se comprueba al compilar y transpila a JS; núcleo del curso.
- **Dart** — 2011 (Google), tipado y compilable a JS o nativo. Clave: motor de Flutter para apps multiplataforma.
- **Prototipos** — modelo de OO donde los objetos heredan de otros objetos, no de clases. Clave: rasgo distintivo de JavaScript.

## 🧩 Situación

Un proyecto JavaScript crece a 50.000 líneas y los errores de 'undefined is not a function' se disparan. Adoptar TypeScript hace que el compilador atrape esos fallos antes de ejecutar: la misma familia, con red de seguridad.

## 🔎 Ejemplo

TypeScript es JavaScript con tipos: mismo código, más garantías.

```text
JavaScript:  function doble(x) { return x * 2; }
TypeScript:  function doble(x: number): number { return x * 2; }
```

El segundo falla al compilar si alguien llama `doble("hola")`.

## ✍️ Práctica

TypeScript infiere y comprueba tipos como Java o Rust, pero desaparece al ejecutar (transpila a JS). ¿A qué modelo del núcleo se parece más y en qué se diferencia?

## ⚠️ Errores comunes

- **Creer que TypeScript es un lenguaje distinto de JS** → causa: no ver que es un superset → solución: recordar que todo JS válido es TS válido; TS solo añade tipos
- **Ignorar la asincronía** → causa: programar como si todo fuera secuencial → solución: entender el bucle de eventos, callbacks y async/await desde el inicio

## ❓ Preguntas frecuentes

- **¿TypeScript reemplaza a JavaScript?** No: lo complementa. Al final se convierte en JavaScript para poder ejecutarse.
- **¿Por qué JS corre en el servidor?** Node.js incrustó el motor V8 fuera del navegador; hizo de JS un lenguaje de propósito general.

## 🔗 Referencias

- Documentación de referencia de cada lenguaje del núcleo.

---

> [⏮️ Clase 020](../../parte-1-atlas-y-genealogia-de-los-lenguajes/020-familia-net-c-sharp-f-sharp-vb-net/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 022 ⏭️](../../parte-1-atlas-y-genealogia-de-los-lenguajes/022-familia-funcional-tipada-ml-haskell-ocaml-f-sharp-y-la-influencia-en-rust/README.md)
