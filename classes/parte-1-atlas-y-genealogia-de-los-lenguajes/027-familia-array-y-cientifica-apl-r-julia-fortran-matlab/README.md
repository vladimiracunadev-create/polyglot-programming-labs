# Clase 027 — Familia array y científica: APL, R, Julia, Fortran, MATLAB

> Parte **1 — Atlas y genealogía de los lenguajes** · ⏱️ Duración estimada: **75 min** · Nivel: **Fundamentos**
> ✅ **Clase construida.**

---

## 🎯 Objetivo

Conocer los lenguajes hechos para el cálculo numérico y el trabajo intensivo con datos, y con ellos un estilo de pensamiento distinto: la **vectorización**, operar sobre arreglos completos de una sola vez en lugar de elemento a elemento con bucles. **Fortran** (1957) inauguró la computación científica y aún reina en el cálculo de alto rendimiento; **MATLAB** y **R** dominan la ingeniería y la estadística; **Julia** es la apuesta moderna que busca rendimiento de C con comodidad de Python; y **APL** llevó la idea de operar sobre arreglos hasta un extremo casi matemático. Ninguno está en el núcleo, pero su estilo define cómo se trabaja hoy con datos y con inteligencia artificial.

Esto importa porque la vectorización es el motor silencioso detrás de la revolución de los datos y el aprendizaje automático. Sebesta sitúa a Fortran como el primer lenguaje de alto nivel de la historia y el origen de la computación numérica; el estilo de arreglos que APL popularizó vive hoy en NumPy, en R, en Julia y en las bibliotecas de tensores que entrenan redes neuronales. Entender este linaje explica por qué "pensar en arreglos" y no "pensar en elementos" es la diferencia entre un programa lento y uno rápido cuando hay millones de números.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Explicar la vectorización: operar sobre arreglos completos sin bucles explícitos.
2. Situar Fortran, MATLAB, R y Julia según su dominio y su época.
3. Reconocer por qué este estilo importa para datos, ciencia e IA.
4. Entender qué aporta Julia (rendimiento + multiple dispatch) frente a Python.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Vectorización | Operar sobre todo un arreglo de una vez |
| 2 | Fortran: el pionero | Cálculo numérico desde 1957, aún en HPC |
| 3 | R y MATLAB | Estadística e ingeniería, orientados a matrices |
| 4 | Julia y APL | Lo moderno y lo radical del estilo array |
| 5 | Multiple dispatch | Elegir la operación según los tipos de todos los argumentos |

## 📖 Definiciones y características

La historia empieza donde empieza todo lenguaje de alto nivel: **Fortran** (FORmula TRANslator, John Backus, IBM, 1957). Nació para que los científicos e ingenieros escribieran fórmulas matemáticas sin bajar al ensamblador, y su compilador demostró que se podía abstraer sin perder velocidad. Siete décadas después, Fortran sigue siendo el rey de la **computación de alto rendimiento** (HPC): mucho del software de simulación de clima, física de partículas, dinámica de fluidos y álgebra lineal pesada corre sobre Fortran extremadamente optimizado, y bibliotecas fundamentales como BLAS y LAPACK, que sostienen el cálculo numérico de casi todos los demás lenguajes, tienen su raíz aquí. Que un lenguaje de 1957 siga siendo insustituible en su nicho dice mucho sobre lo bien que resolvió su problema.

El rasgo que unifica a esta familia es la **vectorización**, y su origen conceptual más puro es **APL** (A Programming Language, Kenneth Iverson, 1962). APL tomó la notación matemática de operar sobre vectores y matrices enteros y la convirtió en un lenguaje: en vez de escribir un bucle que sume los elementos de dos vectores uno a uno, escribes una sola operación que actúa sobre los arreglos completos. Esta idea —pensar en colecciones enteras como unidades, no en sus elementos— es tan potente que se propagó a toda la computación científica. **MATLAB** (Cleve Moler, años 80) la llevó a la ingeniería con matrices como ciudadano de primera clase y un entorno interactivo. **R** (Ross Ihaka y Robert Gentleman, 1993), descendiente del lenguaje S, la especializó en estadística y visualización, con un ecosistema gigantesco de paquetes de análisis. En todos ellos, escribir `c <- a + b` para sumar dos vectores no solo es más corto que un bucle: suele ser más rápido, porque la operación vectorizada se ejecuta en código nativo optimizado por debajo, aprovechando instrucciones SIMD del procesador.

**Julia** (2012, del MIT) es la respuesta moderna al viejo dilema de esta familia, conocido como "el problema de los dos lenguajes": los científicos prototipaban en un lenguaje cómodo pero lento (como Python o R) y luego reescribían las partes críticas en uno rápido (C o Fortran). Julia busca eliminar ese paso: es dinámico y cómodo como Python, pero compila a código nativo (vía LLVM) alcanzando rendimiento cercano a C. Su paradigma central es el **multiple dispatch**: qué implementación de una función se ejecuta se decide según los tipos de **todos** sus argumentos a la vez, no solo del primero (como en la orientación a objetos clásica). Esto encaja de maravilla con las matemáticas, donde `+` debe comportarse distinto para escalares, vectores y matrices en cualquier combinación. Van Roy y Haridi encuadran este estilo dentro del pensamiento declarativo: describes la operación sobre la estructura completa y dejas que el sistema la ejecute eficientemente.

