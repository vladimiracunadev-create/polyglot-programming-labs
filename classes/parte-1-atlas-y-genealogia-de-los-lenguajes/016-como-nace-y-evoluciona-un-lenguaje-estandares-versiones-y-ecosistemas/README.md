# Clase 016 — Cómo nace y evoluciona un lenguaje: estándares, versiones y ecosistemas

> Parte **1 — Atlas y genealogía de los lenguajes** · ⏱️ Duración estimada: **75 min** · Nivel: **Fundamentos**
> ✅ **Clase construida.**

---

## 🎯 Objetivo

Entender que un lenguaje de programación no es un objeto fijo sino un proceso vivo: nace de una necesidad concreta, se formaliza en un **estándar**, se materializa en una o varias **implementaciones**, publica **versiones** con reglas de compatibilidad y crece —o muere— según su **ecosistema** de librerías, herramientas y comunidad. Saber leer una etiqueta como `C23`, `ES2023` o `Python 3.12` no es un detalle burocrático: te dice qué características puedes usar, qué compatibilidad esperar y por qué un ejemplo de internet compila en la máquina de otro pero no en la tuya.

Esto importa porque la mayoría de la frustración temprana del programador nace de confundir estas capas. Scott, en *Programming Language Pragmatics*, dedica su primer capítulo a separar cuidadosamente el **lenguaje** (una especificación abstracta) de su **implementación** (un compilador o intérprete concreto), y advierte que tratar ambos como lo mismo lleva a errores de diagnóstico que cuestan horas. Comprender el ciclo de vida de un lenguaje es lo que convierte "no compila y no sé por qué" en "esta feature es de C++20 y mi compilador es C++17".

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Distinguir el lenguaje (estándar) de su implementación (compilador/intérprete).
2. Interpretar un número de versión y deducir qué implica para la compatibilidad.
3. Explicar el papel de la gobernanza (PEP, JEP, TC39/ECMA, RFC, ISO).
4. Argumentar por qué el ecosistema decide, a menudo, más que el lenguaje en sí.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Estándar vs. implementación | El lenguaje se especifica; varios programas lo implementan |
| 2 | Versionado y compatibilidad | Mayor/menor indica qué código sigue funcionando |
| 3 | Gobernanza | Quién decide los cambios y con qué proceso |
| 4 | Ecosistema | Librerías y herramientas que hacen útil al lenguaje |
| 5 | Editions y feature flags | Evolucionar sin romper el código existente |

## 📖 Definiciones y características

Un **estándar** es un documento que define, con precisión, qué es válido en un lenguaje y qué significa cada construcción. C está definido por la norma ISO/IEC 9899 (de ahí C89, C99, C11, C17, C23); JavaScript por ECMAScript, publicado por Ecma International; C# tiene una norma ECMA e ISO. Ese documento es abstracto: no ejecuta nada. Quien ejecuta es la **implementación** —GCC y Clang para C, V8 y SpiderMonkey para JavaScript, CPython y PyPy para Python—. Scott subraya que puede haber muchas implementaciones del mismo estándar, cada una con objetivos distintos (velocidad, portabilidad, tamaño, tiempo de arranque), y que las diferencias entre ellas, dentro de lo que el estándar deja "sin especificar", son una fuente clásica de bugs no portables.

No todos los lenguajes tienen un estándar externo. Python no se define por una norma ISO sino por su implementación de referencia, CPython, y por los **PEP** (Python Enhancement Proposals), documentos donde se discute y aprueba cada cambio. Java usa **JEP** (JDK Enhancement Proposals) bajo el paraguas de OpenJDK; JavaScript evoluciona en el comité **TC39**, que publica una edición anual (ES2015, ES2020, ES2023); Rust usa **RFC** públicas gestionadas por sus equipos. Este es el aspecto de **gobernanza**: quién tiene autoridad para cambiar el lenguaje y con qué proceso. La lección es que un lenguaje maduro no cambia al azar ni por capricho de una persona, sino a través de un mecanismo formal, deliberado y normalmente público.

El **versionado** codifica la promesa de compatibilidad. Muchos lenguajes siguen la idea del versionado semántico: un salto de versión mayor puede romper código antiguo, uno menor añade cosas sin romper. Pero cada comunidad tiene su matiz. El caso más doloroso de la historia reciente fue la transición de **Python 2 a Python 3** (2008), deliberadamente incompatible, que fragmentó el ecosistema durante más de una década. Escarmentados de rupturas así, lenguajes modernos inventaron mecanismos para evolucionar sin romper: Rust usa **editions** (2015, 2018, 2021, 2024), donde cada crate declara la suya y el compilador respeta la sintaxis correspondiente aunque el proyecto vecino use otra. Finalmente, el **ecosistema** —npm, PyPI, Maven, crates.io, Composer— es a menudo el factor decisivo de adopción: Van Roy y Haridi recuerdan que un lenguaje se elige tanto por sus ideas como por el trabajo que ya han hecho otros y que puedes reutilizar.

