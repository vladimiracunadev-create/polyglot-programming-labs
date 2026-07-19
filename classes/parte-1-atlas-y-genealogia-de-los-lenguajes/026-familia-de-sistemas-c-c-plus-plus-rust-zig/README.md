# Clase 026 — Familia de sistemas: C, C++, Rust, Zig

> Parte **1 — Atlas y genealogía de los lenguajes** · ⏱️ Duración estimada: **75 min** · Nivel: **Fundamentos**
> ✅ **Clase construida.**

---

## 🎯 Objetivo

Conocer los lenguajes hechos para escribir software cercano a la máquina: sistemas operativos, drivers, motores de bases de datos, navegadores, runtimes y sistemas embebidos. **C**, **C++** y **Rust** están en el núcleo del curso o son primos directos; **Zig** es el recién llegado. Lo que los agrupa no es la sintaxis (aunque la comparten) sino un requisito: **control fino de la memoria** y rendimiento predecible, sin un recolector de basura que pause el programa en momentos impredecibles.

Esto importa porque estos lenguajes sostienen todo lo demás. El intérprete de Python está escrito en C; el motor V8 que ejecuta tu JavaScript, en C++; muchos componentes de sistemas modernos, en Rust. Y también importa por un dato demoledor que Sebesta y la industria repiten: alrededor del 70% de las vulnerabilidades graves de seguridad en software de sistemas son errores de gestión de memoria en C y C++. La historia reciente de esta familia es, en buena medida, la historia del intento de conservar el rendimiento de C eliminando su peligrosidad.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Explicar qué distingue a un lenguaje de sistemas (control de memoria, sin GC obligatorio).
2. Comparar cómo cada uno gestiona la seguridad de memoria.
3. Situar Rust y Zig como respuestas modernas a los peligros de C.
4. Entender por qué las comprobaciones de Rust no cuestan rendimiento en ejecución.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Qué es un lenguaje de sistemas | Control de memoria y rendimiento predecible |
| 2 | C y C++: potencia sin red | Máximo control, máxima responsabilidad |
| 3 | Rust: seguridad sin GC | Propiedad y préstamos comprobados al compilar |
| 4 | Zig: C moderno | Simplicidad, comptime, sin GC ni sorpresas |
| 5 | Seguridad de memoria | El eje que separa a la vieja escuela de la nueva |

## 📖 Definiciones y características

Un **lenguaje de sistemas** se define por lo que permite y por lo que se niega a imponer. Permite manipular la memoria directamente, controlar su disposición (layout), acercarse al hardware. Y se niega a imponer un **recolector de basura** obligatorio, porque el GC introduce pausas impredecibles —momentos en que el programa se detiene a limpiar memoria— que son inaceptables en un driver de red, en un sistema de tiempo real o en el bucle de un motor de juego. A cambio de ese control, el programador asume la responsabilidad de gestionar la memoria correctamente, y ahí está el peligro. **C** (1972) y **C++** (1985) representan la vieja escuela: control total mediante `malloc`/`free` en C, o mediante **RAII** en C++ (los destructores liberan recursos automáticamente al salir de ámbito, una mejora enorme pero que no elimina todos los fallos). Ambos ofrecen máximo poder y ninguna protección contra los errores clásicos: usar memoria ya liberada (*use-after-free*), leer o escribir fuera de los límites de un buffer, o desreferenciar un puntero nulo.

**Rust** (Graydon Hoare, Mozilla; primer diseño hacia 2010, versión 1.0 en 2015) fue creado precisamente para romper el falso dilema "o rendimiento o seguridad". Su innovación central es el sistema de **propiedad y préstamos** (*ownership and borrowing*), verificado por el compilador. La regla es simple en su enunciado: cada valor tiene un único dueño; cuando el dueño sale de ámbito, el valor se libera; y se pueden tomar prestadas referencias, pero o bien muchas de solo lectura, o bien una sola de escritura, nunca ambas a la vez. El componente que impone estas reglas, el **borrow checker**, rechaza en tiempo de compilación cualquier programa que pudiera provocar un use-after-free o una carrera de datos. Lo crucial —y lo que suele malentenderse— es que estas comprobaciones ocurren **al compilar**, no al ejecutar: el binario resultante no lleva ningún recolector de basura ni verificación en tiempo de ejecución, y por eso Rust iguala el rendimiento de C sin su inseguridad. Como vimos en la clase 022, Rust toma este esqueleto de tipos de la familia ML mientras conserva la piel y la cercanía a la máquina de C.

**Zig** (Andrew Kelley, 2016) toma un camino distinto y más humilde. En lugar de un borrow checker sofisticado, apuesta por la simplicidad y la transparencia: no oculta nada, no hay asignaciones de memoria escondidas, y quien reserva memoria pasa explícitamente un **asignador** (*allocator*), de modo que siempre es visible dónde y cómo se gestiona. Su rasgo estrella es `comptime`: la capacidad de ejecutar código Zig arbitrario en tiempo de compilación, lo que reemplaza a los macros y las plantillas con el propio lenguaje. Zig se presenta como "un C moderno": tan cercano a la máquina como C, sin GC, pero con herramientas que hacen los errores más difíciles y el código más explícito. Entre C, C++, Rust y Zig se despliega todo el espectro de cómo un lenguaje puede combinar control y seguridad.

