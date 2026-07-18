# Clase 003 — Problema, contexto, entradas, proceso y salidas

> Parte **0 — Pensamiento computacional y el método políglota** · ⏱️ Duración estimada: **75 min** · Nivel: **Fundamentos**
> ✅ **Clase construida.**

---

## 🎯 Objetivo

Antes de escribir una línea de código hay que **modelar** el problema: qué entra, qué sale, bajo qué reglas y en qué contexto. Ese modelo es independiente del lenguaje y es lo primero que define cada ficha del curso.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Descomponer un problema en entradas, proceso y salidas.
2. Identificar el contexto y las restricciones que condicionan la solución.
3. Escribir la especificación de un problema sin mencionar ningún lenguaje.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Entradas | Qué datos recibe el programa y de qué tipo |
| 2 | Proceso | Qué transformación ocurre entre entrada y salida |
| 3 | Salidas | Qué produce y cómo se observa el resultado |
| 4 | Contexto y restricciones | Condiciones que limitan las soluciones válidas |

## 📖 Definiciones y características

- **Especificación** — descripción de *qué* debe hacer un programa, no *cómo*. Clave: neutral al lenguaje.
- **Entrada** — dato que el programa recibe. Clave: define el dominio del problema.
- **Salida** — resultado observable. Clave: es lo que se verifica con casos.json.
- **Restricción** — condición que la solución debe respetar. Clave: acota el espacio de soluciones.

## 🧩 Situación

"Calcula el total de una venta." Suena trivial, pero: ¿el descuento es porcentaje o monto? ¿la cantidad puede ser 0? ¿el total lleva impuesto? Sin modelar entradas, proceso y salidas, dos personas resuelven problemas distintos.

## 🔎 Ejemplo

Especificación del problema de la venta (neutral al lenguaje):

```text
Entrada:  precio_unitario (real ≥ 0), cantidad (entero ≥ 0), descuento (real 0..1)
Proceso:  total = precio_unitario * cantidad * (1 - descuento)
Salida:   "Total: <total con 2 decimales>"
Límite:   cantidad = 0  ⇒  total = 0.00
```

Esta es la base de la clase 041, idéntica para los 10 lenguajes.

## ✍️ Práctica

Especifica (entrada/proceso/salida/límite) el problema "contar cuántas palabras tiene una frase". No escribas código.

## ⚠️ Errores comunes

- **Empezar a codificar sin especificar** → causa: saltarse el modelo → solución: escribir entrada/proceso/salida antes de tocar el teclado
- **Olvidar los casos límite** → causa: pensar solo el caso feliz → solución: listar valores extremos (0, vacío, negativo) en la especificación

## ❓ Preguntas frecuentes

- **¿Por qué no empezar a programar directo?** Porque el 80% de los bugs nacen de un problema mal entendido, no de mala sintaxis.
- **¿La especificación cambia por lenguaje?** No: es la parte que permanece. Por eso los casos.json sirven para los 10.

## 🔗 Referencias

- Documentación de referencia de cada lenguaje del núcleo.

---

> [⏮️ Clase 002](../../parte-0-pensamiento-computacional-y-el-metodo-poliglota/002-las-tres-clases-de-diferencia-sintactica-semantica-y-paradigmatica/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 004 ⏭️](../../parte-0-pensamiento-computacional-y-el-metodo-poliglota/004-descomposicion-y-reconocimiento-de-patrones/README.md)
