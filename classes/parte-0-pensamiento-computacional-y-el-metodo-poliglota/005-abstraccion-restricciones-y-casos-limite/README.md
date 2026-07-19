# Clase 005 — Abstracción, restricciones y casos límite

> Parte **0 — Pensamiento computacional y el método políglota** · ⏱️ Duración estimada: **75 min** · Nivel: **Fundamentos**
> ✅ **Clase construida.**

---

## 🎯 Objetivo

Dominar tres herramientas del pensamiento: la abstracción (quedarse con lo esencial e ignorar el detalle), las restricciones (las reglas que la solución debe cumplir) y los casos límite (las entradas extremas donde los programas suelen fallar).

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Abstraer un problema quedándote con lo relevante.
2. Enumerar las restricciones explícitas e implícitas de un problema.
3. Identificar los casos límite antes de programar.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Abstracción | Ignorar el ruido para razonar sobre lo esencial |
| 2 | Restricciones | Definen qué soluciones son válidas |
| 3 | Casos límite | El vacío, el cero, el negativo, el máximo: donde se rompen los programas |

## 📖 Definiciones y características

- **Abstracción** — representar solo los aspectos relevantes de algo. Clave: un mapa no es el territorio, y por eso es útil.
- **Restricción** — condición que la solución debe respetar (rango, formato, rendimiento). Clave: acota lo válido.
- **Caso límite** — entrada extrema o inusual (vacío, 0, negativo, enorme). Clave: donde nacen la mayoría de los bugs.

## 🧩 Situación

Un programa suma precios y funciona perfecto en las demos. En producción falla: llegó una lista vacía y dividió entre cero al calcular el promedio. El caso límite "lista vacía" no se pensó.

## 🔎 Ejemplo

```text
Problema: promedio de una lista de números
Abstracción: solo importan los números, no de dónde vienen
Restricción: el resultado es un real
Casos límite:
  - lista vacía      ⇒ ¿0? ¿error? (¡hay que decidirlo!)
  - un solo elemento ⇒ el promedio es ese elemento
  - números enormes  ⇒ ¿desbordamiento?
```

## ✍️ Práctica

Para "buscar el mayor de una lista", enumera 3 casos límite y decide qué hace el programa en cada uno.

## ⚠️ Errores comunes

- **Probar solo el caso feliz** → causa: olvidar los extremos → solución: escribir los casos límite en casos.json desde el inicio
- **Abstraer de más o de menos** → causa: quedarse sin datos clave o con ruido → solución: revisar que la abstracción conserve lo que el problema necesita

## ❓ Preguntas frecuentes

- **¿Los casos límite son los tests?** Son la semilla de los tests: cada caso límite debería ser un caso de prueba.
- **¿Cómo sé si abstraje bien?** Si puedes resolver el problema con tu abstracción sin volver a los detalles, está bien.

## 🔗 Referencias

- G. Polya — *How to Solve It* (Princeton University Press).
- H. Abelson y G. J. Sussman — *Structure and Interpretation of Computer Programs* (2ª ed., MIT Press) — [gratis online](https://mitpress.mit.edu/9780262510875/).
- A. Hunt y D. Thomas — *The Pragmatic Programmer* (2ª ed., Addison-Wesley).
- T. Cormen, C. Leiserson, R. Rivest y C. Stein — *Introduction to Algorithms* (4ª ed., MIT Press).

---

> [⏮️ Clase 004](../../parte-0-pensamiento-computacional-y-el-metodo-poliglota/004-descomposicion-y-reconocimiento-de-patrones/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 006 ⏭️](../../parte-0-pensamiento-computacional-y-el-metodo-poliglota/006-algoritmos-correccion-y-terminacion/README.md)
