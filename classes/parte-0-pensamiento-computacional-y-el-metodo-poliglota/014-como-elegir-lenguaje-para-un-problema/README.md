# Clase 014 — Cómo elegir lenguaje para un problema

> Parte **0 — Pensamiento computacional y el método políglota** · ⏱️ Duración estimada: **75 min** · Nivel: **Fundamentos**
> ✅ **Clase construida.**

---

## 🎯 Objetivo

Cerrar la Parte 0 con criterio de ingeniería: dado un problema y su contexto, saber elegir el lenguaje adecuado según sus fortalezas, su ecosistema y las restricciones del proyecto — y justificar la decisión.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Enumerar criterios para elegir lenguaje (rendimiento, ecosistema, equipo, plataforma).
2. Asociar tipos de problema con familias adecuadas.
3. Justificar una elección de lenguaje con argumentos, no por moda.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Criterios de elección | Rendimiento, seguridad, ecosistema, equipo, plazo |
| 2 | Problema → familia | Cada tipo de problema tiene familias que encajan |
| 3 | Sistemas políglotas | Elegir por componente, no un solo lenguaje para todo |

## 📖 Definiciones y características

- **Criterio de selección** — factor que inclina la elección de lenguaje (rendimiento, plataforma, talento disponible). Clave: se ponderan, no hay uno absoluto.
- **Ecosistema** — librerías, herramientas y comunidad de un lenguaje. Clave: a veces pesa más que el lenguaje en sí.
- **Sistema políglota** — software que usa varios lenguajes, uno por componente. Clave: es lo normal en producción.

## 🧩 Situación

Un equipo quiere un servicio web con una parte de cálculo numérico intenso y un frontend interactivo. 'Usemos un solo lenguaje' suena simple, pero la respuesta real es políglota: TypeScript en el frontend, un backend en Go o Java, y quizá Rust o C para el núcleo numérico.

## 🔎 Ejemplo

```text
Problema                         Familias que encajan
-------------------------------  ----------------------------
Script rápido / automatización   Python, Bash, PHP
Servicio web de alto tráfico     Go, Java, C#
Núcleo de rendimiento crítico    C, Rust, C++
Interactividad en el navegador   JavaScript, TypeScript
Consulta y análisis de datos     SQL, Python (con librerías)
```

## ✍️ Práctica

Para 'una app móvil con sincronización en la nube', propón un lenguaje por componente (cliente, backend, base de datos) y justifica cada uno en una frase.

## ⚠️ Errores comunes

- **Elegir por moda o por comodidad** → causa: ignorar el problema y el contexto → solución: ponderar criterios reales: rendimiento, ecosistema, equipo, plataforma
- **Forzar un solo lenguaje para todo** → causa: creer que uniformidad = simplicidad → solución: aceptar que los sistemas reales son políglotas y elegir por componente

## ❓ Preguntas frecuentes

- **¿Hay un 'mejor lenguaje'?** No. Hay lenguajes mejores para un problema y contexto dados. Ese es todo el punto del curso.
- **¿Y si el equipo solo sabe uno?** El talento disponible es un criterio legítimo y a menudo decisivo.

## 🔗 Referencias

- Documentación de referencia de cada lenguaje del núcleo.

---

> [⏮️ Clase 013](../../parte-0-pensamiento-computacional-y-el-metodo-poliglota/013-el-concepto-en-la-familia-leer-un-lenguaje-que-no-conoces/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 015 ⏭️](../../parte-1-atlas-y-genealogia-de-los-lenguajes/015-el-arbol-genealogico-de-los-lenguajes-mapa-general/README.md)
