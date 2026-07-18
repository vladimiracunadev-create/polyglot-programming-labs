# Clase 007 — Pseudocódigo neutral: escribir sin lenguaje

> Parte **0 — Pensamiento computacional y el método políglota** · ⏱️ Duración estimada: **75 min** · Nivel: **Fundamentos**
> ✅ **Clase construida.**

---

## 🎯 Objetivo

Aprender a expresar un algoritmo en **pseudocódigo**: una notación legible, independiente de cualquier lenguaje, que captura la lógica sin comprometerse con una sintaxis. Es el puente entre la idea y las 10 implementaciones.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Escribir un algoritmo en pseudocódigo claro y neutral.
2. Traducir pseudocódigo a cualquier lenguaje del núcleo.
3. Evitar el 'pseudocódigo' que en realidad es un lenguaje disfrazado.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Convenciones del pseudocódigo | Un vocabulario mínimo y consistente |
| 2 | Neutralidad | No favorecer la sintaxis de ningún lenguaje |
| 3 | Del pseudocódigo al código | Cómo cada lenguaje 'rellena' la misma lógica |

## 📖 Definiciones y características

- **Pseudocódigo** — descripción de un algoritmo en lenguaje estructurado pero informal. Clave: legible por humanos, neutral.
- **Notación neutral** — sin sintaxis específica de un lenguaje real. Clave: se traduce igual de fácil a los 10.
- **Asignación (<-)** — dar un valor a un nombre. Clave: convención neutral en vez de `=`, `:=` o `let`.

## 🧩 Situación

En una entrevista te piden 'resolverlo en el lenguaje que quieras'. Si primero escribes el pseudocódigo, la traducción a Python, Java o Go es mecánica; si vas directo al código, te enredas con la sintaxis y pierdes la lógica.

## 🔎 Ejemplo

El mismo algoritmo en pseudocódigo neutral, listo para traducir:

```text
LEER precio, cantidad, descuento
subtotal <- precio * cantidad
total    <- subtotal * (1 - descuento)
ESCRIBIR "Total: " + FORMATEAR(total, 2 decimales)
```

Compara con las implementaciones reales en la [clase 041](../../parte-3-valores-tipos-y-variables/041-literales-valores-variables-y-constantes/README.md).

## ✍️ Práctica

Escribe en pseudocódigo el algoritmo "invertir una cadena de texto". No uses funciones específicas de ningún lenguaje.

## ⚠️ Errores comunes

- **Pseudocódigo que es Python disfrazado** → causa: usar `for i in range` y métodos reales → solución: usar PARA/MIENTRAS/SI y verbos neutrales (LEER, ESCRIBIR)
- **Demasiado detalle o demasiado vago** → causa: perder la lógica en ruido o en ambigüedad → solución: capturar cada paso esencial, sin sintaxis

## ❓ Preguntas frecuentes

- **¿Hay un estándar de pseudocódigo?** No universal. Este curso usa <-, PARA, MIENTRAS, SI, LEER, ESCRIBIR de forma consistente.
- **¿Siempre debo escribirlo?** Para problemas nuevos o difíciles, sí. Para triviales, va en tu cabeza.

## 🔗 Referencias

- Documentación de referencia de cada lenguaje del núcleo.

---

> [⏮️ Clase 006](../../parte-0-pensamiento-computacional-y-el-metodo-poliglota/006-algoritmos-correccion-y-terminacion/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 008 ⏭️](../../parte-0-pensamiento-computacional-y-el-metodo-poliglota/008-trazado-manual-y-ejecucion-simbolica/README.md)
