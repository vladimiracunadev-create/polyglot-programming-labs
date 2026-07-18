# Clase 024 — Familia lógica y declarativa: SQL, Prolog, Datalog

> Parte **1 — Atlas y genealogía de los lenguajes** · ⏱️ Duración estimada: **75 min** · Nivel: **Fundamentos**
> ✅ **Clase construida.**

---

## 🎯 Objetivo

Conocer los lenguajes donde describes QUÉ quieres, no CÓMO obtenerlo. SQL (en el núcleo) describe conjuntos de datos; Prolog describe hechos y reglas y deja que el motor deduzca. Es el salto paradigmático más grande respecto de los lenguajes imperativos del curso.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Distinguir programación declarativa de imperativa con un ejemplo.
2. Explicar el modelo de SQL (consultas sobre conjuntos) y de Prolog (hechos, reglas, unificación).
3. Reconocer cuándo el enfoque declarativo simplifica un problema.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Declarativo vs. imperativo | Describir el resultado vs. describir los pasos |
| 2 | SQL: consultas sobre datos | El motor decide cómo ejecutar la consulta |
| 3 | Prolog: hechos y reglas | Deducción por unificación y backtracking |
| 4 | Datalog | Subconjunto de Prolog para consultas de datos |

## 📖 Definiciones y características

- **Declarativo** — paradigma en el que se describe el resultado deseado, no el algoritmo. Clave: el motor decide el 'cómo'.
- **SQL** — 1974 (IBM), lenguaje de consulta de bases de datos relacionales. Clave: núcleo del curso; declarativo sobre conjuntos.
- **Prolog** — 1972 (Colmerauer, Kowalski), programación lógica. Clave: describes hechos y reglas; el motor deduce por unificación.
- **Unificación** — mecanismo que hace coincidir términos para satisfacer una consulta lógica. Clave: motor de la deducción en Prolog.

## 🧩 Situación

Para obtener 'los clientes con más de 3 pedidos', un lenguaje imperativo recorre listas y acumula contadores. SQL lo dice en una frase (`GROUP BY ... HAVING COUNT(*) > 3`) y el motor se encarga del cómo. Ese cambio de mentalidad es el corazón de lo declarativo.

## 🔎 Ejemplo

Mismo objetivo, dos mentalidades:

```text
Imperativo (pseudocódigo):
  PARA cada cliente: contar pedidos; SI > 3, añadir a resultado

Declarativo (SQL):
  SELECT cliente FROM pedidos GROUP BY cliente HAVING COUNT(*) > 3;

Lógico (Prolog):
  abuelo(X, Z) :- padre(X, Y), padre(Y, Z).
```

## ✍️ Práctica

Escribe en una frase, sin código, qué resultado pides (no cómo). Luego nota que eso es 'pensar declarativamente'. Compáralo con cómo lo harías con un bucle.

## ⚠️ Errores comunes

- **Programar SQL como si fuera imperativo** → causa: querer controlar el 'cómo' → solución: confiar en el optimizador y describir solo el 'qué'
- **Creer que lo declarativo sirve para todo** → causa: forzarlo donde el control paso a paso es necesario → solución: usarlo donde el problema es 'describir un resultado'

## ❓ Preguntas frecuentes

- **¿SQL es 'de verdad' un lenguaje de programación?** Es un lenguaje declarativo especializado; Turing-completo con extensiones, pero su fuerte es consultar datos.
- **¿Dónde se usa Prolog hoy?** IA simbólica, sistemas expertos, análisis de lenguaje y verificación; nicho pero potente.

## 🔗 Referencias

- Documentación de referencia de cada lenguaje del núcleo.

---

> [⏮️ Clase 023](../../parte-1-atlas-y-genealogia-de-los-lenguajes/023-familia-lisp-scheme-racket-clojure-emacs-lisp/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 025 ⏭️](../../parte-1-atlas-y-genealogia-de-los-lenguajes/025-familia-concurrente-actor-erlang-elixir-y-el-csp-de-go/README.md)
