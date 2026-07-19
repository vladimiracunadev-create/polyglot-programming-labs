# Clase 010 — Legibilidad, estilo e idiomática

> Parte **0 — Pensamiento computacional y el método políglota** · ⏱️ Duración estimada: **75 min** · Nivel: **Fundamentos**
> ✅ **Clase construida.**

---

## 🎯 Objetivo

Entender que el código se lee muchas más veces de las que se escribe, y que cada lenguaje tiene su forma 'idiomática' (la que un experto reconoce como natural). Escribir legible e idiomático no es estética: es mantenibilidad.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Explicar por qué la legibilidad importa más que la brevedad.
2. Reconocer código idiomático frente a una traducción mecánica.
3. Aplicar nombres y estructura que comuniquen intención.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | El código se lee más que se escribe | Optimizar para quien lo lea (incluido tu yo futuro) |
| 2 | Idiomática por lenguaje | Lo natural en Python no lo es en Go |
| 3 | Nombres que comunican | Un buen nombre ahorra un comentario |

## 📖 Definiciones y características

- **Legibilidad** — facilidad con que un humano entiende el código. Clave: prima sobre la astucia.
- **Idiomática** — escribir como lo haría un experto del lenguaje. Clave: aprovecha sus convenciones y su paradigma.
- **Código listo (clever)** — código ingenioso pero difícil de leer. Clave: casi siempre es un error de criterio.

## 🧩 Situación

Un desarrollador escribe en Python un bucle `for i in range(len(lista))` para acceder por índice, como haría en C. Funciona, pero cualquier pythonista escribiría `for x in lista`. La versión idiomática se lee y se mantiene mejor.

## 🔎 Ejemplo

```text
No idiomático (Python, estilo C):
    for i in range(len(nombres)):
        print(nombres[i])

Idiomático (Python):
    for nombre in nombres:
        print(nombre)
```

Mismo resultado; el segundo comunica la intención sin ruido.

## ✍️ Práctica

Busca un fragmento tuyo de hace meses. ¿Lo entiendes en 10 segundos? Reescríbelo para que sí, cambiando nombres y estructura.

## ⚠️ Errores comunes

- **Priorizar líneas cortas sobre claridad** → causa: confundir brevedad con calidad → solución: preferir lo legible aunque ocupe una línea más
- **Escribir todos los lenguajes con el mismo estilo** → causa: ignorar la idiomática → solución: aprender las convenciones de cada lenguaje del núcleo

## ❓ Preguntas frecuentes

- **¿La idiomática es subjetiva?** Menos de lo que parece: cada comunidad tiene guías de estilo (PEP 8, gofmt, rustfmt).
- **¿Legible o rápido?** Legible por defecto; rápido solo donde midas que hace falta.

## 🔗 Referencias

- G. Polya — *How to Solve It* (Princeton University Press).
- H. Abelson y G. J. Sussman — *Structure and Interpretation of Computer Programs* (2ª ed., MIT Press) — [gratis online](https://mitpress.mit.edu/9780262510875/).
- A. Hunt y D. Thomas — *The Pragmatic Programmer* (2ª ed., Addison-Wesley).
- T. Cormen, C. Leiserson, R. Rivest y C. Stein — *Introduction to Algorithms* (4ª ed., MIT Press).

---

> [⏮️ Clase 009](../../parte-0-pensamiento-computacional-y-el-metodo-poliglota/009-complejidad-y-eficiencia-intuicion-de-coste/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 011 ⏭️](../../parte-0-pensamiento-computacional-y-el-metodo-poliglota/011-anatomia-de-una-ficha-de-transferencia-y-como-estudiarla/README.md)
