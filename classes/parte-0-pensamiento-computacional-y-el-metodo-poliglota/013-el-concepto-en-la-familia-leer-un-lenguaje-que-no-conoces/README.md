# Clase 013 — El concepto en la familia: leer un lenguaje que no conoces

> Parte **0 — Pensamiento computacional y el método políglota** · ⏱️ Duración estimada: **75 min** · Nivel: **Fundamentos**
> ✅ **Clase construida.**

---

## 🎯 Objetivo

Adquirir la habilidad central del enfoque políglota: poder **leer** código de un lenguaje que nunca estudiaste, apoyándote en la familia a la que pertenece. Si sabes C, ya reconoces el 80% de Java, C#, JS, Go y PHP.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Ubicar un lenguaje desconocido en su familia a partir de su aspecto.
2. Leer y explicar un fragmento de un lenguaje no estudiado usando su parecido con uno conocido.
3. Distinguir qué parte es familiar y qué parte exige atención (la diferencia semántica).

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Familias y parecidos | Lenguajes primos comparten sintaxis y modelo |
| 2 | Leer por analogía | Mapear lo nuevo a lo conocido |
| 3 | Dónde poner atención | Las diferencias semánticas, no las cosméticas |

## 📖 Definiciones y características

- **Familia de lenguajes** — grupo con antepasado y rasgos comunes (sintaxis, paradigma). Clave: conocer una abre la puerta a las demás.
- **Lectura por analogía** — entender lo nuevo mapeándolo a lo que ya sabes. Clave: acelera enormemente el aprendizaje.
- **Delta** — lo que cambia respecto del representante de la familia. Clave: es lo único que hay que aprender de nuevo.

## 🧩 Situación

Te toca revisar un pull request en Kotlin y nunca lo escribiste. En vez de bloquearte, reconoces que es familia JVM (como Java): `val` es una constante, `fun` una función, la inferencia se parece a Rust. Lees el 90% sin estudiarlo.

## 🔎 Ejemplo

Leer Kotlin sabiendo Java (misma familia JVM):

```text
Kotlin:  val precio = 15000.0        // 'val' = final (constante)
         fun total(c: Int) = ...     // 'fun' = método
Java:    final double precio = 15000.0;
         double total(int c) { ... }
```

El delta: `val`/`fun` e inferencia. Todo lo demás ya lo sabías.

## ✍️ Práctica

Mira la sección '🧬 El concepto en la familia' de la clase 041. Elige un primo (Ruby, Kotlin o Haskell) y explica su línea apoyándote en un lenguaje del núcleo.

## ⚠️ Errores comunes

- **Asumir que 'no sé este lenguaje' = 'no puedo leerlo'** → causa: ignorar el parecido de familia → solución: identificar la familia y leer por analogía
- **Confiar en la analogía sin verificar el delta** → causa: pasar por alto una diferencia semántica → solución: marcar explícitamente qué cambia respecto del representante

## ❓ Preguntas frecuentes

- **¿Esto reemplaza estudiar el lenguaje?** No para escribirlo bien, pero sí para leerlo y entenderlo, que es el 90% del trabajo real.
- **¿Dónde veo las familias?** En el [Atlas](../../../atlas/README.md) y en la Parte 1 del programa.

## 🔗 Referencias

- G. Polya — *How to Solve It* (Princeton University Press).
- H. Abelson y G. J. Sussman — *Structure and Interpretation of Computer Programs* (2ª ed., MIT Press) — [gratis online](https://mitpress.mit.edu/9780262510875/).
- A. Hunt y D. Thomas — *The Pragmatic Programmer* (2ª ed., Addison-Wesley).
- T. Cormen, C. Leiserson, R. Rivest y C. Stein — *Introduction to Algorithms* (4ª ed., MIT Press).

---

> [⏮️ Clase 012](../../parte-0-pensamiento-computacional-y-el-metodo-poliglota/012-casos-json-y-el-verificador-de-equivalencia/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 014 ⏭️](../../parte-0-pensamiento-computacional-y-el-metodo-poliglota/014-como-elegir-lenguaje-para-un-problema/README.md)
