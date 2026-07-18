# Clase 016 — Cómo nace y evoluciona un lenguaje: estándares, versiones y ecosistemas

> Parte **1 — Atlas y genealogía de los lenguajes** · ⏱️ Duración estimada: **75 min** · Nivel: **Fundamentos**
> ✅ **Clase construida.**

---

## 🎯 Objetivo

Entender que un lenguaje no es estático: nace por una necesidad, se estandariza, publica versiones y crece con un ecosistema (librerías, herramientas, comunidad). Saber leer 'C11', 'ES2023' o 'Python 3.12' te dice qué features puedes usar y qué compatibilidad esperar.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Distinguir el lenguaje (estándar) de su implementación (compilador/intérprete).
2. Interpretar una versión y saber qué implica para la compatibilidad.
3. Explicar el papel del ecosistema y la gobernanza (PEP, JEP, ECMA, RFC).

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Estándar vs. implementación | El lenguaje se especifica; varios compiladores lo implementan |
| 2 | Versionado | Mayor/menor indica compatibilidad y features nuevas |
| 3 | Gobernanza | Quién decide los cambios (comités, fundaciones, empresas) |
| 4 | Ecosistema | Librerías y herramientas que hacen útil al lenguaje |

## 📖 Definiciones y características

- **Estándar** — documento que define el lenguaje (ISO C, ECMAScript). Clave: separa la idea de sus implementaciones.
- **Implementación** — compilador o intérprete concreto (GCC, CPython, V8). Clave: puede haber varias del mismo estándar.
- **Proceso de evolución** — mecanismo formal de cambios (PEP en Python, JEP en Java, TC39 en JS). Clave: el lenguaje cambia con reglas, no al azar.
- **Ecosistema** — conjunto de librerías, gestores de paquetes y comunidad. Clave: a menudo decide la elección más que el lenguaje.

## 🧩 Situación

Copias un ejemplo de internet y no compila: usa una feature de C++20 y tu compilador aún es C++17. El problema no es tu código: es la versión. Saber esto ahorra horas.

## 🔎 Ejemplo

Cómo se nombran y gobiernan algunos lenguajes:

```text
Lenguaje    Estándar/versión   Gobernanza         Implementación
--------    ----------------   ----------------   --------------
C           ISO C23            comité ISO/WG14    GCC, Clang
JavaScript  ECMAScript 2023    TC39 (Ecma)        V8, SpiderMonkey
Python      3.12 (PEP)         Steering Council   CPython, PyPy
Java        JDK 21 (JEP)       OpenJDK / Oracle   HotSpot, GraalVM
Rust        edición 2021       RFC / Rust team    rustc
```

## ✍️ Práctica

Averigua la última versión estable de dos lenguajes del núcleo y una feature que introdujeron. ¿Cómo se propuso ese cambio (PEP, JEP, RFC…)?

## ⚠️ Errores comunes

- **Confundir el lenguaje con su compilador** → causa: creer que 'C = GCC' → solución: recordar que un estándar tiene varias implementaciones
- **Ignorar la versión al copiar código** → causa: asumir que todo el código de un lenguaje es intercambiable → solución: verificar la versión mínima que exige un ejemplo

## ❓ Preguntas frecuentes

- **¿Por qué hay varias implementaciones?** Distintos objetivos: rendimiento, portabilidad, tamaño. Todas siguen el mismo estándar.
- **¿'Edición' de Rust es una versión?** Es un mecanismo de compatibilidad: permite cambios sin romper código viejo.

## 🔗 Referencias

- Documentación de referencia de cada lenguaje del núcleo.

---

> [⏮️ Clase 015](../../parte-1-atlas-y-genealogia-de-los-lenguajes/015-el-arbol-genealogico-de-los-lenguajes-mapa-general/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 017 ⏭️](../../parte-1-atlas-y-genealogia-de-los-lenguajes/017-familia-c-y-de-las-llaves-c-c-plus-plus-objective-c/README.md)
