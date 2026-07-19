# 🎓 Examen final por perfil

> [⬅️ Volver al programa](../README.md) · [🧭 Rutas por perfil](../rutas/README.md) · [📊 Rúbrica](rubrica-evaluacion.md)

Cada [ruta por perfil](../rutas/README.md) cierra con un **examen final** que combina teoría,
transferencia real de código y comunicación — igual que una entrevista técnica. Todos comparten
la misma estructura; cambia el contenido.

## Estructura común (100 puntos)

| Bloque | Peso | Formato |
|---|---:|---|
| **Teoría** | 25 | Quiz de las partes de la ruta ([autoevaluación](../autoevaluaciones/README.md)) ≥ 70 %. |
| **Transferencia** | 50 | Portar un programa a otro lenguaje y **pasar el verificador de equivalencia** con código idiomático. |
| **Explicación** | 25 | Documento breve que clasifique las diferencias encontradas (sintáctica / semántica / paradigmática), evaluado con la [rúbrica](rubrica-evaluacion.md). |

**Aprobado:** ≥ 70/100 y transferencia ≥ 30/50.

La regla de oro del bloque de transferencia: **no se acepta una traducción literal**. Si el
resultado parece el lenguaje de origen escrito con otra sintaxis, es nivel C aunque los casos pasen.

---

## 🐍 Vengo de Python / lenguajes dinámicos

- **Teoría:** quizzes de las Partes 3, 5, 8.
- **Transferencia:** toma una clase de la Parte 6 resuelta en Python y llévala a **Rust** y a **Java**. Deberás enfrentarte a tipos explícitos, nulabilidad y propiedad.
- **Explicación:** qué garantías te dio el compilador que el intérprete no te daba, y qué te costó en expresividad.

## ⚙️ Quiero sistemas (C / Rust)

- **Teoría:** quizzes de las Partes 6, 8, 10.
- **Transferencia:** toma una clase de la Parte 8 y resuélvela en **C** (gestión manual) y en **Rust** (propiedad y préstamos); luego contrástala con la versión en **Go** (GC).
- **Explicación:** dónde vive cada dato (pila/heap), quién lo libera y qué error de memoria evita cada modelo.

## 🌐 Web (JavaScript / TypeScript)

- **Teoría:** quizzes de las Partes 3, 7, 10.
- **Transferencia:** toma una clase asíncrona de la Parte 7 y llévala de **JavaScript** a **TypeScript** con tipos estrictos, y luego a **Go** con canales.
- **Explicación:** qué es el bucle de eventos frente a la concurrencia con hilos/goroutines, y qué aporta el tipado estructural de TS.

## 🏢 Backend de empresa (Java / C# / Go)

- **Teoría:** quizzes de las Partes 5, 7, 9.
- **Transferencia:** toma una clase de la Parte 7 (interfaces/traits) y resuélvela en **Java**, **C#** y **Go**, respetando el estilo de cada uno.
- **Explicación:** subtipado nominal (Java/C#) frente a satisfacción implícita de interfaces (Go), y qué implica para el acoplamiento.

## 🗃️ Datos (SQL)

- **Teoría:** quizzes de las Partes 6, 7.
- **Transferencia:** toma una consulta declarativa de la Parte 7 en **SQL** y reprodúcela imperativamente en **Python** y en **Java**, obteniendo la misma salida.
- **Explicación:** qué decide el motor por ti en SQL (el *cómo*) y qué tuviste que decidir tú al hacerlo imperativo.

---

## 🏁 Examen integrador (programa completo)

Si hiciste las 176 clases, el examen final es el
[proyecto integrador de la Parte 11](../classes/parte-11-proyecto-integrador-poliglota/README.md),
evaluado con la [rúbrica del proyecto](rubrica-evaluacion.md#4-rúbrica-del-proyecto-integrador-parte-11).

Se añade una prueba de la tesis del programa: **elige un lenguaje del [Atlas](../atlas/README.md)
que nunca hayas usado**, ubícalo en su familia, y resuelve con él una clase cualquiera del núcleo.
Si lo consigues apoyándote en lo que sabes de su familia, el programa cumplió su objetivo.
