# Clase 027 — Familia array y científica: APL, R, Julia, Fortran, MATLAB

> Parte **1 — Atlas y genealogía de los lenguajes** · ⏱️ Duración estimada: **75 min** · Nivel: **Fundamentos**
> ✅ **Clase construida.**

---

## 🎯 Objetivo

Conocer los lenguajes hechos para el cálculo numérico y el trabajo con datos. Fortran (1957) inauguró la computación científica; MATLAB y R dominan ingeniería y estadística; Julia es la apuesta moderna; APL introdujo operar sobre arreglos completos de una vez. Ninguno está en el núcleo, pero definen un estilo: la vectorización.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Explicar la vectorización (operar sobre arreglos completos sin bucles explícitos).
2. Situar Fortran, MATLAB, R y Julia según su dominio.
3. Reconocer por qué este estilo importa para datos y ciencia.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Vectorización | Operar sobre todo un arreglo de una vez |
| 2 | Fortran: el pionero | Cálculo numérico desde 1957, aún en HPC |
| 3 | R y MATLAB | Estadística e ingeniería, orientados a matrices |
| 4 | Julia: lo moderno | Rendimiento de C con comodidad de Python; multiple dispatch |

## 📖 Definiciones y características

- **Vectorización** — aplicar una operación a un arreglo entero sin escribir el bucle. Clave: código más corto y a menudo más rápido.
- **Fortran** — 1957 (IBM, John Backus), primer lenguaje de alto nivel. Clave: sigue siendo rey del cálculo científico de alto rendimiento.
- **R** — 1993, especializado en estadística y visualización. Clave: enorme ecosistema de análisis de datos.
- **Julia** — 2012, cálculo científico con rendimiento cercano a C. Clave: multiple dispatch como paradigma central.

## 🧩 Situación

Un análisis en Python con un bucle sobre un millón de números tarda segundos; reescrito con operaciones vectorizadas (estilo de esta familia) tarda milisegundos. Pensar en arreglos completos, no en elementos, cambia el rendimiento.

## 🔎 Ejemplo

Sumar dos vectores: con bucle vs. vectorizado.

```text
Con bucle (imperativo):
  PARA i: c[i] <- a[i] + b[i]

Vectorizado (estilo array, p. ej. R/Julia/NumPy):
  c <- a + b        # una sola operación sobre todo el arreglo
```

## ✍️ Práctica

Piensa cómo calcular el promedio de un millón de números 'a la manera de bucle' y 'a la manera vectorizada'. ¿Cuál expresa mejor la intención?

## ⚠️ Errores comunes

- **Escribir bucles donde cabe vectorizar** → causa: traer la mentalidad imperativa a datos → solución: pensar en operaciones sobre arreglos completos
- **Creer que estos lenguajes son 'de matemáticos'** → causa: descartarlos → solución: reconocer que dominan datos, ciencia y buena parte de la IA

## ❓ Preguntas frecuentes

- **¿Fortran sigue en uso?** Sí: mucho software de clima, física y HPC corre sobre Fortran altamente optimizado.
- **¿Julia sustituye a Python en datos?** Compite en rendimiento; Python gana en ecosistema. Conviven según el caso.

## 🔗 Referencias

- R. W. Sebesta — *Concepts of Programming Languages* (12ª ed., Pearson).
- M. L. Scott — *Programming Language Pragmatics* (4ª ed., Morgan Kaufmann).
- B. A. Tate — *Seven Languages in Seven Weeks* (Pragmatic Bookshelf).
- P. Van Roy y S. Haridi — *Concepts, Techniques, and Models of Computer Programming* (MIT Press).

---

> [⏮️ Clase 026](../../parte-1-atlas-y-genealogia-de-los-lenguajes/026-familia-de-sistemas-c-c-plus-plus-rust-zig/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 028 ⏭️](../../parte-1-atlas-y-genealogia-de-los-lenguajes/028-lenguajes-historicos-y-de-nicho-cobol-fortran-pascal-basic-bash/README.md)
