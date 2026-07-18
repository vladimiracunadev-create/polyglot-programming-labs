# Clase 036 — REPL e intérpretes interactivos por lenguaje

> Parte **2 — Herramientas, toolchains y anatomía de comandos** · ⏱️ Duración estimada: **75 min** · Nivel: **Fundamentos**
> ✅ **Clase construida.**

---

## 🎯 Objetivo

Descubrir el REPL (Read-Eval-Print Loop): una consola interactiva donde escribes una expresión y ves su resultado al instante, sin crear un archivo ni compilar. Es la herramienta ideal para explorar, probar una idea o entender cómo se comporta un fragmento. Casi todos los lenguajes del núcleo tienen uno.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Explicar qué es un REPL y cuándo usarlo.
2. Abrir el REPL de al menos dos lenguajes del núcleo.
3. Distinguir explorar en el REPL de escribir un programa en un archivo.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Qué es un REPL | Leer, evaluar, imprimir, repetir |
| 2 | Para qué sirve | Explorar y probar sin ceremonia |
| 3 | REPL por lenguaje | python, node, irb, ghci, dotnet fsi… |
| 4 | Sus límites | No sustituye a un archivo para programas reales |

## 📖 Definiciones y características

- **REPL** — consola interactiva que lee una expresión, la evalúa, imprime el resultado y repite. Clave: retroalimentación inmediata.
- **Evaluar** — calcular el valor de una expresión. Clave: en el REPL, cada línea se evalúa y muestra al instante.
- **Sesión interactiva** — el estado que acumula el REPL mientras trabajas. Clave: las variables persisten hasta cerrarlo.
- **Scratch/exploración** — uso del REPL para tantear ideas. Clave: complementa, no reemplaza, el código en archivos.

## 🧩 Situación

¿Qué devuelve `0.1 + 0.2` en JavaScript? En vez de escribir un archivo, abres el REPL de Node, lo tecleas y ves `0.30000000000000004` al instante. El REPL convierte una duda en un experimento de tres segundos.

## 🔎 Ejemplo

Abrir el REPL de cada lenguaje:

```text
Python   python           >>> 2 + 2
Node     node             > 2 + 2
Go       (no oficial; usar 'gore' o el playground)
Ruby     irb              irb> 2 + 2
Haskell  ghci             ghci> 2 + 2
```

## ✍️ Práctica

Abre el REPL de Python o Node y prueba tres expresiones que te generen curiosidad (por ejemplo, mezclar tipos). Observa las respuestas al instante.

## ⚠️ Errores comunes

- **Escribir un programa entero en el REPL** → causa: perder el trabajo al cerrarlo → solución: usar el REPL para explorar; los programas van en archivos
- **Creer que todos tienen REPL nativo** → causa: asumir uniformidad → solución: saber que algunos (Go, C) no lo traen de serie

## ❓ Preguntas frecuentes

- **¿El REPL sirve para depurar?** Para probar fragmentos, sí; para depurar un programa en marcha, se usa un debugger.
- **¿C tiene REPL?** No de forma nativa; existen herramientas experimentales, pero no es habitual.

## 🔗 Referencias

- Documentación de referencia de cada lenguaje del núcleo.

---

> [⏮️ Clase 035](../../parte-2-herramientas-toolchains-y-anatomia-de-comandos/035-paquetes-y-dependencias-pip-pnpm-cargo-maven-gradle-nuget-go-mod-composer/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 037 ⏭️](../../parte-2-herramientas-toolchains-y-anatomia-de-comandos/037-formateadores-y-linters-black-prettier-gofmt-rustfmt-clang-format-php-cs-fixer/README.md)
