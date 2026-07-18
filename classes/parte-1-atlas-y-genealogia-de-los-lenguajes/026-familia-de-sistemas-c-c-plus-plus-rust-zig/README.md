# Clase 026 — Familia de sistemas: C, C++, Rust, Zig

> Parte **1 — Atlas y genealogía de los lenguajes** · ⏱️ Duración estimada: **75 min** · Nivel: **Fundamentos**
> ✅ **Clase construida.**

---

## 🎯 Objetivo

Conocer los lenguajes para escribir software cercano a la máquina: sistemas operativos, drivers, motores y runtimes. C, C++ y Rust están en el núcleo o son primos directos; Zig es el recién llegado. Comparten el control de la memoria y la ausencia (o control) de recolector de basura.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Explicar qué distingue a un lenguaje de sistemas (control de memoria, sin GC obligatorio).
2. Comparar cómo cada uno gestiona la seguridad de memoria.
3. Situar a Rust y Zig como respuestas modernas a los peligros de C.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Qué es un lenguaje de sistemas | Control fino de memoria y rendimiento predecible |
| 2 | C y C++: potencia sin red | Máximo control, máxima responsabilidad |
| 3 | Rust: seguridad sin GC | Propiedad y préstamos comprobados al compilar |
| 4 | Zig: C moderno | Simplicidad, comptime, sin GC |

## 📖 Definiciones y características

- **Lenguaje de sistemas** — diseñado para software cercano al hardware, con control de memoria y sin GC obligatorio. Clave: rendimiento predecible.
- **Rust** — 2010/2015 (Mozilla, Graydon Hoare), seguridad de memoria sin GC vía propiedad. Clave: núcleo del curso; evita clases enteras de bugs.
- **Zig** — 2016 (Andrew Kelley), alternativa moderna y minimalista a C. Clave: `comptime`, sin GC, gestión manual explícita.
- **Seguridad de memoria** — garantía de no acceder a memoria inválida (use-after-free, desbordamientos). Clave: C no la da; Rust sí, al compilar.

## 🧩 Situación

El 70% de las vulnerabilidades graves en software de sistemas son errores de memoria de C/C++. Rust nació para eliminarlos de raíz: el compilador rechaza el código inseguro antes de ejecutarlo, sin coste en tiempo de ejecución.

## 🔎 Ejemplo

Cómo cada familia gestiona la memoria:

```text
C:     malloc/free manuales        → potente, propenso a errores
C++:   RAII (destructores)         → automático dentro de su ámbito
Rust:  propiedad + préstamos       → comprobado por el compilador
Zig:   asignadores explícitos      → manual pero visible y seguro-por-defecto
```

## ✍️ Práctica

Busca en la implementación en C de la clase 041 dónde se reserva y libera memoria (o dónde podría hacer falta). ¿Qué garantiza Rust que C no?

## ⚠️ Errores comunes

- **Creer que 'sistemas' = 'difícil e innecesario'** → causa: evitar entender la memoria → solución: reconocer que estos lenguajes sostienen todo lo demás
- **Pensar que Rust es 'C más lento'** → causa: asumir que la seguridad cuesta rendimiento → solución: notar que sus comprobaciones son en tiempo de compilación, no de ejecución

## ❓ Preguntas frecuentes

- **¿Rust reemplazará a C?** En proyectos nuevos gana terreno, pero C está en tantos cimientos que convivirán décadas.
- **¿Por qué sin recolector de basura?** El GC introduce pausas impredecibles, inaceptables en drivers o sistemas de tiempo real.

## 🔗 Referencias

- Documentación de referencia de cada lenguaje del núcleo.

---

> [⏮️ Clase 025](../../parte-1-atlas-y-genealogia-de-los-lenguajes/025-familia-concurrente-actor-erlang-elixir-y-el-csp-de-go/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 027 ⏭️](../../parte-1-atlas-y-genealogia-de-los-lenguajes/027-familia-array-y-cientifica-apl-r-julia-fortran-matlab/README.md)