- **Vectorización** — aplicar una operación a un arreglo entero sin escribir el bucle. Clave: código más corto y a menudo mucho más rápido.
- **Fortran** — 1957 (IBM, John Backus), primer lenguaje de alto nivel. Clave: sigue siendo rey del cálculo científico de alto rendimiento.
- **R** — 1993 (Ihaka y Gentleman), especializado en estadística y visualización. Clave: enorme ecosistema de análisis de datos.
- **Julia** — 2012, cálculo científico con rendimiento cercano a C. Clave: multiple dispatch como paradigma central; resuelve el "problema de los dos lenguajes".

## 🧩 Situación

Una analista escribe en Python un bucle que recorre un millón de números para calcular una media y una desviación: funciona, pero tarda varios segundos y consume CPU. Una colega le muestra la versión vectorizada con NumPy —una sola expresión que opera sobre todo el arreglo— y ahora tarda milisegundos. No cambió el algoritmo ni el lenguaje: cambió la **mentalidad**, de "recorrer elementos" a "operar sobre la colección completa". Ese giro, heredado de APL y de toda la familia científica, es una de las lecciones más rentables que un programador de datos puede interiorizar, y es la razón de que las bibliotecas de IA estén construidas enteras sobre operaciones de arreglos.

## 🔎 Ejemplo

Sumar dos vectores, con bucle imperativo frente a estilo vectorizado:

```text
Con bucle (imperativo):
  PARA i desde 0 hasta n-1:
      c[i] <- a[i] + b[i]

Vectorizado (estilo array; R, Julia, MATLAB, NumPy):
  c <- a + b        # una sola operación sobre todo el arreglo
```

El **delta** es doble. En expresividad, la versión vectorizada dice exactamente lo que quieres —"suma estos dos vectores"— sin el ruido del índice `i` ni los límites del bucle. En rendimiento, esa única operación se despacha a código nativo optimizado que puede usar instrucciones SIMD del procesador, mientras que el bucle en un lenguaje dinámico paga el coste del intérprete en cada iteración. Misma matemática, dos mundos de velocidad.

## ✍️ Práctica

Piensa cómo calcular el promedio de un millón de números "a la manera de bucle" (recorrer, acumular, dividir) y "a la manera vectorizada" (una operación sobre el arreglo completo). Escribe ambas en pseudocódigo y responde: ¿cuál expresa mejor la **intención**? ¿Cuál esperarías que fuera más rápida en un lenguaje como R o con NumPy, y por qué?

## ⚠️ Errores comunes

- **Escribir bucles donde cabe vectorizar** → causa: traer la mentalidad imperativa al trabajo con datos → solución: pensar en operaciones sobre arreglos completos, no sobre elementos.
- **Creer que estos lenguajes son "solo para matemáticos"** → causa: descartarlos por prejuicio → solución: reconocer que dominan datos, estadística, ciencia y buena parte de la IA.
- **Asumir que Julia es "Python más rápido" y ya** → causa: ignorar su paradigma → solución: entender que su multiple dispatch es un modelo distinto, no azúcar sintáctico.

## ❓ Preguntas frecuentes

- **¿Fortran sigue en uso de verdad?** Sí: gran parte del software de clima, física, ingeniería y las bibliotecas de álgebra lineal (BLAS/LAPACK) corren sobre Fortran altamente optimizado.
- **¿Julia sustituye a Python en datos?** Compite fuerte en rendimiento; Python gana en tamaño de ecosistema y comunidad. Conviven según el caso, y muchas veces se usan juntos.
- **¿Por qué APL casi no se usa hoy si fue tan influyente?** Su notación con símbolos especiales lo hizo difícil de escribir y leer; pero su idea de operar sobre arreglos triunfó incorporada en R, NumPy, MATLAB y Julia.

## 🔗 Referencias

- R. W. Sebesta — *Concepts of Programming Languages* (12ª ed., Pearson), cap. 2 (Fortran y APL).
- P. Van Roy y S. Haridi — *Concepts, Techniques, and Models of Computer Programming* (MIT Press).
- M. L. Scott — *Programming Language Pragmatics* (4ª ed., Morgan Kaufmann).
- B. A. Tate — *Seven Languages in Seven Weeks* (Pragmatic Bookshelf).

---

> [⏮️ Clase 026](../../parte-1-atlas-y-genealogia-de-los-lenguajes/026-familia-de-sistemas-c-c-plus-plus-rust-zig/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 028 ⏭️](../../parte-1-atlas-y-genealogia-de-los-lenguajes/028-lenguajes-historicos-y-de-nicho-cobol-fortran-pascal-basic-bash/README.md)
