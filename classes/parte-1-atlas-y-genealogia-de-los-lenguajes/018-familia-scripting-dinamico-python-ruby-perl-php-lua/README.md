# Clase 018 — Familia scripting dinámico: Python, Ruby, Perl, PHP, Lua

> Parte **1 — Atlas y genealogía de los lenguajes** · ⏱️ Duración estimada: **75 min** · Nivel: **Fundamentos**
> ✅ **Clase construida.**

---

## 🎯 Objetivo

Conocer la familia de los lenguajes dinámicos: sin declarar tipos, interpretados, pensados para escribir rápido. Python y PHP están en el núcleo; Ruby, Perl y Lua son sus primos. Comparten la filosofía 'el programador antes que la máquina', con distintos acentos.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Explicar qué comparte esta familia (tipado dinámico, interpretado, expresividad).
2. Distinguir el acento de cada uno (claridad, felicidad del dev, texto, web, embebido).
3. Reconocer código de un primo apoyándote en Python o PHP.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Rasgos comunes | Tipado dinámico, interpretado, poca ceremonia |
| 2 | Python y PHP | Los representantes del núcleo: claridad y web |
| 3 | Ruby, Perl, Lua | Felicidad del dev, procesamiento de texto, embebido |
| 4 | Cuándo brillan | Prototipos, scripting, web, automatización |

## 📖 Definiciones y características

- **Python** — 1991 (Guido van Rossum), prioriza la legibilidad. Clave: núcleo del curso; el más usado para enseñar y para datos.
- **Ruby** — 1995 (Matz), diseñado para la felicidad del programador. Clave: bloques y metaprogramación; base de Rails.
- **Perl** — 1987 (Larry Wall), rey del procesamiento de texto y las expresiones regulares. Clave: 'hay más de una forma de hacerlo'.
- **Lua** — 1993 (PUC-Rio), minimalista y embebible. Clave: tablas como única estructura; scripting en juegos y sistemas embebidos.

## 🧩 Situación

Un equipo necesita un script para renombrar 10.000 archivos. Nadie propone C: se hace en Python en 10 líneas. Esa inmediatez es la razón de ser de toda la familia dinámica.

## 🔎 Ejemplo

'Hola, X' revela el aire de familia (todos dinámicos, sin declarar tipos):

```text
Python:  nombre = "Ada"; print(f"Hola, {nombre}")
Ruby:    nombre = "Ada"; puts "Hola, #{nombre}"
PHP:     $nombre = "Ada"; echo "Hola, $nombre";
Lua:     nombre = "Ada"; print("Hola, " .. nombre)
```

## ✍️ Práctica

Compara la interpolación de cadenas en Python (`f"{x}"`), Ruby (`#{x}`) y PHP (`$x`). ¿De qué clase es la diferencia entre ellas?

## ⚠️ Errores comunes

- **Creer que 'dinámico' significa 'sin reglas'** → causa: confundir tipado dinámico con débil → solución: recordar que Python es dinámico pero fuerte: no suma texto y número sin más
- **Usar la familia para todo** → causa: ignorar su coste en rendimiento → solución: reservarla para scripting/prototipos, no para núcleos críticos

## ❓ Preguntas frecuentes

- **¿Python es lento?** Comparado con C/Rust, sí; pero para la mayoría de tareas su velocidad de desarrollo compensa.
- **¿Por qué PHP tiene mala fama?** Por su historia caótica; las versiones modernas (8.x) son un lenguaje sólido y tipado opcionalmente.

## 🔗 Referencias

- R. W. Sebesta — *Concepts of Programming Languages* (12ª ed., Pearson).
- M. L. Scott — *Programming Language Pragmatics* (4ª ed., Morgan Kaufmann).
- B. A. Tate — *Seven Languages in Seven Weeks* (Pragmatic Bookshelf).
- P. Van Roy y S. Haridi — *Concepts, Techniques, and Models of Computer Programming* (MIT Press).

---

> [⏮️ Clase 017](../../parte-1-atlas-y-genealogia-de-los-lenguajes/017-familia-c-y-de-las-llaves-c-c-plus-plus-objective-c/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 019 ⏭️](../../parte-1-atlas-y-genealogia-de-los-lenguajes/019-familia-jvm-java-kotlin-scala-groovy-clojure/README.md)