- **Estándar** — documento que define el lenguaje (ISO C, ECMAScript). Clave: separa la idea de sus implementaciones.
- **Implementación** — compilador o intérprete concreto (GCC, CPython, V8). Clave: varias pueden cumplir el mismo estándar con objetivos distintos.
- **Gobernanza** — mecanismo formal de cambios (PEP, JEP, TC39, RFC). Clave: el lenguaje evoluciona con reglas, no al azar.
- **Edition / versión** — etiqueta que fija qué características y qué compatibilidad esperar. Clave: leerla evita el 90% de los "no compila en mi máquina".

## 🧩 Situación

Copias un ejemplo elegante de Stack Overflow que usa `std::format` y tu compilador lo rechaza con un error críptico. No es que tu código esté mal: `std::format` llegó en C++20 y tu proyecto compila en modo C++17. Cambias un flag (`-std=c++20`) y funciona. La misma escena se repite con async/await que no existe en un Node antiguo, con f-strings que fallan en Python 3.5, o con un `record` que tu JDK 11 no entiende. En cada caso, la etiqueta de versión contenía la respuesta desde el principio; solo había que saber leerla.

## 🔎 Ejemplo

Cómo se nombran, gobiernan e implementan algunos lenguajes del núcleo:

```text
Lenguaje    Estándar / versión   Gobernanza          Implementación
--------    ------------------   -----------------   ----------------
C           ISO C23              comité ISO/WG14     GCC, Clang, MSVC
JavaScript  ECMAScript 2023      TC39 (Ecma Intl.)   V8, SpiderMonkey
Python      3.12 (vía PEP)       Steering Council    CPython, PyPy
Java        JDK 21 (vía JEP)     OpenJDK / Oracle    HotSpot, GraalVM
Rust        edición 2021         RFC / Rust teams    rustc (LLVM)
```

Lee la tabla como tres columnas independientes. La misma idea (el lenguaje) puede tener varias implementaciones; el proceso de gobernanza dice quién decide los cambios; y la versión te dice desde qué punto puedes contar con una característica. Un desarrollador experimentado consulta las tres antes de copiar código ajeno.

## ✍️ Práctica

Elige dos lenguajes del núcleo. Para cada uno, averigua su última versión estable, una característica que introdujo recientemente y cómo se propuso ese cambio (¿un PEP? ¿un JEP? ¿una propuesta TC39? ¿una RFC?). Escribe en una línea qué versión mínima exige esa característica: acabas de hacer, en pequeño, el análisis de compatibilidad que se hace en cualquier proyecto real.

## ⚠️ Errores comunes

- **Confundir el lenguaje con su compilador** → causa: creer que "C = GCC" → solución: recordar que un estándar admite varias implementaciones y que un bug puede estar en una sola.
- **Ignorar la versión al copiar código** → causa: asumir que todo el código de un lenguaje es intercambiable → solución: verificar la versión mínima que exige el ejemplo antes de pegarlo.
- **Fijar dependencias a "la última" sin control** → causa: dar por hecho que menor = seguro → solución: fijar versiones (lockfiles) y leer las notas de cambios antes de subir de mayor.

## ❓ Preguntas frecuentes

- **¿Por qué hay varias implementaciones del mismo lenguaje?** Porque persiguen objetivos distintos: máxima velocidad, portabilidad, arranque rápido o tamaño reducido. Todas se ajustan al mismo estándar.
- **¿Una "edition" de Rust es una versión del lenguaje?** No exactamente: es un mecanismo de compatibilidad que permite introducir cambios de sintaxis sin romper el código escrito para editions anteriores.
- **¿Qué lección dejó Python 2 → 3?** Que una ruptura incompatible, aun por buenas razones, puede costar más de una década de fragmentación; por eso los lenguajes modernos evitan romper y prefieren feature flags o editions.

## 🔗 Referencias

- M. L. Scott — *Programming Language Pragmatics* (4ª ed., Morgan Kaufmann), cap. 1 "Introduction" (lenguaje vs. implementación).
- R. W. Sebesta — *Concepts of Programming Languages* (12ª ed., Pearson), cap. 1 "Preliminaries" y cap. 2.
- B. A. Tate — *Seven Languages in Seven Weeks* (Pragmatic Bookshelf).
- P. Van Roy y S. Haridi — *Concepts, Techniques, and Models of Computer Programming* (MIT Press).

---

> [⏮️ Clase 015](../../parte-1-atlas-y-genealogia-de-los-lenguajes/015-el-arbol-genealogico-de-los-lenguajes-mapa-general/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 017 ⏭️](../../parte-1-atlas-y-genealogia-de-los-lenguajes/017-familia-c-y-de-las-llaves-c-c-plus-plus-objective-c/README.md)
