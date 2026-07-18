# Clase 030 — Compilado vs. interpretado vs. transpilado vs. bytecode/VM

> Parte **2 — Herramientas, toolchains y anatomía de comandos** · ⏱️ Duración estimada: **75 min** · Nivel: **Fundamentos**
> ✅ **Clase construida.**

---

## 🎯 Objetivo

Clasificar cómo un lenguaje llega a ejecutarse: compilado a código máquina (C, Rust, Go), interpretado línea a línea (Python, PHP), transpilado a otro lenguaje (TypeScript → JavaScript) o compilado a bytecode para una máquina virtual (Java → JVM, C# → CLR). Esta clasificación explica el rendimiento, el arranque y los mensajes de error.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Clasificar cada lenguaje del núcleo por su modelo de ejecución.
2. Relacionar el modelo con el rendimiento y el momento en que aparecen los errores.
3. Explicar qué es una máquina virtual y qué es transpilar.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Compilado a máquina | Rápido, errores en compilación (C, Rust, Go) |
| 2 | Interpretado | Flexible, errores en ejecución (Python, PHP) |
| 3 | Bytecode + VM | Portable, con calentamiento (Java, C#) |
| 4 | Transpilado | De un lenguaje a otro (TS → JS) |

## 📖 Definiciones y características

- **Compilación a código máquina** — traducción directa a instrucciones de la CPU. Clave: máximo rendimiento; errores antes de ejecutar.
- **Interpretación** — ejecución del código fuente sin traducirlo por adelantado. Clave: rápido de iterar; errores al llegar a la línea.
- **Bytecode** — código intermedio que ejecuta una máquina virtual (JVM, CLR). Clave: portabilidad entre sistemas operativos.
- **Transpilación** — compilar de un lenguaje de alto nivel a otro (TypeScript a JavaScript). Clave: aprovechar un runtime existente.

## 🧩 Situación

Un error tipográfico en un nombre de variable: en C, el compilador lo detiene antes de correr; en Python, el programa arranca y falla justo al llegar a esa línea. El modelo de ejecución decide cuándo te enteras del error.

## 🔎 Ejemplo

Clasificación del núcleo:

```text
Modelo               Lenguajes del núcleo
-------------------  ---------------------------
Compilado a máquina  C, Rust, Go
Interpretado         Python, PHP, JavaScript*
Bytecode + VM        Java (JVM), C# (CLR)
Transpilado          TypeScript (→ JavaScript)
Declarativo/motor    SQL (lo ejecuta el motor de BD)
```

*JavaScript usa un JIT: interpreta y compila sobre la marcha.

## ✍️ Práctica

Clasifica cada lenguaje que conozcas en una de las categorías. ¿Alguno encaja en más de una? (Pista: JavaScript y su JIT.)

## ⚠️ Errores comunes

- **Creer que 'compilado' siempre es mejor** → causa: ignorar el valor de iterar rápido → solución: elegir según el caso: rendimiento vs. velocidad de desarrollo
- **Pensar que interpretado = sin compilación alguna** → causa: simplificar de más → solución: recordar que muchos interpretan a bytecode internamente

## ❓ Preguntas frecuentes

- **¿Qué es un JIT?** Just-In-Time: compila el código a máquina durante la ejecución, combinando flexibilidad y velocidad (V8, JVM).
- **¿Por qué Java 'tarda en arrancar'?** La JVM debe cargar y calentar (JIT) antes de alcanzar su velocidad máxima.

## 🔗 Referencias

- Documentación de referencia de cada lenguaje del núcleo.

---

> [⏮️ Clase 029](../../parte-2-herramientas-toolchains-y-anatomia-de-comandos/029-que-es-un-toolchain-del-codigo-fuente-al-programa-que-corre/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 031 ⏭️](../../parte-2-herramientas-toolchains-y-anatomia-de-comandos/031-anatomia-de-un-comando-nombre-subcomando-flags-argumentos-y-esquema/README.md)
