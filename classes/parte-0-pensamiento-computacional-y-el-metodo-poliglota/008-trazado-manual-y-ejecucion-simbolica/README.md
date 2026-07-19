# Clase 008 — Trazado manual y ejecución simbólica

> Parte **0 — Pensamiento computacional y el método políglota** · ⏱️ Duración estimada: **75 min** · Nivel: **Fundamentos**
> ✅ **Clase construida.**

---

## 🎯 Objetivo

Aprender a 'ejecutar' un algoritmo con papel y lápiz: seguir el valor de cada variable paso a paso (trazado) para verificar que hace lo que crees, antes de ejecutarlo en una máquina. Es la habilidad de depuración más fundamental.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Trazar la ejecución de un algoritmo con una tabla de variables.
2. Detectar un error de lógica sin ejecutar el programa.
3. Predecir la salida de un fragmento leyéndolo.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Tabla de trazado | Registrar el estado de las variables vuelta a vuelta |
| 2 | Ejecución simbólica | Razonar con valores generales, no solo concretos |
| 3 | Trazar para depurar | Encontrar el error donde el estado se desvía |

## 📖 Definiciones y características

- **Trazado** — seguir a mano el valor de cada variable en cada paso. Clave: revela dónde se desvía la lógica.
- **Estado** — el conjunto de valores de todas las variables en un instante. Clave: el programa avanza cambiando el estado.
- **Ejecución simbólica** — trazar con símbolos (x, n) en vez de números concretos. Clave: cubre todos los casos a la vez.

## 🧩 Situación

Tu bucle debería sumar 1+2+3 = 6 pero devuelve 3. En vez de ejecutar 20 veces cambiando cosas al azar, trazas a mano: descubres que inicializas `suma` dentro del bucle, reiniciándola cada vuelta.

## 🔎 Ejemplo

Trazado de `suma <- 0; PARA i en 1..3: suma <- suma + i`:

```text
paso | i | suma
-----|---|-----
inic | - | 0
  1  | 1 | 1
  2  | 2 | 3
  3  | 3 | 6   ⇐ salida
```

## ✍️ Práctica

Traza a mano `x <- 5; MIENTRAS x > 0: ESCRIBIR x; x <- x - 2`. ¿Qué imprime? ¿Termina?

## ⚠️ Errores comunes

- **Depurar cambiando cosas al azar** → causa: no entender el estado real → solución: trazar a mano hasta ver dónde se desvía
- **Trazar solo un caso concreto** → causa: no generalizar → solución: usar ejecución simbólica para cubrir todos los casos

## ❓ Preguntas frecuentes

- **¿No es más rápido usar el debugger?** El debugger traza por ti, pero si no sabes trazar, no entiendes lo que muestra.
- **¿Cuándo trazar?** Cuando un resultado te sorprende: el trazado localiza el paso exacto del error.

## 🔗 Referencias

- G. Polya — *How to Solve It* (Princeton University Press).
- H. Abelson y G. J. Sussman — *Structure and Interpretation of Computer Programs* (2ª ed., MIT Press) — [gratis online](https://mitpress.mit.edu/9780262510875/).
- A. Hunt y D. Thomas — *The Pragmatic Programmer* (2ª ed., Addison-Wesley).
- T. Cormen, C. Leiserson, R. Rivest y C. Stein — *Introduction to Algorithms* (4ª ed., MIT Press).

---

> [⏮️ Clase 007](../../parte-0-pensamiento-computacional-y-el-metodo-poliglota/007-pseudocodigo-neutral-escribir-sin-lenguaje/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 009 ⏭️](../../parte-0-pensamiento-computacional-y-el-metodo-poliglota/009-complejidad-y-eficiencia-intuicion-de-coste/README.md)
