# Clase 006 — Algoritmos: corrección y terminación

> Parte **0 — Pensamiento computacional y el método políglota** · ⏱️ Duración estimada: **75 min** · Nivel: **Fundamentos**
> ✅ **Clase construida.**

---

## 🎯 Objetivo

Entender qué es un algoritmo y las dos propiedades que lo hacen fiable: **corrección** (produce el resultado correcto para toda entrada válida) y **terminación** (siempre acaba, no se queda en un bucle infinito).

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Definir algoritmo y sus propiedades esenciales.
2. Argumentar informalmente por qué un algoritmo es correcto.
3. Detectar por qué un bucle podría no terminar.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Qué es un algoritmo | Una receta precisa y finita de pasos |
| 2 | Corrección | Da la respuesta correcta para toda entrada válida |
| 3 | Terminación | Siempre acaba; el bucle avanza hacia su fin |
| 4 | Invariante y variante | Herramientas para razonar sobre bucles |

## 📖 Definiciones y características

- **Algoritmo** — secuencia finita y precisa de pasos que resuelve un problema. Clave: finita y sin ambigüedad.
- **Corrección** — el algoritmo produce la salida especificada para toda entrada válida. Clave: se argumenta, no se supone.
- **Terminación** — el algoritmo acaba en un número finito de pasos. Clave: algo debe decrecer hacia un límite.
- **Invariante de bucle** — condición verdadera en cada vuelta del bucle. Clave: prueba la corrección.

## 🧩 Situación

Un algoritmo de búsqueda binaria es rapidísimo… hasta que alguien escribe `fin = medio` en vez de `fin = medio - 1` y el bucle deja de decrecer: nunca termina. Terminación no es un detalle.

## 🔎 Ejemplo

```text
ALGORITMO mayor(lista):
    mayor <- lista[0]           # invariante: 'mayor' es el máximo de lo visto
    PARA cada x en lista[1..]:
        SI x > mayor: mayor <- x
    DEVOLVER mayor

Terminación: la lista es finita ⇒ el bucle da pasos finitos.
Corrección: el invariante garantiza que al final 'mayor' es el máximo total.
```

## ✍️ Práctica

Escribe un algoritmo que cuente cuántos números pares hay en una lista y argumenta en una frase por qué termina.

## ⚠️ Errores comunes

- **Bucle que no decrece** → causa: el índice o la condición no avanzan hacia el fin → solución: asegurar que algo cambia en cada vuelta acercándose al límite
- **Asumir corrección sin argumentar** → causa: confiar en que 'parece bien' → solución: buscar el invariante que lo garantiza

## ❓ Preguntas frecuentes

- **¿Hay que demostrar formalmente todo?** No en este curso: basta un argumento informal claro de por qué es correcto y termina.
- **¿Un programa que no termina siempre es un bug?** Casi siempre. Excepción: servicios que corren en un bucle eventos a propósito.

## 🔗 Referencias

- Documentación de referencia de cada lenguaje del núcleo.

---

> [⏮️ Clase 005](../../parte-0-pensamiento-computacional-y-el-metodo-poliglota/005-abstraccion-restricciones-y-casos-limite/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 007 ⏭️](../../parte-0-pensamiento-computacional-y-el-metodo-poliglota/007-pseudocodigo-neutral-escribir-sin-lenguaje/README.md)