- **Lenguaje de sistemas** — diseñado para software cercano al hardware, con control de memoria y sin GC obligatorio. Clave: rendimiento predecible.
- **Rust** — 2010/2015 (Mozilla, Graydon Hoare), seguridad de memoria sin GC vía propiedad. Clave: núcleo del curso; elimina clases enteras de bugs al compilar.
- **Zig** — 2016 (Andrew Kelley), alternativa moderna y minimalista a C. Clave: `comptime`, asignadores explícitos, sin GC.
- **Seguridad de memoria** — garantía de no acceder a memoria inválida (use-after-free, desbordamientos). Clave: C no la da; Rust la impone al compilar.

## 🧩 Situación

Un equipo mantiene un componente de red escrito en C que sufre, cada pocos meses, un fallo esporádico e irreproducible: a veces se cae, a veces devuelve datos corruptos. Tras semanas de depuración descubren la causa: un puntero que, bajo cierta secuencia de eventos, se usa después de liberarse. Es el bug más costoso de esta familia porque no salta al escribirlo ni en las pruebas normales; se esconde. Cuando reescriben el componente en Rust, el borrow checker rechaza esa misma construcción *antes* de compilar: el error que en C tardó semanas en manifestarse, en Rust es imposible de introducir. Ese es, en una anécdota, el motivo por el que Rust existe.

## 🔎 Ejemplo

Cómo gestiona la memoria cada miembro de la familia:

```text
C:     char* p = malloc(n);  ...  free(p);   → manual: potente y propenso a errores
C++:   std::vector<char> v(n);              → RAII: se libera solo al salir de ámbito
Rust:  let v = vec![0u8; n];                → propiedad: el compilador garantiza su liberación
Zig:   const p = try alloc.alloc(u8, n);    → asignador explícito: visible y deliberado
       defer alloc.free(p);
```

El **delta** es *quién* garantiza que la memoria se libera una sola vez y no se usa tras liberarse. En C, nadie: es tu responsabilidad y el compilador no ayuda. En C++, el destructor de `vector` lo hace al salir de ámbito, pero puedes sortearlo con punteros crudos. En Rust, el sistema de propiedad lo garantiza en tiempo de compilación y rechaza el código que lo violaría. En Zig, sigue siendo manual, pero el asignador es explícito y `defer` hace la liberación difícil de olvidar. Cuatro puntos en el espectro control–seguridad.

## ✍️ Práctica

Busca en la implementación en C de la clase 041 (o en cualquier programa en C) dónde se reserva memoria y dónde se libera, o dónde podría hacer falta. Pregúntate: ¿qué pasaría si se liberara dos veces, o si se usara después de liberar? Luego escribe en una frase qué garantiza el compilador de Rust que el de C no, y en qué momento (compilación vs. ejecución) lo garantiza.

## ⚠️ Errores comunes

- **Creer que "sistemas" significa "difícil e innecesario"** → causa: evitar entender la memoria → solución: reconocer que estos lenguajes sostienen todo el resto del software.
- **Pensar que Rust es "C más lento por seguro"** → causa: asumir que la seguridad cuesta rendimiento → solución: notar que sus comprobaciones son en tiempo de compilación, no de ejecución; el binario no las lleva.
- **Confiar en que "compila, luego es correcto" en C** → causa: creer que el compilador atrapa los errores de memoria → solución: usar herramientas (sanitizers, análisis estático) porque C no los detecta por sí solo.

## ❓ Preguntas frecuentes

- **¿Rust reemplazará a C?** En proyectos nuevos gana terreno con rapidez, pero C está en tantos cimientos (kernels, drivers, runtimes) que ambos convivirán durante décadas.
- **¿Por qué estos lenguajes evitan el recolector de basura?** Porque el GC introduce pausas impredecibles, inaceptables en drivers, sistemas de tiempo real o bucles de latencia crítica.
- **¿Cuándo elegir Zig en vez de Rust?** Cuando se prioriza la simplicidad, la interoperabilidad directa con C y el control manual explícito, aceptando menos garantías automáticas que las del borrow checker.

## 🔗 Referencias

- S. Klabnik y C. Nichols — *The Rust Programming Language* — [gratis online](https://doc.rust-lang.org/book/) (cap. de propiedad y préstamos).
- B. Kernighan y D. Ritchie — *The C Programming Language* (2ª ed., Prentice Hall).
- R. W. Sebesta — *Concepts of Programming Languages* (12ª ed., Pearson), cap. 6 (tipos de datos) y cap. 2.
- M. L. Scott — *Programming Language Pragmatics* (4ª ed., Morgan Kaufmann), cap. 8 (gestión de memoria).

---

> [⏮️ Clase 025](../../parte-1-atlas-y-genealogia-de-los-lenguajes/025-familia-concurrente-actor-erlang-elixir-y-el-csp-de-go/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 027 ⏭️](../../parte-1-atlas-y-genealogia-de-los-lenguajes/027-familia-array-y-cientifica-apl-r-julia-fortran-matlab/README.md)
