# Clase 015 — El árbol genealógico de los lenguajes: mapa general

> Parte **1 — Atlas y genealogía de los lenguajes** · ⏱️ Duración estimada: **75 min** · Nivel: **Fundamentos**
> ✅ **Clase construida.**

---

## 🎯 Objetivo

Ver el mapa completo de las familias de lenguajes y sus antepasados comunes. Casi todos los lenguajes actuales descienden de tres troncos de los años 50-60: Fortran (cálculo), Lisp (funcional/simbólico) y ALGOL (estructurado, del que nace la familia de llaves). Entender el árbol convierte 'decenas de lenguajes' en 'unas pocas familias con variaciones'.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Ubicar los tres troncos históricos (Fortran, Lisp, ALGOL) y qué aportó cada uno.
2. Situar cada lenguaje del núcleo en su rama del árbol.
3. Explicar por qué conocer una familia acelera aprender a sus miembros.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Los tres troncos | Fortran, Lisp y ALGOL originan casi todo lo demás |
| 2 | Ramas principales | Llaves, dinámicos, funcionales, declarativos, lógicos |
| 3 | Herencia de rasgos | Sintaxis, tipos y paradigma se heredan de los ancestros |
| 4 | Representante y primos | Un lenguaje del núcleo por rama abre la puerta a las demás |

## 📖 Definiciones y características

- **Tronco** — lenguaje raíz del que desciende una familia (Fortran, Lisp, ALGOL). Clave: define rasgos que perduran décadas.
- **Familia** — grupo de lenguajes con ancestro y rasgos comunes. Clave: aprender uno facilita los demás.
- **ALGOL** — lenguaje de 1958-60 que introdujo la programación estructurada y los bloques. Clave: padre de C, y por tanto de casi toda la sintaxis de llaves.
- **Influencia** — rasgo que un lenguaje toma de otro sin ser de su familia (p. ej. Rust toma tipos de ML). Clave: el árbol tiene cruces, no solo ramas.

## 🧩 Situación

Un principiante ve una lista de 50 lenguajes y se abruma. Un veterano ve cinco familias y sabe que dominar un representante de cada una cubre el 90% de lo que encontrará. El árbol es lo que separa una visión de la otra.

## 🔎 Ejemplo

Árbol simplificado (año de nacimiento aproximado):

```text
Fortran (1957) ── cálculo numérico ── Fortran, MATLAB, Julia
Lisp (1958) ───── simbólico/funcional ─ Scheme, Clojure, (influye en ML)
ALGOL (1958) ──── estructurado ──┬── C (1972) ── C++, Java, C#, Go, Rust
                                 ├── Pascal (1970)
                                 └── (influye en casi todo)
ML (1973) ─────── funcional tipado ── OCaml, Haskell, F#, (influye en Rust)
Prolog (1972) ─── lógico ──────────── Datalog
```

## ✍️ Práctica

Dibuja tu propio árbol con los 10 lenguajes del núcleo. ¿Cuáles comparten la sintaxis de llaves de C? ¿Cuál no encaja en ninguna rama imperativa? (Pista: SQL.)

## ⚠️ Errores comunes

- **Tratar cada lenguaje como algo aislado y nuevo** → causa: no ver la familia → solución: identificar el ancestro y estudiar los rasgos heredados
- **Creer que el árbol son ramas puras sin cruces** → causa: ignorar las influencias → solución: recordar que Rust toma de C y de ML a la vez

## ❓ Preguntas frecuentes

- **¿Hay un árbol 'oficial'?** No único, pero las relaciones históricas son bien conocidas y consistentes entre fuentes.
- **¿Dónde va SQL?** Fuera del tronco imperativo: es declarativo, primo de la rama lógica (Prolog).

## 🔗 Referencias

- R. W. Sebesta — *Concepts of Programming Languages* (12ª ed., Pearson).
- M. L. Scott — *Programming Language Pragmatics* (4ª ed., Morgan Kaufmann).
- B. A. Tate — *Seven Languages in Seven Weeks* (Pragmatic Bookshelf).
- P. Van Roy y S. Haridi — *Concepts, Techniques, and Models of Computer Programming* (MIT Press).

---

> [⏮️ Clase 014](../../parte-0-pensamiento-computacional-y-el-metodo-poliglota/014-como-elegir-lenguaje-para-un-problema/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 016 ⏭️](../../parte-1-atlas-y-genealogia-de-los-lenguajes/016-como-nace-y-evoluciona-un-lenguaje-estandares-versiones-y-ecosistemas/README.md)
