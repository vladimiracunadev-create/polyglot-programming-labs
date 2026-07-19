# Clase 009 — Complejidad y eficiencia: intuición de coste

> Parte **0 — Pensamiento computacional y el método políglota** · ⏱️ Duración estimada: **75 min** · Nivel: **Fundamentos**
> ✅ **Clase construida.**

---

## 🎯 Objetivo

Desarrollar la intuición de cuánto 'cuesta' un algoritmo en tiempo y memoria según crece la entrada, usando la notación O-grande de forma práctica. No es matemática por deporte: es saber por qué un programa que va bien con 100 datos se cae con 10 millones.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Estimar el orden de crecimiento (O(1), O(n), O(n²)) de un algoritmo simple.
2. Comparar dos soluciones por su coste, no solo por si funcionan.
3. Reconocer el bucle anidado como fuente típica de O(n²).

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Crecimiento con la entrada | Lo que importa es cómo escala, no el tiempo en un caso |
| 2 | O(1), O(n), O(n²), O(log n) | El vocabulario para comparar costes |
| 3 | Tiempo vs. memoria | A veces se cambia uno por el otro |

## 📖 Definiciones y características

- **Complejidad temporal** — cómo crece el número de operaciones con el tamaño de la entrada. Clave: se mide el orden, no los segundos.
- **O-grande** — cota superior del crecimiento (O(n), O(n²)…). Clave: describe el peor caso al escalar.
- **Bucle anidado** — un bucle dentro de otro. Clave: suele producir O(n²); vigílalo.

## 🧩 Situación

Dos funciones ordenan una lista. Con 10 elementos ambas tardan 'nada'. Con un millón, una tarda 1 segundo y la otra, 3 horas. La diferencia no se ve en la demo: se ve en el orden de complejidad, O(n log n) vs. O(n²).

## 🔎 Ejemplo

```text
Buscar en lista NO ordenada  ⇒ recorrer todo        ⇒ O(n)
Buscar en lista ordenada     ⇒ búsqueda binaria    ⇒ O(log n)
Comparar todos con todos     ⇒ bucle dentro de bucle ⇒ O(n²)
Acceder a lista[i]           ⇒ directo             ⇒ O(1)
```

## ✍️ Práctica

¿Cuál es el orden de un algoritmo que, para cada persona de una lista, la compara con todas las demás? (Pista: bucle anidado.)

## ⚠️ Errores comunes

- **Medir con entradas pequeñas** → causa: el coste solo se nota al escalar → solución: razonar el orden, no cronometrar un caso chico
- **Optimizar sin medir** → causa: atacar lo que no es el cuello de botella → solución: primero identificar el orden dominante, luego optimizar

## ❓ Preguntas frecuentes

- **¿Siempre gana el de menor O?** Para entradas grandes, sí. Para pequeñas, un O(n²) simple puede ganar a un O(n log n) complejo.
- **¿Necesito las matemáticas formales?** Aquí basta la intuición: contar cuántas veces se repite el trabajo al crecer n.

## 🔗 Referencias

- G. Polya — *How to Solve It* (Princeton University Press).
- H. Abelson y G. J. Sussman — *Structure and Interpretation of Computer Programs* (2ª ed., MIT Press) — [gratis online](https://mitpress.mit.edu/9780262510875/).
- A. Hunt y D. Thomas — *The Pragmatic Programmer* (2ª ed., Addison-Wesley).
- T. Cormen, C. Leiserson, R. Rivest y C. Stein — *Introduction to Algorithms* (4ª ed., MIT Press).

---

> [⏮️ Clase 008](../../parte-0-pensamiento-computacional-y-el-metodo-poliglota/008-trazado-manual-y-ejecucion-simbolica/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 010 ⏭️](../../parte-0-pensamiento-computacional-y-el-metodo-poliglota/010-legibilidad-estilo-e-idiomatica/README.md)
