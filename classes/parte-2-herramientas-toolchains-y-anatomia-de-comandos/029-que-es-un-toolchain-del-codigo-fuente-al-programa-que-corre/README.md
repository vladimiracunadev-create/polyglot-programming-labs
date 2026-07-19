# Clase 029 — Qué es un toolchain: del código fuente al programa que corre

> Parte **2 — Herramientas, toolchains y anatomía de comandos** · ⏱️ Duración estimada: **75 min** · Nivel: **Fundamentos**
> ✅ **Clase construida.**

---

## 🎯 Objetivo

Entender la cadena de herramientas (toolchain) que convierte el texto que escribes en un programa que se ejecuta: editor, compilador o intérprete, enlazador, gestor de paquetes y runtime. Cada lenguaje tiene su cadena, pero las etapas se repiten. Verlas como un flujo evita tratar los comandos como 'magia'.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Nombrar las etapas típicas de un toolchain.
2. Ubicar dónde encaja cada herramienta (compilador, enlazador, runtime, gestor de paquetes).
3. Explicar por qué un mismo programa necesita pasos distintos en distintos lenguajes.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Fuente → ejecutable | Las etapas entre escribir y ejecutar |
| 2 | Compilador/intérprete | Traduce o ejecuta el código fuente |
| 3 | Enlazador y dependencias | Junta tu código con librerías |
| 4 | Runtime | El entorno donde el programa finalmente corre |

## 📖 Definiciones y características

- **Toolchain** — conjunto de herramientas que llevan el código fuente a un programa ejecutable. Clave: cada lenguaje tiene la suya, con etapas similares.
- **Compilador** — traduce el código fuente a otro lenguaje (máquina o bytecode) antes de ejecutar. Clave: los errores se ven en compilación.
- **Enlazador (linker)** — combina tu código compilado con librerías en un ejecutable. Clave: resuelve referencias a funciones externas.
- **Runtime** — entorno que ejecuta el programa (la CPU directamente, la JVM, Node…). Clave: define qué se necesita para correrlo.

## 🧩 Situación

Un principiante escribe `hola.c`, hace doble clic y no pasa nada. Le falta entender que C debe compilarse y enlazarse antes de existir como programa. Python sí 'se ejecuta al toque' porque su toolchain interpreta. La diferencia está en la cadena.

## 🔎 Ejemplo

La misma meta, dos cadenas distintas:

```text
C (compilado):
  main.c --[compilador]--> main.o --[enlazador]--> ejecutable --> corre

Python (interpretado):
  main.py --[intérprete]--> corre directamente
```

## ✍️ Práctica

Para un lenguaje que uses, enumera qué herramienta interviene en cada etapa (editar, traducir, ejecutar). ¿Compila, interpreta o ambas?

## ⚠️ Errores comunes

- **Tratar los comandos como magia** → causa: no entender qué etapa ejecuta cada uno → solución: mapear cada comando a su etapa del toolchain
- **Esperar que todos los lenguajes se ejecuten igual** → causa: generalizar desde uno → solución: reconocer que compilados e interpretados difieren en la cadena

## ❓ Preguntas frecuentes

- **¿Python no se compila nunca?** Compila a bytecode internamente (.pyc), pero lo hace de forma transparente al ejecutar.
- **¿Por qué tantas etapas en C?** El control fino tiene coste: cada etapa es un punto donde optimizar o fallar.

## 🔗 Referencias

- W. Shotts — *The Linux Command Line* (2ª ed., No Starch Press) — [gratis online](https://linuxcommand.org/tlcl.php).
- B. W. Kernighan y R. Pike — *The Unix Programming Environment* (Prentice Hall).
- A. Hunt y D. Thomas — *The Pragmatic Programmer* (2ª ed., Addison-Wesley).

---

> [⏮️ Clase 028](../../parte-1-atlas-y-genealogia-de-los-lenguajes/028-lenguajes-historicos-y-de-nicho-cobol-fortran-pascal-basic-bash/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 030 ⏭️](../../parte-2-herramientas-toolchains-y-anatomia-de-comandos/030-compilado-vs-interpretado-vs-transpilado-vs-bytecode-vm/README.md)
