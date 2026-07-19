# Clase 002 — Las tres clases de diferencia: sintáctica, semántica y paradigmática

> Parte **0 — Pensamiento computacional y el método políglota** · ⏱️ Duración estimada: **75 min** · Nivel: **Fundamentos**
> ✅ **Clase construida.**

---

## 🎯 Objetivo

Dar el marco que se usa en **cada** comparación del curso. Cuando dos lenguajes difieren, la diferencia es de una de tres clases: sintáctica (se escribe distinto pero significa lo mismo), semántica (cambia el comportamiento, el tipo, la memoria) o paradigmática (invita a estructurar la solución de otra manera).

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Clasificar una diferencia entre lenguajes como sintáctica, semántica o paradigmática.
2. Dar ejemplos propios de cada clase de diferencia.
3. Explicar por qué confundirlas lleva a traducir mecánicamente en vez de programar idiomáticamente.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Diferencia sintáctica | La más superficial: solo cambia cómo se escribe |
| 2 | Diferencia semántica | Cambia qué ocurre: tipos, mutabilidad, memoria, errores |
| 3 | Diferencia paradigmática | Cambia cómo se piensa la solución |
| 4 | Traducción vs. idiomática | Por qué copiar sintaxis produce código antinatural |

## 📖 Definiciones y características

- **Diferencia sintáctica** — distinta escritura, mismo significado esencial. Clave: la más fácil de salvar.
- **Diferencia semántica** — distinto comportamiento observable. Clave: la que causa bugs al portar código.
- **Diferencia paradigmática** — distinta forma de estructurar el problema. Clave: exige cambiar de mentalidad.
- **Código idiomático** — solución escrita como la escribiría un experto de ese lenguaje. Clave: aprovecha el paradigma.

## 🧩 Situación

Portas un bucle de JavaScript a Rust cambiando solo las llaves y los `;`. Compila… pero el programa se comporta distinto porque en Rust el valor se *movió* y ya no puedes usarlo. No era una diferencia sintáctica: era semántica.

## 🔎 Ejemplo

```text
Sintáctica:   for (i=0;i<n;i++)      vs   for i in range(n)
              (mismo bucle, otra escritura)

Semántica:    x = y (copia en C)     vs   x = y (mueve en Rust)
              (misma escritura, otro comportamiento)

Paradigmática: recorrer una lista con un bucle
              vs   describir el resultado con SQL (SELECT ...)
```

## ✍️ Práctica

Toma `a == b`. En Java compara referencias para objetos; en Python compara valor. ¿De qué clase de diferencia se trata? (Respuesta: semántica.)

## ⚠️ Errores comunes

- **Portar código cambiando solo la sintaxis** → causa: asumir que todo es sintáctico → solución: verificar siempre si hay diferencia semántica (tipos, memoria, mutabilidad)
- **Forzar el estilo de un lenguaje en otro** → causa: ignorar el paradigma destino → solución: escribir idiomático: adaptar la estructura, no solo las palabras

## ❓ Preguntas frecuentes

- **¿Cuál es la más peligrosa?** La semántica: el código compila y parece correcto, pero se comporta distinto.
- **¿Y la paradigmática se puede evitar?** A veces sí (imperativo en casi todos), pero perderías la ventaja del lenguaje destino.

## 🔗 Referencias

- G. Polya — *How to Solve It* (Princeton University Press).
- H. Abelson y G. J. Sussman — *Structure and Interpretation of Computer Programs* (2ª ed., MIT Press) — [gratis online](https://mitpress.mit.edu/9780262510875/).
- A. Hunt y D. Thomas — *The Pragmatic Programmer* (2ª ed., Addison-Wesley).
- T. Cormen, C. Leiserson, R. Rivest y C. Stein — *Introduction to Algorithms* (4ª ed., MIT Press).

---

> [⏮️ Clase 001](../../parte-0-pensamiento-computacional-y-el-metodo-poliglota/001-que-es-programar-y-por-que-comparar-lenguajes-la-tesis-poliglota/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 003 ⏭️](../../parte-0-pensamiento-computacional-y-el-metodo-poliglota/003-problema-contexto-entradas-proceso-y-salidas/README.md)
