# Clase 004 — Descomposición y reconocimiento de patrones

> Parte **0 — Pensamiento computacional y el método políglota** · ⏱️ Duración estimada: **75 min** · Nivel: **Fundamentos**
> ✅ **Clase construida.**

---

## 🎯 Objetivo

Aprender a partir un problema grande en subproblemas manejables (descomposición) y a notar cuándo un subproblema ya lo resolviste antes con otra forma (reconocimiento de patrones). Son las dos habilidades que hacen escalable la programación.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Descomponer un problema en subproblemas independientes.
2. Reconocer un patrón repetido y nombrarlo.
3. Explicar cómo la descomposición se traduce en funciones y módulos.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Descomposición | Divide y vencerás: partes pequeñas se resuelven y prueban solas |
| 2 | Reconocimiento de patrones | Reutilizar una solución conocida ahorra trabajo y errores |
| 3 | De subproblema a función | La descomposición prefigura la modularidad (Parte 5) |

## 📖 Definiciones y características

- **Descomposición** — dividir un problema en subproblemas más simples. Clave: cada parte se resuelve y verifica por separado.
- **Patrón** — estructura de solución que reaparece en problemas distintos. Clave: reconocerlo evita reinventar.
- **Abstracción de subproblema** — tratar un subproblema resuelto como una caja negra. Clave: reduce la carga mental.

## 🧩 Situación

"Genera un reporte de ventas en PDF." Enorme. Descompuesto: (1) leer datos, (2) calcular totales, (3) dar formato, (4) exportar a PDF. Cada pieza es un problema conocido; el patrón "leer → transformar → escribir" reaparece en casi todo software.

## 🔎 Ejemplo

```text
Problema: promedio de las notas aprobadas
Descomposición:
  1. filtrar las notas >= 4      (patrón: filtrar)
  2. sumar las que quedaron      (patrón: reducir)
  3. dividir entre cuántas son   (patrón: contar)
```

Los patrones filtrar/reducir/contar reaparecen en la Parte 4 (map/filter/reduce).

## ✍️ Práctica

Descompón "corregir automáticamente un test de opción múltiple" en 3-4 subproblemas y nombra el patrón de cada uno.

## ⚠️ Errores comunes

- **Resolver todo en una sola función gigante** → causa: no descomponer → solución: extraer cada subproblema a su propia función
- **No ver que dos partes son el mismo patrón** → causa: falta de reconocimiento → solución: preguntar "¿esto se parece a algo que ya resolví?"

## ❓ Preguntas frecuentes

- **¿Cuánto descomponer?** Hasta que cada parte quepa en tu cabeza y se pueda probar sola.
- **¿Los patrones son los 'patrones de diseño'?** Aquí es más básico: estructuras de solución. Los patrones de diseño formales llegan en la Parte 9.

## 🔗 Referencias

- Documentación de referencia de cada lenguaje del núcleo.

---

> [⏮️ Clase 003](../../parte-0-pensamiento-computacional-y-el-metodo-poliglota/003-problema-contexto-entradas-proceso-y-salidas/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 005 ⏭️](../../parte-0-pensamiento-computacional-y-el-metodo-poliglota/005-abstraccion-restricciones-y-casos-limite/README.md)
